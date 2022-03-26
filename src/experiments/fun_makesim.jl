"函数：运行一次仿真"

##########################################
#状态/修复
##########################################



"函数：运行一次仿真"
function makesim(agent::SystemicRiskAgent, para::Dict, env::EnvironmentVariables)

    #NOW 写入agent运行步骤在这
    systemicRiskModel = create_systemicRiskModel(agent, env, para)
    _, _ = run!(systemicRiskModel, systemicRiskAgent_step!, env[:max_num_tau])
    wsave(datadir(env[:folderpathOfExperimentsData], savename(para, "jld2", connector = "|", equals = "=")), BB) #FIXME
    # return BB, BI, BB_tau, BI_tau, env
end