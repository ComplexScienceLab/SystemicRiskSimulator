"""
模型算法IB1111
"""
import random
from PySystemicRiskLab import logging
from PySystemicRiskLab.core.define.define_entity import Entity
from PySystemicRiskLab.core.operations.processor import Processor as p
from PySystemicRiskLab.core.operations.builder import Builder as b

# from PySystemicRiskLab.models.contents.algorithms_contents.content_ExBankInsolventShock import content_ExBankInsolventShock
# from PySystemicRiskLab.models.contents.algorithms_contents.content_ExBankIlliquidShock import content_ExBankIlliquidShock
# from PySystemicRiskLab.models.contents.algorithms_contents.content_InterBankInsolventShock import content_InterBankInsolventShock
# from PySystemicRiskLab.models.contents.algorithms_contents.content_InterBankInsolventContagion import content_InterBankInsolventContagion
# from PySystemicRiskLab.models.contents.algorithms_contents.content_InterBankIlliquidContagionShock import content_InterBankIlliquidContagionShock
# from PySystemicRiskLab.models.contents.algorithms_contents.content_InterBankIlliquidAllocate import content_InterBankIlliquidAllocate
# from PySystemicRiskLab.models.contents.algorithms_contents.content_InterBankIlliquidRepay import content_InterBankIlliquidRepay

pass  # end import

# import PySystemicRiskLab.models.contents  # NOTE 动态导入，严禁删除


content_IB1111 = \
    """
    define process entity_IB1111
    
    execute content node_START
    
    execute process node_01
    if node_01_condition_01 goto node_02
    if node_01_condition_02 goto node_03
    
    execute process node_02
    if node_02_condition_01 goto node_02
    if node_02_condition_02 goto node_03
    
    execute process node_03
    if node_03_condition_01 goto node_04
    if node_03_condition_02 goto node_END
    
    execute process node_04
    if node_04_condition_01 goto node_04
    if node_04_condition_02 goto node_END
    
    execute content node_END
    
    end define
    """

#
#
# ## 定义实体entity_IB1111之各节点node之条件condition
# condition_01 = "random.sample(range(1,100),1)>10"
# condition_02 = "random.sample(range(1,100),1)<=10"
# condition_01 = "random.sample(range(1,100),1)>10"
# condition_02 = "random.sample(range(1,100),1)<=10"
# condition_01 = "random.sample(range(1,100),1)>10"
# condition_02 = "random.sample(range(1,100),1)<=10"
# condition_01 = "random.sample(range(1,100),1)>10"
# condition_02 = "random.sample(range(1,100),1)<=10"
# # condition_01 = "(A.BB.isv != A_data.BB[env['round']-1]['dataBB'].isv).any()"
# # condition_02 = "(A.BB.isv == A_data.BB[env['round']-1]['dataBB'].isv).all()"
# # condition_01 = "(A.BB.isv != A_data.BB[env['round']-1]['dataBB'].isv).any()"
# # condition_02 = "(A.BB.isv == A_data.BB[env['round']-1]['dataBB'].isv).all()"
# # condition_01 = "(A.BB.ilq != A_data.BB[env['round']-1]['dataBB'].ilq).any()"
# # condition_02 = "(A.BB.ilq == A_data.BB[env['round']-1]['dataBB'].ilq).all()"
# # condition_01 = "(A.BB.ilq != A_data.BB[env['round']-1]['dataBB'].ilq).any()"
# # condition_02 = "(A.BB.ilq == A_data.BB[env['round']-1]['dataBB'].ilq).all()"


# ## 定义各实体之具体函数之内容
#
# ## 开始实体
# def entity_START():
#     print("Executing entity_START")
#
#
# ## 结束实体
# def entity_END():
#     print("Executing entity_END")
#
#
# def entity_ExBankInsolventShock():
#     print("Executing entity_ExBankInsolventShock")
#
#
# def entity_InterBankInsolventContagion():
#     print("Executing entity_InterBankInsolventContagion")
#
#
# def entity_InterBankInsolventShock():
#     print("Executing entity_InterBankInsolventShock")
#
#
# def entity_ExBankIlliquidShock():
#     print("Executing entity_ExBankIlliquidShock")
#
#
# def entity_InterBankIlliquidContagionShock():
#     print("Executing entity_InterBankIlliquidContagionShock")
#
#
# def entity_InterBankIlliquidAllocate():
#     print("Executing entity_InterBankIlliquidAllocate")
#
#
# def entity_InterBankIlliquidRepay():
#     print("Executing entity_InterBankIlliquidRepay")
