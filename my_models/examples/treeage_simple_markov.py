from lab.markov_tunnel_db_v5 import MarkovModel, State
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

    # 分析结果
    print(f"总成本: {model.results['total_cost']:.2f}")
    print(f"总效用: {model.results['total_utility']:.2f}")

    # 查看特定边的累积转移
    print(f"从健康到死亡的累积转移: {model.get_cumulative_edge_transitions('Healthy', 'Death'):.2f}")
    print(f"从疾病到死亡的累积转移: {model.get_cumulative_edge_transitions('Disease', 'Death'):.2f}")
    print(f"最终状态分布: {model.results['state_counts'][-1]}")
    print(f"每个时间步状态分布: {model.results['state_counts']}")

    # 查看停留时间分布
    print("\n健康状态的停留时间分布:")
    for t in range(5):
        dist = model.get_dwell_time_distribution('Healthy', t)
        print(f"周期 {t}: {[f'{x:.4f}' for x in dist]}")

    print("\n疾病状态的停留时间分布:")
    for t in range(5):
        dist = model.get_dwell_time_distribution('Disease', t)
        print(f"周期 {t}: {[f'{x:.4f}' for x in dist]}")

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

    # 可视化健康状态的停留时间分布
    plt.figure(figsize=(12, 6))
    healthy_idx = model._get_state_index('Healthy')
    max_dwell = healthy.tunnel_cycle if healthy.tunnel_cycle is not None else 0
    for dwell_time in range(max_dwell + 1):
        dwell_dist = [model.dwell_time_distributions[t][healthy_idx, dwell_time] for t in range(11)]
        plt.plot(time_points, dwell_dist, label=f"停留{dwell_time}周期")
    plt.xlabel("周期")
    plt.ylabel("比例")
    plt.title("健康状态的停留时间分布")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 可视化疾病状态的停留时间分布
    plt.figure(figsize=(12, 6))
    disease_idx = model._get_state_index('Disease')
    max_dwell = disease.tunnel_cycle if disease.tunnel_cycle is not None else 0
    for dwell_time in range(max_dwell + 1):
        dwell_dist = [model.dwell_time_distributions[t][disease_idx, dwell_time] for t in range(11)]
        plt.plot(time_points, dwell_dist, label=f"停留{dwell_time}周期")
    plt.xlabel("周期")
    plt.ylabel("比例")
    plt.title("疾病状态的停留时间分布")
    plt.legend()
    plt.grid(True)
    plt.show()