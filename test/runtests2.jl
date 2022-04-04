## temp文件

##########################################
#用途/草稿；
##########################################


using DataFrames

## 定义类型别名
TypeIds{NDIMS1} = Array{Int16,NDIMS1} # 向量编号类型
TypeAbbrs{NDIMS1} = Array{String,NDIMS1} # 向量缩写类型
TypeNames{NDIMS1} = Array{String,NDIMS1} # 向量名称类型
TypeMoney{NDIMS2} = Array{Float32,NDIMS2} # 向量资金类型
TypeState{NDIMS2} = Array{Bool,NDIMS2} # 一维向量状态类型
# EnvironmentVariables = Dict # 环境变量字典类型
# ParameterVariables = Dict # 参数变量Î字典类型
# primitive type EnvironmentVariables <: AbstractDict{Any,Any} end
ItemId = Int8
ItemName = Symbol
TypeItem = Dict{ItemId,ItemName}

"定义模型结构体"
mutable struct Model
    id::ItemId # 编号 id
    name::ItemName # 模型名称 name
    list_process::Vector{Symbol} # 模型需要的过程列表 list_process
    # list_process::DataFrame # 模型需要的过程列表 list_process
end

set_model = Set([
    :process_exBank_insolvent,
    :process_interBank_insolvent,
    :process_exBank_illiquity,
    :process_interBank_illiquity,
    :process_exBank_bankrupt,
    :process_interBank_bankrupt,
])

model_BI1111 = Model(
    1,
    :model_BI1111,
    [
        :process_exBank_insolvent,
        :process_interBank_insolvent,
        :process_exBank_illiquity,
        :process_interBank_illiquity,
        :process_interBank_bankrupt
    ]
)




