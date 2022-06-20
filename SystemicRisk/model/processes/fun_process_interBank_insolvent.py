"功能函数：过程之于资不抵债银行间违约损失传染冲击"

##########################################
#状态/维护
##########################################

"函数：过程之于资不抵债银行间违约损失传染冲击"
def process_interBank_insolvent(self, BB:BankCommercial, BI:BankInterbank, para:dict, env:dict):
    ## 过程：资不抵债银行间违约损失传染冲击
    # env['process_name'] = "资不抵债银行间违约损失传染冲击过程"
    # @testprintln "开始过程：$(env['process_name'])："

    env['index_stage'] = 0 # 初始化阶段所在位置
    env['is_loop'] = True # 初始化循环状态
    env['is_round'] = True # 初始化回合状态
    env['is_rocess'] = True # 初始化过程状态
    while env['is_loop'] == True:

        env['tau'] += 1 # 回合累加一
        # @testprintln "开始回合$(env['tau'])"

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(BB.Shock_t)
        BB_isv_t1 = deepcopy(BB.isv)

        b = TypeState{1}(BB.on | BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on | BB.off) & (BB.on | BB.off)') # 临时设置BI示性变量

        ## # 资不抵债银行间违约损失冲击阶段
        # env['stage_name'] = "资不抵债银行间违约损失冲击阶段"
        # # @testprintln "阶段：$(env['stage_name'])"
        #= @scheduler_stage  =#BB, BI = stage_interBank_insolvent_shock(BB, BI, b, ib, para, env)

        ## # 资不抵债银行间违约损失传染阶段
        # env['stage_name'] = "资不抵债银行间违约损失传染阶段"
        # # @testprintln "阶段：$(env['stage_name'])"
        #= @scheduler_stage  =#BB, BI = stage_interBank_insolvent_contagion(BB, BI, b, ib, para, env)


        # ## 设置临时变量
        # BB_t1 = deepcopy(BB)
        # BI_t1 = deepcopy(BI)

        ## TODO存储数据
        # A_data.BB[env['tau']] = deepcopy(BB) # 存储该回合传染结果数据
        # A_data.BI[env['tau']] = deepcopy(BI) # 存储该回合传染结果数据

        if BB.isv == BB_isv_t1: # 判定是否结束过程:
            env['is_rocess'] = False
            pass
        is_round() # 判断是否结束回合
        is_loop() # 判断是否结束循环
        is_step() # 判断是否跳出本次过程
        
        pass # while
    
    # @testprintln "结束过程：$(env['process_name'])。"

    return BB, BI, para, env

    pass # functions


