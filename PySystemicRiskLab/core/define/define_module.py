"程序：定义模型及其相关的结构体"

from PySystemicRiskLab.core.define.define_type import *

pass  # end import


class Module:
    """
    定义模块
    """
    id: ItemIdType  # 编号 id
    functionName: ItemFunctionNameType  # 函数名称 name
    textName: ItemTextNameType  # 文本名称 name
    contentType: str  # 内容之类型
    content: ContentAspectType  # 内容
    execute: None  # 执行

    def __init__(self, id, function_name, text_name, content_type, content, execute):
        self.id = id
        self.functionName = function_name
        self.textName = text_name
        self.contentType = content_type
        self.content = content
        self.execute = execute
        pass

    pass  # class


class AlgorithmModule(Module): #HACK 无用
    """
    定义算法模块
    """
    # execute: Executer.runModel()  # 执行阶段
    execute = None  # 执行阶段

    # content:Array{AlgorithmModule} # 算法模块列表

    def __init__(self, id, function_name, text_name, execute):
        # super(AlgorithmModule, self).__init__()
        super().__init__(id, function_name, text_name)
        self.execute = execute
        pass

    pass  # class


class ProcessModule(Module): #HACK 无用
    """
    定义过程模块
    """
    # conditionToContinueProcess:Expr # 判断条件用以结束过程 conditionToContinueProcess
    # execute: Executer.execute_branch_node()  # 执行过程
    execute = None  # 执行过程
    # processEntity:Array{ProcessModule} # 算法模块列表
    content: list  # 算法模块列表

    def __init__(self, id, function_name, text_name, execute, content: list):
        super().__init__(id, function_name, text_name)
        self.execute = execute
        self.content = content
        pass

    pass  # class


class ModelModule(Module): #HACK 无用
    """
    定义模型模块
    """
    # execute: Executer.execute()  # 执行模型
    execute = None  # 执行模型
    content: list  # 过程模块列表

    def __init__(self, id, function_name, text_name, execute, content: list):
        super().__init__(id, function_name, text_name)
        self.execute = execute
        self.content = content
        pass

    pass  # class
