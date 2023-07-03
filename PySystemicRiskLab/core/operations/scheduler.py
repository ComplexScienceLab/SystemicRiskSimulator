"""
调度机
"""

from PySystemicRiskLab import np, logging, Optional
# from PySystemicRiskLab.core.define.define_type import StateType, MoneyType
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
# from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
# from PySystemicRiskLab.core.define.define_environmentVariables import env

# from PySystemicRiskLab.core.operations.collector import Collector

pass  # end import


class Scheduler:
    """
    调度机，负责模型运作过程中的各种调度。
    """

    # ## NOTE：调度机，以装饰器形式，调度各功能函数。
    # # @classmethod
    # # def scheduler(cls, env: dict, A: SystemicRiskAgent, A_data: AgentDataCollection):
    # @classmethod
    # def scheduler(cls, func):
    #     """
    #     调度机装饰器
    #
    #     Args:
    #         func ():
    #
    #     Returns:
    #
    #     """
    #     def decorator(*args, **kwargs):
    #         ## 执行函数
    #         kwargs['env'] = Scheduler.schedule(kwargs['env'])  # 调度状态变成`running`
    #         func(*args, **kwargs)  # 真正执行函数的地方
    #
    #         ## 收集数据 #BUG #NOW 改成每执行一步都搜集数据
    #         kwargs['env'] = Scheduler.schedule(kwargs['env'])  # 调度状态变成`collecting`
    #         kwargs['A_data'], kwargs['env'] = Collector.collect(kwargs['A'], kwargs['A_data'], kwargs['env'])
    #
    #         logging.debug("运行一次调度")
    #         pass
    #
    #     return decorator

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
            env['state_of_schedule'] = cls.schedule_running(env['state_of_schedule'], env['is_continue_process'])
        elif env['state_of_schedule'] is StateOfScheduleEnum.collecting:
            env['state_of_schedule'] = cls.schedule_collecting(env['state_of_schedule'], env['running_mode'])
        # elif env['state_of_schedule'] is StateOfScheduleEnum.loading:
        #     env['state_of_schedule'] = cls.schedule_loading(env['state_of_schedule'], env['index_process'], env['index_stage'], env['loaded_index_process'], env['saved_index_process'], env['is_continue_process'])
        # elif env['state_of_schedule'] is StateOfScheduleEnum.stepping:
        #     env['state_of_schedule'], env['step'], env['is_step'] = cls.schedule_stepping(env['state_of_schedule'], env['step'], env['step_size'])
        # elif env['state_of_schedule'] is StateOfScheduleEnum.saving:
        #     env['state_of_schedule'], env['saved_index_process'], env['saved_index_stage'], env['loaded_index_process'], env['loaded_index_stage'] = cls.schedule_saving(env['state_of_schedule'], env['index_process'], env['index_stage'], env['is_process'], env['index_of_schedule_position'])
        # elif env['state_of_schedule'] is StateOfScheduleEnum.indexing:
        #     env['index_of_schedule_position'], env['state_of_schedule'] = cls.schedule_indexing(entity)
        elif env['state_of_schedule'] is StateOfScheduleEnum.initializing:
            env['state_of_schedule'] = cls.schedule_initializing(env['state_of_schedule'], env['running_mode'])
        elif env['state_of_schedule'] is StateOfScheduleEnum.ending:
            env['state_of_schedule'] = cls.schedule_ending(env['state_of_schedule'])
        elif env['state_of_schedule'] is StateOfScheduleEnum.idle:
            env['state_of_schedule'] = cls.schedule_idle(env['state_of_schedule'])
        else:
            raise Exception("关键词state_of_schedule取词错误".format(env['state_of_schedule']))
            pass  # if

        return env
        pass  # method

    # @classmethod
    # def schedule_loading(cls, state_of_schedule: StateOfScheduleEnum, index_process: int, index_stage: int, loaded_index_process: int, loaded_index_stage: int, is_process: bool):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """
    #     调度读取
    #
    #     Args:
    #         state_of_schedule (StateOfScheduleEnum): 调度状态
    #         index_process (int): 当前过程之位置
    #         index_stage (int): 当前阶段之位置
    #         loaded_index_process (int): 读取的过程之位置
    #         loaded_index_stage (int): 读取的阶段之位置
    #         is_process (bool): 是否继续过程
    #
    #
    #     Returns: state_of_schedule: 调度状态
    #
    #     """
    #     logging.debug("                        调度读取中……")
    #     ## 如果待读取过程和阶段是应该读取的过程和阶段，则继续判断，否则跳到下一阶段尝试读取
    #     if (index_process == loaded_index_process) & (index_stage == loaded_index_stage):
    #         ## 如果待读取过程不是该模型之最后一个过程之最后一个阶段，且继续运作过程，则读取成功。
    #         if not ((cls.get_process_index(index_process, env['index_of_schedule_position']) == cls.get_model_length(env['index_of_schedule_position'])) and (cls.get_stage_index(index_process, index_stage, env['index_of_schedule_position']) == cls.get_process_length(index_process, env['index_of_schedule_position']))) and (is_process == True):
    #             state_of_schedule = StateOfScheduleEnum.stepping
    #             logging.debug("                        调度读取成功。切换调度状态为%s。", state_of_schedule)
    #         ## 如果待读取过程是该模型之最后一个过程之最后一个阶段，且不继续运作过程，则说明程序之模型部分已经运作到终点了，此时应停止读取，然后改状态为idle。
    #         elif (cls.get_process_index(index_process, env['index_of_schedule_position']) == cls.get_model_length(env['index_of_schedule_position'])) and (cls.get_stage_index(index_process, index_stage, env['index_of_schedule_position']) == cls.get_process_length(index_process, env['index_of_schedule_position'])) and (is_process == False):
    #             state_of_schedule = StateOfScheduleEnum.ending
    #             logging.debug("                        调度读取结束。模型运行到终点了。切换调度状态为%s。", state_of_schedule)
    #             pass  # if
    #
    #         # ## 如果所处的过程未结束，则读取成功：
    #         # if is_process:
    #         #     state_of_schedule = StateOfScheduleEnum.stepping
    #         #     logging.debug("                        调度读取成功。切换调度状态为%s。", state_of_schedule)
    #         #     pass  # if
    #         # ## 如果所处的过程结束，则读取完毕，暨程序之模型部分已经运作到终点了
    #         # else:
    #         #     state_of_schedule = StateOfScheduleEnum.ending
    #         #     logging.debug("                        调度读取结束。模型运行到终点了。切换调度状态为%s。", state_of_schedule)
    #         #     pass  # else
    #         # pass  # if
    #
    #     return state_of_schedule
    #     pass  # method

    # @classmethod
    # def schedule_stepping(cls, state_of_schedule: StateOfScheduleEnum, step: int, step_size: int):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """
    #     调度步进
    #
    #     Args:
    #         state_of_schedule (StateOfScheduleEnum): 调度状态
    #         step (int): 步进步数
    #         step_size (int): 步进尺寸
    #
    #     Returns:
    #         step (int): 步进步数, is_step (bool): 是否步进, state_of_schedule (Symbol): 调度状态
    #
    #     """
    #
    #     step += 1
    #     if step % step_size == 0:  # 是否完成本次步进:
    #         is_step = False
    #         state_of_schedule = StateOfScheduleEnum.saving
    #         logging.debug("                        步进停止。切换调度状态为%s", state_of_schedule)
    #     else:
    #         is_step = True
    #         pass
    #     return state_of_schedule, step, is_step
    #     pass  # method

    @classmethod
    def schedule_running(cls, state_of_schedule: StateOfScheduleEnum, is_continue_process: bool):
        """

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态
            is_continue_process (bool) 是否继续运行过程

        Returns: state_of_schedule 调度状态

        """
        if is_continue_process is True:
            state_of_schedule = StateOfScheduleEnum.collecting
        else:
            state_of_schedule = StateOfScheduleEnum.ending
        logging.debug("                        切换调度状态为%s", state_of_schedule)

        return state_of_schedule
        pass  # method

    # @classmethod
    # def schedule_saving(cls, state_of_schedule: StateOfScheduleEnum, index_process: int, index_stage: int, is_process: bool, index_of_schedule_position: tuple):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """
    #     调度存储
    #
    #     Args:
    #         state_of_schedule (StateOfScheduleEnum): 调度状态
    #         index_process (int): 当前过程之位置
    #         index_stage (int): 当前阶段之位置
    #         is_process (bool): 是否在过程状态中
    #         index_of_schedule_position (tuple): 调度位置索引列表``env['index_of_schedule_position']``
    #
    #     Returns:
    #         state_of_schedule, saved_index_process, saved_index_stage, loaded_index_process, loaded_index_stage
    #
    #     """
    #
    #     saved_index_process = cls.get_process_index(index_process, index_of_schedule_position)
    #     saved_index_stage = cls.get_stage_index(index_process, index_stage, index_of_schedule_position)
    #     logging.debug("                        存储的过程和阶段：%s，%s。", saved_index_process, saved_index_stage)
    #
    #     ## 计算索引之于待读取的下一阶段
    #     if is_process:  # 如果所处的过程未结束，则继续判断：
    #         # 如果当前阶段不是其所处过程之最后一个阶段，则读取所处过程之下一阶段，
    #         if cls.get_stage_index(index_process, index_stage, index_of_schedule_position) < cls.get_stage_index(index_process, -1, index_of_schedule_position):
    #             loaded_index_process = cls.get_process_index(index_process, index_of_schedule_position)
    #             loaded_index_stage = cls.get_stage_index(index_process, index_stage + 1, index_of_schedule_position)
    #             state_of_schedule = StateOfScheduleEnum.collecting
    #             pass  # if
    #         # 否则如果当前阶段是其所处过程之最后一个阶段，则读取所处过程之第一个阶段。
    #         else:
    #             loaded_index_process = cls.get_process_index(index_process, index_of_schedule_position)
    #             loaded_index_stage = cls.get_stage_index(index_process, 1, index_of_schedule_position)
    #             state_of_schedule = StateOfScheduleEnum.collecting
    #             pass  # else
    #     else:  # 如果所处的过程结束，则继续判断
    #         # 如果当前过程不是该模型之最后一个过程，则读取当前过程之下一个过程之第一个阶段，
    #         if cls.get_process_index(index_process, index_of_schedule_position) < cls.get_model_length(index_of_schedule_position):
    #             loaded_index_process = cls.get_process_index(index_process + 1, index_of_schedule_position)
    #             loaded_index_stage = cls.get_stage_index(index_process + 1, 1, index_of_schedule_position)
    #             state_of_schedule = StateOfScheduleEnum.collecting
    #             pass  # if
    #         # 否则如果当前过程是该模型之最后一个过程，则只读取当前存储的阶段，暨程序之模型部分已经运作到终点了。
    #         else:
    #             loaded_index_process = saved_index_process
    #             loaded_index_stage = saved_index_stage
    #             state_of_schedule = StateOfScheduleEnum.ending
    #             pass  # else
    #         pass  # else
    #
    #     logging.debug("                        下次读取的过程和阶段：%s，%s。", loaded_index_process, loaded_index_stage)
    #
    #     logging.debug("                        切换调度状态为%s", state_of_schedule)
    #
    #     return saved_index_process, saved_index_stage, loaded_index_process, loaded_index_stage, state_of_schedule
    #     pass  # method

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
        elif running_mode == "step mode":
            state_of_schedule = StateOfScheduleEnum.loading

        logging.debug("                        切换调度状态为%s", state_of_schedule)

        return state_of_schedule
        pass  # method

    # @classmethod
    # def schedule_indexing(cls, state_of_schedule: StateOfScheduleEnum, entity: Entity):  # TODO 移走  #HACK 暂时不需要，也还没有做对应重构。
    #     """
    #     调度索引状态。HACK 无用
    #
    #     Args:
    #         state_of_schedule (StateOfScheduleEnum): 调度状态
    #         entity (Entity):被调度的实体（针对模型实体）
    #
    #     Returns:
    #         index_of_schedule_position 调度位置索引列表, state_of_schedule 调度状态
    #     """
    #     index_of_schedule_position = []
    #     for i in range(len(entity.content)):
    #         index_of_schedule_position_stages = tuple((j + 1 for j in range(len(entity.content[i].content))))  # 获取过程的内容，暨阶段
    #         index_of_schedule_position_processes = tuple((i + 1, index_of_schedule_position_stages))
    #         index_of_schedule_position.append(index_of_schedule_position_processes)  # 获取模型的内容，暨过程
    #         # index_of_schedule_position+=tuple(((index_of_schedule_position_processes)))
    #         pass
    #     del index_of_schedule_position_processes, index_of_schedule_position_stages
    #     index_of_schedule_position = tuple(index_of_schedule_position)
    #     logging.debug("                        模型%s索引完成。值为：%s", entity.functionName, index_of_schedule_position)
    #
    #     state_of_schedule = StateOfScheduleEnum.saving
    #     logging.debug("                        切换调度状态为%s", state_of_schedule)
    #
    #     return state_of_schedule, index_of_schedule_position
    #     pass  # method

    @classmethod
    def schedule_initializing(cls, state_of_schedule: StateOfScheduleEnum, running_mode: str):
        """
        调度初始状态。

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态
            running_mode (str): 运行模式

        Returns:
            state_of_schedule: 调度状态
        """
        if running_mode == "continue running mode":
            state_of_schedule = StateOfScheduleEnum.running
        elif running_mode == "step mode":
            state_of_schedule = StateOfScheduleEnum.saving

        logging.debug("                        切换调度状态为%s", state_of_schedule)

        return state_of_schedule
        pass  # method

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

        logging.debug("                        切换调度状态为%s", state_of_schedule)

        return state_of_schedule
        pass  # method

    @classmethod
    def schedule_idle(cls, state_of_schedule: StateOfScheduleEnum):
        """

        Args:
            state_of_schedule (StateOfScheduleEnum): 调度状态

        Returns:
             state_of_schedule: 调度状态
        """
        state_of_schedule = StateOfScheduleEnum.initializing

        logging.debug("                        切换调度状态为%s", state_of_schedule)

        return state_of_schedule
        pass  # method

    # @classmethod
    # def get_process_index(cls, index_process: int, index_of_schedule_position: tuple):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """
    #     获取过程之索引。
    #
    #     Args:
    #         index_process (int): 过程之索引
    #         index_of_schedule_position (tuple): 调度位置索引
    #
    #     Returns: 过程之索引
    #
    #     """
    #     return index_of_schedule_position[index_process - 1][0]
    #     pass

    # @classmethod
    # def get_stage_index(cls, index_process: int, index_stage: int, index_of_schedule_position: tuple):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """
    #     获取阶段之索引。
    #
    #     Args:
    #         index_process (int): 过程之索引
    #         index_stage (int): 阶段之索引
    #         index_of_schedule_position (tuple): 调度位置索引
    #
    #     Returns: 阶段之索引
    #
    #     """
    #     if index_stage == -1:
    #         return index_of_schedule_position[index_process - 1][1][-1]
    #     else:
    #         return index_of_schedule_position[index_process - 1][1][index_stage - 1]
    #     pass

    # @classmethod
    # def get_model_length(cls, index_of_schedule_position: tuple):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """
    #     获取模型之内容之列表之长度（暨过程个数）
    #
    #     Args:
    #         index_of_schedule_position (tuple):
    #
    #     Returns: 过程个数
    #
    #     """
    #     return len(index_of_schedule_position)
    #     pass

    # @classmethod
    # def get_process_length(cls, index_process: int, index_of_schedule_position: tuple):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """
    #     获取过程之内容之列表之长度（暨该过程之阶段个数）
    #
    #     Args:
    #         index_process (int):
    #         index_of_schedule_position (tuple):
    #
    #     Returns: 过程之阶段个数
    #
    #     """
    #     return len(index_of_schedule_position[index_process - 1])
    #     pass

    # @classmethod
    # def is_process(cls, A: SystemicRiskAgent, BB_isv_t1: StateType, BB_Shock_t_t1: MoneyType, is_process: bool, stageFunctionName: str, process):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """
    #     判断是否继续运作过程
    #
    #     Args:
    #         A (SystemicRiskAgent): Agent群变量
    #         BB_isv_t1 (StateType): 商业银行之资不抵债之状态，于时期1
    #         BB_Shock_t_t1 (MoneyType): 商业银行受到的冲击，于时期1
    #         is_process (bool): 是否在运作过程状态
    #         stageFunctionName (str): 阶段函数名称
    #         process (ProcessModule): 过程
    #
    #     Returns: is_process
    #
    #     """
    #     if stageFunctionName == process.content[-1].entity_name:  # 如果当前阶段是所处过程之最后的阶段，则继续判断，否则过程未结束，后续继续运作。:
    #         if (
    #                 process.functionName == 'processEntity_ExBankInsolvent' or
    #                 process.functionName == 'processEntity_ExBankIlliquid' or
    #                 process.functionName == 'processEntity_ExBankBankrupt'
    #         ):
    #             is_process = False
    #             logging.debug("                        结束过程：%s。", env['process_name'])
    #             pass
    #         elif (
    #                 process.functionName == 'processEntity_InterBankInsolvent'
    #         ):
    #             if A.BB.isv.all() == BB_isv_t1.all():  # 判断是否继续运作过程: #BUG，可能存在逻辑问题:
    #                 is_process = False
    #                 logging.debug("                        结束过程：%s。", env['process_name'])
    #                 pass
    #         else:
    #             if A.BB.Shock_t.all() == BB_Shock_t_t1.all():  # 判断是否继续运作过程:
    #                 is_process = False
    #                 logging.debug("                        结束过程：%s。", env['process_name'])
    #                 pass
    #             pass  # if:
    #     else:
    #         is_process = True
    #         logging.info("继续过程：%s。", env['process_name'])
    #         pass  # if:
    #
    #     return is_process
    #     pass  # method

    # @classmethod
    # def is_round(cls, env: dict):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """判断是否继续运作回合"""
    #     if (env['round'] < env['test_max_num_of_round']):
    #         env['is_round'] = True
    #     else:
    #         env['is_round'] = False
    #         logging.debug("                        结束回合%s。", env['process_name'])
    #         pass
    #     pass  # method

    # @classmethod
    # def is_step(cls, env: dict):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """判断是否继续步进"""
    #     if ~env['is_step']:
    #         logging.debug("                        暂时跳出模型%s之过程%s之阶段%s。", env['model_name'], env['process_name'], env['stage_name'])
    #         pass
    #     pass  # method

    # @classmethod
    # def is_loop(cls, env: dict):  # HACK 暂时不需要。还没有做对应重构，已经不能直接用于当前版本的程序了。
    #     """
    #     判断是否继续运作循环。
    #     只有同时满足继续运作过程、继续步进、继续运作回合时，才继续运作循环。否则跳出循环。
    #     """
    #     if (env['is_process'] and env['is_step'] and env['is_round']):
    #         env['is_loop'] = True
    #     else:
    #         env['is_loop'] = False
    #         logging.debug("                        跳出过程%s之循环。\n", env['process_name'])
    #         pass
    #     pass  # method

    pass  # class
