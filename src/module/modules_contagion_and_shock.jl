## 函数：模块之于银行传染与冲击

##########################################
#状态/开发
##########################################

"函数：银行外部违约损失传染"
function exBank_insolvent_contagion!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 银行外部违约损失传染阶段
    BB.Shock_P_def_t[para["idx_Shock_exBI_t"]] = para["Shock_exBI_t"][para["idx_Shock_exBI_t"]] # 生成厂商贷款违约损失冲击
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_P_def_t") # 厂商贷款违约损失冲击传导至银行内资产冲击

    return BB, BI
end # function


"函数：银行外部违约损失冲击"
function exBank_insolvent_shock!(BB::BankCommercial, BI::BankInterbank, BB_t1::BankCommercial, BI_t1::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 银行外部违约损失冲击阶段
    BB.A_P[b] -= BB.Shock_def_t[b] # 银行之非银行间资产变动
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "A_P")
    update_B_state!(BB, BI; to = "insolvent", from = "healthy")
    @. BB.E_all[BB.on] = max(BB.E_all[BB.on] - BB.Shock_def_t[BB.on], 0.0) # 银行之所有者权益
    @. BB.Shock_BI_def_s[BB.isv] = abs((BB.Shock_def_t[BB.isv] - BB_t1.E_all[BB.isv]) / (BB_t1.Z_BI_all[BB.isv] + BB_t1.Z_D[BB.isv]) * BB_t1.Z_BI_all[BB.isv]) # 银行内冲击传导至银行间传染冲击
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_def_s") # 更新违约损失冲击源头变量Shock_def_s
    BB.Z_BI_all[BB.isv] = BB_t1.Z_BI_all[BB.isv] - BB.Shock_BI_def_s[BB.isv] # 银行间负债变动，由于违约
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "Z_BI_all") # 汇总各银行之非银行间负债Z_exBI、总负债Z_all，被动地计算所有者权益
    @. BB.Shock_D_def_s[BB.isv] = abs((BB.Shock_def_t[BB.isv] - BB_t1.E_all[BB.isv]) / (BB_t1.Z_BI_all[BB.isv] + BB_t1.Z_D[BB.isv]) * BB_t1.Z_D[BB.isv]) # 银行内冲击传导至银行存款传染冲击
    BB.Z_D[BB.isv] = BB_t1.Z_D[BB.isv] - BB.Shock_D_def_s[BB.isv] # 存款负债变动，由于违约
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "Z_D") # 汇总各银行之非银行间负债Z_exBI、总负债Z_all，被动地计算所有者权益

    # update_B_Shock!(BB, BI, b, ib; byWay = "clear Shock_B_A and Shock_B_Z") # 清零银行内资产负债冲击

    BB.Shock_P_def_t[BB.isv] = ZEROS1[BB.isv] # 清零银行间和银行外冲击变量
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_P_def_t") # 更新违约损失冲击目标变量Shock_def_t

    return BB, BI, BB_t1, BI_t1
end # function




"函数：资不抵债银行间违约损失传染"
function interBank_insolvent_contagion!(BB::BankCommercial, BI::BankInterbank, BB_t1::BankCommercial, BI_t1::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 资不抵债银行间违约损失传染阶段
    for i in findall(BB.isv) # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击
        @. BI.Shock_BI_def[BI.cre[i], i] = BI.Z_BI[i, BI.cre[i]] * BB.Shock_BI_def_s[i] / BB_t1.Z_BI_all[i]
        BI.Z_BI[i, BI.cre[i]] -= BI.Shock_BI_def[BI.cre[i], i]
    end
    # HACK以下部分是否提取出来在阶段1结束之前使用
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "alter to A_BI from Z_BI") # 转换银行间资产负债邻接矩阵
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_def") # 更新违约损失冲击目标变量Shock_def_t

    return BB, BI
end # function


"函数：资不抵债银行间违约损失冲击"
function interBank_insolvent_shock!(BB::BankCommercial, BI::BankInterbank, BB_t1::BankCommercial, BI_t1::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 资不抵债银行间违约损失冲击阶段
    @. BB.A_BI_all[b] = max(BB.A_BI_all[b] - BB.Shock_def_t[b], 0.0) # 银行之银行间资产变动
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "A_BI_all")
    @. BB.E_all[BB.on] = max(BB.E_all[BB.on] - BB.Shock_def_t[BB.on], 0.0) # 银行之所有者权益变动
    update_B_state!(BB, BI; to = "insolvent", from = "healthy") # 更新各银行之状态，从健康到资不抵债
    @. BB.Z_BI_all[BB.isv] = BB_t1.Z_BI_all[BB.isv] - ((BB.Shock_def_t[BB.isv] - BB_t1.E_all[BB.isv]) / (BB_t1.Z_BI_all[BB.isv] + BB_t1.Z_D[BB.isv]) * BB_t1.Z_BI_all[BB.isv]) # 银行间负债变动，由于违约
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "Z_BI_all") # 更新资产负债表，通过Z_D或Z_BI_all
    @. BB.Z_D[BB.isv] = BB_t1.Z_D[BB.isv] - ((BB.Shock_def_t[BB.isv] - BB_t1.E_all[BB.isv]) / (BB_t1.Z_BI_all[BB.isv] + BB_t1.Z_D[BB.isv]) * BB_t1.Z_D[BB.isv]) # 存款负债变动，由于违约
    update_B_balanceSheet!(BB, BI, b, ib; byWay = "Z_D") # 更新资产负债表，通过Z_D或Z_BI_all
    @. BB.Shock_BI_def_s[BB.isv] = abs(BB.Z_BI_all[BB.isv] - BB_t1.Z_BI_all[BB.isv]) # 银行内冲击传导至银行间传染冲击
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_def_s") # 更新违约损失冲击源头变量Shock_def_s
    @. BB.Shock_D_def_s[BB.isv] = abs(BB.Z_D[BB.isv] - BB_t1.Z_D[BB.isv]) # 银行内冲击传导至银行存款传染冲击

    # update_B_Shock!(BB, BI, b, ib; byWay = "clear Shock_B_A and Shock_B_Z") # 清零银行内资产负债冲击

    return BB, BI, BB_t1, BI_t1
end # function


"函数：银行外部挤兑流动冲击。考虑情况：存在部分债务银行之部分债务因为流动性短缺从而无法偿还。"
function exBank_illiquity_shock!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict) #= BB_t1::BankCommercial, BI_t1::BankInterbank,  =#
    ## # 银行外部挤兑流动冲击阶段
    BB.Shock_D_run_t[para["idx_Shock_exBI_t"]] = para["Shock_exBI_t"][para["idx_Shock_exBI_t"]] # 生成居民存款挤兑流动冲击
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_D_run_t") # 居民存款挤兑流动冲击传导至银行内负债冲击
    update_B_state!(BB, BI; to = "illiquity", from = "healthy") # 更新各银行之状态，从健康到流动性短缺

    return BB, BI
end # function


"函数：流动性短缺银行间挤兑流动传染冲击。考虑情况：存在部分债务银行之部分债务因为流动性短缺从而无法偿还。"
function interBank_illiquity_contagion_shock!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 流动性短缺银行间挤兑流动传染冲击

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

    return BB, BI
end # function


"函数：流动性短缺银行间挤兑流动分配借贷流量阶段"
function interBank_illiquity_allocate!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 流动性短缺银行间挤兑流动分配借贷流量阶段

    update_B_state!(BB, BI; to = "needed collect A_P", from = "any")
    update_B_state!(BB, BI; to = "enabled collect A_P", from = "any")
    BB.Li_P[BB.eLiP] = BB.Shock_P_run_s[BB.eLiP] # 计算银行收回厂商贷款流量
    update_B_transfer!(BB, BI, b, ib; byWay = "Li_P")

    update_B_state!(BB, BI; to = "needed repay Z_D", from = "any")
    update_B_state!(BB, BI; to = "enabled repay Z_D", from = "any")
    update_B_state!(BB, BI; to = "needed repay BI", from = "any")
    update_B_state!(BB, BI; to = "enabled repay BI", from = "any")
    @. BB.Bo_all[BB.eBoBI|BB.eBoD] = min(BB.A_Q[BB.eBoBI|BB.eBoD], BB.Shock_run_t[BB.eBoBI|BB.eBoD]) # 计算银行偿还借款总流量
    @. BB.Bo_D[BB.eBoBI|BB.eBoD] = BB.Shock_D_run_t[BB.eBoBI|BB.eBoD] * (BB.Bo_all[BB.eBoBI|BB.eBoD] / BB.Shock_run_t[BB.eBoBI|BB.eBoD]) # 计算银行偿还居民借款流量
    @. BB.Bo_BI_all[BB.eBoBI|BB.eBoD] = BB.Shock_BI_run_ilq_t[BB.eBoBI|BB.eBoD] * (BB.Bo_all[BB.eBoBI|BB.eBoD] / BB.Shock_run_t[BB.eBoBI|BB.eBoD]) # 计算银行偿还银行间借款流量
    update_B_transfer!(BB, BI, b, ib; byWay = "Bo_D") #HACK 这个必须放在这里！
    update_B_transfer!(BB, BI, b, ib; byWay = "Bo_BI_all")
    for i in findall(BB.eBoBI) # 计算银行偿还各债权银行借款流量
        @. BI.Bo_BI[i, BI.cre[i]] = BI.Shock_BI_run_ilq[i, BI.cre[i]] * (BB.Bo_BI_all[i] / BB.Shock_BI_run_ilq_t[i])
    end
    update_B_transfer!(BB, BI, b, ib; byWay = "Bo_BI")

    return BB, BI
end # function

"函数：流动性短缺银行间挤兑流动执行借贷流量阶段"
function interBank_illiquity_repay!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 流动性短缺银行间挤兑流动执行借贷流量阶段

    BB.A_Q[b], BB.A_P[b], BB.Shock_P_run_s[b] = transfer_B_capital_reverse(BB.A_Q[b], BB.A_P[b], BB.Shock_P_run_s[b], BB.Li_P[b]) # 流动资产变动，因收回厂商贷款
    # @. BB.A_Q[b] *= (1 - para["kappa_A_P"]) #HACK 暂时还不用！
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

    return BB, BI
end # function


#TODO"函数：外生破产银行间挤兑流动传染"
function exBank_bankrupt_contagion!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 外生破产银行间挤兑流动传染
    BB.br[para["idx_Shock_exBI_t"]] = para["Shock_exBI_t"][para["idx_Shock_exBI_t"]]
    update_B_state!(BB, BI; to = "bankrupt", from = "any")

    return BB, BI

end # function


"过程：破产银行应偿还负债冲击"#HACK暂时不用
function bankrupt_repay_shock!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 破产银行遭受偿还冲击

    update_B_state!(BB, BI; to = "bankrupt", from = "any")
    BB.Shock_D_run_t[BB.br] = BB.Z_D[BB.br] # 计算破产银行遭受偿还居民存款冲击
    BB.Shock_BI_t[BB.br] = BB.Z_BI_all[BB.br] # 计算破产银行遭受偿还银行间负债冲击

    return BB, BI
end # function

"过程：破产银行间挤兑流动传染冲击"
function interBank_bankrupt_contagion_shock!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict)
    ## # 破产银行间挤兑流动传染冲击

    update_B_state!(BB, BI; to = "bankrupt", from = "any")
    BB.Shock_BI_run_br_s[BB.br] = BB.A_BI_all[BB.br] # 计算应银行内冲击传导至银行间传染冲击
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_br_s") # 更新挤兑流动冲击源头变量Shock_run_s
    BB.Shock_P_run_s[BB.br] = BB.A_P[BB.br] # 银行内冲击传导至银行厂商贷款传染冲击
    for i in findall(BB.br) # 破产银行计划收回资产，导致其对各债务银行之资产变动，造成破产银行间挤兑流动冲击
        BI.Shock_BI_run_br[BI.deb[i], i] = BI.A_BI[i, BI.deb[i]]
    end
    update_B_Shock!(BB, BI, b, ib; byWay = "Shock_BI_run_br") # 更新挤兑流动冲击目标变量Shock_run_t
    update_B_state!(BB, BI; to = "bankrupt", from = "any")

    return BB, BI
end # function





