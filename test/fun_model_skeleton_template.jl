"函数：通用模型框架"

## 函数：通用模型框架

##########################################
#状态/暂缓开发
##########################################

"""
通用模型框架：
Argument: 
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
"""
function fun_model_skeleton!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict) # 此处需要修改函数名称为实际待生成函数模型名称

    env[:index_process] = 0 # 初始化过程所在位置
    # env[:state_of_schedule] = :stepping
    # @testprintln "切换调度运作状态为$(env[:state_of_schedule])"

    env[:tau] = 0 # 初始化回合

    if (env[:is_model])
        if (env[:tau] > 0)
            @testprintln "继续模型model：\n"
        else
            @testprintln "开始模型model：\n"
        end
    end

    ## 过程

    #=【插入表达式】=#

    ## 判断是否结束
    if !env[:is_step]
        @testprintln "步进已结束，跳出$(env[:model_name])。"
    end

    if env[:state_of_schedule] == :idle
        env[:is_model] = false
        env[:is_experiment] = false
    end

    if (!env[:is_model] || !env[:is_experiment])
        @testprintln "$(env[:model_name])结束。"
    end


    # return BB, BI, para, env
    # return BB, BI, BB_tau, BI_tau, para, env
end # function

# end # module






