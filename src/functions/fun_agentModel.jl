"功能函数区：Agent模型相关功能函数，基于Agents工具包"


##########################################
#状态/开发
##########################################




"初始化systemicRiskAgent和systemicRiskModel"
function init_systemicRiskAgent!(para::Dict, env::Dict)
    bank, interbank, bank_tau_0, interbank_tau_0, bank_tau, bankinter_tau = init_B_and_BI(; init_method = env[:init_method])

    systemicRiskAgent = SystemicRiskAgent(
        1, # 编号（必备的）
        bank, # 商业银行群
        interbank # 银行间邻接矩阵
    )
    systemicRiskModel = ABM(systemicRiskAgent; properties = para) # 构建Agent模型
    return systemicRiskAgent, systemicRiskModel, bank_tau_0, interbank_tau_0, bank_tau, bankinter_tau
end

# space = GraphSpace(#= #TODO生成图空间 =#)


# "函数：构建Agent模型" #HACK 冗余
# function create_systemicRiskModel(systemicRiskAgent::SystemicRiskAgent, para::Dict)
#     return systemicRiskModel
# end


"函数：Agent模型步进" #TODO方案一
function systemicRiskAgent_step!(systemicRiskAgent::SystemicRiskAgent, systemicRiskModel::ABM, para::Dict, env::Dict)
    systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = model_BI1111(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # 调用具体的模型
end


"函数：Agent模型步进" #NOW 方案二
function systemicRiskAgent_step!(systemicRiskAgent::SystemicRiskAgent, systemicRiskModel::ABM, para::Dict, env::Dict)
    systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = model_BI1111(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # 调用具体的模型
end
