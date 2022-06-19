"函数：通用过程框架"

## 函数：通用过程框架

##########################################
#状态/暂缓开发
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
    env[:process_name] = "资不抵债银行间违约损失传染冲击过程"
    @testprintln "开始过程：$(env[:process_name])："

    env[:index_stage] = 0 # 初始化阶段所在位置
    env[:is_loop] = true # 初始化循环状态
    env[:is_round] = true # 初始化回合状态
    env[:is_process] = true # 初始化过程状态
    while env[:is_loop] == true

        env[:tau] += 1 # 回合累加一
        @testprintln "开始回合$(env[:tau])"

        ## 设置临时变量
        BB_Shock_t_t1 = deepcopy(BB.Shock_t)
        BB_isv_t1 = deepcopy(BB.isv)

        b = TypeState{1}(BB.on .|| BB.off) # 临时设置BB示性变量
        ib = TypeState{2}((BB.on .|| BB.off) .&& (BB.on .|| BB.off)') # 临时设置BI示性变量

        ## 运行每一个阶段
        for (j,s) in eval(Meta.parse(enumerate(env[:process_name] * ".listStage")))
            env[:index_stage] = j
            env[:stage_name] = Symbol(s)
            expr = "BB, BI = " * String(s) * "!(BB, BI, b, ib, para)"
            #= @scheduler_stage  =#Meta.parse(expr)
        end

        # ## 判断是否结束
        # if !env[:is_step]
        #     @testprintln "步进已结束，跳出$(env[:model_name])。"
        # end

        # if env[:state_of_schedule] == :idle
        #     env[:is_model] = false
        #     env[:is_experiment] = false
        # end

        # if (!env[:is_model] || !env[:is_experiment])
        #     @testprintln "$(env[:model_name])结束。"
        # end

        # ## 设置临时变量
        # BB_t1 = deepcopy(BB)
        # BI_t1 = deepcopy(BI)

        ## TODO存储数据
        # BB_tau[env[:tau]] = deepcopy(BB) # 存储该回合传染结果数据
        # BI_tau[env[:tau]] = deepcopy(BI) # 存储该回合传染结果数据

        if BB.isv == BB_isv_t1 # 判定是否结束过程
            env[:is_process] = false
        end
        is_round!() # 判断是否结束回合
        is_loop!() # 判断是否结束循环
        isJumpOutModel!() # 判断是否跳出本次过程

    end # while

    return BB, BI, env

end # function









