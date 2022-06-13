"函数：运行一次仿真"

##########################################
#状态/修复
##########################################



"函数：运行一次仿真"
function makesim(model::ModelComponent, para::dict, env::dict)

    ## 初始化agent及其模型
    A, M, A_data = init_systemicRiskAgent(para, env)
    # systemicRiskModel = create_systemicRiskModel(systemicRiskAgent, para)

    ##BUG 测试具体模型。
    maxnum = 0
    env['stateOfProcess'] = StateOfSchedule.running
    while env['isModel'] == True && maxnum <= 20: #HACK可能需要设置最大次数maxnum
        maxnum += 1
        systemicRiskAgent_step(A, M, para, env, model, A_data)
        # return BB, BI, A_data.BB, A_data.BI, env
        pass # while


    ##BUG 测试Agents框架
    # maxnum = 0
    # while env['isModel'] == True && maxnum <= 20:
    #     maxnum += 1
    #     step(systemicRiskModel, systemicRiskAgent_step!, env['stepSize'])
    #     # _, _ = run(systemicRiskModel, systemicRiskAgent_step!, 1)
    #     _, _ = run(systemicRiskModel, systemicRiskAgent_step!, env['maxNumOfTau'])
    #     # return BB, BI, A_data.BB, A_data.BI, env
    #     pass # while

    ## 导出数据之于已经收集的
    env['stateOfProcess'] = :finishing
    collector(A; A_data, stateOfProcess=env['stateOfProcess'], para=para)

    pass # functions