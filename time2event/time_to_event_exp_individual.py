import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from symengine import symbols, exp
from scipy.optimize import minimize
from scipy.stats import expon
import time

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class HCCDiscreteEventModel:
    """
    Discrete Event Simulation for HCC progression with 5 states
    States: [health, chb, cc, hcc, death]
    Uses exponential distributions for transition times
    """

    def __init__(self, initial_population=10000, max_age=85, n_simulations=1000):
        self.initial_population = initial_population
        self.max_age = max_age
        self.n_simulations = n_simulations
        self.hazard_rates = None
        self.cc_to_hcc_hazard = symbols('cc_to_hcc_hazard')  # 符号危险率

    def set_hazard_rates(self,
                         health_to_chb=0.04,
                         health_to_death=0.01,
                         chb_to_cc=0.08,
                         chb_to_death=0.03,
                         cc_to_death=0.06,
                         hcc_to_death=0.25):
        """
        设置危险率（瞬时风险率）
        使用符号变量 cc_to_hcc_hazard
        """
        self.hazard_rates = {
            'health_to_chb': health_to_chb,
            'health_to_death': health_to_death,
            'chb_to_cc': chb_to_cc,
            'chb_to_death': chb_to_death,
            'cc_to_death': cc_to_death,
            'cc_to_hcc': self.cc_to_hcc_hazard,  # 符号变量
            'hcc_to_death': hcc_to_death
        }

    def simulate_individual(self, cc_to_hcc_value, current_age=0):
        """
        模拟单个个体的疾病进展过程
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
                if 'cc_to_hcc' in transition:
                    actual_rate = cc_to_hcc_value
                else:
                    actual_rate = rate

                # 指数分布采样：时间 = -ln(U)/λ
                if actual_rate > 0:
                    u = rng.random()
                    transition_time = -np.log(u) / actual_rate if u > 0 else float('inf')
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
                'cc_to_hcc': self.hazard_rates['cc_to_hcc'],
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

    def simulate_population(self, cc_to_hcc_value):
        """模拟整个群体的疾病进展"""
        results = []

        print(f"开始模拟 {self.n_simulations} 个个体...")
        start_time = time.time()

        for i in range(self.n_simulations):
            if (i + 1) % 1000 == 0:
                print(f"已模拟 {i + 1} 个个体")

            state_history, time_history = self.simulate_individual(cc_to_hcc_value)
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
            for i in range(1, len(state_history)):
                if (state_history[i] == 'hcc' and state_history[i - 1] != 'hcc' and
                        age_start <= time_history[i] <= age_end):
                    incidence_count += 1
                    break

            # 计算风险人群：在50岁时存活且未患HCC
            for i in range(len(time_history)):
                if time_history[i] >= age_start:
                    if state_history[i] in ['health', 'chb', 'cc']:
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

    def optimize_cc_to_hcc(self, target_incidence, age_start=50, age_end=55):
        """优化cc_to_hcc参数以达到目标发病率（50-55岁）"""

        def objective(cc_to_hcc_value):
            print(f"测试 cc_to_hcc = {cc_to_hcc_value[0]:.6f}")
            results = self.simulate_population(cc_to_hcc_value[0])
            incidence_rate, _, _ = self.calculate_incidence_rate(results, age_start, age_end)
            loss = (incidence_rate - target_incidence) ** 2
            print(f"发病率: {incidence_rate:.6f}, 目标: {target_incidence}, 损失: {loss:.6e}")
            return loss

        # 优化
        print(f"开始优化，目标发病率: {target_incidence} (年龄 {age_start}-{age_end}岁)")
        result = minimize(objective, [0.02], method='L-BFGS-B', bounds=[(0.001, 0.5)])

        return result.fun, result.x[0]

    def plot_results(self, results, cc_to_hcc_value):
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
        plt.title(f'疾病患病率随年龄变化 (cc_to_hcc={cc_to_hcc_value:.4f})')
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
        cc_to_hcc值: {cc_to_hcc_value:.6f}
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
    # 创建离散事件模拟模型实例
    model = HCCDiscreteEventModel(initial_population=10000, max_age=85, n_simulations=1000)

    # 设置危险率
    model.set_hazard_rates(
        health_to_chb=0.04,
        health_to_death=0.01,
        chb_to_cc=0.08,
        chb_to_death=0.03,
        cc_to_death=0.06,
        hcc_to_death=0.25
    )

    # 测试特定cc_to_hcc值
    cc_to_hcc_test = 0.12
    print(f"测试 cc_to_hcc = {cc_to_hcc_test}")
    results = model.simulate_population(cc_to_hcc_test)
    # print(results)


    # 计算50-55岁发病率
    incidence_rate, incidence_count, at_risk_count = model.calculate_incidence_rate(results, 50, 55)
    print(f"50-55岁HCC发病率: {incidence_rate:.6f}")
    print(f"发病人数: {incidence_count}")
    print(f"风险人群: {at_risk_count}")

    # 优化cc_to_hcc参数以达到目标发病率
    target_incidence = 0.015  # 1.5%的50-55岁发病率
    loss, optimal_cc_to_hcc = model.optimize_cc_to_hcc(target_incidence)

    print(f"\n优化结果:")
    print(f"目标发病率: {target_incidence}")
    print(f"最优cc_to_hcc(\lambda): {optimal_cc_to_hcc:.6f}")
    print(f"损失值: {loss:.6e}")

    # 使用最优参数重新模拟并绘制结果
    optimal_results = model.simulate_population(optimal_cc_to_hcc)
    optimal_incidence, _, _ = model.calculate_incidence_rate(optimal_results, 50, 55)
    print(f"最优参数下的50-55岁发病率: {optimal_incidence:.6f}")

    # 绘制结果图表
    # model.plot_results(optimal_results, optimal_cc_to_hcc)

