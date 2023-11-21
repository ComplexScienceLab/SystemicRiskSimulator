"""
安装模型机
"""

from SystemicRiskSimulator import deepcopy, re
from SystemicRiskSimulator.core.define.define_entity import Entity
from SystemicRiskSimulator.core.operations.entity_manager import EntityManager
from SystemicRiskSimulator.core.define.define_environmentVariables import env
from SystemicRiskSimulator.core.define.define_parameterVariables import para
from SystemicRiskSimulator.core.operations.builder import Builder
from SystemicRiskSimulator.tools.tools import Tools

pass  # end import


class ModelInstaller:
    """安装模型机"""

    @classmethod
    def install_model(cls):
        """
        安装模型

        Returns:
            models: 模型字典集
        """
        ## 构建、安装本次实验组所需的所有模型

        ## 复制模型数据与内容到`SystemicRiskSimulator/models`文件夹下
        Tools._delete_and_recreate_folder("SystemicRiskSimulator/models", is_auto_confirmation=False)
        Tools.copy_files_from_other_folders(env['folderpath_models'], "SystemicRiskSimulator/models")

        ## 导入实体数据，生成实体集、内容集并返回
        # entities = Builder.build_entities_by_node_component(env) #BUG还未适配，暂时用不到
        entities = Builder.build_entities_by_process_and_container_component(env)

        ## 生成待运行的模型列表
        return EntityManager.modelEntities

        pass  # function

    @classmethod
    def build_postorder_traversial(cls, modelEntity: Entity):
        """
        根据已经生成的模型，生成遍历序列，用于后序遍历所有节点。 #HACK 暂时还没有用到

        Args:
            modelEntity: 模型实体

        Returns: result 结果遍历序列

        """
        stack_entity = []  # 定义一个栈，存储实体
        stack_entity.append(modelEntity)  # 入栈根实体，即模型实体
        queue_entities = {}  # 定义一个字典序列，存储实体遍历顺序
        if modelEntity != None:
            stack_entity.append(modelEntity)
        while not len(stack_entity) == 0:
            entity: Entity = stack_entity[-1]
            if entity is not None:  # 只有当实体节点不是空时，才将子节点入栈
                stack_entity.pop()  # 将该节点弹出，避免重复操作，下面再将右中左节点添加到栈中
                stack_entity.append(entity)  # 添加根节点（空节点不入栈）
                stack_entity.append(None)  # 根节点被访问过，但是还没有处理，加入空节点做为标记。
                sub_nodes = deepcopy(entity.container)  # 获取实体容器之子节点
                sub_nodes.reverse()  # 反序子节点 #FIXME运行出错AttributeError: 'NoneType' object has no attribute 'reverse'
                for sub_node in sub_nodes:  # 入栈子节点（不入栈空节点）
                    if sub_node is not None:
                        stack_entity.append(sub_node)
            else:  # 只有遇到空节点的时候，才放下一个节点进结果序列
                stack_entity.pop()  # 弹出空节点
                entity = stack_entity.pop()  # 重新取出栈里的节点
                queue_entities[entity.attribute.entity_name] = deepcopy(entity)  # 该节点之内容加入结果集
        return queue_entities

        pass  # function

    @classmethod
    def get_info_of_init_entity_that_corresponding_of_entity(cls, entity: Entity):  # HACK 无用
        """
        获取实体对应的初始态实体之信息

        Args:
            entity: 实体

        Returns: initEntity: 初始态实体, initEntity_name: 初始态实体名称, container: 容器内容, content_type: 内容类型
        """

        entity_name = entity.attribute.entity_name
        pattern = r".*" + "Entity" + ".*"
        splited_entity_name = re.split(pattern, entity_name)
        initEntity_name = splited_entity_name[0] + "Component" + splited_entity_name[1]
        initEntity = eval(initEntity_name)
        container_content = initEntity['container']
        content_type = initEntity['property_content']['content_type']

        return initEntity, initEntity_name, container_content, content_type
        pass  # function


    pass  # class
