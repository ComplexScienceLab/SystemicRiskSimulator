"功能函数：过程之于资不抵债银行间违约损失传染冲击"

##########################################
#状态/维护
##########################################

"函数：过程之于资不抵债银行间违约损失传染冲击"
function process_interBank_insolvent!(BB::BankCommercial, BI::BankInterbank, BB_t1::BankCommercial, BI_t1::BankInterbank, para::Dict, env::Dict)
    ## 过程：资不抵债银行间违约损失传染冲击
    env[:processName] = "资不抵债银行间违约损失传染冲击"
    @test println("过程：$(env[:processName])")

    while (env[:isEndRound] != true .&& env[:isEndProcess] != true)

        env[:tau] += 1 # 回合累加一
        @test println("开始回合$(env[:tau])")

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## # 资不抵债银行间违约损失传染阶段
        # env[:stageName] = "t1 资不抵债银行间违约损失传染阶段"
        # @test println("阶段：$(env[:stageName])")
        # @run_stage("BB, BI = interBank_insolvent_contagion!(BB, BI, BB_t1, BI_t1, b, ib, para)") #HACK 暂时用不了
        if env[:stageName] == env[:savedStageName]
            BB, BI = interBank_insolvent_contagion!(BB, BI, BB_t1, BI_t1, b, ib, para)
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                env[:isEndStep] = true
                # break
            end
        end


        ## 设置临时变量
        BB_t1 = deepcopy(BB)
        BI_t1 = deepcopy(BI)


        ## # 资不抵债银行间违约损失冲击阶段
        # env[:stageName] = "t2 资不抵债银行间违约损失冲击阶段"
        # @test println("阶段：$(env[:stageName])")
        # @run_stage("BB, BI, BB_t1, BI_t1 = interBank_insolvent_shock!(BB, BI, BB_t1, BI_t1, b, ib, para)") #HACK 暂时用不了
        if env[:stageName] == env[:savedStageName]
            BB, BI, BB_t1, BI_t1 = interBank_insolvent_shock!(BB, BI, BB_t1, BI_t1, b, ib, para)
            env[:step] += 1
            if env[:step] % env[:stepSize] == 0
                env[:savedProcessName] = env[:processName]
                env[:savedStageName] = env[:stageName]
                env[:isEndStep] = true
                # break
            end
        end


        # update_B_state!(BB, BI; to = "bankrupt", from = "insolvent") # 更新各银行之状态到破产

        ## TODO存储数据
        # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        ## 判定是否结束循环
        if BB.isv == BB_t1.isv
            env[:isEndProcess] = true
        end
        if (env[:isEndStep] .&& env[:isEndProcess])
            env[:isEndRound] = true
        end

    end # while 过程：违约损失传染冲击

    return BB, BI, BB_t1, BI_t1, env

end # function


