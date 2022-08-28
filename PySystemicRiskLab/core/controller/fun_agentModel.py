"功能函数区：Agent模型相关功能函数，基于Agents工具包"

##########################################
# 状态/开发
##########################################

# from PySystemicRiskLab.core import env, paras, SystemicRiskAgent, ModelInitVariable, StateOfScheduleEnum, ModelComponent, AgentDataCollection, ModelRunner, ModelCollector
import dataclasses

pass  # end import

from PySystemicRiskLab.core.define.define_environment_variables import env
from PySystemicRiskLab.core.define.define_parameterVariables import paras
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.controller.model_initVariable import ModelInitVariable
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
from PySystemicRiskLab.core.define.define_component import ModelComponent
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.controller.model_runner import ModelRunner
from PySystemicRiskLab.core.controller.fun_scheduler import ModelCollector

pass  # end import


@dataclasses.dataclass
class AgentsModel:
    # TODO初始化systemicRiskAgent和systemicRiskModel

    modelInitVariable = ModelInitVariable()

    @classmethod
    def init_systemicRiskAgent(cls, A_data: AgentDataCollection = AgentDataCollection([], []), para: dict = paras, env: dict = env):
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
    def makesim(cls, model: ModelComponent, para: dict = paras, env: dict = env):
        """函数：运行一次仿真"""
        ## 初始化agent及其模型
        A, M, A_data = cls.init_systemicRiskAgent(para, env)
        # systemicRiskModel = create_systemicRiskModel(systemicRiskAgent, paras)

        ##BUG 测试具体模型。
        maxnum = 0
        env['state_of_process'] = StateOfScheduleEnum.running
        while env['is_model'] == True & maxnum <= 20:  # HACK可能需要设置最大次数maxnum
            maxnum += 1
            cls.systemicRiskAgent_step(A, M, para, env, model, A_data)
            # return BB, BI, A_data.BB, A_data.BI, env
            pass  # while

        ##BUG 测试Agents框架
        # maxnum = 0
        # while env[:is_model] == true && maxnum <= 20
        #     maxnum += 1
        #     step!(systemicRiskModel, systemicRiskAgent_step!, env[:step_size])
        #     # _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, 1)
        #     _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, env[:max_num_of_tau])
        #     # return BB, BI, A_data.BB, A_data.BI, env
        # end # while

        ## 导出数据之于已经收集的
        env['state_of_process'] = StateOfScheduleEnum.finishing
        ModelCollector.collector(A, A_data, para=para)

        pass  # function

    pass  # class
