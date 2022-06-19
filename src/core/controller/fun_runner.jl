"运行器"

## 模型运行器

##########################################
#状态/使用
##########################################

"""
模型运行器。
输入参数将被直接修改。

Argument: 
- A::SystemicRiskAgent: Agent群变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- modelComponent::ModelComponent: 模型组件实例；
- A_data::AgentDataCollection: Agent群变量之数据；

Return:
- A::SystemicRiskAgent: Agent群变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- A_data::AgentDataCollection: Agent群变量之数据；
"""
function runModel!(A::SystemicRiskAgent, para::Dict, env::Dict, modelComponent::ModelComponent, A_data::AgentDataCollection)
    A, para, env, A_data = modelComponent.run(A, para, env, modelComponent, A_data)
    return A, para, env, A_data
end


"""
过程运行器。
输入参数将被直接修改。

Argument: 
- A::SystemicRiskAgent: Agent群变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- processComponent::ProcessComponent: 过程组件实例；
- A_data::AgentDataCollection: Agent群变量之数据；

Return:
- A::SystemicRiskAgent: Agent群变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- A_data::AgentDataCollection: Agent群变量之数据；
"""
function runProcess!(A::SystemicRiskAgent, para::Dict, env::Dict, processComponent::ProcessComponent, A_data::AgentDataCollection)
    A, para, env, A_data = processComponent.run(A, para, env, processComponent, A_data)
    return A, para, env, A_data
end


"""
阶段运行器。
输入参数将被直接修改。

Argument: 
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- b::TypeState{1}: 商业银行群示性向量；
- ib::TypeState{2}: 银行间邻接矩阵示性矩阵；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- stageComponent::StageComponent: 阶段组件实例；

Return:
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
"""
function runStage!(A::SystemicRiskAgent, b::TypeState{1}, ib::TypeState{2}, para::Dict, env::Dict, stageComponent::StageComponent)
    A.BB, A.BI = stageComponent.run(A.BB, A.BI, b, ib, para, env)
    return A
end





