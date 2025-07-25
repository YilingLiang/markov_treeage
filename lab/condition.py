from typing import Dict, Callable


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