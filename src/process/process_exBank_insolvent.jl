## 函数：过程之于外部违约损失传染冲击

##########################################
#状态/维护
##########################################

"函数：过程之于外部违约损失传染冲击"
function process_exBank_insolvent!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)


    ## 过程：银行外部违约损失传染冲击
    env[:processName] = "银行外部违约损失传染冲击过程"
    @test println("开始过程：$(env[:processName])：")

    env[:tau] = 0 # 初始化回合
    env[:isRound] = true # 初始化回合状态

    env[:tau] += 1 # 回合累加一
    @test println("开始回合$(env[:tau])")

    b = TypeState{1}(BB.on .| BB.off) # 临时设置BB示性变量
    ib = TypeState{2}((BB.on .| BB.off) .& (BB.on .| BB.off)') # 临时设置BI示性变量

    ## # 银行外部违约损失传染阶段
    env[:stageName] = "银行外部违约损失传染阶段"
    # @test println("阶段：$(env[:stageName])")
    if (env[:stateOfStageStep] == :stepping || (env[:stateOfStageStep] == :loading && env[:stageName] == env[:savedStageName]))
        env[:isStep] = true
        @test println("步进开始：")
        env[:stateOfStageStep] = :stepping # 切换阶段运作状态为步进
        @test println("切换阶段运作状态为stepping")
        BB, BI = exBank_insolvent_contagion!(BB, BI, b, ib, para)
        env[:step] += 1
        if env[:step] % env[:stepSize] == 0 # 是否完成本次步进
            env[:isStep] = false
            @test println("步进结束。")
            env[:stateOfStageStep] = :saving # 切换阶段运作状态为存储
            @test println("切换阶段运作状态为saving")
            env[:stateOfProcessStep] = :saving # 切换过程运作状态为存储
            @test println("切换过程运作状态为saving")
        end
    elseif (env[:stateOfStageStep] == :saving)
        env[:savedStageName] = env[:stageName]
        @test println("下一次步进运行的阶段：$(env[:stageName])。")
        env[:stateOfStageStep] = :collecting # 切换阶段运作状态为收集数据 #TODO 收集数据
        @test println("切换阶段运作状态为collecting")
        env[:stateOfStageStep] = :loading  # 切换阶段运作状态为读取
        @test println("切换阶段运作状态为loading")
        # break
    end
    # @run_stage("BB, BI = exBank_insolvent_contagion!(BB, BI, b, ib, para)") #HACK 暂时用不了


    ## 设置临时变量
    BB_t1 = deepcopy(BB)
    BI_t1 = deepcopy(BI)


    ## # 银行外部违约损失冲击阶段
    env[:stageName] = "银行外部违约损失冲击阶段"
    # @test println("阶段：$(env[:stageName])")
    if (env[:stateOfStageStep] == :stepping || (env[:stateOfStageStep] == :loading && env[:stageName] == env[:savedStageName]))
        env[:isStep] = true
        @test println("步进开始：")
        env[:stateOfStageStep] = :stepping # 切换阶段运作状态为步进
        @test println("切换阶段运作状态为stepping")
        BB, BI, BB_t1, BI_t1 = exBank_insolvent_shock!(BB, BI, BB_t1, BI_t1, b, ib, para)
        env[:step] += 1
        if env[:step] % env[:stepSize] == 0 # 是否完成本次步进
            env[:isStep] = false
            @test println("步进结束。")
            env[:stateOfStageStep] = :saving # 切换阶段运作状态为存储
            @test println("切换阶段运作状态为saving")
            env[:stateOfProcessStep] = :saving # 切换过程运作状态为存储
            @test println("切换过程运作状态为saving")
        end
    elseif (env[:stateOfStageStep] == :saving)
        env[:savedStageName] = env[:stageName]
        @test println("下一次步进运行的阶段：$(env[:stageName])。")
        env[:stateOfStageStep] = :collecting # 切换阶段运作状态为收集数据 #TODO 收集数据
        @test println("切换阶段运作状态为collecting")
        env[:stateOfStageStep] = :loading  # 切换阶段运作状态为读取
        @test println("切换阶段运作状态为loading")
        # break
    end
    # @run_stage("BB, BI, BB_t1, BI_t1 = exBank_insolvent_shock!(BB, BI, BB_t1, BI_t1, b, ib, para)") #HACK 暂时用不了


    ## TODO存储数据
    # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
    # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

    ## 判定是否结束过程
    if BB.isv == BB_t1.isv
        env[:isProcess] = false
    end

    ## 判定是否结束
    if (!env[:isProcess] || env[:tau] >= env[:maxNumOfTau])
        env[:isRound] = false
        @test println("结束过程：$(env[:processName])。")
    end
    if !env[:isStep]
        @test println("跳出过程：$(env[:processName])。")
    end

    return BB, BI, BB_t1, BI_t1, env
    # return BB, BI, env


end # function
