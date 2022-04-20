"生成器"

##########################################
#状态/开发
##########################################



"""
NOW函数：阶段生成器
做如下事情：
1. 调取阶段核心内容stageContent、阶段外围框架stageSkeleton；
2. 插入阶段核心内容stageContent至阶段外围框架stageSkeleton内，组合成阶段stage；
3. 写出阶段stage为文件stage.jl；
Argument: 
- stageContent::StageContent: 阶段核心内容
"""
function buildStage(stageContent::StageContent; stageSkeleton::Function=stageSkeleton)
    ## 获得阶段类型
    stageInstanceType = Symbol(stageContent.functionName)

    ## 生成阶段stage
    stage = StageComponent{stageInstanceType}(
        stageSkeleton,
        stageContent,
    )

    @test println("已经生成阶段$(stageContent.functionName)")

    return stage
end




"""
NOW函数：过程生成器
做如下事情：
1. 调取过程核心内容processContent、过程外围框架processSkeleton；
2. 插入过程核心内容processContent至过程外围框架processSkeleton内，组合成过程process；
3. 写出过程process为文件process.jl；
Argument: 
- processContent::ProcessContent: 过程核心内容
"""
function buildProcess(processContent::ProcessContent; processSkeleton::Function=fun_process_skeleton!,stage::StageComponent=stage)
    ## 获得过程类型
    processInstanceType = Symbol(processContent.functionName)

    ## 生成过程process
    process = ProcessComponent{processInstanceType}(
        processSkeleton,
        processContent,
        stage=buildStage(processContent.listStageContent)
    )

    @test println("已经生成过程$(processContent.functionName)")

    return process
end



"""
NOW函数：模型生成器
做如下事情：
1. 调取模型核心内容modelContent、模型外围框架modelSkeleton；
2. 插入模型核心内容modelContent至模型外围框架modelSkeleton内，组合成模型model；
3. 写出模型model为文件model.jl；
Argument: 
- modelContent::ModelContent: 模型核心内容
"""
function buildModel(modelContent::ModelContent; modelSkeleton::Function=fun_model_skeleton!)

    ## 获得模型类型
    modelType = Symbol(modelContent.functionName)

    ## 生成模型model
    model = ModelComponent{modelType}(
        modelSkeleton,
        modelContent,
        for i in modelContent.listProcessContent
            process[i]=buildProcess(i)
        end
    )

    @test println("已经生成模型$(modelContent.functionName)")

    return model
end

