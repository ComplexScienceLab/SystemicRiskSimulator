
"程序：定义各类Agents，基于模式3-1"

## 程序：定义各类Agents，基于模式3-1

# using Agents#HACK暂时不用

"定义商业银行复合类型。"
mutable struct BankCommercial{NDIMS1,NDIMS2}
    id::TypeIds{NDIMS1} # 编号 id
    abbr::TypeAbbrs{NDIMS1} # 缩写 abbr
    name::TypeNames{NDIMS1} # 全名 name
    A_all::TypeMoney{NDIMS2} # 总资产 A_all：$A_all=A_BI+A_exBI$
    A_BI_all::TypeMoney{NDIMS2} # 银行间资产加总 A_BI_all
    A_exBI::TypeMoney{NDIMS2} # 非银行间资产 A_exBI：$A_exBI=A_P+A_Q+A_R+A_other$
    A_P::TypeMoney{NDIMS2} # 银行贷款给生产部门之资产（非流动性资产） A_P
    A_Q::TypeMoney{NDIMS2} # 银行持有超额准备金（流动性资产） A_Q
    A_R::TypeMoney{NDIMS2} # 银行持有法定准备金（非流动性资产） A_R
    A_other::TypeMoney{NDIMS2} # 银行持有的其它资产（非流动性资产） A_other
    Z_all::TypeMoney{NDIMS2} # 总负债 Z_all：$Z_total=Z_BI+Z_exBI$
    Z_BI_all::TypeMoney{NDIMS2} # 银行间负债加总 Z_BI_all
    Z_exBI::TypeMoney{NDIMS2} # 非银行间负债 Z_exBI：$Z_exBI=Z_D+Z_other$
    Z_D::TypeMoney{NDIMS2} # 银行获得居民部门存款（非流动性负债） Z_D
    Z_other::TypeMoney{NDIMS2} # 银行持有的其他负债（非流动性负债） Z_other
    E_all::TypeMoney{NDIMS2} # 所有者权益 E_all
    T_all::TypeMoney{NDIMS2} # 总交易流量 Transfer_all：$Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
    Lo_all::TypeMoney{NDIMS2} # 总贷款流出 Lo_all：$Lo_all=Lo_BI_all+Lo_exBI$
    Lo_BI_all::TypeMoney{NDIMS2} # 银行间贷款流出 Lo_BI_all
    Lo_exBI::TypeMoney{NDIMS2} # 非银行间贷款流出 Lo_exBI：$Lo_exBI=Lo_P$
    Lo_P::TypeMoney{NDIMS2} # 银行贷款流出给生产部门 Lo_P
    Li_all::TypeMoney{NDIMS2} # 总贷款流入 Li_all：$Li_all=Li_BI_all+Li_exBI$
    Li_BI_all::TypeMoney{NDIMS2} # 银行间贷款流入 Li_BI_all
    Li_exBI::TypeMoney{NDIMS2} # 非银行间贷款流入 Li_exBI：$Li_exBI=Li_D$
    Li_P::TypeMoney{NDIMS2} # 银行贷款流入从生产部门 Li_P
    Bi_all::TypeMoney{NDIMS2} # 总借款流入 Bi_all：$Bi_all=Bi_BI_all+Bi_exBI$
    Bi_BI_all::TypeMoney{NDIMS2} # 银行间借款流入 Bi_BI_all
    Bi_exBI::TypeMoney{NDIMS2} # 非银行间借款流入 Bi_exBI：$Bi_exBI=Bi_D$
    Bi_D::TypeMoney{NDIMS2} # 银行借款流入从居民部门 Bi_D
    Bo_all::TypeMoney{NDIMS2} # 总借款流出 Bo_all：$Bo_all=Bo_BI_all+Bo_exBI$
    Bo_BI_all::TypeMoney{NDIMS2} # 银行间借款流出 Bo_BI_all
    Bo_exBI::TypeMoney{NDIMS2} # 非银行间借款流出 Bo_exBI：$Bo_exBI=Bo_P$
    Bo_D::TypeMoney{NDIMS2} # 银行借款流出给居民部门 Bo_D
    Shock_t::TypeMoney{NDIMS2} # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
    Shock_s::TypeMoney{NDIMS2} # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
    Shock_def_t::TypeMoney{NDIMS2} # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_P_def_t+Shock_D_run_t$
    Shock_def_s::TypeMoney{NDIMS2} # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
    Shock_run_t::TypeMoney{NDIMS2} # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
    Shock_run_s::TypeMoney{NDIMS2} # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
    Shock_exBI_t::TypeMoney{NDIMS2} # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
    Shock_exBI_s::TypeMoney{NDIMS2} # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
    Shock_P_run_s::TypeMoney{NDIMS2} # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
    Shock_P_def_t::TypeMoney{NDIMS2} # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
    Shock_D_def_s::TypeMoney{NDIMS2} # 银行存款违约损失冲击源头 Shock_D_def_s
    Shock_D_run_t::TypeMoney{NDIMS2} # 银行存款挤兑流动冲击目标 Shock_D_run_t
    Shock_B::TypeMoney{NDIMS2} # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
    Shock_B_A::TypeMoney{NDIMS2} # 银行内资产负债之银行间资产端冲击 Shock_B_A
    Shock_B_Z::TypeMoney{NDIMS2} # 银行内资产负债之银行间负债端冲击 Shock_B_Z
    Shock_BI_s::TypeMoney{NDIMS2} # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
    Shock_BI_t::TypeMoney{NDIMS2} # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
    Shock_BI_def_s::TypeMoney{NDIMS2} # 银行间违约损失冲击源头 Shock_BI_def_s
    Shock_BI_def_t::TypeMoney{NDIMS2} # 银行间违约损失冲击目标 Shock_BI_def_t
    Shock_BI_run_s::TypeMoney{NDIMS2} # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
    Shock_BI_run_t::TypeMoney{NDIMS2} # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
    Shock_BI_run_ilq_s::TypeMoney{NDIMS2} # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
    Shock_BI_run_ilq_t::TypeMoney{NDIMS2} # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
    Shock_BI_run_br_s::TypeMoney{NDIMS2} # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
    Shock_BI_run_br_t::TypeMoney{NDIMS2} # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
    Loss_BI::TypeMoney{NDIMS2} # 银行间市场冲击损失 Loss_BI
    Loss_BI_def_t::TypeMoney{NDIMS2} # 银行间资产负债违约冲击损失 Loss_BI_def_t
    Loss_BI_run_t::TypeMoney{NDIMS2} # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
    on::TypeState{NDIMS2} # 示性向量之于银行是否存在 isOn
    off::TypeState{NDIMS2} # 示性向量之于银行是否已退出不存在 isOff
    hel::TypeState{NDIMS2} # 示性向量之于银行是否健康 isHealthy
    isv::TypeState{NDIMS2} # 示性向量之于银行是否资不抵债 isInsolvent
    ilq::TypeState{NDIMS2} # 示性向量之于银行是否流动性短缺 isIlliquity
    br::TypeState{NDIMS2} # 示性向量之于银行是否破产 isBankrupt
    nBoBI::TypeState{NDIMS2} # 示性向量之于银行是否需要偿还银行间借款 isNeededBoBI
    eBoBI::TypeState{NDIMS2} # 示性向量之于银行是否可以偿还银行间借款 isEnabledBoBI
    nBoD::TypeState{NDIMS2} # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
    eBoD::TypeState{NDIMS2} # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
    nLiP::TypeState{NDIMS2} # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
    eLiP::TypeState{NDIMS2} # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP
    isAllocatedShock::TypeState{NDIMS2} # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
    listOfExist::Array{Any} # 列表之于存在的银行编号 listOfExist
    listOfInsolvent::Array{Any} # 列表之于资不抵债的银行编号 listOfInsolvent
    listOfIlliquity::Array{Any} # 列表之于流动性短缺的银行编号 listOfIlliquity
    listOfBankrupt::Array{Any} # 列表之于破产的银行编号 listOfBankrupt
end
# isDefault::TypeState{NDIMS2} # 示性向量之于银行是否违约
# TODO 补充损失变量；
# TODO 增加监管约束之状态；



"定义银行间邻接矩阵复合类型。"
mutable struct BankInterbank{NDIMS2}
    # id::TypeIds{NDIMS2} # 编号
    A_BI::TypeMoney{NDIMS2} # 银行间资产邻接矩阵 A_BI
    Z_BI::TypeMoney{NDIMS2} # 银行间负债邻接矩阵 Z_BI
    Lo_BI::TypeMoney{NDIMS2} # 银行间贷款流出邻接矩阵 Lo_BI
    Li_BI::TypeMoney{NDIMS2} # 银行间贷款流入邻接矩阵 Li_BI
    Bo_BI::TypeMoney{NDIMS2} # 银行间借款流入邻接矩阵 Bo_BI
    Bi_BI::TypeMoney{NDIMS2} # 银行间借款流出邻接矩阵 Bi_BI
    Shock_BI::TypeMoney{NDIMS2} # 银行间冲击 Shock_BI：$Shock_BI=Shock_BI_def+Shock_BI_run$
    Shock_BI_def::TypeMoney{NDIMS2} # 银行间违约损失冲击 Shock_BI_def
    Shock_BI_run::TypeMoney{NDIMS2} # 银行间挤兑流动冲击 Shock_BI_run：$Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
    Shock_BI_run_ilq::TypeMoney{NDIMS2} # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
    Shock_BI_run_br::TypeMoney{NDIMS2} # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
    Loss_BI::TypeMoney{NDIMS2} # 银行间市场冲击损失 Loss_BI
    Loss_BI_def::TypeMoney{NDIMS2} # 银行间资产负债违约冲击损失 Loss_BI_def
    Loss_BI_run::TypeMoney{NDIMS2} # 银行间负债流动性挤兑冲击损失 Loss_BI_run
    # isExposure::TypeState{NDIMS2} # 信息邻接矩阵之于是否有银行间敞口 isExposure
    on::TypeState{NDIMS2} # 信息邻接矩阵之于银行间存在的 isOn
    off::TypeState{NDIMS2} # 信息邻接矩阵之于银行间已退出不存在的 isOff
    hel::TypeState{NDIMS2} # 信息邻接矩阵之于银行间健康的 isHealthy
    isv::TypeState{NDIMS2} # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
    ilq::TypeState{NDIMS2} # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
    br::TypeState{NDIMS2} # 信息邻接矩阵之于银行间破产的 isBankrupt
    cre::Array{Any} # 信息列表之于各银行之债权方银行编号 listOfCreditors
    deb::Array{Any} # 信息列表之于各银行之债务方银行编号 listOfDebtors
    cre_isv::Array{Any} # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
    deb_isv::Array{Any} # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
    cre_ilq::Array{Any} # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
    deb_ilq::Array{Any} # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
    cre_br::Array{Any} # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
    deb_br::Array{Any} # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt
end



