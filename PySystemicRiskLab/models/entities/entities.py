"""
过程实体
"""

##########################################
# 状态/可扩展
##########################################

from PySystemicRiskLab.core.define.define_entity import Entity

pass  # end import

modelEntity_IB1111 = Entity(
    id=1111,
)

modelEntity_IB0000 = Entity(  # BUG 这个是为了凑数，防止出现遍历的时候只能遍历字符串的bug。
    id=0000,
)

processEntity_ExBankInsolvent = Entity(
    id=2010,
)

processEntity_InterBankInsolvent = Entity(
    id=2020,
)

processEntity_ExBankIlliquid = Entity(
    id=2030,
)

processEntity_InterBankIlliquid = Entity(
    id=2040,
)

# #HACK 用不到 processEntity_ExBankBankrupt = Entity(
#    id= 2050,
#    
processEntity_InterBankBankrupt = Entity(
    id=2060,
)

algorithmEntity_ExBankInsolventShock = Entity(
    id=4010,
)

algorithmEntity_InterBankInsolventShock = Entity(
    id=4020,
)

algorithmEntity_InterBankInsolventContagion = Entity(
    id=4030,
)

algorithmEntity_ExBankIlliquidShock = Entity(
    id=4040,
)

algorithmEntity_InterBankIlliquidContagionShock = Entity(
    id=4050,
)

algorithmEntity_InterBankIlliquidAllocate = Entity(
    id=4060,
)

algorithmEntity_InterBankIlliquidRepay = Entity(
    id=4070,
)

algorithmEntity_ExBankBankruptContagion = Entity(
    id=4080,
)

algorithmEntity_BankruptRepayShock = Entity(
    id=4090,
)

algorithmEntity_InterBankBankruptContagionShock = Entity(
    id=4100,
)
