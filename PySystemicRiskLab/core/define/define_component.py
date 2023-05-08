"""
定义组件
"""
from PySystemicRiskLab import Any
from PySystemicRiskLab.core.define.define_type import *


class AttributeComponent:
    """
    特征组件
    """

    id: int  # 事物之编号
    entity_name: str  # 事物之名称
    text_name: str  # 事物之文本名称
    content_type: str  # 事物之内容类型
    content_name: Union[str, None]  # 事物之内容名称
    other: Union[dict, Any, None]  # 事物之其他特征

    def __init__(self, attribute: dict):
        """
        初始化特征组件

        Args:
            attribute: 特征
        """
        self.id = attribute['id']
        self.entity_name = attribute['entity_name']
        self.text_name = attribute['text_name']
        self.node_type = attribute['node_type']
        self.content_type = attribute['content_type']
        self.content_name = None
        self.other = {}
        for k, v in attribute.items():
            if not (k == "id" or k == "entity_name" or k == "text_name" or k == "node_type" or k == "content_type"):
                self.other.update({k: v})
        pass  # method

    pass  # class


class ContentComponent:
    """
    内容组件
    """

    content: NodeComponentType

    def __init__(self, content):
        """

        Args:
            content: 内容
        """
        self.attribute = None
        self.content = content

    pass  # class


class ContainerComponent:
    """
    容器组件
    """

    container: ContainerComponentType

    def __init__(self, container):
        """

        Args:
            container: 容器之内容
        """
        self.container = container
        pass  # method

    pass  # class


class ProcessComponent:
    """
    过程组件
    """

    process: ProcessComponentType

    def __init__(self, process):
        """

        Args:
            process: 过程之内容
        """
        self.process = process
        pass  # method

    pass  # class

class ExecuteComponent:
    """
    执行组件
    """

    execute: ExecuteComponentType

    def __init__(self, execute):
        """

        Args:
            execute: 执行之内容
        """
        self.execute = execute
        pass  # method

    pass  # class


class NodeComponent:
    """
    节点组件
    """

    node: NodeComponentType

    def __init__(self, node):
        """

        Args:
            node: 过程之内容
        """
        self.node = node
        pass  # method

    pass  # class
