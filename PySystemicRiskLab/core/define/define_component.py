"程序：定义模型及其相关的结构体"

from PySystemicRiskLab.core.define.define_type import *

# from PySystemicRiskLab.core import ModelRunner
pass  # end import


class Component:
    """
    定义公共组件
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

    pass  # class


class StageComponent(Component):
    """
    定义阶段组件
    """
    # run: ModelRunner.run_model()  # 运行阶段
    run = None  # 运行阶段

    # content:Array{StageComponent} # 阶段组件列表

    # @classmethod
    def __init__(self, id, function_name, text_name, model_function):
        Component.__init__(Component, id, function_name, text_name)
        self.modelFunction = model_function
        pass

    pass  # class


class ProcessComponent(Component):
    """
    定义过程组件
    """
    # conditionToContinueProcess:Expr # 判断条件用以结束过程 conditionToContinueProcess
    # run: ModelRunner.run_process()  # 运行过程
    run = None  # 运行过程
    # processContent:Array{ProcessComponent} # 阶段组件列表
    content: list  # 阶段组件列表

    # @classmethod
    def __init__(self, id, function_name, text_name, run, content: list):
        Component.__init__(self, id, function_name, text_name)
        self.run = run
        self.content = content
        pass

    pass  # class


class ModelComponent(Component):
    """
    定义模型组件
    """
    # run: ModelRunner.run_stage()  # 运行模型
    run = None  # 运行模型
    content: list  # 过程组件列表

    # @classmethod
    def __init__(self, id, function_name, text_name, run, content: list):
        Component.__init__(self, id, function_name, text_name)
        self.run = run
        self.content = content

        pass

    pass
