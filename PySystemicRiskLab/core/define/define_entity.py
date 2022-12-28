"""程序：定义模型实体"""

from PySystemicRiskLab.core.define.define_aspect import *

pass  # end import


class Entity:
    """
    定义实体
    """
    attribute: AttributeAspect
    content: ContentAspect
    container: ContainerAspect
    process: ProcessAspect

    # id: ItemIdType  # 编号 id
    # entity_name: ItemFunctionNameType  # 函数名称 name
    # text_name: ItemTextNameType  # 文本名称 name
    # content_type: str  # 内容之类型
    # conditionToRun: str  # 运作条件
    # content: ContentAspectType  # 内容
    #

    def __init__(self, entityData: Any):
        self.attribute = AttributeAspect(entityData['attribute'])
        self.content = entityData['content']
        self.container = entityData['container']
        self.process = entityData['process']
        pass  # method

    # def __init__(self, property_content: AttributeAspect, content: ContentAspect, container: ContainerAspect, process: ProcessAspect):
    #     self.attribute = property_content
    #     self.content = content
    #     self.container = container
    #     self.process = process
    #     pass  # method

    # @clsassmethod
    # def installEntity(cls,):
    #
    #     pas  # method

    pass  # class


# class AlgorithmEntity(Entity):  # HACK 无用
#     """
#     定义算法实体
#     """
#     # content = Executer.execute  # 函数
#     content = None  # 函数
#
#     # @classmethod
#     def __init__(self, id, entity_name, text_name, content):
#         super().__init__(id, entity_name, text_name)
#         self.content = content
#         pass
#
#     pass
#
#
# class ProcessEntity(Entity):  # HACK 无用
#     """
#     定义过程实体
#     """
#     # content:Vector{ProcessEntity} # 过程实体列表 listContentProcess
#     content: list  # 阶段实体列表 content
#
#     # @classmethod
#     def __init__(self, id, entity_name, text_name, content: list):
#         super().__init__(id, entity_name, text_name)
#         self.content = content
#         pass
#
#     pass
#
#
# class ModelEntity(Entity):  # HACK 无用
#     """
#     定义模型实体
#     """
#     content: list  # 过程实体列表 listContentProcess
#
#     # @classmethod
#     def __init__(self, id, entity_name, text_name, content: list):
#         super().__init__(id, entity_name, text_name)
#         self.content = content
#         pass
#
#     pass  # class
