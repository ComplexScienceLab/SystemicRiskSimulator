"""
@File   : experiment_manager.py
@Author : Ethan Lin
@Date   : 2022/06/17
@Desc   : 
"""
# from SystemicRisk.core import env, para, ModelComponent, StateOfScheduleEnum, ModelSetter, RunModel, ModelCollector
from PySystemicRiskLab.core.controller.fun_agentModel import ModelRunner
from PySystemicRiskLab.core.define.define_environment_variables import env
from PySystemicRiskLab.core.define.define_parameterVariables import para
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.controller.model_initVariable import ModelInitVariable
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum
from PySystemicRiskLab.core.define.define_component import ModelComponent
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.controller.model_runner import ModelRunner
from PySystemicRiskLab.core.controller.fun_scheduler import ModelCollector

class ExperimentManager:
    def makesim(model: ModelComponent, para: dict = para, env: dict = env):
        """函数：运行一次仿真"""
        ## 初始化agent及其模型
        A, M, A_data = ModelSetter.init_systemicRiskAgent(para, env)
        # systemicRiskModel = create_systemicRiskModel(systemicRiskAgent, para)

        ##BUG 测试具体模型。
        maxnum = 0
        env['state_of_process'] = StateOfScheduleEnum.running
        while env['is_model'] == True & maxnum <= 20:  # HACK可能需要设置最大次数maxnum
            maxnum += 1
            RunModel.systemicRiskAgent_step(A, M, para, env, model, A_data)
            # return BB, BI, A_data.BB, A_data.BI, env
            pass  # while

        ##BUG 测试Agents框架
        # maxnum = 0
        # while env['is_model'] == True & maxnum <= 20:
        #     maxnum += 1
        #     step(systemicRiskModel, systemicRiskAgent_step, env['step_size'])
        #     # _, _ = run(systemicRiskModel, systemicRiskAgent_step, 1)
        #     _, _ = run(systemicRiskModel, systemicRiskAgent_step, env['max_num_of_tau'])
        #     # return BB, BI, A_data.BB, A_data.BI, env
        #     pass # while

        ## 导出数据之于已经收集的
        env['state_of_process'] = StateOfScheduleEnum.finishing
        ModelCollector.collector(A, A_data, state_of_process=env['state_of_process'], para=para)

        pass  # functions

    pass  # class
