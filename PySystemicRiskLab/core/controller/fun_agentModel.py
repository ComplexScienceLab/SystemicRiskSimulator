"功能函数区：Agent模型相关功能函数，基于Agents工具包"

##########################################
# 状态/开发
##########################################

# from PySystemicRiskLab.core import env, paras, SystemicRiskAgent, ModelInitVariable, StateOfScheduleEnum, ModelComponent, AgentDataCollection, ModelRunner, ModelCollector

from PySystemicRiskLab import dataclass, logging
from PySystemicRiskLab.core.define.define_environment_variables import env
from PySystemicRiskLab.core.define.define_parameterVariables import para
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.controller.model_initVariable import ModelInitVariable
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum, StateOfProcessEnum
from PySystemicRiskLab.core.define.define_component import ModelComponent
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.controller.model_runner import ModelRunner
from PySystemicRiskLab.core.controller.fun_scheduler import ModelCollector

pass  # end import


@dataclass
class AgentsModel:
    modelInitVariable = ModelInitVariable()

    # def init_systemicRiskAgent(cls, A_data: AgentDataCollection = AgentDataCollection([], []), para: dict = paras, env: dict = env):
    @classmethod
    def init_systemicRiskAgent(cls, env: dict = env):
        systemicRiskAgent, systemicRiskAgent_data = cls.modelInitVariable.init_B_and_BI(init_method=env['init_method'])

        ## 调度状态
        env['state_of_schedule'] = StateOfScheduleEnum.loading

        return systemicRiskAgent, systemicRiskAgent_data
        pass

    @classmethod
    def systemicRiskAgent_step(cls, A: SystemicRiskAgent, para: dict, env: dict, model: ModelComponent, A_data: AgentDataCollection):
        """函数：Agent模型步进"""
        env['is_step'] = True
        A, para, env, A_data = ModelRunner.runModel(A, para, env, model, A_data)  # 运行具体的模型，通过运行模型组件的方式
        pass

    pass  # class

    @classmethod
    def makesim(cls, model: ModelComponent, para: dict = para, env: dict = env):
        """函数：运行一次仿真"""
        ## 初始化agent及其模型
        A, A_data = cls.init_systemicRiskAgent(env)

        num_step_of_model = 0
        env['state_of_process'] = StateOfProcessEnum.running
        # logging.debug("过程之状态 = %s", env['state_of_process'])
        while (env['is_model'] == True and num_step_of_model <= env['max_num_steps_of_model']):
            num_step_of_model += 1
            cls.systemicRiskAgent_step(A, para, env, model, A_data)
            pass  # while

        if num_step_of_model >= env['max_num_steps_of_model']:
            logging.info("超过该模型最大步进次数，强制跳出循环。")
            pass

        ## 导出数据之于已经收集的
        env['state_of_process'] = StateOfProcessEnum.finishing
        ModelCollector.collector(A, A_data, env['state_of_process'], env, para)

        pass  # function

    pass  # class
