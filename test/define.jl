

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
ItemList = Vector{Any}


"定义过程结构体"
struct ProcessContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 functionName
    textName::ItemTextName # 文本名称 textName
    listStage::ItemList # 阶段列表 listStage
end

"定义模型结构体"
struct ModelContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    listProcess::Vector{ProcessContent} # 过程列表 listProcess
end


# 定义：运行模型
macro runModel()
    expr = quote
        include("model.jl")
        model()
    end
    println("开始运行模型model：")
    eval(expr)
    println("结束运行模型model。")
end

"宏：当测试时使用"
macro test(content)
    if env[:isTest]
        return esc(content)
        # return :(content)
        # return $(content)
        # return :($(content))
    end
end



