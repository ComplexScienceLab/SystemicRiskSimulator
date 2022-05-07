"运行器"

## 模型运行器

##########################################
#状态/使用
##########################################

"""
TODO模型运行器。
输入参数将被直接修改。

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
function runModel!(A::SystemicRiskAgent, para::Dict, env::Dict, modelComponent::ModelComponent, A_data::AgentDataCollection)
    return A_data, para, env, A_data = modelComponent.run(A, para, env, modelComponent, A_data)
end


"""
TODO过程运行器。
输入参数将被直接修改。

Argument: 
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- processComponent::ProcessComponent: 过程组件实例；

Return:
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
"""
function runProcess!(A::SystemicRiskAgent, para::Dict, env::Dict, processComponent::ProcessComponent, A_data::AgentDataCollection)
    return A, para, env, A_data = processComponent.run(A, para, env, processComponent, A_data)
end


"""
阶段运行器。
输入参数将被直接修改。

Argument: 
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
- stageComponent::StageComponent: 阶段组件实例；

Return:
- BB::BankCommercial: 商业银行群变量；
- BI::BankInterbank: 银行间邻接矩阵变量；
- para::Dict: 参数变量；
- env::Dict: 环境变量；
"""
function runStage!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict, env::Dict, stageComponent::StageComponent)
    stageComponent.run(BB, BI, b, ib, para, env)
end





