"程序：定义模型及其相关的结构体"

from SystemicRisk.core.define.define_type import *
# from SystemicRisk.core import ModelRunner


class Component:
    """
    定义公共组件
    """
    id: TypeItemId  # 编号 id
    function_name: TypeItemFunctionName  # 函数名称 name
    text_name: TypeItemTextName  # 文本名称 name

    def __init__(self, id, function_name, text_name):
        self.id = id
        self.function_name = function_name
        self.text_name = text_name
        pass

    pass


class StageComponent(Component):
    """
    定义阶段组件
    """
    # run: ModelRunner.run_model()  # 运行阶段
    run = None  # 运行阶段

    # content:Array{StageComponent} # 阶段组件列表

    def __init__(self, id, function_name, text_name):
        Component.__init__(id, function_name, text_name)

    pass


class ProcessComponent(Component):
    """
    定义过程组件
    """
    # conditionToContinueProcess:Expr # 判断条件用以结束过程 conditionToContinueProcess
    # run: ModelRunner.run_process()  # 运行过程
    run = None  # 运行过程
    # processContent:Array{ProcessComponent} # 阶段组件列表
    content: list  # 阶段组件列表

    def __init__(self, id, function_name, text_name):
        Component.__init__(id, function_name, text_name)

    pass


class ModelComponent(Component):
    """
    定义模型组件
    """
    # run: ModelRunner.run_stage()  # 运行模型
    run = None  # 运行模型
    content: list  # 过程组件列表

    def __init__(self, id, function_name, text_name):
        Component.__init__(id, function_name, text_name)

    pass
