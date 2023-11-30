"""
调度机
"""

from SystemicRiskSimulator import logging
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_enum import StateOfScheduleEnum
from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

# from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

# from SystemicRiskSimulator.core.operations.collector import Collector

pass  # end import


class Scheduler:
    """
    调度机，负责模型运作过程中的各种调度。
    """

    @classmethod
    def schedule(cls, sgv: dict):
        """
        调度机

        Args:
            sgv (dict): 模拟器全局变量
            A (SystemicRiskAgent): 系统性风险主体众，可选
            A_data (AgentDataCollection): 系统性风险主体众数据集，可选

        """
        if sgv['state_of_schedule'] is StateOfScheduleEnum.running:
            sgv['state_of_schedule'] = cls.schedule_running(sgv['state_of_schedule'], sgv)
        elif sgv['state_of_schedule'] is StateOfScheduleEnum.collecting:
            sgv['state_of_schedule'] = cls.schedule_collecting(sgv['state_of_schedule'], sgv['running_mode'])
        elif sgv['state_of_schedule'] is StateOfScheduleEnum.initializing:
            sgv['state_of_schedule'] = cls.schedule_initializing(sgv['state_of_schedule'], sgv['running_mode'], sgv)
        elif sgv['state_of_schedule'] is StateOfScheduleEnum.ending:
            sgv['state_of_schedule'] = cls.schedule_ending(sgv['state_of_schedule'])
        elif sgv['state_of_schedule'] is StateOfScheduleEnum.idle:
            sgv['state_of_schedule'] = cls.schedule_idle(sgv['state_of_schedule'])
        else:
            raise Exception("关键词state_of_schedule取词错误".format(sgv['state_of_schedule']))
            pass  # if

        return sgv
        pass  # function


    @classmethod
    def schedule_running(cls, state_of_schedule: StateOfScheduleEnum, sgv: dict):
        """

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态

        Returns:
            state_of_schedule 调度状态
            sgv 模拟器全局变量

        """

        ## 判断是否继续运作轮次
        if (sgv['round'] < sgv['test_max_num_of_round']):
            sgv['is_continue_round'] = True
        else:
            sgv['is_continue_round'] = False
            logging.error("                        超出最大轮次限制，强制结束运作轮次！")
            print("                        超出最大轮次限制，强制结束运作轮次！")
            pass

        ## 判断是否继续运作。只有同时满足继续运行过程、继续运行轮次时，才继续运作。否则不再继续运作。
        if (sgv['is_continue_round'] and sgv['is_continue_process']):
            sgv['is_continue_operation'] = True
        else:
            sgv['is_continue_operation'] = False
            logging.debug("                        不再继续运作。")
            pass

        ## 切换调度状态
        if sgv['is_continue_operation'] is True:
            state_of_schedule = StateOfScheduleEnum.collecting
        else:
            state_of_schedule = StateOfScheduleEnum.ending
        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {sgv['step']}，round = {sgv['round']}，phase = {sgv['phase']}")

        return state_of_schedule
        pass  # function


    @classmethod
    def schedule_collecting(cls, state_of_schedule: StateOfScheduleEnum, running_mode: str):
        """
        调度搜集数据

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态
            running_mode (str): 运行模式

        Returns:
            state_of_schedule 调度状态

        """

        if running_mode == "continue running mode":
            state_of_schedule = StateOfScheduleEnum.running
        elif running_mode == "stepping running mode":
            state_of_schedule = StateOfScheduleEnum.loading

        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {sgv['step']}，round = {sgv['round']}，phase = {sgv['phase']}")

        return state_of_schedule
        pass  # function

    @classmethod
    def schedule_initializing(cls, state_of_schedule: StateOfScheduleEnum, running_mode: str, sgv: dict):
        """
        调度初始状态。

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态
            running_mode (str): 运行模式
            sgv (dict): 模拟器全局变量

        Returns:
            state_of_schedule: 调度状态
        """
        if running_mode == "continue running mode":
            sgv['is_continue_round'] = True
            sgv['is_continue_process'] = True
            state_of_schedule = StateOfScheduleEnum.running
        elif running_mode == "stepping running mode":  # HACK暂时不需要
            state_of_schedule = StateOfScheduleEnum.saving

        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {sgv['step']}，round = {sgv['round']}，phase = {sgv['phase']}")

        return state_of_schedule
        pass  # function

    @classmethod
    def schedule_ending(cls, state_of_schedule: StateOfScheduleEnum):
        """
        调度收尾状态。

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态

        Returns:
            state_of_schedule: 调度状态
        """
        state_of_schedule = StateOfScheduleEnum.idle

        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {sgv['step']}，round = {sgv['round']}，phase = {sgv['phase']}")

        return state_of_schedule
        pass  # function

    @classmethod
    def schedule_idle(cls, state_of_schedule: StateOfScheduleEnum):
        """

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态

        Returns:
             state_of_schedule: 调度状态
        """
        state_of_schedule = StateOfScheduleEnum.initializing

        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {sgv['step']}，round = {sgv['round']}，phase = {sgv['phase']}")

        return state_of_schedule
        pass  # function


    pass  # class
