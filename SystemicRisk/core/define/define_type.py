"定义类型"

## 定义类型，模式3-1

##########################################
# 状态/开发
##########################################

import numpy as np

## 定义类型别名
typeIds = np.dtype(np.int16)  # 向量编号类型
typeAbbr = np.dtype(np.str)  # 向量缩写类型
typeName = np.dtype(np.str)  # 向量名称类型
typeMoney = np.dtype(np.float32)  # 向量资金类型
typeState = np.dtype(np.bool)  # 一维向量状态类型
typeList = list  # 一维向量状态类型

# HACK无用
# 定义个体抽象类型
# abstract type Object     pass
# abstract type Bank <:  Object     pass
# abstract type BB <:  Bank     pass # 定义商业银行BankCommercial个体抽象类型
# abstract type BS <:  Bank     pass # 定义影子银行BankShadow个体抽象类型
# TypeIds{NDIMS1} = Array{Int16,NDIMS1} # 向量编号类型
# TypeAbbrs{NDIMS1} = Array{String,NDIMS1} # 向量缩写类型
# TypeNames{NDIMS1} = Array{String,NDIMS1} # 向量名称类型
# TypeMoney{NDIMS2} = Array{Float32,NDIMS2} # 向量资金类型
# TypeState{NDIMS2} = Array{Bool,NDIMS2} # 一维向量状态类型
# TypeList{Any} = Array{Any} # 一维向量状态类型
# EnvironmentVariables = dict # 环境变量字典类型
# ParameterVariables = dict # 参数变量字典类型
# primitive type EnvironmentVariables <: AbstractDict{Any,Any}     pass
typeItemId = np.dtype(np.int8)
typeItemFunctionName = np.dtype(np.str)
typeItemTextName = np.dtype(np.str)
# ItemList = Vector{ItemFunctionName}
# # ItemList = Vector{S}
# class ComponentHierarchyType     pass # 定义组件层级结构类型：模型Model、过程Process、阶段Stage；
# class ComponentInstanceType     pass # 定义组件元素类型，有具体的定义；
# class ModelType     pass # 定义模型类型
# class ProcessType     pass # 定义过程类型
# class StageType     pass # 定义阶段类型

# ProcessItemList = Vector{ProcessContent}
# ProcessItemList = Vector{StageContent}


# "定义个体复合类型。"
# class Objects{NDIMS2}
#     id:TypeIds{NDIMS2} # 编号
#     abbr:TypeAbbrs{NDIMS2} # 缩写
#     name:TypeNames{NDIMS2} # 全名
#     pass
