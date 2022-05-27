## 函数：银行间挤兑流动执行借贷流量阶段

##########################################
#状态/使用
##########################################

"函数：银行间挤兑流动执行借贷流量阶段"
function stage_interBank_illiquity_repay!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict,env::Dict)
    ## # 流动性短缺银行间挤兑流动执行借贷流量阶段
    # env[:stageName] = "银行间挤兑流动执行借贷流量阶段"
    @testprintln "开始阶段$(env[:stageName])："

    BB.A_Q[b], BB.A_P[b], BB.Shock_P_run_s[b] = transfer_B_capital_reverse(BB.A_Q[b], BB.A_P[b], BB.Shock_P_run_s[b], BB.Li_P[b]) # 流动资产变动，因收回厂商贷款
    # @. BB.A_Q[b] *= (1 - para[:kappa_A_P]) #HACK 暂时还不用！
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "A_Q")
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "A_P")
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_P_run_s")

    BB.Z_D[b], BB.A_Q[b], BB.Shock_D_run_t[b] = transfer_B_capital_reduce(BB.Z_D[b], BB.A_Q[b], BB.Shock_D_run_t[b], BB.Bo_D[b]) # 流动资产变动，因偿还居民存款
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "A_Q")
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "Z_D")
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_D_run_t")

    BI.Shock_BI_run_ilq[ib] -= BI.Bo_BI[ib] # 各银行间挤兑流动冲击变动，当偿还相应的银行间借款时
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_ilq")
    BB.Shock_BI_run_ilq_s[b] -= BB.Li_BI_all[b] # 各银行之银行间挤兑流动冲击源头变动，当收回相应的银行间贷款时
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_ilq_s")
    BI.Z_BI[ib] -= BI.Bo_BI[ib] # 各银行间负债变动，当偿还相应的银行间借款时
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "sum Z_BI")
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "alter to A_BI from Z_BI")
    # BI.A_BI[ib] += BI.Li_BI[ib]' # 各银行间资产变动，当收回相应的银行间贷款时
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "sum A_BI")
    BB.A_Q[b] += (BB.Li_BI_all[b] - BB.Bo_BI_all[b]) # 各银行流动资金变动，当收回相应的银行间贷款、偿还相应的银行间借款时
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "A_Q")

    update_B_state!(BB, BI; to = "healthy", from = "illiquity") # 更新银行状态之流动性短缺的与健康的

    update_B_transfer!(BB, BI, b, ib; byWay = "clear transfer all") # 清零所有不必要的借贷流量变量；

    @testprintln "结束阶段$(env[:stageName])。"
    # return BB, BI
end # function
