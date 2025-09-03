"""
对 tmp_0902.trex TreeAge 文件的 Python 实现
"""
import numpy as np

from lab.markov_simple import MarkovModel, State
from lab.condition import create_condition, create_condition_gq_leq
from parameter.define_parameters import Parameters
from parameter.define_tables import Table
import matplotlib.pyplot as plt


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
 12: 0.000236615999999999,
 13: 0.000272836,
 14: 0.000261231,
 15: 0.0002827,
 16: 0.000247996999999999,
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
    HCCIdeath = Table({0: 0.168841742,
 5: 0.172967452,
 10: 0.168532489,
 15: 0.166811506,
 20: 0.158333117,
 25: 0.136455063,
 30: 0.149607158,
 35: 0.168662903,
 40: 0.145862319,
 45: 0.163663608,
 50: 0.210845768,
 55: 0.168017125,
 60: 0.19682212,
 65: 0.197315309,
 70: 0.162911856,
 75: 0.208827907,
 80: 0.248466723})
    HCCIIdeath = Table({0: 0.217532697,
 5: 0.183973012,
 10: 0.169753133,
 15: 0.180635705,
 20: 0.193378244,
 25: 0.214194574,
 30: 0.200650976,
 35: 0.170206277,
 40: 0.207949708,
 45: 0.19939164,
 50: 0.233102423,
 55: 0.183340603,
 60: 0.230438353,
 65: 0.215190602,
 70: 0.239023904,
 75: 0.249982717,
 80: 0.259566745})
    HCCIIIdeath = Table({0: 0.234457863,
 5: 0.232069236,
 10: 0.237836608,
 15: 0.230789525,
 20: 0.229724734,
 25: 0.215917099,
 30: 0.221961541,
 35: 0.220154001,
 40: 0.209375844,
 45: 0.208505951,
 50: 0.267958758,
 55: 0.193582381,
 60: 0.235664984,
 65: 0.257892328,
 70: 0.245997391,
 75: 0.278361951,
 80: 0.328260728})
    HCCIVdeath = Table({0: 0.238623706,
 5: 0.238623706,
 10: 0.252115033,
 15: 0.235732737,
 20: 0.234090839,
 25: 0.24028112,
 30: 0.249114879,
 35: 0.244188829,
 40: 0.239528015,
 45: 0.252344626,
 50: 0.303993039,
 55: 0.232032961,
 60: 0.284038499,
 65: 0.277957033,
 70: 0.264111405,
 75: 0.298714668,
 80: 0.391823347})
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
    0: 0.00002704500,
    5: 0.00005070110,
    10: 0.00030724800,
    15: 0.00017783200,
    20: 0.00005397770,
    25: 0.00004286340,
    30: 0.00008639170,
    35: 0.00797812100,
    40: 0.00659399400,
    45: 0.00004775160,
    50: 0.00976703100,
    55: 0.00702063200,
    60: 0.00008521510,
    65: 0.00716413100,
    70: 0.00162877000,
    75: 0.00048909600,
    80: 0.00470835700
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
        dr=(0.00, "贴现率1"),
        DR=(0.03, "贴现率"),
        P_CC_cure=(0.079, "代偿肝硬化治愈率"),
        p_CC_DCC=(0.058, "代偿肝硬化_失代偿肝硬化"),
        p_CC_DCC_treat=(0.019, "治疗后 代偿肝硬化_失代偿肝硬化"),
        p_CC_Death=(0.031, "代偿肝硬化_死于代偿肝硬化"),
        p_CC_Death_treat=(0.017, ""),
        p_CC_PHCCI=(0.0316, "代偿肝硬化_临床前I期"),
        p_CC_PHCCI_treat=(0.02, "治疗后 代偿肝硬化_临床前I期"),
        p_CC_treat=(0.7, ""),
        p_CC_zifa=(0.15, ""),
        P_DCC_cure=(0.033, "失代偿肝硬化治愈率"),
        p_DCC_Death=(0.17, "失代偿肝硬化_死于失代偿肝硬化"),
        p_DCC_Death_treat=(0.095, ""),
        p_DCC_PHCCI=(0.034, "失代偿肝硬化_临床前I期"),
        p_DCC_PHCCI_treat=(0.024, ""),
        p_DCC_treat=(0.7, ""),
        p_DCC_zifa=(0.7, ""),
        p_Death=(Death, "xxx_死于其他原因"),
        p_HBV_CC=(0.0173, "慢性乙肝_代偿肝硬化"),
        p_HBV_pHCCI=(pHBVToHCCI, "慢性乙肝_临床前I期(---)"),
        p_HCC_treat=(0.7, "HCC治疗率"),
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
        p_sHCCI_Death=(0.74 * HCCIdeath, ""),
        p_sHCCII_Death=(0.74 * HCCIIdeath, ""),
        p_sHCCIII_Death=(0.74 * HCCIIIdeath, ""),
        p_sHCCIV_Death=(0.74 * HCCIVdeath, ""),
        Posrate_highrisk=(1, "HBsAg阳性高危率"),
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
    death_cc = State(
        name="death_cc",
        description="死于代偿肝硬化",
        is_absorbing=True
    )
    # endregion
    # region ===== 治愈状态 =====
    cured = State(
        name="cured",
        description="cured",
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
    # region ===== 健康状态 =====
    from my_models.my_utils.utility import health_utility_func
    Healthy = State(
        name="Healthy",
        description="健康"
    )
    # endregion

    # region ===== CHB慢性乙肝感染 =====
    CHB = State(
        name="CHB",
        description="慢性乙肝感染"
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
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    CHB.add_transition(
        CHB_noshaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== pCC =====
    pCC = State(
        name="pCC",
        description="pCC"
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
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pCC.add_transition(
        pCC_noshaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion

    # region ===== 临床前I期 =====
    pHCCI = State(
        name="pHCCI",
        description="临床前I期",
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
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pHCCI.add_transition(
        pHCCI_noshaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion

    # region ===== cHCC-I =====
    cHCCI = State(
        name="cHCCI",
        description="cHCCI",
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

    # region ===== sHCC-I =====
    sHCCI = State(
        name="sHCCI",
        description="sHCCI",
    )
    sHCCI.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    sHCCI_live = State(
        name="sHCCI_live",
        description="sHCCI live",
        is_temporary=True
    )
    sHCCI_live.add_transition(
        cured,
        probability_func=lambda cycle, p: params.get(key="p_HCC_treat")
    )
    sHCCI_live.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCC_treat")
    )
    sHCCI.add_transition(
        death_hcc,
        probability_func=lambda cycle, p: params.get(key="p_sHCCI_Death", index=int(cycle // 5 * 5))
    )
    sHCCI.add_transition(
        sHCCI_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_sHCCI_Death", index=int(cycle // 5 * 5))
    )
    # endregion

    sCC = State(
        name="sCC",
        description="sCC",
    )
    CC = State(
        name="CC",
        description="CC",
    )
    tCC = State(
        name="tCC",
        description="CC treated",
    )
    # region ===== 健康分支 =====
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
        Healthy,
        probability_func=lambda cycle, p: \
            1 - params.get(key="p_health_pHCCI", index=int(cycle // 5 * 5))
            - params.get(key="p_Death", index=cycle) - params.get(key="p_health_CHB", index=int(cycle // 5 * 5))

    )
    # endregion
    # region ===== CHB筛查分支 =====
    pre_ps_CC = State(
        name="pre_ps_CC",
        description="CHB screening to CC",
        is_temporary=True
    )
    pre_ps_CC.add_transition(
        sCC,
        probability_func=lambda cycle, p: params.True_pos_cc * params.Rate_screening2
    )
    pre_ps_CC.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.True_pos_cc * params.Rate_screening2
    )
    pre_ps_HCCI_1 = State(
        name="pre_ps_HCCI_1",
        description="CHB screening to pHCCI",
        is_temporary=True
    )
    pre_ps_HCCI_1.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pre_ps_HCCI_1.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    CHB_shaicha.add_transition(
        pre_ps_CC,
        probability_func=lambda cycle, p: params.get(key="p_HBV_CC", index=cycle),

    )
    CHB_shaicha.add_transition(
        pre_ps_HCCI_1,
        probability_func=lambda cycle, p: params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5)),

    )
    CHB_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    CHB_shaicha.add_transition(
        CHB,
        probability_func=lambda cycle, p: \
            1 - params.get(key="p_Death", index=cycle) - params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5)) - params.get(key="p_HBV_CC", index=cycle),

    )
    # endregion
    # region ===== CHB不筛查分支 =====
    CHB_noshaicha.add_transition(
        pCC,
        probability_func=lambda cycle, p: params.get(key="p_HBV_CC", index=cycle)
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
            1 - params.get(key="p_Death", index=cycle) - params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5)) - params.get(
                key="p_HBV_CC", index=cycle)
    )
    # endregion
    # region ===== pCC 筛查分支 =====
    pCC_stemp1 = State(
        name="pCC_stemp1",
        description="pCC screening stay here",
        is_temporary=True
    )
    pCC_stemp3 = State(
        name="pCC_stemp3",
        description="pCC screening CC_to_HCCI",
        is_temporary=True
    )
    pCC_stemp1.add_transition(
        sCC,
        probability_func=lambda cycle, p: params.True_pos_cc * params.Rate_screening2
    )
    pCC_stemp1.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.True_pos_cc * params.Rate_screening2
    )
    pCC_stemp3.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pCC_stemp3.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pCC_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pCC_shaicha.add_transition(
        pCC_stemp3,
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle),

    )
    pCC_shaicha.add_transition(
        pCC_stemp1,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_CC_PHCCI", index=cycle),

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
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle)
    )
    pCC_ns_fx_nt.add_transition(
        CC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_PHCCI", index=cycle)
    )
    pCC_ns_fx.add_transition(
        pCC_ns_fx_nt,
        probability_func=lambda cycle, p: 0.3
    )
    pCC_ns_fx.add_transition(
        tCC,
        probability_func=lambda cycle, p: 0.7
    )
    pCC_ns_nfx = State(
        name="pCC_ns_nfx",
        description="pCC no screening live no diagnose",
        is_temporary=True
    )
    pCC_ns_nfx.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle)
    )
    pCC_ns_nfx.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.get(
            key="p_CC_PHCCI", index=cycle)
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
    # region ===== 临床前I期筛查分支 =====
    pHCCI_s_stay = State(
        name="pHCCI_s_stay",
        description="pHCCI screening stay here",
        is_temporary=True
    )
    pHCCI_s_stay.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCI_s_stay.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCI_s_to_cI = State(
        name="pHCCI_s_to_cI",
        description="pHCCI screening pHCCI_to_cHCCI",
        is_temporary=True
    )
    pHCCI_s_to_cI.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCI_s_to_cI.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
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
        pHCCI_s_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle),

    )
    # endregion
    # region ===== 临床前I期不筛查分支 =====
    pHCCI_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCI_noshaicha.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5))
    )
    pHCCI_noshaicha.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle)
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
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle)
    )
    sCC_live_nt.add_transition(
        sCC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_PHCCI", index=cycle)
    )
    sCC_live.add_transition(
        tCC,
        probability_func=lambda cycle, p: params.get(key="p_CC_treat", index=cycle)
    )
    sCC_live.add_transition(
        sCC_live_nt,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_treat", index=cycle)
    )
    sCC.add_transition(
        death_cc,
        probability_func=lambda cycle, p: params.get(key="p_CC_Death", index=cycle)
    )
    sCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    sCC.add_transition(
        sCC_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_CC_Death", index=cycle)
    )
    # endregion
    # region ===== CC 分支 =====
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
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle)
    )
    CC_live_nt.add_transition(
        CC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_PHCCI", index=cycle)
    )
    CC_live.add_transition(
        tCC,
        probability_func=lambda cycle, p: params.get(key="p_CC_treat", index=cycle)
    )
    CC_live.add_transition(
        CC_live_nt,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_treat", index=cycle)
    )
    CC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    CC.add_transition(
        death_cc,
        probability_func=lambda cycle, p: params.get(key="p_CC_Death", index=cycle)
    )
    CC.add_transition(
        CC_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_Death", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== tCC 分支 =====
    # >>> _tunnel_ 前 10 年未进展 >>>
    tCC.add_transition(
        cured,
        probability_func=lambda cycle, p: 0.079
    )
    tCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    tCC.add_transition(
        tCC,
        probability_func=lambda cycle, p: 1 - 0.079 - params.get(key="p_Death", index=cycle)
    )
    # <<< _tunnel_ 前 10 年未进展 <<<
    # endregion
    model = MarkovModel(
        states=[
            death, death_hcc, death_cc,
            Healthy,
            CHB, CHB_shaicha, CHB_noshaicha,
            pCC, pCC_shaicha, pCC_noshaicha,
            pHCCI, pHCCI_shaicha, pHCCI_noshaicha,
            cHCCI, sHCCI, sHCCI_live,
            sCC, CC, tCC,
            cured,
            pre_ps_CC, pre_ps_HCCI_1,
            pCC_stemp1, pCC_stemp3,
            pCC_ns_live, pCC_ns_fx, pCC_ns_fx_nt, pCC_ns_nfx,
            pHCCI_s_stay, pHCCI_s_to_cI,
            sCC_live, sCC_live_nt,
            CC_live, CC_live_nt,
        ],
        initial_distribution={"Healthy": 100000}
    )

    print("状态下标：", model.state_index)

    model.run(cycles=84, params=params)

    np.set_printoptions(precision=3, suppress=True)
    print(f"最终状态分布\nhealthy | CHB:\n {model.results['state_counts'][-1][[3, 4]]}")
    k = 10
    print(f"前 {k} cycle 状态分布\nhealthy | CHB | death:")
    for i in range(k):
        tmp = model.results['state_counts'][i]
        tmp = np.array(tmp)
        print(f"{tmp[[3, 4, 0]]}")

    # 可视化状态分布随时间的变化
    plt.figure(figsize=(12, 16))
    time_points = range(85)
    for state in model.non_temporary_states:
        idx = model._get_state_index(state.name)
        plt.plot(time_points, model.results["state_counts"][:, idx], label=f"{state.name} ({state.description})")
    plt.xlabel("周期")
    plt.ylabel("比例")
    plt.title("状态分布随时间的变化")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    my_treeage_shaicha()
