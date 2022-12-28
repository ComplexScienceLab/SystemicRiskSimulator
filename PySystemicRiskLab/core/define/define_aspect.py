"""
定义方面
"""
from PySystemicRiskLab import Any
from PySystemicRiskLab.core.define.define_type import *


class AttributeAspect:
    """
    特征方面
    """

    id: int  # 事物之编号
    entity_name: str  # 事物之名称
    text_name: str  # 事物之文本名称
    content_type: str  # 事物之内容类型
    content_name: Union[str, None]  # 事物之内容名称
    other: Union[dict, Any, None]  # 事物之其他特征

    def __init__(self, attribute: dict):
        """
        初始化特征方面

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


class ContentAspect:
    """
    内容方面
    """

    content: NodeAspectType

    def __init__(self, content):
        """

        Args:
            content: 内容
        """
        self.content = content
        pass  # method

    pass  # class


class ContainerAspect:
    """
    容器方面
    """

    container: ContainerAspectType

    def __init__(self, container):
        """

        Args:
            container: 容器之内容
        """
        self.container = container
        pass  # method

    pass  # class


class ProcessAspect:
    """
    过程方面
    """

    process: ProcessAspectType

    def __init__(self, process):
        """

        Args:
            process: 过程之内容
        """
        self.process = process
        pass  # method

    pass  # class
