"函数：通用过程框架"

## 函数：通用过程框架

##########################################
#状态/开发
##########################################

"""
通用过程框架：
Argument: 
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
"""
function fun_process_skeleton!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict)
    ## 过程：资不抵债银行间违约损失传染冲击
    env[:processName] = "资不抵债银行间违约损失传染冲击过程"
    @test println("开始过程：$(env[:processName])：")

    env[:indexStage] = 0 # 初始化阶段所在位置
    env[:isLoop] = true # 初始化循环状态
    env[:isRound] = true # 初始化回合状态
    env[:isProcess] = true # 初始化过程状态
    while env[:isLoop] == true

        env[:tau] += 1 # 回合累加一
        @test println("开始回合$(env[:tau])")

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(BB.Shock_t)
        BB_isv_t1 = deepcopy(BB.isv)

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ##NOW 运行每一个阶段
        for (j,s) in eval(Meta.parse(enumerate(env[:processName] * ".listStage")))
            env[:indexStage] = j
            env[:stageName] = Symbol(s)
            expr = "BB, BI = " * String(s) * "!(BB, BI, b, ib, para)"
            @scheduler_stage Meta.parse(expr)
        end

        # ## 判断是否结束
        # if !env[:isStep]
        #     @test println("步进已结束，跳出$(env[:modelName])。")
        # end

        # if env[:stateOfSchedule] == :standing
        #     env[:isModel] = false
        #     env[:isExperiment] = false
        # end

        # if (!env[:isModel] || !env[:isExperiment])
        #     @test println("$(env[:modelName])结束。")
        # end

        # ## 设置临时变量
        # BB_t1 = deepcopy(BB)
        # BI_t1 = deepcopy(BI)

        ## TODO存储数据
        # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        if BB.isv == BB_isv_t1 # 判定是否结束过程
            env[:isProcess] = false
        end
        isRound!(env) # 判断是否结束回合
        isLoop!(env) # 判断是否结束循环
        isJumpOutModel!(env) # 判断是否跳出本次过程

    end # while

    return BB, BI, env

end # function









