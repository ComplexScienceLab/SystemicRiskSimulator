"变量：阶段列表"

## 列出各阶段结构体实例

##########################################
# 状态/可扩展
##########################################

from PySystemicRiskLab.core.define.define_content import StageContent
from PySystemicRiskLab.model.stages import *
pass  # end import



stageContent_exBank_insolvent_shock = StageContent(
    id=1,  # 编号 id
    function_name='stage_exBank_insolvent_shock',  # 函数名称 functionName
    text_name="银行外部违约损失冲击阶段",  # 文本名称 textName
    model_function=stage_exBank_insolvent_shock  # 函数 run
)

stageContent_interBank_insolvent_shock = StageContent(
    id=2,  # 编号 id
    function_name='stage_interBank_insolvent_shock',  # 函数名称 functionName
    text_name="资不抵债银行间违约损失冲击阶段",  # 文本名称 textName
    model_function=stage_interBank_insolvent_shock  # 函数 run
)

stageContent_interBank_insolvent_contagion = StageContent(
    id=3,  # 编号 id
    function_name='stage_interBank_insolvent_contagion',  # 函数名称 functionName
    text_name="资不抵债银行间违约损失传染阶段",  # 文本名称 textName
    model_function=stage_interBank_insolvent_contagion  # 函数 run
)

stageContent_exBank_illiquity_shock = StageContent(
    id=4,  # 编号 id
    function_name='stage_exBank_illiquity_shock',  # 函数名称 functionName
    text_name="银行外部挤兑流动冲击阶段",  # 文本名称 textName
    model_function=stage_exBank_insolvent_shock  # 函数 run
)

stageContent_interBank_illiquity_contagion_shock = StageContent(
    id=5,  # 编号 id
    function_name='stage_interBank_illiquity_contagion_shock',  # 函数名称 functionName
    text_name="流动性短缺银行间挤兑流动传染冲击阶段",  # 文本名称 textName
    model_function=stage_interBank_illiquity_contagion_shock  # 函数 run
)

stageContent_interBank_illiquity_allocate = StageContent(
    id=6,  # 编号 id
    function_name='stage_interBank_illiquity_allocate',  # 函数名称 functionName
    text_name="银行间挤兑流动分配借贷流量阶段",  # 文本名称 textName
    model_function=stage_interBank_illiquity_allocate  # 函数 run
)

stageContent_interBank_illiquity_repay = StageContent(
    id=7,  # 编号 id
    function_name='stage_interBank_illiquity_repay',  # 函数名称 functionName
    text_name="银行间挤兑流动执行借贷流量阶段",  # 文本名称 textName
    model_function=stage_interBank_illiquity_repay  # 函数 run
)

stageContent_exBank_bankrupt_contagion = StageContent(
    id=8,  # 编号 id
    function_name='stage_exBank_bankrupt_contagion',  # 函数名称 functionName
    text_name="外生破产银行间挤兑流动冲击阶段",  # 文本名称 textName
    model_function=stage_exBank_bankrupt_contagion  # 函数 run
)

stageContent_bankrupt_repay_shock = StageContent(
    id=9,  # 编号 id
    function_name='stage_bankrupt_repay_shock',  # 函数名称 functionName
    text_name="破产银行应偿还负债冲击阶段",  # 文本名称 textName # FIXME
    model_function=stage_bankrupt_repay_shock  # 函数 run
)

stageContent_interBank_bankrupt_contagion_shock = StageContent(
    id=10,  # 编号 id
    function_name='stage_interBank_bankrupt_contagion_shock',  # 函数名称 functionName
    text_name="破产银行间挤兑流动传染冲击阶段",  # 文本名称 textName
    model_function=stage_interBank_bankrupt_contagion_shock  # 函数 run
)
