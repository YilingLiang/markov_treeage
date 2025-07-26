from lab.markov_tunnel_db_v4 import MarkovModel, State, discount
from lab.condition import create_condition
import matplotlib.pyplot as plt


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
    death = State(
        name="Death",
        description="死亡状态",
        is_absorbing=True,  # 死亡是吸收态
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: 0
    )

    disease = State(
        name="Disease",
        description="患病状态",
        cost_func=lambda cycle, p: 2000,
        utility_func=lambda cycle, p: 0.7,
        tunnel_cycle=4,
    )
    # dtmp1 = State(
    #     name="Dtmp1",
    #     is_temporary=True
    # )
    # dtmp2 = State(
    #     name="Dtmp2",
    #     is_temporary=True
    # )
    # # 疾病状态转移
    # disease.add_transition(
    #     dtmp1,
    #     probability_func=lambda cycle, p: 0.6
    # )
    # disease.add_transition(
    #     dtmp2,
    #     probability_func=lambda cycle, p: 0.6
    # )

    disease.add_transition(
        disease,
        probability_func=lambda cycle, p: 0.4
    )
    disease.add_tunnel_transition(
        disease,
        lambda cycle, p: 0.8
    )
    disease.add_tunnel_transition(
        death,
        lambda cycle, p: 0.2
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

    disease.add_transition(
        diagnosis,
        probability_func=lambda cycle, p: 0.6,
        condition=create_condition(max_cycle=50)  # 前50个周期走诊断路径
    )
    disease.add_transition(
        treatment,
        probability_func=lambda cycle, p: 0.6,
        condition=create_condition(min_cycle=50)  # 50个周期后走治疗路径
    )

    # 初始化模型
    model = MarkovModel(
        states=[healthy, disease, death, treatment, diagnosis],
        initial_distribution={"Healthy": 1, "Disease": 0, "Death": 0},
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
    print(f"状态分布: {model.results['state_counts']}")
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
