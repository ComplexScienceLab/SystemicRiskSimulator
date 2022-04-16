"变量：过程列表"

## 列出各过程结构体实例

##########################################
#状态/可扩展
##########################################

process_exBank_insolvent = ProcessContent(
    1, # 编号 id
    :process_exBank_insolvent, # 函数名称 functionName
    "银行外部违约损失传染冲击过程", # 文本名称 textName
    [
        :stage_exBank_insolvent_shock,
        :stage_interBank_insolvent_contagion,
    ] # 阶段列表 listStage
)

process_interBank_insolvent = ProcessContent(
    2, # 编号 id
    :process_interBank_insolvent, # 函数名称 functionName
    "资不抵债银行间违约损失传染冲击过程", # 文本名称 textName
    [
        :stage_interBank_insolvent_shock,
        :stage_interBank_insolvent_contagion,
    ] # 阶段列表 listStage
)

process_exBank_illiquity = ProcessContent(
    3, # 编号 id
    :process_exBank_illiquity, # 函数名称 functionName
    "银行外部挤兑流动传染冲击过程", # 文本名称 textName
    [
        :stage_exBank_illiquity_shock,
    ] # 阶段列表 listStage
)

process_interBank_illiquity = ProcessContent(
    4, # 编号 id
    :process_interBank_illiquity, # 函数名称 functionName
    "流动性短缺银行间挤兑流动传染冲击过程", # 文本名称 textName
    [
        :stage_interBank_illiquity_contagion_shock,
        :stage_interBank_illiquity_allocate,
        :stage_interBank_illiquity_repay,
    ] # 阶段列表 listStage
)

process_exBank_bankrupt = ProcessContent(
    5, # 编号 id
    :process_exBank_bankrupt, # 函数名称 functionName
    "外生破产银行间挤兑流动传染冲击过程", # 文本名称 textName
    [
        :exBank_bankrupt_shock,
    ] # 阶段列表 listStage
)

process_interBank_bankrupt = ProcessContent(
    6, # 编号 id
    :process_exBank_bankrupt, # 函数名称 functionName
    "破产银行间挤兑流动传染冲击过程", # 文本名称 textName
    [
        :stage_interBank_bankrupt_contagion_shock,
        :stage_interBank_illiquity_allocate,
        :stage_interBank_illiquity_repay,
    ] # 阶段列表 listStage
)




