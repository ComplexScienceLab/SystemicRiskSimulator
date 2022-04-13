"程序：定义模型结构体"


"定义模型结构体"
mutable struct ModelContent
    id::ItemId # 编号 id
    funName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    listProcess::ItemList # 过程列表 listProcess
end

"定义过程结构体"
mutable struct ProcessContent
    id::ItemId # 编号 id
    funName::ItemFunctionName # 函数名称 functionName
    textName::ItemTextName # 文本名称 textName
    listStage::ItemList # 阶段列表 listStage
end

"定义阶段结构体"
mutable struct StageContent
    id::ItemId # 编号 id
    funName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
end

