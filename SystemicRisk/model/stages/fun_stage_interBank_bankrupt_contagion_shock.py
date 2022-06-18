## 函数：破产银行间挤兑流动传染冲击阶段

##########################################
#状态/调试
##########################################

"函数：破产银行间挤兑流动传染冲击阶段"
def stage_interBank_bankrupt_contagion_shock(A:SystemicRiskAgent, b:TypeState{1}, ib:TypeState{2}, para:dict,env:dict):
    ## # 破产银行间挤兑流动传染冲击
    # env['stage_name'] = "破产银行间挤兑流动传染冲击阶段"
    # @testprintln "开始阶段$(env['stage_name'])："
    
    update_B_state(BB, BI; to = "bankrupt", from = "any")
    A.BB.Shock_BI_run_br_s[A.BB.br] = A.BB.A_BI_all[A.BB.br] # 计算应银行内冲击传导至银行间传染冲击
    update_B_Shock(BB, BI, b, ib; byWay = "Shock_BI_run_br_s") # 更新挤兑流动冲击源头变量Shock_run_s
    A.BB.Shock_P_run_s[A.BB.br] = A.BB.A_P[A.BB.br] # 银行内冲击传导至银行厂商贷款传染冲击
    for i in findall(A.BB.br) # 破产银行计划收回资产，导致其对各债务银行之资产变动，造成破产银行间挤兑流动冲击
        A.BI.Shock_BI_run_br[A.BI.deb[i], i] = A.BI.A_BI[i, A.BI.deb[i]]
        pass
    update_B_Shock(BB, BI, b, ib; byWay = "Shock_BI_run_br") # 更新挤兑流动冲击目标变量Shock_run_t
    update_B_state(BB, BI; to = "bankrupt", from = "any")

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass # functions
