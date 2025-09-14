from graphviz import Digraph
from typing import Dict, List, Callable, Tuple
from lab.markov_tunnel_db_v5_no_cu import MarkovModel, State


def visualize_markov_model(model: MarkovModel, current_cycle: int = 0, params: Dict = None) -> Digraph:
    """
    可视化整个马尔可夫模型在指定周期的状态转移图

    Args:
        model: 马尔可夫模型实例
        current_cycle: 当前周期，用于计算转移概率
        params: 模型参数

    Returns:
        Digraph: Graphviz有向图对象
    """
    if params is None:
        params = {}

    dot = Digraph(comment='Markov Model')
    dot.attr(rankdir='LR', size='8,5')

    # 添加所有状态节点
    for state in model.states:
        # 设置节点属性
        node_attrs = {}
        if state.is_absorbing:
            node_attrs['shape'] = 'doublecircle'
            node_attrs['color'] = 'red'
        elif state.is_temporary:
            node_attrs['shape'] = 'diamond'
            node_attrs['color'] = 'blue'
        else:
            node_attrs['shape'] = 'circle'
            node_attrs['color'] = 'black'

        # 添加节点
        dot.node(state.name, f"{state.name}\n{state.description}", **node_attrs)

    # 添加转移边
    for state in model.states:
        if state.is_absorbing:
            continue  # 吸收态没有出边

        # 获取当前周期的转移规则
        if state.tunnel_cycle is not None:
            # 使用tunnel转移规则
            transitions = state.tunnel_transitions
            get_prob = lambda t: t[1](current_cycle, params)
            get_target = lambda t: t[0].name
        else:
            # 使用默认转移规则
            transitions = [
                trans for trans in state.transitions
                if trans["condition"](current_cycle, params)
            ]
            get_prob = lambda t: t["probability_func"](current_cycle, params)
            get_target = lambda t: t["to_state"].name

        # 添加转移边
        for transition in transitions:
            prob = get_prob(transition)
            target = get_target(transition)

            # 格式化概率显示
            prob_str = f"{prob:.3f}"
            if prob < 0.001:
                prob_str = f"{prob:.2e}"

            dot.edge(state.name, target, label=prob_str)

    return dot


def visualize_markov_model_state(model: MarkovModel, state: State,
                                 current_cycle: int = 0, params: Dict = None,
                                 max_depth: int = 3, current_depth: int = 0) -> Digraph:
    """
    可视化从指定状态开始的马尔可夫模型分支

    Args:
        model: 马尔可夫模型实例
        state: 起始状态
        current_cycle: 当前周期，用于计算转移概率
        params: 模型参数
        max_depth: 最大递归深度
        current_depth: 当前递归深度

    Returns:
        Digraph: Graphviz有向图对象
    """
    if params is None:
        params = {}

    dot = Digraph(comment=f'Markov Model from {state.name}')
    dot.attr(fontname="SimHei")  # 中文显示
    dot.attr(rankdir='LR', size='10,8', dpi='300')

    def add_state_and_transitions(state_obj, depth):
        if depth > max_depth:
            return

        # 添加当前状态节点
        node_attrs = {}
        if state_obj.is_absorbing:
            node_attrs['shape'] = 'doublecircle'
            node_attrs['color'] = 'red'
        elif state_obj.is_temporary:
            node_attrs['shape'] = 'diamond'
            node_attrs['color'] = 'blue'
        else:
            node_attrs['shape'] = 'circle'
            node_attrs['color'] = 'black'

        node_attrs["fontname"] = "SimHei"
        dot.node(state_obj.name, f"{state_obj.name}\n{state_obj.description}", **node_attrs)

        if state_obj.is_absorbing:
            return  # 吸收态没有出边

        # 获取当前周期的转移规则
        if state_obj.tunnel_cycle is not None:
            transitions = state_obj.tunnel_transitions
            get_prob = lambda t: t[1](current_cycle, params)
            get_target = lambda t: t[0]
        else:
            transitions = [
                trans for trans in state_obj.transitions
                if trans["condition"](current_cycle, params)
            ]
            get_prob = lambda t: t["probability_func"](current_cycle, params)
            get_target = lambda t: t["to_state"]

        # 添加转移边和递归处理目标状态
        for transition in transitions:
            prob = get_prob(transition)
            target_state = get_target(transition)

            # 格式化概率显示
            prob_str = f"{prob:.3f}"
            if prob < 0.001:
                prob_str = f"{prob:.2e}"

            # 添加边
            dot.edge(state_obj.name, target_state.name, label=prob_str)

            # 递归处理目标状态（如果还没处理过）
            if target_state.name not in processed_states:
                processed_states.add(target_state.name)
                add_state_and_transitions(target_state, depth + 1)

    # 跟踪已处理的状态以避免循环
    processed_states = set()
    processed_states.add(state.name)

    # 从起始状态开始构建图
    add_state_and_transitions(state, current_depth)

    return dot


# 辅助函数：创建条件函数
def create_condition(min_cycle: int = None, max_cycle: int = None) -> Callable[[int, Dict], bool]:
    """创建周期条件函数"""

    def condition(cycle, params):
        if min_cycle is not None and cycle < min_cycle:
            return False
        if max_cycle is not None and cycle > max_cycle:
            return False
        return True

    return condition
