"程序：定义模型内容结构体"


"定义阶段组件内容结构体"
struct StageContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    modelFunction::Function # 函数
end


"定义过程组件内容结构体"
struct ProcessContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 functionName
    textName::ItemTextName # 文本名称 textName
    # run!::Function # 函数
    # conditionToContinueProcess::Expr # 判断条件用以结束过程 conditionToContinueProcess
    listStageContent::Vector{StageContent} # 阶段内容列表 listStageContent
    # modelFunction::Function # 函数
end


"定义模型组件内容结构体"
struct ModelContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    # run!::Function # 函数
    listProcessContent::Vector{ProcessContent} # 过程内容列表 listContentProcess
    # modelFunction::Function # 函数
end


