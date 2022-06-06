## 函数：破产银行间挤兑流动传染冲击阶段

##########################################
#状态/调试
##########################################

"函数：破产银行间挤兑流动传染冲击阶段"
function stage_interBank_bankrupt_contagion_shock!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict,env::Dict)
    ## # 破产银行间挤兑流动传染冲击
    # env[:stageName] = "破产银行间挤兑流动传染冲击阶段"
    @testprintln "开始阶段$(env[:stageName])："
    
    update_B_state!(BB, BI; to = "bankrupt", from = "any")
    BB.Shock_BI_run_br_s[BB.br] = BB.A_BI_all[BB.br] # 计算应银行内冲击传导至银行间传染冲击
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_br_s") # 更新挤兑流动冲击源头变量Shock_run_s
    BB.Shock_P_run_s[BB.br] = BB.A_P[BB.br] # 银行内冲击传导至银行厂商贷款传染冲击
    for i in findall(BB.br) # 破产银行计划收回资产，导致其对各债务银行之资产变动，造成破产银行间挤兑流动冲击
        BI.Shock_BI_run_br[BI.deb[i], i] = BI.A_BI[i, BI.deb[i]]
    end
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_br") # 更新挤兑流动冲击目标变量Shock_run_t
    update_B_state!(BB, BI; to = "bankrupt", from = "any")

    @testprintln "结束阶段$(env[:stageName])。"
    return BB, BI
end # function
