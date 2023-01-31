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
        # env['list_algorithm_contents'] =Tools.import_modules_from_package(env['folderpath_project']+'/PySystemicRiskLab/models/contents')

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
            # nodeEntity = Entity(entityData)
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

                # ## 构建过程：将过程之内容改成箭头实体字典列表之内容 #HACK 废弃字典形式，改成列表形式
                # for node in algorithmEntity.container.values():
                #     arrowEntities = {}
                #     if node.process is not None:
                #         for idx_arrow, arrow in enumerate(node.process):
                #             if arrow['arrow'] is not None:
                #                 arrow_name = "arrow_" + idx_arrow.__str__()
                #                 arrow['arrow']['name'] = arrow_name  # 补充name信息
                #                 arrowEntities[arrow['arrow']['name']] = arrow['arrow']
                #         algorithmEntity.container[node.attribute.entity_name].process = arrowEntities
                #         del arrowEntities

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

        # ## 装配算法实体之节点：将算法实体之节点之值链接至对应的同层的节点实体
        # for algorithmEntity in algorithmEntities.values():
        #     if (
        #             algorithmEntity.attribute.node_type == {"container node", "process node"} and
        #             algorithmEntity.attribute.content_type == {"algorithm content"}
        #     ) or (
        #             algorithmEntity.attribute.node_type == {"content node"} and
        #             algorithmEntity.attribute.content_type == {"algorithm content"}
        #     ) or (
        #             algorithmEntity.attribute.node_type == {"process node"} and
        #             algorithmEntity.attribute.content_type == {"process content"}
        #     ):
        #         if algorithmEntity.node is None:
        #             algorithmEntity.node = nodeEntity  # 算法实体指向对应的节点实体
        #             pass  # if
        #         pass  # if
        #     if (
        #             algorithmEntity.attribute.node_type == {"container node", "process node"} and
        #             algorithmEntity.attribute.content_type == {"model content"}
        #     ):
        #         if algorithmEntity.node is None:
        #             algorithmEntity.node = nodeEntity  # 算法实体指向对应的节点实体
        #             pass  # if
        #         pass  # if
        #         algorithmEntity.execute = algorithmContents[algorithmEntity.execute]
        #     pass  # for

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

    # @classmethod #HACK旧的后续可删除
    # def build_entities(cls, env: EnvironmentVariableType = env):
    #     """
    #     构建实体众
    #
    #     Args:
    #         env(EnvironmentVariableType): 环境变量集
    #
    #     Returns:
    #         entities: 实体列表, contents: 内容列表
    #
    #     """
    #
    #     ## 导入相关模块（#NOTE 动态导入，严禁删除）
    #     ## 导入模型、过程、算法初始态实体之数据内容
    #     import PySystemicRiskLab.models.entities_data
    #     env['list_entityData'] = Tools.import_modules_from_package(env['folderpath_import_modules'], r"entityData_")
    #     ## 导入模型、过程、算法内容
    #     import PySystemicRiskLab.models.contents
    #     env['list_algorithm_contents'] = Tools.import_modules_from_package(env['folderpath_import_modules'], r"content_")
    #     # env['list_algorithm_contents'] =Tools.import_modules_from_package(env['folderpath_project']+'/PySystemicRiskLab/models/contents')
    #
    #     ## 根据实体数据列表之数据，生成相应的实体对象，然后组成实体列表
    #     entities = {}
    #     for entityData_name, entityData in env['list_entityData'].items():
    #         entity = Entity(entityData)  # 构造每个实体
    #         entities[entityData_name] = deepcopy(entity)
    #
    #     ## 生成内容列表
    #     contents = env['list_algorithm_contents']
    #
    #     ## 根据实体列表，将其之实体之内容改成实体对象数据格式与实际内容格式
    #     for entity_name, entity in entities.items():  # 遍历每个实体
    #         # pattern = r'\"(.*)\"'
    #         # repl = r""
    #         if entity.attribute.content_name is None:
    #             entity.attribute.content_name = entity.content  # 补充实体之特性之内容名称`content_name`
    #         if entity.container is not None:
    #             for idx_container_item, container_item in enumerate(entity.container):  # 遍历容器之每项之内容改成实体对象数据格式
    #                 entity.container[idx_container_item] = entities[container_item]
    #         if entity.process is not None:
    #             for idx_process_item, process_item in enumerate(entity.process):  # 遍历过程之每项之内容改成实体对象数据格式
    #                 if process_item['flow'] is not None:
    #                     process_item['flow'] = entities[process_item['flow']]
    #         if entity.content is not None:  # 遍历内容之每项之内容改成实体之内容对象数据格式
    #             if (entity.attribute.node_type == {"process node"} and entity.attribute.content_type == {"model content"}) or (entity.attribute.node_type == {"container node", "process node"} and entity.attribute.content_type == {"algorithm content"}):
    #                 entity.content = eval(entity.content)
    #             if entity.attribute.node_type == {"terminal node"} and entity.attribute.content_type == {"algorithm content"}:
    #                 entity.content = contents[entity.content]
    #             # entity.content = {entity.content: contents[entity.content]}
    #
    #     # ## 根据实体列表之各实体之名称，生成相应的全局变量之于实体  #HACK 未生成，放弃
    #     # for entity_name, entity in entities.items():
    #     #     globals()[entity_name] = entity
    #
    #     return entities, contents
    #     pass  # method

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

    @classmethod
    def build_process(cls, entityData: Any):  # TODO
        pass
