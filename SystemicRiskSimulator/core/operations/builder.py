"""
构建机
"""

from SystemicRiskSimulator import Any, deepcopy, re
from SystemicRiskSimulator.core.define.define_type import EnvironmentVariableType
from SystemicRiskSimulator.core.define.define_environmentVariables import env
from SystemicRiskSimulator.core.operations.entity_manager import EntityManager
from SystemicRiskSimulator.core.operations.compiler import Compiler
from SystemicRiskSimulator.core.operations.processor import Processor  # NOTE 动态导入，严禁删除。如果 IDE 报错，是正常的。因为这个是在程序运行时动态导入。
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
            modelEntities: 模型实体（模型模板实体）列表, modelContents: 模型实体之内容（模型内容）列表

        """
        ## 导入相关模块（#NOTE 动态导入，严禁删除。如果 IDE 报错，是正常的。因为这个是在程序运行时动态导入。）
        ## 导入模型之初始态实体之数据内容
        import SystemicRiskSimulator.models.entities_data
        list_entityData = Tools.import_modules_from_package(env['folderpath_import_modules'], r"entityData_", env['folderpath_project'])

        ## 导入模型之内容
        import SystemicRiskSimulator.models.contents
        modelContents = Tools.import_modules_from_package(env['folderpath_import_modules'], r"content_", env['folderpath_project'])

        ## 根据模型实体数据列表之数据，生成相应的模型实体对象，然后组成模型实体列表
        for entityData in list_entityData.values():
            EntityManager.create_entity(entityData=entityData)  # 根据实体数据，创建每个实体
            pass  # for

        ## 补充模型实体之特征
        for modelEntity in EntityManager.modelEntities.values():
            if modelEntity.attribute.content_name is None:
                modelEntity.attribute.content_name = modelEntity.content  # 内容名称`content_name`
            pass  # for

        ## 补充主模型实体之特征
        for mainModelInstanceEntity in EntityManager.mainModelTemplateEntities.values():
            mainModelInstanceEntity.attribute.other['process_state'] = "has not process"  # 设置节点之处理状态

        ## 生成模型实体之实例（对应一个节点实体）
        for modelEntity in EntityManager.modelEntities.values():
            nodeEntities = {}
            if modelEntity.container is not None:
                for node_name, node_value in modelEntity.container.items():
                    nodeEntity = EntityManager.create_entity()  # 构造一个空节点实体
                    nodeEntity.attribute.entity_name = node_name  # 设置节点实体之名称
                    nodeEntity.attribute.structure_type = {"content structure"}  # 设置节点实体之结构类型
                    nodeEntity.attribute.content_type = {"node content"}  # 设置节点实体之内容类型
                    if nodeEntity.content is None:
                        nodeEntity.content = node_value  # 设置节点实体之内容组件。此时，其内容为模型实体之字符串数据，需要进一步装配。#BUG 是否应该放在content而不是execute？
                        pass  # if
                    nodeEntities[node_name] = nodeEntity  # 生成节点实体字典列表
                    pass  # for
                modelEntity.container = nodeEntities  # 构建节点：将节点组件之值替换成节点实体字典列表之值
                pass  # if
            pass  # for

        ## 装配模型实体之实例之内容组件
        for modelEntity in EntityManager.modelEntities.values():
            if (
                    modelEntity.attribute.entity_type == {"template entity"} and
                    modelEntity.attribute.structure_type == {"container structure", "process structure"} and
                    modelEntity.attribute.container_type == {"branch container"} and
                    modelEntity.attribute.process_type == {"executive process"} and
                    modelEntity.attribute.content_type == {"model content"}
            ) or (
                    modelEntity.attribute.entity_type == {"template entity"} and
                    modelEntity.attribute.structure_type == {"container structure", "process structure"} and
                    modelEntity.attribute.container_type == {"root container"} and
                    modelEntity.attribute.process_type == {"executive process"} and
                    modelEntity.attribute.content_type == {"model content"}
            ):
                for nodeEntity in modelEntity.container.values():
                    if nodeEntity.content is not None:
                        nodeEntity.content = EntityManager.modelEntities[nodeEntity.content]
                        pass  # if
                    pass  # for
                continue
                pass  # if
            pass  # for

        ## 生成模型实体之条件实体
        for modelEntity in EntityManager.modelEntities.values():
            conditionEntities = {}
            if modelEntity.condition is not None:
                for condition_name, condition_value in modelEntity.condition.items():
                    conditionEntity = EntityManager.create_entity()  # 构造一个空条件实体
                    conditionEntity.attribute.entity_name = condition_name  # 设置条件实体之名称
                    nodeEntity.attribute.content_type = {"condition content"}  # 设置条件实体之节点类型
                    if conditionEntity.content is None:
                        conditionEntity.content = condition_value  # 设置条件实体之内容组件。此时其内容为表达式字符串数据，需要进一步解析。 #BUG 是否应该放在content而不是execute？
                        pass  # if
                    conditionEntities[condition_name] = conditionEntity  # 生成条件实体字典列表
                    pass  # for
                modelEntity.condition = conditionEntities  # 构建条件：将条件组件之值替换成条件实体字典列表之值
                pass  # if
            pass  # for

        ## 装配模型实体之执行器：将模型实体之执行器之值链接至对应的模型内容功能函数
        for modelEntity in EntityManager.modelEntities.values():
            if (
                    modelEntity.attribute.entity_type == {"template entity"} and
                    modelEntity.attribute.structure_type == {"container structure", "process structure"} and
                    modelEntity.attribute.container_type == {"branch container"} and
                    modelEntity.attribute.process_type == {"executive process"} and
                    modelEntity.attribute.content_type == {"model content"}
            ) or (
                    modelEntity.attribute.entity_type == {"template entity"} and
                    modelEntity.attribute.structure_type == {"container structure", "process structure"} and
                    modelEntity.attribute.container_type == {"root container"} and
                    modelEntity.attribute.process_type == {"executive process"} and
                    modelEntity.attribute.content_type == {"model content"}
            ) or (
                    modelEntity.attribute.entity_type == {"template entity"} and
                    modelEntity.attribute.structure_type == {"process structure"} and
                    modelEntity.attribute.container_type == {"leaf container"} and
                    modelEntity.attribute.process_type == {"schedule process"} and
                    modelEntity.attribute.content_type == {"model content"}
            ):
                if modelEntity.execute is not None:
                    modelEntity.execute = eval(modelEntity.execute)  # 设置执行器之值是处理机 #BUG 是否有必要继续用处理机处理？
                    pass  # if
                pass  # if
            if (
                    modelEntity.attribute.entity_type == {"template entity"} and
                    modelEntity.attribute.structure_type == {"content structure"} and
                    modelEntity.attribute.container_type == {"leaf container"} and
                    modelEntity.attribute.process_type == {"executive process"} and
                    modelEntity.attribute.content_type == {"model content"}
            ):
                modelEntity.execute = modelContents[modelEntity.execute]  # 设置执行器之值是具体的模型内容
                pass  # if
            pass  # for

        ## 装配模型实体之过程组件
        for modelEntity in EntityManager.modelEntities.values():
            if modelEntity.process is not None:
                modelEntity.process = modelContents[modelEntity.process]
                pass  # if
            pass  # for

        ## 生成模型实例实体用于存放对应的主模型实体
        for mainModelTemplateEntity in EntityManager.mainModelTemplateEntities.values():
            mainModelInstanceEntity_name = mainModelTemplateEntity.attribute.entity_name
            mainModelInstanceEntity = EntityManager.create_entity(entity_name='model_' + mainModelInstanceEntity_name, entity_type={"instance entity"}, structure_type={"container structure", "process structure"}, container_type={"root container"}, process_type={"executive process"}, content_type={"model content", "node content"})  # 构造一个空实体
            mainModelInstanceEntity.content = mainModelTemplateEntity  # 设置模型实例实体之内容组件为主模型实体

        ## 装配主模型实体之过程组件
        ## 编译主模型实体。
        ## 编译过程会自动编译主程序相关的各子程序过程。最终生成一个可执行的主程序过程，然后装配到主模型实体之过程组件。
        for mainModelInstanceEntity in EntityManager.mainModelInstanceEntities.values():
            compile_process = Compiler.compile(mainModelInstanceEntity)
            mainModelTemplateEntity = mainModelInstanceEntity.content
            mainModelTemplateEntity.process = compile_process
            pass  # for

        pass  # function


    pass  # class
