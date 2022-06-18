## 函数：银行间挤兑流动分配借贷流量阶段

##########################################
#状态/使用
##########################################

"函数：银行间挤兑流动分配借贷流量阶段"
def stage_interBank_illiquity_allocate(A:SystemicRiskAgent, b:TypeState{1}, ib:TypeState{2}, para:dict,env:dict):
    ## # 流动性短缺银行间挤兑流动分配借贷流量阶段
    # env['stage_name'] = "银行间挤兑流动分配借贷流量阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    update_B_state(BB, BI; to = "needed collect A_P", from = "any")
    update_B_state(BB, BI; to = "enabled collect A_P", from = "any")
    A.BB.Li_P[A.BB.eLiP] = A.BB.Shock_P_run_s[A.BB.eLiP] # 计算银行收回厂商贷款流量
    update_B_transfer(BB, BI, b, ib; byWay = "Li_P")

    update_B_state(BB, BI; to = "needed repay Z_D", from = "any")
    update_B_state(BB, BI; to = "enabled repay Z_D", from = "any")
    update_B_state(BB, BI; to = "needed repay BI", from = "any")
    update_B_state(BB, BI; to = "enabled repay BI", from = "any")
    @. A.BB.Bo_all[A.BB.eBoBI|A.BB.eBoD] = min(A.BB.A_Q[A.BB.eBoBI|A.BB.eBoD], A.BB.Shock_run_t[A.BB.eBoBI|A.BB.eBoD]) # 计算银行偿还借款总流量
    @. A.BB.Bo_D[A.BB.eBoBI|A.BB.eBoD] = A.BB.Shock_D_run_t[A.BB.eBoBI|A.BB.eBoD] * (A.BB.Bo_all[A.BB.eBoBI|A.BB.eBoD] / A.BB.Shock_run_t[A.BB.eBoBI|A.BB.eBoD]) # 计算银行偿还居民借款流量
    @. A.BB.Bo_BI_all[A.BB.eBoBI|A.BB.eBoD] = A.BB.Shock_BI_run_ilq_t[A.BB.eBoBI|A.BB.eBoD] * (A.BB.Bo_all[A.BB.eBoBI|A.BB.eBoD] / A.BB.Shock_run_t[A.BB.eBoBI|A.BB.eBoD]) # 计算银行偿还银行间借款流量
    update_B_transfer(BB, BI, b, ib; byWay = "Bo_D") #HACK 这个必须放在这里！
    update_B_transfer(BB, BI, b, ib; byWay = "Bo_BI_all")
    for i in findall(A.BB.eBoBI) # 计算银行偿还各债权银行借款流量
        @. A.BI.Bo_BI[i, A.BI.cre[i]] = A.BI.Shock_BI_run_ilq[i, A.BI.cre[i]] * (A.BB.Bo_BI_all[i] / A.BB.Shock_BI_run_ilq_t[i])
        pass
    update_B_transfer(BB, BI, b, ib; byWay = "Bo_BI")

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass # functions
