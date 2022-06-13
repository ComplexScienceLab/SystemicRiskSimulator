## 考虑情况：存在部分债务银行之部分债务因为流动性短缺从而无法偿还

##########################################
#状态/测试
##########################################

"函数：过程之于流动性短缺银行间挤兑流动传染冲击"
def process_interBank_illiquity(BB:BankCommercial, BI:BankInterbank, para:dict, env:dict):

    ## 过程：流动性短缺银行间挤兑流动传染冲击
    # env['processName'] = "流动性短缺银行间挤兑流动传染冲击过程"
    @testprintln "开始过程：$(env['processName'])："

    env['indexStage'] = 0 # 初始化阶段所在位置
    env['isLoop'] = True # 初始化循环状态
    env['isRound'] = True # 初始化回合状态
    env['isProcess'] = True # 初始化过程状态
    while env['isLoop'] == True:

        env['tau'] += 1 # 回合累加一
        @testprintln "开始回合$(env['tau'])"

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(BB.Shock_t)

        ## # 流动性短缺银行间挤兑流动传染冲击阶段
        BB, BI = stage_interBank_illiquity_contagion_shock(BB, BI, b, ib, para, env)        #= @scheduler_stage  =#

        ## # 流动性短缺银行间挤兑流动分配借贷流量阶段
        BB, BI = stage_interBank_illiquity_allocate(BB, BI, b, ib, para, env)        #= @scheduler_stage  =#

        ## # 流动性短缺银行间挤兑流动执行借贷流量阶段
        BB, BI = stage_interBank_illiquity_repay(BB, BI, b, ib, para, env)        #= @scheduler_stage  =#

        ## TODO存储数据
        # A_data.BB[env['tau']] = deepcopy(BB) # 存储该回合传染结果数据
        # A_data.BI[env['tau']] = deepcopy(BI) # 存储该回合传染结果数据

        if BB.Shock_t == BB_Shock_t_t1# 判定是否结束过程
            env['isProcess'] = False
            pass
        isRound() # 判断是否结束回合
        isLoop() # 判断是否结束循环
        isStep() # 判断是否跳出本次过程
        
        pass # while
    
    @testprintln "结束过程：$(env['processName'])。"

    return BB, BI, para, env


    pass # functions




