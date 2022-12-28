"""
模型构建机
"""

from PySystemicRiskLab import Any, deepcopy
from PySystemicRiskLab.core.define.define_type import EnvironmentVariableType
from PySystemicRiskLab.core.define.define_environment_variables import env
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.operations.processor import Processor  # HACK不能删除

pass  # end import


class ModelBuilder:
    """构造模型机"""

    @classmethod
    def build_entities(cls, env: EnvironmentVariableType = env):
        """
        构建实体众

        Args:
            env(EnvironmentVariableType): 环境变量集

        Returns:
            entities: 实体列表, contents: 内容列表

        """

        ## 导入相关模块（#HACK不能删除）
        import PySystemicRiskLab.models.entities_data  # 导入模型、过程、算法初始态实体之数据内容
        import PySystemicRiskLab.models.contents  # 导入模型、过程、算法内容

        ## 根据实体数据列表之数据，生成相应的实体对象，然后组成实体列表
        entities = {}
        for entityData_name, entityData in env['list_entityData'].items():
            entity = Entity(entityData)  # 构造每个实体
            entities[entityData_name] = deepcopy(entity)

        ## 生成内容列表
        contents = env['list_contents']

        ## 根据实体列表，将其之实体之内容改成实体对象数据格式与实际内容格式
        for entity_name, entity in entities.items():  # 遍历每个实体
            # pattern = r'\"(.*)\"'
            # repl = r""
            if entity.attribute.content_name is None:
                entity.attribute.content_name = entity.content  # 补充实体之特性之内容名称`content_name`
            if entity.container is not None:
                for idx_container_item, container_item in enumerate(entity.container):  # 遍历容器之每项之内容改成实体对象数据格式
                    entity.container[idx_container_item] = entities[container_item]
            if entity.process is not None:
                for idx_process_item, process_item in enumerate(entity.process):  # 遍历过程之每项之内容改成实体对象数据格式
                    if process_item['flow'] is not None:
                        process_item['flow'] = entities[process_item['flow']]
            if entity.content is not None:  # 遍历内容之每项之内容改成实体之内容对象数据格式
                if (entity.attribute.node_type == {"process node"} and entity.attribute.content_type == {"model content"}) or (entity.attribute.node_type == {"container node", "process node"} and entity.attribute.content_type == {"algorithm content"}):
                    entity.content = eval(entity.content)
                if entity.attribute.node_type == {"terminal node"} and entity.attribute.content_type == {"algorithm content"}:
                    entity.content = contents[entity.content]
                # entity.content = {entity.content: contents[entity.content]}

        # ## 根据实体列表之各实体之名称，生成相应的全局变量之于实体  #HACK 未生成，放弃
        # for entity_name, entity in entities.items():
        #     globals()[entity_name] = entity

        return entities, contents
        pass  # method

    @classmethod
    def build_entity(cls, entityData: Any):
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
