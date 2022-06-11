"函数区：收集数据"

## 函数区：收集数据

##########################################
#状态/使用
##########################################


function collector(A::SystemicRiskAgent; A_data::AgentDataCollection=AgentDataCollection([], []), stateOfProcess::Symbol=:running, env::Dict=env, para::Dict=Dict([]))
    if stateOfProcess == :running
        A_data = collectAgentData(A, A_data)
        return A_data
    elseif stateOfProcess == :initializing
        A_data = initAgentDataCollection(A)
        return A_data
    elseif stateOfProcess == :finishing
        exportAgentData(A_data; para)
    else
        throw(DomainError(stateOfProcess, "关键词stateOfProcess取值错误！"))
    end # if
end


## 方案三 
"""
TODO函数：初始化实验数据容器
"""
function initAgentDataCollection(A::SystemicRiskAgent; env::Dict=env)
    BB_data_item = [Dict([
        (getkey(env, env[:dataId], :dataId), env[:dataId]),
        (getkey(env, env[:tau], :tau), env[:tau]),
        (getkey(env, env[:indexProcess], :indexProcess), env[:indexProcess]),
        (getkey(env, env[:indexStage], :indexStage), env[:indexStage]),
        (:dataBB, deepcopy(A.BB))
    ])]
    BB_data = []
    append!(BB_data, BB_data_item) # 初始化banks之数据为一字典数组

    BI_data_item = [Dict([
        (getkey(env, env[:dataId], :dataId), env[:dataId]),
        (getkey(env, env[:tau], :tau), env[:tau]),
        (getkey(env, env[:indexProcess], :indexProcess), env[:indexProcess]),
        (getkey(env, env[:indexStage], :indexStage), env[:indexStage]),
        (:dataBI, deepcopy(A.BI))
    ])]
    BI_data = []
    append!(BI_data, BI_data_item) # 初始化interbank之数据为一字典数组

    A_data = AgentDataCollection(deepcopy(BB_data), deepcopy(BI_data))
    return A_data
end


"""
TODO函数：收集数据并存储
"""
function collectAgentData(A::SystemicRiskAgent, A_data::AgentDataCollection; env::Dict=env)
    BB_data_item = [Dict([
        (getkey(env, env[:dataId], :dataId), env[:dataId]),
        (getkey(env, env[:tau], :tau), env[:tau]),
        (getkey(env, env[:indexProcess], :indexProcess), env[:indexProcess]),
        (getkey(env, env[:indexStage], :indexStage), env[:indexStage]),
        (:dataBB, deepcopy(A.BB))
    ])]
    append!(A_data.BB, BB_data_item) # 收集banks之数据为一字典数组

    BI_data_item = [Dict([
        (getkey(env, env[:dataId], :dataId), env[:dataId]),
        (getkey(env, env[:tau], :tau), env[:tau]),
        (getkey(env, env[:indexProcess], :indexProcess), env[:indexProcess]),
        (getkey(env, env[:indexStage], :indexStage), env[:indexStage]),
        (:dataBI, deepcopy(A.BI))
    ])]
    append!(A_data.BI, BI_data_item) # 收集interbank之数据为一字典数组
    return A_data
end

"""
TODO函数：导出实验结果数据
"""
function exportAgentData(A_data::AgentDataCollection; env::Dict=env, para::Dict=para)

    ## 整理banks之数据为一数据框
    BB_data_export = DataFrame()
    BB_data = DataFrame()
    numRow = size(getfield(A_data.BB[1][:dataBB], fieldnames(typeof(A_data.BB[1][:dataBB]))[1]))[1]
    for (i1, v1) in enumerate(A_data.BB)
        BB_data[!, :dataId] = fill(v1[:dataId], numRow)
        BB_data[!, :tau] = fill(v1[:tau], numRow)
        BB_data[!, :indexProcess] = fill(v1[:indexProcess], numRow)
        BB_data[!, :indexStage] = fill(v1[:indexStage], numRow)
        fieldNames = fieldnames(typeof(v1[:dataBB]))
        fieldValues = [getfield(v1[:dataBB], fieldName) for fieldName in fieldNames]
        for (i2, v2) in enumerate(fieldValues)
            BB_data[!, fieldNames[i2]] = v2
        end
        append!(BB_data_export, BB_data)
    end
    CSV.write(datadir("$(env[:folderpathOfExperimentsOutputData])","BB_exp=$(env[:id_experiment]).csv"), BB_data_export) # 导出为csv格式；

    ## 整理interbank之数据为一数据框
    BI_data_export = DataFrame()
    BI_data = DataFrame()
    numRow, numCol = size(getfield(A_data.BI[1][:dataBI], fieldnames(typeof(A_data.BI[1][:dataBI]))[1]))
    for (i1, v1) in enumerate(A_data.BI)
        BI_data[!, :dataId] = fill(v1[:dataId], numRow * numCol)
        BI_data[!, :tau] = fill(v1[:tau], numRow * numCol)
        BI_data[!, :indexProcess] = fill(v1[:indexProcess], numRow * numCol)
        BI_data[!, :indexStage] = fill(v1[:indexStage], numRow * numCol)
        BI_data[!, :indexStage] = fill(v1[:indexStage], numRow * numCol)
        BI_data[!, :row] = repeat(1:numRow, inner=numCol)
        BI_data[!, :col] = repeat(1:numCol, outer=numRow)
        fieldNames = fieldnames(typeof(v1[:dataBI]))
        fieldValues = [getfield(v1[:dataBI], fieldName) for fieldName in fieldNames]
        for (i2, v2) in enumerate(fieldValues)
            if (typeof(v2) == TypeMoney{2} || typeof(v2) == TypeState{2} || typeof(v2) == TypeIds{2})
                BI_data[!, fieldNames[i2]] = [v2'...] # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
            elseif typeof(v2) == TypeList{Any}
                ## 转换信息列表为矩阵形式
                m2 = Matrix{Any}(falses(numRow, numCol))
                for (i3, v3) in enumerate(v2)
                    for i4 in v3
                        m2[i3, i4] = true
                    end
                end
                BI_data[!, fieldNames[i2]] = [m2'...] # 赋值相应的字段之矩阵给数据框之相应的字段之数据列
            end
        end
        append!(BI_data_export, BI_data)
    end
    CSV.write(datadir("$(env[:folderpathOfExperimentsOutputData])","BI_exp=$(env[:id_experiment]).csv"), BI_data_export) # 导出为csv格式

    ## 整理env之数据为一数据框，然后导出为csv格式
    # wsave(datadir(env[:folderpathOfExperimentsOutputData], savename(para, "|exp=$(env[:id_experiment]).jld2", connector="|", equals="=")), para)
    
end


# ## 方案一 #HACK失败
# functions initAgentDataCollection(A::SystemicRiskAgent)
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
# 函数：收集数据并存储
# """
# functions collector(A::SystemicRiskAgent, A_data::AgentDataCollection; env::Dict=env)
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
# 
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
# 函数：初始化待收集数据容器
# """
# functions initAgentDataCollection(A::SystemicRiskAgent)
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
# 函数：收集数据并存储
# """
# functions collector(A::SystemicRiskAgent, A_data::AgentDataCollection; env::Dict=env)
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


