"程序：定义模型及其相关的结构体"

# "定义综合组件"# HACK 较为抽象，暂时不会用。
# struct Component{ComponentHierarchyType,ComponentInstanceType}
#     name::String # 组件名称
#     content::Union{ComponentHierarchyType,ComponentInstanceType} # 组件核心内容
#     run::Function # 运行组件
# end


"定义阶段组件"
struct StageComponent{ComponentInstanceType}
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    run::Function # 运行阶段
    # content::Array{StageComponent} # 阶段组件列表
end


"定义过程组件"
struct ProcessComponent{ComponentInstanceType}
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    # conditionToContinueProcess::Expr # 判断条件用以结束过程 conditionToContinueProcess
    run::Function # 运行过程
    content::Array{StageComponent} # 阶段组件列表
end


"定义模型组件"
struct ModelComponent{ComponentInstanceType}
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    run::Function # 运行模型
    content::Array{ProcessComponent} # 过程组件列表
end



