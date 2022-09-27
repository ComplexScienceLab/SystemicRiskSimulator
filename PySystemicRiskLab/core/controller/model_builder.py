##########################################
# 状态/使用
##########################################
# from PySystemicRiskLab.core import ModelContent, ProcessContent, StageContent, ModelComponent, ProcessComponent, StageComponent, fun_model_skeleton, fun_process_skeleton
pass  # end import

from PySystemicRiskLab import deepcopy, np, logging
from PySystemicRiskLab.core.define.define_component import ModelComponent, ProcessComponent, StageComponent
from PySystemicRiskLab.core.define.define_content import ProcessContent, StageContent
from PySystemicRiskLab.core.model.fun_model_skeleton import ModelSkeleton
from PySystemicRiskLab.core.model.fun_process_skeleton import ProcessSkeleton

pass  # end import


class ModelBuilder:
    "模型生成器"

    @classmethod
    def buildStage(cls, stage_content: StageContent):
        """
        函数：阶段实例生成器

        Args:
            stage_content (StageContent): 阶段核心内容

        Returns: stage (StageComponent): 阶段组件实例

        """

        ## 获得阶段类型
        stageInstanceType = stage_content.functionName

        ## 生成阶段stage
        stage = StageComponent(
            id=stage_content.id,
            function_name=stage_content.functionName,
            text_name=stage_content.textName,
            model_function=deepcopy(stage_content.stageFunction),
        )

        logging.debug("已经生成阶段%s", stage_content.functionName)

        return stage
        pass  # function

    @classmethod
    def buildProcess(cls, process_content: ProcessContent, processSkeleton=ProcessSkeleton.fun_process_skeleton):
        """
        函数：过程实例生成器

        Args:
            process_content (ProcessContent): 过程核心内容
            processSkeleton (Function): 过程架构函数

        Returns: process (ProcessComponent): 过程组件实例

        """

        ## 获得过程类型
        processInstanceType = process_content.functionName

        ## 生成子阶段组件列表
        list_stage = [cls.buildStage(stageContent) for stageContent in process_content.listStageContent]

        ## 生成过程process
        process = ProcessComponent(
            id=process_content.id,
            function_name=process_content.functionName,
            text_name=process_content.textName,
            # processContent.conditionToContinueProcess,
            run=processSkeleton,
            content=list_stage,
        )

        logging.debug("已经生成过程%s", process_content.functionName)

        return process
        pass  # function

    @classmethod
    def buildModel(cls, modelContent, modelSkeleton=ModelSkeleton.fun_model_skeleton):
        """
        函数：模型实例生成器

        Args:
            modelContent (ModelContent): 模型核心内容
            modelSkeleton (Function): 模型架构函数

        Returns: models (ModelComponent): 模型组件实例

        """

        ## 获得模型类型
        modelInstanceType = modelContent.functionName

        ## 生成子过程组件列表
        list_process = [cls.buildProcess(processContent) for processContent in modelContent.listProcessContent]

        ## 生成模型model
        model = ModelComponent(
            id=modelContent.id,
            function_name=modelContent.functionName,
            text_name=modelContent.textName,
            run=modelSkeleton,
            content=list_process,
        )

        logging.debug("已经生成模型%s", modelContent.functionName)

        return model
        pass  # function

    pass  # class
