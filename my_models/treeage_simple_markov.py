from lab.markov5 import MarkovModel, State, discount, create_condition_gq_leq, create_condition
from parameter.define_parameters import Parameters
from lab.plot_markov import visualize_markov_model
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


if __name__ == "__main__":
    # 创建状态
    healthy = State(
        name="Healthy",
        description="健康状态",
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: 1.0,
    )

    disease = State(
        name="Disease",
        description="患病状态",
        cost_func=lambda cycle, p: 2000,
        utility_func=lambda cycle, p: 0.7,
    )

    death = State(
        name="Death",
        description="死亡状态",
        is_absorbing=True,
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: 0
    )

    # 添加正常转移规则
    healthy.add_transition(healthy, lambda c, p: 0.9)
    healthy.add_transition(disease, lambda c, p: 0.09)  # 每年10%概率患病
    healthy.add_transition(death, lambda c, p: 0.01)  # 每年2%概率死亡

    disease.add_transition(disease, lambda c, p: 0.7)
    disease.add_transition(healthy, lambda c, p: 0.1)  # 每年20%概率康复
    disease.add_transition(death, lambda c, p: 0.2)  # 每年10%概率死亡

    # 创建模型
    model = MarkovModel([healthy, disease, death], {"Healthy": 1.0})
    model.run(10, {"dr": 0.00})

    # 可视化结果
    graph = visualize_markov_model(model, current_cycle=3)
    graph.render('markov_model', view=True)

    print(model.results["state_counts"])

    # 分析结果
    print(f"总成本: {model.results['total_cost']:.2f}")
    print(f"总效用: {model.results['total_utility']:.2f}")

    # 查看特定边的累积转移
    print(f"从健康到死亡的累积转移: {model.get_cumulative_edge_transitions('Healthy', 'Death'):.2f}")
    print(f"从疾病到死亡的累积转移: {model.get_cumulative_edge_transitions('Disease', 'Death'):.2f}")
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
        ("Healthy", "Death"),
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
