"程序：定义模型及其相关的结构体"

"定义组件"# HACK 较为抽象，暂时不会用。
struct Component{ComponentHierarchyType,ComponentInstanceType}
    name::String # 组件名称
    content::Union{ComponentHierarchyType,ComponentInstanceType} # 组件核心内容
    run::Function # 运行组件
end

"定义阶段组件内容结构体"
struct StageContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    run::Function # 函数
end

"定义过程组件内容结构体"
struct ProcessContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 functionName
    textName::ItemTextName # 文本名称 textName
    listStageContent::Vector{StageContent} # 阶段内容列表 listStageContent
    listStageFunction::Vector{Function} # 阶段函数列表 listStageFunction
end

"定义模型组件内容结构体"
struct ModelContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    listProcessContent::Vector{ProcessContent} # 过程内容列表 listContentProcess
end



"定义模型组件"
struct ModelComponent{ComponentInstanceType}
    name::String # 模型名称
    content::ModelContent # 模型核心内容
    run::Function # 运行模型
end

"定义过程组件"
struct ProcessComponent{ComponentInstanceType}
    name::String # 过程名称
    content::ProcessContent # 过程核心内容
    run::Function # 运行过程
end

"定义阶段组件"
struct StageComponent{ComponentInstanceType}
    name::String # 过程名称
    content::StageContent # 过程核心内容
    run::Function # 运行过程
end
