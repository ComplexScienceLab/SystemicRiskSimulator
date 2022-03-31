##########################################
#状态/测试
##########################################


"函数：过程之于破产银行间挤兑流动传染冲击"
function process_interBank_bankrupt!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)

    ## 过程：破产银行间挤兑流动传染冲击 #BUG
    env[:processName] = "破产银行间挤兑流动传染冲击过程"
    @test println("开始过程：$(env[:processName])：")

    env[:isLoop] = true # 初始化循环状态
    env[:isRound] = true # 初始化回合状态
    env[:isProcess] = true # 初始化过程状态
    while env[:isLoop] == true

        env[:tau] += 1 # 回合累加一
        @test println("开始回合$(env[:tau])")

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(BB.Shock_t)

        ## # 破产银行间挤兑流动传染冲击阶段
        env[:stageName] = "破产银行间挤兑流动传染冲击阶段"
        # @test println("阶段：$(env[:stageName])")
        @scheduler_stage BB, BI = interBank_bankrupt_contagion_shock!(BB, BI, b, ib, para)

        ## # 破产银行间挤兑流动分配借贷流量阶段
        env[:stageName] = "银行间挤兑流动分配借贷流量阶段"
        # @test println("阶段：$(env[:stageName])")
        @scheduler_stage BB, BI = interBank_illiquity_allocate!(BB, BI, b, ib, para)

        ## # 破产银行间挤兑流动执行借贷流量阶段
        env[:stageName] = "银行间挤兑流动执行借贷流量阶段"
        # @test println("阶段：$(env[:stageName])")
        @scheduler_stage BB, BI = interBank_illiquity_repay!(BB, BI, b, ib, para)

        ## TODO存储数据
        # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        ## 判定是否结束过程 #FIXME
        if BB.Shock_t == BB_Shock_t_t1
            env[:isProcess] = false
            @test println("env[:isProcess]=$(env[:isProcess])")
        end

        isEndLoop!(env) # 判断是否结束循环
        isJumpOutProcess!(env) # 判断是否跳出过程    

    end # while

    return BB, BI, env
end # if
