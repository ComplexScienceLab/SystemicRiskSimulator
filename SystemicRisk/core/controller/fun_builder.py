"生成器"

##########################################
#状态/使用
##########################################

class ModelBuilder:

    """
    函数：阶段实例生成器

    Argument:
    - stageContent:StageContent: 阶段核心内容；
    - stageSkeleton:Function = fun_stage_skeleton!: 阶段架构函数；

    Return:
    - stage:StageComponent: 阶段组件实例
    """
    def buildStage(stageContent:StageContent):
        ## 获得阶段类型
        stageInstanceType = Symbol(stageContent.function_name)

        ## 生成阶段stage
        stage = StageComponent{stageInstanceType}(
            stageContent.id,
            stageContent.function_name,
            stageContent.text_name,
            stageContent.modelFunction,
        )

        @testprintln "已经生成阶段$(stageContent.functionName)"

        return stage
        pass



    """
    函数：过程实例生成器
    
    Argument: 
    - processContent:ProcessContent: 过程核心内容；
    - processSkeleton:Function = fun_process_skeleton!: 过程架构函数；
    
    Return:
    - process:ProcessComponent: 过程组件实例
    """
    def buildProcess(processContent:ProcessContent, processSkeleton:Function=fun_process_skeleton):
        ## 获得过程类型
        processInstanceType = Symbol(processContent.function_name)

        ## 生成子阶段组件列表
        list_stage = []
        for stageContent in processContent.listStageContent
            stage = buildStage(stageContent)
            append(list_stage, [stage])
            pass

        ## 生成过程process
        process = ProcessComponent{processInstanceType}(
            processContent.id,
            processContent.function_name,
            processContent.text_name,
            # processContent.conditionToContinueProcess,
            processSkeleton,
            list_stage,
        )

        @testprintln "已经生成过程$(processContent.functionName)"

        return process
        pass



    """
    函数：模型实例生成器
    
    Argument: 
    - modelContent:ModelContent: 模型核心内容；
    - modelSkeleton:Function = fun_model_skeleton!: 模型架构函数；
    
    Return:
    - model:ModelComponent: 模型组件实例
    """
    def buildModel(modelContent:ModelContent, modelSkeleton:Function=fun_model_skeleton):

        ## 获得模型类型
        modelInstanceType = Symbol(modelContent.function_name)

        ## 生成子过程组件列表
        list_process = []
        for processContent in modelContent.listProcessContent
            process = buildProcess(processContent)
            append(list_process, [process])
            pass

        ## 生成模型model
        model = ModelComponent(
            modelContent.id,
            modelContent.function_name,
            modelContent.text_name,
            modelSkeleton,
            list_process,
        )

        @testprintln "已经生成模型$(modelContent.functionName)"

        return model
        pass

    pass # class