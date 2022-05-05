"函数区：收集数据"

## 函数区：收集数据

##########################################
#状态/开发
##########################################

"""
TODO函数：初始化数据框
"""
function initCollectionData(A::SystemicRiskAgent)
    list_fielddata = Array{Symbol}[:id, :tau, :stage]
    append!(list_fielddata, fieldnames(typeof(A.banks)))
    df = DataFrame(list_fielddata)
    return list
end


"""
TODO函数：收集数据并存储
"""
function collector(df_BB::DataFrame, BB_tau::Array, A::SystemicRiskAgent; env::Ditc=env)
    data_BB = DataFrame()
    # data_BB[!, :tau] = fill(env[:tau], length(fieldnames(typeof(s))))
    data_BB[!, :tau] = fill(env[:tau], length(A))
    data_BB[!, :id_stage] = fill(env[:indexStage], length(A))
    for field in fieldnames(typeof(A.banks))
        data_BB[!,field]=collect(vcat(values(agent)) for agent in A.banks)
    end

    append!(df_BB, data_BB) # 收集banks之数据为一数据框

    NOW # 收集BI之数据为一结构体向量
    return df_BB, BB_tau
end




