"运行机"

## 模型运行机

##########################################
#状态/开发
##########################################

"模型运行机"
function runModel!(data::Float64, modelComponent::ModelComponent)
    data = modelComponent.run(data, modelComponent)
    return data
end


"过程运行机"
function runProcess!(data::Float64, processComponent::ProcessComponent)
    data = processComponent.run(data, processComponent)
    return data
end


"阶段运行机"
function runStage!(data::Float64, stageComponent::StageComponent)
    data = stageComponent.run(data)
    return data
end





