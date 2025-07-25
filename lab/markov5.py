"""
我写的markov进行成本效用分析的代码，定义State类：
1. 这个类中可以定义一个状态以及该状态的中文描述，以及状态类型是否是临时状态或吸收态，临时态一定会在当前时间步继续转移；
2. 可以定义这个状态能转移到的状态，和相应的概率，还有状态的成本和效用；
3. 可以定义状态转移依据布尔条件触发，如当"45<模型时间<50"走一条路，其他情况走另一条路
4. 状态转移并非只有一条边，里面有"临时状态"，注意临时状态是不稳定状态，在每个模型时间步转移中一定是以状态开始到状态结束，也就是在转移的每个时间步如果遇到"临时状态"，需要继续往后运算直到另一个状态截至；
(实际上State是一个多条边的计算图，它是一个状态到另一个状态，但是状态到状态的中间过程可以很复杂，并非只有一条边。)
此外，定义Markov类可以根据多个State组成的计算图来模拟离散马尔科夫模型，并计算成本和效用进行成本效用分析，还有个能记录在每个时间步，每个计算图上的边发生转移的数量到底是多少。
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Callable
import networkx as nx  # 用于处理状态转移图

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class State:
    """定义状态或临时状态及其转移规则"""

    def __init__(self, name: str, description: str = "", is_temporary: bool = False,
                 is_absorbing: bool = False,
                 cost_func: Callable[[int, Dict], float] = None,
                 utility_func: Callable[[int, Dict], float] = None):
        """
        初始化状态
        :param name: 状态名称
        :param description: 状态的中文描述
        :param is_temporary: 是否为临时状态
        :param is_absorbing: 是否为吸收态(无法离开的状态)
        :param cost_func: 成本计算函数(周期, 状态时间, 参数)
        :param utility_func: 效用计算函数(周期, 状态时间, 参数)
        """
        self.name = name
        self.description = description
        self.is_temporary = is_temporary
        self.is_absorbing = is_absorbing
        self.cost_func = cost_func if cost_func else lambda c, p: 0
        self.utility_func = utility_func if utility_func else lambda c, p: 0
        self.transitions = []  # 存储转移规则

    def add_transition(self, to_state: 'State', probability_func: Callable[[int, Dict], float],
                       condition: Callable[[int, Dict], bool] = None):
        """
        添加从当前状态到另一个状态的转移规则
        :param to_state: 目标状态
        :param probability_func: 转移概率函数(周期, 状态时间, 参数)
        :param condition: 转移触发条件(周期, 状态时间, 参数)，默认无条件
        """
        if condition is None:
            condition = lambda c, p: True  # 默认条件始终为真

        self.transitions.append({
            "to_state": to_state,
            "probability_func": probability_func,
            "condition": condition
        })


class MarkovModel:
    """运行马尔可夫模型并进行成本效用分析"""

    def __init__(self, states: List[State], initial_distribution: Dict[str, float]):
        """
        初始化马尔可夫模型
        :param states: 所有状态列表
        :param initial_distribution: 初始状态分布
        """
        self.states = states
        self.initial_distribution = initial_distribution
        self.state_map = {state.name: state for state in states}
        self.non_temporary_states = [s for s in states if not s.is_temporary]

        # 结果存储
        self.results = None

    def run(self, cycles: int, params: Dict, cohort: bool=False) -> None:
        """
        运行模型
        :param cycles: 模拟周期数
        :param params: 模型参数
        :param cohort: 是否进行队列模拟
        """
        # 初始化状态分布
        state_counts = np.zeros((cycles + 1, len(self.states)))
        # 存每个时间步新增的成本和效用
        stage_utilities = []
        stage_costs = []
        for state_name, prob in self.initial_distribution.items():
            state_counts[0, self._get_state_index(state_name)] = prob

        # 初始化边转移计数 [周期, 边ID]
        edges = [(s.name, t["to_state"].name) for s in self.states for t in s.transitions]
        edge_indices = {(s, t): i for i, (s, t) in enumerate(edges)}
        edge_counts = np.zeros((cycles, len(edges)))

        # 累计成本和效用
        total_cost = 0.0
        total_utility = 0.0

        for t in range(cycles):
            # 更新各状态持续时间
            current_state = state_counts[t].copy()

            # 初始化下一周期状态分布
            next_state = np.zeros(len(self.states))

            # 记录每个状态的转移情况
            state_transitions = {s.name: [] for s in self.states}

            # 处理每个状态的转移
            for from_state in self.states:
                from_idx = self._get_state_index(from_state.name)
                population = current_state[from_idx]

                # 如果当前状态没有人口或是吸收态，直接跳过
                if population <= 0 or from_state.is_absorbing:
                    next_state[from_idx] += population
                    continue

                # 处理该状态的所有转移规则
                applicable_transitions = [
                    transition for transition in from_state.transitions
                    if transition["condition"](t + 1, params)
                ]

                # 计算总概率
                total_prob = sum(tran["probability_func"](t + 1, params)
                                 for tran in applicable_transitions)

                # 确保总概率不超过1
                if total_prob > 1 + 1e-8:  # 允许小的浮点误差
                    raise ValueError(f"在周期{t + 1}，状态{from_state.name}的总转移概率{total_prob}超过1")

                # 如果总概率小于1，剩余概率留在当前状态（仅对非临时状态）
                if not from_state.is_temporary and total_prob < 1 - 1e-8:
                    print(f"{from_state.name} 的转移概率和{total_prob}小于 1, 已自动处理")
                    stay_prob = 1 - total_prob
                    next_state[from_idx] += population * stay_prob
                    state_transitions[from_state.name].append((from_state.name, stay_prob))

                # 处理每个适用的转移
                for transition in applicable_transitions:
                    to_state = transition["to_state"]
                    prob = transition["probability_func"](t + 1, params)

                    # 记录边转移数量
                    edge_id = edge_indices[(from_state.name, to_state.name)]
                    edge_counts[t, edge_id] += population * prob

                    # 记录状态转移
                    state_transitions[from_state.name].append((to_state.name, prob))

                    # 处理转移
                    transferred_pop = population * prob

                    # 如果目标是临时状态，需要继续转移直到到达非临时状态
                    if to_state.is_temporary:
                        final_states = self._resolve_temporary_state(t, transferred_pop, to_state,
                                                                     edge_counts, edge_indices, params)
                        for final_state, pop in final_states.items():
                            final_idx = self._get_state_index(final_state)
                            next_state[final_idx] += pop
                    else:
                        # 直接转移到非临时状态
                        to_idx = self._get_state_index(to_state.name)
                        next_state[to_idx] += transferred_pop

            # 更新状态分布
            state_counts[t + 1] = next_state

            if not cohort:
                # 如果是概率模拟则验证概率和一定小于1(吸收态的存在)，否则是队列模拟
                if abs(sum(next_state) - 1) > 1e-6:
                    raise ValueError(f"在周期{t + 1}，状态概率总和超过1: {sum(next_state)}")

            # 计算当前周期的成本和效用
            cur_state = current_state
            cycle_cost = 0.0
            cycle_utility = 0.0
            # 用于非半周期矫正能正确存储
            last_cost = 0.0
            last_utility = 0.0

            for i, state in enumerate(self.non_temporary_states):
                idx = self._get_state_index(state.name)
                if cur_state[idx] == 0:
                    continue

                # 计算成本和效用
                cost = state.cost_func(t + 1, params)
                utility = state.utility_func(t + 1, params)

                # 应用折扣
                discounted_cost = discount(cost, params.get("dr", 0), t + 1)
                discounted_utility = discount(utility, params.get("dr", 0), t + 1)

                cycle_cost += cur_state[idx] * discounted_cost
                cycle_utility += cur_state[idx] * discounted_utility
                if t == cycles - 1:
                    # 最终状态的成本和效用也需要计算
                    last_cost += next_state[idx] * discounted_cost
                    last_utility += next_state[idx] * discounted_utility

            stage_costs.append(cycle_cost)
            stage_utilities.append(cycle_utility)

            # last_cost、last_utility 仅在最后一次转移有值
            if t == cycles - 1:
                stage_costs.append(last_cost)
                stage_utilities.append(last_utility)
                cycle_cost += last_cost
                cycle_utility += last_utility

            total_cost += cycle_cost
            total_utility += cycle_utility

        # 存储结果
        self.results = {
            "state_counts": state_counts,
            "stage_costs": stage_costs,
            "stage_utilities": stage_utilities,
            "total_cost": total_cost,
            "total_utility": total_utility,
            "edge_counts": edge_counts,
            "edge_indices": edge_indices,
        }

    def _resolve_temporary_state(self, t: int, population: float, temp_state: State,
                                 edge_counts: np.ndarray, edge_indices: Dict, params: Dict) -> Dict[str, float]:
        """
        解析临时状态转移，返回最终状态及其人口分布
        """
        final_distribution = {}
        remaining_pop = population

        # 使用队列处理临时状态转移
        from queue import Queue
        q = Queue()
        q.put((temp_state.name, remaining_pop))

        while not q.empty():
            current_state_name, current_pop = q.get()
            current_state = self.state_map[current_state_name]

            # 处理该临时状态的所有转移规则
            applicable_transitions = [
                transition for transition in current_state.transitions
                if transition["condition"](t + 1, params)
            ]

            # 计算总概率
            total_prob = sum(tran["probability_func"](t + 1, params)
                             for tran in applicable_transitions)

            if total_prob <= 0:
                raise ValueError(f"在周期{t + 1}，临时状态{current_state_name}没有有效的转移路径")

            # 处理每个适用的转移
            for transition in applicable_transitions:
                to_state = transition["to_state"]
                prob = transition["probability_func"](t + 1, params)
                actual_prob = prob / total_prob  # 归一化概率

                # 记录边转移数量
                edge_id = edge_indices[(current_state_name, to_state.name)]
                edge_counts[t, edge_id] += current_pop * actual_prob

                # 转移人口
                transferred_pop = current_pop * actual_prob

                if to_state.is_temporary:
                    # 如果目标仍然是临时状态，加入队列继续处理
                    q.put((to_state.name, transferred_pop))
                else:
                    # 到达非临时状态，记录最终分布
                    if to_state.name in final_distribution:
                        final_distribution[to_state.name] += transferred_pop
                    else:
                        final_distribution[to_state.name] = transferred_pop

        return final_distribution

    def _get_state_index(self, state_name: str) -> int:
        """获取状态的索引"""
        return list(self.state_map.keys()).index(state_name)

    def get_edge_transitions(self, from_state: str, to_state: str) -> np.ndarray:
        """获取两状态间所有周期的转移数量（边的转移）"""
        if (from_state, to_state) not in self.results["edge_indices"]:
            raise ValueError(f"边 {from_state}->{to_state} 不存在")

        edge_id = self.results["edge_indices"][(from_state, to_state)]
        return self.results["edge_counts"][:, edge_id]

    def get_cumulative_edge_transitions(self, from_state: str, to_state: str) -> float:
        """获取两状态间的累积转移数量（边的累积转移）"""
        return self.get_edge_transitions(from_state, to_state).sum()

# 辅助函数：计算折扣值
def discount(value: float, rate: float, cycle: int) -> float:
    """计算折扣后的值"""
    return value / ((1 + rate) ** cycle)


# 辅助函数：创建条件函数
def create_condition(min_cycle: int = None, max_cycle: int = None) -> Callable:
    """
    创建状态转移条件函数
    :param min_cycle: 最小模型时间（包含）
    :param max_cycle: 最大模型时间（不包含）
    :return: 条件函数
    """

    def condition(cycle: int, params: Dict) -> bool:
        result = True
        if min_cycle is not None:
            result = result and (cycle >= min_cycle)
        if max_cycle is not None:
            result = result and (cycle < max_cycle)
        return result

    return condition


def create_condition_gq_leq(min_cycle: int = None, max_cycle: int = None, cycle_mode: str="and") -> Callable:
    """
    创建状态转移条件函数
    :param min_cycle: 最小模型时间（包含）
    :param max_cycle: 最大模型时间（不包含）
    :param cycle_mode: and or
    :return: 条件函数
    """

    def condition(cycle: int, params: Dict) -> bool:
        result = True
        if min_cycle is not None:
            result = result and (cycle > min_cycle)
        if max_cycle is not None:
            result = result and (cycle <= max_cycle)
        return result

    def condition2(cycle: int, params: Dict) -> bool:
        result = condition(cycle, params)
        return not result

    if cycle_mode == "and":
        return condition
    else:
        return condition2


if __name__ == "__main__":
    # 定义参数
    params = {
        "dr": 0.0  # 折扣率
    }

    # 定义状态
    healthy = State(
        name="Healthy",
        description="健康状态",
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: 1
    )

    disease = State(
        name="Disease",
        description="患病状态",
        cost_func=lambda cycle, p: 2000,
        utility_func=lambda cycle, p: 0.7
    )

    death = State(
        name="Death",
        description="死亡状态",
        is_absorbing=True,  # 死亡是吸收态
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: 0
    )

    # 定义临时状态
    treatment = State(
        name="Treatment",
        description="治疗中",
        is_temporary=True,
    )

    diagnosis = State(
        name="Diagnosis",
        description="诊断中",
        is_temporary=True,
    )

    # 定义状态转移
    # 健康状态转移

    healthy.add_transition(
        healthy,
        probability_func=lambda cycle, p: 0.89
    )
    healthy.add_transition(
        diagnosis,
        probability_func=lambda cycle, p: 0.1,
        condition=create_condition(max_cycle=50)  # 前50个周期走诊断路径
    )

    healthy.add_transition(
        treatment,
        probability_func=lambda cycle, p: 0.1,
        condition=create_condition(min_cycle=50)  # 50个周期后走治疗路径
    )

    healthy.add_transition(
        death,
        probability_func=lambda cycle, p: 0.01
    )

    # 诊断状态转移（临时状态）
    diagnosis.add_transition(
        disease,
        probability_func=lambda cycle, p: 0.9
    )

    diagnosis.add_transition(
        death,
        probability_func=lambda cycle, p: 0.1
    )

    # 治疗状态转移（临时状态）
    treatment.add_transition(
        healthy,
        probability_func=lambda cycle, p: 0.49  # 治愈
    )

    treatment.add_transition(
        disease,
        probability_func=lambda cycle, p: 0.5  # 治疗无效
    )

    treatment.add_transition(
        death,
        probability_func=lambda cycle, p: 0.01  # 治疗中死亡
    )

    # 疾病状态转移
    disease.add_transition(
        disease,
        probability_func=lambda cycle, p: 0.9
    )

    disease.add_transition(
        death,
        probability_func=lambda cycle, p: 0.1
    )

    # 初始化模型
    model = MarkovModel(
        states=[healthy, disease, death, treatment, diagnosis],
        initial_distribution={"Healthy": 1.0, "Disease": 0.0, "Death": 0.0, "Treatment": 0.0, "Diagnosis": 0.0}
    )

    # 运行模型
    model.run(cycles=10, params=params, cohort=True)

    # 分析结果
    print(f"每个时间步的成本与效用：\n{model.results['stage_costs']}\n{model.results['stage_utilities']}")
    print(f"总成本: {model.results['total_cost']:.2f}")
    print(f"总效用: {model.results['total_utility']:.2f}")

    # 查看特定边的累积转移
    print(f"从健康到死亡的累积转移: {model.get_cumulative_edge_transitions('Healthy', 'Death'):.2f}")
    print(f"从诊断到死亡的累积转移: {model.get_cumulative_edge_transitions('Diagnosis', 'Death'):.2f}")
    print(f"从疾病到死亡的累积转移: {model.get_cumulative_edge_transitions('Disease', 'Death'):.2f}")
    print(f"从治疗到死亡的累积转移: {model.get_cumulative_edge_transitions('Treatment', 'Death'):.2f}")
    print(f"前5次状态分布: {model.results['state_counts'][:5]}")
    print(f"最终状态分布: {model.results['state_counts'][-1]}")

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

    # 可视化边转移数量
    plt.figure(figsize=(14, 8))
    edges_to_plot = [
        ("Healthy", "Diagnosis"),
        ("Healthy", "Treatment"),
        ("Healthy", "Death"),
        ("Diagnosis", "Disease"),
        ("Disease", "Death")
    ]

    for i, (from_state, to_state) in enumerate(edges_to_plot, 1):
        plt.subplot(2, 3, i)
        transitions = model.get_edge_transitions(from_state, to_state)
        plt.plot(range(1, 11), transitions)
        plt.title(f"{from_state} → {to_state}")
        plt.xlabel("周期")
        plt.ylabel("转移数量")
        plt.grid(True)

    plt.tight_layout()
    plt.show()
