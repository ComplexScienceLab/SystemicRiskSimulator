##########################################
#状态/测试
##########################################


"函数：过程之于破产银行间挤兑流动传染冲击"
function process_interBank_bankrupt!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    ## 过程：破产银行间挤兑流动传染冲击 #BUG
    env[:processName] = "破产银行间挤兑流动传染冲击过程"
    @test println("开始过程：$(env[:processName])：")

    env[:isRound] = true # 初始化回合状态
    while env[:isRound] == true

        env[:tau] += 1 # 回合累加一
        @test println("开始回合$(env[:tau])")

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## 设置临时变量
        Shock_t_t1 = deepcopy(BB.Shock_t)

        ## # 破产银行间挤兑流动传染冲击阶段
        # env[:stageName] = "破产银行间挤兑流动传染冲击阶段"
        # @test println("阶段：$(env[:stageName])")
        # @run_stage("BB, BI = interBank_bankrupt_contagion_shock!(BB, BI, b, ib, para)") #HACK 暂时用不了
        if (env[:stateOfStageStep] == :stepping && env[:stageName] == env[:savedStageName])
            BB, BI = interBank_bankrupt_contagion_shock!(BB, BI, b, ib, para)
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0 # 是否完成本次步进
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                # break
            end
        end

        ## # 破产银行间挤兑流动分配借贷流量阶段
        # env[:stageName] = "银行间挤兑流动分配借贷流量阶段"
        # @test println("阶段：$(env[:stageName])")
        # @run_stage("BB, BI = interBank_illiquity_allocate!(BB, BI, b, ib, para)") #HACK 暂时用不了
        if (env[:stateOfStageStep] == :stepping && env[:stageName] == env[:savedStageName])
            BB, BI = interBank_illiquity_allocate!(BB, BI, b, ib, para)
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0 # 是否完成本次步进
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                # break
            end
        end

        ## # 破产银行间挤兑流动执行借贷流量阶段
        # env[:stageName] = "银行间挤兑流动执行借贷流量阶段"
        # @test println("阶段：$(env[:stageName])")
        # @run_stage("BB, BI = interBank_illiquity_repay!(BB, BI, b, ib, para)") #HACK 暂时用不了
        if (env[:stateOfStageStep] == :stepping && env[:stageName] == env[:savedStageName])
            BB, BI = interBank_illiquity_repay!(BB, BI, b, ib, para)
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0 # 是否完成本次步进
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                # break
            end
        end

        ## TODO存储数据
        # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        ## 判定是否结束#FIXME
        if BB.Shock_t == Shock_t_t1
            env[:isProcess] = false
        end
        if (env[:stateOfStageStep] != :stepping || !env[:isProcess] || env[:tau] >= env[:maxNumOfTau])
            env[:isRound] = false
            @test println("结束过程：$(env[:processName])。")
        end


    end # while

    return BB, BI, env
end # if
