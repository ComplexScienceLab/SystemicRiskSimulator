function fun_model_skeleton!(data::Float64, modelComponent::ModelComponent)
    for (idx_process, processComponent) in enumerate(modelComponent.content)
        # data = processComponent.run(data, processComponent)
        runProcess!(data, processComponent)
    end
    return data
end

function fun_process_skeleton!(data::Float64, processComponent::ProcessComponent)
    for (idx_stage, stageComponent) in enumerate(processComponent.content)
        # data = stageComponent.run(data)
        data = runStage!(data, stageComponent)
    end
    return data
end

function fun_stage_skeleton!(data::Float64, stageComponent::StageComponent)
    return data
end