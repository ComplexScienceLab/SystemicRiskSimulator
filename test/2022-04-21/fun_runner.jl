"运行器"

## 模型运行器

##########################################
#状态/开发
##########################################

"模型运行器"
function runModel!(modelComponent::ModelComponent)
    data = modelComponent.run(modelComponent)
    return data
end


"过程运行器"
function runProcess!(processComponent::StageComponent)
    data = processComponent.run(processComponent)
    return data
end


"阶段运行器"
function runStage!(stageComponent::StageComponent)
    data = stageComponent.run(stageComponent)
    return data
end





