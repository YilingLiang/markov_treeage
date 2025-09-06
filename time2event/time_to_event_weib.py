import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from symengine import symbols, exp, lambdify
from scipy.optimize import minimize
from scipy.integrate import odeint
from scipy.stats import weibull_min


class HCCSurvivalWeibullModel:
    """
    Time-to-Event model with Weibull distribution for cc_to_hcc transition
    States: [health, chb, cc, hcc, death]
    """

    def __init__(self, initial_population=10000, max_time=20):
        self.initial_population = initial_population
        self.max_time = max_time
        self.hazard_rates = None
        self.weibull_shape = symbols('weibull_shape')  # 韦伯分布形状参数 k (\alpha)
        self.weibull_scale = symbols('weibull_scale')  # 韦伯分布尺度参数 λ (\beta)

    def set_hazard_rates(self,
                         health_to_chb=0.04,
                         health_to_death=0.01,
                         chb_to_cc=0.08,
                         chb_to_death=0.03,
                         cc_to_death=0.06,
                         hcc_to_death=0.25):
        """
        设置危险率（瞬时风险率）
        cc_to_hcc使用韦伯分布
        """
        self.hazard_rates = {
            'health_to_chb': health_to_chb,
            'health_to_death': health_to_death,
            'chb_to_cc': chb_to_cc,
            'chb_to_death': chb_to_death,
            'cc_to_death': cc_to_death,
            'hcc_to_death': hcc_to_death
        }

    def weibull_hazard(self, t, shape, scale):
        """韦伯分布危险函数"""
        return (shape / scale) * (t / scale) ** (shape - 1)

    def weibull_survival(self, t, shape, scale):
        """韦伯分布生存函数"""
        return exp(-(t / scale) ** shape)

    def simulate_time_to_event_weibull(self, shape, scale):
        """使用韦伯分布模拟Time-to-Event过程"""

        # 定义微分方程组
        def model(y, t, params):
            health, chb, cc, hcc, death = y
            h2chb, h2d, chb2cc, chb2d, cc2d, hcc2d = params

            # 计算时间相关的cc_to_hcc危险率（韦伯分布）
            cc2hcc = self.weibull_hazard(t, shape, scale)

            dhealth_dt = - (h2chb + h2d) * health
            dchb_dt = h2chb * health - (chb2cc + chb2d) * chb
            dcc_dt = chb2cc * chb - (cc2hcc + cc2d) * cc
            dhcc_dt = cc2hcc * cc - hcc2d * hcc
            ddeath_dt = h2d * health + chb2d * chb + cc2d * cc + hcc2d * hcc

            return [dhealth_dt, dchb_dt, dcc_dt, dhcc_dt, ddeath_dt]

        # 参数设置（固定参数）
        params = (
            self.hazard_rates['health_to_chb'],
            self.hazard_rates['health_to_death'],
            self.hazard_rates['chb_to_cc'],
            self.hazard_rates['chb_to_death'],
            self.hazard_rates['cc_to_death'],
            self.hazard_rates['hcc_to_death']
        )

        # 初始条件
        y0 = [self.initial_population, 0, 0, 0, 0]

        # 时间点
        t_points = np.linspace(0, self.max_time, self.max_time * 10 + 1)  # 更细的时间网格

        # 求解微分方程
        solution = odeint(model, y0, t_points, args=(params,))

        return t_points, solution

    def calculate_prevalence_weibull(self, shape, scale):
        """计算韦伯分布模型的患病率"""
        t, solution = self.simulate_time_to_event_weibull(shape, scale)

        prevalence = []
        for i in range(len(t)):
            health, chb, cc, hcc, death = solution[i]
            alive_population = health + chb + cc + hcc
            disease_cases = chb + cc + hcc

            if alive_population > 0:
                prevalence.append(disease_cases / alive_population)
            else:
                prevalence.append(0)

        return t, prevalence, solution

    def get_final_prevalence(self, shape, scale, target_time=20):
        """获取目标时间点的患病率"""
        t, prevalence, _ = self.calculate_prevalence_weibull(shape, scale)
        # 找到最接近目标时间点的索引
        idx = np.argmin(np.abs(t - target_time))
        return prevalence[idx]

    def optimize_weibull_params(self, target_prevalence, target_time=20,
                                initial_shape=1.5, initial_scale=10.0):
        """优化韦伯分布参数以达到目标患病率"""

        def objective(params):
            shape, scale = params
            try:
                final_prev = self.get_final_prevalence(shape, scale, target_time)
                loss = (final_prev - target_prevalence) ** 2
                return loss
            except:
                return float('inf')

        # 参数边界：形状参数k>0，尺度参数λ>0
        bounds = [(0.1, 5.0), (1.0, 50.0)]

        # 初始值
        initial_params = [initial_shape, initial_scale]

        # 优化
        result = minimize(objective, initial_params, method='L-BFGS-B',
                          bounds=bounds, options={'maxiter': 100})

        optimal_shape, optimal_scale = result.x
        final_loss = result.fun

        return optimal_shape, optimal_scale, final_loss

    def plot_weibull_hazard(self, shape, scale, title="韦伯分布危险函数"):
        """绘制韦伯分布危险函数"""
        t = np.linspace(0, self.max_time, 100)
        hazard = self.weibull_hazard(t, shape, scale)

        plt.figure(figsize=(10, 6))
        plt.plot(t, hazard, 'r-', linewidth=2)
        plt.xlabel('时间 (年)')
        plt.ylabel('危险率')
        plt.title(f'{title} (k={shape:.2f}, λ={scale:.2f})')
        plt.grid(True)
        plt.show()

    def plot_simulation_results(self, shape, scale, target_prevalence=None):
        """绘制模拟结果"""
        t, prevalence, solution = self.calculate_prevalence_weibull(shape, scale)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # 绘制各状态人数
        ax1.plot(t, solution[:, 0], 'g-', label='健康', linewidth=2)
        ax1.plot(t, solution[:, 1], 'b-', label='CHB', linewidth=2)
        ax1.plot(t, solution[:, 2], 'orange', label='CC', linewidth=2)
        ax1.plot(t, solution[:, 3], 'r-', label='HCC', linewidth=2)
        ax1.plot(t, solution[:, 4], 'k-', label='死亡', linewidth=2)
        ax1.set_xlabel('时间 (年)')
        ax1.set_ylabel('人数')
        ax1.set_title('各状态人数随时间变化')
        ax1.legend()
        ax1.grid(True)

        # 绘制患病率
        ax2.plot(t, prevalence, 'purple', linewidth=3, label='患病率')
        if target_prevalence is not None:
            ax2.axhline(y=target_prevalence, color='red', linestyle='--',
                        label=f'目标患病率: {target_prevalence}')
        ax2.set_xlabel('时间 (年)')
        ax2.set_ylabel('患病率')
        ax2.set_title('疾病患病率随时间变化')
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()


# 使用示例
if __name__ == "__main__":
    # 创建韦伯分布模型实例
    weibull_model = HCCSurvivalWeibullModel(initial_population=10000, max_time=20)

    # 设置危险率
    weibull_model.set_hazard_rates(
        health_to_chb=0.04,
        health_to_death=0.01,
        chb_to_cc=0.08,
        chb_to_death=0.03,
        cc_to_death=0.06,
        hcc_to_death=0.25
    )

    # 测试特定韦伯参数
    test_shape, test_scale = 1.8, 8.0
    t, prevalence, _ = weibull_model.calculate_prevalence_weibull(test_shape, test_scale)
    print(f"测试参数: k={test_shape}, λ={test_scale}")
    print(f"第20年患病率: {prevalence[-1]:.4f}")

    # 绘制韦伯危险函数
    weibull_model.plot_weibull_hazard(test_shape, test_scale)

    # 优化韦伯分布参数
    target_prev = 0.45
    optimal_shape, optimal_scale, loss = weibull_model.optimize_weibull_params(
        target_prevalence=target_prev,
        initial_shape=1.5,
        initial_scale=10.0
    )

    print(f"\n优化结果:")
    print(f"目标患病率: {target_prev}")
    print(f"最优形状参数 k: {optimal_shape:.6f}")
    print(f"最优尺度参数 λ: {optimal_scale:.6f}")
    print(f"损失值: {loss:.6e}")

    # 验证优化结果
    final_prev = weibull_model.get_final_prevalence(optimal_shape, optimal_scale)
    print(f"第20年实际患病率: {final_prev:.6f}")

    # 绘制优化前后的对比
    weibull_model.plot_simulation_results(optimal_shape, optimal_scale, target_prev)

    # 比较不同形状参数的影响
    shapes = [0.8, 1.5, 3.0]  # k < 1:递减危险，k = 1:恒定危险，k > 1:递增危险
    scale_fixed = 10.0

    plt.figure(figsize=(10, 6))
    for shape in shapes:
        t, prevalence, _ = weibull_model.calculate_prevalence_weibull(shape, scale_fixed)
        plt.plot(t, prevalence, label=f'k={shape}, λ={scale_fixed}')

    plt.axhline(y=target_prev, color='red', linestyle='--', label=f'目标患病率')
    plt.xlabel('时间 (年)')
    plt.ylabel('患病率')
    plt.title('不同形状参数对患病率的影响')
    plt.legend()
    plt.grid(True)
    plt.show()