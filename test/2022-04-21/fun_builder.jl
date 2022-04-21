"生成器"

##########################################
#状态/开发
##########################################



"""
函数：阶段生成器
"""
function buildStage(stageContent::StageContent; stageSkeleton::Function=stageSkeleton)
    ## 获得阶段类型
    stageInstanceType = Symbol(stageContent.functionName)

    ## 生成阶段stage
    stage = StageComponent{stageInstanceType}(stageSkeleton,
        stageContent,
    )

    println("已经生成阶段$(stageContent.functionName)")

    return stage
end




"""
函数：过程生成器
"""
function buildProcess(processContent::ProcessContent; processSkeleton::Function=fun_process_skeleton!, stage::StageComponent=stage)
    ## 获得过程类型
    modelType = Symbol(processContent.functionName)

    ## 生成子阶段组件列表
    list_stage = Array{StageComponent}
    for stageContent in processContent.listStageContent
        stage = buildStage(stageContent)
        append!(list_stage, stage)
    end

    ## 生成过程process
    process = StageComponent{modelType}(
        processContent.id,
        processContent.functionName,
        processContent.textName,
        processSkeleton,
        list_stage,
    )

    println("已经生成过程$(processContent.functionName)")

    return process
end



"""
函数：模型生成器
"""
function buildModel(modelContent::ModelContent; modelSkeleton::Function=fun_model_skeleton!)

    ## 获得模型类型
    modelType = Symbol(modelContent.functionName)

    ## 生成子过程组件列表
    list_process = Array{StageComponent}
    for processContent in modelContent.listProcessContent
        process = buildProcess(processContent)
        append!(list_process, process)
    end

    ## 生成模型model
    model = ModelComponent{modelType}(
        modelContent.id,
        modelContent.functionName,
        modelContent.textName,
        modelSkeleton,
        list_process,
    )

    println("已经生成模型$(modelContent.functionName)")

    return model
end

