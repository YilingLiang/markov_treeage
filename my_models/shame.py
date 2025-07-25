from cmd.markov_model import MarkovModel
import numpy as np
from cmd.time_dependency import ProbabilityTools
from cmd.strategy import Strategy
from cmd.sensitivity import SensitivityAnalysis


# 1. 定义状态和初始模型
states = ["pre", "symp", "death"]
init_state = {"pre": 1.0, "symp": 0.0, "death": 0.0}
model = MarkovModel(states, init_state)


# 2. 定义转移矩阵函数（时间依赖）
def transition_func(cycle, params):
    n_states = 3
    t = np.zeros((n_states, n_states))
    # 状态索引
    i_pre, i_symp, i_death = 0, 1, 2

    # 从pre转移
    p_disease = params["p_disease_base"] if cycle == 1 else params["p_disease_base"] * 0.9  # 示例时间依赖
    p_death_all = params["p_death_all"]
    t[i_pre, i_pre] = 1 - p_disease - p_death_all  # 留在pre
    t[i_pre, i_symp] = p_disease # pre 转移到 symp
    t[i_pre, i_death] = p_death_all # pre 转移到 death

    # 从symp转移
    p_cured = params["p_cured"]
    p_death_symp = ProbabilityTools.combine_probs(p_death_all, params["p_death_disease"])
    t[i_symp, i_pre] = p_cured
    t[i_symp, i_symp] = 1 - p_cured - p_death_symp
    t[i_symp, i_death] = p_death_symp

    # 死亡状态固定
    t[i_death, i_death] = 1.0
    return t


model.set_transition_matrix(transition_func)


# 3. 定义成本和效果函数
def cost_func(state, model_time, state_time, params):
    if state == "pre":
        return params["cost_med"] if model_time <= 5 else 0  # 示例时间依赖成本
    elif state == "symp":
        return params["cost_hospit_start"] if state_time < 3 else params["cost_hospit_end"]
    else:
        return 0


def effect_func(state, model_time, state_time, params):
    if state == "pre":
        return 1.0
    elif state == "symp":
        return params["qaly_disease"]
    else:
        return 0.0


model.set_state_values(cost_func, effect_func)

# 4. 定义参数
params = {
    "p_disease_base": 0.25,
    "p_death_all": 0.01,
    "p_death_disease": 0.1,
    "p_cured": 0.001,
    "cost_med": 5000,
    "cost_hospit_start": 11000,
    "cost_hospit_end": 9000,
    "qaly_disease": 0.5,
    "dr": 0.05
}

# 5. 运行基础策略
strat_base = Strategy("base", model, params)
strat_base.run(cycles=10)
print(f"基础策略总成本: {strat_base.results['total_cost']:.2f}")
print(f"基础策略总效果(QALY): {strat_base.results['total_effect']:.2f}")

# 6. 运行DSA
params_ranges = {"p_disease_base": (0.2, 0.3), "p_death_all": (0.005, 0.015)}
dsa_results = SensitivityAnalysis.dsa(strat_base, params_ranges, cycles=10)
print("++++++: ", dsa_results)