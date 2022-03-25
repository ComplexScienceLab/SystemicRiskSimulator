##########################################
#状态/暂停开发
##########################################

"函数：过程之于外生破产银行间挤兑流动传染冲击"#HACK暂时不用
function process_exBank_bankrupt!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    if BB_t0.br != FALSE1 # 当最初存在已经判定倒闭的银行时执行以下过程

        ## 过程：外生破产银行间挤兑流动传染冲击 #TODO增加参数，判断是否增加外生冲击。 #HACK这个过程可以暂时不使用。
        env[:process_name] = "外生破产银行间挤兑流动传染冲击"
        println("过程：", env[:process_name])

        env[:tau] = 0 # 初始化传染回合
        env[:is_end_round] = false # 初始化结束判断

        env[:tau] += 1 # 传染回合累加一
        println("开始回合", env[:tau])

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## 设置临时变量
        Shock_t_t1 = deepcopy(BB.Shock_t)

        ## # 外生破产银行间挤兑流动冲击阶段
        println("t1 外生破产银行间挤兑流动冲击阶段")
        BB, BI = exBank_bankrupt_shock!(BB, BI, b, ib, para)

        ## TODO存储数据
        BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        ## 判定本回合是否有银行转移状态，如果无则后续处理然后结束本轮，如果有则继续处理。
        if BB.Shock_t == Shock_t_t1
            env[:is_end_round] = true
        end

        return BB, BI, env
    end # if


end # function