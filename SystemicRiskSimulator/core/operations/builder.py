"""
构建机
"""

from SystemicRiskSimulator import Any, deepcopy, re
from SystemicRiskSimulator.core.define.define_type import EnvironmentVariableType
from SystemicRiskSimulator.core.define.define_environmentVariables import env
from SystemicRiskSimulator.core.operations.entity_manager import EntityManager
from SystemicRiskSimulator.core.operations.compiler import Compiler
from SystemicRiskSimulator.core.operations.processor import Processor  # NOTE 动态导入，严禁删除
from SystemicRiskSimulator.tools.tools import Tools

pass  # end import


class Builder:
    """构建机"""

    @classmethod
    def build_entities_by_process_and_container_component(cls, env: EnvironmentVariableType = env):
        """
        构建实体众，通过过程与容器组件。

        Args:
            env(EnvironmentVariableType): 环境变量集

        Returns:
            algorithmEntities: 算法实体列表, algorithmContents: 算法内容列表

        """
        ## 导入相关模块（#NOTE 动态导入，严禁删除）
        ## 导入模型、过程、算法初始态实体之数据内容
        import SystemicRiskSimulator.models.entities_data
        list_entityData = Tools.import_modules_from_package(env['folderpath_import_modules'], r"entityData_")

        ## 导入模型、过程、算法内容
        import SystemicRiskSimulator.models.contents
        algorithmContents = Tools.import_modules_from_package(env['folderpath_import_modules'], r"content_")

        ## 根据算法实体数据列表之数据，生成相应的算法实体对象，然后组成算法实体列表
        for entityData in list_entityData.values():
            EntityManager.create_entity(entityData=entityData)  # 根据实体数据，创建每个实体
            pass  # for

        ## 补充算法实体之特征
        for algorithmEntity in EntityManager.algorithmEntities.values():
            if algorithmEntity.attribute.content_name is None:
                algorithmEntity.attribute.content_name = algorithmEntity.content  # 内容名称`content_name`
            pass  # for

        ## 补充模型算法实体之特征
        for modelAlgorithmEntity in EntityManager.modelAlgorithmEntities.values():
            modelAlgorithmEntity.attribute.other['process_state'] = "has not process"  # 设置节点之处理状态

        ## 生成算法实体之节点实体
        for algorithmEntity in EntityManager.algorithmEntities.values():
            nodeEntities = {}
            if algorithmEntity.container is not None:
                for node_name, node_value in algorithmEntity.container.items():
                    nodeEntity = EntityManager.create_entity()  # 构造一个空节点实体
                    nodeEntity.attribute.entity_name = node_name  # 设置节点实体之名称
                    nodeEntity.attribute.node_type = {"container node"}  # 设置节点实体之节点类型
                    nodeEntity.attribute.content_type = {"node content"}  # 设置节点实体之内容类型
                    if nodeEntity.content is None:
                        nodeEntity.content = node_value  # 设置节点实体之内容组件。此时，其内容为算法实体之字符串数据，需要进一步装配。#BUG 是否应该放在content而不是execute？
                        pass  # if
                    nodeEntities[node_name] = nodeEntity  # 生成节点实体字典列表
                    pass  # for
                algorithmEntity.container = nodeEntities  # 构建节点：将节点组件之值替换成节点实体字典列表之值
                pass  # if
            pass  # for

        ## 装配算法实体之节点实体之内容组件
        for algorithmEntity in EntityManager.algorithmEntities.values():
            if (
                    algorithmEntity.attribute.node_type == {"container node", "process node"} and
                    algorithmEntity.attribute.content_type == {"algorithm content"}
            ) or (
                    algorithmEntity.attribute.node_type == {"container node", "process node"} and
                    algorithmEntity.attribute.content_type == {"model content", "algorithm content"}
            ):
                for nodeEntity in algorithmEntity.container.values():
                    # if not (nodeEntity.content is None or nodeEntity.content is 'entity_START' or nodeEntity.content is 'entity_END'):
                    if nodeEntity.content is not None:
                        nodeEntity.content = EntityManager.algorithmEntities[nodeEntity.content]
                        pass  # if
                    pass  # for
                continue
                pass  # if
            pass  # for

        ## 生成算法实体之条件实体
        for algorithmEntity in EntityManager.algorithmEntities.values():
            conditionEntities = {}
            if algorithmEntity.condition is not None:
                for condition_name, condition_value in algorithmEntity.condition.items():
                    conditionEntity = EntityManager.create_entity()  # 构造一个空条件实体
                    conditionEntity.attribute.entity_name = condition_name  # 设置条件实体之名称
                    nodeEntity.attribute.node_type = {"condition node"}  # 设置条件实体之节点类型
                    if conditionEntity.content is None:
                        conditionEntity.content = condition_value  # 设置条件实体之内容组件。此时其内容为表达式字符串数据，需要进一步解析。 #BUG 是否应该放在content而不是execute？
                        pass  # if
                    conditionEntities[condition_name] = conditionEntity  # 生成条件实体字典列表
                    pass  # for
                algorithmEntity.condition = conditionEntities  # 构建条件：将条件组件之值替换成条件实体字典列表之值
                pass  # if
            pass  # for

        ## 装配算法实体之执行器：将算法实体之执行器之值链接至对应的算法内容功能函数
        for algorithmEntity in EntityManager.algorithmEntities.values():
            if (
                    algorithmEntity.attribute.node_type == {"container node", "process node"} and
                    algorithmEntity.attribute.content_type == {"algorithm content"}
            ) or (
                    algorithmEntity.attribute.node_type == {"container node", "process node"} and
                    algorithmEntity.attribute.content_type == {"model content", "algorithm content"}
            ) or (
                    algorithmEntity.attribute.node_type == {"process node"} and
                    algorithmEntity.attribute.content_type == {"process content"}
            ):
                if algorithmEntity.execute is not None:
                    algorithmEntity.execute = eval(algorithmEntity.execute)  # 设置执行器之值是处理机 #BUG 是否有必要继续用处理机处理？
                    pass  # if
                pass  # if
            if (
                    algorithmEntity.attribute.node_type == {"content node"} and
                    algorithmEntity.attribute.content_type == {"algorithm content"}
            ):
                algorithmEntity.execute = algorithmContents[algorithmEntity.execute]  # 设置执行器之值是具体的算法内容
                pass  # if
            pass  # for

        ## 装配算法实体之过程组件
        for algorithmEntity in EntityManager.algorithmEntities.values():
            if algorithmEntity.process is not None:
                algorithmEntity.process = algorithmContents[algorithmEntity.process]
                pass  # if
            pass  # for

        ## 生成模型节点实体（模型实体）用于存放对应的模型算法实体
        for modelAlgorithmEntity in EntityManager.modelAlgorithmEntities.values():
            modelEntity_name = modelAlgorithmEntity.attribute.entity_name
            modelEntity = EntityManager.create_entity(entity_name='model_' + modelEntity_name, node_type={"container node"}, content_type={"model content", "node content"})  # 构造一个空实体
            modelEntity.content = modelAlgorithmEntity  # 设置模型节点实体之内容组件为模型算法实体

        ## 装配模型算法实体之过程组件
        ## 编译模型算法实体。
        ## 编译过程会自动编译主程序相关的各子程序过程。最终生成一个可执行的主程序过程，然后装配到模型算法实体之过程组件。
        for modelEntity in EntityManager.modelEntities.values():
            compile_process = Compiler.compile(modelEntity)
            modelAlgorithmEntity = modelEntity.content
            modelAlgorithmEntity.process = compile_process
            pass  # for

        pass  # function

    @classmethod
    def build_entities_by_node_component(cls, env: EnvironmentVariableType = env):  # FIXME 已经过时
        """
        构建实体众，通过节点组件。#HACK暂时不用。还没有适配新版。以后可能会改造或者删除

        Args:
            env(EnvironmentVariableType): 环境变量集

        Returns:
            algorithmEntities: 算法实体列表, algorithmContents: 算法内容列表

        """

        ## 导入相关模块（#NOTE 动态导入，严禁删除）
        ## 导入模型、过程、算法初始态实体之数据内容
        import SystemicRiskSimulator.models.entities_data
        env['list_entityData'] = Tools.import_modules_from_package(env['folderpath_import_modules'], r"entityData_")
        ## 导入模型、过程、算法内容
        import SystemicRiskSimulator.models.contents
        env['list_algorithm_contents'] = Tools.import_modules_from_package(env['folderpath_import_modules'], r"content_")

        ## 生成算法内容列表
        algorithmContents = env['list_algorithm_contents']

        ## 根据算法实体数据列表之数据，生成相应的算法实体对象，然后组成算法实体列表
        algorithmEntities = {}
        for entityData_name, entityData in env['list_entityData'].items():
            algorithmEntity = EntityManager.create_entity(entityData=entityData)  # 构造每个实体
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
            if algorithmEntity.node is not None:
                for node in algorithmEntity.node:
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
                        nodeEntity.node = None
                        nodeEntity.content = node['node']['content']  # 设置节点之内容
                        ## 生成节点实体列表
                        nodeEntities[node['node']['name']] = nodeEntity
                        pass  # if
                    pass  # for
                ## 构建节点组件：将节点组件之值替换成节点实体字典列表之值
                algorithmEntity.node = nodeEntities
                del nodeEntities

                ## 构建过程：将过程之值改成箭头实体列表之值
                for node in algorithmEntity.node.values():
                    arrowEntities = []
                    if node.process is not None:
                        for idx_arrow, arrow in enumerate(node.process):
                            if arrow['arrow'] is not None:
                                arrowEntities.append(arrow['arrow'])
                        algorithmEntity.node[node.attribute.entity_name].process = arrowEntities
                        del arrowEntities
                    pass  # for

            pass  # for

        ## 装配箭头实体：将过程之箭头实体之方向之值链接至节点组件之对应的节点实体
        for algorithmEntity in algorithmEntities.values():
            if algorithmEntity.node is not None:
                for node in algorithmEntity.node.values():
                    if node.process is not None:
                        for arrow_value in node.process:
                            arrow_value['direction'] = algorithmEntity.node[arrow_value['direction']]
            pass  # for

        ## 装配节点实体：将节点组件之节点实体之内容之值链接至对应的算法实体
        for algorithmEntity in algorithmEntities.values():
            if algorithmEntity.node is not None:
                for node in algorithmEntity.node.values():
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
                    algorithmEntity.attribute.content_type == {"model content", "algorithm content"}
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
                    algorithmEntity.attribute.content_type == {"model content", "algorithm content"}
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
            if algorithmEntity.attribute.content_type == {"model content", "algorithm content"}:
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
                modelEntity.node = None
                modelEntity.content = algorithmEntity  # 设置节点之内容
                modelEntities[algorithmEntity.attribute.entity_name] = modelEntity
                pass  # if
            pass  # for

        return modelEntities
        pass  # function

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
        pass  # function

    pass  # class
