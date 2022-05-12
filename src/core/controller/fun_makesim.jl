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
    
    #BUG
    ## 存储数据，通过Watson.Dr工具包
    dataBB = A_data.BB
    dataBI = A_data.BI
    # wsave(datadir(env[:folderpathOfExperimentsData], savename(para, "jld2", connector="|", equals="=")), para) #FIXME
    # wsave(datadir(env[:folderpathOfExperimentsData], "BB.jld2"), dataBB) #FIXME
    # wsave(datadir(env[:folderpathOfExperimentsData], "BI.jld2"), A_data.BI) #FIXME
    # dataBB_csv=
    wsave(datadir("../test/data/", savename(para, "_$(env[:id_experiment]).jld2", connector="|", equals="=")), para) #FIXME
    jldsave("./test/data/BB$(env[:id_experiment]).jld2"; dataBB)
    jldsave("./test/data/BI$(env[:id_experiment]).jld2"; dataBI)

    # h5save("./test/BB$(env[:id_experiment]).h5", "w") do f
    #     g = create_group(f, "mygroup")
    #     g["mydataset"] = dataBB
    # end
    # 
    # h5save("./test/BB$(env[:id_experiment]).h5"; dataBI)

    # jldopen("./test/BIarray$(env[:id_experiment]).jld2", "w") do f
    #     array_dict_BI = Array[]
    #     for i in 1:length(dataBI)
    #         append!(array_dict_BI, [struct2dict(dataBI[i])])
    #         f[i] = array_dict_BI[i]
    #     end
    # end

    # h5open("./test/BI$(env[:id_experiment]).h5", "w") do f
    #     g = create_group(f, "mygroup")
    #     g["mydataset"] = dataBI
    # end

    # h5open("./test/BIarray$(env[:id_experiment]).h5", "w") do f
    #     array_dict_BI = []
    #     for i in 1:length(dataBI)
    #         # append!(array_dict_BI, struct2dict(dataBI[i]))
    #         append!(array_dict_BI, [[dataBI[i]]])
    #         f[i] = array_dict_BI[i]
    #     end
    # end

    # array_dict_BI = []
    # for i in 1:length(dataBI)
    #     append!(array_dict_BI, [[dataBI[i]]])
    # end
    # print(array_dict_BI)

end # function