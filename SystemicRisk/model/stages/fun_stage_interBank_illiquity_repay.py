## 函数：银行间挤兑流动执行借贷流量阶段

##########################################
#状态/使用
##########################################

from SystemicRisk import SystemicRiskAgent


"函数：银行间挤兑流动执行借贷流量阶段"
def stage_interBank_illiquity_repay(self, A:SystemicRiskAgent, b:TypeState, ib:TypeState, para:dict,env:dict):
    ## # 流动性短缺银行间挤兑流动执行借贷流量阶段
    # env['stage_name'] = "银行间挤兑流动执行借贷流量阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    A.BB.A_Q[b], A.BB.A_P[b], A.BB.Shock_P_run_s[b] = transfer_B_capital_reverse(A.BB.A_Q[b], A.BB.A_P[b], A.BB.Shock_P_run_s[b], A.BB.Li_P[b]) # 流动资产变动，因收回厂商贷款
    # @. A.BB.A_Q[b] *= (1 - para['kappa_A_P']) #HACK 暂时还不用！
    update_B_balanceSheet(BB, BI, b, ib; byWay = "A_Q")
    update_B_balanceSheet(BB, BI, b, ib; byWay = "A_P")
    update_B_Shock(BB, BI, b, ib; byWay = "Shock_P_run_s")

    A.BB.Z_D[b], A.BB.A_Q[b], A.BB.Shock_D_run_t[b] = transfer_B_capital_reduce(A.BB.Z_D[b], A.BB.A_Q[b], A.BB.Shock_D_run_t[b], A.BB.Bo_D[b]) # 流动资产变动，因偿还居民存款
    update_B_balanceSheet(BB, BI, b, ib; byWay = "A_Q")
    update_B_balanceSheet(BB, BI, b, ib; byWay = "Z_D")
    update_B_Shock(BB, BI, b, ib; byWay = "Shock_D_run_t")

    A.BI.Shock_BI_run_ilq[ib] -= A.BI.Bo_BI[ib] # 各银行间挤兑流动冲击变动，当偿还相应的银行间借款时
    update_B_Shock(BB, BI, b, ib; byWay = "Shock_BI_run_ilq")
    A.BB.Shock_BI_run_ilq_s[b] -= A.BB.Li_BI_all[b] # 各银行之银行间挤兑流动冲击源头变动，当收回相应的银行间贷款时
    update_B_Shock(BB, BI, b, ib; byWay = "Shock_BI_run_ilq_s")
    A.BI.Z_BI[ib] -= A.BI.Bo_BI[ib] # 各银行间负债变动，当偿还相应的银行间借款时
    update_B_balanceSheet(BB, BI, b, ib; byWay = "sum Z_BI")
    update_B_balanceSheet(BB, BI, b, ib; byWay = "alter to A_BI from Z_BI")
    # A.BI.A_BI[ib] += A.BI.Li_BI[ib]' # 各银行间资产变动，当收回相应的银行间贷款时
    update_B_balanceSheet(BB, BI, b, ib; byWay = "sum A_BI")
    A.BB.A_Q[b] += (A.BB.Li_BI_all[b] - A.BB.Bo_BI_all[b]) # 各银行流动资金变动，当收回相应的银行间贷款、偿还相应的银行间借款时
    update_B_balanceSheet(BB, BI, b, ib; byWay = "A_Q")

    update_B_state(BB, BI; to = "healthy", from = "illiquity") # 更新银行状态之流动性短缺的与健康的

    update_B_transfer(BB, BI, b, ib; byWay = "clear transfer all") # 清零所有不必要的借贷流量变量；

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass # functions
