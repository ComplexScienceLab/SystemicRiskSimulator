"函数区：收集数据"

## 函数区：收集数据

##########################################
#状态/开发
##########################################

"""
TODO函数：初始化待收集数据容器
"""
function initAgentDataCollection(A::SystemicRiskAgent)
    dict01 = Dict([(:id, RANGE1), (:tau, ONES1), (:indexStage, ONES1)])
    dict02 = struct2dict(A.BB)
    dict_fields = Dict([collect(dict01); collect(dict02)])
    # BB = StructArray([BB for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的商业银行实例数组
    data_BB = DataFrame(dict_fields) # 初始化带回合变量的商业银行实例数据框
    data_BI = StructArray([A.BI for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的银行间市场实例数组
    A_data = AgentDataCollection(data_BB, data_BI)
    return A_data
end


"""
TODO函数：收集数据并存储
"""
function collector(A::SystemicRiskAgent, A_data::AgentDataCollection; env::Dict=env)
    data_BB = DataFrame()
    # data_BB[!, :tau] = fill(env[:tau], length(fieldnames(typeof(s))))
    data_BB[!, :id] = RANGE1
    data_BB[!, :tau] = fill(env[:tau], length(fieldnames(typeof(A.BB))))
    data_BB[!, :indexStage] = fill(env[:indexStage], length(fieldnames(typeof(A.BB))))
    agents = collect(values([A.BB]))
    for field in fieldnames(typeof(A.BB))
        data_BB[!, field] = collect(getproperty(agent) for agent in agents)
    end
    append!(A_data.BB, data_BB) # 收集banks之数据为一数据框
    A_data.BI[env[:tau]] = A.BI # 收集BI之数据为一结构体向量
    return A_data
end






