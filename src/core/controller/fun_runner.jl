"运行器"

## 模型运行器

##########################################
#状态/开发
##########################################

"模型运行器"
function runModel!(modelComponent::ModelComponent)
    BB, BI, para, env = modelComponent.run!(modelComponent)
    return BB, BI, para, env
end


"过程运行器"
function runProcess!(processComponent::ProcessComponent)
    BB, BI, para, env = processComponent.run!(processComponent)
    return BB, BI, para, env
end


"阶段运行器"
function runStage!(stageComponent::StageComponent)
    BB, BI, para, env = stageComponent.run!(stageComponent)
    return BB, BI, para, env
end





