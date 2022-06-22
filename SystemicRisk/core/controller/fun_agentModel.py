"功能函数区：Agent模型相关功能函数，基于Agents工具包"

##########################################
# 状态/开发
##########################################
from SystemicRisk.core import SystemicRiskAgent as Agent, ModelSetter, StateOfScheduleEnum, ModelComponent, AgentDataCollection, ModelRunner


class RunModel:
    "#TODO初始化systemicRiskAgent和systemicRiskModel"

    def init_systemicRiskAgent(self, para: dict, env: dict):
        systemicRiskAgent, systemicRiskAgent_data = ModelSetter.init_B_and_BI(init_method=env['init_method'])

        ## 调度状态
        env['state_of_schedule'] = StateOfScheduleEnum.loading

        return systemicRiskAgent, systemicRiskAgent_data
        pass

    "函数：Agent模型步进"  # BUG方案一

    def systemicRiskAgent_step(self, A: Agent, para: dict, env: dict, model: ModelComponent, A_data: AgentDataCollection):
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
