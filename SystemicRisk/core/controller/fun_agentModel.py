"功能函数区：Agent模型相关功能函数，基于Agents工具包"


##########################################
#状态/开发
##########################################
from SystemicRisk import SystemicRiskAgent

"#TODO初始化systemicRiskAgent和systemicRiskModel"
def init_systemicRiskAgent(para:dict, env:dict):
    systemicRiskAgent, systemicRiskAgent_data = init_B_and_BI( init_method=env['init_method'])

    ## 调度状态
    env['state_of_schedule'] = StateOfSchedule.loading

    # ## 构建Agent模型
    # systemicRiskAgent = SystemicRiskAgent(
    #     1, # 编号（必备的）
    #     banks, # 商业银行群
    #     interbank # 银行间邻接矩阵
    # )
    systemicRiskModel = ABM(systemicRiskAgent; properties=(dict([collect(para); collect(env)])))
    return systemicRiskAgent, systemicRiskModel, systemicRiskAgent_data
    pass

"函数：Agent模型步进" #BUG方案一
def systemicRiskAgent_step(A:SystemicRiskAgent, para:dict, env:dict, model:ModelComponent, A_data:AgentDataCollection):
    env['is_step'] = True
    A, para, env, A_data = runModel(A, para, env, model, A_data) # 运行具体的模型，通过运行模型组件的方式
    # systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = fun_model_skeleton(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # HACK冗余
    # systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = modelComponent.run(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # HACK冗余
    # _, _ = run(systemicRiskModel, systemicRiskAgent_step!, env['max_num_of_tau'])
    pass

# "函数：Agent模型步进" #BUG方案二
# functions systemicRiskAgent_step(systemicRiskAgent:SystemicRiskAgent, systemicRiskModel:ABM, para:dict, env:dict)
#     env['is_step'] = True
#     systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env = model_BI1111(systemicRiskAgent.bank, systemicRiskAgent.interbank, para, env) # 调用具体的模型
#     _, _ = run(systemicRiskModel, systemicRiskAgent_step!, env['max_num_of_tau'])
#     pass


