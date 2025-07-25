import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, binom, lognorm, gamma, poisson
from typing import Dict, List, Callable, Tuple


# 1. 时间依赖参数处理工具
class TimeDependency:
    """处理模型时间（model_time）和状态时间（state_time）"""

    @staticmethod
    def model_time(cycle: int) -> int:
        """返回模型运行的周期数（从1开始）"""
        return cycle

    @staticmethod
    def state_time(cycle_in_state: int) -> int:
        """返回在当前状态的周期数（从1开始）"""
        return cycle_in_state


# 2. 概率工具（对应heemod的概率合并、转换函数）
class ProbabilityTools:
    @staticmethod
    def combine_probs(p1: float, p2: float) -> float:
        """合并两个独立事件的概率：P(A∪B) = 1 - (1-P(A))*(1-P(B))"""
        return 1 - (1 - p1) * (1 - p2)

    @staticmethod
    def rate_to_prob(rate: float, t: float = 1) -> float:
        """将发生率转换为t时间内的概率：1 - exp(-rate*t)"""
        return 1 - np.exp(-rate * t)

    @staticmethod
    def rescale_prob(p: float, original_cycle: float, target_cycle: float) -> float:
        """调整概率至不同周期长度"""
        return 1 - (1 - p) ** (target_cycle / original_cycle)


# 3. 折扣计算工具
def discount(value: float, rate: float, cycle: int) -> float:
    """计算折扣后的值：value / (1 + rate)^cycle"""
    return value / ((1 + rate) ** cycle)