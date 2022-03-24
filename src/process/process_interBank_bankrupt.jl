##########################################
#状态/测试
##########################################


"函数：过程之于破产银行间挤兑流动传染冲击"
function process_interBank_bankrupt!(BB::BankCommercial, BI::BankInterbank, para::ParameterVariables, env::EnvironmentVariables)

    ## 过程：破产银行间挤兑流动传染冲击 #BUG
    env.process_name = "破产银行间挤兑流动传染冲击"
    println("过程：", env.process_name)

    env.is_end_round = false # 初始化结束判断

    while (env.tau <= env.max_num_tau .&& env.is_end_round != true)

        env.tau += 1 # 传染回合累加一
        println("开始回合", env.tau)

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## 设置临时变量
        Shock_t_t1 = deepcopy(BB.Shock_t)

        ## # 破产银行间挤兑流动传染冲击阶段
        println("t1 破产银行间挤兑流动传染冲击阶段")
        BB, BI = interBank_bankrupt_contagion_shock!(BB, BI, b, ib, para)

        ## # 破产银行间挤兑流动分配借贷流量阶段
        println("t2 破产银行间挤兑流动分配借贷流量阶段")
        BB, BI = interBank_illiquity_allocate!(BB, BI, b, ib, para)

        ## # 破产银行间挤兑流动执行借贷流量阶段
        println("t3 破产银行间挤兑流动执行借贷流量阶段")
        BB, BI = interBank_illiquity_repay!(BB, BI, b, ib, para)

        ## TODO存储数据
        BB_tau[env.tau] = deepcopy(BB) # 存储该回合传染结果数据
        BI_tau[env.tau] = deepcopy(BI) # 存储该回合传染结果数据

        ## 判定本回合是否有借贷流量，如果无则后续处理然后结束本轮，如果有则继续处理。
        if BB.Shock_t == Shock_t_t1
            env.is_end_round = true
            break
        end


    end # while

    return BB, BI, env
end # if
