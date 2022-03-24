"定义类型"

## 定义类型，模式3-1

##########################################
#状态/开发
##########################################



# 定义个体抽象类型
# abstract type Object end
# abstract type Bank <: Object end
# abstract type BB <: Bank end # 定义商业银行BankCommercial个体抽象类型
# abstract type BS <: Bank end # 定义影子银行BankShadow个体抽象类型


## 定义类型
TypeIds{NDIMS1} = Array{Int16,NDIMS1} # 向量编号类型
TypeAbbrs{NDIMS1} = Array{String,NDIMS1} # 向量缩写类型
TypeNames{NDIMS1} = Array{String,NDIMS1} # 向量名称类型
TypeMoney{NDIMS2} = Array{Float32,NDIMS2} # 向量资金类型
TypeState{NDIMS2} = Array{Bool,NDIMS2} # 一维向量状态类型


# "定义个体复合类型。"
# mutable struct Objects{NDIMS2}
#     id::TypeIds{NDIMS2} # 编号
#     abbr::TypeAbbrs{NDIMS2} # 缩写
#     name::TypeNames{NDIMS2} # 全名
# end

