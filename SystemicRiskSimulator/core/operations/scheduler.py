"""
调度机
"""

from SystemicRiskSimulator import logging
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_enum import StateOfScheduleEnum
from SystemicRiskSimulator.core.define.define_environmentVariables import env

# from SystemicRiskSimulator.core.define.define_environmentVariables import env

# from SystemicRiskSimulator.core.operations.collector import Collector

pass  # end import


class Scheduler:
    """
    调度机，负责模型运作过程中的各种调度。
    """

    @classmethod
    def schedule(cls, env: dict):
        """
        调度机

        Args:
            env (dict): 环境变量
            A (SystemicRiskAgent): 系统性风险主体众，可选
            A_data (AgentDataCollection): 系统性风险主体众数据集，可选

        """
        if env['state_of_schedule'] is StateOfScheduleEnum.running:
            env['state_of_schedule'] = cls.schedule_running(env['state_of_schedule'], env)
        elif env['state_of_schedule'] is StateOfScheduleEnum.collecting:
            env['state_of_schedule'] = cls.schedule_collecting(env['state_of_schedule'], env['running_mode'])
        elif env['state_of_schedule'] is StateOfScheduleEnum.initializing:
            env['state_of_schedule'] = cls.schedule_initializing(env['state_of_schedule'], env['running_mode'], env)
        elif env['state_of_schedule'] is StateOfScheduleEnum.ending:
            env['state_of_schedule'] = cls.schedule_ending(env['state_of_schedule'])
        elif env['state_of_schedule'] is StateOfScheduleEnum.idle:
            env['state_of_schedule'] = cls.schedule_idle(env['state_of_schedule'])
        else:
            raise Exception("关键词state_of_schedule取词错误".format(env['state_of_schedule']))
            pass  # if

        return env
        pass  # function


    @classmethod
    def schedule_running(cls, state_of_schedule: StateOfScheduleEnum, env: dict):
        """

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态

        Returns:
            state_of_schedule 调度状态
            env 环境变量集

        """

        ## 判断是否继续运作轮次
        if (env['round'] < env['test_max_num_of_round']):
            env['is_continue_round'] = True
        else:
            env['is_continue_round'] = False
            logging.error("                        超出最大轮次限制，强制结束运作轮次！")
            print("                        超出最大轮次限制，强制结束运作轮次！")
            pass

        ## 判断是否继续运作。只有同时满足继续运行过程、继续运行轮次时，才继续运作。否则不再继续运作。
        if (env['is_continue_round'] and env['is_continue_process']):
            env['is_continue_operation'] = True
        else:
            env['is_continue_operation'] = False
            logging.debug("                        不再继续运作。")
            pass

        ## 切换调度状态
        if env['is_continue_operation'] is True:
            state_of_schedule = StateOfScheduleEnum.collecting
        else:
            state_of_schedule = StateOfScheduleEnum.ending
        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {env['step']}，round = {env['round']}，phase = {env['phase']}")

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

        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {env['step']}，round = {env['round']}，phase = {env['phase']}")

        return state_of_schedule
        pass  # function

    @classmethod
    def schedule_initializing(cls, state_of_schedule: StateOfScheduleEnum, running_mode: str, env: dict):
        """
        调度初始状态。

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态
            running_mode (str): 运行模式
            env (dict): 环境变量集

        Returns:
            state_of_schedule: 调度状态
        """
        if running_mode == "continue running mode":
            env['is_continue_round'] = True
            env['is_continue_process'] = True
            state_of_schedule = StateOfScheduleEnum.running
        elif running_mode == "stepping running mode":  # HACK暂时不需要
            state_of_schedule = StateOfScheduleEnum.saving

        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {env['step']}，round = {env['round']}，phase = {env['phase']}")

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

        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {env['step']}，round = {env['round']}，phase = {env['phase']}")

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

        logging.debug(f"                切换调度状态为{state_of_schedule}，step = {env['step']}，round = {env['round']}，phase = {env['phase']}")

        return state_of_schedule
        pass  # function


    pass  # class
