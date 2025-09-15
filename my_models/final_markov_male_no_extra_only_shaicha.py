"""
对 male_0713_single.trex TreeAge 文件的 Python 实现
"""
import numpy as np
from lab.markov_tunnel_db_v5_no_cu import MarkovModel, State, discount
from lab.condition import create_condition, create_condition_gq_leq
from parameter.define_parameters import Parameters
from parameter.define_tables import Table
import matplotlib.pyplot as plt
from my_models.my_utils.utility import state_utility_func # 用于处理半周期矫正


def my_treeage_shaicha():
    # region ===== 参数表格定义: tables definition =====
    Death = Table({0: 0.0003639,
 1: 0.000348633,
 2: 0.000298643,
 3: 0.000262167,
 4: 0.000232254,
 5: 0.0001753,
 6: 0.000183355,
 7: 0.000180006,
 8: 0.000192406,
 9: 0.000220776,
 10: 0.0002317,
 11: 0.000253712,
 12: 0.000236616,
 13: 0.000272836,
 14: 0.000261231,
 15: 0.0002827,
 16: 0.000247997,
 17: 0.000247046,
 18: 0.000240065,
 19: 0.000240099,
 20: 0.0002454,
 21: 0.000314936,
 22: 0.000345656,
 23: 0.000387939,
 24: 0.000507121,
 25: 0.0005246,
 26: 0.000570297,
 27: 0.000579243,
 28: 0.000661445,
 29: 0.000668377,
 30: 0.0007345,
 31: 0.000766685,
 32: 0.000809596,
 33: 0.000781672,
 34: 0.0007745,
 35: 0.0008009,
 36: 0.000863496,
 37: 0.000889723,
 38: 0.001116294,
 39: 0.001079593,
 40: 0.0012295,
 41: 0.001373639,
 42: 0.001419426,
 43: 0.001782734,
 44: 0.00170824,
 45: 0.0019684,
 46: 0.00258378,
 47: 0.003389281,
 48: 0.003982865,
 49: 0.004234744,
 50: 0.0048895,
 51: 0.00427538,
 52: 0.004393411,
 53: 0.004291788,
 54: 0.004600593,
 55: 0.0041088,
 56: 0.005533944,
 57: 0.006287122,
 58: 0.007945187,
 59: 0.008607872,
 60: 0.00981,
 61: 0.011931475,
 62: 0.012891335,
 63: 0.01408957,
 64: 0.014166721,
 65: 0.0161622,
 66: 0.016079008,
 67: 0.018408482,
 68: 0.021124132,
 69: 0.021770405,
 70: 0.0243536,
 71: 0.027086662,
 72: 0.027473872,
 73: 0.032231874,
 74: 0.03863794,
 75: 0.0380657,
 76: 0.047062558,
 77: 0.056195749,
 78: 0.064587912,
 79: 0.062127639,
 80: 0.073152,
 81: 0.073152,
 82: 0.073152,
 83: 0.073152,
 84: 0.073152,
 85: 0.073152})
    HCCIdeath = Table({
    0: 0.014869866,
    5: 0.016110211,
    10: 0.017078674,
    15: 0.018212421,
    20: 0.020263037,
    25: 0.02796458,
    30: 0.059530759,
    35: 0.113428492,
    40: 0.151244794,
    45: 0.170933205,
    50: 0.171417444,
    55: 0.171512303,
    60: 0.17839755,
    65: 0.210762162,
    70: 0.212052307,
    75: 0.243446998,
    80: 0.281806659
})
    HCCIIdeath = Table({
    0: 0.016302651,
    5: 0.01841458,
    10: 0.019963678,
    15: 0.021610312,
    20: 0.02414665,
    25: 0.035744155,
    30: 0.088645402,
    35: 0.15578178,
    40: 0.170345144,
    45: 0.190916262,
    50: 0.191327152,
    55: 0.191390276,
    60: 0.240499344,
    65: 0.247553325,
    70: 0.2483359,
    75: 0.298192654,
    80: 0.334219521
})
    HCCIIIdeath = Table({
    0: 0.019718944,
    5: 0.022355104,
    10: 0.026443191,
    15: 0.028492641,
    20: 0.03123555,
    25: 0.043856577,
    30: 0.117407756,
    35: 0.163849627,
    40: 0.177778372,
    45: 0.195821671,
    50: 0.196658741,
    55: 0.196747608,
    60: 0.247369002,
    65: 0.269723986,
    70: 0.270798304,
    75: 0.305084664,
    80: 0.373460473
})
    HCCIVdeath = Table({
    0: 0.026847398,
    5: 0.027747398,
    10: 0.033057726,
    15: 0.035484783,
    20: 0.038809733,
    25: 0.06102273,
    30: 0.139676425,
    35: 0.172298758,
    40: 0.180292214,
    45: 0.196741663,
    50: 0.393272463,
    55: 0.393427116,
    60: 0.394183758,
    65: 0.395040231,
    70: 0.395708372,
    75: 0.39697946,
    80: 0.398641114
})
    pHBVToHCCI = Table({0: 0.00052,
 5: 0.00052,
 10: 0.00052,
 15: 0.00052,
 20: 0.00052,
 25: 0.00052,
 30: 0.0052,
 35: 0.0052,
 40: 0.0052,
 45: 0.0052,
 50: 0.0052,
 55: 0.0052,
 60: 0.005,
 65: 0.005,
 70: 0.0052,
 75: 0.005,
 80: 0.005,
 85: 0.0052})
    pHCCIIITocHCCIII = Table({0: 0.421721,
 5: 0.421721,
 10: 0.421721,
 15: 0.421721,
 20: 0.421721,
 25: 0.421721,
 30: 0.421721,
 35: 0.421721,
 40: 0.421721,
 45: 0.421721,
 50: 0.421721,
 55: 0.421721,
 60: 0.421721,
 65: 0.421721,
 70: 0.421721,
 75: 0.421721,
 80: 0.421721})
    pHCCIITocHCCII = Table({0: 0.242104,
 5: 0.242104,
 10: 0.242104,
 15: 0.242104,
 20: 0.242104,
 25: 0.242104,
 30: 0.242104,
 35: 0.242104,
 40: 0.242104,
 45: 0.242104,
 50: 0.242104,
 55: 0.242104,
 60: 0.242104,
 65: 0.242104,
 70: 0.242104,
 75: 0.242104,
 80: 0.242104})
    pHCCITocHCCI = Table({0: 0.063222,
 5: 0.063222,
 10: 0.063222,
 15: 0.063222,
 20: 0.063222,
 25: 0.063222,
 30: 0.063222,
 35: 0.063222,
 40: 0.063222,
 45: 0.063222,
 50: 0.063222,
 55: 0.063222,
 60: 0.063222,
 65: 0.063222,
 70: 0.063222,
 75: 0.063222,
 80: 0.063222})
    pHCCIVTocHCCIV = Table({0: 0.6,
 5: 0.6,
 10: 0.6,
 15: 0.6,
 20: 0.6,
 25: 0.6,
 30: 0.6,
 35: 0.6,
 40: 0.6,
 45: 0.6,
 50: 0.6,
 55: 0.6,
 60: 0.6,
 65: 0.6,
 70: 0.6,
 75: 0.6,
 80: 0.6})
    phealthToCHB = Table({
    0: 0.0000138362,
    5: 0.0000165356,
    10: 0.0000184963,
    15: 0.0000203399,
    20: 0.0000226021,
    25: 0.0000271386,
    30: 0.002856438,
    35: 0.005029424,
    40: 0.005032266,
    45: 0.0050335,
    50: 0.005034317,
    55: 0.005034858,
    60: 0.005035349,
    65: 0.005035991,
    70: 0.005037177,
    75: 0.00504195,
    80: 0.005555136
})
    ratescreen = Table({1: 0, 2: 1, 3: 1})
    Utility = Table({0: 1.0, 1: 0.761, 2: 0.643, 3: 0.76, 4: 0.68, 5: 0.4, 6: 0.25})
    # endregion

    # region ===== 参数定义 variables definition =====
    params = Parameters(
        Cost_AFP=(0.65, "AFP检测费用"),
        Cost_Diag=(90.03, "诊断费用"),
        Cost_HBsAgque=(0.07 + 2.22 + 0.65, "HBsAg检查费用（风险评估交通费+误工费+HBsAg检测）"),
        Cost_Treat_CC=(5688.29 + 1392.4, "肝硬化治疗费(直接+间接)"),
        Cost_Treat_DCC=(5688.29 + 1392.4, "失代偿"),
        Cost_Treat_HBV=(4563.5, "HBV治疗"),
        Cost_Treat_I=(9362.96 + 1651.45, ""),
        Cost_Treat_II=(9019.05 + 1960.32, ""),
        Cost_Treat_III=(8983.77 + 1808.38, ""),
        Cost_Treat_IV=(9588.45 + 1860.69, ""),
        Cost_US=(10 + 6.33 + 4.38 + 0.65, "超声检查费用（临床检查交通费+误工费+AFP+US）"),
        Cost_vac=(82.6, ""),
        cost_zhi_CC=(30657.7, "抗病毒治疗下肝硬化费用"),
        cost_zhi_CHB=(18689.5, "抗病毒治疗下慢乙肝费用"),
        cost_zhi_DCC=(43318.1, "抗病毒治疗下失代偿费用"),
        DR=(0.05, "贴现率"),
        dr=(0.00, "贴现率2"),
        p_CC_cure=(0.079, ""),
        p_CC_DCC=(0.058, "代偿肝硬化_失代偿肝硬化"),
        p_CC_DCC_treat=(0.019, "治疗后 代偿肝硬化_失代偿肝硬化"),
        p_CC_Death=(0.031, "代偿肝硬化_死于代偿肝硬化"),
        p_CC_Death_treat=(0.017, ""),
        p_CC_PHCCI=(0.0316, "代偿肝硬化_临床前I期"),
        p_CC_PHCCI_treat=(0.02, "治疗后 代偿肝硬化_临床前I期"),
        p_CC_treat=(0.7, ""),
        p_CC_zifa=(0.15, ""),
        p_DCC_cure=(0.033, ""),
        p_DCC_Death=(0.17, "失代偿肝硬化_死于失代偿肝硬化"),
        p_DCC_Death_treat=(0.095, ""),
        p_DCC_PHCCI=(0.034, "失代偿肝硬化_临床前I期"),
        p_DCC_PHCCI_treat=(0.024, ""),
        p_DCC_treat=(0.7, ""),
        p_DCC_zifa=(0.7, ""),
        p_Death=(Death, "xxx_死于其他原因"),
        p_HBV_CC=(0.0173, "慢性乙肝_代偿肝硬化"),
        p_HBV_pHCCI=(pHBVToHCCI, "慢性乙肝_临床前I期(---)"),
        p_HCC_treat=(0.0, ""),
        p_HCCI_Death=(HCCIdeath, "I期_死于肝癌"),
        p_HCCI_Detected=(pHCCITocHCCI, "临床前I期_I期"),
        p_HCCI_HCCII=(0.29, "临床前I期_临床前II期"),
        p_HCCII_Death=(HCCIIdeath, "II期_死于肝癌"),
        p_HCCII_Detected=(pHCCIITocHCCII, "临床前II期_II期"),
        p_HCCII_HCCIII=(0.4, "临床前II期_临床前III期"),
        p_HCCIII_Death=(HCCIIIdeath, "III期_死于肝癌"),
        p_HCCIII_Detected=(pHCCIIITocHCCIII, "临床前III期_III期"),
        p_HCCIII_HCCIV=(0.4, "临床前III期_临床前IV期"),
        p_HCCIV_Death=(HCCIVdeath, "IV期_死于肝癌"),
        p_HCCIV_Detected=(pHCCIVTocHCCIV, "临床前IV期_IV期"),
        p_health_CHB=(phealthToCHB, "健康_慢性乙肝"),
        p_health_pHCCI=(1 / 23.4 * pHBVToHCCI, "健康_临床前I期(---)"),  # 需要除以 23.4
        p_sHCCI_Death=(0.4 * HCCIdeath, ""),
        p_sHCCII_Death=(0.5 * HCCIIdeath, ""),
        p_sHCCIII_Death=(0.74 * HCCIIIdeath, ""),
        p_sHCCIV_Death=(0.74 * HCCIVdeath, ""),
        Posrate_highrisk=(1, "HBsAg阳性高危率"),
        Rate_screening=(None, ""),  # Empty
        Rate_screening2=(0.7, "筛查即临床检查参与率"),
        Startage=(0, ""),
        True_neg_AFP_US=(0.84, "超声特异度"),
        True_pos_AFP_USearly=(0.63, "超声早期HCC灵敏度"),
        True_pos_AFP_USlate=(0.97, "超声晚期HCC灵敏度"),
        True_pos_cc=(0.687, "超声肝硬化灵敏度"),
        True_pos_HBsAg=(0.9, ""),
        U_CC=(0.761, ""),
        U_DCC=(0.643, ""),
        U_HCCI=(0.76, ""),
        U_HCCII=(0.68, ""),
        U_HCCIII=(0.4, ""),
        U_HCCIV=(0.25, ""),
        U_health=(1, "")
    )

    # endregion
    # region ===== 死亡吸收态 =====
    death = State(
        name="death",
        description="自然死亡",
        is_absorbing=True
    )
    death_hcc = State(
        name="death_hcc",
        description="死于肝癌",
        is_absorbing=True
    )
    death_dcc = State(
        name="death_dcc",
        description="死于失代偿肝硬化",
        is_absorbing=True
    )
    death_cc = State(
        name="death_cc",
        description="死于代偿肝硬化",
        is_absorbing=True
    )
    # endregion
    # region ===== 健康状态 =====
    Healthy = State(
        name="Healthy",
        description="健康",
        utility_func=lambda cycle, p: state_utility_func(params.U_health, params.DR, cycle),
    )
    # endregion
    # region ===== CHB慢性乙肝感染 =====
    CHB = State(
        name="CHB",
        description="慢性乙肝感染",
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: state_utility_func(params.U_health, params.DR, cycle)
    )
    CHB_shaicha = State(
        name="CHB_shaicha",
        description="慢性乙肝感染筛查 screening",
        is_temporary=True
    )
    CHB_noshaicha = State(
        name="CHB_noshaicha",
        description="慢性乙肝感染不筛查 no screening",
        is_temporary=True
    )
    CHB.add_transition(
        CHB_shaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=100, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    CHB.add_transition(
        CHB_noshaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=100, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== pCC =====
    pCC = State(
        name="pCC",
        description="pCC",
        utility_func=lambda cycle, p: state_utility_func(params.U_health, params.DR, cycle),
    )
    pCC_shaicha = State(
        name="pCC_shaicha",
        description="pCC筛查 screening",
        is_temporary=True,
    )
    pCC_noshaicha = State(
        name="pCC_noshaicha",
        description="pCC不筛查 no screening",
        is_temporary=True,
    )
    pCC.add_transition(
        pCC_shaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pCC.add_transition(
        pCC_noshaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== pDCC =====
    pDCC = State(
        name="pDCC",
        description="pDCC",
        utility_func=lambda cycle, p: state_utility_func(params.U_health, params.DR, cycle),
    )
    pDCC_shaicha = State(
        name="pDCC_shaicha",
        description="pDCC筛查 screening",
        is_temporary=True,
    )
    pDCC_noshaicha = State(
        name="pDCC_noshaicha",
        description="pDCC不筛查 no screening",
        is_temporary=True,
    )
    pDCC.add_transition(
        pDCC_shaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pDCC.add_transition(
        pDCC_noshaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== 治愈状态 =====
    cured = State(
        name="cured",
        description="cured",
        utility_func=lambda cycle, p: state_utility_func(params.U_health, params.DR, cycle),
    )
    cured.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    cured.add_transition(
        cured,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前I期 =====
    pHCCI = State(
        name="pHCCI",
        description="临床前I期",
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCI, params.DR, cycle),
    )
    pHCCI_shaicha = State(
        name="pHCCI_shaicha",
        description="临床前I期筛查 screening",
        is_temporary=True,
    )
    pHCCI_noshaicha = State(
        name="pHCCI_noshaicha",
        description="临床前I期不筛查 no screening",
        is_temporary=True,
    )
    pHCCI.add_transition(
        pHCCI_shaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pHCCI.add_transition(
        pHCCI_noshaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== 临床前II期 =====
    pHCCII = State(
        name="pHCCII",
        description="临床前II期",
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCII, params.DR, cycle),
    )
    pHCCII_shaicha = State(
        name="pHCCII_shaicha",
        description="临床前II期筛查 screening",
        is_temporary=True,
    )
    pHCCII_noshaicha = State(
        name="pHCCII_noshaicha",
        description="临床前II期不筛查 no screening",
        is_temporary=True,
    )
    pHCCII.add_transition(
        pHCCII_shaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pHCCII.add_transition(
        pHCCII_noshaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== 临床前III期 =====
    pHCCIII = State(
        name="pHCCIII",
        description="临床前III期",
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCIII, params.DR, cycle),
    )
    pHCCIII_shaicha = State(
        name="pHCCIII_shaicha",
        description="临床前III期筛查 screening",
        is_temporary=True,
    )
    pHCCIII_noshaicha = State(
        name="pHCCIII_noshaicha",
        description="临床前III期不筛查 no screening",
        is_temporary=True,
    )
    pHCCIII.add_transition(
        pHCCIII_shaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pHCCIII.add_transition(
        pHCCIII_noshaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== 临床前IV期 =====
    pHCCIV = State(
        name="pHCCIV",
        description="临床前IV期",
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCIV, params.DR, cycle),
    )
    pHCCIV_shaicha = State(
        name="pHCCIV_shaicha",
        description="临床前IV期筛查 screening",
        is_temporary=True,
    )
    pHCCIV_noshaicha = State(
        name="pHCCIV_noshaicha",
        description="临床前IV期不筛查 no screening",
        is_temporary=True,
    )
    pHCCIV.add_transition(
        pHCCIV_shaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pHCCIV.add_transition(
        pHCCIV_noshaicha,
        condition=create_condition_gq_leq(min_cycle=-350, max_cycle=-100, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion

    # region ===== cHCC-I =====
    cHCCI = State(
        name="cHCCI",
        description="cHCCI",
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCI, params.DR, cycle),
    )
    cHCCI.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    cHCCI.add_transition(
        death_hcc,
        probability_func=lambda cycle, p: params.get(key="p_HCCI_Death", index=int(cycle // 5 * 5))
    )
    cHCCI.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_HCCI_Death", index=int(cycle // 5 * 5))
    )
    # endregion
    # region ===== cHCC-II =====
    cHCCII = State(
        name="cHCCII",
        description="cHCCII",
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCII, params.DR, cycle),
    )
    cHCCII.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    cHCCII.add_transition(
        death_hcc,
        probability_func=lambda cycle, p: params.get(key="p_HCCII_Death", index=int(cycle // 5 * 5))
    )
    cHCCII.add_transition(
        cHCCII,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_HCCII_Death", index=int(cycle // 5 * 5))
    )
    # endregion
    # region ===== cHCC-III =====
    cHCCIII = State(
        name="cHCCIII",
        description="cHCCIII",
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCIII, params.DR, cycle),
    )
    cHCCIII.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    cHCCIII.add_transition(
        death_hcc,
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_Death", index=int(cycle // 5 * 5))
    )
    cHCCIII.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_HCCIII_Death", index=int(cycle // 5 * 5))
    )
    # endregion
    # region ===== cHCC-IV =====
    cHCCIV = State(
        name="cHCCIV",
        description="cHCCIV",
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCIV, params.DR, cycle),
    )
    cHCCIV.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    cHCCIV.add_transition(
        death_hcc,
        probability_func=lambda cycle, p: params.get(key="p_HCCIV_Death", index=int(cycle // 5 * 5))
    )
    cHCCIV.add_transition(
        cHCCIV,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_HCCIV_Death", index=int(cycle // 5 * 5))
    )
    # endregion

    # region ===== sHCC-I =====
    sHCCI = State(
        name="sHCCI",
        description="sHCCI",
        cost_func=lambda cycle, p: state_utility_func(params.Cost_Treat_I, params.DR, cycle),
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCI, params.DR, cycle),
    )
    sHCCI.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    sHCCI.add_transition(
        death_hcc,
        probability_func=lambda cycle, p: params.get(key="p_sHCCI_Death", index=int(cycle // 5 * 5))
    )
    sHCCI.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_sHCCI_Death", index=int(cycle // 5 * 5))
    )
    # endregion
    # region ===== sHCC-II =====
    sHCCII = State(
        name="sHCCII",
        description="sHCCII",
        cost_func=lambda cycle, p: state_utility_func(params.Cost_Treat_II, params.DR, cycle),
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCII, params.DR, cycle),
    )
    sHCCII.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    sHCCII.add_transition(
        death_hcc,
        probability_func=lambda cycle, p: params.get(key="p_sHCCII_Death", index=int(cycle // 5 * 5))
    )
    sHCCII.add_transition(
        sHCCII,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_sHCCII_Death", index=int(cycle // 5 * 5))
    )
    # endregion
    # region ===== sHCC-III =====
    sHCCIII = State(
        name="sHCCIII",
        description="sHCCIII",
        cost_func=lambda cycle, p: state_utility_func(params.Cost_Treat_III, params.DR, cycle),
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCIII, params.DR, cycle),
    )
    sHCCIII.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    sHCCIII.add_transition(
        death_hcc,
        probability_func=lambda cycle, p: params.get(key="p_sHCCIII_Death", index=int(cycle // 5 * 5))
    )
    sHCCIII.add_transition(
        sHCCIII,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_sHCCIII_Death", index=int(cycle // 5 * 5))
    )
    # endregion
    # region ===== sHCC-IV =====
    sHCCIV = State(
        name="sHCCIV",
        description="sHCCIV",
        cost_func=lambda cycle, p: state_utility_func(params.Cost_Treat_IV, params.DR, cycle),
        utility_func=lambda cycle, p: state_utility_func(params.U_HCCIV, params.DR, cycle),
    )
    sHCCIV.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    sHCCIV.add_transition(
        death_hcc,
        probability_func=lambda cycle, p: params.get(key="p_sHCCIV_Death", index=int(cycle // 5 * 5))
    )
    sHCCIV.add_transition(
        sHCCIV,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_sHCCIV_Death", index=int(cycle // 5 * 5))
    )
    # endregion

    sCC = State(
        name="sCC",
        description="sCC",
        utility_func=lambda cycle, p: state_utility_func(params.U_CC, params.DR, cycle)
    )
    sDCC = State(
        name="sDCC",
        description="sDCC",
        utility_func=lambda cycle, p: state_utility_func(params.U_DCC, params.DR, cycle)
    )
    CC = State(
        name="CC",
        description="CC",
        utility_func=lambda cycle, p: state_utility_func(params.U_CC, params.DR, cycle),
    )
    DCC = State(
        name="DCC",
        description="DCC",
        utility_func=lambda cycle, p: state_utility_func(params.U_DCC, params.DR, cycle)
    )
    tCC = State(
        name="tCC",
        description="CC treated",
        cost_func=lambda cycle, p: state_utility_func(params.Cost_Treat_CC, params.DR, cycle),
        utility_func=lambda cycle, p: state_utility_func(params.U_health, params.DR, cycle),
        tunnel_cycle=10 #
    )
    tDCC = State(
        name="tDCC",
        description="DCC treated",
        cost_func=lambda cycle, p: state_utility_func(params.Cost_Treat_DCC, params.DR, cycle),
        utility_func=lambda cycle, p: state_utility_func(params.U_health, params.DR, cycle),
        tunnel_cycle=10
    )

    # region ===== 健康不筛查分支 =====
    Healthy.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_health_pHCCI", index=int(cycle // 5 * 5))
    )
    Healthy.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    Healthy.add_transition(
        CHB,
        probability_func=lambda cycle, p: params.get(key="p_health_CHB", index=int(cycle // 5 * 5))
    )
    Healthy.add_transition(
        Healthy, # 0.9995868327777778
        probability_func=lambda cycle, p: \
            1 - params.get(key="p_health_pHCCI", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle) - params.get(
                key="p_health_CHB", index=int(cycle // 5 * 5))
    )
    # endregion
    # region ===== CHB筛查分支 =====
    CHB_S_TO_CC = State(
        name="CHB_S_TO_CC",
        description="CHB screening to CC",
        is_temporary=True
    )

    CHB_S_TO_CC_3 = State(
        name="CHB_S_TO_CC_3",
        description="CHB screening to CC 3",
        is_temporary=True
    )
    CHB_S_TO_CC_3.add_transition(
        sCC,
        probability_func=lambda cycle, p: params.True_pos_cc,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    CHB_S_TO_CC_3.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.True_pos_cc
    )

    CHB_S_TO_CC.add_transition(
        CHB_S_TO_CC_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    CHB_S_TO_CC.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )

    CHB_S_TO_pHCCI = State(
        name="CHB_S_TO_pHCCI",
        description="CHB screening to pHCCI",
        is_temporary=True
    )
    CHB_S_TO_pHCCI_3 = State(
        name="CHB_S_TO_pHCCI_3",
        description="CHB screening to pHCCI 3",
        is_temporary=True
    )

    CHB_S_TO_pHCCI_3.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    CHB_S_TO_pHCCI_3.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )

    CHB_S_TO_pHCCI.add_transition(
        CHB_S_TO_pHCCI_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    CHB_S_TO_pHCCI.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )

    CHB_stay = State(
        name="CHB_stay",
        description="CHB screening to stay",
        is_temporary=True
    )
    CHB_stay_3 = State(
        name="CHB_stay_3",
        description="CHB screening to stay 3",
        is_temporary=True
    )
    CHB_stay_3.add_transition(
        CHB,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )

    CHB_stay.add_transition(
        CHB_stay_3,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    CHB_shaicha.add_transition(
        CHB_S_TO_CC,
        probability_func=lambda cycle, p: params.p_HBV_CC,
    )
    CHB_shaicha.add_transition(
        CHB_S_TO_pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5)),
    )
    CHB_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    CHB_shaicha.add_transition(
        CHB_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) -
                                          params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5)) - params.p_HBV_CC,
    )
    # endregion
    # region ===== CHB不筛查分支 =====
    CHB_noshaicha.add_transition(
        pCC,
        probability_func=lambda cycle, p: params.p_HBV_CC
    )
    CHB_noshaicha.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5))
    )
    CHB_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    CHB_noshaicha.add_transition(
        CHB,
        probability_func=lambda cycle, p: \
            1 - params.get(key="p_Death", index=cycle) - params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5)) - params.p_HBV_CC
    )
    # endregion
    # region ===== pCC 筛查分支 =====
    pCC_stay = State(
        name="pCC_stay",
        description="pCC screening stay here",
        is_temporary=True
    )
    pCC_stay_3 = State(
        name="pCC_stay_3",
        description="pCC screening stay here 3",
        is_temporary=True
    )
    pCC_stay_3.add_transition(
        sCC,
        probability_func=lambda cycle, p: params.True_pos_cc,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pCC_stay_3.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.True_pos_cc
    )

    pCC_stay.add_transition(
        pCC_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pCC_stay.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pCC_to_DCC = State(
        name="pCC_to_DCC",
        description="pCC screening CC_to_DCC",
        is_temporary=True
    )

    pCC_to_DCC_3 = State(
        name="pCC_to_DCC_3",
        description="pCC to DCC here 3",
        is_temporary=True
    )
    pCC_to_DCC_3.add_transition(
        sDCC,
        probability_func=lambda cycle, p: params.True_pos_cc,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pCC_to_DCC_3.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.True_pos_cc
    )
    pCC_to_DCC.add_transition(
        pCC_to_DCC_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pCC_to_DCC.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pCC_to_HCCI = State(
        name="pCC_to_HCCI",
        description="pCC screening CC_to_HCCI",
        is_temporary=True
    )
    pCC_to_HCCI_3 = State(
        name="pCC_to_HCCI_3",
        description="pCC to HCCI here 3",
        is_temporary=True
    )
    pCC_to_HCCI_3.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pCC_to_HCCI_3.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pCC_to_HCCI.add_transition(
        pCC_to_HCCI_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pCC_to_HCCI.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pCC_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pCC_shaicha.add_transition(
        pCC_to_HCCI,
        probability_func=lambda cycle, p: params.p_CC_PHCCI
    )
    pCC_shaicha.add_transition(
        pCC_to_DCC,
        probability_func=lambda cycle, p: params.p_CC_DCC
    )
    pCC_shaicha.add_transition(
        pCC_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.p_CC_PHCCI - params.p_CC_DCC
    )
    # endregion
    # region ===== pCC 不筛查分支 =====
    # live 路线
    pCC_ns_live = State(
        name="pCC_ns",
        description="pCC no screening live",
        is_temporary=True
    )
    pCC_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pCC_noshaicha.add_transition(
        pCC_ns_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle)
    )
    pCC_ns_fx = State(
        name="pCC_ns_fx",
        description="pCC no screening live diagnose",
        is_temporary=True
    )
    pCC_ns_fx_nt = State(
        name="pCC_ns_fx_nt",
        description="pCC no screening live diagnose no treat",
        is_temporary=True
    )
    pCC_ns_fx_nt.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.p_CC_PHCCI
    )
    pCC_ns_fx_nt.add_transition(
        DCC,
        probability_func=lambda cycle, p: params.p_CC_DCC
    )
    pCC_ns_fx_nt.add_transition(
        CC,
        probability_func=lambda cycle, p: 1 - params.p_CC_DCC - params.p_CC_PHCCI
    )
    pCC_ns_fx.add_transition(
        pCC_ns_fx_nt,
        probability_func=lambda cycle, p: 1 - params.p_CC_treat
    )
    pCC_ns_fx.add_transition(
        tCC,
        probability_func=lambda cycle, p: params.p_CC_treat
    )
    pCC_ns_nfx = State(
        name="pCC_ns_nfx",
        description="pCC no screening live no diagnose",
        is_temporary=True
    )
    pCC_ns_nfx.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.p_CC_PHCCI
    )
    pCC_ns_nfx.add_transition(
        pDCC,
        probability_func=lambda cycle, p: params.p_CC_DCC
    )
    pCC_ns_nfx.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.p_CC_DCC - params.p_CC_PHCCI
    )
    pCC_ns_live.add_transition(
        pCC_ns_fx,
        probability_func=lambda cycle, p: 0.1
    )
    pCC_ns_live.add_transition(
        pCC_ns_nfx,
        probability_func=lambda cycle, p: 0.9
    )
    # endregion
    # region ===== pDCC 筛查分支 =====
    pDCC_stay = State(
        name="pDCC_stay",
        description="pDCC screening stay here",
        is_temporary=True
    )
    pDCC_stay_3 = State(
        name="pDCC_stay_3",
        description="pDCC stay here 3",
        is_temporary=True
    )
    pDCC_stay_3.add_transition(
        sDCC,
        probability_func=lambda cycle, p: params.True_pos_cc,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pDCC_stay_3.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.True_pos_cc
    )
    pDCC_stay.add_transition(
        pDCC_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pDCC_stay.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )

    pDCC_to_pHCCI = State(
        name="pDCC_to_pHCCI",
        description="pDCC screening DCC_to_pHCCI",
        is_temporary=True
    )
    pDCC_to_pHCCI_3 = State(
        name="pDCC_to_pHCCI_3",
        description="pDCC to pHCCI here 3",
        is_temporary=True
    )
    pDCC_to_pHCCI_3.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pDCC_to_pHCCI_3.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pDCC_to_pHCCI.add_transition(
        pDCC_to_pHCCI_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pDCC_to_pHCCI.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )

    pDCC_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pDCC_shaicha.add_transition(
        pDCC_to_pHCCI,
        probability_func=lambda cycle, p: params.p_DCC_PHCCI
    )
    pDCC_shaicha.add_transition(
        pDCC_stay,
        probability_func=lambda cycle, p: 1 - params.p_DCC_PHCCI - params.get(key="p_Death", index=cycle),
    )
    # endregion
    # region ===== pDCC 不筛查分支 =====
    # live 路线
    pDCC_ns_live = State(
        name="pDCC_ns_live",
        description="pDCC no screening live",
        is_temporary=True
    )
    pDCC_ns_live_fx = State(
        name="pDCC_ns_live_fx",
        description="pDCC no screening live diagnose",
        is_temporary=True
    )
    pDCC_ns_live_fx_nt = State(
        name="pDCC_ns_live_fx_nt",
        description="pDCC no screening live diagnose no treat",
        is_temporary=True
    )
    pDCC_ns_live_fx_nt.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.p_DCC_PHCCI
    )
    pDCC_ns_live_fx_nt.add_transition(
        DCC,
        probability_func=lambda cycle, p: 1 - params.p_DCC_PHCCI
    )
    pDCC_ns_live_fx.add_transition(
        tDCC,
        probability_func=lambda cycle, p: 0.7
    )
    pDCC_ns_live_fx.add_transition(
        pDCC_ns_live_fx_nt,
        probability_func=lambda cycle, p: 0.3
    )
    pDCC_ns_live_nfx = State(
        name="pDCC_ns_live_nfx",
        description="pDCC no screening live no diagnose",
        is_temporary=True
    )
    pDCC_ns_live_nfx.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.p_DCC_PHCCI
    )
    pDCC_ns_live_nfx.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.p_DCC_PHCCI
    )
    pDCC_ns_live.add_transition(
        pDCC_ns_live_fx,
        probability_func=lambda cycle, p: 0.1
    )
    pDCC_ns_live.add_transition(
        pDCC_ns_live_nfx,
        probability_func=lambda cycle, p: 0.9
    )
    pDCC_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pDCC_noshaicha.add_transition(
        pDCC_ns_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前I期筛查分支 =====
    pHCCI_s_stay = State(
        name="pHCCI_s_stay",
        description="pHCCI screening stay here",
        is_temporary=True
    )
    pHCCI_s_stay_3 = State(
        name="pHCCI_s_stay_3",
        description="pHCCI stay here 3",
        is_temporary=True
    )
    pHCCI_s_stay_3.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCI_s_stay_3.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pHCCI_s_stay.add_transition(
        pHCCI_s_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCI_s_stay.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )

    pHCCI_s_to_pII = State(
        name="pHCCI_s_to_pII",
        description="pHCCI screening pHCCI_to_pHCCII",
        is_temporary=True
    )
    pHCCI_s_to_pII_3 = State(
        name="pHCCI_s_to_pII_3",
        description="pHCCI to pII here 3",
        is_temporary=True
    )
    pHCCI_s_to_pII_3.add_transition(
        sHCCII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCI_s_to_pII_3.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pHCCI_s_to_pII.add_transition(
        pHCCI_s_to_pII_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCI_s_to_pII.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCI_s_to_cI = State(
        name="pHCCI_s_to_cI",
        description="pHCCI screening pHCCI_to_cHCCI",
        is_temporary=True
    )
    pHCCI_s_to_cI_3 = State(
        name="pHCCI_s_to_cI_3",
        description="pHCCI to cI here 3",
        is_temporary=True
    )
    pHCCI_s_to_cI_3.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCI_s_to_cI_3.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pHCCI_s_to_cI.add_transition(
        pHCCI_s_to_cI_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCI_s_to_cI.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCI_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCI_shaicha.add_transition(
        pHCCI_s_to_cI,
        probability_func=lambda cycle, p: params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5)),
    )
    pHCCI_shaicha.add_transition(
        pHCCI_s_to_pII,
        probability_func=lambda cycle, p: params.p_HCCI_HCCII
    )
    pHCCI_shaicha.add_transition(
        pHCCI_s_stay,
        probability_func=lambda cycle, p: 1 - params.p_HCCI_HCCII -
                                          params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle),
    )
    # endregion
    # region ===== 临床前I期不筛查分支 =====
    pHCCI_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCI_noshaicha.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: params.p_HCCI_HCCII
    )
    pHCCI_noshaicha.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5))
    )
    pHCCI_noshaicha.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5)) -
                                          params.p_HCCI_HCCII - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前II期筛查分支 =====
    pHCCII_s_stay = State(
        name="pHCCII_s_stay",
        description="pHCCII screening stay here",
        is_temporary=True
    )
    pHCCII_s_stay_3 = State(
        name="pHCCII_s_stay_3",
        description="pHCCII stay here 3",
        is_temporary=True
    )
    pHCCII_s_stay_3.add_transition(
        sHCCII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCII_s_stay_3.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pHCCII_s_stay.add_transition(
        pHCCII_s_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCII_s_stay.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCII_s_to_pIII = State(
        name="pHCCII_s_to_pIII",
        description="pHCCII screening pHCCII_to_pHCCIII",
        is_temporary=True
    )

    pHCCII_s_to_pIII_3 = State(
        name="pHCCII_s_to_pIII_3",
        description="pHCCII to pIII here 3",
        is_temporary=True
    )
    pHCCII_s_to_pIII_3.add_transition(
        sHCCIII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USlate,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCII_s_to_pIII_3.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USlate
    )
    pHCCII_s_to_pIII.add_transition(
        pHCCII_s_to_pIII_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCII_s_to_pIII.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCII_s_to_cII = State(
        name="pHCCII_s_to_cII",
        description="pHCCII screening pHCCII_to_cHCCII",
        is_temporary=True
    )
    pHCCII_s_to_cII_3 = State(
        name="pHCCII_s_to_cII_3",
        description="pHCCII to cII here 3",
        is_temporary=True
    )
    pHCCII_s_to_cII_3.add_transition(
        sHCCII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCII_s_to_cII_3.add_transition(
        cHCCII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pHCCII_s_to_cII.add_transition(
        pHCCII_s_to_cII_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCII_s_to_cII.add_transition(
        cHCCII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCII_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCII_shaicha.add_transition(
        pHCCII_s_to_cII,
        probability_func=lambda cycle, p: params.get(key="p_HCCII_Detected", index=int(cycle // 5 * 5)),
    )
    pHCCII_shaicha.add_transition(
        pHCCII_s_to_pIII,
        probability_func=lambda cycle, p: params.p_HCCII_HCCIII
    )
    pHCCII_shaicha.add_transition(
        pHCCII_s_stay,
        probability_func=lambda cycle, p: 1 - params.p_HCCII_HCCIII - params.get(
            key="p_HCCII_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle),
    )
    # endregion
    # region ===== 临床前II期不筛查分支 =====
    pHCCII_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCII_noshaicha.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: params.p_HCCII_HCCIII
    )
    pHCCII_noshaicha.add_transition(
        cHCCII,
        probability_func=lambda cycle, p: params.get(key="p_HCCII_Detected", index=int(cycle // 5 * 5))
    )
    pHCCII_noshaicha.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCII_Detected", index=int(cycle // 5 * 5)) - params.p_HCCII_HCCIII - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前III期筛查分支 =====
    pHCCIII_s_stay = State(
        name="pHCCIII_s_stay",
        description="pHCCIII screening stay here",
        is_temporary=True
    )
    pHCCIII_s_stay_3 = State(
        name="pHCCIII_s_stay_3",
        description="pHCCIII stay here 3",
        is_temporary=True
    )
    pHCCIII_s_stay_3.add_transition(
        sHCCIII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USlate,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCIII_s_stay_3.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USlate
    )
    pHCCIII_s_stay.add_transition(
        pHCCIII_s_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIII_s_stay.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIII_s_to_pIV = State(
        name="pHCCIII_s_to_pIV",
        description="pHCCIII screening pHCCIII_to_pHCCIV",
        is_temporary=True
    )
    pHCCIII_s_to_pIV_3 = State(
        name="pHCCIII_s_to_pIV_3",
        description="pHCCIII to pIV 3",
        is_temporary=True
    )
    pHCCIII_s_to_pIV_3.add_transition(
        sHCCIV,
        probability_func=lambda cycle, p: params.True_pos_AFP_USlate,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCIII_s_to_pIV_3.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USlate
    )
    pHCCIII_s_to_pIV.add_transition(
        pHCCIII_s_to_pIV_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIII_s_to_pIV.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIII_s_to_cIII = State(
        name="pHCCIII_s_to_cIII",
        description="pHCCIII screening pHCCII_to_cHCCIII",
        is_temporary=True
    )
    pHCCIII_s_to_cIII_3 = State(
        name="pHCCIII_s_to_cIII_3",
        description="pHCCIII to cIII 3",
        is_temporary=True
    )
    pHCCIII_s_to_cIII_3.add_transition(
        sHCCIII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCIII_s_to_cIII_3.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pHCCIII_s_to_cIII.add_transition(
        pHCCIII_s_to_cIII_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIII_s_to_cIII.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIII_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCIII_shaicha.add_transition(
        pHCCIII_s_to_cIII,
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_Detected", index=int(cycle // 5 * 5))
    )
    pHCCIII_shaicha.add_transition(
        pHCCIII_s_to_pIV,
        probability_func=lambda cycle, p: params.p_HCCIII_HCCIV
    )
    pHCCIII_shaicha.add_transition(
        pHCCIII_s_stay,
        probability_func=lambda cycle, p: 1 - params.p_HCCIII_HCCIV - params.get(
            key="p_HCCIII_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前III期不筛查分支 =====
    pHCCIII_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCIII_noshaicha.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: params.p_HCCIII_HCCIV,
    )
    pHCCIII_noshaicha.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_Detected", index=int(cycle // 5 * 5))
    )
    pHCCIII_noshaicha.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCIII_Detected", index=int(cycle // 5 * 5)) - params.p_HCCIII_HCCIV - params.get(key="p_Death", index=cycle),
    )
    # endregion
    # region ===== 临床前IV期筛查分支 =====
    pHCCIV_s_stay = State(
        name="pHCCIV_s_stay",
        description="pHCCIV screening stay here",
        is_temporary=True
    )
    pHCCIV_s_stay_3 = State(
        name="pHCCIV_s_stay_3",
        description="pHCCIV stay 3",
        is_temporary=True
    )
    pHCCIV_s_stay_3.add_transition(
        sHCCIV,
        probability_func=lambda cycle, p: params.True_pos_AFP_USlate,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCIV_s_stay_3.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USlate
    )
    pHCCIV_s_stay.add_transition(
        pHCCIV_s_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIV_s_stay.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIV_s_to_cIV = State(
        name="pHCCIV_s_to_cIV",
        description="pHCCIV screening pHCCIV_to_cHCCIV",
        is_temporary=True
    )
    pHCCIV_s_to_cIV_3 = State(
        name="pHCCIV_s_to_cIV_3",
        description="pHCCIV to cIV 3",
        is_temporary=True
    )
    pHCCIV_s_to_cIV_3.add_transition(
        sHCCIV,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCIV_s_to_cIV_3.add_transition(
        cHCCIV,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pHCCIV_s_to_cIV.add_transition(
        pHCCIV_s_to_cIV_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIV_s_to_cIV.add_transition(
        cHCCIV,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIV_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCIV_shaicha.add_transition(
        pHCCIV_s_to_cIV,
        probability_func=lambda cycle, p: params.get(key="p_HCCIV_Detected", index=int(cycle // 5 * 5)),
    )
    pHCCIV_shaicha.add_transition(
        pHCCIV_s_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCIV_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle),
    )
    # endregion
    # region ===== 临床前IV期不筛查分支 =====
    pHCCIV_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCIV_noshaicha.add_transition(
        cHCCIV,
        probability_func=lambda cycle, p: params.get(key="p_HCCIV_Detected", index=int(cycle // 5 * 5))
    )
    pHCCIV_noshaicha.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCIV_Detected", index=int(cycle // 5 * 5)) - params.get(
            key="p_Death", index=cycle)
    )
    # endregion
    # region ===== sCC 分支 =====
    sCC_live = State(
        name="sCC_live",
        description="sCC live",
        is_temporary=True
    )
    sCC_live_nt = State(
        name="sCC_live_nt",
        description="sCC live no treat",
        is_temporary=True
    )
    sCC_live_nt.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.p_CC_PHCCI
    )
    sCC_live_nt.add_transition(
        sDCC,
        probability_func=lambda cycle, p: params.p_CC_DCC
    )
    sCC_live_nt.add_transition(
        sCC,
        probability_func=lambda cycle, p: 1 - params.p_CC_DCC - params.p_CC_PHCCI
    )
    sCC_live.add_transition(
        tCC,
        probability_func=lambda cycle, p: params.p_CC_treat
    )
    sCC_live.add_transition(
        sCC_live_nt,
        probability_func=lambda cycle, p: 1 - params.p_CC_treat
    )
    sCC.add_transition(
        death_cc,
        probability_func=lambda cycle, p: params.p_CC_Death
    )
    sCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    sCC.add_transition(
        sCC_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.p_CC_Death
    )
    # endregion
    # region ===== sDCC =====
    sDCC_live = State(
        name="sDCC_live",
        description="sDCC live",
        is_temporary=True
    )
    sDCC_live_nt = State(
        name="sDCC_live_nt",
        description="sDCC live no treat",
        is_temporary=True
    )
    sDCC_live_nt.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.p_DCC_PHCCI
    )
    sDCC_live_nt.add_transition(
        sDCC,
        probability_func=lambda cycle, p: 1 - params.p_DCC_PHCCI
    )
    sDCC_live.add_transition(
        tDCC,
        probability_func=lambda cycle, p: params.p_DCC_treat
    )
    sDCC_live.add_transition(
        sCC_live_nt,
        probability_func=lambda cycle, p: 1 - params.p_DCC_treat
    )
    sDCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    sDCC.add_transition(
        death_dcc,
        probability_func=lambda cycle, p: params.p_DCC_Death
    )
    sDCC.add_transition(
        sDCC_live,
        probability_func=lambda cycle, p: 1 - params.p_DCC_Death - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== CC =====
    CC_live = State(
        name="CC_live",
        description="CC live",
        is_temporary=True
    )
    CC_live_nt = State(
        name="CC_live_nt",
        description="CC live no treat",
        is_temporary=True
    )
    CC_live_nt.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.p_CC_PHCCI
    )
    CC_live_nt.add_transition(
        DCC,
        probability_func=lambda cycle, p: params.p_CC_DCC
    )
    CC_live_nt.add_transition(
        CC,
        probability_func=lambda cycle, p: 1 - params.p_CC_DCC - params.p_CC_PHCCI
    )
    CC_live.add_transition(
        tCC,
        probability_func=lambda cycle, p: params.p_CC_treat
    )
    CC_live.add_transition(
        CC_live_nt,
        probability_func=lambda cycle, p: 1 - params.p_CC_treat
    )
    CC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    CC.add_transition(
        death_cc,
        probability_func=lambda cycle, p: params.p_CC_Death
    )
    CC.add_transition(
        CC_live,
        probability_func=lambda cycle, p: 1 - params.p_CC_Death - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== DCC =====
    DCC_live = State(
        name="DCC_live",
        description="DCC live",
        is_temporary=True
    )
    DCC_live_nt = State(
        name="DCC_live_nt",
        description="DCC live no treat",
        is_temporary=True
    )
    DCC_live_nt.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.p_DCC_PHCCI
    )
    DCC_live_nt.add_transition(
        DCC,
        probability_func=lambda cycle, p: 1 - params.p_DCC_PHCCI
    )
    DCC_live.add_transition(
        tDCC,
        probability_func=lambda cycle, p: params.p_DCC_treat
    )
    DCC_live.add_transition(
        DCC_live_nt,
        probability_func=lambda cycle, p: 1 - params.p_DCC_treat
    )
    DCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    DCC.add_transition(
        death_dcc,
        probability_func=lambda cycle, p: params.p_DCC_Death
    )
    DCC.add_transition(
        DCC_live,
        probability_func=lambda cycle, p: 1 - params.p_DCC_Death - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== tCC 分支 =====
    # >>> _tunnel_ 前 10 年未进展 >>>
    tCC.add_tunnel_transition(
        cured,
        probability_func=lambda cycle, p: params.p_CC_cure
    )
    tCC.add_tunnel_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    tCC.add_tunnel_transition(
        tCC,
        probability_func=lambda cycle, p: 1 - params.p_CC_cure - params.get(key="p_Death", index=cycle)
    )
    # <<< _tunnel_ 前 10 年未进展 <<<
    tCC_live = State(
        name="tCC_live",
        description="tCC_live",
        is_temporary=True
    )
    tCC_live.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.p_CC_PHCCI_treat
    )
    tCC_live.add_transition(
        DCC,
        probability_func=lambda cycle, p: params.p_CC_DCC_treat
    )
    tCC_live.add_transition(
        tCC,
        probability_func=lambda cycle, p: 1 - params.p_CC_PHCCI_treat - params.p_CC_DCC_treat
    )
    tCC.add_transition(
        death_cc,
        probability_func=lambda cycle, p: params.p_CC_Death_treat
    )
    tCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    tCC.add_transition(
        tCC_live,
        probability_func=lambda cycle, p: 1 - params.p_CC_Death_treat - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== tDCC 分支 =====
    tDCC.add_tunnel_transition(
        cured,
        probability_func=lambda cycle, p: params.p_DCC_cure
    )
    tDCC.add_tunnel_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    tDCC.add_tunnel_transition(
        tDCC,
        probability_func=lambda cycle, p: 1 - params.p_DCC_cure - params.get(key="p_Death", index=cycle)
    )
    tDCC_live = State(
        name="tDCC_live",
        description="tDCC_live",
        is_temporary=True
    )
    tDCC_live.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.p_DCC_PHCCI_treat
    )
    tDCC_live.add_transition(
        tDCC,
        probability_func=lambda cycle, p: 1 - params.p_DCC_PHCCI_treat
    )
    tDCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    tDCC.add_transition(
        death_dcc,
        probability_func=lambda cycle, p: params.p_DCC_Death_treat
    )
    tDCC.add_transition(
        tDCC_live,
        probability_func=lambda cycle, p: 1 - params.p_DCC_Death_treat - params.get(key="p_Death", index=cycle)
    )
    # endregion
    model = MarkovModel(
        states=[Healthy, CHB, pCC, pDCC, death_hcc, death, death_dcc, death_cc, pHCCI, pHCCII, pHCCIII, pHCCIV,
                sHCCI, sHCCII, sHCCIII, sHCCIV, sCC, sDCC, CC, DCC, tCC, tDCC, cured, cHCCI, cHCCII, cHCCIII, cHCCIV,
                CHB_shaicha, CHB_noshaicha,  pCC_shaicha, pCC_noshaicha, pDCC_shaicha,
                pDCC_noshaicha, pHCCI_shaicha, pHCCI_noshaicha, pHCCII_shaicha, pHCCII_noshaicha, pHCCIII_shaicha,
                pHCCIII_noshaicha, pHCCIV_shaicha, pHCCIV_noshaicha,
                CHB_S_TO_CC, CHB_S_TO_CC_3, CHB_S_TO_pHCCI, CHB_S_TO_pHCCI_3, CHB_stay, CHB_stay_3,
                pCC_stay, pCC_stay_3, pCC_to_DCC, pCC_to_DCC_3, pCC_to_HCCI, pCC_to_HCCI_3, pCC_ns_live, pCC_ns_fx, pCC_ns_fx_nt, pCC_ns_nfx,
                pDCC_stay, pDCC_stay_3, pDCC_to_pHCCI, pDCC_to_pHCCI_3, pDCC_ns_live, pDCC_ns_live_fx, pDCC_ns_live_fx_nt, pDCC_ns_live_nfx,
                pHCCI_s_stay, pHCCI_s_stay_3, pHCCI_s_to_pII, pHCCI_s_to_pII_3, pHCCI_s_to_cI, pHCCI_s_to_cI_3,
                pHCCII_s_stay, pHCCII_s_stay_3, pHCCII_s_to_pIII, pHCCII_s_to_pIII_3, pHCCII_s_to_cII, pHCCII_s_to_cII_3,
                pHCCIII_s_stay, pHCCIII_s_stay_3, pHCCIII_s_to_pIV, pHCCIII_s_to_pIV_3, pHCCIII_s_to_cIII, pHCCIII_s_to_cIII_3,
                pHCCIV_s_stay, pHCCIV_s_stay_3, pHCCIV_s_to_cIV, pHCCIV_s_to_cIV_3,
                sCC_live, sCC_live_nt, sDCC_live, sDCC_live_nt, CC_live, CC_live_nt, DCC_live, DCC_live_nt, tCC_live, tDCC_live,
                ],
        initial_distribution={"Healthy": 100000}
    )

    print("状态下标：", model.state_index)

    model.run(cycles=85, params=params, cohort=True)

    np.set_printoptions(precision=3, suppress=True)
    print(f"最终状态分布:\n \
{model.results['state_counts'][-1][[i for i in range(27)]]}\n===================================")
    k = 86
    # print(f"前 {k} cycle 状态分布\nhealthy | CHB | pCC | pDCC | death_hcc | death | death_dcc | death_cc | tCC | tDCC:")
    print(f"前 {k} cycle 状态分布\ndeath_hcc | death | death_dcc | death_cc | pI-IV | sI-IV | tCC | tDCC:")
    # 定义列名
    columns = [ 'Healthy', 'CHB', 'pCC','pDCC',
        'death_hcc', 'death', 'death_dcc', 'death_cc',
        'pHCCI', 'pHCCII', 'pHCCIII', 'pHCCIV',
        'sHCCI', 'sHCCII', 'sHCCIII', 'sHCCIV', 'sCC', 'sDCC',
        'CC', 'DCC', 'tCC', 'tDCC', 'cured', 'cHCCI', 'cHCCII', 'cHCCIII', 'cHCCIV'
    ]
    # 初始化一个空列表来存储所有行的数据
    data_list = []
    for i in range(k):
        tmp = model.results['state_counts'][i]
        tmp = np.array(tmp)
        data_list.append(tmp[[i for i in range(27)]])
        print(f"{i}- {tmp[[i for i in range(27)]]}")
    df = pd.DataFrame(data_list, columns=columns)
    # df.to_excel("res1.xlsx")
    ss = []
    for state in model.states:
        ss.append(state.name)
    print(len(ss), len(list(set(ss))))


if __name__ == "__main__":
    import pandas as pd
    my_treeage_shaicha()
