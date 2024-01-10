"""
处理机。
#NOTE：如果不是因为Python语言会出现循环调用的情况，那么会将这里的一些功能和内容放入`operator`。
"""

from SystemicRiskSimulator.external_packages import dataclass
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_entity import Entity
from SystemicRiskSimulator.core.operations.executer import Executer


@dataclass()
class Processor:
    """
    处理机
    """

    @classmethod
    def process_entity_by_execute_component(cls, model: Entity, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        处理所有类型的实体，通过执行组件。这个适用于非流程版形式的模型实体。#HACK 似乎无用了。

        Args:
            model (Any): 模型实体（NOTE：本函数中，特指模型实例实体而不是主模型模板实体。）
            A (SystemicRiskAgent): Agent群变量
            A_data (AgentDataCollection): Agent群变量之数据
            para (dict): 参数变量
            sgv (dict): 模拟器全局变量

        Returns: entity: 模型模板实体, A: Agent群变量, para: 参数变量, sgv: 模拟器全局变量, A_data: Agent群变量之数据

        """

        ## 根据模型模板实体执行相关的内容
        modelEntity = model.content
        A, A_data, sgv = Executer.execute_main_model_entity(A, A_data, para, sgv, modelEntity)

        return model, A, A_data, para, sgv

        pass  # function

    pass  # class
