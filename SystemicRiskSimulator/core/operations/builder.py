"""
构建机
"""

from SystemicRiskSimulator.external_packages import Path
from SystemicRiskSimulator.core.define.define_type import SimulatorGlobalVariableType
from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv
from SystemicRiskSimulator.core.operations.entity_manager import EntityManager
from SystemicRiskSimulator.tools.tools import Tools

pass  # end import


class Builder:
    """构建机"""

    @classmethod
    def build_entities_by_execute(cls, sgv: SimulatorGlobalVariableType = sgv):
        """
        构建实体众，通过执行组件。这个适用于非流程版形式的模型实体。该方法无需编译流程。

        Args:
            sgv(SimulatorGlobalVariableType): 模拟器全局变量

        Returns:
            modelEntities: 模型实体（模型模板实体）列表, modelContents: 模型实体之内容（模型内容）列表

        """
        ## 导入相关模块
        ## 导入模型之初始态实体之数据内容（NOTE 动态导入）

        if sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is False:
            ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型 #DEBUG
            ### #NOTE 子方案一：自定义的模型内容与使用强化学习环境工具包自定义的环境模型分成两个文件 #DEBUG
            ## 导入实体之内容
            list_entityData = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/entities')), r"entity", sgv['folderpath_simulator'])
            ## 导入模型之内容（NOTE 动态导入）
            modelContents = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/contents')), r"content_", sgv['folderpath_simulator'])
            ## 导入使用强化学习环境工具包自定义的环境模型（NOTE 动态导入）
            modelEnvironment = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/env')), r"environment", sgv['folderpath_simulator'])
            ## 导入使用强化学习环境工具包自定义的运行过程（NOTE 动态导入）
            modelProcess = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/process')), r"process", sgv['folderpath_simulator'])

            ## 根据模型实体数据列表之数据，生成相应的模型实体对象，然后组成模型实体列表
            for entityData in list_entityData.values():
                EntityManager.create_entity(entityData=entityData)
                pass  # for

            # 补充模型实体之特征
            # for modelEntity in EntityManager.modelEntities.values():
            #     if modelEntity.attribute.content_name is None:
            #         modelEntity.attribute.content_name = modelEntity.content  # 内容名称`content_name`
            #     pass  # for

            ## 生成模型实体之实例（对应一个节点实体）
            for modelEntity in EntityManager.modelEntities.values():
                nodeEntities = {}
                if modelEntity.container is not None:
                    for node_name, node_value in modelEntity.container.items():
                        nodeEntity = EntityManager.create_entity()  # 构造一个空节点实体
                        nodeEntity.attribute.entity_name = node_name  # 设置节点实体之名称
                        nodeEntity.attribute.entity_type = {"instance entity"}  # 设置节点实体之实体类型
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

            ## 装配模型实体之执行器、内容器之值链接至对应的模型内容功能函数
            for modelEntity in EntityManager.modelEntities.values():
                if (
                        modelEntity.attribute.entity_type == {"template entity"} and
                        modelEntity.attribute.structure_type == {"content structure"} and
                        modelEntity.attribute.container_type == {"root container"} and
                        modelEntity.attribute.process_type == {"executive process"} and
                        modelEntity.attribute.content_type == {"model content"}
                ):
                    # modelEntity.execute = dict()
                    # modelEntity.execute['model'] = modelContents[modelEntity.execute]  # 设置执行器之值是具体的模型内容
                    # modelEntity.execute['finance'] = modelContents[modelEntity.content]  # 设置执行器之值是具体的模型内容
                    modelEntity.content = modelContents  # 设置内容器之值是具体的模型相关的功能函数
                    # modelEntity.content = modelContents[modelEntity.content]  # 设置内容器之值是具体的模型相关的功能函数
                    modelEntity.environment = modelEnvironment[modelEntity.environment]  # 设置环境之值是具体的模型相关的功能函数
                    modelEntity.process = modelProcess[modelEntity.process]  # 设置运作器之值是具体的模型相关的功能函数
                    pass  # if
                pass  # for

            ## 生成模型实例实体用于存放对应的主模型实体
            for mainModelTemplateEntity in EntityManager.mainModelTemplateEntities.values():
                mainModelInstanceEntity_name = mainModelTemplateEntity.attribute.entity_name
                mainModelInstanceEntity = EntityManager.create_entity(entity_name='model_' + mainModelInstanceEntity_name, entity_type={"instance entity"}, structure_type={"container structure", "process structure"}, container_type={"root container"}, process_type={"executive process"}, content_type={"model content", "node content"})  # 构造一个空实体
                mainModelInstanceEntity.content = mainModelTemplateEntity  # 设置模型实例实体之内容组件为主模型实体
                pass  # for

        elif sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is True:
            ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型 #DEBUG
            ### #NOTE 子方案一：自定义的模型内容与使用强化学习环境工具包自定义的环境模型分成两个文件 #DEBUG
            ## 导入实体之内容
            list_entityData = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/entities')), r"entity", sgv['folderpath_simulator'])
            ## 导入模型之内容（NOTE 动态导入）
            modelContents = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/contents')), r"content_", sgv['folderpath_simulator'])
            ## 导入使用强化学习环境工具包自定义的环境模型（NOTE 动态导入）
            # modelEnvironment = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/env')), r"Environment|Train", sgv['folderpath_simulator'])
            modelEnvironment = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/env')), r"environment", sgv['folderpath_simulator'])
            ## 导入使用强化学习算法工具包自定义的算法模型（NOTE 动态导入）
            modelAlgorithm = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/algorithm')), r"train", sgv['folderpath_simulator'])
            ## 导入使用强化学习环境工具包自定义的运行过程（NOTE 动态导入）
            modelProcess = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/process')), r"process", sgv['folderpath_simulator'])
            # ### #NOTE 子方案二：自定义的模型内容与使用强化学习环境工具包自定义的环境模型合在一个类里面 #HACK 这个方案暂时无用，也没有实现。
            # ## 导入实体之内容
            # list_entityData = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/entities')), r"entity_", sgv['folderpath_simulator'])
            # ## 导入模型之内容类（使用强化学习环境工具包自定义的）（NOTE 动态导入）
            # modelContents = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/gym_model')), r"gym_model_", sgv['folderpath_simulator'])

            ## 根据模型实体数据列表之数据，生成相应的模型实体对象，然后组成模型实体列表
            for entityData in list_entityData.values():
                EntityManager.create_entity(entityData=entityData)
                pass  # for

            # 补充模型实体之特征
            # for modelEntity in EntityManager.modelEntities.values():
            #     if modelEntity.attribute.content_name is None:
            #         modelEntity.attribute.content_name = modelEntity.content  # 内容名称`content_name`
            #     pass  # for

            ## 生成模型实体之实例（对应一个节点实体）
            for modelEntity in EntityManager.modelEntities.values():
                nodeEntities = {}
                if modelEntity.container is not None:
                    for node_name, node_value in modelEntity.container.items():
                        nodeEntity = EntityManager.create_entity()  # 构造一个空节点实体
                        nodeEntity.attribute.entity_name = node_name  # 设置节点实体之名称
                        nodeEntity.attribute.entity_type = {"instance entity"}  # 设置节点实体之实体类型
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

            ## 装配模型实体之执行器、内容器之值链接至对应的模型内容功能函数
            for modelEntity in EntityManager.modelEntities.values():
                if (
                        modelEntity.attribute.entity_type == {"template entity"} and
                        modelEntity.attribute.structure_type == {"content structure"} and
                        modelEntity.attribute.container_type == {"root container"} and
                        modelEntity.attribute.process_type == {"executive process"} and
                        modelEntity.attribute.content_type == {"model content"}
                ):
                    # modelEntity.execute = dict()
                    # modelEntity.execute['model'] = modelContents[modelEntity.execute]  # 设置执行器之值是具体的模型内容
                    # modelEntity.execute['finance'] = modelContents[modelEntity.content]  # 设置执行器之值是具体的模型内容
                    modelEntity.content = modelContents  # 设置内容器之值是具体的模型相关的功能函数
                    # modelEntity.content = modelContents[modelEntity.content]  # 设置内容器之值是具体的模型相关的功能函数
                    # modelEntity.environment = modelEnvironment  # 设置环境之值是具体的模型相关的功能函数
                    modelEntity.environment = modelEnvironment[modelEntity.environment]  # 设置环境之值是具体的模型相关的功能函数
                    modelEntity.algorithm = modelAlgorithm[modelEntity.algorithm]  # 设置算法之值是具体的模型相关的功能函数
                    modelEntity.process = modelProcess[modelEntity.process]  # 设置运作器之值是具体的模型相关的功能函数
                    pass  # if
                pass  # for

            ## 生成模型实例实体用于存放对应的主模型实体
            for mainModelTemplateEntity in EntityManager.mainModelTemplateEntities.values():
                mainModelInstanceEntity_name = mainModelTemplateEntity.attribute.entity_name
                mainModelInstanceEntity = EntityManager.create_entity(entity_name='model_' + mainModelInstanceEntity_name, entity_type={"instance entity"}, structure_type={"container structure", "process structure"}, container_type={"root container"}, process_type={"executive process"}, content_type={"model content", "node content"})  # 构造一个空实体
                mainModelInstanceEntity.content = mainModelTemplateEntity  # 设置模型实例实体之内容组件为主模型实体
                pass  # for

        else:
            ## NOTE 如果使用模拟器自带的模型，不使用使用强化学习环境工具包自定义的模型 #DEBUG
            ## 导入实体之内容
            list_entityData = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/entities')), r"entity_", sgv['folderpath_simulator'])
            ## 导入模型之内容（NOTE 动态导入）
            modelContents = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/models/contents')), r"content_", sgv['folderpath_simulator'])
            ## 根据模型实体数据列表之数据，生成相应的模型实体对象，然后组成模型实体列表
            for entityData in list_entityData.values():
                EntityManager.create_entity(entityData=entityData)  # 根据实体数据，创建每个实体
                pass  # for

            # 补充模型实体之特征
            # for modelEntity in EntityManager.modelEntities.values():
            #     if modelEntity.attribute.content_name is None:
            #         modelEntity.attribute.content_name = modelEntity.content  # 内容名称`content_name`
            #     pass  # for

            ## 生成模型实体之实例（对应一个节点实体）
            for modelEntity in EntityManager.modelEntities.values():
                nodeEntities = {}
                if modelEntity.container is not None:
                    for node_name, node_value in modelEntity.container.items():
                        nodeEntity = EntityManager.create_entity()  # 构造一个空节点实体
                        nodeEntity.attribute.entity_name = node_name  # 设置节点实体之名称
                        nodeEntity.attribute.entity_type = {"instance entity"}  # 设置节点实体之实体类型
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

            ## 装配模型实体之执行器、内容器之值链接至对应的模型内容功能函数
            for modelEntity in EntityManager.modelEntities.values():
                if (
                        modelEntity.attribute.entity_type == {"template entity"} and
                        modelEntity.attribute.structure_type == {"content structure"} and
                        modelEntity.attribute.container_type == {"root container"} and
                        modelEntity.attribute.process_type == {"executive process"} and
                        modelEntity.attribute.content_type == {"model content"}
                ):
                    # modelEntity.execute = dict()
                    # modelEntity.execute['model'] = modelContents[modelEntity.execute]  # 设置执行器之值是具体的模型内容
                    # modelEntity.execute['finance'] = modelContents[modelEntity.content]  # 设置执行器之值是具体的模型内容
                    modelEntity.execute = modelContents[modelEntity.execute]  # 设置执行器之值是具体的模型内容
                    modelEntity.content = modelContents[modelEntity.content]  # 设置内容器之值是具体的模型相关的功能函数
                    pass  # if
                pass  # for

            ## 生成模型实例实体用于存放对应的主模型实体
            for mainModelTemplateEntity in EntityManager.mainModelTemplateEntities.values():
                mainModelInstanceEntity_name = mainModelTemplateEntity.attribute.entity_name
                mainModelInstanceEntity = EntityManager.create_entity(entity_name='model_' + mainModelInstanceEntity_name, entity_type={"instance entity"}, structure_type={"container structure", "process structure"}, container_type={"root container"}, process_type={"executive process"}, content_type={"model content", "node content"})  # 构造一个空实体
                mainModelInstanceEntity.content = mainModelTemplateEntity  # 设置模型实例实体之内容组件为主模型实体
                pass  # for

            pass  # if

        pass  # function

    pass  # class
