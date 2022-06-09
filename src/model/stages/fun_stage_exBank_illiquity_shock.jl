## 函数：银行外部挤兑流动冲击阶段

##########################################
#状态/使用
##########################################

"函数：银行外部挤兑流动冲击阶段"
function stage_exBank_illiquity_shock!(A::SystemicRiskAgent, b::TypeState{1}, ib::TypeState{2}, para::Dict, env::Dict) #= BB_t1::BankCommercial, BI_t1::BankInterbank,  =#
    ## # 银行外部挤兑流动冲击阶段
    # env[:stageName] = "银行外部挤兑流动冲击阶段"
    @testprintln "开始阶段$(env[:stageName])："

    A.BB.Shock_D_run_t[para[:list_Shock_exBI_t]] = para[:Shock_exBI_run_t][para[:list_Shock_exBI_t]] # 生成居民存款挤兑流动冲击
    update_B_Shock!(BB, BI, b, ib; byWay="Shock_D_run_t") # 居民存款挤兑流动冲击传导至银行内负债冲击
    update_B_state!(BB, BI; to="illiquity", from="healthy") # 更新各银行之状态，从健康到流动性短缺

    @testprintln "结束阶段$(env[:stageName])。"
    return BB, BI
end # function
