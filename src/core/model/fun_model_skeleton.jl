"函数：通用模型框架"

## 函数：通用模型框架

##########################################
#状态/开发
##########################################

"""
TODO通用模型框架：

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
function fun_model_skeleton!(A::SystemicRiskAgent, para::Dict, env::Dict, model::ModelComponent, A_data::AgentDataCollection)

    if (env[:isModel])
        if (env[:tau] > 1)
            @testprintln "\n继续模型：$(env[:modelName])"
        else
            @testprintln "\n开始模型：$(env[:modelName])"
        end
    end

    ## 运行每个过程
    for (idx_process, process) in enumerate(model.content)
        env[:indexProcess] = idx_process
        if env[:indexProcess] == env[:loadedIndexProcess] # 调度读取：如果当前过程等于待读取的过程，则进入继续读取。
            env[:processName] = Symbol(process.functionName)
            A, para, env, A_data = runProcess!(A, para, env, process, A_data)
        end
    end # for

    ## 判断是否结束步进
    if !env[:isStep]
        @testprintln "步进已结束，跳出模型：$(env[:modelName])。"
    end
    # 判断是否结束模型
    if env[:stateOfSchedule] == :idle
        env[:isModel] = false
        env[:isExperiment] = false
    end
    if (!env[:isModel] || !env[:isExperiment])
        @testprintln "结束模型：$(env[:modelName])。\n"
    end


    # return BB, BI, para, env
    return A, para, env, A_data
end # function

# end # module






