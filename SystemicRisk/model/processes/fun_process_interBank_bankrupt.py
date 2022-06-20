##########################################
#状态/测试
##########################################


"函数：过程之于破产银行间挤兑流动传染冲击"
def process_interBank_bankrupt(self, BB:BankCommercial, BI:BankInterbank, para:dict, env:dict):

    ## 过程：破产银行间挤兑流动传染冲击 #BUG
    # env['process_name'] = "破产银行间挤兑流动传染冲击过程"
    # @testprintln "开始过程：$(env['process_name'])："

    env['index_stage'] = 0 # 初始化阶段所在位置
    env['is_loop'] = True # 初始化循环状态
    env['is_round'] = True # 初始化回合状态
    env['is_rocess'] = True # 初始化过程状态
    while env['is_loop'] == True:

        env['tau'] += 1 # 回合累加一
        # @testprintln "开始回合$(env['tau'])"

        b = TypeState{1}(BB.on | BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on | BB.off) & (BB.on | BB.off)') # 临时设置BI示性变量

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(BB.Shock_t)

        ## # 破产银行间挤兑流动传染冲击阶段
        # env['stage_name'] = "破产银行间挤兑流动传染冲击阶段"
        # # @testprintln "阶段：$(env['stage_name'])"
        #= @scheduler_stage  =#BB, BI = stage_interBank_bankrupt_contagion_shock(BB, BI, b, ib, para, env)

        ## # 破产银行间挤兑流动分配借贷流量阶段
        # env['stage_name'] = "银行间挤兑流动分配借贷流量阶段"
        # # @testprintln "阶段：$(env['stage_name'])"
        #= @scheduler_stage  =#BB, BI = stage_interBank_illiquity_allocate(BB, BI, b, ib, para, env)

        ## # 破产银行间挤兑流动执行借贷流量阶段
        # env['stage_name'] = "银行间挤兑流动执行借贷流量阶段"
        # # @testprintln "阶段：$(env['stage_name'])"
        #= @scheduler_stage  =#BB, BI = stage_interBank_illiquity_repay(BB, BI, b, ib, para, env)

        ## TODO存储数据
        # A_data.BB[env['tau']] = deepcopy(BB) # 存储该回合传染结果数据
        # A_data.BI[env['tau']] = deepcopy(BI) # 存储该回合传染结果数据

        if BB.Shock_t == BB_Shock_t_t1: # 判定是否结束过程: #FIXME
            env['is_rocess'] = False
            pass
        is_round() # 判断是否结束回合
        is_loop() # 判断是否结束循环
        is_step() # 判断是否跳出本次过程
    

        pass # while
    
    # @testprintln "结束过程：$(env['process_name'])。"

    return BB, BI, para, env
    pass # if
