"函数区：收集数据"

## 函数区：收集数据

##########################################
#状态/开发
##########################################


function collector(A::SystemicRiskAgent; A_data::AgentDataCollection, stateOfProcess::Symbol=:running, env::Dict=env)
    if stateOfProcess == :running
        A_data = collectAgentData(A, A_data)
        return A_data
    elseif stateOfProcess == :initializing
        A_data = initAgentDataCollection(A)
        return A_data
    elseif stateOfProcess == :finishing
        exportAgentData(A, A_data)
    else
        throw(DomainError(stateOfProcess, "关键词stateOfProcess取值错误！"))
    end # if
end

# ## 方案一 #HACK待续
# function initAgentDataCollection(A::SystemicRiskAgent)
#     dict_fields_BB = merge(Dict([(:dataId, 1), (:tau, Vector{Int}(ones(env[:numBank]))), (:indexStage, Vector{Int}(ones(env[:numBank])))]), struct2dict(A.BB))
#     BB_data = DataFrame(dict_fields_BB) # 初始化带回合变量的商业银行实例数据框
#     # BI_data = []
#     dict_fields_BI = merge(Dict([(:dataId, 1), (:tau, Vector{Int}(ones(env[:numBank]))), (:indexStage, Vector{Int}(ones(env[:numBank]))), (:bankRow, collect(range(1, env[:numBank], step=1))), (:bankCol, collect(range(1, env[:numBank], step=1)))]), struct2dict(A.BI)) # 初始化带回合变量的银行间市场实例字典向量
#     BI_data = DataFrames(dict_fields_BI)
#     # append!(BI_data, [dict_fields_BI])
#     A_data = AgentDataCollection(BB_data, BI_data)
#     return A_data
# end


# """
# TODO函数：收集数据并存储
# """
# function collector(A::SystemicRiskAgent, A_data::AgentDataCollection; env::Dict=env)
#     BB_data = DataFrame()
#     BB_data[!, :dataId] = fill(env[:dataId], env[:numBank])
#     BB_data[!, :tau] = fill(env[:tau], env[:numBank])
#     BB_data[!, :indexStage] = fill(env[:indexStage], env[:numBank])
#     # agentsFields = fieldnames(typeof(A.BB))[4:end]
#     # agentsFields = collect(keys(struct2dict(A.BB)))
#     # agentsValues = collect(values(struct2dict(A.BB)))
#     for (k, v) in struct2dict(A.BB)
#         BB_data[!, k] = v
#     end
#     append!(A_data.BB, BB_data) # 收集banks之数据为一数据框

#     #TODO
#     BI_data = DataFrame()
#     BB_data[!, :dataId] = fill(env[:dataId], env[:numBank]^2)
#     BB_data[!, :tau] = fill(env[:tau], env[:numBank]^2)
#     BB_data[!, :indexStage] = fill(env[:indexStage], env[:numBank]^2)
#     for (k, v) in struct2dict(A.BI)
#         BB_data[1, k] = v
#     end

#     BI_data = merge(Dict([(:dataId, env[:dataId]), (:tau, env[:tau]), (:indexStage, env[:indexStage])]), struct2dict(A.BI))
#     append!(A_data.BI, [BI_data]) # 收集banks之数据为一字典向量

#     # A_data.BI[env[:tau]] = A.BI # 收集BI之数据为一结构体向量
#     return A_data
# end


## 方案二 #HACK失效
# """
# TODO函数：初始化待收集数据容器
# """
# function initAgentDataCollection(A::SystemicRiskAgent)
#     # dict01 = Dict([(:id, collect(range(1, env[:numBank], step=1))), (:tau, ones(env[:numBank])), (:indexStage, ones(env[:numBank]))])
#     # dict02 = struct2dict(A.BB)
#     # dict_fields = Dict([collect(dict01); collect(dict02)])
#     dict_fields_BB = merge(Dict([(:dataId, 1), (:tau, ones(env[:numBank])), (:indexStage, ones(env[:numBank]))]), struct2dict(A.BB))
#     # BB = StructArray([BB for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的商业银行实例数组
#     BB_data = DataFrame(dict_fields_BB) # 初始化带回合变量的商业银行实例数据框
#     # dict_fields_BI = merge(Dict([(:tau, 1), (:indexStage, 1)]), struct2dict(A.BI))
#     BI_data = []
#     dict_fields_BI = merge(Dict([(:dataId, 1), (:tau, 1), (:indexStage, 1)]), struct2dict(A.BI)) # 初始化带回合变量的银行间市场实例字典向量
#     append!(BI_data, [dict_fields_BI])
#     # dict_fields_BI = merge(Dict([(:tau, 1), (:indexStage, 1)]))
#     # BI_data = DataFrame(keys(dict_fields_BI)) # 初始化带回合变量的银行间市场实例数据框
#     # for (k, v) in struct2dict(A.BI)
#     #     BI_data[1, k] = v
#     # end
#     # BI_data = StructArray([A.BI for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的银行间市场实例数组
#     A_data = AgentDataCollection(BB_data, BI_data)
#     return A_data
# end


# """
# TODO函数：收集数据并存储
# """
# function collector(A::SystemicRiskAgent, A_data::AgentDataCollection; env::Dict=env)
#     BB_data = DataFrame()
#     BB_data[!, :dataId] = fill(env[:dataId], env[:numBank])
#     BB_data[!, :tau] = fill(env[:tau], env[:numBank])
#     BB_data[!, :indexStage] = fill(env[:indexStage], env[:numBank])
#     # agentsFields = fieldnames(typeof(A.BB))[4:end]
#     # agentsFields = collect(keys(struct2dict(A.BB)))
#     # agentsValues = collect(values(struct2dict(A.BB)))
#     for (k, v) in struct2dict(A.BB)
#         BB_data[!, k] = v
#     end
#     append!(A_data.BB, BB_data) # 收集banks之数据为一数据框

#     # BI_data = DataFrame()
#     # BI_data[1, :tau] = env[:tau]
#     # BI_data[1, :indexStage] = env[:indexStage]
#     # for (k, v) in struct2dict(A.BI)
#     #     BB_data[1, k] = v
#     # end
#     BI_data = merge(Dict([(:dataId, env[:dataId]), (:tau, env[:tau]), (:indexStage, env[:indexStage])]), struct2dict(A.BI))
#     append!(A_data.BI, [BI_data]) # 收集banks之数据为一字典向量

#     # A_data.BI[env[:tau]] = A.BI # 收集BI之数据为一结构体向量
#     return A_data
# end



##NOW 方案三 
function initAgentDataCollection(A::SystemicRiskAgent; env::Dict=env)

    # BB_data_item = merge(Dict([(:dataId, fill(env[:dataId], env[:numBank])), (:tau, Vector{Int}(ones(env[:numBank]))), (:indexProcess, Vector{Int}(ones(env[:numBank]))), (:indexStage, Vector{Int}(ones(env[:numBank])))]), struct2dict(A.BB))
    # BB_data = DataFrame(BB_data_item) # 初始化带回合变量的商业银行实例为数据框
    # BB_data = []
    # append!(BB_data, A.BB)

    BB_data_item = [Dict([
        (getkey(env, env[:dataId], :dataId), env[:dataId]),
        (getkey(env, env[:tau], :tau), env[:tau]),
        (getkey(env, env[:indexProcess], :indexProcess), env[:indexProcess]),
        (getkey(env, env[:indexStage], :indexStage), env[:indexStage]),
        (:dataBB, A.BB)
    ])]
    BB_data = []
    append!(BB_data, BB_data_item) # 初始化banks之数据为一字典数组

    BI_data_item = [Dict([
        (getkey(env, env[:dataId], :dataId), env[:dataId]),
        (getkey(env, env[:tau], :tau), env[:tau]),
        (getkey(env, env[:indexProcess], :indexProcess), env[:indexProcess]),
        (getkey(env, env[:indexStage], :indexStage), env[:indexStage]),
        (:dataBI, A.BI)
    ])]
    BI_data = []
    append!(BI_data, BI_data_item) # 初始化interbank之数据为一字典数组

    A_data = AgentDataCollection(BB_data, BI_data)
    return A_data
end


"""
TODO函数：收集数据并存储
"""
function collectAgentData(A::SystemicRiskAgent, A_data::AgentDataCollection; env::Dict=env)
    BB_data_item = Dict([
        (getkey(env, env[:dataId], :dataId), env[:dataId]),
        (getkey(env, env[:tau], :tau), env[:tau]),
        (getkey(env, env[:indexProcess], :indexProcess), env[:indexProcess]),
        (getkey(env, env[:indexStage], :indexStage), env[:indexStage]),
        (:dataBB, A.BB)
    ])
    append!(A_data.BB, BB_data_item) # 收集banks之数据为一字典数组

    BI_data_item = Dict([
        (getkey(env, env[:dataId], :dataId), env[:dataId]),
        (getkey(env, env[:tau], :tau), env[:tau]),
        (getkey(env, env[:indexProcess], :indexProcess), env[:indexProcess]),
        (getkey(env, env[:indexStage], :indexStage), env[:indexStage]),
        (:dataBI, A.BI)
    ])
    append!(A_data.BI, BI_data_item) # 收集interbank之数据为一字典数组



    # BB_data = DataFrame()
    # BB_data[!, :dataId] = fill(env[:dataId], env[:numBank])
    # BB_data[!, :tau] = fill(env[:tau], env[:numBank])
    # BB_data[!, :indexStage] = fill(env[:indexStage], env[:numBank])
    # for (k, v) in struct2dict(A.BB)
    #     BB_data[!, k] = v
    # end
    # append!(A_data.BB, BB_data) # 收集banks之数据为一数据框

    # append!(A_data.BB, A.BB) # 收集banks之数据为一结构体数组
    # append!(A_data.BI, A.BI) # 收集banks之数据为一结构体数组
    return A_data
end

"""
TODO函数：导出实验结果数据
"""
function exportAgentData(A::SystemicRiskAgent, A_data::AgentDataCollection; env::Dict=env)
    #BUG
    ## 整理并导出数据
    dataBB = A_data.BB
    dataBI = A_data.BI

    ## 整理banks之数据为一数据框
    BB_data_export=DataFrames()
    BB_data = DataFrame()
    for (i1,v1) in enumerate(A_data.BB)
        BB_data[!, :dataId] = fill(v1[:dataId],env[:numBank])
        BB_data[!, :tau] = fill(v1[:tau], env[:numBank])
        BB_data[!, :indexProcess] = fill(v1[:indexProcess], env[:numBank])
        BB_data[!, :indexStage] = fill(v1[:indexStage], env[:numBank])
        for (i2, v2) in v1[:dataBB]
            BB_data[!, i2] = v2
        end
        append!(BB_data_export, BB_data)
    end

    ## NOW整理interbank之数据为一数据框
    BI_data_export=DataFrames()
    BI_data = DataFrame()
    for (i1,v1) in enumerate(A_data.BI)
        BI_data[!, :dataId] = fill(v1[:dataId],env[:numBank]^2)
        BI_data[!, :tau] = fill(v1[:tau], env[:numBank]^2)
        BI_data[!, :indexProcess] = fill(v1[:indexProcess], env[:numBank]^2)
        BI_data[!, :indexStage] = fill(v1[:indexStage], env[:numBank]^2)
        for (i2, v2) in v1[:dataBI]
            BI_data[!, i2] = 
        end
        append!(BI_data_export, BI_data)
    end



    # wsave(datadir(env[:folderpathOfExperimentsData], savename(para, "jld2", connector="|", equals="=")), para) #FIXME
    # wsave(datadir(env[:folderpathOfExperimentsData], "BB.jld2"), dataBB) #FIXME
    # wsave(datadir(env[:folderpathOfExperimentsData], "BI.jld2"), A_data.BI) #FIXME
    # dataBB_csv=
    wsave(datadir("../test/data/", savename(para, "_$(env[:id_experiment]).jld2", connector="|", equals="=")), para) #FIXME
    jldsave("./test/data/BB$(env[:id_experiment]).jld2"; dataBB)
    jldsave("./test/data/BI$(env[:id_experiment]).jld2"; dataBI)
    # jldsave("./test/data/BB$(env[:id_experiment]).h5"; dataBB)
    # jldsave("./test/data/BI$(env[:id_experiment]).h5"; dataBI)
    CSV.write("./test/data/BB$(env[:id_experiment]).csv", dataBB)

    h5open("./test/data/BI$(env[:id_experiment]).h5", "w") do f
        for (i, oneOfDataBI) in enumerate(dataBI)
            create_group(f, "$(i)")
            g = f["$(i)"]
            g["$(i)"] = oneOfDataBI
        end
        # g = create_group(f, "BI$(env[:id_experiment])")
        # g["BI$(env[:id_experiment])"] = dataBI
    end

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
end



