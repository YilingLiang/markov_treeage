import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Callable, Tuple

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class State:
    """定义状态或临时状态及其转移规则，包含tunnel机制"""

    def __init__(self, name: str, description: str = "", is_temporary: bool = False,
                 is_absorbing: bool = False,
                 cost_func: Callable[[int, Dict], float] = None,
                 utility_func: Callable[[int, Dict], float] = None,
                 tunnel_cycle: int = None,
                 tunnel_transitions: List[Tuple['State', Callable[[int, Dict], float], Callable[[int, Dict], float], Callable[[int, Dict], float]]] = None):
        """
        初始化状态
        :param name: 状态名称
        :param description: 状态的中文描述
        :param is_temporary: 是否为临时状态
        :param is_absorbing: 是否为吸收态(无法离开的状态)
        :param cost_func: 成本计算函数(周期, 参数)
        :param utility_func: 效用计算函数(周期, 参数)
        :param tunnel_cycle: 触发强制转移的周期数N
        :param tunnel_transitions: 强制转移的规则列表
        """
        self.name = name
        self.description = description
        self.is_temporary = is_temporary
        self.is_absorbing = is_absorbing
        self.cost_func = cost_func if cost_func else lambda c, p: 0
        self.utility_func = utility_func if utility_func else lambda c, p: 0
        self.transitions = []  # 存储默认转移规则

        # Tunnel机制参数
        self.tunnel_cycle = tunnel_cycle  # 触发强制转移的周期数N
        self.tunnel_transitions = tunnel_transitions if tunnel_transitions else []  # 强制转移规则

    def add_transition(self, to_state: 'State',
                       probability_func: Callable[[int, Dict], float],
                       transition_cost_func: Callable[[int, Dict], float] = None,
                       transition_utility_func: Callable[[int, Dict], float] = None,
                       condition: Callable[[int, Dict], bool] = None):
        """
        添加从当前状态到另一个状态的转移规则（含转移动作的成本和效用）
        :param to_state: 目标状态
        :param probability_func: 转移概率函数(周期, 参数)
        :param transition_cost_func: 转移动作的成本函数(周期, 参数)
        :param transition_utility_func: 转移动作的效用函数(周期, 参数)
        :param condition: 转移触发条件(周期, 参数)，默认无条件
        """
        if condition is None:
            condition = lambda c, p: True  # 默认条件始终为真

        # 转移成本和效用默认值为0
        if transition_cost_func is None:
            transition_cost_func = lambda c, p: 0
        if transition_utility_func is None:
            transition_utility_func = lambda c, p: 0

        self.transitions.append({
            "to_state": to_state,
            "probability_func": probability_func,
            "transition_cost_func": transition_cost_func,
            "transition_utility_func": transition_utility_func,
            "condition": condition
        })

    def add_tunnel_transition(self, to_state: 'State',
                              probability_func: Callable[[int, Dict], float],
                              transition_cost_func: Callable[[int, Dict], float] = None,
                              transition_utility_func: Callable[[int, Dict], float] = None,
                              ):
        """
        添加tunnel机制的转移规则（含转移动作的成本和效用）
        :param to_state: 目标状态
        :param probability_func: 转移概率函数(周期, 参数)
        :param transition_cost_func: 转移动作的成本函数(周期, 参数)
        :param transition_utility_func: 转移动作的效用函数(周期, 参数)
        """
        if self.tunnel_cycle is None:
            raise ValueError("非 tunnel 状态不支持设置 tunnel 转移")

        # 转移成本和效用默认值为0
        if transition_cost_func is None:
            transition_cost_func = lambda c, p: 0
        if transition_utility_func is None:
            transition_utility_func = lambda c, p: 0

        self.tunnel_transitions.append((to_state, probability_func, transition_cost_func, transition_utility_func))


class MarkovModel:
    """运行马尔可夫模型并进行成本效用分析，包含tunnel机制和转移成本/效用"""

    def __init__(self, states: List[State], initial_distribution: Dict[str, float]):
        """
        初始化马尔可夫模型
        :param states: 所有状态列表
        :param initial_distribution: 初始状态分布
        """
        self.states = states
        self.initial_distribution = initial_distribution
        self.state_map = {state.name: state for state in states}
        self.state_index = {i: state.name for i, state in enumerate(states)}
        self.non_temporary_states = [s for s in states if not s.is_temporary]

        # 结果存储
        self.results = None

        # 停留时间分布 [周期, 状态索引, 停留时间]
        self.dwell_time_distributions = None

    def _resolve_temporary_state(self, cycle: int, population: float, temp_state: State,
                                 edge_counts: np.ndarray, edge_indices: Dict,
                                 edge_costs: np.ndarray, edge_utilities: np.ndarray,
                                 params: Dict) -> Tuple[float, float, float, float, Dict[str, float]]:
        """
        解析临时状态转移，返回:
        - 临时状态本身的成本
        - 临时状态本身的效用
        - 临时状态转移过程的成本
        - 临时状态转移过程的效用
        - 最终状态及其人口分布
        """
        total_temp_state_cost = 0.0
        total_temp_state_utility = 0.0
        total_temp_transition_cost = 0.0
        total_temp_transition_utility = 0.0
        final_distribution = {}

        # 使用队列处理临时状态转移
        from queue import Queue
        q = Queue()
        q.put((temp_state.name, population, 0))  # (状态名称, 人口数量, 停留时间)

        while not q.empty():
            current_state_name, current_pop, dwell_time = q.get()
            current_state = self.state_map[current_state_name]
            # 计算当前临时状态**停留**产生的成本和效用
            tmp_state_cost = current_state.cost_func(cycle, params)
            tmp_state_utility = current_state.utility_func(cycle, params)
            # 应用折扣（与周期一致）
            discounted_state_cost = discount(tmp_state_cost, params.get("dr", 0), cycle)
            discounted_state_utility = discount(tmp_state_utility, params.get("dr", 0), cycle)
            # 累计状态成本和效用
            total_temp_state_cost += current_pop * discounted_state_cost
            total_temp_state_utility += current_pop * discounted_state_utility

            # 处理转移（含转移动作的成本和效用）
            # 检查是否触发强制转移 (停留时间 >= tunnel_cycle)
            if current_state.tunnel_cycle is not None and dwell_time >= current_state.tunnel_cycle:
                transitions = current_state.tunnel_transitions # 格式：(to_state, prob_func, cost_func, utility_func)
            else:
                # 使用默认转移规则
                transitions = [
                    (transition["to_state"],
                     transition["probability_func"],
                     transition["transition_cost_func"],
                     transition["transition_utility_func"])
                    for transition in current_state.transitions
                    if transition["condition"](cycle + 1, params)
                ]

            # 验证转移概率和为1
            total_prob = sum(prob_func(cycle, params) for _, prob_func, _, _ in transitions)
            if not np.isclose(total_prob, 1.0, atol=1e-8):
                raise ValueError(f"周期{cycle}，临时状态{current_state_name}转移概率和为{total_prob}，应等于1")

            # 处理每个适用的转移
            for to_state, prob_func, trans_cost_func, trans_utility_func in transitions:
                prob = prob_func(cycle, params)
                transferred_pop = current_pop * prob  # 转移的人口数量

                # 记录边转移数量
                edge_id = edge_indices[(current_state_name, to_state.name)]
                edge_counts[cycle - 1, edge_id] += transferred_pop

                # 3. 计算**转移动作**的成本和效用
                trans_cost = trans_cost_func(cycle, params)  # 转移动作本身的成本（如住院费）
                trans_utility = trans_utility_func(cycle, params)  # 转移动作本身的效用（如治疗效果）
                # 应用折扣
                discounted_trans_cost = discount(trans_cost, params.get("dr", 0), cycle)
                discounted_trans_utility = discount(trans_utility, params.get("dr", 0), cycle)
                # 累计转移成本和效用
                total_temp_transition_cost += transferred_pop * discounted_trans_cost
                total_temp_transition_utility += transferred_pop * discounted_trans_utility
                # 记录到边成本和效用数组
                edge_costs[cycle - 1, edge_id] += transferred_pop * discounted_trans_cost
                edge_utilities[cycle - 1, edge_id] += transferred_pop * discounted_trans_utility

                # 4. 处理目标状态
                if to_state.is_temporary:
                    # 如果目标仍然是临时状态，加入队列继续处理，停留时间重置为0
                    q.put((to_state.name, transferred_pop, 0))
                else:
                    # 到达非临时状态，记录最终分布
                    if to_state.name in final_distribution:
                        final_distribution[to_state.name] += transferred_pop
                    else:
                        final_distribution[to_state.name] = transferred_pop

        # 总临时成本 = 状态停留成本 + 转移动作成本
        total_temp_cost = total_temp_state_cost + total_temp_transition_cost
        # 总临时效用 = 状态停留效用 + 转移动作效用
        total_temp_utility = total_temp_state_utility + total_temp_transition_utility
        return total_temp_cost, total_temp_utility, total_temp_transition_cost, total_temp_transition_utility, final_distribution

    def run(self, cycles: int, params: Dict, cohort: bool = False) -> None:
        """
        运行模型
        :param cycles: 模拟周期数
        :param params: 模型参数
        :param cohort: 是否进行队列模拟
        """
        # 初始化状态分布 [周期, 状态索引]
        num_states = len(self.states)
        state_counts = np.zeros((cycles + 1, num_states))
        for state_name, prob in self.initial_distribution.items():
            state_counts[0, self._get_state_index(state_name)] = prob

        # 初始化停留时间分布 [周期, 状态索引, 停留时间]
        max_dwell = max((s.tunnel_cycle for s in self.states if s.tunnel_cycle is not None), default=0)
        self.dwell_time_distributions = []

        # 初始停留时间分布：所有状态停留时间都是0
        initial_dwell = np.zeros((num_states, max_dwell + 1))
        for state_idx, state in enumerate(self.states):
            initial_dwell[state_idx, 0] = state_counts[0, state_idx]
        self.dwell_time_distributions.append(initial_dwell)

        # 初始化边转移计数 [周期, 边ID]
        edges = [(s.name, t["to_state"].name) for s in self.states for t in s.transitions]
        edges += [(s.name, t[0].name) for s in self.states for t in s.tunnel_transitions]
        edge_indices = {(s, t): i for i, (s, t) in enumerate(edges)}
        edge_counts = np.zeros((cycles, len(edges)))  # 每个周期每条边的转移人口

        # 记录每条边的转移成本和效用
        edge_costs = np.zeros((cycles, len(edges)))  # 每个周期每条边的转移成本
        edge_utilities = np.zeros((cycles, len(edges)))  # 每个周期每条边的转移效用

        # 存储每个周期的总成本和效用（含状态停留和转移动作）
        stage_total_costs = []
        stage_total_utilities = []
        # 细分：每个周期的状态停留成本、转移动作成本
        stage_state_costs = []  # 状态停留成本
        stage_transition_costs = []  # 转移动作成本
        stage_state_utilities = []  # 状态停留效用
        stage_transition_utilities = []  # 转移动作效用

        # 累计总指标
        total_state_cost = 0.0  # 所有状态停留的总成本
        total_transition_cost = 0.0  # 所有转移动作的总成本
        total_state_utility = 0.0  # 所有状态停留的总效用
        total_transition_utility = 0.0  # 所有转移动作的总效用

        for t in range(cycles):
            current_dwell = self.dwell_time_distributions[t] # 当前周期的停留时间分布

            # 初始化下一周期状态分布和停留时间分布
            next_state = np.zeros(num_states)
            next_dwell = np.zeros((num_states, max_dwell + 1))

            # 本周期的临时变量
            cycle_state_cost = 0.0  # 非临时状态的停留成本
            cycle_state_utility = 0.0  # 非临时状态的停留效用
            cycle_transition_cost = 0.0  # 非临时状态的转移动作成本
            cycle_transition_utility = 0.0  # 非临时状态的转移动作效用

            # 记录每个状态的转移情况
            state_transitions = {s.name: [] for s in self.states}

            # 处理每个状态的转移
            for state_idx, from_state in enumerate(self.states):
                state_name = from_state.name
                max_stay = from_state.tunnel_cycle if from_state.tunnel_cycle is not None else max_dwell

                # 处理该状态下不同停留时间的个体
                for dwell_time in range(max_stay + 1):
                    # 当前停留时间的个体数量
                    population = current_dwell[state_idx, dwell_time]
                    if population <= 0:
                        continue

                    if not from_state.is_temporary and not from_state.is_absorbing:
                        # 当前状态的成本和效用（状态本身）
                        cost = from_state.cost_func(t, params)
                        utility = from_state.utility_func(t, params)

                        # 应用折扣
                        discounted_cost = discount(cost, params.get("dr", 0), t)
                        discounted_utility = discount(utility, params.get("dr", 0), t)

                        # 累计状态本身的成本和效用
                        cycle_state_cost += population * discounted_cost
                        cycle_state_utility += population * discounted_utility

                        # print("============", population, cycle_state_cost, cycle_state_utility)
                    # 如果是吸收态，直接转移到下一周期
                    if from_state.is_absorbing:
                        next_state[state_idx] += population
                        next_dwell[state_idx, min(dwell_time + 1, max_stay)] += population

                        continue

                    # 检查是否触发 tunnel 需要强制转移 (停留时间 >= tunnel_cycle)
                    if from_state.tunnel_cycle is not None and dwell_time >= from_state.tunnel_cycle:
                        applicable_transitions = [
                            transition for transition in from_state.tunnel_transitions
                        ]

                        # 计算总概率
                        total_prob = sum(tran[1](t, params)
                                         for tran in applicable_transitions)

                        # 确保总概率为1
                        if not np.isclose(total_prob, 1.0, atol=1e-8):
                            raise ValueError(f"周期{t}，状态{state_name}强制转移概率和为{total_prob}，应等于1")

                        # 使用强制转移规则
                        for to_state, prob_func, trans_cost_func, trans_utility_func in from_state.tunnel_transitions:
                            prob = prob_func(t, params)
                            transferred_pop = population * prob

                            # 记录边转移数量
                            edge_id = edge_indices[(from_state.name, to_state.name)]
                            edge_counts[t, edge_id] += transferred_pop

                            # 计算转移过程的成本和效用
                            trans_cost = trans_cost_func(t, params)
                            trans_utility = trans_utility_func(t, params)

                            # 应用折扣
                            discounted_trans_cost = discount(trans_cost, params.get("dr", 0), t)
                            discounted_trans_utility = discount(trans_utility, params.get("dr", 0), t)

                            # 累计转移成本和效用
                            trans_total_cost = transferred_pop * discounted_trans_cost
                            trans_total_util = transferred_pop * discounted_trans_utility
                            cycle_transition_cost += trans_total_cost
                            cycle_transition_utility += trans_total_util

                            # 记录边的成本和效用
                            edge_costs[t, edge_id] += trans_total_cost
                            edge_utilities[t, edge_id] += trans_total_util

                            # 处理临时状态的转移
                            if to_state.is_temporary:
                                print("这个如果被打印，说明出错？")
                                # 解析临时状态转移，获取临时状态的成本、效用和最终分布
                                temp_total_cost, temp_total_utility, temp_trans_cost, temp_trans_utility, final_states = self._resolve_temporary_state(
                                    t, transferred_pop, to_state, edge_counts, edge_indices, edge_costs, edge_utilities, params)
                                # print(f"临时成本与效用：{temp_total_cost}, {temp_total_utility}, {temp_trans_cost}, {temp_trans_utility}")
                                # 累计临时状态的成本和效用
                                cycle_state_cost += (temp_total_cost - temp_trans_cost)  # 临时状态停留成本
                                cycle_state_utility += (temp_total_utility - temp_trans_utility)  # 临时状态停留效用
                                cycle_transition_cost += temp_trans_cost  # 临时转移动作成本
                                cycle_transition_utility += temp_trans_utility  # 临时转移动作效用

                                # 更新最终状态分布
                                for final_state_name, pop in final_states.items():
                                    final_state = self.state_map[final_state_name]
                                    final_idx = self._get_state_index(final_state_name)

                                    if final_state.name == from_state.name:
                                        # 转移到自身，停留时间加1
                                        new_dwell = min(dwell_time + 1, max_stay)
                                        next_state[final_idx] += pop
                                        next_dwell[final_idx, new_dwell] += pop
                                    else:
                                        # 转移到其他状态，停留时间重置为0
                                        next_state[final_idx] += pop
                                        next_dwell[final_idx, 0] += pop  # 新状态停留时间为0
                            else:
                                # 直接转移到非临时状态
                                to_idx = self._get_state_index(to_state.name)

                                if to_state.name == from_state.name:
                                    # 转移到自身，停留时间加1
                                    new_dwell = min(dwell_time + 1, max_stay)
                                    next_state[to_idx] += transferred_pop
                                    next_dwell[to_idx, new_dwell] += transferred_pop
                                else:
                                    # 转移到其他状态，停留时间重置为0
                                    next_state[to_idx] += transferred_pop
                                    next_dwell[to_idx, 0] += transferred_pop
                    else:
                        # 使用默认转移规则
                        applicable_transitions = [
                            transition for transition in from_state.transitions
                            if transition["condition"](t + 1, params)
                               and not from_state.is_temporary # 新增，因转移一定是非临时状态开始的，不过加不加应该效果一样，因为临时一定转移到非临时，这样它计数在每轮开始都是0
                        ]

                        # 计算总概率
                        total_prob = sum(tran["probability_func"](t, params)
                                         for tran in applicable_transitions)

                        # 确保总概率为1
                        if not np.isclose(total_prob, 1.0, atol=1e-8):
                            raise ValueError(f"周期{t}，状态{state_name}转移概率和为{total_prob}，应等于1")

                        # 处理每个适用的转移
                        for transition in applicable_transitions:
                            to_state = transition["to_state"]
                            prob = transition["probability_func"](t, params)
                            transferred_pop = population * prob

                            # 记录边转移数量
                            edge_id = edge_indices[(from_state.name, to_state.name)]
                            edge_counts[t, edge_id] += transferred_pop

                            # 计算转移动作的成本和效用（如从健康到患病的诊断费）
                            trans_cost = transition["transition_cost_func"](t, params)
                            trans_utility = transition["transition_utility_func"](t, params)
                            discounted_trans_cost = discount(trans_cost, params.get("dr", 0), t)
                            discounted_trans_utility = discount(trans_utility, params.get("dr", 0), t)

                            # 累计转移动作成本和效用
                            cycle_transition_cost += transferred_pop * discounted_trans_cost
                            cycle_transition_utility += transferred_pop * discounted_trans_utility
                            edge_costs[t, edge_id] += transferred_pop * discounted_trans_cost
                            edge_utilities[t, edge_id] += transferred_pop * discounted_trans_utility

                            if to_state.is_temporary:
                                # 计算临时状态的成本和效用
                                temp_total_cost, temp_total_utility, temp_trans_cost, temp_trans_utility, final_states = self._resolve_temporary_state(
                                    t, transferred_pop, to_state, edge_counts, edge_indices, edge_costs, edge_utilities, params)
                                # print(f"2临时成本与效用：{temp_total_cost}, {temp_total_utility}, {temp_trans_cost}, {temp_trans_utility}")
                                # 累计临时状态的成本和效用
                                cycle_state_cost += (temp_total_cost - temp_trans_cost)  # 临时状态停留成本
                                cycle_state_utility += (temp_total_utility - temp_trans_utility)  # 临时状态停留效用
                                cycle_transition_cost += temp_trans_cost  # 临时转移动作成本
                                cycle_transition_utility += temp_trans_utility  # 临时转移动作效用

                                # 更新最终状态分布
                                for final_state_name, pop in final_states.items():
                                    final_state = self.state_map[final_state_name]
                                    final_idx = self._get_state_index(final_state_name)

                                    if final_state.name == from_state.name:
                                        # print("转移终态与初态一致", to_state.name, final_state.name, from_state.name)
                                        # 转移到自身，停留时间加1
                                        new_dwell = min(dwell_time + 1, max_stay)
                                        next_state[final_idx] += pop
                                        next_dwell[final_idx, new_dwell] += pop
                                    else:
                                        next_state[final_idx] += pop
                                        next_dwell[final_idx, 0] += pop  # 新状态停留时间为0

                            else:
                                # 目标状态索引
                                to_idx = self._get_state_index(to_state.name)

                                # 记录状态转移
                                state_transitions[from_state.name].append((to_state.name, prob))

                                if to_state.name == from_state.name:
                                    # 转移到自身，停留时间加1
                                    new_dwell = min(dwell_time + 1, max_stay)
                                    next_state[to_idx] += transferred_pop
                                    next_dwell[to_idx, new_dwell] += transferred_pop
                                else:
                                    # 转移到其他状态，停留时间重置为0
                                    next_state[to_idx] += transferred_pop
                                    next_dwell[to_idx, 0] += transferred_pop

            # 验证状态分布总和
            if not cohort:
                if not np.isclose(np.sum(next_state), np.sum(state_counts[t]), atol=1e-6):
                    raise ValueError(
                        f"在周期{t}，状态概率总和不守恒: {np.sum(next_state)} vs {np.sum(state_counts[t])}")

            # 更新状态分布
            state_counts[t + 1] = next_state
            self.dwell_time_distributions.append(next_dwell)

            # 累计本周期指标
            stage_state_costs.append(cycle_state_cost)
            stage_transition_costs.append(cycle_transition_cost)
            stage_state_utilities.append(cycle_state_utility)
            stage_transition_utilities.append(cycle_transition_utility)

            total_state_cost += cycle_state_cost
            total_transition_cost += cycle_transition_cost
            total_state_utility += cycle_state_utility
            total_transition_utility += cycle_transition_utility

        # 计算最终状态（最后一个周期结束时）的成本和效用
        final_dwell = self.dwell_time_distributions[-1]
        final_state_cost = 0.0
        final_state_utility = 0.0

        for state_idx, state in enumerate(self.states):
            max_stay = state.tunnel_cycle if state.tunnel_cycle is not None else max_dwell
            for dwell_time in range(max_stay + 1):
                pop = final_dwell[state_idx, dwell_time]
                if pop <= 0:
                    continue

                # 最终状态的成本和效用（使用最后一个周期数作为计算依据）
                cost = state.cost_func(cycles, params)
                utility = state.utility_func(cycles, params)

                # 应用折扣（周期数为总周期数）
                discounted_cost = discount(cost, params.get("dr", 0), cycles)
                discounted_utility = discount(utility, params.get("dr", 0), cycles)

                final_state_cost += pop * discounted_cost
                final_state_utility += pop * discounted_utility

        # print(f"final_state_cost: {final_state_cost}, final_state_utility: {final_state_utility}")
        # 汇总最终指标
        total_state_cost += final_state_cost
        total_state_utility += final_state_utility
        total_cost = total_state_cost + total_transition_cost
        total_utility = total_state_utility + total_transition_utility

        # 存储结果
        self.results = {
            # 状态分布
            "state_counts": state_counts,
            "dwell_time_distributions": self.dwell_time_distributions,
            # 成本指标
            "total_cost": total_cost,
            "total_state_cost": total_state_cost,
            "total_transition_cost": total_transition_cost,
            "stage_state_costs": stage_state_costs + [final_state_cost],
            "stage_transition_costs": stage_transition_costs,
            # 效用指标
            "total_utility": total_utility,
            "total_state_utility": total_state_utility,
            "total_transition_utility": total_transition_utility,
            "stage_state_utilities": stage_state_utilities + [final_state_utility],
            "stage_transition_utilities": stage_transition_utilities,
            # 边转移详情
            "edge_counts": edge_counts,
            "edge_costs": edge_costs,
            "edge_utilities": edge_utilities,
            "edge_indices": edge_indices
        }

    def _get_state_index(self, state_name: str) -> int:
        """获取状态的索引"""
        return list(self.state_map.keys()).index(state_name)

    def get_dwell_time_distribution(self, state_name: str, cycle: int) -> np.ndarray:
        """获取指定状态在指定周期的停留时间分布"""
        state_idx = self._get_state_index(state_name)
        state = self.state_map[state_name]
        max_stay = state.tunnel_cycle if state.tunnel_cycle is not None else len(
            self.dwell_time_distributions[0][state_idx]) - 1
        return self.dwell_time_distributions[cycle][state_idx, :max_stay + 1]

    def get_edge_transitions(self, from_state: str, to_state: str) -> np.ndarray:
        """获取两状态间所有周期的转移数量（边的转移）"""
        if (from_state, to_state) not in self.results["edge_indices"]:
            return np.zeros(len(self.results["edge_counts"]))

        edge_id = self.results["edge_indices"][(from_state, to_state)]
        return self.results["edge_counts"][:, edge_id]

    def get_edge_metrics(self, from_state: str, to_state: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """获取两状态间转移的数量、成本、效用随周期的变化"""
        if (from_state, to_state) not in self.results["edge_indices"]:
            return np.zeros_like(self.results["edge_counts"][:, 0]), \
                np.zeros_like(self.results["edge_costs"][:, 0]), \
                np.zeros_like(self.results["edge_utilities"][:, 0])

        edge_id = self.results["edge_indices"][(from_state, to_state)]
        return (self.results["edge_counts"][:, edge_id],
                self.results["edge_costs"][:, edge_id],
                self.results["edge_utilities"][:, edge_id])

    def get_cumulative_edge_transitions(self, from_state: str, to_state: str) -> float:
        """获取两状态间的累积转移数量（边的累积转移）"""
        return self.get_edge_transitions(from_state, to_state).sum()

    def get_cumulative_edge_metrics(self, from_state: str, to_state: str) -> Tuple[float, float, float]:
        """获取两状态间转移的累计数量、成本、效用"""
        counts, costs, utilities = self.get_edge_metrics(from_state, to_state)
        return counts.sum(), costs.sum(), utilities.sum()

# 辅助函数：计算折扣值
def discount(value: float, rate: float, cycle: int) -> float:
    """计算折扣后的值"""
    return value / ((1 + rate) ** cycle)


if __name__ == "__main__":
    # 创建状态
    death = State(
        name="Death",
        description="死亡状态",
        is_absorbing=True,
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: 0
    )

    disease = State(
        name="Disease",
        description="患病状态",
        cost_func=lambda cycle, p: 2000,
        utility_func=lambda cycle, p: 0.7,
        # --- 定义 Tunnel ---
        # tunnel_cycle=2,  # 停留2个周期后强制转移
        # tunnel_transitions=[(death, lambda cycle, p: 1.0)]  # 强制转移到死亡
    )

    healthy = State(
        name="Healthy",
        description="健康状态",
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: 1.0,
        # --- 定义 Tunnel ---
        # 注意这里因数组下标和TreeAge的区别，TreeAge中初始停留周期数是 1 ，我们这里是 0，所以这里等价于TreeAge中的 _tunnel < 5
        tunnel_cycle=4,  # 停留 tunnel_cycle 个周期后强制转移
        tunnel_transitions=[(death, lambda cycle, p: 0.2, lambda cycle, p: 0.2, lambda cycle, p: 0.2), (disease, lambda cycle, p: 0.8, lambda cycle, p: 0.2, lambda cycle, p: 0.2)]  # 强制转移的情况
    )

    # 添加正常转移规则
    healthy.add_transition(healthy, lambda c, p: 0.9)
    healthy.add_transition(disease, lambda c, p: 0.09)  # 每年9%概率患病
    healthy.add_transition(death, lambda c, p: 0.01)  # 每年1%概率死亡

    disease.add_transition(disease, lambda c, p: 0.7)
    disease.add_transition(healthy, lambda c, p: 0.1)  # 每年10%概率康复
    disease.add_transition(death, lambda c, p: 0.2)  # 每年20%概率死亡

    # 创建模型
    model = MarkovModel([healthy, disease, death], {"Healthy": 1.0})
    model.run(10, {"dr": 0.00})

    # 分析结果
    print(f"总成本: {model.results['total_cost']:.2f}")
    print(f"总效用: {model.results['total_utility']:.2f}")

    # 查看特定边的累积转移
    print(f"从健康到死亡的累积转移: {model.get_cumulative_edge_transitions('Healthy', 'Death'):.2f}")
    print(f"从疾病到死亡的累积转移: {model.get_cumulative_edge_transitions('Disease', 'Death'):.2f}")
    print(f"最终状态分布: {model.results['state_counts'][-1]}")
    print(f"每个时间步状态分布: {model.results['state_counts']}")

    # 查看停留时间分布
    print("\n健康状态的停留时间分布:")
    for t in range(5):
        dist = model.get_dwell_time_distribution('Healthy', t)
        print(f"周期 {t}: {[f'{x:.4f}' for x in dist]}")

    print("\n疾病状态的停留时间分布:")
    for t in range(5):
        dist = model.get_dwell_time_distribution('Disease', t)
        print(f"周期 {t}: {[f'{x:.4f}' for x in dist]}")

    # 可视化状态分布随时间的变化
    plt.figure(figsize=(12, 6))
    time_points = range(11)
    for state in model.non_temporary_states:
        idx = model._get_state_index(state.name)
        plt.plot(time_points, model.results["state_counts"][:, idx], label=f"{state.name} ({state.description})")
    plt.xlabel("周期")
    plt.ylabel("比例")
    plt.title("状态分布随时间的变化")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 可视化健康状态的停留时间分布
    plt.figure(figsize=(12, 6))
    healthy_idx = model._get_state_index('Healthy')
    max_dwell = healthy.tunnel_cycle if healthy.tunnel_cycle is not None else 0
    for dwell_time in range(max_dwell + 1):
        dwell_dist = [model.dwell_time_distributions[t][healthy_idx, dwell_time] for t in range(11)]
        plt.plot(time_points, dwell_dist, label=f"停留{dwell_time}周期")
    plt.xlabel("周期")
    plt.ylabel("比例")
    plt.title("健康状态的停留时间分布")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 可视化疾病状态的停留时间分布
    plt.figure(figsize=(12, 6))
    disease_idx = model._get_state_index('Disease')
    max_dwell = disease.tunnel_cycle if disease.tunnel_cycle is not None else 0
    for dwell_time in range(max_dwell + 1):
        dwell_dist = [model.dwell_time_distributions[t][disease_idx, dwell_time] for t in range(11)]
        plt.plot(time_points, dwell_dist, label=f"停留{dwell_time}周期")
    plt.xlabel("周期")
    plt.ylabel("比例")
    plt.title("疾病状态的停留时间分布")
    plt.legend()
    plt.grid(True)
    plt.show()