from typing import Dict, Callable

def create_condition(min_cycle: int = None, max_cycle: int = None) -> Callable:
    """
    创建状态转移条件函数
    因当前时间步是上一步转移而来，故当前时间步看前一步，可与 treeage 保持一致
    :param min_cycle: 最小模型时间（包含）
    :param max_cycle: 最大模型时间（不包含）
    :return: 条件函数
    """
    if min_cycle is not None:
        min_cycle += 1
    if max_cycle is not None:
        max_cycle += 1

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
    因当前时间步是上一步转移而来，故当前时间步看前一步，可与 treeage 保持一致
    :param min_cycle: 最小模型时间（包含）
    :param max_cycle: 最大模型时间（不包含）
    :param cycle_mode: and or
    :return: 条件函数
    """
    if min_cycle is not None:
        min_cycle += 1
    if max_cycle is not None:
        max_cycle += 1

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
