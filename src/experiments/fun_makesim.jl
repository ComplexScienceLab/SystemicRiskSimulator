"函数：运行一次仿真"

##########################################
#状态/修复
##########################################



"函数：运行一次仿真"
function makesim(para::Dict, env::Dict)

    # 写入agent运行步骤在这
    A, M, BB_tau_0, BI_tau_0, BB_tau, BI_tau = init_systemicRiskAgent!(para, env)
    # M = create_systemicRiskModel(A, para)
    systemicRiskAgent_step!(A, M, para, env)
    _, _ = run!(M, systemicRiskAgent_step!, env[:max_num_tau])
    wsave(datadir(env[:folderpathOfExperimentsData], savename(para, "jld2", connector = "|", equals = "=")), BB) #FIXME
    # return BB, BI, BB_tau, BI_tau, env
end