## 假设所有流动性短缺或者破产银行都能收回其债务银行之所有资金。

##########################################
#状态/备用
##########################################

"函数：过程之于流动性短缺银行间挤兑流动传染冲击"
function process_interBank_illiquity!(BB::BankCommercial, BI::BankInterbank, BB_t1::BankCommercial, BI_t1::BankInterbank, para::Dict, env::EnvironmentVariables)

    ## 过程：流动性短缺银行间挤兑流动传染冲击
    env[:process_name] = "流动性短缺银行间挤兑流动传染冲击"
    println("过程：", env[:process_name])

    while (env[:tau] <= env[:max_num_tau] .&& env[:is_end_round] != true)

        env[:tau] += 1 # 传染回合累加一
        println("开始回合", env[:tau])

        ## 初始阶段$t_{0}$，当$\env[:tau]>1$时：
        println("t0 初始阶段")

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## # 流动性短缺银行间挤兑流动传染阶段
        println("t1 流动性短缺银行间挤兑流动传染阶段")
        BB, BI, BB_t1, BI_t1 = interBank_illiquity_contagion!(BB, BI, BB_t1, BI_t1, para)

        ## 设置临时变量
        BB_t1 = deepcopy(BB)
        BI_t1 = deepcopy(BI)

        ## # 流动性短缺银行间挤兑流动冲击阶段
        println("t2 流动性短缺银行间挤兑流动冲击阶段")
        BB, BI, BB_t1, BI_t1 = interBank_illiquity_shock!(BB, BI, BB_t1, BI_t1, para)

        ## # 尾声阶段$t_{4}$：
        println("t4 开始尾声阶段")

        # update_B_state!(BB, BI; to = "bankrupt", from = "illiquity") # 更新各银行之状态到破产

        ## TODO存储数据
        BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        ## 清零银行内冲击变量
        update_B_Shock!(BB, BI, b, ib; byWay = "clear Shock_B_A and Shock_B_Z") # 清零银行内资产负债冲击

        ## 判定本回合是否有银行转移状态，如果无则后续处理然后结束本轮，如果有则继续处理。
        if BB.ilq == BB_t1.ilq
            env[:is_end_round] = true
            break
        end


    end # while # 过程：流动性短缺银行间挤兑流动传染冲击


    return BB, BI, BB_t1, BI_t1, env


end # function




