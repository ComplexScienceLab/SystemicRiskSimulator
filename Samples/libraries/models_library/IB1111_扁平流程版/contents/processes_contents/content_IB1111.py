"""
模型IB1111
"""
import random
from SystemicRiskSimulator.external_packages import logging
from SystemicRiskSimulator.core.define.define_entity import Entity
from SystemicRiskSimulator.core.operations.processor import Processor as p
from SystemicRiskSimulator.core.operations.builder import Builder as b

# from SystemicRiskSimulator.data.model.contents.models_contents.content_ExBankInsolventShock import content_ExBankInsolventShock
# from SystemicRiskSimulator.data.model.contents.models_contents.content_ExBankIlliquidShock import content_ExBankIlliquidShock
# from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankInsolventShock import content_InterBankInsolventShock
# from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankInsolventContagion import content_InterBankInsolventContagion
# from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankIlliquidContagionShock import content_InterBankIlliquidContagionShock
# from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankIlliquidAllocate import content_InterBankIlliquidAllocate
# from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankIlliquidRepay import content_InterBankIlliquidRepay

pass  # end import

# import SystemicRiskSimulator.data.model.contents


content_IB1111 = \
    """
    define process entity_IB1111
    
    execute content node_START
    
    execute content node_01
    if node_01_condition_01 goto node_02
    if node_01_condition_02 goto node_04
    
    execute content node_02
    
    execute content node_03
    if node_03_condition_01 goto node_02
    if node_03_condition_02 goto node_04
    
    execute content node_04
    if node_04_condition_01 goto node_05
    if node_04_condition_02 goto node_END
    
    execute content node_05
    
    execute content node_06
    
    execute content node_07
    if node_07_condition_01 goto node_05
    if node_07_condition_02 goto node_END
    
    execute content node_END
    
    end define
    """

