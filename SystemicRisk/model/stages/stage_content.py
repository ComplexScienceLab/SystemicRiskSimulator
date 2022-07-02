"变量：阶段列表"

## 列出各阶段结构体实例

##########################################
# 状态/可扩展
##########################################

from SystemicRisk.core import StageContent
from SystemicRisk.model import *
pass  # end import



stageContent_exBank_insolvent_shock = StageContent(
    1,  # 编号 id
    'stage_exBank_insolvent_shock',  # 函数名称 functionName
    "银行外部违约损失冲击阶段",  # 文本名称 textName
    stage_exBank_insolvent_shock  # 函数 run
)

stageContent_interBank_insolvent_shock = StageContent(
    2,  # 编号 id
    'stage_interBank_insolvent_shock',  # 函数名称 functionName
    "资不抵债银行间违约损失冲击阶段",  # 文本名称 textName
    stage_interBank_insolvent_shock  # 函数 run
)

stageContent_interBank_insolvent_contagion = StageContent(
    3,  # 编号 id
    'stage_interBank_insolvent_contagion',  # 函数名称 functionName
    "资不抵债银行间违约损失传染阶段",  # 文本名称 textName
    stage_interBank_insolvent_contagion  # 函数 run
)

stageContent_exBank_illiquity_shock = StageContent(
    4,  # 编号 id
    'stage_exBank_illiquity_shock',  # 函数名称 functionName
    "银行外部挤兑流动冲击阶段",  # 文本名称 textName
    stage_exBank_insolvent_shock  # 函数 run
)

stageContent_interBank_illiquity_contagion_shock = StageContent(
    5,  # 编号 id
    'stage_interBank_illiquity_contagion_shock',  # 函数名称 functionName
    "流动性短缺银行间挤兑流动传染冲击阶段",  # 文本名称 textName
    stage_interBank_illiquity_contagion_shock  # 函数 run
)

stageContent_interBank_illiquity_allocate = StageContent(
    6,  # 编号 id
    'stage_interBank_illiquity_allocate',  # 函数名称 functionName
    "银行间挤兑流动分配借贷流量阶段",  # 文本名称 textName
    stage_interBank_illiquity_allocate  # 函数 run
)

stageContent_interBank_illiquity_repay = StageContent(
    7,  # 编号 id
    'stage_interBank_illiquity_repay',  # 函数名称 functionName
    "银行间挤兑流动执行借贷流量阶段",  # 文本名称 textName
    stage_interBank_illiquity_repay  # 函数 run
)

stageContent_exBank_bankrupt_contagion = StageContent(
    8,  # 编号 id
    'stage_exBank_bankrupt_contagion',  # 函数名称 functionName
    "外生破产银行间挤兑流动冲击阶段",  # 文本名称 textName
    stage_exBank_bankrupt_contagion  # 函数 run
)

stageContent_bankrupt_repay_shock = StageContent(
    9,  # 编号 id
    'stage_bankrupt_repay_shock',  # 函数名称 functionName
    "破产银行应偿还负债冲击阶段",  # 文本名称 textName # FIXME
    stage_bankrupt_repay_shock  # 函数 run
)

stageContent_interBank_bankrupt_contagion_shock = StageContent(
    10,  # 编号 id
    'stage_interBank_bankrupt_contagion_shock',  # 函数名称 functionName
    "破产银行间挤兑流动传染冲击阶段",  # 文本名称 textName
    stage_interBank_bankrupt_contagion_shock  # 函数 run
)
