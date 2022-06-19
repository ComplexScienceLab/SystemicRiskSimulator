## 函数：资不抵债银行间违约损失冲击阶段

##########################################
#状态/使用
##########################################

"函数：资不抵债银行间违约损失冲击阶段"
def stage_interBank_insolvent_shock(A:SystemicRiskAgent, b:TypeState{1}, ib:TypeState{2}, para:dict, env:dict):
    ## # 资不抵债银行间违约损失冲击阶段
    # env['stage_name'] = "资不抵债银行间违约损失冲击阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    @. A.BB.A_BI_all[b] = max(A.BB.A_BI_all[b] - A.BB.Shock_def_t[b], 0.0) # 银行之银行间资产变动
    update_B_balanceSheet(BB, BI, b, ib; byWay="A_BI_all")
    @. A.BB.E_all[A.BB.on] = max(A.BB.E_all[A.BB.on] - A.BB.Shock_def_t[A.BB.on], 0.0) # 银行之所有者权益变动
    update_B_state(BB, BI; to="insolvent", from="healthy") # 更新各银行之状态，从健康到资不抵债
    @. A.BB.Shock_BI_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_BI_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_BI_all[A.BB.isv]) # 计算应银行内冲击传导至银行间传染冲击
    update_B_Shock(BB, BI, b, ib; byWay="Shock_BI_def_s") # 更新违约损失冲击源头变量Shock_def_s
    @. A.BB.Shock_D_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_BI_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_D[A.BB.isv]) # 计算应银行内冲击传导至银行存款传染冲击
    @. A.BB.Z_BI_all[A.BB.isv] -= A.BB.Shock_BI_def_s[A.BB.isv]  # 银行间负债变动，由于违约
    update_B_balanceSheet(BB, BI, b, ib; byWay="Z_BI_all") # 更新资产负债表，通过Z_D或Z_BI_all
    @. A.BB.Z_D[A.BB.isv] -= A.BB.Shock_D_def_s[A.BB.isv] # 存款负债变动，由于违约
    update_B_balanceSheet(BB, BI, b, ib; byWay="Z_D") # 更新资产负债表，通过Z_D或Z_BI_all

    # update_B_Shock(BB, BI, b, ib; byWay = "clear Shock_B_A and Shock_B_Z") # 清零银行内资产负债冲击

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass # functions

