import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from symengine import symbols, exp
from scipy.optimize import minimize
from scipy.stats import weibull_min
import time

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class HCCWeibullEventModel:
    """
    Discrete Event Simulation for HCC progression with 5 states using Weibull distributions
    States: [health, chb, cc, hcc, death]
    Uses Weibull distributions for transition times
    """

    def __init__(self, initial_population=10000, max_age=85, n_simulations=1000):
        self.initial_population = initial_population
        self.max_age = max_age
        self.n_simulations = n_simulations
        self.hazard_rates = None
        self.weibull_params = {}  # 存储韦伯分布参数

    def set_hazard_rates(self,
                         health_to_chb=0.04,
                         health_to_death=0.01,
                         chb_to_cc=0.08,
                         chb_to_death=0.03,
                         cc_to_death=0.06,
                         hcc_to_death=0.25):
        """
        设置基础危险率（用于非韦伯分布的转移）
        """
        self.hazard_rates = {
            'health_to_chb': health_to_chb,
            'health_to_death': health_to_death,
            'chb_to_cc': chb_to_cc,
            'chb_to_death': chb_to_death,
            'cc_to_death': cc_to_death,
            'hcc_to_death': hcc_to_death
        }

    def set_weibull_params(self, k=1.0, lam=1.0):
        """
        设置韦伯分布参数（用于cc_to_hcc转移）
        k: 形状参数
        lam: 尺度参数
        """
        self.weibull_params = {
            'k': k,  # 形状参数
            'lam': lam  # 尺度参数
        }

    def weibull_hazard(self, t, k, lam):
        """韦伯分布风险函数"""
        if t <= 0:
            return float('inf') if k < 1 else 0
        return (k / lam) * (t / lam) ** (k - 1)

    def weibull_survival(self, t, k, lam):
        """韦伯分布生存函数"""
        if t <= 0:
            return 1.0
        return np.exp(-(t / lam) ** k)

    def weibull_inverse_survival(self, u, k, lam):
        """韦伯分布生存函数的反函数"""
        if u <= 0:
            return 0
        elif u >= 1:
            return float('inf')
        return lam * (-np.log(u)) ** (1 / k)

    def simulate_individual(self, k, lam, current_age=0):
        """
        模拟单个个体的疾病进展过程，使用韦伯分布
        返回：状态历史和时间历史
        """
        states = ['health', 'chb', 'cc', 'hcc', 'death']
        state_history = []
        time_history = []
        current_state = 'health'
        current_time = current_age

        # 设置随机数生成器
        rng = np.random.default_rng()

        while current_state != 'death' and current_time <= self.max_age:
            state_history.append(current_state)
            time_history.append(current_time)

            # 获取当前状态的所有可能转移
            transitions = self._get_transitions_from_state(current_state)

            # 为每个转移采样时间
            transition_times = {}
            for transition, rate in transitions.items():
                if transition == 'cc_to_hcc':
                    # 使用韦伯分布采样
                    u = rng.random()
                    # 从当前时间开始的剩余时间
                    if current_state == 'cc':
                        # 使用韦伯分布的条件生存函数
                        current_survival = self.weibull_survival(current_time, k, lam)
                        if current_survival > 0:
                            conditional_u = u * current_survival
                            transition_time = self.weibull_inverse_survival(conditional_u, k, lam)
                            elapsed_time = transition_time - current_time
                        else:
                            elapsed_time = 0
                    else:
                        # 常规韦伯分布采样
                        transition_time = self.weibull_inverse_survival(u, k, lam)
                        elapsed_time = transition_time

                    transition_times[transition] = elapsed_time
                else:
                    # 使用指数分布采样
                    if rate > 0:
                        u = rng.random()
                        transition_time = -np.log(u) / rate if u > 0 else float('inf')
                        transition_times[transition] = transition_time
                    else:
                        transition_times[transition] = float('inf')

            # 找到最早发生的转移
            if not transition_times:
                break

            min_transition = min(transition_times.items(), key=lambda x: x[1])
            next_transition, min_time = min_transition

            # 计算下一个状态和到达时间
            next_state = self._get_next_state(current_state, next_transition)
            next_time = current_time + min_time

            # 如果超过最大年龄，停留在当前状态
            if next_time > self.max_age:
                break

            current_state = next_state
            current_time = next_time

        # 记录最终状态
        state_history.append(current_state)
        time_history.append(min(current_time, self.max_age))

        return state_history, time_history

    def _get_transitions_from_state(self, state):
        """获取从当前状态出发的所有转移"""
        transitions = {}
        if state == 'health':
            transitions = {
                'health_to_chb': self.hazard_rates['health_to_chb'],
                'health_to_death': self.hazard_rates['health_to_death']
            }
        elif state == 'chb':
            transitions = {
                'chb_to_cc': self.hazard_rates['chb_to_cc'],
                'chb_to_death': self.hazard_rates['chb_to_death']
            }
        elif state == 'cc':
            transitions = {
                'cc_to_hcc': 1.0,  # 韦伯分布，rate参数不再使用
                'cc_to_death': self.hazard_rates['cc_to_death']
            }
        elif state == 'hcc':
            transitions = {
                'hcc_to_death': self.hazard_rates['hcc_to_death']
            }

        return transitions

    def _get_next_state(self, current_state, transition):
        """根据转移确定下一个状态"""
        transition_map = {
            'health_to_chb': 'chb',
            'health_to_death': 'death',
            'chb_to_cc': 'cc',
            'chb_to_death': 'death',
            'cc_to_hcc': 'hcc',
            'cc_to_death': 'death',
            'hcc_to_death': 'death'
        }
        return transition_map.get(transition, current_state)

    def simulate_population(self, k, lam):
        """模拟整个群体的疾病进展"""
        results = []

        print(f"开始模拟 {self.n_simulations} 个个体 (k={k:.4f}, λ={lam:.4f})...")
        start_time = time.time()

        for i in range(self.n_simulations):
            if (i + 1) % 1000 == 0:
                print(f"已模拟 {i + 1} 个个体")

            state_history, time_history = self.simulate_individual(k, lam)
            results.append({
                'state_history': state_history,
                'time_history': time_history,
                'final_state': state_history[-1],
                'final_age': time_history[-1]
            })

        end_time = time.time()
        print(f"模拟完成，耗时: {end_time - start_time:.2f} 秒")

        return results

    def calculate_incidence_rate(self, results, age_start=50, age_end=55):
        """计算50-55岁年龄段的HCC发病率"""
        incidence_count = 0
        at_risk_count = 0

        for result in results:
            state_history = result['state_history']
            time_history = result['time_history']

            # 检查个体是否在50-55岁期间进入HCC状态
            hcc_occurred = False
            for i in range(1, len(state_history)):
                if (state_history[i] == 'hcc' and state_history[i - 1] != 'hcc' and
                        age_start <= time_history[i] <= age_end):
                    incidence_count += 1
                    hcc_occurred = True
                    break

            # 计算风险人群：在50岁时存活且未患HCC
            for i in range(len(time_history)):
                if time_history[i] >= age_start:
                    if state_history[i] in ['health', 'chb', 'cc'] and not hcc_occurred:
                        at_risk_count += 1
                    break

        if at_risk_count > 0:
            incidence_rate = incidence_count / at_risk_count
        else:
            incidence_rate = 0

        return incidence_rate, incidence_count, at_risk_count

    def calculate_prevalence_by_age(self, results):
        """计算各年龄段的患病率"""
        age_bins = np.arange(0, self.max_age + 1, 1)
        prevalence = np.zeros(len(age_bins))
        population_count = np.zeros(len(age_bins))
        disease_count = np.zeros(len(age_bins))

        for result in results:
            state_history = result['state_history']
            time_history = result['time_history']

            for i in range(len(time_history)):
                age = int(time_history[i])
                if age < len(age_bins):
                    state = state_history[i]
                    population_count[age] += 1
                    if state in ['chb', 'cc', 'hcc']:
                        disease_count[age] += 1

        # 计算患病率
        for i in range(len(age_bins)):
            if population_count[i] > 0:
                prevalence[i] = disease_count[i] / population_count[i]

        return age_bins, prevalence

    def optimize_weibull_params(self, target_incidence, age_start=50, age_end=55):
        """优化韦伯分布参数以达到目标发病率（50-55岁）"""

        def objective(params):
            k, lam = params
            print(f"测试 k={k:.4f}, λ={lam:.4f}")
            results = self.simulate_population(k, lam)
            incidence_rate, _, _ = self.calculate_incidence_rate(results, age_start, age_end)
            loss = (incidence_rate - target_incidence) ** 2
            print(f"发病率: {incidence_rate:.6f}, 目标: {target_incidence}, 损失: {loss:.6e}")
            return loss

        # 优化
        print(f"开始优化韦伯分布参数，目标发病率: {target_incidence} (年龄 {age_start}-{age_end}岁)")

        # 初始猜测值
        initial_guess = [1.5, 10.0]  # k=1.5, λ=10

        # 参数边界：k > 0, λ > 0
        bounds = [(0.1, 5.0), (1.0, 50.0)]

        result = minimize(objective, initial_guess, method='L-BFGS-B', bounds=bounds)

        optimal_k, optimal_lam = result.x
        return result.fun, optimal_k, optimal_lam

    def plot_weibull_comparison(self, k, lam):
        """绘制韦伯分布与指数分布的对比"""
        t = np.linspace(0, 50, 100)

        # 计算韦伯分布风险函数
        weibull_hazards = [self.weibull_hazard(t_i, k, lam) for t_i in t]

        # 计算等效的指数分布风险率（平均风险相同）
        equivalent_exp_rate = 1 / (lam * np.math.gamma(1 + 1 / k))
        exp_hazards = [equivalent_exp_rate] * len(t)

        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(t, weibull_hazards, 'r-', label=f'韦伯分布 (k={k:.2f}, λ={lam:.2f})', linewidth=2)
        plt.plot(t, exp_hazards, 'b--', label=f'指数分布 (λ={equivalent_exp_rate:.4f})', linewidth=2)
        plt.xlabel('时间')
        plt.ylabel('风险率')
        plt.title('风险函数对比')
        plt.legend()
        plt.grid(True)

        plt.subplot(1, 2, 2)
        weibull_survival = [self.weibull_survival(t_i, k, lam) for t_i in t]
        exp_survival = [np.exp(-equivalent_exp_rate * t_i) for t_i in t]

        plt.plot(t, weibull_survival, 'r-', label='韦伯分布', linewidth=2)
        plt.plot(t, exp_survival, 'b--', label='指数分布', linewidth=2)
        plt.xlabel('时间')
        plt.ylabel('生存概率')
        plt.title('生存函数对比')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    def plot_results(self, results, k, lam):
        """绘制结果图表"""
        # 计算各年龄段患病率
        ages, prevalence = self.calculate_prevalence_by_age(results)

        # 计算发病率
        incidence_rate, incidence_count, at_risk_count = self.calculate_incidence_rate(results, 50, 55)

        # 绘制患病率曲线
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.plot(ages, prevalence, 'b-', linewidth=2)
        plt.xlabel('年龄')
        plt.ylabel('患病率')
        plt.title(f'疾病患病率随年龄变化 (k={k:.4f}, λ={lam:.4f})')
        plt.grid(True)

        # 绘制最终状态分布
        plt.subplot(2, 2, 2)
        final_states = [r['final_state'] for r in results]
        state_counts = pd.Series(final_states).value_counts()
        plt.bar(state_counts.index, state_counts.values)
        plt.xlabel('最终状态')
        plt.ylabel('人数')
        plt.title('最终状态分布')

        # 绘制年龄分布
        plt.subplot(2, 2, 3)
        final_ages = [r['final_age'] for r in results]
        plt.hist(final_ages, bins=30, alpha=0.7, edgecolor='black')
        plt.xlabel('最终年龄')
        plt.ylabel('频数')
        plt.title('最终年龄分布')

        # 显示统计信息
        plt.subplot(2, 2, 4)
        plt.axis('off')
        stats_text = f"""
        统计信息:
        模拟个体数: {self.n_simulations}
        韦伯参数 k: {k:.6f}
        韦伯参数 λ: {lam:.6f}
        50-55岁HCC发病率: {incidence_rate:.6f}
        发病人数: {incidence_count}
        风险人群: {at_risk_count}
        平均最终年龄: {np.mean(final_ages):.2f}
        """
        plt.text(0.1, 0.5, stats_text, fontsize=10, verticalalignment='center')

        plt.tight_layout()
        plt.show()


# 使用示例
if __name__ == "__main__":
    # 创建韦伯分布事件模拟模型实例
    model = HCCWeibullEventModel(initial_population=10000, max_age=85, n_simulations=5000)

    # 设置基础危险率
    model.set_hazard_rates(
        health_to_chb=0.04,
        health_to_death=0.01,
        chb_to_cc=0.08,
        chb_to_death=0.03,
        cc_to_death=0.06,
        hcc_to_death=0.25
    )

    # 测试特定韦伯参数
    k_test, lam_test = 1.8, 15.0
    print(f"测试 k={k_test}, λ={lam_test}")
    model.set_weibull_params(k_test, lam_test)
    results = model.simulate_population(k_test, lam_test)

    # 计算50-55岁发病率
    incidence_rate, incidence_count, at_risk_count = model.calculate_incidence_rate(results, 50, 55)
    print(f"50-55岁HCC发病率: {incidence_rate:.6f}")
    print(f"发病人数: {incidence_count}")
    print(f"风险人群: {at_risk_count}")

    # 绘制韦伯分布对比图
    # model.plot_weibull_comparison(k_test, lam_test)

    # 优化韦伯分布参数以达到目标发病率
    target_incidence = 0.015  # 1.5%的50-55岁发病率
    loss, optimal_k, optimal_lam = model.optimize_weibull_params(target_incidence)

    print(f"\n优化结果:")
    print(f"目标发病率: {target_incidence}")
    print(f"最优k参数: {optimal_k:.6f}")
    print(f"最优λ参数: {optimal_lam:.6f}")
    print(f"损失值: {loss:.6e}")

    # 使用最优参数重新模拟并绘制结果
    optimal_results = model.simulate_population(optimal_k, optimal_lam)
    optimal_incidence, _, _ = model.calculate_incidence_rate(optimal_results, 50, 55)
    print(f"最优参数下的50-55岁发病率: {optimal_incidence:.6f}")

    # 绘制结果图表
    # model.plot_results(optimal_results, optimal_k, optimal_lam)

    # 绘制最优参数的韦伯分布对比
    # model.plot_weibull_comparison(optimal_k, optimal_lam)