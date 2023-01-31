"""程序：定义模型实体"""

from PySystemicRiskLab.core.define.define_component import *

pass  # end import


class Entity:
    """
    定义实体
    """

    attribute: AttributeComponent
    content: ContentComponent
    container: ContainerComponent
    process: ProcessComponent
    node: NodeComponent
    execute: ExecuteComponent

    def __init__(self, entityData: Any):
        """
        attribute: AttributeComponent
        content: ContentComponent
        container: ContainerComponent
        process: ProcessComponent
        node: NodeComponent
        execute: ExecuteComponent

        Args:
            entityData ():
        """
        self.attribute = AttributeComponent(entityData['attribute'])
        self.content = entityData['content'] if entityData['content'] is not None else None
        self.container = entityData['container'] if entityData['container'] is not None else None
        # self.process = entityData['process'] if entityData['process'] is not None else None
        # self.node = entityData['node'] if entityData['node'] is not None else None
        self.execute = entityData['execute'] if entityData['execute'] is not None else None
        pass  # method

    # def __init__(self, property_content: AttributeComponent, content: ContentComponent, container: ContainerComponent, process: ProcessComponent):
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
