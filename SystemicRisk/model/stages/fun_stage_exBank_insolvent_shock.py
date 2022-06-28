## 函数：银行外部违约损失冲击

##########################################
#状态/使用
##########################################

"函数：银行外部违约损失冲击阶段"
def stage_exBank_insolvent_shock(self, BB:BankCommercial, BI:BankInterbank, b:TypeState, ib:TypeState, para:dict, env:dict):
    ## # 银行外部违约损失冲击阶段
    # env['stage_name'] = "银行外部违约损失冲击阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    BB.Shock_P_def_t[para['list_Shock_exBI_t']] = para['Shock_exBI_def_t'][para['list_Shock_exBI_t']] # 生成厂商贷款违约损失冲击
    update_B_Shock(BB, BI, b, ib; byWay="Shock_P_def_t") # 厂商贷款违约损失冲击传导至银行内资产冲击
    BB.A_P[b] -= BB.Shock_def_t[b] # 银行之非银行间资产变动
    update_B_balanceSheet(BB, BI, b, ib; byWay="A_P")
    update_B_state(BB, BI; to="insolvent", from="healthy")
    @. BB.E_all[BB.on] = max(BB.E_all[BB.on] - BB.Shock_def_t[BB.on], 0.0) # 银行之所有者权益变动
    update_B_state(BB, BI; to="insolvent", from="healthy") # 更新各银行之状态，从健康到资不抵债
    @. BB.Shock_BI_def_s[BB.isv] = abs((BB.Shock_def_t[BB.isv] - BB.E_all[BB.isv]) / (BB.Z_BI_all[BB.isv] + BB.Z_D[BB.isv]) * BB.Z_BI_all[BB.isv]) # 计算应银行内冲击传导至银行间传染冲击
    update_B_Shock(BB, BI, b, ib; byWay="Shock_BI_def_s") # 更新违约损失冲击源头变量Shock_def_s
    @. BB.Shock_D_def_s[BB.isv] = abs((BB.Shock_def_t[BB.isv] - BB.E_all[BB.isv]) / (BB.Z_BI_all[BB.isv] + BB.Z_D[BB.isv]) * BB.Z_D[BB.isv]) # 计算应银行内冲击传导至银行存款传染冲击
    @. BB.Z_BI_all[BB.isv] -= BB.Shock_BI_def_s[BB.isv]  # 银行间负债变动，由于违约
    update_B_balanceSheet(BB, BI, b, ib; byWay="Z_BI_all") # 更新资产负债表，通过Z_D或Z_BI_all
    @. BB.Z_D[BB.isv] -= BB.Shock_D_def_s[BB.isv] # 存款负债变动，由于违约
    update_B_balanceSheet(BB, BI, b, ib; byWay="Z_D") # 更新资产负债表，通过Z_D或Z_BI_all

    # update_B_Shock(BB, BI, b, ib; byWay = "clear Shock_B_A and Shock_B_Z") # 清零银行内资产负债冲击

    BB.Shock_P_def_t[BB.isv] = np.zeros(env['num_bank'])[BB.isv] # 清零银行间和银行外冲击变量
    update_B_Shock(BB, BI, b, ib; byWay="Shock_P_def_t") # 更新违约损失冲击目标变量Shock_def_t

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass # functions
