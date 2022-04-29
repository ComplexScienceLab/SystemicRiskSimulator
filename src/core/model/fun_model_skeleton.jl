"函数：通用模型框架"

## 函数：通用模型框架

##########################################
#状态/开发
##########################################

"""
通用模型框架：

Argument: 
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- modelComponent::ModelComponent: 模型组件实例；

Return:
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
"""
function fun_model_skeleton!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict, model::ModelComponent)

    # env[:indexProcess] = 0 # 初始化过程所在位置
    # env[:stateOfSchedule] = :stepping
    # @test println("切换调度运作状态为$(env[:stateOfSchedule])")


    if (env[:isModel])
        if (env[:tau] > 1)
            @test println("\n继续模型：env[:modelName]\n")
        else
            @test println("开始模型：$(env[:modelName])\n")
        end
    end

    ##NOW 运行每一个过程
    # for (i, p) in eval(Meta.parse(enumerate(para[:modelName] * ".listProcess"))) # HACK 元编程方式
    # for (idx_process, processComponent) in modelComponent.content.listProcessComponent
    # for (idx_process, processContent) in modelComponent.content.listProcessContent
    for (idx_process, process) in enumerate(model.content)
        env[:indexProcess] = idx_process
        if env[:indexProcess] == env[:loadedIndexProcess]
            env[:processName] = Symbol(process.functionName)
            # expr = "BB, BI, env = " * String(p) * "!(BB, BI, para, env)"
            # @scheduler_process Meta.parse(expr)
            # scheduler!(env)
            # if env[:stateOfSchedule] == :stepping
            # eval(Meta.parse(expr))
            runProcess!(BB, BI, para, env, process)
        end
        # BB, BI, env = runProcess!(processComponent)(BB, BI, para, env)
        # end
        # if env[:stateOfSchedule] == :collecting
        #TODO 收集数据
        # end
        # scheduler!(ModelContent, env, expr)
        # @scheduler_process Meta.parse(expr)
    end # for

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


    return BB, BI, para, env
    # return BB, BI, BB_tau, BI_tau, para, env
end # function

# end # module






