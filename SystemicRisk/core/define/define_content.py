"程序：定义模型内容结构体"



class StageContent
    """
    定义阶段组件内容结构体
    """
    id:type_item_id # 编号 id
    functionName:ItemFunctionName # 函数名称 name
    textName:ItemTextName # 文本名称 name
    modelFunction:Function # 函数
    pass



class ProcessContent
    """
    定义过程组件内容结构体
    """
    id:type_item_id # 编号 id
    functionName:ItemFunctionName # 函数名称 functionName
    textName:ItemTextName # 文本名称 textName
    # listProcessContent:Vector{ProcessContent} # 过程内容列表 listContentProcess
    listStageContent:Vector{StageContent} # 阶段内容列表 listStageContent
    pass



class ModelContent
    """
    定义模型组件内容结构体
    """
    id:type_item_id # 编号 id
    functionName:ItemFunctionName # 函数名称 name
    textName:ItemTextName # 文本名称 name
    listProcessContent:Vector{ProcessContent} # 过程内容列表 listContentProcess
    pass


