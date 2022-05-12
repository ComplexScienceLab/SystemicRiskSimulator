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

    ## 存储数据，通过Watson.Dr工具包
    dataBB = A_data.BB
    dataBI = A_data.BI
    # wsave(datadir(env[:folderpathOfExperimentsData], savename(para, "jld2", connector="|", equals="=")), para) #FIXME
    # wsave(datadir(env[:folderpathOfExperimentsData], "BB.jld2"), dataBB) #FIXME
    # wsave(datadir(env[:folderpathOfExperimentsData], "BI.jld2"), A_data.BI) #FIXME
    # dataBB_csv=
    
    wsave(datadir("../test/",savename(para, "_$(env[:id_experiment]).jld2", connector="|", equals="=")), para) #FIXME

    jldsave("./test/BB$(env[:id_experiment]).jld2"; dataBB)

    jldsave("./test/BI$(env[:id_experiment]).jld2"; dataBI)

    h5open("./test/BB$(env[:id_experiment]).h5", "w") do f
        g = create_group(f, "mygroup")
        g["mydataset"] = dataBB
    end

    h5open("./test/BI$(env[:id_experiment]).h5", "w") do f
        g = create_group(f, "mygroup")
        g["mydataset"] = dataBI
    end

    jldopen("./test/BIarray$(env[:id_experiment]).jld2", "w") do f
        array_dict_BI = Array{Any}[]
        for i in 1:length(array_dict_BI)
            array_dict_BI[i] = struct2dict(dataBI[i])
            f[i] = array_dict_BI[i]
        end
    end

    h5open("./test/BIarray$(env[:id_experiment]).h5", "w") do f
        array_dict_BI = Array{Any}[]
        for i in 1:length(array_dict_BI)
            array_dict_BI[i] = struct2dict(dataBI[i])
            f[i] = array_dict_BI[i]
        end
    end

end # function