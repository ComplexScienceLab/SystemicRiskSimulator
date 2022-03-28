"函数：运行一次仿真"

##########################################
#状态/修复
##########################################



"函数：运行一次仿真"
function makesim(para::Dict, env::Dict)

    # 写入agent运行步骤在这
    systemicRiskAgent, systemicRiskModel, BB_tau_0, BI_tau_0, BB_tau, BI_tau = init_systemicRiskAgent!(para, env)
    # systemicRiskModel = create_systemicRiskModel(systemicRiskAgent, para)

    ##BUG 测试具体模型。
    systemicRiskAgent_step!(systemicRiskAgent, systemicRiskModel, para, env)

    ##BUG 测试Agents框架
    # step!(systemicRiskModel, systemicRiskAgent_step!, 1)
    # _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, 1)
    # _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, env[:maxNumOfTau])
    # wsave(datadir(env[:folderpathOfExperimentsData], savename(para, "jld2", connector = "|", equals = "=")), BB) #FIXME
    # return BB, BI, BB_tau, BI_tau, env
end