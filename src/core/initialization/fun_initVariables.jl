"函数区：初始化各类变量"

## 函数区：初始化各类变量

##########################################
#状态/扩展
##########################################

# process InitVariables
# export obj_BI,initObj


"初始化模型变量ModelComponent"
function initModel()
    model = ModelComponent(
        model_BI1111!, # 任意初始化为某个过程
        modelContent_BI1111 # 初始化为某个模型之内容
    )
    return model
end

"仅初始化银行变量"
function init_B_variables_only()
    ## 初始化商业银行实例
    bank = BankCommercial{1,1}(
        collect(range(1, env[:numBank], step=1)), # 编号 id
        fill("", env[:numBank]), # 缩写 abbr
        fill("", env[:numBank]), # 全名 name
        ones(env[:numBank]), # 总资产 A_all: $A_all=A_BI+A_exBI$
        ones(env[:numBank]), # 银行间资产加总 A_BI_all
        ones(env[:numBank]), # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
        ones(env[:numBank]), # 银行贷款给生产部门之资产（非流动性资产） A_P
        ones(env[:numBank]), # 银行持有超额准备金（流动性资产） A_Q
        ones(env[:numBank]), # 银行持有法定准备金（非流动性资产） A_R
        ones(env[:numBank]), # 银行持有的其它资产（非流动性资产） A_other
        ones(env[:numBank]), # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
        ones(env[:numBank]), # 银行间负债加总 Z_BI_all
        ones(env[:numBank]), # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
        ones(env[:numBank]), # 银行获得居民部门存款（非流动性负债） Z_D
        ones(env[:numBank]), # 银行持有的其他负债（非流动性负债） Z_other
        ones(env[:numBank]), # 所有者权益 E_all
        zeros(env[:numBank]), # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
        zeros(env[:numBank]), # 银行间贷款流出 Lo_BI_all
        zeros(env[:numBank]), # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
        zeros(env[:numBank]), # 银行贷款流出给生产部门 Lo_P
        zeros(env[:numBank]), # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
        zeros(env[:numBank]), # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
        zeros(env[:numBank]), # 银行间贷款流入 Li_BI_all
        zeros(env[:numBank]), # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
        zeros(env[:numBank]), # 银行贷款流入从生产部门 Li_P
        zeros(env[:numBank]), # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
        zeros(env[:numBank]), # 银行间借款流入 Bi_BI_all
        zeros(env[:numBank]), # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
        zeros(env[:numBank]), # 银行借款流入从居民部门 Bi_D
        zeros(env[:numBank]), # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
        zeros(env[:numBank]), # 银行间借款流出 Bo_BI_all
        zeros(env[:numBank]), # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
        zeros(env[:numBank]), # 银行借款流出给居民部门 Bo_D
        zeros(env[:numBank]), # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
        zeros(env[:numBank]), # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
        zeros(env[:numBank]), # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exBI_def_t+Shock_BI_def_t$
        zeros(env[:numBank]), # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
        zeros(env[:numBank]), # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
        zeros(env[:numBank]), # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
        zeros(env[:numBank]), # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
        zeros(env[:numBank]), # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
        zeros(env[:numBank]), # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
        zeros(env[:numBank]), # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
        zeros(env[:numBank]), # 银行存款违约损失冲击源头 Shock_D_def_s
        zeros(env[:numBank]), # 银行存款挤兑流动冲击目标 Shock_D_run_t
        zeros(env[:numBank]), # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
        zeros(env[:numBank]), # 银行内资产负债之银行间资产端冲击 Shock_B_A
        zeros(env[:numBank]), # 银行内资产负债之银行间负债端冲击 Shock_B_Z
        zeros(env[:numBank]), # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
        zeros(env[:numBank]), # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
        zeros(env[:numBank]), # 银行间违约损失冲击源头 Shock_BI_def_s
        zeros(env[:numBank]), # 银行间违约损失冲击目标 Shock_BI_def_t
        zeros(env[:numBank]), # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
        zeros(env[:numBank]), # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
        zeros(env[:numBank]), # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
        zeros(env[:numBank]), # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
        zeros(env[:numBank]), # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
        zeros(env[:numBank]), # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
        zeros(env[:numBank]), # 银行间市场冲击损失 Loss_BI
        zeros(env[:numBank]), # 银行间资产负债违约冲击损失 Loss_BI_def_t
        zeros(env[:numBank]), # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
        trues(env[:numBank]), # 示性向量之于银行是否存在 isOn
        falses(env[:numBank]), # 示性向量之于银行是否已退出不存在 isOff
        trues(env[:numBank]), # 示性向量之于银行是否健康 isHealthy
        falses(env[:numBank]), # 示性向量之于银行是否资不抵债 isInsolvent
        falses(env[:numBank]), # 示性向量之于银行是否流动性短缺 isIlliquity
        falses(env[:numBank]), # 示性向量之于银行是否破产 isBankrupt
        falses(env[:numBank]), # 示性向量之于银行是否需要偿还借款 isNeededBoBI
        trues(env[:numBank]), # 示性向量之于银行是否可以偿还借款 isEnabledBoBI
        falses(env[:numBank]), # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
        trues(env[:numBank]), # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
        falses(env[:numBank]), # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
        trues(env[:numBank]), # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP    
        falses(env[:numBank]), # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
        fill(missing, env[:numBank]),  # 列表之于存在的银行编号 listOfExist
        fill(missing, env[:numBank]),  # 列表之于资不抵债的银行编号 listOfInsolvent
        fill(missing, env[:numBank]),  # 列表之于流动性短缺的银行编号 listOfIlliquity
        fill(missing, env[:numBank])  # 列表之于破产的银行编号 listOfBankrupt
    )

    ## 初始化银行间邻接矩阵
    interbank = BankInterbank{2}(
        # reshape(range(1, env[:numBank]^2, step = 1), (env[:numBank], env[:numBank])), # 编号
        zeros(env[:numBank], env[:numBank]), # 银行间资产邻接矩阵 A_BI
        zeros(env[:numBank], env[:numBank]), # 银行间负债邻接矩阵 Z_BI
        zeros(env[:numBank], env[:numBank]), # 银行间贷款流出邻接矩阵 Lo_BI
        zeros(env[:numBank], env[:numBank]), # 银行间贷款流入邻接矩阵 Li_BI
        zeros(env[:numBank], env[:numBank]), # 银行间借款流入邻接矩阵 Bo_BI
        zeros(env[:numBank], env[:numBank]), # 银行间借款流出邻接矩阵 Bi_BI
        zeros(env[:numBank], env[:numBank]), # 银行间冲击 Shock_BI: $Shock_BI=Shock_BI_def+Shock_BI_run$
        zeros(env[:numBank], env[:numBank]), # 银行间违约损失冲击 Shock_BI_def
        zeros(env[:numBank], env[:numBank]), # 银行间挤兑流动冲击 Shock_BI_run: $Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
        zeros(env[:numBank], env[:numBank]), # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
        zeros(env[:numBank], env[:numBank]), # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
        zeros(env[:numBank], env[:numBank]), # 银行间市场冲击损失 Loss_BI
        zeros(env[:numBank], env[:numBank]), # 银行间资产负债违约冲击损失 Loss_BI_def
        zeros(env[:numBank], env[:numBank]), # 银行间负债流动性挤兑冲击损失 Loss_BI_run
        # zeros(env[:numBank], env[:numBank]), # 信息邻接矩阵之于是否有银行间敞口 isExposure
        trues(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间存在的 isOn
        falses(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间已退出不存在的 isOff
        trues(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间健康的 isHealthy
        falses(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
        falses(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
        falses(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间破产的 isBankrupt
        [], # 信息列表之于各银行之债权方银行编号 listOfCreditors
        [], # 信息列表之于各银行之债务方银行编号 listOfDebtors
        [], # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
        [], # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
        [], # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
        [], # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
        [], # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
        [] # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt
    )

    return bank, interbank

end





#TODO"随机化初始化银行变量"
function init_B_variables_randomly()

end


#TODO"导入数据以初始化银行变量"
function init_B_variables_importData()

end

"手动设置以初始化银行变量" #FIXME 须提取手动初始化方式为单独的方式
function initVariables_setManually()
    ## 初始化商业银行群
    bank = BankCommercial{1,1}(
        collect(range(1, env[:numBank], step=1)), # 编号 id
        ["1", "2", "3", "4", "5"], # 缩写 abbr
        ["BK1", "BK2", "BK3", "BK4", "BK5"], # 全名 name
        zeros(env[:numBank]), # 总资产 A_all: $A_all=A_BI+A_exBI$
        [2185.24, 398.37, 730.99, 1357.75, 2717.39], # 银行间资产加总 A_BI_all
        zeros(env[:numBank]), # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
        [1631.73, 4303.24, 3379.72, 4351.47, 620.69], # 银行贷款给生产部门之资产（非流动性资产） A_P
        [477.125, 587.693, 513.847, 713.662, 417.257], # 银行持有超额准备金（流动性资产） A_Q
        zeros(env[:numBank]), # 银行持有法定准备金（非流动性资产） A_R
        zeros(env[:numBank]), # 银行持有的其它资产（非流动性资产） A_other
        zeros(env[:numBank]), # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
        [959.6, 1844.24, 1253.34, 2851.85, 480.71], # 银行间负债加总 Z_BI_all
        zeros(env[:numBank]), # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
        [3160.99, 3231.37, 3184.36, 3311.51, 3122.9], # 银行获得居民部门存款（非流动性负债） Z_D
        zeros(env[:numBank]), # 银行持有的其他负债（非流动性负债） Z_other
        [216.83, 267.13, 233.56, 324.39, 189.66], # 所有者权益 E_all
        zeros(env[:numBank]), # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
        zeros(env[:numBank]), # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
        zeros(env[:numBank]), # 银行间贷款流出 Lo_BI_all
        zeros(env[:numBank]), # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
        zeros(env[:numBank]), # 银行贷款流出给生产部门 Lo_P
        zeros(env[:numBank]), # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
        zeros(env[:numBank]), # 银行间贷款流入 Li_BI_all
        zeros(env[:numBank]), # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
        zeros(env[:numBank]), # 银行贷款流入从生产部门 Li_P
        zeros(env[:numBank]), # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
        zeros(env[:numBank]), # 银行间借款流入 Bi_BI_all
        zeros(env[:numBank]), # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
        zeros(env[:numBank]), # 银行借款流入从居民部门 Bi_D
        zeros(env[:numBank]), # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
        zeros(env[:numBank]), # 银行间借款流出 Bo_BI_all
        zeros(env[:numBank]), # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
        zeros(env[:numBank]), # 银行借款流出给居民部门 Bo_D
        zeros(env[:numBank]), # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
        zeros(env[:numBank]), # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
        zeros(env[:numBank]), # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exBI_def_t+Shock_BI_def_t$
        zeros(env[:numBank]), # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
        zeros(env[:numBank]), # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
        zeros(env[:numBank]), # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
        zeros(env[:numBank]), # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
        zeros(env[:numBank]), # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
        zeros(env[:numBank]), # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
        zeros(env[:numBank]), # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
        zeros(env[:numBank]), # 银行存款违约损失冲击源头 Shock_D_def_s
        zeros(env[:numBank]), # 银行存款挤兑流动冲击目标 Shock_D_run_t
        zeros(env[:numBank]), # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
        zeros(env[:numBank]), # 银行内资产负债之银行间资产端冲击 Shock_B_A
        zeros(env[:numBank]), # 银行内资产负债之银行间负债端冲击 Shock_B_Z
        zeros(env[:numBank]), # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
        zeros(env[:numBank]), # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
        zeros(env[:numBank]), # 银行间违约损失冲击源头 Shock_BI_def_s
        zeros(env[:numBank]), # 银行间违约损失冲击目标 Shock_BI_def_t
        zeros(env[:numBank]), # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
        zeros(env[:numBank]), # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
        zeros(env[:numBank]), # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
        zeros(env[:numBank]), # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
        zeros(env[:numBank]), # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
        zeros(env[:numBank]), # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
        zeros(env[:numBank]), # 银行间市场冲击损失 Loss_BI
        zeros(env[:numBank]), # 银行间资产负债违约冲击损失 Loss_BI_def_t
        zeros(env[:numBank]), # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
        trues(env[:numBank]), # 示性向量之于银行是否存在 isOn
        falses(env[:numBank]), # 示性向量之于银行是否已退出不存在 isOff
        trues(env[:numBank]), # 示性向量之于银行是否健康 isHealthy
        falses(env[:numBank]), # 示性向量之于银行是否资不抵债 isInsolvent
        falses(env[:numBank]), # 示性向量之于银行是否流动性短缺 isIlliquity
        falses(env[:numBank]), # 示性向量之于银行是否破产 isBankrupt
        falses(env[:numBank]), # 示性向量之于银行是否需要偿还借款 isNeededBoBI
        trues(env[:numBank]), # 示性向量之于银行是否可以偿还借款 isEnabledBoBI
        falses(env[:numBank]), # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
        trues(env[:numBank]), # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
        falses(env[:numBank]), # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
        trues(env[:numBank]), # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP    
        falses(env[:numBank]), # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
        fill(missing, env[:numBank]), # 列表之于存在的银行编号 listOfExist
        fill(missing, env[:numBank]), # 列表之于资不抵债的银行编号 listOfInsolvent
        fill(missing, env[:numBank]), # 列表之于流动性短缺的银行编号 listOfIlliquity
        fill(missing, env[:numBank])  # 列表之于破产的银行编号 listOfBankrupt
    )

    ## 初始化银行间邻接矩阵
    interbank = BankInterbank{2}(
        # reshape(range(1, env[:numBank]^2, step = 1), (env[:numBank], env[:numBank])), # 编号
        [0 1728.55 0 134.46 322.23; 109.35 0 289.02 0 0; 730.99 0 0 0 0; 119.26 115.69 964.32 0 158.48; 0 0 0 2717.39 0], # 银行间资产邻接矩阵 A_BI
        [0 1728.55 0 134.46 322.23; 109.35 0 289.02 0 0; 730.99 0 0 0 0; 119.26 115.69 964.32 0 158.48; 0 0 0 2717.39 0]', # 银行间负债邻接矩阵 Z_BI
        zeros(env[:numBank], env[:numBank]), # 银行间贷款流出邻接矩阵 Lo_BI
        zeros(env[:numBank], env[:numBank]), # 银行间贷款流入邻接矩阵 Li_BI
        zeros(env[:numBank], env[:numBank]), # 银行间借款流入邻接矩阵 Bo_BI
        zeros(env[:numBank], env[:numBank]), # 银行间借款流出邻接矩阵 Bi_BI
        zeros(env[:numBank], env[:numBank]), # 银行间冲击 Shock_BI: $Shock_BI=Shock_BI_def+Shock_BI_run$
        zeros(env[:numBank], env[:numBank]), # 银行间违约损失冲击 Shock_BI_def
        zeros(env[:numBank], env[:numBank]), # 银行间挤兑流动冲击 Shock_BI_run: $Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
        zeros(env[:numBank], env[:numBank]), # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
        zeros(env[:numBank], env[:numBank]), # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
        zeros(env[:numBank], env[:numBank]), # 银行间市场冲击损失 Loss_BI
        zeros(env[:numBank], env[:numBank]), # 银行间资产负债违约冲击损失 Loss_BI_def
        zeros(env[:numBank], env[:numBank]), # 银行间负债流动性挤兑冲击损失 Loss_BI_run
        # zeros(env[:numBank], env[:numBank]), # 信息邻接矩阵之于是否有银行间敞口 isExposure
        trues(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间存在的 isOn
        falses(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间已退出不存在的 isOff
        trues(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间健康的 isHealthy
        falses(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
        falses(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
        falses(env[:numBank], env[:numBank]), # 信息邻接矩阵之于银行间破产的 isBankrupt
        [], # 信息列表之于各银行之债权方银行编号 listOfCreditors
        [], # 信息列表之于各银行之债务方银行编号 listOfDebtors
        [], # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
        [], # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
        [], # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
        [], # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
        [], # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
        [] # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt
    )

    return bank, interbank
end


## 不同的方式
"""
初始化银行变量
# Arguments
`init_method::String`:  参数，初始化方式；
- `only init`:  仅单纯初始化；
- `randomly`:  生成随机数据以初始化；
- `import data`:  导入数据以初始化
- `manually`:  手动设置以初始化；
"""
function init_B_and_BI(; init_method::String)
    if init_method == "only init"
        BB, BI = init_B_variables_only()
    elseif init_method == "randomly"
        BB, BI = init_B_variables_randomly()
    elseif init_method == "import data"
        BB, BI = init_B_variables_only()
        BB, BI, A_data.BB, A_data.BI = init_B_variables_importData() # 导入数据以初始化银行变量
    elseif init_method == "set manually"
        BB, BI = initVariables_setManually() # 手动设置以初始化银行变量
    else
        throw(DomainError(init_method, "关键词取值错误！"))
    end

    ## 构建Agent模型
    A = SystemicRiskAgent(
        1, # 编号（必备的）
        BB, # 商业银行群
        BI # 银行间邻接矩阵
    )

    # 初始化带回合变量的商业银行实例数组、初始化带回合变量的银行间市场实例数组
    A_data = initAgentDataCollection(A)

    # A_data.BB = StructArray([BB for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的商业银行实例数组
    # A_data.BI = StructArray([BI for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的银行间市场实例数组

    ## 更新各银行之变量，在第一回合初始时
    b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
    ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量
    update_B_Shock!(BB, BI, b, ib; byWay="all") # 更新各银行之所有冲击变量，在第一回合开始时
    update_B_balanceSheet!(BB, BI, b, ib; byWay="all") # 更新各银行之资产负债表变量
    update_B_state!(BB, BI; to="any", from="any") # 更新各银行之状态示性变量

    ## 存储初始数据
    # A_data.BB_0 = deepcopy(BB)
    # A_data.BI_0 = deepcopy(BI)
    # A_data_0 = deepcopy(A)




    return A, A_data
end




