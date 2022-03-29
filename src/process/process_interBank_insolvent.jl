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

        env[:tau] += 1 # 传染回合累加一
        @test println("开始回合$(env[:tau])")

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## # 资不抵债银行间违约损失传染阶段
        BB, BI = interBank_insolvent_contagion!(BB, BI, BB_t1, BI_t1, b, ib, para)


        ## 设置临时变量
        BB_t1 = deepcopy(BB)
        BI_t1 = deepcopy(BI)


        ## # 资不抵债银行间违约损失冲击阶段
        BB, BI, BB_t1, BI_t1 = interBank_insolvent_shock!(BB, BI, BB_t1, BI_t1, b, ib, para)


        # update_B_state!(BB, BI; to = "bankrupt", from = "insolvent") # 更新各银行之状态到破产

        ## TODO存储数据
        # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        ## 判定本回合是否有银行转移状态，如果无则后续处理然后结束本轮，如果有则继续处理。
        if BB.isv == BB_t1.isv
            env[:isEndProcess] = true
            break
        end

    end # while 过程：违约损失传染冲击

    return BB, BI, BB_t1, BI_t1, env

end # function


