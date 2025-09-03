import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 设置随机种子以确保结果可重现
np.random.seed(42)


class FiveStateMarkovModel:
    def __init__(self, initial_population=10000, years=20):
        self.initial_population = initial_population
        self.years = years
        self.transition_matrix = None
        self.results = None

    def set_transition_probabilities(self,
                                     health_to_chb=0.04,
                                     health_to_death=0.01,
                                     chb_to_cc=0.08,
                                     chb_to_death=0.03,
                                     cc_to_hcc=0.12,
                                     cc_to_death=0.06,
                                     hcc_to_death=0.25):
        """
        设置五状态转移概率
        状态: 0=health, 1=chb, 2=cc, 3=hcc, 4=death
        """
        self.transition_matrix = np.array([
            # health 到: [health, chb, cc, hcc, death]
            [1 - health_to_chb - health_to_death, health_to_chb, 0, 0, health_to_death],
            # chb 到: [health, chb, cc, hcc, death]
            [0, 1 - chb_to_cc - chb_to_death, chb_to_cc, 0, chb_to_death],
            # cc 到: [health, chb, cc, hcc, death]
            [0, 0, 1 - cc_to_hcc - cc_to_death, cc_to_hcc, cc_to_death],
            # hcc 到: [health, chb, cc, hcc, death]
            [0, 0, 0, 1 - hcc_to_death, hcc_to_death],
            # death 到: [health, chb, cc, hcc, death] (死亡是吸收状态)
            [0, 0, 0, 0, 1]
        ])

    def simulate(self):
        """运行马尔科夫模拟"""
        # 初始化状态向量
        state_vector = np.array([self.initial_population, 0, 0, 0, 0])

        # 存储每年的结果
        self.results = np.zeros((self.years + 1, 5))
        self.results[0] = state_vector

        # 逐年模拟
        for year in range(1, self.years + 1):
            new_state = np.zeros(5)

            # 对每个状态的人群应用转移概率
            for from_state in range(5):
                # 当前处于from_state状态的人数
                current_count = state_vector[from_state]

                # 如果没有人处于该状态，则跳过
                if current_count == 0:
                    continue

                # 计算转移到各状态的人数
                transitions = np.random.multinomial(current_count, self.transition_matrix[from_state])

                # 累加到新状态
                for to_state in range(5):
                    new_state[to_state] += transitions[to_state]

            # 更新状态向量
            state_vector = new_state
            self.results[year] = state_vector

        return self.results

    def get_results_table(self):
        """返回结果为DataFrame"""
        if self.results is None:
            print("请先运行模拟")
            return

        return pd.DataFrame(self.results,
                            columns=['Health', 'CHB', 'CC', 'HCC', 'Death'],
                            index=range(self.years + 1))

    def calculate_prevalence(self):
        """计算每年的疾病患病率"""
        if self.results is None:
            print("请先运行模拟")
            return

        # 总患病率 = (CHB + CC + HCC) / 总存活人口
        alive_population = self.results[:, 0:4].sum(axis=1)
        disease_cases = self.results[:, 1:4].sum(axis=1)
        prevalence = np.divide(disease_cases, alive_population,
                               out=np.zeros_like(disease_cases),
                               where=alive_population != 0)

        return prevalence


if __name__ == "__main__":
    # 创建模型实例
    model = FiveStateMarkovModel(initial_population=10000, years=20)

    # 设置转移概率
    model.set_transition_probabilities(
        health_to_chb=0.04,  # 每年health到chb的概率
        health_to_death=0.01,  # 每年health到death的概率(其他原因)
        chb_to_cc=0.08,  # 每年chb到cc的概率
        chb_to_death=0.03,  # 每年chb到death的概率
        cc_to_hcc=0.12,  # 每年cc到hcc的概率
        cc_to_death=0.06,  # 每年cc到death的概率
        hcc_to_death=0.25  # 每年hcc到death的概率
    )

    # 运行模拟
    results = model.simulate()

    # 显示结果表格
    results_df = model.get_results_table()
    print("五状态马尔科夫模拟结果:")
    print(results_df.round(0))

    # 计算并显示患病率
    prevalence = model.calculate_prevalence()
    prevalence_df = pd.DataFrame({
        'Year': range(21),
        'Prevalence': prevalence
    })
    print("\n每年疾病患病率:")
    print(prevalence_df.round(4))

    # 显示最终状态
    final_state = results_df.iloc[-1]
    print("\n20年后最终状态:")
    print(f"Health: {final_state['Health']:.0f}人")
    print(f"CHB: {final_state['CHB']:.0f}人")
    print(f"CC: {final_state['CC']:.0f}人")
    print(f"HCC: {final_state['HCC']:.0f}人")
    print(f"Death: {final_state['Death']:.0f}人")
    print(f"总存活人数: {final_state['Health'] + final_state['CHB'] + final_state['CC'] + final_state['HCC']:.0f}人")
    print(f"疾病总患病率: {prevalence[-1]:.4f} ({prevalence[-1] * 100:.2f}%)")
