"""
树数据结构

#HACK 没有做覆盖性的单元测试。目前只要求能够在主程序中正确运行就好。

"""
from SystemicRiskSimulator import Union, logging
from SystemicRiskSimulator.core.define.define_entity import Entity
from SystemicRiskSimulator.core.operations.entity_manager import EntityManager


class Tree:
    """
    树结构类。

    用于构建、遍历一棵树。
    """
    root_node: Entity  # 根节点

    def __init__(self):
        """
        初始化根节点
        """
        self.root_node = EntityManager.create_entity(entity_name='root', node_type={"tree node"})  # 创建根节点
        EntityManager.add_treeNodeEntity(self.root_node)  # 将根节点添加到树节点实体字典中
        self.root_node.attribute.other['parent'] = None
        pass  # def

    def get_root(self) -> Entity:
        """
        获取树之根节点
        Returns:

        """
        return self.root_node
        pass  # def

    def get_parent(self, item: Union[str, Entity]) -> Union[Entity, None]:
        """
        根据当前节点获取父节点。但是不包含父节点之父节点。

        Args:
            item (Union[str, Entity]): 当前节点。可以取其`id`或者`Entity`自身。

        Returns:
            如果是非根节点，则返回父节点，否则返回空
        """

        node = self._distinguish_node_format_and_type(item)

        if node is not None:
            return node.attribute.other['parent']
        else:
            logging.info("当前节点是根节点，没有父节点。")
            return None

        pass  # def

    def get_node_by_id(self, id: str) -> Union[Entity, None]:
        """
        根据树节点`id`获取树节点

        Args:
            id (str): 节点`id`

        Returns:
            Entity: 节点实体，如果没有找到，则返回空。

        """
        return EntityManager.treeEntities[id] if id in EntityManager.treeEntities else None
        pass  # def

    def get_content(self, item: Union[str, Entity]):
        """
        获取当前节点之内容。

        Args:
            item (Union[str, Entity]): 如果是`str`，则是节点`id`；如果是`Entity`，则是节点实体。

        Returns:
            Entity.content: 节点内容。
        """

        node = self._distinguish_node_format_and_type(item)

        return node.content
        pass  # def

    def get_children(self, item: Union[str, Entity]):
        """
        获取当前节点之所有子节点。但是不包含所有子节点之子节点。

        Args:
            item (Union[str, Entity]): 当前节点。可以取其`id`或者`Entity`自身。

        Returns:
            如果存在子节点，返回子节点字典列表，否则返回空列表。
        """
        node = self._distinguish_node_format(item)

        if node is not None:
            return list(node.container.values()) if node.container is not None else []
        else:
            logging.info("当前节点没有子节点。")
            return []
            pass  # if

        pass  # def

    def get_child(self, item: Union[str, Entity], child_item: Union[str, Entity]) -> Union[Entity, None]:
        """
        根据子节点之`id`获取当前节点之子节点。

        Args:
            item (Union[str, Entity]): 当前节点。可以取其`id`或者`Entity`自身。
            child_item (Union[str, Entity]): 子节点。可以取算法实体之节点实体之`id`、树节点实体`id`、算法实体之节点实体`Entity`自身、树节点实体`Entity`自身。

        Returns:
            如果存在子节点，返回子节点，否则返回空。
        """
        node = self._distinguish_node_format_and_type(item)
        child_node = self._distinguish_node_format_and_type(child_item)

        children = self.get_children(node)

        if children is not None:
            for child in children:
                if child.attribute.id == child_node.attribute.id:
                    result_child_node = child_node
                    break
                else:
                    result_child_node = None
                    pass  # if
                pass  # for
        else:
            logging.info(f"节点{node.attribute.entity_name}不存在任何子节点。")
            return None
            pass  # if

        if result_child_node is not None:
            logging.debug(f"节点{node.attribute.entity_name}之子节点为{result_child_node.attribute.entity_name}。")
            return result_child_node
        else:
            logging.info(f"节点{node.attribute.entity_name}之子节点不存在。")
            return None

        pass  # def

    def create_and_add_node(self, id: Union[str, None] = None, entity_name: Union[str, None] = None, content: Union[Entity, None] = None, parent_item: Union[str, Entity, None] = None) -> Entity:
        """
        创建一个节点，并将其附加到树内的其中一个节点。

        根据`id`和实体名称`entity_name`、创建一个树节点，内容并将其附加到树。

        Args:
            id (Union[str, None]): 节点`id`。如果为空，则自动生成。
            entity_name (str): 节点实体名称。
            content (Union[Entity, None]): 节点内容。如果为空，则创建一个空内容。
            parent_item (Union[str, Entity, None]): 父节点。可以取其`id`或者`Entity`自身。如果为空，则将子节点附加到根节点。

        Returns:
            创建的节点。

        """
        node = EntityManager.create_entity(entityData=None, id=id, entity_name=entity_name, node_type={"tree node"}, content=content)
        self.add_child(child_item=node, parent_item=parent_item)
        return node

        pass  # def

    def add_child(self, child_item: Union[str, Entity, None], parent_item: Union[str, Entity, None] = None):
        """
        附加一个子节点到树。

        如果子节点为空，则创建新子节点，然后附加到根节点。

        如果父节点为空，则将子节点附加到根节点。

        Args:
            child_item (Union[str, Entity]): 子节点。可以取其`id`或者`Entity`自身。
            parent_item (Union[str, Entity, None]): 父节点。可以取其`id`或者`Entity`自身。如果为空，则附加到根节点。

        """
        child_node = self._distinguish_node_format(child_item)
        parent_node = self._distinguish_node_format(parent_item)

        # 如果子节点为空，则创建新子节点，然后附加到根节点
        if child_node is None:
            child_node = self.create_and_add_node(id=None, entity_name=child_item, content=None, parent_item=parent_item)
            pass

        # 如果父节点为空，则将子节点附加到根节点
        if parent_node is None:
            parent_node = self.root_node

        child_node.attribute.other['parent'] = parent_node  # 设置子节点之父节点

        ## 子节点附加到父节点
        if parent_node.container is not None:
            parent_node.container.update({child_node.attribute.entity_name: child_node})
        else:
            parent_node.container = {child_node.attribute.entity_name: child_node}
            pass  # if

        EntityManager.add_treeNodeEntity(child_node)  # 添加到树实体集

        pass  # def

    def add_children(self, childern: list, parent: Union[str, Entity, None]):
        """
        附加列表的所有子节点到树。

        Args:
            childern (list): 子节点列表。可以是`id`列表或者`Entity`列表。
            parent (Entity): 父节点。可以是`id`或者`Entity`。如果为空，则附加到根节点。

        """

        # 如果父节点为空，则将子节点附加到根节点
        childern_nodes = [self._distinguish_node_format(child) for child in childern]
        parent_node = self._distinguish_node_format(parent)

        parent_node = parent_node if parent_node is not None else self.root_node

        for child in childern_nodes:
            child.attribute.other['parent'] = parent_node

        ## 子节点附加到父节点
        if parent_node.container is not None:
            for child in childern_nodes:
                parent_node.container.update({child.attribute.id: child})
        else:
            for child in childern_nodes:
                parent_node.container = {child_node.attribute.id: child_node for child_node in childern}
            pass  # if

        ## 添加到树实体集
        for child in childern_nodes:
            EntityManager.add_treeNodeEntity(child)

        pass

    def find_targetNode_from_sourceNode(self, sourceNode: Entity, targetNode_name: str) -> Union[Entity, None]:
        """
        使用迭代查找节点

        Args:
            sourceNode (Entity): 当前源节点
            targetNode_name (str): 目标节点名称

        Returns:
            Entity: 目标节点，如果找到；否则返回None

        """
        stack = [sourceNode]
        while stack:
            curr_node = stack.pop()
            if curr_node.attribute.entity_name == targetNode_name:
                return curr_node
            stack.extend(reversed(curr_node.container))
        return None
        pass  # def

    def remove_node(self, node: Entity, is_link_children_node: bool = False) -> bool:
        """
        从树中移除节点。

        Args:
            node (Entity): 要移除的节点
            is_link_children_node (bool): 是否连接该节点之子节点到该节点之父节点

        Returns:
            bool: True表示移除成功；False表示移除失败

        """
        if node == self.root_node:
            return False  # 没有父节点，移除失败
        parent = node.attribute.other['parent']
        if not parent:
            return False  # 没有父节点，移除失败
        # 父节点的子节点列表移除该节点
        parent.container.remove(node)
        # 该节点的父节点设置为空
        node.attribute.other['parent'] = None

        # 如果需要移除子节点，则将子节点的父节点设置为当前节点的父节点
        if is_link_children_node:
            for child in node.container:
                child.attribute.other['parent'] = parent
                parent.container.append(child)

        EntityManager.treeEntities.pop(node.attribute.id)  # 从树实体集中移除该节点实体

        return True  # 有父节点，移除成功
        pass  # def

    def preorder_traversal(root_node: Entity) -> list:  # HACK 未做单元测试。虽然需要改成自定义的Stack结构，但是目前不怎么做。
        """
        前序遍历

        Args:
            root_node (Entity): 根节点

        Returns:
            List[Entity]: 遍历结果

        """
        if root_node is None:
            return []

        result = []
        stack = [root_node]
        while stack:
            curr_node = stack.pop()
            result.append(curr_node)
            children = reversed(curr_node.container)
            stack.extend(children)
            pass  # while

        return result
        pass  # def

    def inorder_traversal(root_node: Entity) -> list:  # HACK 未做单元测试。虽然需要改成自定义的Stack结构，但是目前不怎么做。
        """
        中序遍历

        Args:
            root_node (Entity): 根节点

        Returns:
            List[Entity]: 遍历结果

        """
        if root_node is None:
            return []

        result = []
        stack = []
        curr_node = root_node
        while curr_node or stack:
            while curr_node:
                stack.append(curr_node)
                curr_node = curr_node.container[0] if curr_node.container else None
            curr_node = stack.pop()
            result.append(curr_node)
            curr_node = curr_node.container[1] if len(curr_node.container) > 1 else None

        return result
        pass  # def

    def postorder_traversal(root_node: Entity) -> list:  # HACK 未做单元测试。虽然需要改成自定义的Stack结构，但是目前不怎么做。
        """
        后序遍历
        Args:
            root_node (Entity): 根节点

        Returns:
            List[Entity]: 遍历结果

        """
        if root_node is None:
            return []

        result = []
        stack = [(root_node, False)]
        while stack:
            curr_node, visited = stack.pop()
            if visited:
                result.append(curr_node)
            else:
                stack.append((curr_node, True))
                children = reversed(curr_node.container)
                for child in children:
                    stack.append((child, False))

        return result
        pass  # def

    def print_tree(self, node: Union[Entity, None] = None, info: str = 'entity_name', prefix="", _is_tail=True):  # NOTE 由于目前预计其生成树结构之规模小，因此无需改成非递归的方式。
        """
        以类似Linux中tree命令的输出结果打印树结构及其相关信息。

        递归编程方式。

        Args:
            node (Entity): 树节点。
            info (str): 要打印的信息。默认为实体名称`entity_name`。

        Returns:

        """

        ## NOTE 基于递归形式的
        if not node:
            node = self.root_node
            pass  # if
        node_info = node.attribute.entity_name
        node_prefix = "└── " if _is_tail else "├── "
        logging.info(prefix + node_prefix + str(node_info))
        child_prefix = prefix + (" " * 8 if _is_tail else "│" + " " * 6)
        if self.get_children(node) is not None:
            child_count = len(self.get_children(node))
            for i, child in enumerate(self.get_children(node)):
                _is_tail = (i == child_count - 1)
                self.print_tree(node=child, info=node_info, prefix=child_prefix, _is_tail=_is_tail)
        else:
            pass  # if

        # node_info = eval('node.attribute.info') #HACK 这个是基于递归形式的，可以提供多个打印信息的。但是还没有完成。
        # node_prefix = "└── " if _is_tail else "├── "
        # logging.info(prefix + node_prefix + str(node_info))
        # child_prefix = prefix + (" " * 8 if _is_tail else "│" + " " * 6)
        # if self.get_children(node) is not None:
        #     child_count = len(self.get_children(node))
        #     for i, child in enumerate(self.get_children(node).values()):
        #         _is_tail = (i == child_count - 1)
        #         self.print_tree(node=child, prefix=child_prefix, _is_tail=_is_tail)
        # else:
        #     pass  # if

        pass  # def

    # def print_tree(self):  # HACK 未能运行起来。后续需要改进。需要广度优先遍历生成前缀字符串。需要前序遍历生成打印顺序。
    #     """
    #     以类似Linux中tree命令的输出结果打印树结构。
    #
    #     非递归编程方式。
    #
    #     Returns:
    #
    #     """
    #     child_prefix = ""
    #     stack = [(self, "", 0, True)]
    #     queue = []
    #     while stack:
    #         node, node_prefix, level, is_tail = stack.pop()
    #         node_prefix = ("└── " if is_tail else "├── ")
    #         # print(child_prefix + " " * 8 * level + node_prefix + str(node.value))
    #         print(child_prefix + node_prefix + str(node.value))
    #         if node != None:
    #             if node.children:
    #                 # child_prefix = child_prefix + (" " * 8 if is_tail else "│" + " " * 6)
    #                 child_prefix = (" " * 8 * (level + 1) if is_tail else "│" + " " * 6)
    #                 child_count = len(node.children)
    #                 for i, child in enumerate(reversed(node.children)):
    #                     is_tail = (i == child_count - 1)
    #                     stack.append((child, child_prefix, level + 1, is_tail))
    #             stack.append((node, node_prefix, level, is_tail))
    #         else:
    #             node =;
    #             stack.pop()
    #     pass  # def

    def _distinguish_node_format(self, item: Union[str, Entity, None]):
        """
        判断输入的节点之输入格式。是以节点`id`还是节点实体本身的格式。然后返回节点实体本身。

        Args:
            item (Union[str, Entity]): 输入的节点。可以是`id`或者是节点实体本身。

        Returns:
            Entity: 节点实体本身。

        """

        if isinstance(item, str):
            node = self.get_node_by_id(item)
        elif isinstance(item, Entity):
            node = item
        else:
            node = None
            pass  # if
        if node is not None:
            return node
        else:
            logging.info(f"没有找到节点")
            return None
            pass  # if

        pass  # def

    def _distinguish_node_format_and_type(self, item: Union[str, Entity, None]):
        """
        判断输入的节点之输入格式与实体类型。是以节点`id`还是节点实体本身的格式，并且判断实体类型。然后返回节点实体本身。

        Args:
            item (Union[str, Entity]): 输入的节点。可以是树节点之`id`或者是树节点实体本身，也可以是算法节点之`id`或者是算法节点实体本身。

        Returns:
            Entity: 树节点实体本身，如果没有找到则返回`None`。

        """

        if isinstance(item, str):
            node_format = "id"
        elif isinstance(item, Entity):
            node_format = "entity"

        if node_format == "id":
            if item in EntityManager.treeEntities.keys():
                node = EntityManager.treeEntities[id]
                type_name = "树节点实体"
            else:
                for entity in EntityManager.entities.values():
                    if item == entity.attribute.id:
                        node = entity
                        type_name = "算法实体之节点实体"
                        break
                    else:
                        node = None
                    pass  # if
                pass  # for
            pass  # if

        if node_format == "entity":
            if item in EntityManager.treeEntities.values():
                node = item
                type_name = "树节点实体"
            elif item in EntityManager.entities.values():
                node = item
                type_name = "算法实体之节点实体"
            else:
                node = None
            pass

        if type_name == "树节点实体":
            result_node = node
        elif type_name == "算法实体之节点实体":
            ## 根据算法实体之节点实体获取树节点实体。
            for tree_entity in EntityManager.treeEntities.values():
                if node.attribute.id == tree_entity.content.attribute.id:
                    result_node = tree_entity
                    break
                else:
                    result_node = None
                pass

        if result_node is not None:
            logging.debug(f"通过{node_format}和{type_name}找到树节点：{node.attribute.entity_name}")
            return result_node
        else:
            logging.info(f"没有找到节点")
            return None
            pass  # if

    pass  # def


pass  # class
