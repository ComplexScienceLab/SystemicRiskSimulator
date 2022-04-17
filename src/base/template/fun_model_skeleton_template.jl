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

    env[:indexProcess] = 0 # 初始化过程所在位置
    # env[:stateOfSchedule] = :stepping
    # @test println("切换调度运作状态为$(env[:stateOfSchedule])")

    env[:tau] = 0 # 初始化回合

    if (env[:isModel])
        if (env[:tau] > 0)
            @test println("继续模型model：\n")
        else
            @test println("开始模型model：\n")
        end
    end

    ## 过程

    #=【插入表达式】=#

    ## 判断是否结束
    if !env[:isStep]
        @test println("步进已结束，跳出$(env[:modelName])。")
    end

    if env[:stateOfSchedule] == :idle
        env[:isModel] = false
        env[:isExperiment] = false
    end

    if (!env[:isModel] || !env[:isExperiment])
        @test println("$(env[:modelName])结束。")
    end


    # return BB, BI, para, env
    # return BB, BI, BB_tau, BI_tau, para, env
end # function

# end # module






