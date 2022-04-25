"运行器"

## 模型运行器

##########################################
#状态/使用
##########################################

"""
模型运行器。
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
function runModel!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict, modelComponent::ModelComponent)
    BB, BI, para, env = modelComponent.run(BB, BI, para, env, modelComponent)
end


"""
过程运行器。
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
function runProcess!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict, processComponent::ProcessComponent)
    BB, BI, para, env = processComponent.run(BB, BI, para, env, processComponent)
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
function runStage!(BB::BankCommercial, BI::BankInterbank, para::Dict, env::Dict, stageComponent::StageComponent)
    BB, BI, para, env = stageComponent.run(BB, BI, para, env)
    return BB, BI, para, env
end





