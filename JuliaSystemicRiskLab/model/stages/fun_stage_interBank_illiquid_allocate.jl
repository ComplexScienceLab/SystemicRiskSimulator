## 函数：银行间挤兑流动分配借贷流量阶段

##########################################
#状态/使用
##########################################

"函数：银行间挤兑流动分配借贷流量阶段"
function stage_interBank_illiquid_allocate!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict,env::Dict)
    ## # 流动性短缺银行间挤兑流动分配借贷流量阶段
    # env[:stage_name] = "银行间挤兑流动分配借贷流量阶段"
    @testprintln "开始阶段$(env[:stage_name])："

    update_B_state!(BB, BI; target = "needed collect A_P", source = "any")
    update_B_state!(BB, BI; target = "enabled collect A_P", source = "any")
    BB.Li_P[BB.eLiP] = BB.Shock_P_run_s[BB.eLiP] # 计算银行收回厂商贷款流量
    update_B_transfer!(BB, BI, b, ib; byWay = "Li_P")

    update_B_state!(BB, BI; target = "needed repay Z_D", source = "any")
    update_B_state!(BB, BI; target = "enabled repay Z_D", source = "any")
    update_B_state!(BB, BI; target = "needed repay BI", source = "any")
    update_B_state!(BB, BI; target = "enabled repay BI", source = "any")
    @. BB.Bo_all[BB.eBoBI|BB.eBoD] = min(BB.A_Q[BB.eBoBI|BB.eBoD], BB.Shock_run_t[BB.eBoBI|BB.eBoD]) # 计算银行偿还借款总流量
    @. BB.Bo_D[BB.eBoBI|BB.eBoD] = BB.Shock_D_run_t[BB.eBoBI|BB.eBoD] * (BB.Bo_all[BB.eBoBI|BB.eBoD] / BB.Shock_run_t[BB.eBoBI|BB.eBoD]) # 计算银行偿还居民借款流量
    @. BB.Bo_BI_all[BB.eBoBI|BB.eBoD] = BB.Shock_BI_run_ilq_t[BB.eBoBI|BB.eBoD] * (BB.Bo_all[BB.eBoBI|BB.eBoD] / BB.Shock_run_t[BB.eBoBI|BB.eBoD]) # 计算银行偿还银行间借款流量
    update_B_transfer!(BB, BI, b, ib; byWay = "Bo_D") #HACK 这个必须放在这里！
    update_B_transfer!(BB, BI, b, ib; byWay = "Bo_BI_all")
    for i in findall(BB.eBoBI) # 计算银行偿还各债权银行借款流量
        @. BI.Bo_BI[i, BI.cre[i]] = BI.Shock_BI_run_ilq[i, BI.cre[i]] * (BB.Bo_BI_all[i] / BB.Shock_BI_run_ilq_t[i])
    end
    update_B_transfer!(BB, BI, b, ib; byWay = "Bo_BI")

    @testprintln "结束阶段$(env[:stage_name])。"
    return BB, BI
end # function
