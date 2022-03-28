## 考虑情况：存在部分债务银行之部分债务因为流动性短缺从而无法偿还。

##########################################
#状态/开发
##########################################

"函数：过程之于银行外部挤兑流动冲击"
function process_exBank_illiquity!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    ## 过程：银行外部挤兑流动传染冲击
    env[:processName] = "银行外部挤兑流动传染冲击"
    @test println("过程：$(env[:processName])")

    env[:tau] = 0 # 初始化传染回合
    env[:isEndRound] = false # 初始化结束判断

    env[:tau] += 1 # 传染回合累加一
    @test println("开始回合$(env[:tau])")

    b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
    ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

    ## 设置临时变量
    Shock_t_t1 = deepcopy(BB.Shock_t)

    ## # 银行外部挤兑流动冲击阶段
    BB, BI = exBank_illiquity_shock!(BB, BI, b, ib, para)

    ## TODO存储数据
    # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
    # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

    ## 判定本回合是否有银行转移状态，如果无则后续处理然后结束本轮，如果有则继续处理。
    if BB.Shock_t == Shock_t_t1
        env[:isEndRound] = true
    end

    return BB, BI, env

end # function
