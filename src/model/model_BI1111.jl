

## 模块之银行间市场BI1111

##########################################
#状态/开发
##########################################

# module model_BI1111

function model_BI1111(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    ## 设置临时变量
    BB_t0 = deepcopy(BB) # 临时设置BB变量，被读取于阶段1
    BI_t0 = deepcopy(BI) # 临时设置BI变量，被读取于阶段1


    ## 过程：外部违约损失传染冲击
    BB, BI, BB_t1, BI_t1, env = process_exBank_insolvent!(BB, BI, para, env)

    ## 过程：资不抵债银行间违约损失传染冲击
    BB, BI, BB_t1, BI_t1, env = process_interBank_insolvent!(BB, BI, BB_t1, BI_t1, para, env)

    ## 过程：外部挤兑流动传染冲击
    BB, BI, env = process_exBank_illiquity!(BB, BI, para, env)

    ## 过程：流动性短缺银行间挤兑流动传染冲击
    BB, BI, env = process_interBank_illiquity!(BB, BI, para, env)

    ## 过程：外生破产银行间挤兑流动传染冲击 #HACK暂时不用
    # BB, BI, env = process_exBank_bankrupt!(BB, BI,para,env)

    ## 过程：破产银行间挤兑流动传染冲击
    BB, BI, env = process_interBank_bankrupt!(BB, BI, para, env)


    ## 传染过程结束
    @test println("传染过程结束")
    ## 收尾
    # update_B_balanceSheet!(BB, BI,b,ib; byWay = "calc all E_all") # 更新计算各银行之所有者权益
    # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
    # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据
    #TODO 最终破产清算


    @test println("model_BI1111结束。")

    return BB, BI, para, env
    # return BB, BI, BB_tau, BI_tau, para, env
end # function

# end # module




