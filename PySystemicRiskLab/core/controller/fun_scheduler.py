"调度器"

## 调度器

##########################################
# 状态/开发
##########################################

# from PySystemicRiskLab.core import np, env, SystemicRiskAgent, AgentDataCollection, StateOfScheduleEnum, ModelComponent, ModelCollector
import logging

pass  # end import

from PySystemicRiskLab import np, logging
from PySystemicRiskLab.core.define.define_type import TypeState, TypeMoney
from PySystemicRiskLab.core.controller.model_collector import ModelCollector
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_component import ModelComponent, ProcessComponent
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
from PySystemicRiskLab.core.define.define_environment_variables import env

pass  # end import


class ModelScheduler:

    # @classmethod
    # def __init__(cls, env:dict):
    #     env: dict = env  # HACK 没用
    #     pass

    @classmethod
    def scheduler(cls, env: dict, A: SystemicRiskAgent, A_data: AgentDataCollection):
        """
        函数：调度器 #HACK 或将废弃

        Args:
            env (dict): 环境参数
            A (SystemicRiskAgent): 系统性风险主体众
            A_data (AgentDataCollection): 系统性风险主体众数据集

        Returns:

        """

        if env['state_of_schedule'] == StateOfScheduleEnum.loading:
            env['state_of_schedule'] = cls.scheduler_loading(env['index_process'], env['index_stage'], env['loaded_index_process'], env['saved_index_process'], env['state_of_schedule'], env['is_process'])  # 读取
            pass
        if env['state_of_schedule'] == StateOfScheduleEnum.stepping:
            env['step'], env['is_step'], env['state_of_schedule'] = cls.scheduler_stepping(env['step'], env['step_size'])  # 步进
            pass
        if env['state_of_schedule'] == StateOfScheduleEnum.saving:
            env['saved_index_process'], env['saved_index_stage'], env['loaded_index_process'], env['loaded_index_stage'], env['state_of_schedule'] = cls.scheduler_saving(env['index_process'], env['index_stage'], env['is_process'], env['index_of_schedule_position'])  # 存储
            pass
        if env['state_of_schedule'] == StateOfScheduleEnum.collecting:
            env['state_of_schedule'] = cls.scheduler_collecting(A, A_data)
            pass
        # if (state_of_schedule == StateOfScheduleEnum.indexing): #HACK 冗余:
        #     env['index_of_schedule_position'], env['state_of_schedule'] = cls.scheduler_indexing(component) # 索引
        #     pass
        pass  # functions

    @classmethod
    def scheduler_indexing(cls, model: ModelComponent) -> (tuple, object):  # BUG Py版本中下标起始为0导致读取和存储过程数组时，出现问题，需要修复。
        """
        调度索引。

        完成索引后，切换调度状态为``saving``。

        Args:
            model (ModelComponent):被调度的模型内容

        Returns:
            index_of_schedule_position 调度位置索引列表, state_of_schedule 调度状态
        """
        index_of_schedule_position = []
        for i in range(len(model.content)):
            index_of_schedule_position_stages = tuple((j + 1 for j in range(len(model.content[i].content))))  # 获取过程的内容，暨阶段
            index_of_schedule_position_processes = tuple((i + 1, index_of_schedule_position_stages))
            index_of_schedule_position.append(index_of_schedule_position_processes)  # 获取模型的内容，暨过程
            # index_of_schedule_position+=tuple(((index_of_schedule_position_processes)))
            pass
        del index_of_schedule_position_processes, index_of_schedule_position_stages
        index_of_schedule_position = tuple(index_of_schedule_position)
        logging.debug("模型%s索引完成。值为：%s", model.functionName, index_of_schedule_position)
        state_of_schedule = StateOfScheduleEnum.saving  # 切换调度状态为``saving``
        logging.debug("切换调度运作状态为%s", state_of_schedule)
        return index_of_schedule_position, state_of_schedule
        pass  # function

    @classmethod
    def scheduler_loading(cls, index_process: int, index_stage: int, loaded_index_process: int, loaded_index_stage: int, state_of_schedule: StateOfScheduleEnum, is_process: bool):
        """
        函数：调度读取

        Args:
            index_process (int): 当前过程之位置
            index_stage (int): 当前阶段之位置
            loaded_index_process (int): 读取的过程之位置
            loaded_index_stage (int): 读取的阶段之位置
            state_of_schedule (Symbol): 调度状态
            is_process (bool): 是否继续过程


        Returns: newStateOfSchedule

        """
        logging.debug("调度读取中……")
        newStateOfSchedule = state_of_schedule
        # 如果待读取过程和阶段是应该读取的过程和阶段，则继续判断，否则跳到下一阶段尝试读取
        if (index_process == loaded_index_process) & (index_stage == loaded_index_stage):
            pass  # if
            # 如果待读取过程不是该模型之最后一个过程之最后一个阶段，且继续运行过程，则读取成功。
            if not ((cls.get_process_index(index_process, env['index_of_schedule_position']) == cls.get_model_length(env['index_of_schedule_position'])) and (cls.get_stage_index(index_process, index_stage, env['index_of_schedule_position']) == cls.get_process_length(index_process, env['index_of_schedule_position']))) and (is_process == True):
                newStateOfSchedule = StateOfScheduleEnum.stepping  # 切换调度运作状态为步进
                logging.debug("调度读取成功。切换调度运作状态为%s。", newStateOfSchedule)
            # 如果待读取过程是该模型之最后一个过程之最后一个阶段，且不继续运行过程，则说明程序之模型部分已经运行到终点了，此时应停止读取，然后改状态为idle。
            elif (cls.get_process_index(index_process, env['index_of_schedule_position']) == cls.get_model_length(env['index_of_schedule_position'])) and (cls.get_stage_index(index_process, index_stage, env['index_of_schedule_position']) == cls.get_process_length(index_process, env['index_of_schedule_position'])) and (is_process == False):
                newStateOfSchedule = StateOfScheduleEnum.idle  # 切换调度运作状态为待命
                pass

            # 如果所处的过程未结束，则读取成功：
            if is_process:
                newStateOfSchedule = StateOfScheduleEnum.stepping  # 切换调度运作状态为步进
                logging.debug("调度读取成功。切换调度运作状态为%s。", newStateOfSchedule)
                pass  # if
            # 如果所处的过程结束，则读取完毕，暨程序之模型部分已经运行到终点了
            else:
                newStateOfSchedule = StateOfScheduleEnum.idle  # 切换调度运作状态为待命
                pass  # else
            pass  # if

        return newStateOfSchedule
        pass  # function

    @classmethod
    def scheduler_stepping(cls, step: int, step_size: int):
        """
        函数：调度步进

        Args:
            step (int): 步进步数
            step_size (int): 步进尺寸

        Returns:
            step (int): 步进步数, is_step (bool): 是否步进, state_of_schedule (Symbol): 调度状态

        """

        step += 1
        if step % step_size == 0:  # 是否完成本次步进:
            is_step = False
            state_of_schedule = StateOfScheduleEnum.saving  # 切换调度运作状态为存储
            logging.debug("步进停止。切换调度运作状态为%s", state_of_schedule)
        else:
            is_step = True
            state_of_schedule = StateOfScheduleEnum.stepping
            logging.debug("步进继续：")
            pass
        return step, is_step, state_of_schedule
        pass  # function

    @classmethod
    def scheduler_saving(cls, index_process: int, index_stage: int, is_process: bool, index_of_schedule_position: tuple):
        """
        函数：调度存储

        Args:
            index_process (int): 当前过程之位置
            index_stage (int): 当前阶段之位置
            is_process (bool): 是否在过程状态中
            index_of_schedule_position (tuple): 调度位置索引列表``env['index_of_schedule_position']``

        Returns: saved_index_process, saved_index_stage, loaded_index_process, loaded_index_stage, state_of_schedule

        """

        saved_index_process = cls.get_process_index(index_process, index_of_schedule_position)
        saved_index_stage = cls.get_stage_index(index_process, index_stage, index_of_schedule_position)
        logging.debug("存储的过程和阶段：%s，%s。", saved_index_process, saved_index_stage)

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
            # 否则如果当前过程是该模型之最后一个过程，则只读取当前存储的阶段，暨程序之模型部分已经运行到终点了。
            else:
                loaded_index_process = saved_index_process
                loaded_index_stage = saved_index_stage
                pass  # else
            pass  # else

        logging.debug("下次读取的过程和阶段：%s，%s。", loaded_index_process, loaded_index_stage)

        state_of_schedule = StateOfScheduleEnum.collecting  # 切换调度运作状态为收集数据
        logging.debug("切换调度运作状态为%s", state_of_schedule)

        return saved_index_process, saved_index_stage, loaded_index_process, loaded_index_stage, state_of_schedule
        pass  # function

    @classmethod
    def scheduler_collecting(cls, A: SystemicRiskAgent, A_data: AgentDataCollection = np.nan, env: dict = env):
        """
        函数：调度搜集数据

        Args:
            A (SystemicRiskAgent): Agent群变量
            A_data (AgentDataCollection): Agent群变量之数据
            env (dict): 环境变量

        Returns: state_of_schedule: Symbol: 调度状态；

        """
        logging.debug("收集数据：")
        env['id_data'] += 1  # 累加数据帧ID号
        ModelCollector.collector(A, A_data, env['state_of_process'], env)  # 收集数据
        state_of_schedule = StateOfScheduleEnum.loading  # 切换调度运作状态为读取
        logging.debug("完成收集数据，切换调度运作状态为%s", state_of_schedule)
        return state_of_schedule
        pass  # function

    @classmethod
    def get_process_index(cls, index_process: int, index_of_schedule_position: tuple):
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
    def get_stage_index(cls, index_process: int, index_stage: int, index_of_schedule_position: tuple):
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
    def get_model_length(cls, index_of_schedule_position: tuple):
        """
        获取模型之内容之列表之长度（暨过程个数）

        Args:
            index_of_schedule_position (tuple):

        Returns: 过程个数

        """
        return len(index_of_schedule_position)
        pass

    @classmethod
    def get_process_length(cls, index_process: int, index_of_schedule_position: tuple):
        """
        获取过程之内容之列表之长度（暨该过程之阶段个数）

        Args:
            index_process (int):
            index_of_schedule_position (tuple):

        Returns: 过程之阶段个数

        """
        return len(index_of_schedule_position[index_process - 1])
        pass

    @classmethod
    def is_process(cls, A: SystemicRiskAgent, BB_isv_t1: TypeState, BB_Shock_t_t1: TypeMoney, is_process: bool, stageFunctionName: str, process: ProcessComponent):
        """
        判断是否继续运行过程

        Args:
            A (SystemicRiskAgent): Agent群变量
            BB_isv_t1 (TypeState): 商业银行之资不抵债之状态，于时期1
            BB_Shock_t_t1 (TypeMoney): 商业银行受到的冲击，于时期1
            is_process (bool): 是否在运行过程状态
            stageFunctionName (str): 阶段函数名称
            process (ProcessComponent): 过程

        Returns: is_process

        """
        if stageFunctionName == process.content[-1].functionName:  # 如果当前阶段是所处过程之最后的阶段，则继续判断，否则过程未结束，后续继续运行。:
            if (
                    process.functionName == 'process_exBank_insolvent' or
                    process.functionName == 'process_exBank_illiquity' or
                    process.functionName == 'process_exBank_bankrupt'
            ):
                is_process = False
                logging.debug("结束过程：%s。", env['process_name'])
                pass
            elif (
                    process.functionName == 'process_interBank_insolvent'
            ):
                if A.BB.isv.all() == BB_isv_t1.all():  # 判断是否继续运行过程: #BUG，可能存在逻辑问题:
                    is_process = False
                    logging.debug("结束过程：%s。", env['process_name'])
                    pass
            else:
                if A.BB.Shock_t.all() == BB_Shock_t_t1.all():  # 判断是否继续运行过程:
                    is_process = False
                    logging.debug("结束过程：%s。", env['process_name'])
                    pass
                pass  # if:
        else:
            is_process = True
            logging.info("继续过程：%s。", env['process_name'])
            pass  # if:

        return is_process
        pass  # functions

    @classmethod
    def is_round(cls, env: dict = env):
        """函数：判断是否继续运行回合"""
        if (env['tau'] < env['max_num_of_tau']):
            env['is_round'] = True
        else:
            env['is_round'] = False
            logging.debug("结束回合%s。", env['process_name'])
            pass
        pass  # function

    @classmethod
    def is_step(cls, env: dict = env):
        """函数：判断是否继续步进"""
        if ~env['is_step']:
            logging.debug("暂时跳出模型%s之过程%s之阶段%s。", env['model_name'], env['process_name'], env['stage_name'])
            pass
        pass  # function

    @classmethod
    def is_loop(cls, env: dict = env):
        """
        函数：判断是否继续运行循环。
        只有同时满足继续运行过程、继续步进、继续运行回合时，才继续运行循环。否则跳出循环。
        """
        if (env['is_process'] and env['is_step'] and env['is_round']):
            env['is_loop'] = True
        else:
            env['is_loop'] = False
            logging.debug("跳出过程%s之循环。\n", env['process_name'])
            pass
        pass  # function

    pass  # class
