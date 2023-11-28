"""
执行机
"""

from SystemicRiskSimulator import logging
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.define.define_entity import Entity
from SystemicRiskSimulator.core.define.define_enum import StateOfScheduleEnum
from SystemicRiskSimulator.core.operations.scheduler import Scheduler
from SystemicRiskSimulator.core.functions.fun_finance import Finance
from SystemicRiskSimulator.core.operations.collector import Collector

pass  # end import


class Executer:
    """
    执行机
    """

    ## NOTE：执行一次步进更新。
    @classmethod
    def step_update(cls, update_way: str, A: SystemicRiskAgent, para: dict, env: dict):
        """
        执行一次步进更新

        Args:
            update_way (str): 更新方式
            A (SystemicRiskAgent): 多主体
            para (dict): 参数集
            env (dict): 环境变量集

        Returns:
            env (dict): 环境变量集

        """

        Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way=update_way)  # 更新金融变量

        if env['state_of_schedule'] == StateOfScheduleEnum.running:
            Scheduler.schedule(env)  # 调度状态变成`collecting`或者`ending`
        if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
            env['A_data'], env = Collector.collect(A, env['A_data'], env)  # 收集数据
            Scheduler.schedule(env)  # 调度状态变成`running`
        elif env['state_of_schedule'] == StateOfScheduleEnum.ending:
            # Scheduler.schedule(env)  # 调度状态变成`idle`
            pass  # if

        env['step'] += 1  # 步进加一
        env['phase'] += 1  # 逐相加一

        return env
        pass  # function

    @classmethod
    def execute_model_entity(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, env: dict, entity: Entity):
        """
        执行模型实体（模型模板实体）。

        NOTE：输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            A_data (Optional[AgentDataCollection]): Agent群变量之数据
            para (dict): 参数变量
            env (dict): 环境变量
            entity (Entity): 模型实体

        Returns: agent

        """
        # entity = node.content  # 获取节点实体对应的模型实体

        logging.debug("    开始执行模型内容：")

        env['round'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
        env['phase'] = 1  # 逐相复位（起始为1）
        # env['step'] += 1  # 步进加一
        env['process_name'] = entity.attribute.entity_name  # 执行的过程名称（英文名称）
        A, env = entity.execute(A, para, env)

        # ## 收集数据
        # if env['state_of_schedule'] == StateOfScheduleEnum.running:
        #     Scheduler.schedule(env)
        #     if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
        #         A_data, env = Collector.collect(A, A_data, env)

        logging.debug("    结束执行模型内容。")

        return A, A_data, env
        pass  # function


    pass  # class
