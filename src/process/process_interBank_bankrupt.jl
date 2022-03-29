##########################################
#状态/测试
##########################################


"函数：过程之于破产银行间挤兑流动传染冲击"
function process_interBank_bankrupt!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    ## 过程：破产银行间挤兑流动传染冲击 #BUG
    env[:processName] = "破产银行间挤兑流动传染冲击"
    @test println("过程：$(env[:processName])")

    env[:isEndRound] = false # 初始化结束判断

    while (env[:isEndRound] != true .&& env[:isEndProcess] != true)

        env[:tau] += 1 # 回合累加一
        @test println("开始回合$(env[:tau])")

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## 设置临时变量
        Shock_t_t1 = deepcopy(BB.Shock_t)

        ## # 破产银行间挤兑流动传染冲击阶段
        # env[:stageName] = "t1 破产银行间挤兑流动传染冲击阶段"
        # @test println("阶段：$(env[:stageName])")
        # @run_stage("BB, BI = interBank_bankrupt_contagion_shock!(BB, BI, b, ib, para)") #HACK 暂时用不了
        if env[:stageName] == env[:savedStageName]
            BB, BI = interBank_bankrupt_contagion_shock!(BB, BI, b, ib, para)
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                env[:isEndStep] = true
                # break
            end
        end

        ## # 破产银行间挤兑流动分配借贷流量阶段
        # env[:stageName] = "t2 银行间挤兑流动分配借贷流量阶段"
        # @test println("阶段：$(env[:stageName])")
        # @run_stage("BB, BI = interBank_illiquity_allocate!(BB, BI, b, ib, para)") #HACK 暂时用不了
        if env[:stageName] == env[:savedStageName]
            BB, BI = interBank_illiquity_allocate!(BB, BI, b, ib, para)
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                env[:isEndStep] = true
                # break
            end
        end

        ## # 破产银行间挤兑流动执行借贷流量阶段
        # env[:stageName] = "t3 银行间挤兑流动执行借贷流量阶段"
        # @test println("阶段：$(env[:stageName])")
        # @run_stage("BB, BI = interBank_illiquity_repay!(BB, BI, b, ib, para)") #HACK 暂时用不了
        if env[:stageName] == env[:savedStageName]
            BB, BI = interBank_illiquity_repay!(BB, BI, b, ib, para)
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                env[:isEndStep] = true
                # break
            end
        end

        ## TODO存储数据
        # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        ## 判定是否结束循环#FIXME
        if BB.Shock_t == Shock_t_t1
            env[:isEndProcess] = true
        end
        if (env[:isEndStep] .&& env[:isEndProcess])
            env[:isEndRound] = true
        end


    end # while

    return BB, BI, env
end # if
