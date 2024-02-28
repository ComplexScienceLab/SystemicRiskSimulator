"""
调度机
#状态/未适配
"""

pass  # end import

from SystemicRiskSimulator import np, logging, Optional
from SystemicRiskSimulator.core.define.define_type import StateType, MoneyType
from SystemicRiskSimulator.core.operations.collector import Collector
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_entity import Entity
# from SystemicRiskSimulator.core.define.define_module import ModelModule, ProcessModule
from SystemicRiskSimulator.core.define.define_enum import ScheduleState
from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv
# from SystemicRiskSimulator.core.operations.installer import DataInstaller

pass  # end import


class Scheduler:
    """
    调度机，负责模型运作过程中的各种调度。
    """

    # has_installed: bool = False  # 尚未调度安装

    @classmethod
    def scheduler(cls, env: dict, entity: Optional[Entity] = None):
        """
        调度机

        Args:
            env (dict): 环境变量
            A (SystemicRiskAgent): 系统性风险主体众，可选
            A_data (AgentDataCollection): 系统性风险主体众数据集，可选
            entity (Entity): 实体，可选

        Returns: env 环境变量

        """
        if sgv['state_of_schedule'] is ScheduleState.running:
            sgv['state_of_schedule'] = cls.scheduler_running(sgv['state_of_schedule'], sgv['is_step'])
            pass
        elif sgv['state_of_schedule'] is ScheduleState.collecting:
            sgv['state_of_schedule'] = cls.scheduler_collecting(sgv['state_of_schedule'], sgv['state_of_collecting'], sgv['is_step'])
            pass
        elif sgv['state_of_schedule'] is ScheduleState.loading:
            sgv['state_of_schedule'], sgv['state_of_collecting'] = cls.scheduler_loading(sgv['state_of_schedule'], sgv['state_of_collecting'], sgv['index_process'], sgv['index_stage'], sgv['loaded_index_process'], sgv['saved_index_process'], sgv['is_process'])
            pass
        elif sgv['state_of_schedule'] is ScheduleState.stepping:
            sgv['state_of_schedule'], sgv['step'], sgv['is_step'] = cls.scheduler_stepping(sgv['state_of_schedule'], sgv['step'], sgv['step_size'])
            pass
        elif sgv['state_of_schedule'] is ScheduleState.saving:
            sgv['state_of_schedule'], sgv['saved_index_process'], sgv['saved_index_stage'], sgv['loaded_index_process'], sgv['loaded_index_stage'] = cls.scheduler_saving(sgv['state_of_schedule'], sgv['index_process'], sgv['index_stage'], sgv['is_process'], sgv['index_of_schedule_position'])
            pass
        # elif sgv['state_of_schedule'] is ScheduleState.indexing:
        #     sgv['index_of_schedule_position'], sgv['state_of_schedule'] = cls.scheduler_indexing(entity)
        #     pass
        elif sgv['state_of_schedule'] is ScheduleState.initializing:
            sgv['state_of_schedule'], sgv['state_of_collecting'] = cls.scheduler_installing(sgv['state_of_schedule'], sgv['state_of_collecting'], sgv['is_step'])
            pass
        elif sgv['state_of_schedule'] is ScheduleState.idle:
            sgv['state_of_schedule'], sgv['state_of_collecting'] = cls.scheduler_idle(sgv['state_of_schedule'], sgv['state_of_collecting'])
            pass
        else:
            raise Exception("关键词state_of_schedule取词错误".format(sgv['state_of_schedule']))
            pass  # if

        return env
        pass  # method

    @classmethod
    def scheduler_loading(cls, state_of_schedule: ScheduleState, state_of_collecting: StateOfCollectingEnum, index_process: int, index_stage: int, loaded_index_process: int, loaded_index_stage: int, is_process: bool):  # HACK 暂时不需要，也还没有做对应重构。
        """
        调度读取

        Args:
            state_of_schedule (ScheduleState): 调度状态
            state_of_collecting (StateOfCollectingEnum): 收集状态
            index_process (int): 当前过程之位置
            index_stage (int): 当前阶段之位置
            loaded_index_process (int): 读取的过程之位置
            loaded_index_stage (int): 读取的阶段之位置
            is_process (bool): 是否继续过程


        Returns: state_of_schedule

        """
        logging.debug("        调度读取中……")
        ## 如果待读取过程和阶段是应该读取的过程和阶段，则继续判断，否则跳到下一阶段尝试读取
        if (index_process == loaded_index_process) & (index_stage == loaded_index_stage):
            ## 如果待读取过程不是该模型之最后一个过程之最后一个阶段，且继续运作过程，则读取成功。
            if not ((cls.get_process_index(index_process, sgv['index_of_schedule_position']) == cls.get_model_length(sgv['index_of_schedule_position'])) and (cls.get_stage_index(index_process, index_stage, sgv['index_of_schedule_position']) == cls.get_process_length(index_process, sgv['index_of_schedule_position']))) and (is_process == True):
                state_of_schedule = ScheduleState.stepping
                logging.debug("        调度读取成功。切换调度状态为%s。", state_of_schedule)
            ## 如果待读取过程是该模型之最后一个过程之最后一个阶段，且不继续运作过程，则说明程序之模型部分已经运作到终点了，此时应停止读取，然后改状态为idle。
            elif (cls.get_process_index(index_process, sgv['index_of_schedule_position']) == cls.get_model_length(sgv['index_of_schedule_position'])) and (cls.get_stage_index(index_process, index_stage, sgv['index_of_schedule_position']) == cls.get_process_length(index_process, sgv['index_of_schedule_position'])) and (is_process == False):
                state_of_schedule = ScheduleState.idle
                logging.debug("        调度读取结束。模型运行到终点了。切换调度状态为%s。", state_of_schedule)
                state_of_collecting = StateOfCollectingEnum.idle
                logging.debug("        切换收集状态为%s", state_of_collecting)
                pass  # if

            # ## 如果所处的过程未结束，则读取成功：
            # if is_process:
            #     state_of_schedule = ScheduleState.stepping
            #     logging.debug("        调度读取成功。切换调度状态为%s。", state_of_schedule)
            #     pass  # if
            # ## 如果所处的过程结束，则读取完毕，暨程序之模型部分已经运作到终点了
            # else:
            #     state_of_schedule = ScheduleState.idle
            #     logging.debug("        调度读取结束。模型运行到终点了。切换调度状态为%s。", state_of_schedule)
            #     state_of_collecting = StateOfCollectingEnum.idle
            #     logging.debug("        切换收集状态为%s", state_of_collecting)
            #     pass  # else
            # pass  # if

        return state_of_schedule, state_of_collecting
        pass  # method

    @classmethod
    def scheduler_stepping(cls, state_of_schedule: ScheduleState, step: int, step_size: int):  # HACK 暂时不需要，也还没有做对应重构。
        """
        调度步进

        Args:
            state_of_schedule (ScheduleState): 调度状态
            step (int): 步进步数
            step_size (int): 步进尺寸

        Returns:
            step (int): 步进步数, is_step (bool): 是否步进, state_of_schedule (Symbol): 调度状态

        """

        step += 1
        if step % step_size == 0:  # 是否完成本次步进:
            is_step = False
            state_of_schedule = ScheduleState.saving
            logging.debug("        步进停止。切换调度状态为%s", state_of_schedule)
        else:
            is_step = True
            pass
        return state_of_schedule, step, is_step
        pass  # method

    @classmethod
    def scheduler_running(cls, state_of_schedule: ScheduleState, is_step: bool):
        """

        Args:
            state_of_schedule (ScheduleState): 调度状态
            is_step (bool): 是否步进

        Returns: state_of_schedule 调度状态

        """
        state_of_schedule = ScheduleState.collecting
        logging.debug("        切换调度状态为%s", state_of_schedule)
        return state_of_schedule
        pass  # method

    @classmethod
    def scheduler_saving(cls, state_of_schedule: ScheduleState, index_process: int, index_stage: int, is_process: bool, index_of_schedule_position: tuple):  # HACK 暂时不需要，也还没有做对应重构。
        """
        调度存储

        Args:
            state_of_schedule (ScheduleState): 调度状态
            index_process (int): 当前过程之位置
            index_stage (int): 当前阶段之位置
            is_process (bool): 是否在过程状态中
            index_of_schedule_position (tuple): 调度位置索引列表``sgv['index_of_schedule_position']``

        Returns:
            state_of_schedule, saved_index_process, saved_index_stage, loaded_index_process, loaded_index_stage

        """

        saved_index_process = cls.get_process_index(index_process, index_of_schedule_position)
        saved_index_stage = cls.get_stage_index(index_process, index_stage, index_of_schedule_position)
        logging.debug("        存储的过程和阶段：%s，%s。", saved_index_process, saved_index_stage)

        ## 计算索引之于待读取的下一阶段
        if is_process:  # 如果所处的过程未结束，则继续判断：
            # 如果当前阶段不是其所处过程之最后一个阶段，则读取所处过程之下一阶段，
            if cls.get_stage_index(index_process, index_stage, index_of_schedule_position) < cls.get_stage_index(index_process, -1, index_of_schedule_position):
                loaded_index_process = cls.get_process_index(index_process, index_of_schedule_position)
                loaded_index_stage = cls.get_stage_index(index_process, index_stage + 1, index_of_schedule_position)
                pass  # if
            # 否则如果当前阶段是其所处过程之最后一个阶段，则读取所处过程之第一个阶段。
            else:
                loaded_index_process = cls.get_process_index(index_process, index_of_schedule_position)
                loaded_index_stage = cls.get_stage_index(index_process, 1, index_of_schedule_position)
                pass  # else
        else:  # 如果所处的过程结束，则继续判断
            # 如果当前过程不是该模型之最后一个过程，则读取当前过程之下一个过程之第一个阶段，
            if cls.get_process_index(index_process, index_of_schedule_position) < cls.get_model_length(index_of_schedule_position):
                loaded_index_process = cls.get_process_index(index_process + 1, index_of_schedule_position)
                loaded_index_stage = cls.get_stage_index(index_process + 1, 1, index_of_schedule_position)
                pass  # if
            # 否则如果当前过程是该模型之最后一个过程，则只读取当前存储的阶段，暨程序之模型部分已经运作到终点了。
            else:
                loaded_index_process = saved_index_process
                loaded_index_stage = saved_index_stage
                pass  # else
            pass  # else

        logging.debug("        下次读取的过程和阶段：%s，%s。", loaded_index_process, loaded_index_stage)

        state_of_schedule = ScheduleState.collecting
        logging.debug("        切换调度状态为%s", state_of_schedule)

        return saved_index_process, saved_index_stage, loaded_index_process, loaded_index_stage, state_of_schedule
        pass  # method

    @classmethod
    def scheduler_collecting(cls, state_of_schedule: ScheduleState, state_of_collecting: StateOfCollectingEnum, is_step: bool):
        """
        调度搜集数据

        Args:
            state_of_schedule (ScheduleState): 调度状态
            state_of_collecting (StateOfCollectingEnum) :收集状态
            is_step (bool): 是否步进

        Returns:
            state_of_schedule 调度状态

        """

        ## 如果不步进
        if is_step is False and state_of_collecting is StateOfCollectingEnum.running:
            state_of_schedule = ScheduleState.running
        elif is_step is False and state_of_collecting is StateOfCollectingEnum.idle:
            state_of_schedule = ScheduleState.idle
        ## 如果步进
        elif is_step is True:
            state_of_schedule = ScheduleState.loading

        logging.debug("        切换调度状态为%s", state_of_schedule)

        return state_of_schedule
        pass  # method

    @classmethod
    def scheduler_indexing(cls, state_of_schedule: ScheduleState, entity: Entity):  # TODO 移走  #HACK 暂时不需要，也还没有做对应重构。
        """
        调度索引状态。HACK 无用

        Args:
            state_of_schedule (ScheduleState): 调度状态
            entity (Entity):被调度的实体（针对模型实体）

        Returns:
            index_of_schedule_position 调度位置索引列表, state_of_schedule 调度状态
        """
        index_of_schedule_position = []
        for i in range(len(entity.content)):
            index_of_schedule_position_stages = tuple((j + 1 for j in range(len(entity.content[i].content))))  # 获取过程的内容，暨阶段
            index_of_schedule_position_processes = tuple((i + 1, index_of_schedule_position_stages))
            index_of_schedule_position.append(index_of_schedule_position_processes)  # 获取模型的内容，暨过程
            # index_of_schedule_position+=tuple(((index_of_schedule_position_processes)))
            pass
        del index_of_schedule_position_processes, index_of_schedule_position_stages
        index_of_schedule_position = tuple(index_of_schedule_position)
        logging.debug("        模型%s索引完成。值为：%s", entity.functionName, index_of_schedule_position)

        state_of_schedule = ScheduleState.saving
        logging.debug("        切换调度状态为%s", state_of_schedule)

        return state_of_schedule, index_of_schedule_position
        pass  # method

    @classmethod
    def scheduler_installing(cls, state_of_schedule: ScheduleState, state_of_collecting: StateOfCollectingEnum, is_step: bool):
        """
        调度安装状态。

        Args:
            state_of_schedule (ScheduleState): 调度状态
            state_of_collecting (StateOfCollectingEnum): 收集状态
            is_step (bool): 是否步进

        Returns:
            state_of_schedule: 调度状态, state_of_collecting: 收集状态
        """
        if is_step is False:
            state_of_schedule = ScheduleState.running
        else:
            state_of_schedule = ScheduleState.saving
        state_of_collecting = StateOfCollectingEnum.running

        logging.debug("        切换调度状态为%s", state_of_schedule)
        logging.debug("        切换收集状态为%s", state_of_collecting)

        return state_of_schedule, state_of_collecting
        pass  # method

    @classmethod
    def scheduler_idle(cls, state_of_schedule: ScheduleState, state_of_collecting: StateOfCollectingEnum):
        """

        Args:
            state_of_schedule (ScheduleState): 调度状态
            state_of_collecting (StateOfCollectingEnum): 收集状态

        Returns:
             state_of_schedule: 调度状态, state_of_collecting: 收集状态
        """
        state_of_schedule = ScheduleState.initializing
        state_of_collecting = StateOfCollectingEnum.initializing

        logging.debug("        切换调度状态为%s", state_of_schedule)
        logging.debug("        切换收集状态为%s", state_of_collecting)

        return state_of_schedule, state_of_collecting
        pass  # method

    @classmethod
    def get_process_index(cls, index_process: int, index_of_schedule_position: tuple):  # HACK 暂时不需要，也还没有做对应重构。
        """
        获取过程之索引。

        Args:
            index_process (int): 过程之索引
            index_of_schedule_position (tuple): 调度位置索引

        Returns: 过程之索引

        """
        return index_of_schedule_position[index_process - 1][0]
        pass

    @classmethod
    def get_stage_index(cls, index_process: int, index_stage: int, index_of_schedule_position: tuple):  # HACK 暂时不需要，也还没有做对应重构。
        """
        获取阶段之索引。

        Args:
            index_process (int): 过程之索引
            index_stage (int): 阶段之索引
            index_of_schedule_position (tuple): 调度位置索引

        Returns: 阶段之索引

        """
        if index_stage == -1:
            return index_of_schedule_position[index_process - 1][1][-1]
        else:
            return index_of_schedule_position[index_process - 1][1][index_stage - 1]
        pass

    @classmethod
    def get_model_length(cls, index_of_schedule_position: tuple):  # HACK 暂时不需要，也还没有做对应重构。
        """
        获取模型之内容之列表之长度（暨过程个数）

        Args:
            index_of_schedule_position (tuple):

        Returns: 过程个数

        """
        return len(index_of_schedule_position)
        pass

    @classmethod
    def get_process_length(cls, index_process: int, index_of_schedule_position: tuple):  # HACK 暂时不需要，也还没有做对应重构。
        """
        获取过程之内容之列表之长度（暨该过程之阶段个数）

        Args:
            index_process (int):
            index_of_schedule_position (tuple):

        Returns: 过程之阶段个数

        """
        return len(index_of_schedule_position[index_process - 1])
        pass

    # @classmethod
    # def is_process(cls, A: SystemicRiskAgent, BB_isv_t1: StateType, BB_Shock_t_t1: MoneyType, is_process: bool, stageFunctionName: str, process: ProcessModule):
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
    #                 process.entity_name == 'processEntity_ExBankInsolvent' or
    #                 process.entity_name == 'processEntity_ExBankIlliquity' or
    #                 process.entity_name == 'process_exBank_bankrupt'
    #         ):
    #             is_process = False
    #             logging.debug("        结束过程：%s。", sgv['process_name'])
    #             pass
    #         elif (
    #                 process.entity_name == 'processEntity_InterBankInsolvent'
    #         ):
    #             if A.BB.isv.all() == BB_isv_t1.all():  # 判断是否继续运作过程: #BUG，可能存在逻辑问题:
    #                 is_process = False
    #                 logging.debug("        结束过程：%s。", sgv['process_name'])
    #                 pass
    #         else:
    #             if A.BB.Shock_t.all() == BB_Shock_t_t1.all():  # 判断是否继续运作过程:
    #                 is_process = False
    #                 logging.debug("        结束过程：%s。", sgv['process_name'])
    #                 pass
    #             pass  # if:
    #     else:
    #         is_process = True
    #         logging.info("继续过程：%s。", sgv['process_name'])
    #         pass  # if:
    #
    #     return is_process
    #     pass  # method

    @classmethod
    def is_process(cls, A: SystemicRiskAgent, BB_isv_t1: StateType, BB_Shock_t_t1: MoneyType, is_process: bool, stageFunctionName: str, process: ProcessModule):  # HACK 暂时不需要，也还没有做对应重构。
        """
        判断是否继续运作过程

        Args:
            A (SystemicRiskAgent): Agent群变量
            BB_isv_t1 (StateType): 商业银行之资不抵债之状态，于时期1
            BB_Shock_t_t1 (MoneyType): 商业银行受到的冲击，于时期1
            is_process (bool): 是否在运作过程状态
            stageFunctionName (str): 阶段函数名称
            process (ProcessModule): 过程

        Returns: is_process

        """
        if stageFunctionName == process.content[-1].entity_name:  # 如果当前阶段是所处过程之最后的阶段，则继续判断，否则过程未结束，后续继续运作。:
            if (
                    process.functionName == 'processEntity_ExBankInsolvent' or
                    process.functionName == 'processEntity_ExBankIlliquity' or
                    process.functionName == 'processEntity_ExBankBankrupt'
            ):
                is_process = False
                logging.debug("        结束过程：%s。", sgv['process_name'])
                pass
            elif (
                    process.functionName == 'processEntity_InterBankInsolvent'
            ):
                if A.BB.isv.all() == BB_isv_t1.all():  # 判断是否继续运作过程: #BUG，可能存在逻辑问题:
                    is_process = False
                    logging.debug("        结束过程：%s。", sgv['process_name'])
                    pass
            else:
                if A.BB.Shock_t.all() == BB_Shock_t_t1.all():  # 判断是否继续运作过程:
                    is_process = False
                    logging.debug("        结束过程：%s。", sgv['process_name'])
                    pass
                pass  # if:
        else:
            is_process = True
            logging.info("继续过程：%s。", sgv['process_name'])
            pass  # if:

        return is_process
        pass  # method

    @classmethod
    def is_round(cls, env: dict):  # HACK 暂时不需要，也还没有做对应重构。
        """判断是否继续运作回合"""
        if (sgv['round'] < sgv['max_num_of_round']):
            sgv['is_round'] = True
        else:
            sgv['is_round'] = False
            logging.debug("        结束回合%s。", sgv['process_name'])
            pass
        pass  # method

    @classmethod
    def is_step(cls, env: dict):  # HACK 暂时不需要，也还没有做对应重构。
        """判断是否继续步进"""
        if ~sgv['is_step']:
            logging.debug("        暂时跳出模型%s之过程%s之阶段%s。", sgv['model_name'], sgv['process_name'], sgv['stage_name'])
            pass
        pass  # method

    @classmethod
    def is_loop(cls, env: dict):  # HACK 暂时不需要，也还没有做对应重构。
        """
        判断是否继续运作循环。
        只有同时满足继续运作过程、继续步进、继续运作回合时，才继续运作循环。否则跳出循环。
        """
        if (sgv['is_process'] and sgv['is_step'] and sgv['is_round']):
            sgv['is_loop'] = True
        else:
            sgv['is_loop'] = False
            logging.debug("        跳出过程%s之循环。\n", sgv['process_name'])
            pass
        pass  # method

    pass  # class

