"模型运行器"

## 模型运行器

##########################################
#状态/使用
##########################################
from SystemicRisk import AgentDataCollection
from SystemicRisk.core.define.define_agents import *
from SystemicRisk.core.define.component import *


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
    def run_model(A:SystemicRiskAgent, para:dict, env:dict, modelComponent:ModelComponent, A_data:AgentDataCollection):
        A, para, env, A_data = modelComponent.run(A, para, env, modelComponent, A_data)
        return A, para, env, A_data
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
    def run_process(A:SystemicRiskAgent, para:dict, env:dict, processComponent:ProcessComponent, A_data:AgentDataCollection):
        A, para, env, A_data = processComponent.run(A, para, env, processComponent, A_data)
        return A, para, env, A_data
        pass


    """
    阶段运行器。
    输入参数将被直接修改。
    
    Argument: 
    - BB:BankCommercial: 商业银行群变量；
    - BI:BankInterbank: 银行间邻接矩阵变量；
    - b:TypeState{1}: 商业银行群示性向量；
    - ib:TypeState{2}: 银行间邻接矩阵示性矩阵；
    - para:dict: 参数变量；
    - env:dict: 环境变量；
    - stageComponent:StageComponent: 阶段组件实例；
    
    Return:
    - BB:BankCommercial: 商业银行群变量；
    - BI:BankInterbank: 银行间邻接矩阵变量；
    """
    def run_stage(A:SystemicRiskAgent, b:type_state, ib:type_state, para:dict, env:dict, stageComponent:StageComponent):
        A = stageComponent.run(A, b, ib, para, env)
        return A
        pass


    pass


