import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from symengine import Matrix, sympify, zeros, lambdify, symbols, Add, Mul, Basic, sqrt, exp, log
from scipy.optimize import minimize
from scipy.integrate import odeint

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class HCCSurvivalModel:
    """
    Time-to-Event model for HCC progression with 5 states
    States: [health, chb, cc, hcc, death]
    Uses hazard rates instead of transition probabilities
    """

    def __init__(self, initial_population=10000, max_time=20):
        self.initial_population = initial_population
        self.max_time = max_time
        self.hazard_rates = None
        self.cc_to_hcc_hazard = symbols('cc_to_hcc_hazard')  # 符号危险率
        self.survival_functions = None
        self.cumulative_hazards = None

    def set_hazard_rates(self,
                         health_to_chb=0.04,
                         health_to_death=0.01,
                         chb_to_cc=0.08,
                         chb_to_death=0.03,
                         cc_to_death=0.06,
                         hcc_to_death=0.25):
        """
        设置危险率（瞬时风险率）
        使用符号变量cc_to_hcc_hazard
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

    def calculate_survival_functions(self):
        """计算各状态的生存函数（符号表达式）"""
        t = symbols('t')  # 时间变量

        # 健康状态的生存函数
        S_health = exp(-(self.hazard_rates['health_to_chb'] +
                         self.hazard_rates['health_to_death']) * t)

        # CHB状态的生存函数（从健康状态转移而来）
        S_chb = (self.hazard_rates['health_to_chb'] /
                 (self.hazard_rates['health_to_chb'] + self.hazard_rates['health_to_death'] -
                  self.hazard_rates['chb_to_cc'] - self.hazard_rates['chb_to_death'])) * \
                (exp(-(self.hazard_rates['chb_to_cc'] + self.hazard_rates['chb_to_death']) * t) -
                 exp(-(self.hazard_rates['health_to_chb'] + self.hazard_rates['health_to_death']) * t))

        # CC状态的生存函数（需要积分计算）
        # 这里简化处理，使用近似表达式
        lambda_cc = self.hazard_rates['cc_to_hcc'] + self.hazard_rates['cc_to_death']
        S_cc = exp(-lambda_cc * t)

        # HCC状态的生存函数
        S_hcc = exp(-self.hazard_rates['hcc_to_death'] * t)

        self.survival_functions = {
            'S_health': S_health,
            'S_chb': S_chb,
            'S_cc': S_cc,
            'S_hcc': S_hcc
        }

        return self.survival_functions

    def calculate_cumulative_incidence(self):
        """计算累积发病率（符号表达式）"""
        t = symbols('t')

        # 从健康到CHB的累积发病率
        F_chb = 1 - exp(-self.hazard_rates['health_to_chb'] * t)

        # 从CHB到CC的累积发病率
        F_cc = 1 - exp(-self.hazard_rates['chb_to_cc'] * t)

        # 从CC到HCC的累积发病率（使用符号变量）
        F_hcc = 1 - exp(-self.hazard_rates['cc_to_hcc'] * t)

        self.cumulative_incidence = {
            'F_chb': F_chb,
            'F_cc': F_cc,
            'F_hcc': F_hcc
        }

        return self.cumulative_incidence

    def simulate_time_to_event(self, cc_to_hcc_value):
        """使用数值方法模拟Time-to-Event过程"""

        # 定义微分方程组
        def model(y, t, params):
            health, chb, cc, hcc, death = y
            h2chb, h2d, chb2cc, chb2d, cc2hcc, cc2d, hcc2d = params

            dhealth_dt = - (h2chb + h2d) * health
            dchb_dt = h2chb * health - (chb2cc + chb2d) * chb
            dcc_dt = chb2cc * chb - (cc2hcc + cc2d) * cc
            dhcc_dt = cc2hcc * cc - hcc2d * hcc
            ddeath_dt = h2d * health + chb2d * chb + cc2d * cc + hcc2d * hcc

            return [dhealth_dt, dchb_dt, dcc_dt, dhcc_dt, ddeath_dt]

        # 参数设置
        params = (
            self.hazard_rates['health_to_chb'],
            self.hazard_rates['health_to_death'],
            self.hazard_rates['chb_to_cc'],
            self.hazard_rates['chb_to_death'],
            cc_to_hcc_value,  # 使用具体数值
            self.hazard_rates['cc_to_death'],
            self.hazard_rates['hcc_to_death']
        )

        # 初始条件
        y0 = [self.initial_population, 0, 0, 0, 0]

        # 时间点
        t = np.linspace(0, self.max_time, self.max_time + 1)

        # 求解微分方程
        solution = odeint(model, y0, t, args=(params,))

        return t, solution

    def calculate_prevalence_time_to_event(self, cc_to_hcc_value):
        """计算Time-to-Event模型的患病率"""
        t, solution = self.simulate_time_to_event(cc_to_hcc_value)

        prevalence = []
        for i in range(len(t)):
            health, chb, cc, hcc, death = solution[i]
            alive_population = health + chb + cc + hcc
            disease_cases = chb + cc + hcc

            if alive_population > 0:
                prevalence.append(disease_cases / alive_population)
            else:
                prevalence.append(0)

        return t, prevalence

    def optimize_cc_to_hcc(self, target_prevalence, time_point=20):
        """优化cc_to_hcc参数以达到目标患病率"""

        # 定义目标函数
        def objective(cc_to_hcc_value):
            t, prevalence = self.calculate_prevalence_time_to_event(cc_to_hcc_value[0])
            # 找到指定时间点的患病率
            idx = np.where(t == time_point)[0]
            if len(idx) > 0:
                return (prevalence[idx[0]] - target_prevalence) ** 2
            else:
                return float('inf')

        # 优化
        result = minimize(objective, [0.02], method='L-BFGS-B', bounds=[(0, 1)])

        return result.fun, result.x[0]

    def get_prevalence_function_symbolic(self):
        """获取患病率的符号表达式函数"""
        # 这里需要更复杂的符号推导，简化版本
        t = symbols('t')
        lambda_h = self.hazard_rates['health_to_chb'] + self.hazard_rates['health_to_death']
        lambda_c = self.hazard_rates['chb_to_cc'] + self.hazard_rates['chb_to_death']
        lambda_cc = self.cc_to_hcc_hazard + self.hazard_rates['cc_to_death']
        lambda_hcc = self.hazard_rates['hcc_to_death']

        # 近似患病率表达式
        prevalence = (self.hazard_rates['health_to_chb'] * (1 - exp(-lambda_c * t)) / lambda_c +
                      self.hazard_rates['chb_to_cc'] * (1 - exp(-lambda_cc * t)) / lambda_cc)

        func = lambdify((t, self.cc_to_hcc_hazard), prevalence)
        return func


# 使用示例
if __name__ == "__main__":
    # 创建Time-to-Event模型实例
    survival_model = HCCSurvivalModel(initial_population=10000, max_time=20)

    # 设置危险率
    survival_model.set_hazard_rates(
        health_to_chb=0.04,
        health_to_death=0.01,
        chb_to_cc=0.08,
        chb_to_death=0.03,
        cc_to_death=0.06,
        hcc_to_death=0.25
    )

    # 计算生存函数和累积发病率
    survival_funcs = survival_model.calculate_survival_functions()
    incidence_funcs = survival_model.calculate_cumulative_incidence()

    print("生存函数:")
    for state, func in survival_funcs.items():
        print(f"{state}: {func}")

    print("\n累积发病率:")
    for transition, func in incidence_funcs.items():
        print(f"{transition}: {func}")

    # 测试特定cc_to_hcc值
    cc_to_hcc_test = 0.12
    t, prevalence = survival_model.calculate_prevalence_time_to_event(cc_to_hcc_test)

    print(f"\n第20年患病率 (cc_to_hcc={cc_to_hcc_test}): {prevalence[-1]:.4f}")

    # 优化cc_to_hcc参数
    target_prev = 0.45
    loss, optimal_cc_to_hcc = survival_model.optimize_cc_to_hcc(target_prev)

    print(f"\n优化结果:")
    print(f"目标患病率: {target_prev}")
    print(f"最优cc_to_hcc: {optimal_cc_to_hcc:.6f}")
    print(f"损失值: {loss:.6e}")

    # 验证优化结果
    t, final_prevalence = survival_model.calculate_prevalence_time_to_event(optimal_cc_to_hcc)
    print(f"第20年实际患病率: {final_prevalence[-1]:.6f}")

    # 绘制患病率曲线
    plt.figure(figsize=(10, 6))
    plt.plot(t, prevalence, 'b-', label=f'cc_to_hcc={cc_to_hcc_test}')
    plt.plot(t, final_prevalence, 'r--', label=f'优化后 cc_to_hcc={optimal_cc_to_hcc:.4f}')
    plt.axhline(y=target_prev, color='g', linestyle=':', label=f'目标患病率={target_prev}')
    plt.xlabel('时间 (年)')
    plt.ylabel('患病率')
    plt.title('Time-to-Event模型患病率曲线')
    plt.legend()
    plt.grid(True)
    plt.show()