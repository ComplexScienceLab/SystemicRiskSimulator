"函数：运行一次仿真"

##########################################
#状态/修复
##########################################



"函数：运行一次仿真"
function makesim(model::ModelComponent, para::Dict, env::Dict)

    ## 初始化agent及其模型
    A, M, A_data = init_systemicRiskAgent!(para, env)
    # systemicRiskModel = create_systemicRiskModel(systemicRiskAgent, para)

    ##BUG 测试具体模型。
    maxnum = 0
    env[:stateOfProcess] = :running
    while env[:isModel] == true && maxnum <= 20
        maxnum += 1
        systemicRiskAgent_step!(A, M, para, env, model, A_data)
        # return BB, BI, A_data.BB, A_data.BI, env
    end # while


    ##BUG 测试Agents框架
    # maxnum = 0
    # while env[:isModel] == true && maxnum <= 20
    #     maxnum += 1
    #     step!(systemicRiskModel, systemicRiskAgent_step!, env[:stepSize])
    #     # _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, 1)
    #     _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, env[:maxNumOfTau])
    #     # return BB, BI, A_data.BB, A_data.BI, env
    # end # while

    env[:stateOfProcess] = :finishing
    collector(A;A_data)

end # function