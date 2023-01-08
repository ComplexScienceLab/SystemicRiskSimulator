"""
执行机
"""

from PySystemicRiskLab import logging, pd
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
    def execute_branch_node(cls, entity: Entity, agent: SystemicRiskAgent, agentData: AgentDataCollection, para: dict, env: dict):
        """
        执行非终端节点。
        输入参数将被直接修改。

        Args:
            entity (Entity): 过程实体
            agent (SystemicRiskAgent): Agent群变量
            agentData (AgentDataCollection): Agent群变量之数据
            para (dict): 参数变量
            env (dict): 环境变量

        Returns: A, para, env, agentData

        """

        if entity.attribute.node_type == {"process node", "container node"}:
            logging.debug("- 入过程：%s %s", entity.attribute.text_name, entity.attribute.entity_name)

        agent, agentData, para, env = entity.content(entity, agent, agentData, para, env)

        if entity.attribute.node_type == {"process node", "container node"}:
            logging.debug("- 出过程：%s %s", entity.attribute.text_name, entity.attribute.entity_name)

        return agent, agentData, para, env
        pass  # method

    # @classmethod
    # def execute_branch_node(cls, agent: SystemicRiskAgent, para: dict, env: dict, process: Entity, agentData: AgentDataCollection):
    #     """
    #     执行过程节点。
    #     输入参数将被直接修改。
    #
    #     Args:
    #         agent (SystemicRiskAgent): Agent群变量
    #         para (dict): 参数变量
    #         env (dict): 环境变量
    #         process (ProcessModule): 过程模块实例
    #         agentData (AgentDataCollection): Agent群变量之数据
    #
    #     Returns: agent, para, env, agentData
    #
    #     """
    #     agent, para, env, agentData = process.content(agent, para, env, process, agentData)
    #     return agent, para, env, agentData
    #     pass  # method
    #
    @classmethod
    def execute_terminal_node(cls, A: SystemicRiskAgent, b: StateType, ib: StateType, para: dict, env: dict, entity: Entity):
        """
        执行终端节点。
        输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            b (StateType): 商业银行群示性向量
            ib (StateType): 银行间邻接矩阵示性矩阵
            para (dict): 参数变量
            env (dict): 环境变量
            entity (Entity): 算法实体

        Returns: agent

        """
        logging.debug("- - 开始阶段：%s %s", entity.attribute.text_name, entity.attribute.entity_name)
        env['round'] += 1  # 计次回合数
        A.BB, A.BI = entity.content(A.BB, A.BI, b, ib, para, env)
        logging.debug("- - 结束阶段：%s %s", entity.attribute.text_name, entity.attribute.entity_name)
        return A
        pass  # method

    pass  # class
