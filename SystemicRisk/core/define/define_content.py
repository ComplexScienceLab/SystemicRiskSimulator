"程序：定义模型内容结构体"
import numpy as np

from SystemicRisk import ModelRunner
from SystemicRisk.core.define.define_type import *


class Content:
    """
    定义抽象内容
    """
    id: type_item_id  # 编号 id
    function_name: np.dtype(np.str)  # 函数名称 name
    text_name: np.dtype(np.str)  # 文本名称 name

    def __init__(self, id, function_name, text_name):
        self.id = id
        self.function_name = function_name
        self.text_name = text_name
        pass

    pass


class StageContent(Content):
    """
    定义阶段组件内容结构体
    """
    modelFunction: ModelRunner.run_stage()  # 函数

    def __init__(self, id, function_name, text_name):
        Content.__init__(id, function_name, text_name)
        pass

    pass


class ProcessContent:
    """
    定义过程组件内容结构体
    """
    # listProcessContent:Vector{ProcessContent} # 过程内容列表 listContentProcess
    listStageContent: list  # 阶段内容列表 listStageContent

    def __init__(self, id, function_name, text_name):
        Content.__init__(id, function_name, text_name)
        pass

    pass


class ModelContent:
    """
    定义模型组件内容结构体
    """
    listProcessContent: list  # 过程内容列表 listContentProcess

    def __init__(self, id, function_name, text_name):
        Content.__init__(id, function_name, text_name)
        pass

    pass
