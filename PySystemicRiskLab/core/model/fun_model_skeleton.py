"函数：通用模型框架"

## 函数：通用模型框架

##########################################
# 状态/开发
##########################################

# from PySystemicRiskLab.core import SystemicRiskAgent, ModelComponent, AgentDataCollection, ModelRunner, StateOfScheduleEnum
pass  # end import

from PySystemicRiskLab.core.controller.model_runner import ModelRunner
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_component import ModelComponent
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum

pass  # end import





"""
通用模型框架：

Argument: 
- A:SystemicRiskAgent: Agent群变量；
- paras:dict: 参数变量；
- env:dict: 环境变量；
- models:ModelComponent: 模型组件实例；
- A_data:AgentDataCollection: Agent群变量之数据；

Return:
- A:SystemicRiskAgent: Agent群变量；
- paras:dict: 参数变量；
- env:dict: 环境变量；
- A_data:AgentDataCollection: Agent群变量之数据；
"""


@classmethod
def fun_model_skeleton(cls, A: SystemicRiskAgent, para: dict, env: dict, model: ModelComponent, A_data: AgentDataCollection):
    if (env['is_model']):
        if (env['tau'] > 1):
            # @testprintln "\n继续模型：$(env['model_name'])"
            pass
        else:
            # @testprintln "\n开始模型：$(env['model_name'])"
            pass
        pass

    ## 运行每个过程
    for (idx_process, process) in enumerate(model.content):
        env['index_process'] = idx_process
        if env['index_process'] == env['loadedIndexProcess']:  # 调度读取：如果当前过程等于待读取的过程，则进入继续读取。:
            env['process_name'] = str(process.functionName)
            A, para, env, A_data = ModelRunner.runProcess(A, para, env, process, A_data)
            pass
        pass  # for

    ## 判断是否结束步进
    if ~env['is_step']:
        # @testprintln "步进已结束，跳出模型：$(env['model_name'])。"
        pass
    # 判断是否结束模型
    if env['state_of_schedule'] == StateOfScheduleEnum.idle:
        env['is_model'] = False
        env['is_experiment'] = False
        pass
    if (~env['is_model'] | ~env['is_experiment']):
        # @testprintln "结束模型：$(env['model_name'])。\n"
        pass

    # return BB, BI, paras, env
    return A, para, env, A_data
    pass  # functions

#     pass # module
