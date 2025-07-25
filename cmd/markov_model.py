import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, binom, lognorm, gamma, poisson
from typing import Dict, List, Callable, Tuple
from cmd.time_dependency import discount


class MarkovModel:
    def __init__(self, states: List[str], init_state: Dict[str, float]):
        """
        初始化马尔可夫模型
        :param states: 状态列表（如["pre", "symp", "death"]）
        :param init_state: 初始状态分布（如{"pre": 1.0, "symp": 0, "death": 0}）
        """
        self.states = states
        self.n_states = len(states)
        self.state_index = {s: i for i, s in enumerate(states)}
        self.init_state = np.array([init_state[s] for s in states])
        self.cycles = 0
        self.results = None  # 存储各周期的状态分布、成本、效果
        self.transition_counts = None  # 转移计数矩阵

    def set_transition_matrix(self, transition_func: Callable[[int, Dict], np.ndarray]):
        """
        设置转移矩阵（支持时间依赖）
        :param transition_func: 函数，输入(周期, 参数)，返回转移矩阵
        """
        self.transition_func = transition_func

    def set_state_values(self, cost_func: Callable[[str, int, int, Dict], float],
                         effect_func: Callable[[str, int, int, Dict], float]):
        """
        设置状态的成本和效果函数（支持时间依赖）
        :param cost_func: 计算状态成本的函数（状态名, 模型时间, 状态时间, 参数）
        :param effect_func: 计算状态效果的函数（状态名, 模型时间, 状态时间, 参数）
        """
        self.cost_func = cost_func
        self.effect_func = effect_func

    def run(self, cycles: int, params: Dict) -> None:
        """运行模型指定周期数"""
        self.cycles = cycles
        state_counts = np.zeros((cycles + 1, self.n_states))
        state_counts[0] = self.init_state  # 初始状态

        # 初始化转移计数矩阵 [周期数, 起始状态, 目标状态]
        self.transition_counts = np.zeros((cycles, self.n_states, self.n_states))

        total_cost = 0.0
        total_effect = 0.0
        state_time = {s: 0 for s in self.states}  # 跟踪每个状态的持续时间

        for t in range(cycles):
            # 获取当前周期的转移矩阵
            transition_matrix = self.transition_func(t + 1, params)  # t从1开始（模型时间）

            # 记录从状态A到状态B的转移数量
            for a in range(self.n_states):  # 遍历所有起始状态
                for b in range(self.n_states):  # 遍历所有目标状态
                    if a != b:  # 只记录不同状态间的转移
                        self.transition_counts[t, a, b] = state_counts[t, a] * transition_matrix[a, b]

            # 更新状态分布
            state_counts[t + 1] = state_counts[t] @ transition_matrix

            # 计算当前周期的成本和效果（折扣后）
            for i, s in enumerate(self.states):
                if state_counts[t, i] == 0:
                    continue
                # 状态时间更新（若当前状态为s，持续时间+1）
                state_time[s] += 1 if np.argmax(state_counts[t]) == i else 0
                # 计算成本和效果（应用折扣率）
                cost = self.cost_func(s, t + 1, state_time[s], params)
                effect = self.effect_func(s, t + 1, state_time[s], params)
                discounted_cost = discount(cost, params.get("dr", 0), t + 1)
                discounted_effect = discount(effect, params.get("dr", 0), t + 1)

                total_cost += state_counts[t, i] * discounted_cost
                total_effect += state_counts[t, i] * discounted_effect

        self.results = {
            "state_counts": state_counts,
            "total_cost": total_cost,
            "total_effect": total_effect,
            "transition_counts": self.transition_counts  # 将转移计数添加到结果中
        }

    def run_with_half(self, cycles: int, params: Dict, half_cycle_correction: bool = False) -> None:
        """运行模型，支持半周期矫正"""
        self.cycles = cycles

        state_counts = np.zeros((cycles + 1, self.n_states))
        state_counts[0] = self.init_state  # 初始状态

        # 初始化转移计数矩阵 [周期数, 起始状态, 目标状态]
        self.transition_counts = np.zeros((cycles, self.n_states, self.n_states))

        total_cost = 0.0
        total_effect = 0.0
        state_time = {s: 0 for s in self.states}

        for t in range(cycles):
            # 1. 计算转移矩阵（不变）
            transition_matrix = self.transition_func(t + 1, params)

            # 记录从状态A到状态B的转移数量
            for a in range(self.n_states):  # 遍历所有起始状态
                for b in range(self.n_states):  # 遍历所有目标状态
                    if a != b:  # 只记录不同状态间的转移
                        self.transition_counts[t, a, b] = state_counts[t, a] * transition_matrix[a, b]

            state_counts[t + 1] = state_counts[t] @ transition_matrix

            # 2. 半周期矫正：使用平均状态计数
            if half_cycle_correction:
                # 周期内平均状态 = （起点状态 + 终点状态）/ 2
                current_state = (state_counts[t] + state_counts[t + 1]) / 2
            else:
                current_state = state_counts[t]  # 原逻辑：仅用起点状态

            # 3. 基于当前状态（矫正后）计算成本和效果
            for i, s in enumerate(self.states):
                if current_state[i] == 0:
                    continue
                state_time[s] += 1 if np.argmax(state_counts[t]) == i else 0
                cost = self.cost_func(s, t + 1, state_time[s], params)
                effect = self.effect_func(s, t + 1, state_time[s], params)
                discounted_cost = discount(cost, params.get("dr", 0), t + 1)
                discounted_effect = discount(effect, params.get("dr", 0), t + 1)

                # 用矫正后的状态计数累加
                total_cost += current_state[i] * discounted_cost
                total_effect += current_state[i] * discounted_effect

        self.results = {
            "state_counts": state_counts,
            "total_cost": total_cost,
            "total_effect": total_effect,
            "transition_counts": self.transition_counts
        }