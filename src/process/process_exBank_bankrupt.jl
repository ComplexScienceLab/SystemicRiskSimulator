##########################################
#状态/暂停开发
##########################################

"函数：过程之于外生破产银行间挤兑流动传染冲击"#HACK暂时不用
function process_exBank_bankrupt!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    if BB_t0.br != FALSE1 # 当最初存在已经判定倒闭的银行时执行以下过程

        ## 过程：外生破产银行间挤兑流动传染冲击 #TODO增加参数，判断是否增加外生冲击。 #HACK这个过程可以暂时不使用。
        env[:processName] = "外生破产银行间挤兑流动传染冲击过程"
        @test println("开始过程：$(env[:processName])：")

        env[:tau] = 0 # 初始化回合
        env[:isRound] = true # 初始化回合状态

        env[:tau] += 1 # 回合累加一
        @test println("开始回合$(env[:tau])")

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## 设置临时变量
        Shock_t_t1 = deepcopy(BB.Shock_t)

        ## # 外生破产银行间挤兑流动冲击阶段
        # @run_stage("BB, BI = exBank_bankrupt_shock!(BB, BI, b, ib, para)") #HACK 暂时用不了
        if (env[:stateOfStageStep] == :stepping && env[:stageName] == env[:savedStageName])
            BB, BI = exBank_bankrupt_shock!(BB, BI, b, ib, para)
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

        return BB, BI, env
    end # if


end # function