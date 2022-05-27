## 函数：过程之于外部违约损失传染冲击

##########################################
#状态/维护
##########################################

"函数：过程之于外部违约损失传染冲击"
function process_exBank_insolvent!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)


    ## 过程：银行外部违约损失传染冲击
    # env[:processName] = "银行外部违约损失传染冲击过程"
    @testprintln "开始过程：$(env[:processName])："

    env[:indexStage] = 0 # 初始化阶段所在位置
    env[:isLoop] = true # 初始化循环状态
    env[:isRound] = true # 初始化回合状态
    env[:isProcess] = true # 初始化过程状态

    env[:tau] += 1 # 回合累加一
    @testprintln "开始回合$(env[:tau])"

    b = TypeState{1}(BB.on .| BB.off) # 临时设置BB示性变量
    ib = TypeState{2}((BB.on .| BB.off) .& (BB.on .| BB.off)') # 临时设置BI示性变量

    ## 设置临时变量
    BB_Shock_t_t1 = deepcopy(BB.Shock_t)
    BB_isv_t1 = deepcopy(BB.isv)

    ## # 银行外部违约损失冲击阶段
    # env[:stageName] = "银行外部违约损失冲击阶段"
    # @testprintln "阶段：$(env[:stageName])"
    push!(env[:indexOfSchedulePosition])
    BB, BI = stage_exBank_insolvent_shock!(BB, BI, b, ib, para, env)    #= @scheduler_stage  =#

    # ## # 资不抵债银行间违约损失传染阶段
    # env[:stageName] = "资不抵债银行间违约损失传染阶段"
    # @testprintln "阶段：$(env[:stageName])"
    BB, BI = stage_interBank_insolvent_contagion!(BB, BI, b, ib, para, env)    #= @scheduler_stage  =#

    # ## 设置临时变量
    # BB_t1 = deepcopy(BB)
    # BI_t1 = deepcopy(BI)


    ## TODO存储数据
    # A_data.BB[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
    # A_data.BI[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据


    if BB.isv == BB_isv_t1 # 判定是否结束过程
        env[:isProcess] = false
    end
    isRound!(env) # 判断是否结束回合
    isLoop!(env) # 判断是否结束循环
    isStep!(env) # 判断是否跳出本次过程


    @testprintln "结束过程：$(env[:processName])。"


    return BB, BI, para, env


end # function
