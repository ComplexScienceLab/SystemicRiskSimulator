"模型运行器"

## 模型运行器

##########################################
# 状态/使用
##########################################
from SystemicRisk.core import AgentDataCollection, SystemicRiskAgent, ModelManager,ModelSetter, StateOfScheduleEnum, ModelComponent, AgentDataCollection, ModelRunner
from SystemicRisk.core.define.define_type import *


class ModelRunner:
    """
    模型运行器
    """

    """
    模型运行器。
    输入参数将被直接修改。
    
    Argument: 
    - A:SystemicRiskAgent: Agent群变量；
    - para:dict: 参数变量；
    - env:dict: 环境变量；
    - modelComponent:ModelComponent: 模型组件实例；
    - A_data:AgentDataCollection: Agent群变量之数据；
    
    Return:
    - A:SystemicRiskAgent: Agent群变量；
    - para:dict: 参数变量；
    - env:dict: 环境变量；
    - A_data:AgentDataCollection: Agent群变量之数据；
    """

    def run_model(self, A: SystemicRiskAgent, para: dict, env: dict, modelComponent: ModelManager.modelComponent, agentData: AgentDataCollection):
        A, para, env, agentData = modelComponent.run(A, para, env, modelComponent, agentData)
        return A, para, env, agentData
        pass

    """
    过程运行器。
    输入参数将被直接修改。
    
    Argument: 
    - A:SystemicRiskAgent: Agent群变量；
    - para:dict: 参数变量；
    - env:dict: 环境变量；
    - processComponent:ProcessComponent: 过程组件实例；
    - A_data:AgentDataCollection: Agent群变量之数据；
    
    Return:
    - A:SystemicRiskAgent: Agent群变量；
    - para:dict: 参数变量；
    - env:dict: 环境变量；
    - A_data:AgentDataCollection: Agent群变量之数据；
    """

    def run_process(self, A: SystemicRiskAgent, para: dict, env: dict, processComponent: ModelManager.processComponent, agentData: AgentDataCollection):
        A, para, env, agentData = processComponent.run(A, para, env, processComponent, agentData)
        return A, para, env, agentData
        pass

    """
    阶段运行器。
    输入参数将被直接修改。
    
    Argument: 
    - BB:BankCommercial: 商业银行群变量；
    - BI:BankInterbank: 银行间邻接矩阵变量；
    - b:TypeState: 商业银行群示性向量；
    - ib:TypeState: 银行间邻接矩阵示性矩阵；
    - para:dict: 参数变量；
    - env:dict: 环境变量；
    - stageComponent:StageComponent: 阶段组件实例；
    
    Return:
    - BB:BankCommercial: 商业银行群变量；
    - BI:BankInterbank: 银行间邻接矩阵变量；
    """

    def run_stage(self, A: SystemicRiskAgent, b: TypeState, ib: TypeState, para: dict, env: dict, stageComponent: ModelManager.stageComponent):
        A = stageComponent.run(A, b, ib, para, env)
        return A
        pass


    def init_systemicRiskAgent(self, para: dict, env: dict):
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




    pass
