"""
构建机
"""

from PySystemicRiskLab import Any, deepcopy, re
from PySystemicRiskLab.core.define.define_type import EnvironmentVariableType
from PySystemicRiskLab.core.define.define_environmentVariables import env
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.define.define_component import AttributeComponent
from PySystemicRiskLab.core.operations.processor import Processor  # NOTE 动态导入，严禁删除
from PySystemicRiskLab.tools.tools import Tools

pass  # end import


class Builder:
    """构建机"""

    @classmethod
    def build_entities(cls, env: EnvironmentVariableType = env):
        """
        构建实体众

        Args:
            env(EnvironmentVariableType): 环境变量集

        Returns:
            algorithmEntities: 算法实体列表, algorithmContents: 算法内容列表

        """

        ## 导入相关模块（#NOTE 动态导入，严禁删除）
        ## 导入模型、过程、算法初始态实体之数据内容
        import PySystemicRiskLab.models.entities_data
        env['list_entityData'] = Tools.import_modules_from_package(env['folderpath_import_modules'], r"entityData_")
        ## 导入模型、过程、算法内容
        import PySystemicRiskLab.models.contents
        env['list_algorithm_contents'] = Tools.import_modules_from_package(env['folderpath_import_modules'], r"content_")

        ## 生成算法内容列表
        algorithmContents = env['list_algorithm_contents']

        ## 根据算法实体数据列表之数据，生成相应的算法实体对象，然后组成算法实体列表
        algorithmEntities = {}
        for entityData_name, entityData in env['list_entityData'].items():
            algorithmEntity = Entity(entityData)  # 构造每个实体
            algorithmEntities[entityData_name] = deepcopy(algorithmEntity)
            pass  # for

        ## 补充算法实体之特征
        for algorithmEntity in algorithmEntities.values():
            if algorithmEntity.attribute.content_name is None:
                algorithmEntity.attribute.content_name = algorithmEntity.content  # 内容名称`content_name`
            pass  # for

        ## 生成节点实体列表
        for algorithmEntity in algorithmEntities.values():
            nodeEntities = {}
            if algorithmEntity.container is not None:
                for node in algorithmEntity.container:
                    if node is not None:
                        ## 构建一个节点实体
                        nodeEntity = deepcopy(algorithmEntities[node['node']['content']])  # 先直接复制以继承该节点实体对应的算法实体之值，然后再改造
                        nodeEntity.attribute.id = None
                        nodeEntity.attribute.entity_name = node['node']['name']  # 设置节点之名称
                        nodeEntity.attribute.content_name = None
                        nodeEntity.attribute.text_name = None
                        nodeEntity.attribute.other['process_state'] = "has not process"  # 设置节点之处理状态
                        nodeEntity.process = node['node']['process']
                        nodeEntity.execute = None
                        nodeEntity.container = None
                        nodeEntity.content = node['node']['content']  # 设置节点之内容
                        ## 生成节点实体列表
                        nodeEntities[node['node']['name']] = nodeEntity
                        pass  # if
                    pass  # for
                ## 构建容器：将容器之值替换成节点实体字典列表之值
                algorithmEntity.container = nodeEntities
                del nodeEntities

                ## 构建过程：将过程之值改成箭头实体列表之值
                for node in algorithmEntity.container.values():
                    arrowEntities = []
                    if node.process is not None:
                        for idx_arrow, arrow in enumerate(node.process):
                            if arrow['arrow'] is not None:
                                arrowEntities.append(arrow['arrow'])
                        algorithmEntity.container[node.attribute.entity_name].process = arrowEntities
                        del arrowEntities
                    pass  # for

            pass  # for

        ## 装配箭头实体：将过程之箭头实体之方向之值链接至容器之对应的节点实体
        for algorithmEntity in algorithmEntities.values():
            if algorithmEntity.container is not None:
                for node in algorithmEntity.container.values():
                    if node.process is not None:
                        for arrow_value in node.process:
                            arrow_value['direction'] = algorithmEntity.container[arrow_value['direction']]
            pass  # for

        ## 装配节点实体：将容器之节点实体之内容之值链接至对应的算法实体
        for algorithmEntity in algorithmEntities.values():
            if algorithmEntity.container is not None:
                for node in algorithmEntity.container.values():
                    node.content = algorithmEntities[node.content]
            pass  # for

        ## 装配算法实体之内容：将算法实体之内容之值链接至对应的算法内容功能函数
        for algorithmEntity in algorithmEntities.values():
            if (
                    algorithmEntity.attribute.node_type == {"process node"} and
                    algorithmEntity.attribute.content_type == {"algorithm content"}
            ) or (
                    algorithmEntity.attribute.node_type == {"container node", "process node"} and
                    algorithmEntity.attribute.content_type == {"algorithm content"}
            ) or (
                    algorithmEntity.attribute.node_type == {"process node"} and
                    algorithmEntity.attribute.content_type == {"process content"}
            ) or (
                    algorithmEntity.attribute.node_type == {"container node", "process node"} and
                    algorithmEntity.attribute.content_type == {"model content"}
            ):
                if algorithmEntity.content is not None:
                    algorithmEntity.content = algorithmContents[algorithmEntity.content]
                    pass  # if
                pass  # if
            pass  # for

        ## 装配算法实体之执行器：将算法实体之执行器之值链接至对应的算法内容功能函数
        for algorithmEntity in algorithmEntities.values():
            if (
                    algorithmEntity.attribute.node_type == {"container node", "process node"} and
                    algorithmEntity.attribute.content_type == {"algorithm content"}
            ) or (
                    algorithmEntity.attribute.node_type == {"container node", "process node"} and
                    algorithmEntity.attribute.content_type == {"model content"}
            ) or (
                    algorithmEntity.attribute.node_type == {"process node"} and
                    algorithmEntity.attribute.content_type == {"process content"}
            ):
                if algorithmEntity.execute is not None:
                    algorithmEntity.execute = eval(algorithmEntity.execute)  # 设置执行器之值是处理机
                    pass  # if
                pass  # if
            if (
                    algorithmEntity.attribute.node_type == {"content node"} and
                    algorithmEntity.attribute.content_type == {"algorithm content"}
            ):
                algorithmEntity.execute = algorithmContents[algorithmEntity.execute]  # 设置执行器之值是具体的算法内容
                pass  # if
            pass  # for

        ## 生成模型节点实体（暨根节点实体，简称模型实体）字典列表
        modelEntities = {}
        for algorithmEntity in algorithmEntities.values():
            if algorithmEntity.attribute.content_type == {"model content"}:
                pattern = r'_'
                ## 构建一个节点实体
                modelEntity = deepcopy(algorithmEntity)  # 先直接复制以继承该节点实体对应的算法实体之值，然后再改造
                modelEntity.attribute.id = None
                modelEntity.attribute.entity_name = "entity_" + re.split(pattern, algorithmEntity.attribute.entity_name)[1]  # 设置节点之名称
                modelEntity.attribute.content_name = None
                modelEntity.attribute.text_name = None
                modelEntity.attribute.other['process_state'] = "has not process"  # 设置节点之处理状态
                modelEntity.process = None
                modelEntity.execute = None
                modelEntity.container = None
                modelEntity.content = algorithmEntity  # 设置节点之内容
                modelEntities[algorithmEntity.attribute.entity_name] = modelEntity
                pass  # if
            pass  # for

        return modelEntities
        pass  # method


    @classmethod
    def build_entity(cls, entityData: Any):  # HACK 无用
        """
        通过实体之数据构造实体对象

        Args:
            entityData: 实体数据

        Returns:
            entity: 实体对象（初始态）
        """
        entity = None
        str_build_specific_entity = "Entity(list_entityData)"
        entity = eval(str_build_specific_entity)
        return entity
        pass  # method

    pass  # class


