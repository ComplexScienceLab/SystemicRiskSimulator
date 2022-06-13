"函数：通用模型框架"

## 函数：通用模型框架

##########################################
#状态/开发
##########################################

"""
通用模型框架：

Argument: 
- A::SystemicRiskAgent: Agent群变量；
- para::dict: 参数变量；
- env::dict: 环境变量；
- model::ModelComponent: 模型组件实例；
- A_data::AgentDataCollection: Agent群变量之数据；

Return:
- A::SystemicRiskAgent: Agent群变量；
- para::dict: 参数变量；
- env::dict: 环境变量；
- A_data::AgentDataCollection: Agent群变量之数据；
"""
def fun_model_skeleton(A:SystemicRiskAgent, para:dict, env:dict, model:ModelComponent, A_data:AgentDataCollection):
    if (env['isModel'])
        if (env['tau'] > 1)
            @testprintln "\n继续模型：$(env['modelName'])"
        else:
            @testprintln "\n开始模型：$(env['modelName'])"
            pass
        pass

    ## 运行每个过程
    for (idx_process, process) in enumerate(model.content)
        env['indexProcess'] = idx_process
        if env['indexProcess'] == env['loadedIndexProcess']: # 调度读取：如果当前过程等于待读取的过程，则进入继续读取。
            env['processName'] = Symbol(process.functionName)
            A, para, env, A_data = runProcess(A, para, env, process, A_data)
            pass
        pass # for

    ## 判断是否结束步进
    if !env['isStep']
        @testprintln "步进已结束，跳出模型：$(env['modelName'])。"
        pass
    # 判断是否结束模型
    if env['stateOfSchedule'] == StateOfSchedule.idle
        env['isModel'] = False
        env['isExperiment'] = False
        pass
    if (!env['isModel'] || !env['isExperiment'])
        @testprintln "结束模型：$(env['modelName'])。\n"
        pass


    # return BB, BI, para, env
    return A, para, env, A_data
    pass # functions

#     pass # module






