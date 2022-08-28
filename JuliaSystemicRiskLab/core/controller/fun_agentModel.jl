"功能函数区：Agent模型相关功能函数，基于Agents工具包"


##########################################
#状态/开发
##########################################




"初始化systemicRiskAgent和systemicRiskModel"
function init_systemicRiskAgent!(para::Dict, env::Dict)
    systemicRiskAgent, systemicRiskAgent_data = init_B_and_BI(; init_method=env[:init_method])

    ## 调度状态
    env[:state_of_schedule] = :loading

    # ## 构建Agent模型
    # systemicRiskAgent = SystemicRiskAgent(
    #     1, # 编号（必备的）
    #     banks, # 商业银行群
    #     interbank # 银行间邻接矩阵
    # )
    systemicRiskModel = ABM(systemicRiskAgent; properties=(Dict([collect(para); collect(env)])))
    return systemicRiskAgent, systemicRiskModel, systemicRiskAgent_data
end

"函数：Agent模型步进"
function systemicRiskAgent_step!(A::SystemicRiskAgent, systemicRiskModel::ABM, para::Dict, env::Dict, model::ModelComponent, A_data::AgentDataCollection)
    env[:is_step] = true
    A, para, env, A_data = runModel!(A, para, env, model, A_data) # 运行具体的模型，通过运行模型组件的方式
    # systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = fun_model_skeleton!(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # HACK冗余
    # systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = modelComponent.run!(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # HACK冗余
    # _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, env[:max_num_of_tau])
end

# "函数：Agent模型步进"
# function systemicRiskAgent_step!(systemicRiskAgent::SystemicRiskAgent, systemicRiskModel::ABM, para::Dict, env::Dict)
#     env[:is_step] = true
#     systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = model_BI1111!(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # 调用具体的模型
#     _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, env[:max_num_of_tau])
# end


