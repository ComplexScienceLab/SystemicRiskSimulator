"函数：运行一次仿真"

##########################################
#状态/修复
##########################################



"函数：运行一次仿真"
function makesim(BB::BankCommercial, BI::BankInterbank, para::Dict, env::EnvironmentVariables)


    BB, BI, BB_tau, BI_tau, para, env = model_BI1111(BB, BI, para, env)

    wsave(datadir(env[:folderpathOfExperimentsData], savename(para, "jld2", connector = "|", equals = "=")), BB) #FIXME
    # return BB, BI, BB_tau, BI_tau, env
end