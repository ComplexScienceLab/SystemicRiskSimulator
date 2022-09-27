"模型运行器"

## 模型运行器

##########################################
# 状态/使用
##########################################
# from PySystemicRiskLab.core import SystemicRiskAgent, ModelComponent, ProcessComponent, StageComponent, AgentDataCollection, TypeState
pass  # end import

from PySystemicRiskLab import logging
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_component import ModelComponent, ProcessComponent, StageComponent
from PySystemicRiskLab.core.define.define_type import *

pass  # end import


class ModelRunner:
    """
    模型运行器
    """

    @classmethod
    def runModel(cls, A: SystemicRiskAgent, para: dict, env: dict, modelComponent: ModelComponent, agentData: AgentDataCollection):
        """
        模型运行器。
        输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            para (dict): 参数变量
            env (dict): 环境变量
            modelComponent (ModelComponent): 模型组件实例
            agentData (AgentDataCollection): Agent群变量之数据

        Returns: A, para, env, agentData

        """
        A, para, env, agentData = modelComponent.run(A, para, env, modelComponent, agentData)
        return A, para, env, agentData
        pass  # function

    @classmethod
    def runProcess(cls, A: SystemicRiskAgent, para: dict, env: dict, processComponent: ProcessComponent, agentData: AgentDataCollection):
        """
        过程运行器。
        输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            para (dict): 参数变量
            env (dict): 环境变量
            processComponent (ProcessComponent): 过程组件实例
            agentData (AgentDataCollection): Agent群变量之数据

        Returns: A, para, env, agentData

        """
        A, para, env, agentData = processComponent.run(A, para, env, processComponent, agentData)
        return A, para, env, agentData
        pass  # function

    @classmethod
    def runStage(cls, A: SystemicRiskAgent, b: TypeState, ib: TypeState, para: dict, env: dict, stageComponent: StageComponent):
        """
        阶段运行器。
        输入参数将被直接修改。

        Args:
            A (SystemicRiskAgent): Agent群变量
            b (TypeState): 商业银行群示性向量
            ib (TypeState): 银行间邻接矩阵示性矩阵
            para (dict): 参数变量
            env (dict): 环境变量
            stageComponent (StageComponent): 阶段组件实例

        Returns: A

        """
        A.BB, A.BI = stageComponent.run(A.BB, A.BI, b, ib, para, env)
        return A
        pass  # function

    pass  # class
