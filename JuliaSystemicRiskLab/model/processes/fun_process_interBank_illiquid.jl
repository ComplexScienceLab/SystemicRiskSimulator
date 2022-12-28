## 考虑情况：存在部分债务银行之部分债务因为流动性短缺从而无法偿还

##########################################
#状态/测试
##########################################

"函数：过程之于流动性短缺银行间挤兑流动传染冲击"
function process_interBank_illiquid!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    ## 过程：流动性短缺银行间挤兑流动传染冲击
    # env[:process_name] = "流动性短缺银行间挤兑流动传染冲击过程"
    @testprintln "开始过程：$(env[:process_name])："

    env[:index_stage] = 0 # 初始化阶段所在位置
    env[:is_loop] = true # 初始化循环状态
    env[:is_round] = true # 初始化回合状态
    env[:is_process] = true # 初始化过程状态
    while env[:is_loop] == true

        env[:tau] += 1 # 回合累加一
        @testprintln "开始回合$(env[:tau])"

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(BB.Shock_t)

        ## # 流动性短缺银行间挤兑流动传染冲击阶段
        BB, BI = stage_interBank_illiquid_contagion_shock!(BB, BI, b, ib, para, env)        #= @scheduler_stage  =#

        ## # 流动性短缺银行间挤兑流动分配借贷流量阶段
        BB, BI = stage_interBank_illiquid_allocate!(BB, BI, b, ib, para, env)        #= @scheduler_stage  =#

        ## # 流动性短缺银行间挤兑流动执行借贷流量阶段
        BB, BI = stage_interBank_illiquid_repay!(BB, BI, b, ib, para, env)        #= @scheduler_stage  =#

        ## TODO存储数据
        # A_data.BB[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # A_data.BI[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        if BB.Shock_t == BB_Shock_t_t1# 判定是否结束过程
            env[:is_process] = false
        end
        is_round!() # 判断是否结束回合
        is_loop!() # 判断是否结束循环
        is_step!() # 判断是否跳出本次过程
        
    end # while
    
    @testprintln "结束过程：$(env[:process_name])。"

    return BB, BI, para, env


end # function




