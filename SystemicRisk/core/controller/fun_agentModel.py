"功能函数区：Agent模型相关功能函数，基于Agents工具包"

##########################################
# 状态/开发
##########################################

# from SystemicRisk.core import env, para, SystemicRiskAgent, ModelSetter, StateOfScheduleEnum, ModelComponent, AgentDataCollection, ModelRunner, ModelCollector
pass  # end import



from SystemicRisk.core.define.define_environment_variables import env
from SystemicRisk.core.define.define_parameterVariables import para
from SystemicRisk.core.define.define_agents import SystemicRiskAgent
from SystemicRisk.core.controller.model_setter import ModelSetter
from SystemicRisk.core.define.define_enum import StateOfScheduleEnum
from SystemicRisk.core.define.define_component import ModelComponent
from SystemicRisk.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRisk.core.controller.model_runner import ModelRunner
from SystemicRisk.core.controller.fun_scheduler import ModelCollector
pass  # end import





class RunModel:
    "#TODO初始化systemicRiskAgent和systemicRiskModel"

    def init_systemicRiskAgent(self, para: dict = para, env: dict = env):
        systemicRiskAgent, systemicRiskAgent_data = ModelSetter.init_B_and_BI(init_method=env['init_method'])

        ## 调度状态
        env['state_of_schedule'] = StateOfScheduleEnum.loading

        return systemicRiskAgent, systemicRiskAgent_data
        pass

    "函数：Agent模型步进"  # BUG方案一
    def systemicRiskAgent_step(self, A: SystemicRiskAgent, para: dict, env: dict, model: ModelComponent, A_data: AgentDataCollection):
        env['is_step'] = True
        A, para, env, A_data = ModelRunner.runModel(A, para, env, model, A_data)  # 运行具体的模型，通过运行模型组件的方式
        pass

    # "函数：Agent模型步进" #BUG方案二
    # functions systemicRiskAgent_step(systemicRiskAgent:SystemicRiskAgent, systemicRiskModel:ABM, para:dict, env:dict)
    #     env['is_step'] = True
    #     systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = model_BI1111(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # 调用具体的模型
    #     _, _ = run(systemicRiskModel, systemicRiskAgent_step, env['max_num_of_tau'])
    #     pass

    pass  # class

    "函数：运行一次仿真"

    def makesim(self, model: ModelComponent, para: dict = para, env: dict = env):
        ## 初始化agent及其模型
        A, M, A_data = self.init_systemicRiskAgent(self, para, env)
        # systemicRiskModel = create_systemicRiskModel(systemicRiskAgent, para)

        ##BUG 测试具体模型。
        maxnum = 0
        env['state_of_process'] = StateOfScheduleEnum.running
        while env['is_model'] == True & maxnum <= 20:  # HACK可能需要设置最大次数maxnum
            maxnum += 1
            self.systemicRiskAgent_step(self, A, M, para, env, model, A_data)
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
        ModelCollector.collector(self, A, A_data, state_of_process=env['state_of_process'], para=para)

        pass  # function

    pass  # class
