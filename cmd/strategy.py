from cmd.markov_model import MarkovModel
from typing import Dict
import numpy as np


class Strategy:
    def __init__(self, name: str, model: MarkovModel, params: Dict):
        self.name = name
        self.model = model
        self.params = params
        self.results = None

    def run(self, cycles: int, half_cycle_correction: bool=False) -> None:
        # self.model.run(cycles, self.params)
        self.model.run_with_half(cycles, self.params, half_cycle_correction=half_cycle_correction)
        self.results = self.model.results


def calculate_icer(strategy_a: Strategy, strategy_b: Strategy) -> float:
    """计算增量成本效益比（ICER）"""
    delta_cost = strategy_b.results["total_cost"] - strategy_a.results["total_cost"]
    delta_effect = strategy_b.results["total_effect"] - strategy_a.results["total_effect"]
    return delta_cost / delta_effect if delta_effect != 0 else np.inf