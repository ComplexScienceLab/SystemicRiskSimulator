"函数：运行一次仿真"

##########################################
#状态/修复
##########################################



"函数：运行一次仿真"
function makesim(model::ModelComponent, para::Dict, env::Dict)

    ## 初始化agent及其模型
    A, M, A_data_0, BB_data, BI_data = init_systemicRiskAgent!(para, env)
    # systemicRiskModel = create_systemicRiskModel(systemicRiskAgent, para)

    ##BUG 测试具体模型。
    maxnum = 0
    while env[:isModel] == true && maxnum <= 20
        maxnum += 1
        systemicRiskAgent_step!(A, M, para, env, model, BB_data, BI_data)
        # return BB, BI, BB_data, BI_data, env
    end # while


    ##BUG 测试Agents框架
    # maxnum = 0
    # while env[:isModel] == true && maxnum <= 20
    #     maxnum += 1
    #     step!(systemicRiskModel, systemicRiskAgent_step!, env[:stepSize])
    #     # _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, 1)
    #     _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, env[:maxNumOfTau])
    #     # return BB, BI, BB_data, BI_data, env
    # end # while

    ## 存储数据，通过Watson.Dr工具包
    # wsave(datadir(env[:folderpathOfExperimentsData], savename(para, "jld2", connector="|", equals="=")), systemicRiskAgent.bank) #FIXME
end # function