from cmd.markov_model import MarkovModel
from cmd.strategy import Strategy
from typing import Dict, Tuple, Callable
import numpy as np
import pandas as pd


class BudgetImpactAnalysis:
    @staticmethod
    def run(initial_pop: Dict[str, int], inflow: Dict[str, int], strategy: Strategy,
            cycles: int) -> pd.DataFrame:
        """
        预算影响分析
        :param initial_pop: 初始人群分布（如{"pre": 25000, "symp": 5000}）
        :param inflow: 每年新增人群（如{"pre": 8000}）
        """
        pop_counts = np.zeros((cycles + 1, strategy.model.n_states))
        # 初始化人群
        for s, cnt in initial_pop.items():
            pop_counts[0, strategy.model.state_index[s]] = cnt

        total_costs = []
        for t in range(cycles):
            # 加入新增人群
            for s, cnt in inflow.items():
                pop_counts[t, strategy.model.state_index[s]] += cnt
            # 应用转移矩阵
            transition_matrix = strategy.model.transition_func(t + 1, strategy.params)
            pop_counts[t + 1] = pop_counts[t] @ transition_matrix
            # 计算当前周期成本
            cycle_cost = 0.0
            for i, s in enumerate(strategy.model.states):
                state_time = t + 1  # 简化：假设状态时间=模型时间
                cost = strategy.model.cost_func(s, t + 1, state_time, strategy.params)
                cycle_cost += pop_counts[t, i] * cost
            total_costs.append(cycle_cost)

        return pd.DataFrame({
            "cycle": range(1, cycles + 1),
            "total_pop": pop_counts[1:].sum(axis=1),
            "total_cost": total_costs
        })