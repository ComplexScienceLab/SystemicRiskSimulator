"""
执行机
"""

from PySystemicRiskLab import logging
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
# from PySystemicRiskLab.core.define.define_type import *
from PySystemicRiskLab.core.operations.scheduler import Scheduler
from PySystemicRiskLab.core.functions.fun_finance import Finance
from PySystemicRiskLab.core.operations.collector import Collector

pass  # end import


class Executer:
    """
    执行机
    """

    ## NOTE：执行一次步进更新。
    @classmethod
    def step_update(cls, update_way: str, Agent: SystemicRiskAgent, para: dict, env: dict):
        """
        执行一次步进更新

        Args:
            update_way (str): 更新方式
            Agent (SystemicRiskAgent): 多主体
            para (dict): 参数集
            env (dict): 环境变量集

        Returns:
            env (dict): 环境变量集

        """
        Finance.update_finance_variables(Agent.BB, Agent.IB, Agent.b, Agent.ib, by_way=update_way)  # 更新金融变量
        env['step'] += 1  # 步进加一
        env = Scheduler.schedule(env)  # 调度状态变成`collecting`
        env['A_data'], env = Collector.collect(Agent, env['A_data'], env)  # 收集数据

        env = Scheduler.schedule(env)  # 调度状态变成`running`
        return env

        pass  # def

    @classmethod
    def execute_algorithm_entity(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, env: dict, entity: Entity):
        """
        执行算法实体。

        NOTE：输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            A_data (Optional[AgentDataCollection]): Agent群变量之数据
            para (dict): 参数变量
            env (dict): 环境变量
            entity (Entity): 算法实体

        Returns: agent

        """
        # entity = node.content  # 获取节点实体对应的算法实体

        logging.debug("    开始执行算法内容：")

        env['round'] += 1  # 计次回合数
        env['step'] = 0  # 步进归零
        env['process_name'] = entity.attribute.entity_name  # 执行的过程名称（英文名称）
        A.BB, A.IB = entity.execute(A, para, env)

        # ## 收集数据
        # if env['state_of_schedule'] == StateOfScheduleEnum.running:
        #     env = Scheduler.schedule(env)
        #     if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
        #         A_data, env = Collector.collect(A, A_data, env)

        logging.debug("    结束执行算法内容。")

        return A, A_data, env
        pass  # method

    @classmethod
    def execute_branch_entity(cls, node: Entity, agent: SystemicRiskAgent, agentData: AgentDataCollection, para: dict, env: dict):  # HACK 没有适配，已经无用
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
    def execute_terminal_entity(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, env: dict, node: Entity):  # HACK 没有适配，已经无用
        """
        执行终端实体。
        输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            A_data (Optional[AgentDataCollection]): Agent群变量之数据
            para (dict): 参数变量
            env (dict): 环境变量
            node (Entity): 节点实体（NOTE：本函数中，特指节点实体而非算法实体。算法实体表示`entity`。）

        Returns: agent

        """
        algorithmEntity = node.content  # 获取节点实体对应的算法实体

        logging.debug("- - 开始阶段：%s %s", algorithmEntity.attribute.text_name, algorithmEntity.attribute.entity_name)

        env['round'] += 1  # 计次回合数

        A.BB, A.IB = algorithmEntity.execute(A.BB, A.IB, A.b, A.ib, para, env)

        ## 收集数据 #BUG
        if env['state_of_schedule'] == StateOfScheduleEnum.running:
            env = Scheduler.schedule(env)
            if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
                A_data, env = Collector.collect(A, A_data, env)

        logging.debug("- - 结束阶段：%s %s", algorithmEntity.attribute.text_name, algorithmEntity.attribute.entity_name)

        return A, A_data, env
        pass  # method

    pass  # class
