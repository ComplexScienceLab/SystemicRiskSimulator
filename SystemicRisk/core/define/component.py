"程序：定义模型及其相关的结构体"

from define_type import *
from SystemicRisk import ModelRunner


# "定义综合组件"# HACK 较为抽象，暂时不会用。
# class Component{ComponentHierarchyType,ComponentInstanceType}
#     name:String # 组件名称
#     content:Union{ComponentHierarchyType,ComponentInstanceType} # 组件核心内容
#     run:Function # 运行组件
#     pass


class StageComponent:
    """
    定义阶段组件
    """
    id: type_item_id  # 编号 id
    functionName: type_item_function_name  # 函数名称 name
    textName: type_item_text_name  # 文本名称 name
    run: ModelRunner.run_model()  # 运行阶段
    # content:Array{StageComponent} # 阶段组件列表
    pass


class ProcessComponent:
    """
    定义过程组件
    """
    id: type_item_id  # 编号 id
    functionName: type_item_function_name  # 函数名称 name
    textName: type_item_text_name  # 文本名称 name
    # conditionToContinueProcess:Expr # 判断条件用以结束过程 conditionToContinueProcess
    run: ModelRunner.run_process()  # 运行过程
    # processContent:Array{ProcessComponent} # 阶段组件列表
    content: list  # 阶段组件列表
    pass


class ModelComponent:
    """
    定义模型组件
    """
    id: type_item_id  # 编号 id
    functionName: type_item_function_name  # 函数名称 name
    textName: type_item_text_name  # 文本名称 name
    run: ModelRunner.run_stage()  # 运行模型
    content: list  # 过程组件列表
    pass
