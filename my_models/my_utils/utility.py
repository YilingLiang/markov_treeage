
def health_utility_func(value: float, rate: float, cycle: int) -> float:
    """计算折扣后的值"""
    if cycle == 0:
        return 0.5 * value / ((1 + rate) ** cycle)
    elif cycle == 84:
        return 0.5 * value / ((1 + rate) ** cycle)
    else:
        return value / ((1 + rate) ** cycle)

