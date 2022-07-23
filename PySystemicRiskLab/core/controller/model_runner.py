"模型运行器"

## 模型运行器

##########################################
# 状态/使用
##########################################
# from PySystemicRiskLab.core import SystemicRiskAgent, ModelComponent, ProcessComponent, StageComponent, AgentDataCollection, TypeState
pass  # end import



from PySystemicRiskLab.core.define.define_type import *
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_component import ModelComponent, ProcessComponent, StageComponent
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
pass  # end import





class ModelRunner:
    """
    模型运行器
    """

    """
    模型运行器。
    输入参数将被直接修改。
    
    Argument: 
    - A:SystemicRiskAgent: Agent群变量；
    - paras:dict: 参数变量；
    - env:dict: 环境变量；
    - modelComponent:ModelComponent: 模型组件实例；
    - A_data:AgentDataCollection: Agent群变量之数据；
    
    Return:
    - A:SystemicRiskAgent: Agent群变量；
    - paras:dict: 参数变量；
    - env:dict: 环境变量；
    - A_data:AgentDataCollection: Agent群变量之数据；
    """

    @staticmethod
    def run_model(self, A: SystemicRiskAgent, para: dict, env: dict, modelComponent: ModelComponent, agentData: AgentDataCollection):
        A, para, env, agentData = modelComponent.run(A, para, env, modelComponent, agentData)
        return A, para, env, agentData
        pass

    """
    过程运行器。
    输入参数将被直接修改。
    
    Argument: 
    - A:SystemicRiskAgent: Agent群变量；
    - paras:dict: 参数变量；
    - env:dict: 环境变量；
    - processComponent:ProcessComponent: 过程组件实例；
    - A_data:AgentDataCollection: Agent群变量之数据；
    
    Return:
    - A:SystemicRiskAgent: Agent群变量；
    - paras:dict: 参数变量；
    - env:dict: 环境变量；
    - A_data:AgentDataCollection: Agent群变量之数据；
    """

    @staticmethod
    def run_process(A: SystemicRiskAgent, para: dict, env: dict, processComponent: ProcessComponent, agentData: AgentDataCollection):
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
    - paras:dict: 参数变量；
    - env:dict: 环境变量；
    - stageComponent:StageComponent: 阶段组件实例；
    
    Return:
    - BB:BankCommercial: 商业银行群变量；
    - BI:BankInterbank: 银行间邻接矩阵变量；
    """

    @classmethod
    def run_stage(A: SystemicRiskAgent, b: TypeState, ib: TypeState, para: dict, env: dict, stageComponent: StageComponent):
        A = stageComponent.run(A, b, ib, para, env)
        return A
        pass

    pass
