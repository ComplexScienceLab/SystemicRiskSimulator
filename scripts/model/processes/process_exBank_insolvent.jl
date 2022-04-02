## 函数：过程之于外部违约损失传染冲击

##########################################
#状态/维护
##########################################

"函数：过程之于外部违约损失传染冲击"
function process_exBank_insolvent!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)


    ## 过程：银行外部违约损失传染冲击
    env[:processName] = "银行外部违约损失传染冲击过程"
    @test println("开始过程：$(env[:processName])：")

    env[:indexStage] = 0 # 初始化阶段所在位置
    env[:isLoop] = true # 初始化循环状态
    env[:isRound] = true # 初始化回合状态
    env[:isProcess] = true # 初始化过程状态

    env[:tau] += 1 # 回合累加一
    @test println("开始回合$(env[:tau])")

    b = TypeState{1}(BB.on .| BB.off) # 临时设置BB示性变量
    ib = TypeState{2}((BB.on .| BB.off) .& (BB.on .| BB.off)') # 临时设置BI示性变量

    ## 设置临时变量
    BB_Shock_t_t1 = deepcopy(BB.Shock_t)
    BB_isv_t1 = deepcopy(BB.isv)

    ## # 银行外部违约损失冲击阶段
    env[:stageName] = "银行外部违约损失冲击阶段"
    # @test println("阶段：$(env[:stageName])")
    push!(env[:indexOfSchedulePosition])
    @scheduler_stage BB, BI = exBank_insolvent_shock!(BB, BI, b, ib, para)

    # ## # 资不抵债银行间违约损失传染阶段
    env[:stageName] = "资不抵债银行间违约损失传染阶段"
    # @test println("阶段：$(env[:stageName])")
    @scheduler_stage BB, BI = interBank_insolvent_contagion!(BB, BI, b, ib, para)

    # ## 设置临时变量
    # BB_t1 = deepcopy(BB)
    # BI_t1 = deepcopy(BI)


    ## TODO存储数据
    # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
    # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据


    if BB.isv == BB_isv_t1 # 判定是否结束过程
        env[:isProcess] = false
    end
    isRound!(env) # 判断是否结束回合
    isLoop!(env) # 判断是否结束循环
    isJumpOutModel!(env) # 判断是否跳出本次过程


    return BB, BI, env


end # function
