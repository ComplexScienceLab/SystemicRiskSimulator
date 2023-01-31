"""
执行机
"""

from PySystemicRiskLab import logging
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.define.define_type import *

pass  # end import


class Executer:
    """
    执行机
    """

    @classmethod
    def execute_branch_entity(cls, node: Entity, agent: SystemicRiskAgent, agentData: AgentDataCollection, para: dict, env: dict):
        """
        执行分支实体。
        输入参数将被直接修改。

        Args:
            node (Entity): 节点实体（NOTE：本函数中，特指节点实体而非算法实体。算法实体表示`entity`。）
            agent (SystemicRiskAgent): Agent群变量
            agentData (AgentDataCollection): Agent群变量之数据
            para (dict): 参数变量
            env (dict): 环境变量

        Returns: modelEntity, A, para, env, agentData

        """
        entity = node.content  # 获取节点实体对应的算法实体

        # if node.attribute.node_type == {"process node", "container node"}:
        logging.debug("- 入过程：%s %s", entity.attribute.text_name, entity.attribute.entity_name)

        node, agent, agentData, para, env = entity.execute(node, agent, agentData, para, env)

        # if node.attribute.node_type == {"process node", "container node"}:
        logging.debug("- 出过程：%s %s", entity.attribute.text_name, entity.attribute.entity_name)

        return node, agent, agentData, para, env
        pass  # method

    @classmethod
    def execute_terminal_entity(cls, A: SystemicRiskAgent, b: StateType, ib: StateType, para: dict, env: dict, node: Entity):
        """
        执行终端实体。
        输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            b (StateType): 商业银行群示性向量
            ib (StateType): 银行间邻接矩阵示性矩阵
            para (dict): 参数变量
            env (dict): 环境变量
            node (Entity): 节点实体（NOTE：本函数中，特指节点实体而非算法实体。算法实体表示`entity`。）

        Returns: agent

        """
        entity = node.content  # 获取节点实体对应的算法实体

        logging.debug("- - 开始阶段：%s %s", entity.attribute.text_name, entity.attribute.entity_name)

        env['round'] += 1  # 计次回合数

        A.BB, A.BI = entity.execute(A.BB, A.BI, b, ib, para, env)

        logging.debug("- - 结束阶段：%s %s", entity.attribute.text_name, entity.attribute.entity_name)

        return A
        pass  # method

    # @classmethod
    # def execute_special_entity(cls, node:Entity): #HACK 无用
    #     """
    #     执行特殊实体。特殊实体指：开始节点实体、结束节点实体。
    #
    #     Args:
    #         node (Entity): 节点实体（NOTE：本函数中，特指节点实体而非算法实体。算法实体表示`entity`。）
    #
    #     Returns: node
    #
    #     """
    #
    #     entity = node.content  # 获取节点实体对应的算法实体
    #
    #     # if node.attribute.node_type == {"process node", "container node"}:
    #     logging.debug("- 入过程：%s %s", entity.attribute.text_name, entity.attribute.entity_name)
    #
    #     node, agent, agentData, para, env = entity.execute(node)
    #
    #     # if node.attribute.node_type == {"process node", "container node"}:
    #     logging.debug("- 出过程：%s %s", entity.attribute.text_name, entity.attribute.entity_name)
    #
    #     pass  # method

    pass  # class
