"程序：定义模型内容结构体"

from PySystemicRiskLab.core.define.define_type import *

# from PySystemicRiskLab.core.controller.model_runner import ModelRunner
pass  # end import


class Content:
    """
    定义抽象内容
    """
    id: TypeItemId  # 编号 id
    functionName: TypeItemFunctionName  # 函数名称 name
    textName: TypeItemTextName  # 文本名称 name

    # @classmethod
    def __init__(self, id, function_name, text_name):
        self.id = id
        self.functionName = function_name
        self.textName = text_name
        pass

    pass


class StageContent(Content):
    """
    定义阶段组件内容结构体
    """
    # model_function = ModelRunner.run_stage  # 函数
    stageFunction = None  # 函数

    # @classmethod
    def __init__(self, id, function_name, text_name, model_function):
        super().__init__(id, function_name, text_name)
        self.stageFunction = model_function
        pass

    pass


class ProcessContent(Content):
    """
    定义过程组件内容结构体
    """
    # list_process_content:Vector{ProcessContent} # 过程内容列表 listContentProcess
    listStageContent: list  # 阶段内容列表 list_stage_content

    # @classmethod
    def __init__(self, id, function_name, text_name, list_stage_content: list):
        super().__init__(id, function_name, text_name)
        self.listStageContent = list_stage_content
        pass

    pass


class ModelContent(Content):
    """
    定义模型组件内容结构体
    """
    listProcessContent: list  # 过程内容列表 listContentProcess

    # @classmethod
    def __init__(self, id, function_name, text_name, list_process_content: list):
        super().__init__(id, function_name, text_name)
        self.listProcessContent = list_process_content
        pass

    pass
