"函数区：收集数据"

## 函数区：收集数据

##########################################
#状态/开发
##########################################

"""
TODO函数：初始化待收集数据容器
"""
function initCollectionData(A::SystemicRiskAgent)
    dict01 = Dict([(:id, ONES1), (:tau, ONES1), (:stage, ONES1)])
    dict02 = struct2dict(A.banks)
    dict_fields=Dict([collect(dict01);collect(dict02)])
    # BB_data = StructArray([BB for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的商业银行实例数组
    BB_data = DataFrame(dict_fields) # 初始化带回合变量的商业银行实例数据框
    BI_data = StructArray([A.interbank for i = 1:env[:maxNumOfTau]]) # 初始化带回合变量的银行间市场实例数组
    return BB_data, BI_data
end


"""
TODO函数：收集数据并存储
"""
function collector(BB_data::DataFrame, BI_data::Array, A::SystemicRiskAgent; env::Dict=env)
    data_BB = DataFrame()
    # data_BB[!, :tau] = fill(env[:tau], length(fieldnames(typeof(s))))
    data_BB[!, :tau] = fill(env[:tau], length(A))
    data_BB[!, :id_stage] = fill(env[:indexStage], length(A))
    for field in fieldnames(typeof(A.banks))
        data_BB[!, field] = collect(vcat(values(agent)) for agent in A.banks)
    end
    append!(BB_data, data_BB) # 收集banks之数据为一数据框
    BI_data[env[:tau]] = A.interbank # 收集BI之数据为一结构体向量

    return BB_data, BI_data
end


"结构体：定义待收集数据类型"
mutable struct DataStepCollection
    banks_data::DataFrame
    interbank_data::StructArray
end



