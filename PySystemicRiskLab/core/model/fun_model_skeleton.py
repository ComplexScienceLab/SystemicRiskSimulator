"函数：通用模型框架"

## 函数：通用模型框架

##########################################
# 状态/开发
##########################################

# from PySystemicRiskLab.core import SystemicRiskAgent, ModelComponent, AgentDataCollection, ModelRunner, StateOfScheduleEnum
import logging

pass  # end import

from PySystemicRiskLab import logging
from PySystemicRiskLab.core.controller.model_runner import ModelRunner
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_component import ModelComponent, ProcessComponent
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum

pass  # end import


class ModelSkeleton:

    @classmethod
    def fun_model_skeleton(cls, A: SystemicRiskAgent, para: dict, env: dict, model: ModelComponent, A_data: AgentDataCollection):
        """
        通用模型框架。

        Args:
            A (SystemicRiskAgent): Agent群变量
            para (dict): 参数变量
            env (dict): 环境变量
            model (ModelComponent): 模型组件实例
            A_data (AgentDataCollection): Agent群变量之数据

        Returns: A, para, env, A_data

        """
        if (env['is_model']):
            if (env['tau'] > 1):
                logging.debug("继续模型：%s\n\n", env['model_name'])
                pass
            else:
                logging.debug("开始模型：%s\n\n", env['model_name'])
                pass
            pass

        ## 运行每个过程
        for (i, process) in enumerate(model.content):
            env['index_process'] = i + 1
            if env['index_process'] == env['loaded_index_process']:  # 调度读取：如果当前过程等于待读取的过程，则进入继续读取。:
                env['process_name'] = str(process.functionName)
                # logging.debug("过程 = %i，名称 = %s", env['index_process'], env['process_name'])
                A, para, env, A_data = ModelRunner.runProcess(A, para, env, process, A_data)  # BUG 为什么A_data是None？
                pass
            pass  # for

        ## 判断是否结束步进
        if ~env['is_step']:
            logging.debug("步进已结束，跳出模型：%s。", env['model_name'])
            pass

        ## 判断是否结束模型，暨结束本次实验
        if env['state_of_schedule'] == StateOfScheduleEnum.idle:
            env['is_model'] = False
            env['is_experiment'] = False
            pass
        if (~env['is_model'] | ~env['is_experiment']):
            logging.debug("结束模型：%s。\n", env['model_name'])
            pass

        # return BB, BI, paras, env
        return A, para, env, A_data
        pass  # function

    pass  # class
