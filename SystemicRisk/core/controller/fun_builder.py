"生成器"

##########################################
# 状态/使用
##########################################
from SystemicRisk.core import ModelContent, ProcessContent, StageContent, ModelComponent, ProcessComponent, StageComponent, fun_model_skeleton, fun_process_skeleton


class ModelBuilder:
    """
    函数：阶段实例生成器

    Argument:
    - stageContent:StageContent: 阶段核心内容；
    - stageSkeleton:Function = fun_stage_skeleton: 阶段架构函数；

    Return:
    - stage:StageComponent: 阶段组件实例
    """

    def build_stage(stage_content: StageContent):
        ## 获得阶段类型
        stageInstanceType = stage_content.function_name

        ## 生成阶段stage
        stage = StageComponent
        {stageInstanceType}(
            stage_content.id,
            stage_content.function_name,
            stage_content.text_name,
            stage_content.model_function,
        )

        # @testprintln "已经生成阶段$(stageContent.functionName)"

        return stage
        pass

    """
    函数：过程实例生成器
    
    Argument: 
    - processContent:ProcessContent: 过程核心内容；
    - processSkeleton:Function = fun_process_skeleton: 过程架构函数；
    
    Return:
    - process:ProcessComponent: 过程组件实例
    """

    def buildProcess(process_content: ProcessContent, processSkeleton = fun_process_skeleton):
        ## 获得过程类型
        processInstanceType = process_content.function_name

        ## 生成子阶段组件列表
        list_stage = []
        for stageContent in process_content.listStageContent:
            stage = buildStage(stageContent)
            append(list_stage, [stage])
            pass

        ## 生成过程process
        process = ProcessComponent
        {processInstanceType}(
            process_content.id,
            process_content.function_name,
            process_content.text_name,
            # processContent.conditionToContinueProcess,
            processSkeleton,
            list_stage,
        )

        # @testprintln "已经生成过程$(processContent.functionName)"

        return process
        pass

    """
    函数：模型实例生成器
    
    Argument: 
    - modelContent:ModelContent: 模型核心内容；
    - modelSkeleton:Function = fun_model_skeleton: 模型架构函数；
    
    Return:
    - model:ModelComponent: 模型组件实例
    """

    def buildModel(modelContent: ModelContent, modelSkeleton = fun_model_skeleton):

        ## 获得模型类型
        modelInstanceType = modelContent.function_name

        ## 生成子过程组件列表
        list_process = []
        for processContent in modelContent.listProcessContent:
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

        # @testprintln "已经生成模型$(modelContent.functionName)"

        return model
        pass

    pass  # class
