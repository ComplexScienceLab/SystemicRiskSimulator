


## 定义类型别名
TypeIds{NDIMS1} = Array{Int16,NDIMS1} # 向量编号类型
TypeAbbrs{NDIMS1} = Array{String,NDIMS1} # 向量缩写类型
TypeNames{NDIMS1} = Array{String,NDIMS1} # 向量名称类型
TypeMoney{NDIMS2} = Array{Float32,NDIMS2} # 向量资金类型
TypeState{NDIMS2} = Array{Bool,NDIMS2} # 一维向量状态类型
# EnvironmentVariables = Dict # 环境变量字典类型
# ParameterVariables = Dict # 参数变量字典类型
# primitive type EnvironmentVariables <: AbstractDict{Any,Any} end
ItemId = Int8
ItemFunctionName = Symbol
ItemTextName = String
# ItemList = Vector{ItemFunctionName}
# ItemList = Vector{S}
struct ComponentHierarchyType end # 定义组件层级结构类型：模型Model、过程Process、阶段Stage；
struct ComponentInstanceType end # 定义组件元素类型，有具体的定义；
struct ModelType end # 定义模型类型
struct ProcessType end # 定义过程类型


