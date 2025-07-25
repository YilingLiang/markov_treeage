from cmd.markov_model import MarkovModel
from cmd.strategy import Strategy
from typing import Dict, Tuple, Callable
import numpy as np
import pandas as pd


class SensitivityAnalysis:
    @staticmethod
    def dsa(base_strategy: Strategy, params_ranges: Dict[str, Tuple[float, float]],
            cycles: int) -> pd.DataFrame:
        """
        确定性敏感性分析（DSA）
        :param params_ranges: 参数的上下界（如{"p_disease_base": (0.2, 0.3)}）
        """
        results = []
        base_results = base_strategy.results
        # 逐个参数分析
        for param, (low, high) in params_ranges.items():
            # 测试下界
            new_params = base_strategy.params.copy()
            new_params[param] = low
            model_low = MarkovModel(base_strategy.model.states,
                                    {s: 1.0 if i == 0 else 0 for i, s in enumerate(base_strategy.model.states)})
            model_low.set_transition_matrix(base_strategy.model.transition_func)
            model_low.set_state_values(base_strategy.model.cost_func, base_strategy.model.effect_func)
            strat_low = Strategy(f"{base_strategy.name}_low_{param}", model_low, new_params)
            strat_low.run(cycles)
            # 测试上界
            new_params[param] = high
            model_high = MarkovModel(base_strategy.model.states,
                                     {s: 1.0 if i == 0 else 0 for i, s in enumerate(base_strategy.model.states)})
            model_high.set_transition_matrix(base_strategy.model.transition_func)
            model_high.set_state_values(base_strategy.model.cost_func, base_strategy.model.effect_func)
            strat_high = Strategy(f"{base_strategy.name}_high_{param}", model_high, new_params)
            strat_high.run(cycles)
            # 记录结果
            results.append({
                "param": param,
                "value": "low",
                "cost": strat_low.results["total_cost"],
                "effect": strat_low.results["total_effect"]
            })
            results.append({
                "param": param,
                "value": "high",
                "cost": strat_high.results["total_cost"],
                "effect": strat_high.results["total_effect"]
            })
        return pd.DataFrame(results)

    @staticmethod
    def psa(base_strategy: Strategy, param_distributions: Dict[str, Callable],
            n_sim: int, cycles: int) -> pd.DataFrame:
        """
        概率敏感性分析（PSA）
        :param param_distributions: 参数的概率分布（如{"p_disease_base": lambda: binom.rvs(n=1, p=0.25)}）
        """
        results = []
        for i in range(n_sim):
            # 从分布中抽样参数
            new_params = base_strategy.params.copy()
            for param, dist in param_distributions.items():
                new_params[param] = dist()
            # 运行模型
            model = MarkovModel(base_strategy.model.states,
                                {s: 1.0 if i == 0 else 0 for i, s in enumerate(base_strategy.model.states)})
            model.set_transition_matrix(base_strategy.model.transition_func)
            model.set_state_values(base_strategy.model.cost_func, base_strategy.model.effect_func)
            strat = Strategy(f"{base_strategy.name}_sim_{i}", model, new_params)
            strat.run(cycles)
            results.append({
                "sim": i,
                "cost": strat.results["total_cost"],
                "effect": strat.results["total_effect"]
            })
        return pd.DataFrame(results)