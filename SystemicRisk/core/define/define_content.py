"程序：定义模型内容结构体"


"定义阶段组件内容结构体"
class StageContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    modelFunction::Function # 函数
    pass


"定义过程组件内容结构体"
class ProcessContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 functionName
    textName::ItemTextName # 文本名称 textName
    # listProcessContent::Vector{ProcessContent} # 过程内容列表 listContentProcess
    listStageContent::Vector{StageContent} # 阶段内容列表 listStageContent
    pass


"定义模型组件内容结构体"
class ModelContent
    id::ItemId # 编号 id
    functionName::ItemFunctionName # 函数名称 name
    textName::ItemTextName # 文本名称 name
    listProcessContent::Vector{ProcessContent} # 过程内容列表 listContentProcess
    pass


