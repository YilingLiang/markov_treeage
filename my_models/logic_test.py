from lab.markov_tunnel_db_v4 import MarkovModel, State, discount
from lab.condition import create_condition
from parameter.define_parameters import Parameters
from lab.plot_markov import visualize_markov_model
from parameter.define_tables import Table
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Callable, Tuple, Union, Optional, Any


if __name__ == "__main__":
    # 定义参数
    params = {
        "dr": 0.0  # 折扣率
    }

    # 定义状态
    healthy = State(
        name="Healthy",
        description="健康状态",
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: 1
    )

    disease = State(
        name="Disease",
        description="患病状态",
        cost_func=lambda cycle, p: 2000,
        utility_func=lambda cycle, p: 0.7
    )

    death = State(
        name="Death",
        description="死亡状态",
        is_absorbing=True,  # 死亡是吸收态
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: 0
    )

    # 定义临时状态
    treatment = State(
        name="Treatment",
        description="治疗中",
        is_temporary=True,
        cost_func=lambda cycle, p: 2000,
        utility_func=lambda cycle, p: 1
    )

    diagnosis = State(
        name="Diagnosis",
        description="诊断中",
        is_temporary=True,
        cost_func=lambda cycle, p: 2000,
        utility_func=lambda cycle, p: 1
    )

    # 定义状态转移
    # 健康状态转移

    healthy.add_transition(
        healthy,
        probability_func=lambda cycle, p: 0.89
    )
    healthy.add_transition(
        diagnosis,
        probability_func=lambda cycle, p: 0.1,
        condition=create_condition(max_cycle=50)  # 前50个周期走诊断路径
    )

    healthy.add_transition(
        treatment,
        probability_func=lambda cycle, p: 0.1,
        condition=create_condition(min_cycle=50)  # 50个周期后走治疗路径
    )

    healthy.add_transition(
        death,
        probability_func=lambda cycle, p: 0.01
    )

    # 诊断状态转移（临时状态）
    diagnosis.add_transition(
        disease,
        probability_func=lambda cycle, p: 0.9
    )

    diagnosis.add_transition(
        death,
        probability_func=lambda cycle, p: 0.1
    )

    # 治疗状态转移（临时状态）
    treatment.add_transition(
        healthy,
        probability_func=lambda cycle, p: 0.49  # 治愈
    )

    treatment.add_transition(
        disease,
        probability_func=lambda cycle, p: 0.5  # 治疗无效
    )

    treatment.add_transition(
        death,
        probability_func=lambda cycle, p: 0.01  # 治疗中死亡
    )

    # 疾病状态转移
    disease.add_transition(
        disease,
        probability_func=lambda cycle, p: 0.9
    )

    disease.add_transition(
        death,
        probability_func=lambda cycle, p: 0.1
    )

    # 初始化模型
    model = MarkovModel(
        states=[healthy, disease, death, treatment, diagnosis],
        initial_distribution={"Healthy": 1.0}
    )

    # 运行模型
    model.run(cycles=10, params=params, cohort=True)

    # 分析结果
    print(f"每个时间步的成本与效用：\n{model.results['stage_costs']}\n{model.results['stage_utilities']}")
    print(f"总成本: {model.results['total_cost']:.2f}")
    print(f"总效用: {model.results['total_utility']:.2f}")

    # 查看特定边的累积转移
    print(f"从健康到死亡的累积转移: {model.get_cumulative_edge_transitions('Healthy', 'Death'):.2f}")
    print(f"从诊断到死亡的累积转移: {model.get_cumulative_edge_transitions('Diagnosis', 'Death'):.2f}")
    print(f"从疾病到死亡的累积转移: {model.get_cumulative_edge_transitions('Disease', 'Death'):.2f}")
    print(f"从治疗到死亡的累积转移: {model.get_cumulative_edge_transitions('Treatment', 'Death'):.2f}")
    print(f"前5次状态分布: {model.results['state_counts'][:5]}")
    print(f"最终状态分布: {model.results['state_counts'][-1]}")

    # 可视化状态分布随时间的变化
    plt.figure(figsize=(12, 6))
    time_points = range(11)
    for state in model.non_temporary_states:
        idx = model._get_state_index(state.name)
        plt.plot(time_points, model.results["state_counts"][:, idx], label=f"{state.name} ({state.description})")
    plt.xlabel("周期")
    plt.ylabel("比例")
    plt.title("状态分布随时间的变化")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 可视化边转移数量
    plt.figure(figsize=(14, 8))
    edges_to_plot = [
        ("Healthy", "Diagnosis"),
        ("Healthy", "Treatment"),
        ("Healthy", "Death"),
        ("Diagnosis", "Disease"),
        ("Disease", "Death")
    ]

    for i, (from_state, to_state) in enumerate(edges_to_plot, 1):
        plt.subplot(2, 3, i)
        transitions = model.get_edge_transitions(from_state, to_state)
        plt.plot(range(1, 11), transitions)
        plt.title(f"{from_state} → {to_state}")
        plt.xlabel("周期")
        plt.ylabel("转移数量")
        plt.grid(True)

    plt.tight_layout()
    plt.show()
