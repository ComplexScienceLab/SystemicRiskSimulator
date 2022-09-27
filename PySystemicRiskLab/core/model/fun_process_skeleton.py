"函数：通用过程框架"

## 函数：通用过程框架

##########################################
# 状态/开发
##########################################

# from PySystemicRiskLab.core import deepcopy, SystemicRiskAgent, ProcessComponent, AgentDataCollection, StateOfScheduleEnum, ModelScheduler, ModelRunner

pass  # end import

from PySystemicRiskLab import deepcopy, logging
from PySystemicRiskLab.core.controller.fun_scheduler import ModelScheduler
from PySystemicRiskLab.core.controller.model_runner import ModelRunner
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_component import ProcessComponent
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum

pass  # end import


class ProcessSkeleton:

    @classmethod
    def fun_process_skeleton(cls, A: SystemicRiskAgent, para: dict, env: dict, process: ProcessComponent, A_data: AgentDataCollection):
        """
        通用过程框架。

        Args:
            cls ():
            A (SystemicRiskAgent): Agent群变量
            para (dict): 参数变量
            env (dict): 环境变量
            process (ProcessComponent): 过程组件实例
            A_data (AgentDataCollection): Agent群变量之数据

        Returns: A, para, env, A_data

        """

        logging.debug("过程%s：%s", env['index_process'], env['process_name'])

        env['index_stage'] = 0  # 初始化阶段所在位置
        env['is_step'] = True  # 初始化步进状态
        env['is_round'] = True  # 初始化回合状态
        env['is_process'] = True  # 初始化过程状态
        env['is_loop'] = True  # 初始化循环状态
        while env['is_loop'] == True:

            ## 回合数变动
            if (env['loaded_index_stage'] != 1):
                logging.debug("继续回合：%s\n", env['tau'])
                pass
            else:
                env['tau'] += 1  # 回合累加一
                logging.debug("开始回合：%s\n", env['tau'])
                pass

            ## 设置临时变量
            BB_Shock_t_t1 = deepcopy(A.BB.Shock_t)
            BB_isv_t1 = deepcopy(A.BB.isv)

            b = (A.BB.on | A.BB.off)  # 临时设置BB示性变量
            ib = (A.BB.on | A.BB.off) & (A.BB.on | A.BB.off).T  # 临时设置BI示性变量

            ## 运行每一个阶段
            for (i, stage) in enumerate(process.content):
                env['index_stage'] = i + 1
                env['stage_name'] = str(stage.functionName)
                logging.debug("阶段%s：%s", env['index_stage'], env['stage_name'])

                ## 调度并运行状态
                if env['state_of_schedule'] == StateOfScheduleEnum.loading:
                    env['state_of_schedule'] = ModelScheduler.scheduler_loading(env['index_process'], env['index_stage'], env['loaded_index_process'], env['loaded_index_stage'], env['state_of_schedule'], env['index_of_schedule_position'])  # 调度读取
                    pass
                if env['state_of_schedule'] == StateOfScheduleEnum.stepping:
                    A = ModelRunner.runStage(A, b, ib, para, env, stage)
                    env['step'], env['is_step'], env['state_of_schedule'] = ModelScheduler.scheduler_stepping(env['step'], env['step_size'])  # 步进
                    # logging.debug("调度状态 = %s",env['state_of_schedule'])
                    pass

                ModelScheduler.is_step()  # 判断是否继续运行步进
                # logging.debug("是否继续步进 = %s", env['is_step'])
                if env['is_step'] == False:  # 如果步进停止，则跳出该循环:
                    break
                    pass
                pass  # for

            env['is_process'] = ModelScheduler.is_process(A, BB_isv_t1, BB_Shock_t_t1, env['is_process'], env['stage_name'], process)  # 判断是否继续运行过程

            if env['state_of_schedule'] == StateOfScheduleEnum.saving:
                env['saved_index_process'], env['saved_index_stage'], env['loaded_index_process'], env['loaded_index_stage'], env['state_of_schedule'] = ModelScheduler.scheduler_saving(env['index_process'], env['index_stage'], env['is_process'], env['index_of_schedule_position'])  # 调度存储
                pass
            if (env['state_of_schedule'] == StateOfScheduleEnum.collecting) and (env['state_of_process'] == StateOfScheduleEnum.running):
                env['state_of_schedule'] = ModelScheduler.scheduler_collecting(A, A_data)
                # logging.debug("调度状态 = %s", env['state_of_schedule'])
                pass

            ModelScheduler.is_round()  # 判断是否继续运行回合 BUG

            ModelScheduler.is_loop()  # 判断是否继续运行循环 BUG
            pass  # while

        return A, para, env, A_data

        pass  # functions

    pass  # class
