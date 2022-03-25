## 函数：过程之于外部违约损失传染冲击

##########################################
#状态/维护
##########################################

"函数：过程之于外部违约损失传染冲击"
function process_exBank_insolvent!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    # if para["theta_Shock_exBI_t"] == 1.0 #HACK无用

    ## 过程：银行外部违约损失传染冲击
    env[:process_name] = "银行外部违约损失传染冲击"
    println("过程：", env[:process_name])

    ## # 初始阶段
    println("t0 初始阶段")

    env[:tau] = 0 # 初始化传染回合
    env[:is_end_round] = false # 初始化结束判断

    env[:tau] += 1 # 传染回合累加一
    println("开始回合", env[:tau])

    b = TypeState{1}(BB.on .| BB.off) # 临时设置BB示性变量
    ib = TypeState{2}((BB.on .| BB.off) .& (BB.on .| BB.off)') # 临时设置BI示性变量

    ## # 银行外部违约损失传染阶段
    println("t1 银行外部违约损失传染阶段")
    BB, BI = exBank_insolvent_contagion!(BB, BI, b, ib, para)


    ## 设置临时变量
    BB_t1 = deepcopy(BB)
    BI_t1 = deepcopy(BI)

    
    ## # 银行外部违约损失冲击阶段
    println("t2 银行外部违约损失冲击阶段")
    BB, BI, BB_t1, BI_t1 = exBank_insolvent_shock!(BB, BI, BB_t1, BI_t1, b, ib, para)


    ## # 尾声阶段
    println("t3 尾声阶段")

    ## TODO存储数据
    BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
    BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

    ## 判定本回合是否有银行转移状态，如果无则后续处理然后结束本轮，如果有则继续处理。
    if BB.isv == BB_t1.isv
        env[:is_end_round] = true
    end

    return BB, BI, BB_t1, BI_t1, env


end # function
