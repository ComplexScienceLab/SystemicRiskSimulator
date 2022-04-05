

## 模块之银行间市场BI1111

##########################################
#状态/开发
##########################################

# module model_BI1111

function model_BI1111!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    env[:indexProcess] = 0 # 初始化过程所在位置
    env[:stateOfSchedule] = :indexing
    @test println("切换调度运作状态为indexing")

    env[:tau] = 0 # 初始化回合

    if (!env[:isModel])
        if (env[:tau] > 0)
            @test println("继续模型model：\n")
        else
            @test println("开始模型model：\n")
        end
    end

    for state in [:indexing, :stepping]
        env[:stateOfSchedule] = state

        ## 过程：银行外部违约损失传染冲击 #BUG测试宏和函数正确性
        env[:processName] = "银行外部违约损失传染冲击过程"
        @scheduler_process BB, BI, env = process_exBank_insolvent!(BB, BI, para, env)

        ## 过程：资不抵债银行间违约损失传染冲击
        env[:processName] = "资不抵债银行间违约损失传染冲击过程"
        @scheduler_process BB, BI, env = process_interBank_insolvent!(BB, BI, para, env)

        ## 过程：外部挤兑流动传染冲击
        env[:processName] = "银行外部挤兑流动传染冲击过程"
        @scheduler_process BB, BI, env = process_exBank_illiquity!(BB, BI, para, env)

        ## 过程：流动性短缺银行间挤兑流动传染冲击
        env[:processName] = "流动性短缺银行间挤兑流动传染冲击过程"
        @scheduler_process BB, BI, env = process_interBank_illiquity!(BB, BI, para, env)

        ## 过程：外生破产银行间挤兑流动传染冲击 #HACK暂时不用
        # env[:processName] = "外生破产银行间挤兑流动传染冲击过程"
        # @run_process BB, BI, env = process_exBank_bankrupt!(BB, BI, para, env)

        ## 过程：破产银行间挤兑流动传染冲击
        env[:processName] = "破产银行间挤兑流动传染冲击过程"
        @scheduler_process BB, BI, env = process_interBank_bankrupt!(BB, BI, para, env)


        # update_B_balanceSheet!(BB, BI,b,ib; byWay = "calc all E_all") # 更新计算各银行之所有者权益
        # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据
        #TODO 最终破产清算

        ## 判断是否结束
        if !env[:isStep]
            @test println("步进已结束，跳出model_BI1111。")
        end

        if env[:stateOfSchedule] == :standing
            env[:isModel] = false
            env[:isExperiment] = false
        end

        if (!env[:isModel] || !env[:isExperiment])
            @test println("model_BI1111结束。")
        end

    end # for

    return BB, BI, para, env
    # return BB, BI, BB_tau, BI_tau, para, env
end # function

# end # module




