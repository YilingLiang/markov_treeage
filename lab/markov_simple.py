import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Callable, Tuple

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class State:
    """Define states or temporary states and their transition rules"""

    def __init__(self,
                 name: str,
                 description: str = "",
                 is_temporary: bool = False,
                 is_absorbing: bool = False
                 ):
        """
        初始化状态
        :param name: 状态名称
        :param description: 状态的中文描述
        :param is_temporary: 是否为临时状态
        :param is_absorbing: 是否为吸收态(无法离开的状态)
        """
        self.name = name
        self.description = description
        self.is_temporary = is_temporary
        self.is_absorbing = is_absorbing
        self.transitions = []  # 存储默认转移规则

    def add_transition(self, to_state: 'State',
                       probability_func: Callable[[int, Dict], float],
                       condition: Callable[[int, Dict], bool] = None):
        """
        添加从当前状态到另一个状态的转移规则（含转移动作的成本和效用）
        :param to_state: 目标状态
        :param probability_func: 转移概率函数(周期, 参数)
        :param condition: 转移触发条件(周期, 参数)，默认无条件
        """
        if condition is None:
            condition = lambda c, p: True  # 默认条件始终为真

        self.transitions.append({
            "to_state": to_state,
            "probability_func": probability_func,
            "condition": condition
        })


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
                                 params: Dict) -> Dict[str, float]:
        """
        解析临时状态转移，返回:
        - 最终状态及其人口分布
        """
        final_distribution = {}

        # 使用队列处理临时状态转移
        from queue import Queue
        q = Queue()
        q.put((temp_state.name, population, 0))  # (状态名称, 人口数量, 停留时间)

        while not q.empty():
            current_state_name, current_pop, dwell_time = q.get()
            current_state = self.state_map[current_state_name]

            # 2. 处理转移（含转移动作的成本和效用）
            # 使用默认转移规则
            transitions = [
                (transition["to_state"],
                 transition["probability_func"])
                for transition in current_state.transitions
                if transition["condition"](cycle, params)
            ]

            # 验证转移概率和为1
            total_prob = sum(prob_func(cycle, params) for _, prob_func, in transitions)
            if not np.isclose(total_prob, 1.0, atol=1e-8):
                raise ValueError(f"周期{cycle}，临时状态{current_state_name}转移概率和为{total_prob}，应等于1")

            # 处理每个适用的转移
            for to_state, prob_func in transitions:
                prob = prob_func(cycle, params)
                transferred_pop = current_pop * prob  # 转移的人口数量

                # 记录边转移数量
                edge_id = edge_indices[(current_state_name, to_state.name)]
                edge_counts[cycle - 1, edge_id] += transferred_pop

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

        return final_distribution

    def run(self, cycles: int, params: Dict) -> None:
        """
        运行模型
        :param cycles: 模拟周期数
        :param params: 模型参数
        """
        # 初始化状态分布 [周期, 状态索引]
        num_states = len(self.states)
        state_counts = np.zeros((cycles + 1, num_states))
        for state_name, prob in self.initial_distribution.items():
            state_counts[0, self._get_state_index(state_name)] = prob

        # 初始化停留时间分布 [周期, 状态索引, 停留时间]
        max_dwell = 0
        self.dwell_time_distributions = []

        # 初始停留时间分布：所有状态停留时间都是0
        initial_dwell = np.zeros((num_states, max_dwell + 1))
        for state_idx, state in enumerate(self.states):
            initial_dwell[state_idx, 0] = state_counts[0, state_idx]
        self.dwell_time_distributions.append(initial_dwell)

        # 初始化边转移计数 [周期, 边ID]
        edges = [(s.name, t["to_state"].name) for s in self.states for t in s.transitions]
        edge_indices = {(s, t): i for i, (s, t) in enumerate(edges)}
        edge_counts = np.zeros((cycles, len(edges)))  # 每个周期每条边的转移人口

        for t in range(cycles):
            current_dwell = self.dwell_time_distributions[t] # 当前周期的停留时间分布

            # 初始化下一周期状态分布和停留时间分布
            next_state = np.zeros(num_states)
            next_dwell = np.zeros((num_states, max_dwell + 1))

            # 记录每个状态的转移情况
            state_transitions = {s.name: [] for s in self.states}

            # 处理每个状态的转移
            for state_idx, from_state in enumerate(self.states):
                state_name = from_state.name
                max_stay = max_dwell

                # 处理该状态下不同停留时间的个体
                for dwell_time in range(max_stay + 1):
                    # 当前停留时间的个体数量
                    population = current_dwell[state_idx, dwell_time]
                    if population <= 0:
                        continue

                    # 如果是吸收态，直接转移到下一周期
                    if from_state.is_absorbing:
                        next_state[state_idx] += population
                        next_dwell[state_idx, min(dwell_time + 1, max_stay)] += population
                        continue

                    # 使用默认转移规则
                    applicable_transitions = [
                        transition for transition in from_state.transitions
                        if transition["condition"](t + 1, params)
                           and not from_state.is_temporary # 新增，因转移一定是非临时状态开始的，不过加不加应该效果一样，因为临时一定转移到非临时，这样它计数在每轮开始都是0
                    ]

                    # 计算总概率
                    total_prob = sum(tran["probability_func"](t + 1, params)
                                     for tran in applicable_transitions)

                    # 确保总概率为1
                    if not np.isclose(total_prob, 1.0, atol=1e-8):
                        raise ValueError(f"周期{t + 1}，状态{state_name}转移概率和为{total_prob}，应等于1")

                    # 处理每个适用的转移
                    for transition in applicable_transitions:
                        to_state = transition["to_state"]
                        prob = transition["probability_func"](t, params)
                        transferred_pop = population * prob

                        # 记录边转移数量
                        edge_id = edge_indices[(from_state.name, to_state.name)]
                        edge_counts[t, edge_id] += transferred_pop

                        if to_state.is_temporary:
                            # 计算临时状态的最终
                            final_states = self._resolve_temporary_state(
                                t, transferred_pop, to_state, edge_counts, edge_indices, params)

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

            # 更新状态分布
            state_counts[t + 1] = next_state
            self.dwell_time_distributions.append(next_dwell)

        # 存储结果
        self.results = {
            # 状态分布
            "state_counts": state_counts,
            "dwell_time_distributions": self.dwell_time_distributions,
            # 边转移详情
            "edge_counts": edge_counts,
            "edge_indices": edge_indices
        }

    def _get_state_index(self, state_name: str) -> int:
        """获取状态的索引"""
        return list(self.state_map.keys()).index(state_name)


if __name__ == "__main__":
    pass
