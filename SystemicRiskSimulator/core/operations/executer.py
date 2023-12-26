"""
执行机
"""

from SystemicRiskSimulator.external_packages import logging
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
    def step_update(cls, update_way: str, A: SystemicRiskAgent, para: dict, sgv: dict):
        """
        执行一次步进更新

        更新方式具体见：`Finance.update_finance_variables` 对应的[文档](SystemicRiskSimulator/core/functions/fun_finance.py)。

        Args:
            update_way (str): 更新方式
            A (SystemicRiskAgent): 多主体
            para (dict): 参数集
            sgv (dict): 模拟器全局变量

        Returns:
            sgv (dict): 模拟器全局变量

        """

        # logging.debug("               步进更新")
        logging.debug(f"               步进：{sgv['step']}，相：{sgv['phase']}，更新源：{update_way}")
        Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way=update_way)  # 更新金融变量
        # sgv['A_data'], sgv = Collector.collect(A, sgv['A_data'], sgv)  # 收集数据
        # logging.debug("                    收集数据")
        # sgv['id_data'] += 1  # 累加数据帧ID号
        sgv['A_data'] = Collector.collect_agent_data(A, sgv['A_data'], sgv)

        # if sgv['state_of_schedule'] == StateOfScheduleEnum.running:  #HACK 不再使用调度状态，可删除
        # Scheduler.schedule(sgv)  # 调度状态变成`collecting`或者`ending`
        # if sgv['state_of_schedule'] == StateOfScheduleEnum.collecting:
        #     sgv['A_data'], sgv = Collector.collect(A, sgv['A_data'], sgv)  # 收集数据
        #     Scheduler.schedule(sgv)  # 调度状态变成`running`
        # elif sgv['state_of_schedule'] == StateOfScheduleEnum.ending:
        #     # Scheduler.schedule(sgv)  # 调度状态变成`idle`
        #     pass  # if

        sgv['step'] += 1  # 步进加一
        sgv['phase'] += 1  # 逐相加一

        return sgv
        pass  # function

    @classmethod
    def execute_model_entity(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict, entity: Entity):
        """
        执行模型实体（模型模板实体）。

        NOTE：输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            A_data (Optional[AgentDataCollection]): Agent群变量之数据
            para (dict): 参数变量
            sgv (dict): 模拟器全局变量
            entity (Entity): 模型实体

        Returns: agent

        """
        # entity = node.content  # 获取节点实体对应的模型实体

        logging.debug("    开始执行模型内容：")

        sgv['round'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
        sgv['phase'] = 1  # 逐相复位（起始为1）
        # sgv['step'] += 1  # 步进加一
        sgv['process_name'] = entity.attribute.entity_name  # 执行的过程之名称（英文名称）
        A, sgv = entity.execute(A, para, sgv)

        # if sgv['state_of_schedule'] == StateOfScheduleEnum.running:  #HACK 不再使用调度状态，可删除
        #     Scheduler.schedule(sgv)  # 调度状态变成`ending`或者继续`running`
        # elif sgv['state_of_schedule'] == StateOfScheduleEnum.ending:
        #     # Scheduler.schedule(sgv)  # 调度状态变成`idle`
        #     pass  # if

        logging.debug("    结束执行模型内容。")

        return A, A_data, sgv
        pass  # function

    @classmethod
    def execute_main_model_entity(cls, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict, entity: Entity):
        """
        执行非流程版本的模型实体（模型模板实体）。

        NOTE：输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            A_data (Optional[AgentDataCollection]): Agent群变量之数据
            para (dict): 参数变量
            sgv (dict): 模拟器全局变量
            entity (Entity): 模型实体

        Returns: agent

        """
        # entity = node.content  # 获取节点实体对应的模型实体

        logging.debug("    开始执行模型内容：")

        # sgv['round'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
        # sgv['phase'] = 1  # 逐相复位（起始为1）
        # # sgv['step'] += 1  # 步进加一
        sgv['process_name'] = entity.attribute.entity_name  # 执行的过程之名称（英文名称）
        entity.execute(A, A_data, para, sgv)

        # if sgv['state_of_schedule'] == StateOfScheduleEnum.running:  #HACK 不再使用调度状态，可删除
        #     Scheduler.schedule(sgv)  # 调度状态变成`ending`或者继续`running`
        # elif sgv['state_of_schedule'] == StateOfScheduleEnum.ending:
        #     # Scheduler.schedule(sgv)  # 调度状态变成`idle`
        #     pass  # if

        logging.debug("    结束执行模型内容。")

        return A, A_data, sgv
        pass  # function

    pass  # class
