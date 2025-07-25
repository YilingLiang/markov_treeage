from lab.markov5 import MarkovModel, State, discount, create_condition_gq_leq, create_condition
from parameter.define_parameters import Parameters
from parameter.define_tables import Table
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict

from graphviz import Digraph
import textwrap


def visualize_markov_model(model: MarkovModel, current_cycle: int = 0, params: Dict = None) -> Digraph:
    """
    使用Graphviz可视化Markov模型的状态转移图

    参数:
        model: MarkovModel实例
        current_cycle: 当前周期(用于计算条件概率)
        params: 模型参数

    返回:
        graphviz.Digraph对象
    """
    if params is None:
        params = {}

    # 创建有向图
    dot = Digraph(comment='Markov Model', format='png')
    dot.attr(fontname="SimHei") # 中文显示
    dot.attr(rankdir='LR', size='10,8', dpi='300')
    dot.attr('node', shape='ellipse', style='filled', fillcolor='lightgrey')
    dot.attr('edge', fontsize='10')

    # 添加状态节点
    for state in model.states:
        # 设置节点属性
        node_attrs = {}

        # 根据状态类型设置不同样式
        if state.is_absorbing:
            node_attrs['shape'] = 'doublecircle'
            node_attrs['fillcolor'] = '#ffcccc'  # 浅红色
            node_attrs["fontname"] = "SimHei"
        elif state.is_temporary:
            node_attrs['shape'] = 'diamond'
            node_attrs['fillcolor'] = '#ccffcc'  # 浅绿色
            node_attrs["fontname"] = "SimHei"
        else:
            node_attrs['fillcolor'] = '#ccccff'  # 浅蓝色
            node_attrs["fontname"] = "SimHei"

        # 添加节点
        label = f"{state.name}\n({state.description})" if state.description else state.name
        dot.node(state.name, label=label, **node_attrs)

    # 添加转移边
    for from_state in model.states:
        # 收集所有适用的转移
        applicable_transitions = []
        for transition in from_state.transitions:
            if transition["condition"](current_cycle, params):
                applicable_transitions.append(transition)

        # 计算总概率(用于归一化)
        total_prob = sum(t["probability_func"](current_cycle, params)
                         for t in applicable_transitions)

        # 添加每条边
        for transition in applicable_transitions:
            to_state = transition["to_state"]
            prob = transition["probability_func"](current_cycle, params)

            # 归一化概率(如果总概率>0)
            normalized_prob = prob / total_prob if total_prob > 0 else 0

            # 创建边标签
            condition = ""
            if transition["condition"].__code__.co_code != create_condition().__code__.co_code:
                # 如果有自定义条件，尝试提取信息
                code = transition["condition"].__code__
                if "min_cycle" in code.co_varnames or "max_cycle" in code.co_varnames:
                    min_c = transition["condition"].__defaults__[0] if transition["condition"].__defaults__ else None
                    max_c = transition["condition"].__defaults__[1] if transition["condition"].__defaults__ and len(
                        transition["condition"].__defaults__) > 1 else None
                    if min_c is not None or max_c is not None:
                        condition = f"[{f'cycle≥{min_c}' if min_c else ''}{' & ' if min_c and max_c else ''}{f'cycle<{max_c}' if max_c else ''}]"

            label = f"{normalized_prob:.2f}\n{condition}" if condition else f"{normalized_prob:.2f}"

            # 设置边属性
            edge_attrs = {}
            if from_state.is_temporary:
                edge_attrs['style'] = 'dashed'
                edge_attrs['color'] = 'green'
            elif to_state.is_temporary:
                edge_attrs['style'] = 'dashed'
                edge_attrs['color'] = 'blue'

            # 添加边
            dot.edge(from_state.name, to_state.name, label=label, **edge_attrs)

    return dot
