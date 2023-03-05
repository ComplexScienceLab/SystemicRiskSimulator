

## 模块之银行间市场IB1111

##########################################
#状态/废弃
##########################################

# module model_IB1111

def model_IB1111(self, BB:BankCommercial, IB:BankInterbank, para:dict, env:dict):

    env['index_process'] = 0 # 初始化过程所在位置
    env['state_of_schedule'] = StateOfScheduleEnum.initializing
    # @testprintln "切换调度状态为$(env['state_of_schedule'])"

    env['tau'] = 0 # 初始化回合

    if (!env['is_model']):
        if (env['tau'] > 0):
            # @testprintln "继续模型model：\n"
        else:
            # @testprintln "开始模型model：\n"
            pass
        pass


    ## 过程：外部资产违约损失传染冲击 #BUG测试宏和函数正确性
    env['process_name'] = "外部资产违约损失传染冲击过程"
    #= @scheduler_process  =#BB, IB, env = processEntity_ExBankInsolvent(BB, IB, paras, env)

    ## 过程：资不抵债银行间违约损失传染冲击
    env['process_name'] = "资不抵债银行间违约损失传染冲击过程"
    #= @scheduler_process  =#BB, IB, env = processEntity_InterBankInsolvent(BB, IB, paras, env)

    ## 过程：外部挤兑流动传染冲击
    env['process_name'] = "银行存款挤兑流动传染冲击过程"
    #= @scheduler_process  =#BB, IB, env = processEntity_ExBankIlliquid(BB, IB, paras, env)

    ## 过程：流动性短缺银行间挤兑流动传染
    env['process_name'] = "流动性短缺银行间挤兑流动传染过程"
    #= @scheduler_process  =#BB, IB, env = processEntity_InterBankIlliquid(BB, IB, paras, env)

    ## 过程：外生破产银行间挤兑流动传染冲击 #HACK暂时不用
    # env['process_name'] = "外生破产银行间挤兑流动传染冲击过程"
    # @execute_branch_node BB, IB, env = process_exBank_bankrupt(BB, IB, paras, env)

    ## 过程：破产银行间挤兑流动传染冲击
    env['process_name'] = "破产银行间挤兑流动传染冲击过程"
    #= @scheduler_process  =#BB, IB, env = processEntity_InterBankBankrupt(BB, IB, paras, env)


    # update_B_balance_sheet(BB, IB,b,ib; by_way = 'calc all E_all') # 更新计算各银行之所有者权益
    # A_data.BB[env['tau']] = deepcopy(BB) # 存储该回合传染结果数据
    # A_data.IB[env['tau']] = deepcopy(IB) # 存储该回合传染结果数据
    #TODO 最终破产清算

    ## 判断是否结束
    if !env['is_step']:
        # @testprintln "步进已结束，跳出model_IB1111。"
        pass

    if env['state_of_schedule'] == StateOfScheduleEnum.idle:
        env['is_model'] = False
        env['is_experiment'] = False
        pass

    if (!env['is_model'] | !env['is_experiment']):
        # @testprintln "model_IB1111结束。"
        pass


    return BB, IB, para, env
    # return BB, IB, A_data.BB, A_data.IB, paras, env
    pass  # method

#     pass # module




