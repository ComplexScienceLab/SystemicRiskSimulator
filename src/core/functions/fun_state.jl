# "功能函数集：计算构建银行与银行间相关状态及其转换。"

## 功能函数集：计算构建银行与银行间相关状态及其转换。

##########################################
#状态/使用
##########################################



function init_listOfRelationInStateOfBanks!(bank::BankCommercial, interbank::BankInterbank)
    interbank.cre = calc_listOfRelationInStateOfBanks(interbank; isState = bank.on, goal = "creditor")
    interbank.deb = calc_listOfRelationInStateOfBanks(interbank; isState = bank.on, goal = "debtor")
end


"计算示性向量之于银行健康的。"
function calc_isHealthy!(bank::BankCommercial, interbank::BankInterbank)
    condition = (bank.E_all .>= LESS1 .&& bank.A_Q .>= LESS1 .&& bank.Shock_def_t + LESS1 .<= bank.E_all .&& bank.Shock_run_t + LESS1 .<= bank.A_Q .&& bank.on)
    if bank.hel != condition
        bank.hel = condition
        interbank.hel = (bank.hel .&& bank.hel')
    end
end

"计算示性向量之于银行健康的，来自资不抵债的。"
function calc_isHealthy_from_isInsolvent!(bank::BankCommercial, interbank::BankInterbank)
    condition = (bank.E_all .>= LESS1 .&& bank.A_Q .>= LESS1 .&& bank.Shock_def_t + LESS1 .<= bank.E_all .&& bank.on)
    if bank.hel != condition
        bank.hel = condition
        interbank.hel = (bank.hel .&& bank.hel')
    end
end

"更新示性向量之于银行健康的，来自资不抵债的。"
function update_isHealthy_from_isInsolvent!(bank::BankCommercial, interbank::BankInterbank)
    condition = (.!(bank.isv .|| bank.ilq) .&& bank.on)
    if bank.hel != condition
        bank.hel = condition
        interbank.hel = (bank.hel .&& bank.hel')
    end
end

"计算示性向量之于银行健康的，来自流动性短缺的。" # 内容同于calc_isHealthy!。
function calc_isHealthy_from_isIlliquity!(bank::BankCommercial, interbank::BankInterbank)
    condition = (bank.E_all .>= LESS1 .&& bank.A_Q .>= LESS1 .&& bank.Shock_run_t + LESS1 .<= bank.A_Q .&& bank.on)
    if bank.hel != condition
        bank.hel = condition
        interbank.hel = (bank.hel .&& bank.hel')
    end
end

"更新示性向量之于银行健康的，来自流动性短缺的。" # 内容同于update_isHealthy_from_isInsolvent!
function update_isHealthy_from_isIlliquity!(bank::BankCommercial, interbank::BankInterbank)
    condition = (.!(bank.isv .|| bank.ilq) .&& bank.on)
    if bank.hel != condition
        bank.hel = condition
        interbank.hel = (bank.hel .&& bank.hel')
    end
end



"计算示性向量之于银行资不抵债的。"
function calc_isInsolvent!(bank::BankCommercial, interbank::BankInterbank)
    condition = ((bank.A_all .< bank.Z_all + LESS1 .|| bank.E_all .< LESS1 .|| bank.Shock_def_t + LESS1 .> bank.E_all) .&& bank.on)
    if bank.isv != condition
        bank.isv = condition
        interbank.isv = (bank.isv .|| bank.isv')
        interbank.cre_isv = calc_listOfRelationInStateOfBanks(interbank; isState = bank.isv, goal = "creditor")
        interbank.deb_isv = calc_listOfRelationInStateOfBanks(interbank; isState = bank.isv, goal = "debtor")
    end
end

"计算示性向量之于银行资不抵债的，来自健康的。"
function calc_isInsolvent_from_isHealthy!(bank::BankCommercial, interbank::BankInterbank)
    condition = ((bank.A_all .< bank.Z_all + LESS1 .|| bank.E_all .< LESS1 .|| bank.Shock_def_t + LESS1 .> bank.E_all) .&& bank.on)
    if bank.isv != condition
        bank.isv = condition
        interbank.isv = (bank.isv .|| bank.isv')
        interbank.cre_isv = calc_listOfRelationInStateOfBanks(interbank; isState = bank.isv, goal = "creditor")
        interbank.deb_isv = calc_listOfRelationInStateOfBanks(interbank; isState = bank.isv, goal = "debtor")
    end
end

"更新示性向量之于银行资不抵债的，来自健康的。" # 内容同于calc_isInsolvent_from_isHealthy!
function update_isInsolvent_from_isHealthy!(bank::BankCommercial, interbank::BankInterbank)
    condition = ((bank.A_all .< bank.Z_all + LESS1 .|| bank.E_all .< LESS1 .|| bank.Shock_def_t + LESS1 .> bank.E_all) .&& bank.on)
    if bank.isv != condition
        bank.isv = condition
        interbank.isv = (bank.isv .|| bank.isv')
        interbank.cre_isv = calc_listOfRelationInStateOfBanks(interbank; isState = bank.isv, goal = "creditor")
        interbank.deb_isv = calc_listOfRelationInStateOfBanks(interbank; isState = bank.isv, goal = "debtor")
    end
end

"计算示性向量之于银行流动性短缺的。"
function calc_isIlliquity!(bank::BankCommercial, interbank::BankInterbank)
    condition = ((bank.Shock_run_t + LESS1 .>= bank.A_Q) .&& bank.on)
    if bank.ilq != condition
        bank.ilq = condition
        interbank.ilq = (bank.ilq .|| bank.ilq')
        interbank.cre_ilq = calc_listOfRelationInStateOfBanks(interbank; isState = bank.ilq, goal = "creditor")
        interbank.deb_ilq = calc_listOfRelationInStateOfBanks(interbank; isState = bank.ilq, goal = "debtor")
    end
end

"计算示性向量之于银行流动性短缺的，来自健康的。" # 内容同于calc_isIlliquity!
function calc_isIlliquity_from_isHealthy!(bank::BankCommercial, interbank::BankInterbank)
    condition = ((bank.Shock_run_t + LESS1 .>= bank.A_Q) .&& bank.on)
    if bank.ilq != condition
        bank.ilq = condition
        interbank.ilq = (bank.ilq .|| bank.ilq')
        interbank.cre_ilq = calc_listOfRelationInStateOfBanks(interbank; isState = bank.ilq, goal = "creditor")
        interbank.deb_ilq = calc_listOfRelationInStateOfBanks(interbank; isState = bank.ilq, goal = "debtor")
    end
end

"更新示性向量之于银行流动性短缺的，来自健康的。" # 内容同于calc_isIlliquity!
function update_isIlliquity_from_isHealthy!(bank::BankCommercial, interbank::BankInterbank)
    condition = ((bank.Shock_run_t + LESS1 .>= bank.A_Q) .&& bank.on)
    if bank.ilq != condition
        bank.ilq = condition
        interbank.ilq = (bank.ilq .|| bank.ilq')
        interbank.cre_ilq = calc_listOfRelationInStateOfBanks(interbank; isState = bank.ilq, goal = "creditor")
        interbank.deb_ilq = calc_listOfRelationInStateOfBanks(interbank; isState = bank.ilq, goal = "debtor")
    end
end

"计算示性向量之于银行破产的。"
function calc_isBankrupt!(bank::BankCommercial, interbank::BankInterbank)
    condition = (bank.isv .|| bank.ilq)
    if bank.br != condition
        bank.br = condition
        interbank.br = (bank.br .&& bank.br')
        interbank.cre_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "creditor")
        interbank.deb_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "debtor")
    end
end

"计算示性向量之于破产的，来自资不抵债的。" # 同于calc_isBankrupt!
function calc_isBankrupt_from_isInsolvent!(bank::BankCommercial, interbank::BankInterbank)
    condition = (bank.isv .|| bank.ilq)
    if bank.br != condition
        bank.br = condition
        interbank.br = (bank.br .&& bank.br')
        interbank.cre_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "creditor")
        interbank.deb_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "debtor")
    end
end

"计算示性向量之于破产的，来自流动性短缺的。" # 同于calc_isBankrupt!
function calc_isBankrupt_from_isIlliquity!(bank::BankCommercial, interbank::BankInterbank)
    condition = (bank.isv .|| bank.ilq)
    if bank.br != condition
        bank.br = condition
        interbank.br = (bank.br .&& bank.br')
        interbank.cre_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "creditor")
        interbank.deb_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "debtor")
    end
end

"计算示性向量之于银行存在的。"
function together_isOn!(bank::BankCommercial, interbank::BankInterbank)
    condition = (bank.hel .|| bank.isv .|| bank.ilq .|| bank.br)
    if bank.on != condition
        bank.on = condition
        interbank.on = (bank.on .&& bank.on')
        # interbank.listOfCreditorsInOn = calc_listOfRelationInStateOfBanks(interbank; isState = bank.on, goal = "creditor") #HACK，未定义，无用。
        # interbank.listOfDebtorsInOn = calc_listOfRelationInStateOfBanks(interbank; isState = bank.on, goal = "debtor") #HACK，未定义，无用。
    end
end

"更新示性向量之于银行破产的，来自退出的。" #FIXME，有一定不稳定的风险。
function update_isBankrupt_from_isOff!(bank::BankCommercial, interbank::BankInterbank)
    condition = (bank.off)
    if bank.br == condition
        bank.br[: ] = FALSE1
        interbank.br = (bank.br .&& bank.br')
        interbank.cre_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "creditor")
        interbank.deb_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "debtor")
    end
end

"更新示性向量之于银行存在的，来自退出的。"
function update_isOn_from_isOff!(bank::BankCommercial, interbank::BankInterbank)
    condition = (.!bank.off)
    if bank.on != condition
        bank.on = condition
        interbank.on = (bank.on .&& bank.on')
        interbank.cre_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "creditor")
        interbank.deb_br = calc_listOfRelationInStateOfBanks(interbank; isState = bank.br, goal = "debtor")
    end
end

"计算示性向量之于银行退出的。"
function calc_isOff!(bank::BankCommercial, interbank::BankInterbank)
    condition = bank.br .|| bank.off
    if bank.off != condition
        bank.off = condition
        interbank.off = (bank.off .&& bank.off')
    end
end

"更新示性向量之于银行退出的，来自存在的。"
function update_isOff_from_isOn!(bank::BankCommercial, interbank::BankInterbank)
    condition = .!bank.on
    if bank.off != condition
        bank.off = condition
        interbank.off = (bank.off .&& bank.off')
    end
end

"计算示性向量之于银行退出的，来自破产的。"
function calc_isOff_from_isBankrupt!(bank::BankCommercial, interbank::BankInterbank)
    calc_isOff!(bank, interbank)
    interbank.cre_br = []
    interbank.deb_br = []
end

"计算示性向量之于银行需要偿还银行间负债的。"
function calc_isNeededBoBI!(bank::BankCommercial, interbank::BankInterbank)
    bank.nBoBI = (bank.Shock_BI_run_ilq_t .> 0 .&& bank.on)
end

"计算示性向量之于银行能够偿还银行间负债的。"
function calc_isEnabledBoBI!(bank::BankCommercial, interbank::BankInterbank)
    bank.eBoBI = (bank.Shock_BI_run_ilq_t .> 0 .&& bank.A_Q .> 0 .&& bank.on)
end

"计算示性向量之于银行能够偿还银行间负债的，从需要偿还银行间负债的。"
function calc_isEnabledBoBI_from_isNeededBoBI!(bank::BankCommercial, interbank::BankInterbank)
    bank.eBoBI = (bank.nBoBI .&& bank.A_Q .> 0)
end

"计算示性向量之于银行需要偿还居民部门存款的。"
function calc_isNeededBoD!(bank::BankCommercial, interbank::BankInterbank)
    bank.nBoD = (bank.Shock_D_run_t .> 0 .&& bank.on)
end

"计算示性向量之于银行能够偿还居民部门存款的。"
function calc_isEnabledBoD!(bank::BankCommercial, interbank::BankInterbank)
    bank.eBoD = (bank.Shock_D_run_t .> 0 .&& bank.A_Q .> 0 .&& bank.on)
end

"计算示性向量之于银行能够偿还居民部门存款的，从需要偿还居民部门存款的。"
function calc_isEnabledBoD_from_isNeededBoD!(bank::BankCommercial, interbank::BankInterbank)
    bank.eBoD = (bank.nBoD .&& bank.A_Q .> 0)
end

"计算示性向量之于银行需要收回厂商贷款的。"
function calc_isNeededLiP!(bank::BankCommercial, interbank::BankInterbank)
    bank.nLiP = (bank.Shock_P_run_s .> 0 .&& bank.on)
end

"计算示性向量之于银行能够收回厂商贷款的。"
function calc_isEnabledLiP!(bank::BankCommercial, interbank::BankInterbank)
    bank.eLiP = (bank.Shock_P_run_s .> 0 .&& bank.on) #HACK后续可能会补充条件 .&& producer.A_Q .> 0
end

"计算示性向量之于银行能够收回厂商贷款的，从需要收回厂商贷款的。"
function calc_isEnabledLiP_from_isNeededLiP!(bank::BankCommercial, interbank::BankInterbank)
    bank.eLiP = (bank.nLiP) #HACK后续可能会补充条件 .&& producer.A_Q .> 0
end




"""
计算信息列表之于各状态银行之各关联银行。
# Arguments
- `interbank::BankInterbank`:  银行间主体。
- `listOfRelationInStateOfBanks::Array`:  列表之于各银行之各状态之关系。
- `isState::Vector`:  示性向量之于各银行之状态。
- `goal::String`:  参数，确定计算债务方或债权方。
    - `debtor`:  计算对应的债务方银行；
    - `creditor`:  计算对应的债权方银行；
# Returns
- `listOfRelationInStateOfBanks`:  返回对应状态下的债权或者债务关系的银行列表；
"""
function calc_listOfRelationInStateOfBanks(interbank::BankInterbank; isState::Vector, goal::String)
    # 计算示性矩阵之于银行间风险敞口的
    if goal == "debtor"
        isExposure = ((interbank.A_BI .> 0.0) .&& isState)
    elseif goal == "creditor"
        isExposure = ((interbank.Z_BI .> 0.0) .&& isState)
    else
        throw(DomainError(byWay, "关键词取值错误！"))
    end
    listOfRelationInStateOfBanks = [[] for i in 1: env[:numBank]]
    for i in 1: env[:numBank]
        listOfRelationInStateOfBanks[i] = findall(isExposure[i, : ]) # 获取对应状态下的债权或者债务关系的银行列表
    end
    return listOfRelationInStateOfBanks
end


"""
更新各银行之状态

# Arguments

`to::String`:  参数，转移状态目标；
- `any`:  到任意状态；
- `healthy`:  到健康状态；
- `insolvent`:  到资不抵债状态；
- `illiquity`:  到流动性短缺状态；
- `bankrupt`:  到破产状态；
- `off`:  到退出状态；
- `needed repay BI`:  到是否需要偿还银行间借款状态；
- `enabled repay BI`:  到是否可以偿还银行间借款状态；
- `needed repay Z_D`:  到是否需要偿还居民存款状态；
- `enabled repay Z_D`:  到是否需要偿还借款状态；
- `needed collect A_P`:  到是否可以收回厂商贷款状态；
- `enabled collect A_P`:  到是否可以收回厂商贷款状态；

`from::String`:  参数，转移状态源头；
- `any`:  从任意状态出发；
- `healthy`:  从健康状态出发；
- `insolvent`:  从资不抵债状态出发；
- `illiquity`:  从流动性短缺状态出发；
- `bankrupt`:  从破产状态出发；
- `off`:  从退出状态出发；
- `needed repay BI`:  到是否需要偿还银行间借款状态；
- `needed repay Z_D`:  到是否需要偿还居民存款状态；
- `needed collect A_P`:  到是否可以收回厂商贷款状态；
"""
function update_B_state!(bank::BankCommercial, interbank::BankInterbank; to::String = "any", from::String = "any")
    if to == "any" #FIXME 这个可能有缺陷
        if from == "any"
            init_listOfRelationInStateOfBanks!(bank, interbank)
            calc_isInsolvent!(bank, interbank)
            calc_isIlliquity!(bank, interbank)
            calc_isHealthy!(bank, interbank)
            calc_isBankrupt!(bank, interbank)
            together_isOn!(bank, interbank)
            # calc_isOff!(bank, interbank)
            # calc_isOn!(bank, interbank)
        elseif from == "healthy"
            calc_isInsolvent_from_isHealthy!(bank, interbank)
            update_isHealthy_from_isInsolvent!(bank, interbank)
            calc_isIlliquity_from_isHealthy!(bank, interbank)
            update_isHealthy_from_isIlliquity!(bank, interbank)
        elseif from == "insolvent"
            calc_isHealthy_from_isInsolvent!(bank, interbank)
            update_isInsolvent_from_isHealthy!(bank, interbank)
            calc_isBankrupt_from_isInsolvent!(bank, interbank)
        elseif from == "illiquity"
            calc_isHealthy_from_isIlliquity!(bank, interbank)
            update_isIlliquity_from_isHealthy!(bank, interbank)
            calc_isBankrupt_from_isIlliquity!(bank, interbank)
        elseif from == "bankrupt"
            calc_isOff_from_isBankrupt!(bank, interbank)
            update_isOn_from_isOff!(bank, interbank)
            interbank.cre = calc_listOfRelationInStateOfBanks(interbank; isState = bank.on, goal = "creditor")
            interbank.deb = calc_listOfRelationInStateOfBanks(interbank; isState = bank.on, goal = "debtor")
        elseif from == "off"
            @testprintln "无须更新！"
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "healthy"
        if from == "any"
            calc_isHealthy!(bank, interbank)
            update_isInsolvent_from_isHealthy!(bank, interbank)
            update_isIlliquity_from_isHealthy!(bank, interbank)
        elseif from == "healthy"
            @testprintln "无须更新！"
        elseif from == "insolvent"
            calc_isHealthy_from_isInsolvent!(bank, interbank)
            calc_isInsolvent_from_isHealthy!(bank, interbank)
        elseif from == "illiquity"
            calc_isHealthy_from_isIlliquity!(bank, interbank)
            update_isIlliquity_from_isHealthy!(bank, interbank)
        elseif from == "bankrupt"
            @testprintln "无须更新！"
        elseif from == "off"
            @testprintln "无须更新！"
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "insolvent"
        if from == "any"
            calc_isInsolvent!(bank, interbank)
            update_isHealthy_from_isInsolvent!(bank, interbank)
        elseif from == "healthy"
            calc_isInsolvent_from_isHealthy!(bank, interbank)
            update_isHealthy_from_isInsolvent!(bank, interbank)
        elseif from == "insolvent"
            @testprintln "无须更新！"
        elseif from == "illiquity"
            # calc_isIlliquity_from_isHealthy!(bank, interbank) # 错误，可以删除！
            # calc_isHealthy_from_isIlliquity!(bank, interbank) # 错误，可以删除！
            # calc_isHealthy_from_isInsolvent!(bank, interbank) # 错误，可以删除！
            # calc_isInsolvent_from_isHealthy!(bank, interbank) # 错误，可以删除！
            @testprintln "无须更新！"
        elseif from == "bankrupt"
            @testprintln "无须更新！"
        elseif from == "off"
            @testprintln "无须更新！"
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "illiquity"
        if from == "any"
            calc_isIlliquity!(bank, interbank)
            update_isHealthy_from_isIlliquity!(bank, interbank)
        elseif from == "healthy"
            calc_isIlliquity_from_isHealthy!(bank, interbank)
            update_isHealthy_from_isIlliquity!(bank, interbank)
        elseif from == "insolvent"
            # calc_isHealthy_from_isInsolvent!(bank, interbank) # 错误，可以删除！
            # update_isInsolvent_from_isHealthy!(bank, interbank) # 错误，可以删除！
            # update_isIlliquity_from_isHealthy!(bank, interbank) # 错误，可以删除！
            @testprintln "无须更新！"
        elseif from == "illiquity"
            @testprintln "无须更新！"
        elseif from == "bankrupt"
            @testprintln "无须更新！"
        elseif from == "off"
            @testprintln "无须更新！"
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "bankrupt"
        if from == "any"
            calc_isBankrupt!(bank, interbank)
        elseif from == "healthy"
            calc_isInsolvent_from_isHealthy!(bank, interbank)
            update_isHealthy_from_isInsolvent!(bank, interbank)
            calc_isIlliquity!(bank, interbank)
            update_isHealthy_from_isIlliquity!(bank, interbank)
            calc_isBankrupt_from_isInsolvent!(bank, interbank)
            calc_isBankrupt_from_isIlliquity!(bank, interbank)
        elseif from == "insolvent"
            calc_isBankrupt_from_isInsolvent!(bank, interbank)
        elseif from == "illiquity"
            calc_isBankrupt_from_isIlliquity!(bank, interbank)
        elseif from == "bankrupt"
            @testprintln "无须更新！"
        elseif from == "off"
            @testprintln "无须更新！"
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "off"
        if from == "any"
            calc_isOff!(bank, interbank)
            update_isOn_from_isOff!(bank, interbank)
        elseif from == "healthy"
            @testprintln "无须更新！"
        elseif from == "insolvent"
            @testprintln "无须更新！"
        elseif from == "illiquity"
            @testprintln "无须更新！"
        elseif from == "bankrupt"
            calc_isOff_from_isBankrupt!(bank, interbank)
            update_isOn_from_isOff!(bank, interbank)
            update_isBankrupt_from_isOff!(bank, interbank)
            interbank.cre = calc_listOfRelationInStateOfBanks(interbank; isState = bank.on, goal = "creditor")
            interbank.deb = calc_listOfRelationInStateOfBanks(interbank; isState = bank.on, goal = "debtor")
        elseif from == "off"
            @testprintln "无须更新！"
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "on"
        if from == "any"
            together_isOn!(bank, interbank)
            update_isOff_from_isOn!(bank, interbank)
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "needed repay BI"
        if from == "any"
            calc_isNeededBoBI!(bank, interbank)
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "enabled repay BI"
        if from == "any"
            calc_isEnabledBoBI!(bank, interbank)
        elseif from == "needed repay BI"
            calc_isEnabledBoBI_from_isNeededBoBI!(bank, interbank)
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "needed repay Z_D"
        if from == "any"
            calc_isNeededBoD!(bank, interbank)
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "enabled repay Z_D"
        if from == "any"
            calc_isEnabledBoD!(bank, interbank)
        elseif from == "needed repay Z_D"
            calc_isEnabledBoD_from_isNeededBoD!(bank, interbank)
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "needed collect A_P"
        if from == "any"
            calc_isNeededLiP!(bank, interbank)
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    elseif to == "enabled collect A_P"
        if from == "any"
            calc_isEnabledLiP!(bank, interbank)
        elseif from == "needed collect A_P"
            calc_isEnabledLiP_from_isNeededLiP!(bank, interbank)
        else
            throw(DomainError(byWay, "关键词from取值错误！"))
        end
    else
        throw(DomainError(to, "关键词to取值错误！"))
    end
end # function
