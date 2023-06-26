"""
实体管理机
"""

from PySystemicRiskLab import np, logging
from PySystemicRiskLab.core.define.define_component import *
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.tools.tools import Tools

pass  # end import


class EntityManager:
    """
    实体管理机。

    其中可用变量如下：
    entities：实体字典。键是实体`id`，值是实体。
    algorithmEntities：算法实体字典。键是实体名称`entity_name`，值是实体。
    modelEntities：模型实体字典。键是实体名称`entity_name`，值是实体。
    treeEntities：树实体字典。键是实体`id`，值是实体。

    管理所有存在变量空间的实体变量。
    """

    entities: dict = {}  # 实体字典。键是实体`id`，值是实体。
    algorithmEntities: dict = {}  # 算法实体字典。键是实体名称`entity_name`，值是实体。
    modelEntities: dict = {}  # 模型实体（模型节点实体）字典。键是实体名称`entity_name`，值是实体。
    modelAlgorithmEntities: dict = {}  # 模型算法字典。键是实体名称`entity_name`，值是实体。
    treeEntities: dict = {}  # 树实体字典。键是实体`id`，值是实体。

    @classmethod
    def create_entity(cls, entityData: Any = None, **kwargs):
        """
        创建一个新实体。

        新实体可以传入参数为空，但是生成的新实体一定具有两个非空的属性：`attribute.id`、`attribute.entity_name`。其中，`attribute.id`是实体唯一标识符，每一个实体之`id`都不重复。

        有以下方式创建实体：

        1. 通过传入实体数据创建实体。

        2. 通过传入任意的键值对到`**kwargs`创建实体。

        如果没有手动设置新建的节点`id`，那么自动设置一个`id`。

        其中，`id`开头为"user"的为保留字段，用于表示用户自定义的`id`。

        如果没有手动设置新建的节点名称，那么自动使用`id`作为名称。

        如果新建的节点`id`与变量区中现有的节点的`id`重复，或者前4位是`"user"`，那么就重新生成新的不重复的`id`，然后返回相应的信息。

        创建一个新实体之后，根据实体之节点属性`attribute.node_type`、实体之内容属性`attribute.content_type`，加入新建的实体`id`到实体列表。

        **kwargs: 其它参数

        其中，推荐手动设置以下参数：

        - attribute (AttirbuteComponentType) = None: 实体属性

        - id (Union[int, str,None]) = None: 实体id

        - name: Union[str,None] = None: 实体名称

        - content: Union[str, Any] = None: 实体内容


        Args:
            entityData (Any): 已经事先设置好了的实体数据
            **kwargs: 其它参数

        Returns:
            Entity: 新节点

        """

        ## 如果传入了实体数据，那么就直接创建实体，否则根据传入的其他参数创建实体
        if entityData is not None:
            entity = Entity(entityData=entityData)
        else:
            ## 判别是否需要创建新的`id`、`kwargs`是否有`id`键
            if 'id' in kwargs.keys():  # 如果有键`id`
                is_kwargs_has_key_id = True
                if kwargs['id'] is None:  # 如果`id`是空的，那么就自动生成一个新的`id`
                    is_need_create_new_id = True
                else:  # 如果`id`不是空的，那么就考虑使用手动设置的`id`
                    if cls._distinguish_is_need_create_new_id(kwargs['id']):  # 判断是否需要自动生成`id`
                        logging.info(f"手动设置的节点id={kwargs['id']}无效，需要重新生成一个新的节点id")
                        is_need_create_new_id = True  # 手动设置的`id`无效，需要重新生成`id`
                    else:
                        is_need_create_new_id = False  # 手动设置的`id`有效，不需要重新生成`id`
                        pass  # if
                    pass  # if
            else:  # 如果没有键`id`，则需要自动生成一个`id`
                is_kwargs_has_key_id = False
                is_need_create_new_id = True
                pass  # if

            ## 根据判别结果设置`id`
            if is_need_create_new_id:  # 如果需要创建新的`id`
                new_id = Tools.generate_unique_identifier()
                while cls._distinguish_is_need_create_new_id(new_id):  # 判断是否需要重新创建`id`
                    new_id = Tools.generate_unique_identifier()
                    pass  # while
                logging.info(f"自动生成一个新的节点id={new_id}")
            else:
                new_id = str(kwargs['id']).zfill(8)  # 使用手动设置的节点`id`
                pass  # if

            ## 根据判别结果更新`kwargs`之`id`
            if is_kwargs_has_key_id:  # 如果有键`id`
                kwargs['id'] = new_id
            else:  # 如果没有键`id`
                kwargs.update({'id': new_id})
                pass  # if

            ## 设置`entity_name`
            ## 判别是否需要创建新的`entity_name`、`kwargs`是否有`entity_name`键
            if 'entity_name' in kwargs.keys():  # 如果有键`entity_name`
                is_kwargs_has_key_entity_name = True
                if kwargs['entity_name'] is None:  # 如果没有手动设置`entity_name`，就用`id`作为`entity_name`
                    is_need_create_new_name = True
                else:
                    is_need_create_new_name = False
                    pass  # if
            else:
                is_kwargs_has_key_entity_name = False
                is_need_create_new_name = True
                pass  # if

            ## 根据判别结果设置`entity_name`
            if is_need_create_new_name:  # 如果需要创建新的`entity_name`
                new_name = f"name_{new_id}"
                logging.info(f"未设置name，自动命名为名称：「{new_name}」。")
            else:
                new_name = kwargs['entity_name']
                pass  # if

            ## 根据判别结果更新`kwargs`之`entity_name`
            if is_kwargs_has_key_entity_name:  # 如果有键`entity_name`
                kwargs['entity_name'] = new_name
            else:  # 如果没有键`entity_name`
                kwargs.update({'entity_name': new_name})

            ## 根据上述判断，创建实体
            entity = Entity(entityData=None, **kwargs)

            # ## 设置节点类型
            # is_need_set_nodeType = None  # 初始化是否需要设置节点类型
            # if 'node_type' in kwargs.keys():  # 如果有键`node_type`，并且有值，就设置节点类型，否则不设置。
            #     if kwargs['node_type'] is None:
            #         is_need_set_nodeType = False
            #     else:
            #         is_need_set_nodeType = True
            #         pass  # if
            # else:
            #     is_need_set_nodeType = False
            #     pass  # if
            #
            # ## 根据上述判断，创建实体
            # if is_need_set_nodeType:
            #     entity = Entity(entityData=None, id=new_id, entity_name=new_name, node_type=kwargs['node_type'])
            # else:
            #     entity = Entity(entityData=None, id=new_id, entity_name=new_name)
            #     pass  # if

        pass  # if

        ## 将新建的实体id加入各个实体列表
        cls.add_entity(entity)
        cls.add_algorithmEntity(entity)
        cls.add_modelEntity(entity)
        cls.add_modelAlgorithmEntity(entity)
        cls.add_treeNodeEntity(entity)
        return entity

    @classmethod
    def delete_entity(cls, entity: Entity):
        """
        删除实体。

        注意：永久删除实体。

        Args:
            entity (Entity): 实体

        Returns:

        """

        id = entity.attribute.id
        name = entity.attribute.entity_name

        ## 分别从各实体列表中移除实体
        if id in cls.entities.keys():
            cls.entities.pop(id)
            logging.info(f"已从 entities 移除实体")
        if name in cls.algorithmEntities.keys():
            cls.algorithmEntities.pop(name)
            logging.info(f"已从 algorithmEntities 移除实体")
        if name in cls.modelEntities.keys():
            cls.modelEntities.pop(name)
            logging.info(f"已从 modelEntities 移除实体")
        if id in cls.treeEntities.keys():
            cls.treeEntities.pop(id)
            logging.info(f"已从 treeEntities 移除实体")

        ## 删除实体
        del entity
        logging.info(f"已删除实体。id：{id}，名称：{name}。")

        pass  # def

    @classmethod
    def add_entity(cls, entity: Entity):
        """
        添加新建的实体到实体字典，键是实体`id`，值是实体。

        Args:
            entity (Entity): 实体

        Returns:

        """
        cls.entities.update({entity.attribute.id: entity})
        logging.info(f"已添加实体到 entities。id：「{entity.attribute.id}」，名称：「{entity.attribute.entity_name}」。")
        pass  # def

    @classmethod
    def add_treeNodeEntity(cls, entity: Entity):
        """
        添加树实体到树实体字典。键是实体`id`，值是实体。

        Args:
            entity (Entity): 实体

        Returns:

        """
        if (
                entity.attribute.node_type == {"tree node"}
        ):
            cls.treeEntities.update({entity.attribute.id: entity})
            logging.info(f"已添加实体到 treeEntities。id：「{entity.attribute.id}」，名称：「{entity.attribute.entity_name}」。")
        pass  # def

    @classmethod
    def add_algorithmEntity(cls, entity: Entity):
        """
        添加算法实体到算法实体字典。键是实体名称`entity_name`，值是实体。

        Args:
            entity (Entity): 实体

        Returns:

        """
        if (
                entity.attribute.node_type == {"container node", "process node"} and
                entity.attribute.content_type == {"algorithm content"}
        ) or (
                entity.attribute.node_type == {"container node", "process node"} and
                entity.attribute.content_type == {"model content", "algorithm content"}
        ) or (
                entity.attribute.node_type == {"content node"} and
                entity.attribute.content_type == {"algorithm content"}
        ) or (
                entity.attribute.node_type == {"process node"} and
                entity.attribute.content_type == {"process content"}
        ):
            cls.algorithmEntities.update({entity.attribute.entity_name: entity})
            logging.info(f"已添加实体到 algorithmEntities。id：「{entity.attribute.id}」，名称：「{entity.attribute.entity_name}」。")
        pass  # def

    @classmethod
    def add_modelAlgorithmEntity(cls, entity: Entity):
        """
        添加模型算法实体到模型算法实体字典。键是实体名称`entity_name`，值是实体。

        Args:
            entity (Entity): 实体

        Returns:

        """

        # if (
        #         entity.attribute.node_type == {"container node"} and
        #         entity.attribute.content_type == {"model content", "node content"}
        # ):
        if (
                entity.attribute.node_type == {"container node", "process node"} and
                entity.attribute.content_type == {"model content", "algorithm content"}
        ):
            cls.modelAlgorithmEntities.update({entity.attribute.entity_name: entity})
            logging.info(f"已添加实体到 modelAlgorithmEntities。id：「{entity.attribute.id}」，名称：「{entity.attribute.entity_name}」。")
        pass  # def

    @classmethod
    def add_modelEntity(cls, entity: Entity):
        """
        添加模型实体（模型节点实体）到模型实体字典。键是实体名称`entity_name`，值是实体。

        Args:
            entity (Entity): 实体

        Returns:

        """

        # if (
        #         entity.attribute.node_type == {"container node", "process node"} and
        #         entity.attribute.content_type == {"model content", "algorithm content"}
        # ) or (
        #         entity.attribute.node_type == {"container node"} and
        #         entity.attribute.content_type == {"model content", "node content"}
        # ):
        if (
                entity.attribute.node_type == {"container node"} and
                entity.attribute.content_type == {"model content", "node content"}
        ):
            cls.modelEntities.update({entity.attribute.entity_name: entity})
            logging.info(f"已添加实体到 modelEntities。id：「{entity.attribute.id}」，名称：「{entity.attribute.entity_name}」。")
        pass  # def

    @classmethod
    def _distinguish_is_need_create_new_id(cls, id: Union[str, None]) -> bool:
        """
        判断是否需要创建新的实体`id`。

        Args:
            id (Union[str, None]): 实体`id`

        Returns:
            bool: 是否需要创建新的实体`id`

        """
        if id in cls.entities.keys():
            logging.warning(f"节点id={id}已存在！")
            return True
        elif id[:4].lower() == "user":
            logging.warning(f"节点id={id}以「user」开头！")
            return True
        else:
            return False
            pass  # if

        pass  # def

    pass  # class
