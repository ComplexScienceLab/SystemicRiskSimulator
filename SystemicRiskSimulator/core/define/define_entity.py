"""
定义实体
"""

from SystemicRiskSimulator.core.define.define_component import *

pass  # end import


class Entity:
    """
    实体。

    实体是系统中的基本单元。实体是一个有特征的对象，它可以是一个节点、一个内容、一个容器、一个过程、一个条件、一个执行器。

    实体的特征是由实体的组件决定的。实体的组件包括：实体特征、实体内容、实体容器、实体过程、实体节点、实体条件、实体执行器。

    包含的组件有：

    - attribute: AttributeComponentType: 实体特征
    - content: Union[ContentComponent, None]: 实体内容
    - process: Union[ProcessComponent, None]: 实体过程
    - container: Union[ContainerComponent, None]: 实体容器
    - condition: Union[ConditionComponent, None]: 实体条件
    - execute: Union[ExecuteComponent, None]: 实体执行器
    - operate: Union[OperateComponent, None]: 实体运作器
    - environment: Union[EnvironmentComponent, None]: 实体环境
    - node: Union[NodeComponent, None]: 实体节点
    """

    attribute: AttributeComponent
    content: Union[ContentComponent, None]
    process: Union[ProcessComponent, None]
    container: Union[ContainerComponent, None]
    condition: Union[ConditionComponent, None]
    execute: Union[ExecuteComponent, None]
    operate: Union[OperateComponent, None]
    environment: Union[EnvironmentComponent, None]
    node: Union[NodeComponent, None]

    def __init__(self, entityData: Any = None, **kwargs):
        """
        初始化。创建实体

        Args:
            entityData (Any): 事先设置好的实体数据
            attribute (AttributeComponentType): 实体特征
            **kwargs (): 其它参数

        > [!note]
        > 以下是赋值的要求：

        - 如果`entityData`不为空，那么要求`**kwargs`设置为空；

        - 如果`entityData`不为空，那么要求`entityData`数据必须符合格式要求。

        - 如果`entityData`为空且`**kwargs`不为空，那么要求`**kwargs`里面不能有`entityData`；

        - `**kwargs`之所有键名应该与实体类在各组件字段名称保持一致，除了`attribute.other`字段之外；

        - 最好不要在实例化`entity`时赋值`attribute.other`字段。建议在实例化之后，再赋值`attribute.other`字段；

        - 当所有参数都为空的时候，将创建一个具有随机`id`、随机`name`的空实体。


        Returns:
            entity (Entity): 实体

        """

        ## 如果`entityData`不为空，那么直接设置`entityData`数据，否则设置`**kwargs`数据。
        if entityData is not None:
            kwargs = None
            self.attribute = AttributeComponent(attribute=entityData['attribute'])  # HACK 如果`entityData['attribute']`为空，那么entityData数据不符合要求。这里并未给出检查条件。
            self.content = entityData['content']
            self.execute = entityData['execute']
            self.operate = entityData['operate']
            self.environment = entityData['environment']
            self.process = entityData['process']
            self.container = entityData['container']
            self.condition = entityData['condition']
            self.node = entityData['node']
        elif kwargs is not None:  # 如果`attribute`不为空，那么直接设置`attribute`数据至`AttributeComponent`，否则设置`**kwargs`至`AttributeComponent`。
            if 'attribute' in kwargs.keys():  # 有`attribute`组件，就直接通过`attribute`组件创建`attribute`组件
                self.attribute = AttributeComponent(attribute=kwargs['attribute'])
            elif 'attribute' not in kwargs.keys():  # 没有`attribute`组件，就通过其它键值对创建`attribute`组件
                self.attribute = AttributeComponent(attribute=None, **kwargs)
                pass  # if
            ## 一次创建其它组件
            self.content = kwargs['content'] if 'content' in kwargs.keys() else None
            self.execute = kwargs['execute'] if 'execute' in kwargs.keys() else None
            self.operate = kwargs['operate'] if 'operate' in kwargs.keys() else None
            self.environment = kwargs['environment'] if 'environment' in kwargs.keys() else None
            self.process = kwargs['process'] if 'process' in kwargs.keys() else None
            self.container = kwargs['container'] if 'container' in kwargs.keys() else None
            self.condition = kwargs['condition'] if 'condition' in kwargs.keys() else None
            self.node = kwargs['node'] if 'node' in kwargs.keys() else None
        else:  # HACK其实这种情况不可能发生。因为已经自动生成了`id`和`fullName`。
            self.attribute = AttributeComponent(None)
            self.content = None
            self.execute = None
            self.operate = None
            self.environment = None
            self.process = None
            self.container = None
            self.condition = None
            self.node = None
            pass  # if

        pass  # function

    pass  # class
