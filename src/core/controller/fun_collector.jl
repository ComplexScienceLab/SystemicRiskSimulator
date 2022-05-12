"函数区：收集数据"

## 函数区：收集数据

##########################################
#状态/开发
##########################################

"""
TODO函数：初始化待收集数据容器
"""
function initAgentDataCollection(A::SystemicRiskAgent)
    # dict01 = Dict([(:id, collect(range(1, env[:numBank], step=1))), (:tau, ones(env[:numBank])), (:indexStage, ones(env[:numBank]))])
    # dict02 = struct2dict(A.BB)
    # dict_fields = Dict([collect(dict01); collect(dict02)])
    dict_fields_BB = merge(Dict([(:dataId, 1), (:tau, ones(env[:numBank])), (:indexStage, ones(env[:numBank]))]), struct2dict(A.BB))
    # BB = StructArray([BB for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的商业银行实例数组
    BB_data = DataFrame(dict_fields_BB) # 初始化带回合变量的商业银行实例数据框
    # dict_fields_BI = merge(Dict([(:tau, 1), (:indexStage, 1)]), struct2dict(A.BI))
    BI_data = []
    dict_fields_BI = merge(Dict([(:dataId, 1), (:tau, 1), (:indexStage, 1)]), struct2dict(A.BI)) # 初始化带回合变量的银行间市场实例字典向量
    append!(BI_data, [dict_fields_BI])
    # dict_fields_BI = merge(Dict([(:tau, 1), (:indexStage, 1)]))
    # BI_data = DataFrame(keys(dict_fields_BI)) # 初始化带回合变量的银行间市场实例数据框
    # for (k, v) in struct2dict(A.BI)
    #     BI_data[1, k] = v
    # end
    # BI_data = StructArray([A.BI for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的银行间市场实例数组
    A_data = AgentDataCollection(BB_data, BI_data)
    return A_data
end


"""
TODO函数：收集数据并存储 #NOW 调度收集数据
"""
function collector(A::SystemicRiskAgent, A_data::AgentDataCollection; env::Dict=env)
    BB_data = DataFrame()
    BB_data[!, :dataId] = fill(env[:dataId], env[:numBank])
    BB_data[!, :tau] = fill(env[:tau], env[:numBank])
    BB_data[!, :indexStage] = fill(env[:indexStage], env[:numBank])
    # agentsFields = fieldnames(typeof(A.BB))[4:end]
    # agentsFields = collect(keys(struct2dict(A.BB)))
    # agentsValues = collect(values(struct2dict(A.BB)))
    for (k, v) in struct2dict(A.BB)
        BB_data[!, k] = v
    end
    append!(A_data.BB, BB_data) # 收集banks之数据为一数据框

    # BI_data = DataFrame()
    # BI_data[1, :tau] = env[:tau]
    # BI_data[1, :indexStage] = env[:indexStage]
    # for (k, v) in struct2dict(A.BI)
    #     BB_data[1, k] = v
    # end
    BI_data = merge(Dict([(:dataId, env[:dataId]), (:tau, env[:tau]), (:indexStage, env[:indexStage])]), struct2dict(A.BI))
    append!(A_data.BI, [BI_data]) # 收集banks之数据为一字典向量

    # A_data.BI[env[:tau]] = A.BI # 收集BI之数据为一结构体向量
    return A_data
end






