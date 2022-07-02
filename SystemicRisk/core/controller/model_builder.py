"生成器"

##########################################
# 状态/使用
##########################################
# from SystemicRisk.core import ModelContent, ProcessContent, StageContent, ModelComponent, ProcessComponent, StageComponent, fun_model_skeleton, fun_process_skeleton
pass  # end import



from SystemicRisk.core.define.define_content import ModelContent, ProcessContent, StageContent
from SystemicRisk.core.define.define_component import ModelComponent, ProcessComponent, StageComponent
from SystemicRisk.core.model import fun_model_skeleton, fun_process_skeleton
pass  # end import






class ModelBuilder:
    """
    函数：阶段实例生成器

    Argument:
    - stageContent:StageContent: 阶段核心内容；
    - stageSkeleton:Function = fun_stage_skeleton: 阶段架构函数；

    Return:
    - stage:StageComponent: 阶段组件实例
    """

    def build_stage(self, stage_content: StageContent):
        ## 获得阶段类型
        stageInstanceType = stage_content.functionName

        ## 生成阶段stage
        stage = StageComponent(
            stage_content.id,
            stage_content.functionName,
            stage_content.textName,
            stage_content.modelFunction,
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

    def buildProcess(self, process_content: ProcessContent, processSkeleton=fun_process_skeleton):
        ## 获得过程类型
        processInstanceType = process_content.functionName

        ## 生成子阶段组件列表
        list_stage = []
        for stageContent in process_content.listStageContent:
            stage = self.buildStage(stageContent)
            list_stage.append([stage])
            pass

        ## 生成过程process
        process = ProcessComponent(
            process_content.id,
            process_content.functionName,
            process_content.textName,
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

    def buildModel(self, modelContent: ModelContent, modelSkeleton=fun_model_skeleton):

        ## 获得模型类型
        modelInstanceType = modelContent.functionName

        ## 生成子过程组件列表
        list_process = []
        for processContent in modelContent.listProcessContent:
            process = self.buildProcess(processContent)
            list_process.append([process])
            pass

        ## 生成模型model
        model = ModelComponent(
            modelContent.id,
            modelContent.functionName,
            modelContent.textName,
            modelSkeleton,
            list_process,
        )

        # @testprintln "已经生成模型$(modelContent.functionName)"

        return model
        pass

    pass  # class
