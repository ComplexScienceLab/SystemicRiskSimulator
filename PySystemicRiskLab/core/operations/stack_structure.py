"""
栈数据结构。

#HACK 没有做覆盖性的单元测试。目前只要求能够在主程序中正确运行就好。

"""

from PySystemicRiskLab import Union
from PySystemicRiskLab.core.operations.entity_manager import EntityManager
from PySystemicRiskLab.core.define.define_entity import Entity


class Stack:
    """
    栈数据结构。

    该数据结构要求输入存储`Entity`之`id`或者`Entity`自身。但是可以通过`EntityManager`实现判断数据类型然后只在栈中存储`Entity`之`id，并且通过`id`返回`Entity`数据。

    """

    def __init__(self):
        """
        初始化。
        """
        self.content = []
        pass  # def

    def is_empty(self):
        """
        判断栈是否为空。
        Returns:
            bool: 如果是空，则返回True，否则返回False。

        """
        return len(self.content) == 0
        pass  # def

    def push(self, items: Union[str, list, Entity]):
        """
        压入元素入栈。

        Args:
            items (Union[str, Entity]): 元素。可以是`Entity`之`id`或者`Entity`自身。

        """
        if isinstance(items, list):
            items_list = items
        else:
            items_list = [items]
            pass  # if

        if isinstance(items_list[0], str):
            self.content.extend(items_list)
        elif isinstance(items_list[0], Entity):
            self.content.extend([item.attribute.id for item in items_list])
            pass  # if

        pass  # def

    def pop(self) -> Entity:
        """
        弹出元素出栈。
        Returns:
            栈顶元素。
        """
        if self.is_empty():
            raise Exception("Stack 是空的")
        item_id = self.content.pop()
        return EntityManager.entities[item_id]
        pass  # def

    def peek(self) -> Entity:
        """
        返回栈顶元素，但是不弹出元素。
        Returns:
            栈顶元素。
        """
        if self.is_empty():
            raise Exception("Stack 是空的")
        item_id = self.content[-1]
        return EntityManager.entities[item_id]
        pass  # def

    def size(self) -> int:
        """
        返回栈的大小。
        Returns:
            栈的大小。
        """
        return len(self.content)
        pass  # def

    def print_stack(self, mode='return'):
        """
        打印栈中的元素，以元素名称的形式。

        Args:
            mode (str): 打印模式。可以是`return`或者`print`。如果是`return`，则返回字符串；如果是`print`，则直接打印。默认是`return`。

        """
        if not self.is_empty():
            if mode == 'return':
                return '[' + ', '.join([EntityManager.entities[item].attribute.entity_name for item in self.content]) + ']'
            elif mode == 'print':
                names = [EntityManager.entities[item].attribute.entity_name for item in self.content]
                print(*names, sep=", ", end="")
                pass  # if
        else:
            if mode == 'return':
                return '[]'
            elif mode == 'print':
                print('[]')
                pass  # if
            pass  # if

        pass  # def
