import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, binom, lognorm, gamma, poisson
from typing import Dict, List, Callable, Tuple


class State:
    def __init__(self, name: str, desc: str, is_temporary: str):
        self.name = name
        self.desc = desc
        self.is_temporary = is_temporary
        self.outgoing_transitions = []  # 从该状态出发的转移

    def add_transition(self, to_state: 'State', probability_func: Callable[[int, int, Dict], float]):
        """添加从当前状态到另一个状态的转移"""
        self.outgoing_transitions.append((to_state, probability_func))




class States:
    def __init__(self, states: List[str]):
        self.states = states
        self.n_states = len(states)
        self.state_index = {s: i for i, s in enumerate(states)} # 状态到索引的映射

    def get_all_states(self) -> List[str]:
        return self.states

    def get_state_index(self, state: str) -> int:
        return self.state_index[state]

    def get_state(self, index: int) -> str:
        return self.states[index]
