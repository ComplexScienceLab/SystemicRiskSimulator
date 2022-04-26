## 函数：流动性短缺银行间挤兑流动传染冲击阶段

##########################################
#状态/使用
##########################################

"函数：流动性短缺银行间挤兑流动传染冲击阶段"
function stage_interBank_illiquity_contagion_shock!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict,env::Dict)
    ## # 流动性短缺银行间挤兑流动传染冲击
    # env[:stageName] = "流动性短缺银行间挤兑流动传染冲击阶段"
    @test println("开始阶段$(env[:stageName])：")

    ##BUG 方式一：每个银行只有一次分配传染冲击之行为。
    i_nas = (BB.ilq .& .!BB.isAllocatedShock) # 临时设置示性变量，表示银行其未分配传染冲击。暨每个银行只有一次分配传染冲击之行为。
    @. BB.Shock_BI_run_ilq_s[i_nas] = abs((BB.Shock_run_t[i_nas] - BB.A_Q[i_nas]) / (BB.A_P[i_nas] + BB.A_BI_all[i_nas]) * BB.A_BI_all[i_nas]) # 计算应银行内冲击传导至银行间传染冲击
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_ilq_s") # 更新挤兑流动冲击源头变量Shock_run_t
    @. BB.Shock_P_run_s[i_nas] = abs((BB.Shock_run_t[i_nas] - BB.A_Q[i_nas]) / (BB.A_P[i_nas] + BB.A_BI_all[i_nas]) * BB.A_P[i_nas]) # 银行内冲击传导至银行厂商贷款传染冲击
    @. BB.isAllocatedShock |= BB.ilq # 更新已经分配传染冲击的银行
    for i in findall(i_nas) # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
        @. BI.Shock_BI_run_ilq[BI.deb[i], i] = BI.A_BI[i, BI.deb[i]] * BB.Shock_BI_run_ilq_s[i] / BB.A_BI_all[i]
    end
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_ilq") # 更新挤兑流动冲击源头变量Shock_run_t
    update_B_state!(BB, BI; to = "illiquity", from = "healthy")

    # ##BUG 方式二：每个银行可以有多次分配传染冲击之行为。
    # @. BB.Shock_BI_run_ilq_s[BB.ilq] = abs((BB.Shock_run_t[BB.ilq] - BB.A_Q[BB.ilq]) / (BB.A_P[BB.ilq] + BB.A_BI_all[BB.ilq]) * BB.A_BI_all[BB.ilq]) # 计算应银行内冲击传导至银行间传染冲击
    # update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_ilq_s") # 汇总各银行之流动性短缺流动性挤兑冲击
    # @. BB.Shock_P_run_s[BB.ilq] = abs((BB.Shock_run_t[BB.ilq] - BB.A_Q[BB.ilq]) / (BB.A_P[BB.ilq] + BB.A_BI_all[BB.ilq]) * BB.A_P[BB.ilq]) # 银行内冲击传导至银行厂商贷款传染冲击
    # for i in findall(BB.on) # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
    #     @. BI.Shock_BI_run_ilq[BI.deb[i], i] = BI.A_BI[i, BI.deb[i]] * BB.Shock_BI_run_ilq_s[i] / BB.A_BI_all[i]
    # end
    # update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_ilq") # 加总各单个债务银行遭受总银行间挤兑流动冲击
    # update_B_state!(BB, BI; to = "illiquity", from = "healthy") # 更新各银行之状态，从健康到流动性短缺

    @test println("结束阶段$(env[:stageName])。")
    # return BB, BI
end # function
