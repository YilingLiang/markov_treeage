import re

pattern = r'(\w+)\s*=\s*State\('
text = """
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
    # region ===== pDCC =====
    pDCC = State(
        name="pDCC",
        description="pDCC"
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
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="and"),
        probability_func=lambda cycle, p: 1
    )
    pDCC.add_transition(
        pDCC_noshaicha,
        condition=create_condition_gq_leq(min_cycle=35, max_cycle=70, cycle_mode="or"),
        probability_func=lambda cycle, p: 1
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
    # region ===== 临床前I期 =====
    pHCCI = State(
        name="pHCCI",
        description="临床前I期",
        utility_func=lambda cycle, p: discount(params.U_HCCI, params.DR, cycle),
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
    # region ===== 临床前II期 =====
    pHCCII = State(
        name="pHCCII",
        description="临床前II期",
        utility_func=lambda cycle, p: discount(params.U_HCCII, params.DR, cycle),
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
        tunnel_cycle=11 #
    )
    tDCC = State(
        name="tDCC",
        description="DCC treated",
        cost_func=lambda cycle, p: state_utility_func(params.Cost_Treat_DCC, params.DR, cycle),
        utility_func=lambda cycle, p: state_utility_func(params.U_health, params.DR, cycle),
        tunnel_cycle=11
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
    pre_ps_CC = State(
        name="pre_ps_CC",
        description="CHB screening to CC",
        is_temporary=True
    )
    pre_ps_CC_1 = State(
        name="pre_ps_CC_1",
        description="CHB screening to CC 1",
        is_temporary=True
    )
    pre_ps_CC_2 = State(
        name="pre_ps_CC_2",
        description="CHB screening to CC 2",
        is_temporary=True
    )

    pre_ps_CC_3 = State(
        name="pre_ps_CC_3",
        description="CHB screening to CC 3",
        is_temporary=True
    )
    pre_ps_CC_3.add_transition(
        sCC,
        probability_func=lambda cycle, p: params.True_pos_cc,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pre_ps_CC_3.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.True_pos_cc
    )
    pre_ps_CC_2.add_transition(
        pre_ps_CC_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pre_ps_CC_2.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pre_ps_CC_1.add_transition(
        pre_ps_CC_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pre_ps_CC_1.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pre_ps_CC.add_transition(
        pre_ps_CC_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pre_ps_CC.add_transition(
        pCC,
        probability_func=lambda cycle, p: 0
    )

    pre_ps_HCCI = State(
        name="pre_ps_HCCI",
        description="CHB screening to pHCCI",
        is_temporary=True
    )
    pre_ps_HCCI_1 = State(
        name="pre_ps_HCCI_1",
        description="CHB screening to pHCCI 1",
        is_temporary=True
    )
    pre_ps_HCCI_2 = State(
        name="pre_ps_HCCI_2",
        description="CHB screening to pHCCI 2",
        is_temporary=True
    )
    pre_ps_HCCI_3 = State(
        name="pre_ps_HCCI_3",
        description="CHB screening to pHCCI 3",
        is_temporary=True
    )

    pre_ps_HCCI_3.add_transition(
        sHCCI,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pre_ps_HCCI_3.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pre_ps_HCCI_2.add_transition(
        pre_ps_HCCI_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pre_ps_HCCI_2.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )

    pre_ps_HCCI_1.add_transition(
        pre_ps_HCCI_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pre_ps_HCCI_1.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )

    pre_ps_HCCI.add_transition(
        pre_ps_HCCI_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pre_ps_HCCI.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 0
    )

    CHB_stay = State(
        name="CHB_stay",
        description="CHB screening to stay",
        is_temporary=True
    )
    CHB_stay_1 = State(
        name="CHB_stay_1",
        description="CHB screening to stay 1",
        is_temporary=True
    )
    CHB_stay_2 = State(
        name="CHB_stay_2",
        description="CHB screening to stay 2",
        is_temporary=True
    )
    CHB_stay_3 = State(
        name="CHB_stay_3",
        description="CHB screening to stay 3",
        is_temporary=True
    )
    CHB_stay_3.add_transition(
        CHB,
        probability_func=lambda cycle, p: params.True_neg_AFP_US,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    CHB_stay_3.add_transition(
        CHB,
        probability_func=lambda cycle, p: 1 - params.True_neg_AFP_US,
    )
    CHB_stay_2.add_transition(
        CHB_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    CHB_stay_2.add_transition(
        CHB,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    CHB_stay_1.add_transition(
        CHB_stay_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk,
    )
    CHB_stay_1.add_transition(
        CHB,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )

    CHB_stay.add_transition(
        CHB_stay_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    CHB_stay.add_transition(
        CHB,
        probability_func=lambda cycle, p: 0
    )
    CHB_shaicha.add_transition(
        CHB_stay,
        probability_func=lambda cycle, p: \
            1 - params.get(key="p_Death", index=cycle) - params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5)) - params.get(key="p_HBV_CC", index=cycle),
    )
    CHB_shaicha.add_transition(
        pre_ps_CC,
        probability_func=lambda cycle, p: params.get(key="p_HBV_CC", index=cycle),
    )
    CHB_shaicha.add_transition(
        pre_ps_HCCI,
        probability_func=lambda cycle, p: params.get(key="p_HBV_pHCCI", index=int(cycle // 5 * 5)),
    )
    CHB_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
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
    pCC_stay = State(
        name="pCC_stay",
        description="pCC screening stay here",
        is_temporary=True
    )
    pCC_stay_1 = State(
        name="pCC_stay_1",
        description="pCC screening stay here 1",
        is_temporary=True
    )
    pCC_stay_2 = State(
        name="pCC_stay_2",
        description="pCC screening stay here 2",
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
    pCC_stay_2.add_transition(
        pCC_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pCC_stay_2.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pCC_stay_1.add_transition(
        pCC_stay_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pCC_stay_1.add_transition(
        pCC,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pCC_stay.add_transition(
        pCC_stay_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pCC_stay.add_transition(
        pCC,
        probability_func=lambda cycle, p: 0
    )
    pCC_to_DCC = State(
        name="pCC_to_DCC",
        description="pCC screening CC_to_DCC",
        is_temporary=True
    )
    pCC_to_DCC_1 = State(
        name="pCC_to_DCC_1",
        description="pCC to DCC here 1",
        is_temporary=True
    )
    pCC_to_DCC_2 = State(
        name="pCC_to_DCC_2",
        description="pCC to DCC here 2",
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
    pCC_to_DCC_2.add_transition(
        pCC_to_DCC_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pCC_to_DCC_2.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pCC_to_DCC_1.add_transition(
        pCC_to_DCC_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pCC_to_DCC_1.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pCC_to_DCC.add_transition(
        pCC_to_DCC_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pCC_to_DCC.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 0
    )
    pCC_to_HCCI = State(
        name="pCC_to_HCCI",
        description="pCC screening CC_to_HCCI",
        is_temporary=True
    )
    pCC_to_HCCI_1 = State(
        name="pCC_to_HCCI_1",
        description="pCC to HCCI here 1",
        is_temporary=True
    )
    pCC_to_HCCI_2 = State(
        name="pCC_to_HCCI_2",
        description="pCC to HCCI here 2",
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
    pCC_to_HCCI_2.add_transition(
        pCC_to_HCCI_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pCC_to_HCCI_2.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pCC_to_HCCI_1.add_transition(
        pCC_to_HCCI_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pCC_to_HCCI_1.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pCC_to_HCCI.add_transition(
        pCC_to_HCCI_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pCC_to_HCCI.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 0
    )
    pCC_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pCC_shaicha.add_transition(
        pCC_to_HCCI,
        probability_func=lambda cycle, p: params.get(key="p_CC_PHCCI", index=cycle),
    )
    pCC_shaicha.add_transition(
        pCC_to_DCC,
        probability_func=lambda cycle, p: params.get(key="p_CC_DCC", index=cycle),
    )
    pCC_shaicha.add_transition(
        pCC_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_CC_PHCCI", index=cycle) - params.get(key="p_CC_DCC", index=cycle),
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
        description="pCC no screening live no diagnose",
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
    pDCC_stay = State(
        name="pDCC_stay",
        description="pDCC screening stay here",
        is_temporary=True
    )
    pDCC_stay_1 = State(
        name="pDCC_stay_1",
        description="pDCC stay here 1",
        is_temporary=True
    )
    pDCC_stay_2 = State(
        name="pDCC_stay_2",
        description="pDCC stay here 2",
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
    pDCC_stay_2.add_transition(
        pDCC_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pDCC_stay_2.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pDCC_stay_1.add_transition(
        pDCC_stay_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pDCC_stay_1.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pDCC_stay.add_transition(
        pDCC_stay_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pDCC_stay.add_transition(
        pDCC,
        probability_func=lambda cycle, p: 0
    )

    pDCC_to_pHCCI = State(
        name="pDCC_to_pHCCI",
        description="pDCC screening DCC_to_pHCCI",
        is_temporary=True
    )
    pDCC_to_pHCCI_1 = State(
        name="pDCC_to_pHCCI_1",
        description="pDCC to pHCCI here 1",
        is_temporary=True
    )
    pDCC_to_pHCCI_2 = State(
        name="pDCC_to_pHCCI_2",
        description="pDCC to pHCCI here 2",
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
    pDCC_to_pHCCI_2.add_transition(
        pDCC_to_pHCCI_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pDCC_to_pHCCI_2.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pDCC_to_pHCCI_1.add_transition(
        pDCC_to_pHCCI_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pDCC_to_pHCCI_1.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pDCC_to_pHCCI.add_transition(
        pDCC_to_pHCCI_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pDCC_to_pHCCI.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 0
    )

    pDCC_shaicha.add_transition(
        death,
        probability_func=lambda cycle, p: params.get(key="p_Death", index=cycle)
    )
    pDCC_shaicha.add_transition(
        pDCC_to_pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_DCC_PHCCI", index=cycle),
    )
    pDCC_shaicha.add_transition(
        pDCC_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_DCC_PHCCI", index=cycle) - params.get(key="p_Death", index=cycle),
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
        description="pDCC no screening live no diagnose",
        is_temporary=True
    )
    pDCC_ns_live_nfx.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: params.get(key="p_DCC_PHCCI", index=cycle)
    )
    pDCC_ns_live_nfx.add_transition(
        pDCC,
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
    pHCCI_s_stay = State(
        name="pHCCI_s_stay",
        description="pHCCI screening stay here",
        is_temporary=True
    )
    pHCCI_s_stay_1 = State(
        name="pHCCI_s_stay_1",
        description="pHCCI stay here 1",
        is_temporary=True
    )
    pHCCI_s_stay_2 = State(
        name="pHCCI_s_stay_2",
        description="pHCCI stay here 2",
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
    pHCCI_s_stay_2.add_transition(
        pHCCI_s_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCI_s_stay_2.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCI_s_stay_1.add_transition(
        pHCCI_s_stay_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCI_s_stay_1.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCI_s_stay.add_transition(
        pHCCI_s_stay_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCI_s_stay.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 0
    )

    pHCCI_s_to_pII = State(
        name="pHCCI_s_to_pII",
        description="pHCCI screening pHCCI_to_pHCCII",
        is_temporary=True
    )
    pHCCI_s_to_pII_1 = State(
        name="pHCCI_s_to_pII_1",
        description="pHCCI to pII here 1",
        is_temporary=True
    )
    pHCCI_s_to_pII_2 = State(
        name="pHCCI_s_to_pII_2",
        description="pHCCI to pII here 2",
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
    pHCCI_s_to_pII_2.add_transition(
        pHCCI_s_to_pII_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCI_s_to_pII_2.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCI_s_to_pII_1.add_transition(
        pHCCI_s_to_pII_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCI_s_to_pII_1.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCI_s_to_pII.add_transition(
        pHCCI_s_to_pII_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCI_s_to_pII.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 0
    )
    pHCCI_s_to_cI = State(
        name="pHCCI_s_to_cI",
        description="pHCCI screening pHCCI_to_cHCCI",
        is_temporary=True
    )
    pHCCI_s_to_cI_1 = State(
        name="pHCCI_s_to_cI_1",
        description="pHCCI to cI here 1",
        is_temporary=True
    )
    pHCCI_s_to_cI_2 = State(
        name="pHCCI_s_to_cI_2",
        description="pHCCI to cI here 2",
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
    pHCCI_s_to_cI_2.add_transition(
        pHCCI_s_to_cI_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCI_s_to_cI_2.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCI_s_to_cI_1.add_transition(
        pHCCI_s_to_cI_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCI_s_to_cI_1.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCI_s_to_cI.add_transition(
        pHCCI_s_to_cI_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCI_s_to_cI.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: 0
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
        probability_func=lambda cycle, p: params.get(key="p_HCCI_HCCII", index=cycle),
    )
    pHCCI_shaicha.add_transition(
        pHCCI_s_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCI_HCCII", index=cycle) -
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
        probability_func=lambda cycle, p: params.get(key="p_HCCI_HCCII", index=cycle)
    )
    pHCCI_noshaicha.add_transition(
        cHCCI,
        probability_func=lambda cycle, p: params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5))
    )
    pHCCI_noshaicha.add_transition(
        pHCCI,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCI_Detected", index=int(cycle // 5 * 5)) -
                                          params.get(key="p_HCCI_HCCII", index=cycle) - params.get(key="p_Death", index=cycle)
    )
    # endregion
    # region ===== 临床前II期筛查分支 =====
    pHCCII_s_stay = State(
        name="pHCCII_s_stay",
        description="pHCCII screening stay here",
        is_temporary=True
    )
    pHCCII_s_stay_1 = State(
        name="pHCCII_s_stay_1",
        description="pHCCII stay here 1",
        is_temporary=True
    )
    pHCCII_s_stay_2 = State(
        name="pHCCII_s_stay_2",
        description="pHCCII stay here 2",
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
    pHCCII_s_stay_2.add_transition(
        pHCCII_s_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCII_s_stay_2.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCII_s_stay_1.add_transition(
        pHCCII_s_stay_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCII_s_stay_1.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCII_s_stay.add_transition(
        pHCCII_s_stay_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCII_s_stay.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 0
    )
    pHCCII_s_to_pIII = State(
        name="pHCCII_s_to_pIII",
        description="pHCCII screening pHCCII_to_pHCCIII",
        is_temporary=True
    )
    pHCCII_s_to_pIII_1 = State(
        name="pHCCII_s_to_pIII_1",
        description="pHCCII to pIII here 1",
        is_temporary=True
    )
    pHCCII_s_to_pIII_2 = State(
        name="pHCCII_s_to_pIII_2",
        description="pHCCII to pIII here 2",
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
    pHCCII_s_to_pIII_2.add_transition(
        pHCCII_s_to_pIII_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCII_s_to_pIII_2.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCII_s_to_pIII_1.add_transition(
        pHCCII_s_to_pIII_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCII_s_to_pIII_1.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCII_s_to_pIII.add_transition(
        pHCCII_s_to_pIII_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCII_s_to_pIII.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 0
    )
    pHCCII_s_to_cII = State(
        name="pHCCII_s_to_cII",
        description="pHCCII screening pHCCII_to_cHCCII",
        is_temporary=True
    )
    pHCCII_s_to_cII_1 = State(
        name="pHCCII_s_to_cII_1",
        description="pHCCII to cII here 1",
        is_temporary=True
    )
    pHCCII_s_to_cII_2 = State(
        name="pHCCII_s_to_cII_2",
        description="pHCCII to cII here 2",
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
    pHCCII_s_to_cII_2.add_transition(
        pHCCII_s_to_cII_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCII_s_to_cII_2.add_transition(
        cHCCII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCII_s_to_cII_1.add_transition(
        pHCCII_s_to_cII_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCII_s_to_cII_1.add_transition(
        cHCCII,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCII_s_to_cII.add_transition(
        pHCCII_s_to_cII_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCII_s_to_cII.add_transition(
        pHCCII,
        probability_func=lambda cycle, p: 0
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
        probability_func=lambda cycle, p: params.get(key="p_HCCII_HCCIII", index=cycle),
    )
    pHCCII_shaicha.add_transition(
        pHCCII_s_stay,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCII_HCCIII", index=cycle) - params.get(
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
    pHCCIII_s_stay = State(
        name="pHCCIII_s_stay",
        description="pHCCIII screening stay here",
        is_temporary=True
    )
    pHCCIII_s_stay_1 = State(
        name="pHCCIII_s_stay_1",
        description="pHCCIII stay here 1",
        is_temporary=True
    )
    pHCCIII_s_stay_2 = State(
        name="pHCCIII_s_stay_2",
        description="pHCCIII stay here 2",
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
    pHCCIII_s_stay_2.add_transition(
        pHCCIII_s_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCIII_s_stay_2.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIII_s_stay_1.add_transition(
        pHCCIII_s_stay_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCIII_s_stay_1.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCIII_s_stay.add_transition(
        pHCCIII_s_stay_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIII_s_stay.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 0
    )
    pHCCIII_s_to_pIV = State(
        name="pHCCIII_s_to_pIV",
        description="pHCCIII screening pHCCIII_to_pHCCIV",
        is_temporary=True
    )
    pHCCIII_s_to_pIV_1 = State(
        name="pHCCIII_s_to_pIV_1",
        description="pHCCIII to pIV 1",
        is_temporary=True
    )
    pHCCIII_s_to_pIV_2 = State(
        name="pHCCIII_s_to_pIV_2",
        description="pHCCIII to pIV 2",
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
    pHCCIII_s_to_pIV_2.add_transition(
        pHCCIII_s_to_pIV_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCIII_s_to_pIV_2.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIII_s_to_pIV_1.add_transition(
        pHCCIII_s_to_pIV_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCIII_s_to_pIV_1.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCIII_s_to_pIV.add_transition(
        pHCCIII_s_to_pIV_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIII_s_to_pIV.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 0
    )
    pHCCIII_ns_to_cIII = State(
        name="pHCCIII_ns_to_cIII",
        description="pHCCIII screening pHCCII_to_cHCCIII",
        is_temporary=True
    )
    pHCCIII_ns_to_cIII_1 = State(
        name="pHCCIII_ns_to_cIII_1",
        description="pHCCIII to cIII 1",
        is_temporary=True
    )
    pHCCIII_ns_to_cIII_2 = State(
        name="pHCCIII_ns_to_cIII_2",
        description="pHCCIII to cIII 2",
        is_temporary=True
    )
    pHCCIII_ns_to_cIII_3 = State(
        name="pHCCIII_ns_to_cIII_3",
        description="pHCCIII to cIII 3",
        is_temporary=True
    )
    pHCCIII_ns_to_cIII_3.add_transition(
        sHCCIII,
        probability_func=lambda cycle, p: params.True_pos_AFP_USearly,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCIII_ns_to_cIII_3.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USearly
    )
    pHCCIII_ns_to_cIII_2.add_transition(
        pHCCIII_ns_to_cIII_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCIII_ns_to_cIII_2.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIII_ns_to_cIII_1.add_transition(
        pHCCIII_ns_to_cIII_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCIII_ns_to_cIII_1.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCIII_ns_to_cIII.add_transition(
        pHCCIII_ns_to_cIII_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIII_ns_to_cIII.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: 0
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
        pHCCIII_s_to_pIV,
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_HCCIV", index=cycle)
    )
    pHCCIII_shaicha.add_transition(
        pHCCIII_s_stay,
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
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_HCCIV", index=cycle),
        transition_cost_func=lambda cycle,
                                    p: params.Cost_HBsAgque + params.Cost_AFP + params.Cost_US + params.Cost_Diag + params.Cost_Treat_III
    )
    pHCCIII_noshaicha.add_transition(
        cHCCIII,
        probability_func=lambda cycle, p: params.get(key="p_HCCIII_Detected", index=int(cycle // 5 * 5)),
        transition_cost_func=lambda cycle,
                                    p: params.Cost_HBsAgque + params.Cost_AFP + params.Cost_US + params.Cost_Diag + params.Cost_Treat_III
    )
    pHCCIII_noshaicha.add_transition(
        pHCCIII,
        probability_func=lambda cycle, p: 1 - params.get(key="p_HCCIII_Detected", index=int(cycle // 5 * 5)) - params.get(
            key="p_HCCIII_HCCIV", index=cycle) - params.get(key="p_Death", index=cycle),
        transition_cost_func=lambda cycle, p: params.Cost_HBsAgque + params.Cost_AFP + params.Cost_US + params.Cost_Diag + params.Cost_Treat_III
    )
    # endregion
    # region ===== 临床前IV期筛查分支 =====
    pHCCIV_s_stay = State(
        name="pHCCIV_s_stay",
        description="pHCCIV screening stay here",
        is_temporary=True
    )
    pHCCIV_s_stay_1 = State(
        name="pHCCIV_s_stay_1",
        description="pHCCIV stay 1",
        is_temporary=True
    )
    pHCCIV_s_stay_2 = State(
        name="pHCCIV_s_stay_2",
        description="pHCCIV stay 2",
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
    pHCCIV_s_stay_2.add_transition(
        pHCCIV_s_stay_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCIV_s_stay_2.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIV_s_stay_1.add_transition(
        pHCCIV_s_stay_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCIV_s_stay_1.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCIV_s_stay.add_transition(
        pHCCIV_s_stay_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIV_s_stay.add_transition(
        pHCCIV,
        probability_func=lambda cycle, p: 0
    )
    pHCCIV_s_to_cIV = State(
        name="pHCCIV_s_to_cIV",
        description="pHCCIV screening pHCCIV_to_cHCCIV",
        is_temporary=True
    )
    pHCCIV_s_to_cIV_1 = State(
        name="pHCCIV_s_to_cIV_1",
        description="pHCCIV to cIV 1",
        is_temporary=True
    )
    pHCCIV_s_to_cIV_2 = State(
        name="pHCCIV_s_to_cIV_2",
        description="pHCCIV to cIV 2",
        is_temporary=True
    )
    pHCCIV_s_to_cIV_3 = State(
        name="pHCCIV_s_to_cIV_3",
        description="pHCCIV to cIV 3",
        is_temporary=True
    )
    pHCCIV_s_to_cIV_3.add_transition(
        sHCCIV,
        probability_func=lambda cycle, p: params.True_pos_AFP_USlate,
        transition_cost_func=lambda cycle, p: discount(params.Cost_Diag, params.DR, cycle)
    )
    pHCCIV_s_to_cIV_3.add_transition(
        cHCCIV,
        probability_func=lambda cycle, p: 1 - params.True_pos_AFP_USlate
    )
    pHCCIV_s_to_cIV_2.add_transition(
        pHCCIV_s_to_cIV_3,
        probability_func=lambda cycle, p: params.Rate_screening2,
        transition_cost_func=lambda cycle, p: discount(params.Cost_AFP + params.Cost_US, params.DR, cycle)
    )
    pHCCIV_s_to_cIV_2.add_transition(
        cHCCIV,
        probability_func=lambda cycle, p: 1 - params.Rate_screening2
    )
    pHCCIV_s_to_cIV_1.add_transition(
        pHCCIV_s_to_cIV_2,
        probability_func=lambda cycle, p: params.Posrate_highrisk
    )
    pHCCIV_s_to_cIV_1.add_transition(
        cHCCIV,
        probability_func=lambda cycle, p: 1 - params.Posrate_highrisk
    )
    pHCCIV_s_to_cIV.add_transition(
        pHCCIV_s_to_cIV_1,
        probability_func=lambda cycle, p: 1,
        transition_cost_func=lambda cycle, p: discount(params.Cost_HBsAgque, params.DR, cycle)
    )
    pHCCIV_s_to_cIV.add_transition(
        cHCCIV,
        probability_func=lambda cycle, p: 0
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
        probability_func=lambda cycle, p: 1 - params.get(key="p_Death", index=cycle) - params.get(key="p_CC_Death", index=cycle)
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
    # >>> _tunnel_ 前 10 年未进展 >>>
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
    # <<< _tunnel_ 前 10 年未进展 <<<
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
    tCC_live.add_transition(
        tCC,
        probability_func=lambda cycle, p: 1 - params.get(key="p_CC_PHCCI_treat", index=cycle) - params.get(key="p_CC_DCC_treat", index=cycle)
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
"""

# 使用 re.findall 提取所有匹配的状态名
state_names = re.findall(pattern, text, re.MULTILINE)
print(state_names, len(state_names))  # 输出: ['cHCCI', 'cHCCII']
print(str(state_names).replace("'", ""))