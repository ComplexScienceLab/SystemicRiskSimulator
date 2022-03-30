## 考虑情况：存在部分债务银行之部分债务因为流动性短缺从而无法偿还。

##########################################
#状态/开发
##########################################

"函数：过程之于银行外部挤兑流动冲击"
function process_exBank_illiquity!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    ## 过程：银行外部挤兑流动传染冲击
    env[:processName] = "银行外部挤兑流动传染冲击过程"
    @test println("开始过程：$(env[:processName])：")

    env[:tau] = 0 # 初始化回合
    env[:isRound] = true # 初始化回合状态

    env[:tau] += 1 # 回合累加一
    @test println("开始回合$(env[:tau])")

    b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
    ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

    ## 设置临时变量
    Shock_t_t1 = deepcopy(BB.Shock_t)

    ## # 银行外部挤兑流动冲击阶段
    env[:stageName] = "银行外部挤兑流动冲击阶段"
    # @test println("阶段：$(env[:stageName])")
    @run_stage BB, BI = exBank_illiquity_shock!(BB, BI, b, ib, para)

    ## TODO存储数据
    # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
    # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

    ## 判定是否结束过程
    if BB.Shock_t == Shock_t_t1
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

    return BB, BI, env

end # function
