from lab.markov_tunnel_db_v4 import MarkovModel, State, discount
from lab.condition import create_condition, create_condition_gq_leq
from parameter.define_parameters import Parameters
from parameter.define_tables import Table


def my_treeage_shaicha():
    # region ===== 参数表格定义 =====
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
    phealthToCHB = Table({0: 2.7045e-05,
 5: 5.07011e-05,
 10: 0.000307248,
 15: 0.000177832,
 20: 5.39777e-05,
 25: 4.28634e-05,
 30: 8.63917e-05,
 35: 0.007978121,
 40: 0.006593994,
 45: 4.77516e-05,
 50: 0.009767031,
 55: 0.007020632,
 60: 8.52151e-05,
 65: 0.007164131,
 70: 0.00162877,
 75: 0.000489096,
 80: 0.004708357})
    ratescreen = Table({1: 0, 2: 1, 3: 1})
    Utility = Table({0: 1.0, 1: 0.761, 2: 0.643, 3: 0.76, 4: 0.68, 5: 0.4, 6: 0.25})
    # endregion

    # region ===== 参数定义 =====
    params = Parameters(
        Cost_AFP=(0.65, "AFP检测费用"),
        Cost_Diag=(90.03, "诊断费用"),
        Cost_HBsAgque=(0.07 + 2.22, "HBsAg检查费用（风险评估交通费+误工费+HBsAg检测）"),
        Cost_Treat_CC=(5688.29 + 1392.4, "肝硬化治疗费(直接+间接)"),
        Cost_Treat_DCC=(5688.29 + 1392.4, "失代偿"),
        Cost_Treat_HBV=(4563.5, "HBV治疗"),
        Cost_Treat_I=(9362.96 + 1651.45, ""),
        Cost_Treat_II=(9019.05 + 1960.32, ""),
        Cost_Treat_III=(8983.77 + 1808.38, ""),
        Cost_Treat_IV=(9588.45 + 1860.69, ""),
        Cost_US=(10 + 6.33 + 4.38, "超声检查费用（临床检查交通费+误工费+AFP+US）"),
        Cost_vac=(82.6, ""),
        cost_zhi_CC=(30657.7, "抗病毒治疗下肝硬化费用"),
        cost_zhi_CHB=(18689.5, "抗病毒治疗下慢乙肝费用"),
        cost_zhi_DCC=(43318.1, "抗病毒治疗下失代偿费用"),
        DR=(0.03, "贴现率"),
        dr=(0.00, "贴现率2"),
        p_CC_DCC=(0.058, "代偿肝硬化_失代偿肝硬化"),
        p_CC_DCC_treat=(0.019, "治疗后 代偿肝硬化_失代偿肝硬化"),
        p_CC_Death=(0.031, "代偿肝硬化_死于代偿肝硬化"),
        p_CC_Death_treat=(0.017, ""),
        p_CC_PHCCI=(0.0316, "代偿肝硬化_临床前I期"),
        p_CC_PHCCI_treat=(0.02, "治疗后 代偿肝硬化_临床前I期"),
        p_CC_treat=(0.7, ""),
        p_CC_zifa=(0.15, ""),
        p_DCC_Death=(0.17, "失代偿肝硬化_死于失代偿肝硬化"),
        p_DCC_Death_treat=(0.095, ""),
        p_DCC_PHCCI=(0.034, "失代偿肝硬化_临床前I期"),
        p_DCC_PHCCI_treat=(0.024, ""),
        p_DCC_treat=(0.7, ""),
        p_DCC_zifa=(0.7, ""),
        p_Death=(Death, "xxx_死于其他原因"),
        p_HBV_CC=(0.0173, "慢性乙肝_代偿肝硬化"),
        p_HBV_pHCCI=(pHBVToHCCI, "慢性乙肝_临床前I期(---)"),
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
        p_health_pHCCI=(pHBVToHCCI, "健康_临床前I期(---)"),  # Note: Divided by 23.4 in original
        p_sHCCI_Death=(0.74 * HCCIdeath, ""),
        p_sHCCII_Death=(0.74 * HCCIIdeath, ""),
        p_sHCCIII_Death=(0.74 * HCCIIIdeath, ""),
        p_sHCCIV_Death=(0.74 * HCCIVdeath, ""),
        Posrate_highrisk=(1, "HBsAg阳性高危率"),
        Rate_screening=(None, ""),  # Empty in original
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
        utility_func=lambda cycle, p: discount(params.U_health, params.DR, cycle),
    )
    health_shaicha = State(
        name="health_shaicha",
        description="健康筛查",
        is_temporary=True,
    )
    health_noshaicha = State(
        name="health_noshaicha",
        description="健康不筛查",
        is_temporary=True,
    )
    Healthy.add_transition(
        health_shaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70),
        probability_func=lambda cycle, p: 1
    )
    Healthy.add_transition(
        health_noshaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== CHB慢性乙肝感染 =====
    CHB = State(
        name="CHB",
        description="慢性乙肝感染",
        cost_func=lambda cycle, p: 0,
        utility_func=lambda cycle, p: discount(params.U_health, params.DR, cycle)
    )
    CHB_shaicha = State(
        name="CHB_shaicha",
        description="CHB_shaicha",
        is_temporary=True
    )
    CHB_noshaicha = State(
        name="CHB_noshaicha",
        description="CHB_noshaicha",
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
        description="pCC筛查",
        is_temporary=True,
    )
    pCC_noshaicha = State(
        name="pCC_noshaicha",
        description="pCC不筛查",
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
    # region ===== pDCC =====
    pDCC = State(
        name="pDCC",
        description="pDCC"
    )
    pDCC_shaicha = State(
        name="pDCC_shaicha",
        description="pDCC筛查",
        is_temporary=True,
    )
    pDCC_noshaicha = State(
        name="pDCC_noshaicha",
        description="pDCC不筛查",
        is_temporary=True,
    )
    pDCC.add_transition(
        pDCC_shaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pDCC.add_transition(
        pDCC_noshaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion

    # region ===== 临床前I期 =====
    pHCCI = State(
        name="pHCCI",
        description="临床前I期",
        utility_func=lambda cycle, p: discount(params.U_HCCI, params.DR, cycle),
    )
    pHCCI_shaicha = State(
        name="pHCCI_shaicha",
        description="pHCCI_shaicha",
        is_temporary=True,
    )
    pHCCI_noshaicha = State(
        name="pHCCI_noshaicha",
        description="pHCCI_noshaicha",
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
    # region ===== 临床前II期 =====
    pHCCII = State(
        name="pHCCII",
        description="临床前II期",
        utility_func=lambda cycle, p: discount(params.U_HCCII, params.DR, cycle),
    )
    pHCCII_shaicha = State(
        name="pHCCII_shaicha",
        description="pHCCII_shaicha",
        is_temporary=True,
    )
    pHCCII_noshaicha = State(
        name="pHCCII_noshaicha",
        description="pHCCII_noshaicha",
        is_temporary=True,
    )
    pHCCII.add_transition(
        pHCCII_shaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pHCCII.add_transition(
        pHCCII_noshaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== 临床前III期 =====
    pHCCIII = State(
        name="pHCCIII",
        description="临床前III期",
        utility_func=lambda cycle, p: discount(params.U_HCCIII, params.DR, cycle),
    )
    pHCCIII_shaicha = State(
        name="pHCCIII_shaicha",
        description="pHCCIII_shaicha",
        is_temporary=True,
    )
    pHCCIII_noshaicha = State(
        name="pHCCIII_noshaicha",
        description="pHCCIII_noshaicha",
        is_temporary=True,
    )
    pHCCIII.add_transition(
        pHCCIII_shaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pHCCIII.add_transition(
        pHCCIII_noshaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion
    # region ===== 临床前IV期 =====
    pHCCIV = State(
        name="pHCCIV",
        description="临床前IV期",
        utility_func=lambda cycle, p: discount(params.U_HCCIV, params.DR, cycle),
    )
    pHCCIV_shaicha = State(
        name="pHCCIV_shaicha",
        description="pHCCIV_shaicha",
        is_temporary=True,
    )
    pHCCIV_noshaicha = State(
        name="pHCCIV_noshaicha",
        description="pHCCIV_noshaicha",
        is_temporary=True,
    )
    pHCCIV.add_transition(
        pHCCIV_shaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pHCCIV.add_transition(
        pHCCIV_noshaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
    )
    # endregion

    # region ===== cHCC-I =====
    cHCCI = State(
        name="cHCCI",
        description="cHCCI",
        utility_func=lambda cycle, p: discount(params.U_HCCI, params.DR, cycle),
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
        utility_func=lambda cycle, p: discount(params.U_HCCII, params.DR, cycle),
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
        utility_func=lambda cycle, p: discount(params.U_HCCIII, params.DR, cycle),
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
        utility_func=lambda cycle, p: discount(params.U_HCCIV, params.DR, cycle),
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
        cost_func=lambda cycle, p: discount(params.Cost_Treat_I, params.DR, cycle),
        utility_func=lambda cycle, p: discount(params.U_HCCI, params.DR, cycle),
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
        cost_func=lambda cycle, p: discount(params.Cost_Treat_II, params.DR, cycle),
        utility_func=lambda cycle, p: discount(params.U_HCCII, params.DR, cycle),
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
        cost_func=lambda cycle, p: discount(params.Cost_Treat_III, params.DR, cycle),
        utility_func=lambda cycle, p: discount(params.U_HCCIII, params.DR, cycle),
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
        cost_func=lambda cycle, p: discount(params.Cost_Treat_IV, params.DR, cycle),
        utility_func=lambda cycle, p: discount(params.U_HCCIV, params.DR, cycle),
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
        cost_func=lambda cycle, p: params.Cost_Treat_CC,
        utility_func=lambda cycle, p: discount(params.U_CC, params.DR, cycle)
    )
    sDCC = State(
        name="sDCC",
        description="sDCC",
        cost_func=lambda cycle, p: params.Cost_Treat_DCC,
        utility_func=lambda cycle, p: discount(params.U_DCC, params.DR, cycle)
    )
    CC = State(
        name="CC",
        description="CC",
        cost_func=lambda cycle, p: params.Cost_Treat_CC,
        utility_func=lambda cycle, p: discount(params.U_CC, params.DR, cycle),
    )
    DCC = State(
        name="DCC",
        description="DCC",
        cost_func=lambda cycle, p: params.Cost_Treat_DCC,
        utility_func=lambda cycle, p: discount(params.U_DCC, params.DR, cycle)
    )
    tCC = State(
        name="tCC",
        description="tCC",
        tunnel_cycle=11
    )
    tDCC = State(
        name="tDCC",
        description="tDCC",
        tunnel_cycle=11
    )
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
    # region ===== 健康筛查分支 =====
    pre_ps_HCCI = State(
        name="pre_ps_HCCI",
        description="pre_ps_HCCI",
        is_temporary=True
    )
    pre_ps_HCCI.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pre_ps_HCCI.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    health_shaicha.add_transition(
        pre_ps_HCCI,
        probability_func=lambda cycle, p: params.get(key="p_health_pHCCI", index=int(cycle // 5 * 5))
    )
    health_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    health_shaicha.add_transition(
        CHB,
        probability_func=lambda cycle, p: params.get(key="p_health_CHB", index=int(cycle // 5 * 5))
    )
    health_shaicha.add_transition(
        Healthy,
        probability_func=lambda cycle, p: \
            1 - params.get(key="p_health_pHCCI", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle) - params.get(key="p_health_CHB", index=int(cycle // 5 * 5))
    )
    # endregion
    # region ===== 健康不筛查分支 =====
    health_noshaicha.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_health_pHCCI", index=int(cycle // 5 * 5))
    )
    health_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    health_noshaicha.add_transition(
        CHB,
        probability_func=lambda cycle, p: params.get(key="p_health_CHB", index=int(cycle // 5 * 5))
    )
    health_noshaicha.add_transition(
        Healthy,
        probability_func=lambda cycle, p: \
            1 - params.get(key="p_health_pHCCI", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle) - params.get(
                key="p_health_CHB", index=int(cycle // 5 * 5))

    )
    # endregion
    # region ===== CHB筛查分支 =====
    pre_ps_CC = State(
        name="pre_ps_CC",
        description="pre_ps_CC",
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
        name="pre_ps_HCCI_2",
        description="pre_ps_HCCI_2",
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
        probability_func=lambda cycle, p: params.get(key="p_HBV_CC", index=cycle)
    )
    CHB_shaicha.add_transition(
        pre_ps_HCCI_1,
        probability_func=lambda cycle, p: params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5))
    )
    CHB_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    CHB_shaicha.add_transition(
        CHB,
        probability_func=lambda cycle, p: \
            1 - params.get(key="p_Death", index=cycle) - params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5)) - params.get(key="p_HBV_CC", index=cycle)
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
        description="pCC_stemp1",
        is_temporary=True
    )
    pCC_stemp2 = State(
        name="pCC_stemp2",
        description="pCC_stemp2",
        is_temporary=True
    )
    pCC_stemp3 = State(
        name="pCC_stemp3",
        description="pCC_stemp3",
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
    pCC_stemp2.add_transition(
        sDCC,
        probability_func=lambda cycle, p: params.True_pos_cc * params.Rate_screening2
    )
    pCC_stemp2.add_transition(
        pDCC,
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
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle)
    )
    pCC_shaicha.add_transition(
        pCC_stemp2,
        probability_func=lambda cycle, p: params.get(key="p_CC_DCC", index=cycle)
    )
    pCC_shaicha.add_transition(
        pCC_stemp1,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_CC_PHCCI", index=cycle) - params.get(key="p_CC_DCC", index=cycle)
    )
    # endregion
    # region ===== pCC 不筛查分支 =====
    # live 路线
    pCC_ns_live = State(
        name="pCC_ns",
        description="pCC_ns",
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
        description="pCC_ns_fx",
        is_temporary=True
    )
    pCC_ns_fx_nt = State(
        name="pCC_ns_fx_nt",
        description="pCC_ns_fx_nt",
        is_temporary=True
    )
    pCC_ns_fx_nt.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle)
    )
    pCC_ns_fx_nt.add_transition(
        DCC,
        probability_func=lambda cycle, p: params.get(key="p_CC_DCC", index=cycle)
    )
    pCC_ns_fx_nt.add_transition(
        CC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_DCC", index=cycle) - params.get(key="p_CC_PHCCI", index=cycle)
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
        description="pCC_ns_nfx",
        is_temporary=True
    )
    pCC_ns_nfx.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle)
    )
    pCC_ns_nfx.add_transition(
        pDCC,
        probability_func=lambda cycle, p: params.get(key="p_CC_DCC", index=cycle)
    )
    pCC_ns_nfx.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_DCC", index=cycle) - params.get(
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
    # region ===== pDCC 筛查分支 =====
    pDCC_stemp1 = State(
        name="pDCC_stemp1",
        description="pDCC_stemp1",
        is_temporary=True
    )
    pDCC_stemp1.add_transition(
        sDCC,
        probability_func=lambda cycle, p: params.True_pos_cc * params.Rate_screening2
    )
    pDCC_stemp1.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.True_pos_cc * params.Rate_screening2
    )
    pDCC_stemp2 = State(
        name="pDCC_stemp2",
        description="pDCC_stemp2",
        is_temporary=True
    )
    pDCC_stemp2.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pDCC_stemp2.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pDCC_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pDCC_shaicha.add_transition(
        pDCC_stemp2,
        probability_func=lambda cycle, p: params.get(key="p_DCC_PHCCI", index=cycle)
    )
    pDCC_shaicha.add_transition(
        pDCC_stemp1,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_PHCCI", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== pDCC 不筛查分支 =====
    # live 路线
    pDCC_ns_live = State(
        name="pDCC_ns_live",
        description="pDCC_ns_live",
        is_temporary=True
    )
    pDCC_ns_live_fx = State(
        name="pDCC_ns_live_fx",
        description="pDCC_ns_live_fx",
        is_temporary=True
    )
    pDCC_ns_live_fx_nt = State(
        name="pDCC_ns_live_fx_nt",
        description="pDCC_ns_live_fx_nt",
        is_temporary=True
    )
    pDCC_ns_live_fx_nt.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_DCC_PHCCI", index=cycle)
    )
    pDCC_ns_live_fx_nt.add_transition(
        DCC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_PHCCI", index=cycle)
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
        description="pDCC_ns_live_nfx",
        is_temporary=True
    )
    pDCC_ns_live_nfx.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_DCC_PHCCI", index=cycle)
    )
    pDCC_ns_live_nfx.add_transition(
        DCC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_PHCCI", index=cycle)
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
    pHCCI_ns_stay = State(
        name="pHCCI_ns_stay",
        description="pHCCI_ns_stay",
        is_temporary=True
    )
    pHCCI_ns_stay.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCI_ns_stay.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCI_ns_to_pII = State(
        name="pHCCI_ns_to_pII",
        description="pHCCI_ns_to_pII",
        is_temporary=True
    )
    pHCCI_ns_to_pII.add_transition(
        sHCCII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCI_ns_to_pII.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCI_ns_to_cI = State(
        name="pHCCI_ns_to_cI",
        description="pHCCI_ns_to_cI",
        is_temporary=True
    )
    pHCCI_ns_to_cI.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCI_ns_to_cI.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCI_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCI_shaicha.add_transition(
        pHCCI_ns_to_cI,
        probability_func=lambda cycle, p: params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5))
    )
    pHCCI_shaicha.add_transition(
        pHCCI_ns_to_pII,
        probability_func=lambda cycle, p: params.get(key="p_HCCI_HCCII", index=cycle)
    )
    pHCCI_shaicha.add_transition(
        pHCCI_ns_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCI_HCCII", index=cycle) - params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前I期不筛查分支 =====
    pHCCI_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCI_noshaicha.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: params.get(key="p_HCCI_HCCII", index=cycle)
    )
    pHCCI_noshaicha.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5))
    )
    pHCCI_noshaicha.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_HCCI_HCCII", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前II期筛查分支 =====
    pHCCII_ns_stay = State(
        name="pHCCII_ns_stay",
        description="pHCCII_ns_stay",
        is_temporary=True
    )
    pHCCII_ns_stay.add_transition(
        sHCCII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCII_ns_stay.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCII_ns_to_pIII = State(
        name="pHCCII_ns_to_pIII",
        description="pHCCII_ns_to_pIII",
        is_temporary=True
    )
    pHCCII_ns_to_pIII.add_transition(
        sHCCIII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCII_ns_to_pIII.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCII_ns_to_cII = State(
        name="pHCCII_ns_to_cII",
        description="pHCCII_ns_to_cII",
        is_temporary=True
    )
    pHCCII_ns_to_cII.add_transition(
        sHCCII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCII_ns_to_cII.add_transition(
        cHCCII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCII_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCII_shaicha.add_transition(
        pHCCII_ns_to_cII,
        probability_func=lambda cycle, p: params.get(key="p_HCCII_Detected", index=int(cycle // 5 * 5))
    )
    pHCCII_shaicha.add_transition(
        pHCCII_ns_to_pIII,
        probability_func=lambda cycle, p: params.get(key="p_HCCII_HCCIII", index=cycle)
    )
    pHCCII_shaicha.add_transition(
        pHCCII_ns_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCII_HCCIII", index=cycle) - params.get(
            key="p_HCCII_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前II期不筛查分支 =====
    pHCCII_noshaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCII_noshaicha.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: params.get(key="p_HCCII_HCCIII", index=cycle)
    )
    pHCCII_noshaicha.add_transition(
        cHCCII,
        probability_func=lambda cycle, p: params.get(key="p_HCCII_Detected", index=int(cycle // 5 * 5))
    )
    pHCCII_noshaicha.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCII_Detected", index=int(cycle // 5 * 5)) - params.get(
            key="p_HCCII_HCCIII", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前III期筛查分支 =====
    pHCCIII_ns_stay = State(
        name="pHCCIII_ns_stay",
        description="pHCCIII_ns_stay",
        is_temporary=True
    )
    pHCCIII_ns_stay.add_transition(
        sHCCIII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIII_ns_stay.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIII_ns_to_pIV = State(
        name="pHCCIII_ns_to_pIV",
        description="pHCCIII_ns_to_pIV",
        is_temporary=True
    )
    pHCCIII_ns_to_pIV.add_transition(
        sHCCIV,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIII_ns_to_pIV.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIII_ns_to_cIII = State(
        name="pHCCIII_ns_to_cIII",
        description="pHCCII_ns_to_cIII",
        is_temporary=True
    )
    pHCCIII_ns_to_cIII.add_transition(
        sHCCIII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIII_ns_to_cIII.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIII_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCIII_shaicha.add_transition(
        pHCCIII_ns_to_cIII,
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_Detected", index=int(cycle // 5 * 5))
    )
    pHCCIII_shaicha.add_transition(
        pHCCIII_ns_to_pIV,
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_HCCIV", index=cycle)
    )
    pHCCIII_shaicha.add_transition(
        pHCCIII_ns_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCIII_HCCIV", index=cycle) - params.get(
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
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_HCCIV", index=cycle)
    )
    pHCCIII_noshaicha.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_Detected", index=int(cycle // 5 * 5))
    )
    pHCCIII_noshaicha.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCIII_Detected", index=int(cycle // 5 * 5)) - params.get(
            key="p_HCCIII_HCCIV", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前IV期筛查分支 =====
    pHCCIV_s_stay = State(
        name="pHCCIV_s_stay",
        description="pHCCIV_s_stay",
        is_temporary=True
    )
    pHCCIV_s_stay.add_transition(
        sHCCIV,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIV_s_stay.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIV_s_to_cIV = State(
        name="pHCCIV_s_to_cIV",
        description="pHCCIV_s_to_cIV",
        is_temporary=True
    )
    pHCCIV_s_to_cIV.add_transition(
        sHCCIV,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIV_s_to_cIV.add_transition(
        cHCCIV,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly * params.Rate_screening2
    )
    pHCCIV_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pHCCIV_shaicha.add_transition(
        pHCCIV_s_to_cIV,
        probability_func=lambda cycle, p: params.get(key="p_HCCIV_Detected", index=int(cycle // 5 * 5))
    )
    pHCCIV_shaicha.add_transition(
        pHCCIV_s_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCIV_Detected", index=int(cycle // 5 * 5)) - params.get(key="p_Death", index=cycle)
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
        description="sCC_live",
        is_temporary=True
    )
    sCC_live_nt = State(
        name="sCC_live_nt",
        description="sCC_live_nt",
        is_temporary=True
    )
    sCC_live_nt.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle)
    )
    sCC_live_nt.add_transition(
        sDCC,
        probability_func=lambda cycle, p: params.get(key="p_CC_DCC", index=cycle)
    )
    sCC_live_nt.add_transition(
        sCC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_DCC", index=cycle) - params.get(key="p_CC_PHCCI", index=cycle)
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
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== sDCC =====
    sDCC_live = State(
        name="sDCC_live",
        description="sDCC_live",
        is_temporary=True
    )
    sDCC_live_nt = State(
        name="sDCC_live_nt",
        description="sDCC_live_nt",
        is_temporary=True
    )
    sDCC_live_nt.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.get(key="p_DCC_PHCCI", index=cycle)
    )
    sDCC_live_nt.add_transition(
        sDCC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_PHCCI", index=cycle)
    )
    sDCC_live.add_transition(
        tDCC,
        probability_func=lambda cycle, p: params.get(key="p_DCC_treat", index=cycle)
    )
    sDCC_live.add_transition(
        sCC_live_nt,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_treat", index=cycle)
    )
    sDCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    sDCC.add_transition(
        death_dcc,
        probability_func=lambda cycle, p: params.get(key="p_DCC_Death", index=cycle)
    )
    sDCC.add_transition(
        sDCC_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_Death", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== CC =====
    CC_live = State(
        name="CC_live",
        description="CC_live",
        is_temporary=True
    )
    CC_live_nt = State(
        name="CC_live_nt",
        description="CC_live_nt",
        is_temporary=True
    )
    CC_live_nt.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle)
    )
    CC_live_nt.add_transition(
        DCC,
        probability_func=lambda cycle, p: params.get(key="p_CC_DCC", index=cycle)
    )
    CC_live_nt.add_transition(
        CC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_DCC", index=cycle) - params.get(key="p_CC_PHCCI", index=cycle)
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
    # region ===== DCC =====
    DCC_live = State(
        name="DCC_live",
        description="DCC_live",
        is_temporary=True
    )
    DCC_live_nt = State(
        name="DCC_live_nt",
        description="DCC_live_nt",
        is_temporary=True
    )
    DCC_live_nt.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_DCC_PHCCI", index=cycle)
    )
    DCC_live_nt.add_transition(
        DCC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_PHCCI", index=cycle)
    )
    DCC_live.add_transition(
        tDCC,
        probability_func=lambda cycle, p: params.get(key="p_DCC_treat", index=cycle)
    )
    DCC_live.add_transition(
        DCC_live_nt,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_treat", index=cycle)
    )
    DCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    DCC.add_transition(
        death_dcc,
        probability_func=lambda cycle, p: params.get(key="p_DCC_Death", index=cycle)
    )
    DCC.add_transition(
        DCC_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_Death", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== tCC 分支 =====
    tCC.add_tunnel_transition(
        cured,
        probability_func=lambda cycle, p: 0.079
    )
    tCC.add_tunnel_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    tCC.add_tunnel_transition(
        tCC,
        probability_func=lambda cycle, p: 1 - 0.079 - params.get(key="p_Death", index=cycle)
    )
    tCC_live = State(
        name="tCC_live",
        description="tCC_live",
        is_temporary=True
    )
    tCC_live.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI_treat", index=cycle)
    )
    tCC_live.add_transition(
        DCC,
        probability_func=lambda cycle, p: params.get(key="p_CC_DCC_treat", index=cycle)
    )
    tCC.add_transition(
        death_cc,
        probability_func=lambda cycle, p: params.get(key="p_CC_Death_treat", index=cycle)
    )
    tCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    tCC.add_transition(
        tCC_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_Death_treat", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== tDCC 分支 =====
    tDCC.add_tunnel_transition(
        cured,
        probability_func=lambda cycle, p: 0.033
    )
    tDCC.add_tunnel_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    tDCC.add_tunnel_transition(
        tDCC,
        probability_func=lambda cycle, p: 1 - 0.033 - params.get(key="p_Death", index=cycle)
    )
    tDCC_live = State(
        name="tDCC_live",
        description="tDCC_live",
        is_temporary=True
    )
    tDCC_live.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_DCC_PHCCI_treat", index=cycle)
    )
    tDCC_live.add_transition(
        tDCC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_PHCCI_treat", index=cycle)
    )
    tDCC.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    tDCC.add_transition(
        death_dcc,
        probability_func=lambda cycle, p: params.get(key="p_DCC_Death_treat", index=cycle)
    )
    tDCC.add_transition(
        tDCC_live,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_Death_treat", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    model = MarkovModel(
        states=[
            death, death_dcc, death_hcc, death_cc,
            Healthy, health_shaicha, health_noshaicha,
            CHB, CHB_shaicha, CHB_noshaicha,
            pCC, pCC_shaicha, pCC_noshaicha,
            pDCC, pDCC_shaicha, pDCC_noshaicha,
            pHCCI, pHCCI_shaicha, pHCCI_noshaicha,
            pHCCII, pHCCII_shaicha, pHCCII_noshaicha,
            pHCCIII, pHCCIII_shaicha, pHCCIII_noshaicha,
            pHCCIV, pHCCIV_shaicha, pHCCIV_noshaicha,
            cHCCI, cHCCII, cHCCIII, cHCCIV,
            sHCCI, sHCCII, sHCCIII, sHCCIV,
            sCC, sDCC, CC, DCC, tCC, tDCC,
            cured,
            pre_ps_HCCI,
            pre_ps_CC, pre_ps_HCCI_1,
            pCC_stemp1, pCC_stemp2, pCC_stemp3,
            pCC_ns_live, pCC_ns_fx, pCC_ns_fx_nt, pCC_ns_nfx,
            pDCC_stemp1, pDCC_stemp2,
            pDCC_ns_live, pDCC_ns_live_fx, pDCC_ns_live_fx_nt, pDCC_ns_live_nfx,
            pHCCI_ns_stay, pHCCI_ns_to_pII, pHCCI_ns_to_cI,
            pHCCII_ns_stay, pHCCII_ns_to_pIII, pHCCII_ns_to_cII,
            pHCCIII_ns_stay, pHCCIII_ns_to_pIV, pHCCIII_ns_to_cIII,
            pHCCIV_s_stay, pHCCIV_s_to_cIV,
            sCC_live, sCC_live_nt,
            sDCC_live, sDCC_live_nt,
            CC_live, CC_live_nt,
            DCC_live, DCC_live_nt,
            tCC_live,
            tDCC_live,

        ],
        initial_distribution={"Healthy": 100000}
    )
    model.run(cycles=84, params=params, cohort=True)
    print(f"最终状态分布: {model.results['state_counts'][-1]}")


if __name__ == "__main__":
    my_treeage_shaicha()
