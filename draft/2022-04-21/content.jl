
## 列出各模型内容


stageContent_1 = StageContent(
    1, # 编号 id
    :stage_1, # 函数名称 functionName
    "stage_1", # 文本名称 textName
    stage_1!, # 函数名称
)

stageContent_2 = StageContent(
    2, # 编号 id
    :stage_2, # 函数名称 functionName
    "stage_2", # 文本名称 textName
    stage_2!, # 函数名称
)

stageContent_3 = StageContent(
    3, # 编号 id
    :stage_3, # 函数名称 functionName
    "stage_3", # 文本名称 textName
    stage_3!, # 函数名称
)


processContent_1 = ProcessContent(
    1, # 编号 id
    :process_1, # 函数名称 functionName
    "process_1", # 文本名称 textName
    [
        stageContent_1,
        stageContent_3,
    ] # 阶段列表 listStage
)

processContent_2 = ProcessContent(
    2, # 编号 id
    :process_2, # 函数名称 functionName
    "process_2", # 文本名称 textName
    [
        stageContent_2,
        stageContent_3,
    ] # 阶段列表 listStage
)


modelContent_1 = ModelContent(
    1, # 编号 id
    :model_1, # 函数名称 functionName
    "model_1", # 文本名称 textName
    [
        processContent_1,
        processContent_2,
    ] # 过程列表 listProcess
)




