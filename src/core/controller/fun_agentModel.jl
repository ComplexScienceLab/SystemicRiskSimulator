"功能函数区：Agent模型相关功能函数，基于Agents工具包"


##########################################
#状态/开发
##########################################




"初始化systemicRiskAgent和systemicRiskModel"
function init_systemicRiskAgent!(para::Dict, env::Dict)
    bank, interbank, bank_tau_0, interbank_tau_0, bank_tau, bankinter_tau = init_B_and_BI(; init_method=env[:init_method])

    ## 调度状态
    env[:stateOfSchedule] = :loading
    # if env[:stateOfSchedule] == :saving
    #     env[:savedIndexProcess], env[:savedIndexStage], env[:stateOfSchedule] = scheduler_saving(env[:indexOfSchedulePosition], env[:indexProcess], env[:indexStage]) # 存储
    # end
    # if env[:stateOfSchedule] == :collecting
    #     env[:stateOfSchedule] = scheduler_collecting() #TODO 收集数据
    # end

    systemicRiskAgent = SystemicRiskAgent(
        1, # 编号（必备的）
        bank, # 商业银行群
        interbank # 银行间邻接矩阵
    )
    systemicRiskModel = ABM(systemicRiskAgent; properties=para) # 构建Agent模型
    return systemicRiskAgent, systemicRiskModel, bank_tau_0, interbank_tau_0, bank_tau, bankinter_tau
end

# space = GraphSpace(#= #TODO生成图空间 =#)


# "函数：构建Agent模型" #HACK 冗余
# function create_systemicRiskModel(systemicRiskAgent::SystemicRiskAgent, para::Dict)
#     return systemicRiskModel
# end


"函数：Agent模型步进" #BUG方案一
function systemicRiskAgent_step!(systemicRiskAgent::SystemicRiskAgent, systemicRiskModel::ABM, para::Dict, env::Dict, model::ModelComponent)
    env[:isStep] = true
    systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = runModel!(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env, model) # 运行具体的模型，通过运行模型组件的方式
    # systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = fun_model_skeleton!(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # HACK冗余
    # systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = modelComponent.run!(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # HACK冗余
    _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, env[:maxNumOfTau])
end

# "函数：Agent模型步进" #BUG方案二
# function systemicRiskAgent_step!(systemicRiskAgent::SystemicRiskAgent, systemicRiskModel::ABM, para::Dict, env::Dict)
#     env[:isStep] = true
#     systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = model_BI1111!(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # 调用具体的模型
#     _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, env[:maxNumOfTau])
# end


