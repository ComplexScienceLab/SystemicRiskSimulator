"数据：阶段名称集合"
## 配置各阶段专有名称
##########################################
#状态/可扩展
##########################################

set_stageName = Set([
    :stage_exBank_insolvent_shock,
    :stage_interBank_insolvent_shock,
    :stage_interBank_insolvent_contagion,
    :stage_exBank_illiquity_shock,
    :stage_interBank_illiquity_contagion_shock,
    :stage_interBank_illiquity_allocate,
    :stage_interBank_illiquity_repay,
    :stage_exBank_bankrupt_contagion,
    :stage_interBank_bankrupt_contagion_shock,
    :stage_bankrupt_repay_shock,
])