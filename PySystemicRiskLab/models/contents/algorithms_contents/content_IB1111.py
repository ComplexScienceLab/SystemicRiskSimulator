"""
模型算法IB1111
"""

from PySystemicRiskLab import label
from PySystemicRiskLab.core.operations.processor import Processor as p
from PySystemicRiskLab.core.operations.builder import Builder as b

pass  # end import


# from PySystemicRiskLab.models_entities.algorithms_contents import *

def content_IB1111():  #TODO等需要的时候再写
    ## # 算法IB1111

    process_00 = b.build_process("START")
    process_01 = b.build_process("entity_ExBankInsolvent")
    process_02 = b.build_process("entity_InterBankInsolvent")
    process_03 = b.build_process("entity_ExBankIlliquid")
    process_04 = b.build_process("entity_InterBankIlliquid")
    process_05 = b.build_process("entity_InterBankBankrupt")

    p.process_processEntity(process_00)
    p.process_processEntity(process_01)
    condition_01, out_flow_entity = p.process_conditionEntity(process_01)
    for c in condition_01:
        if c is True:
            p.process_processEntity("entity_ExBankInsolvent")

    label .process_02

    entity_InterBankInsolvent

    pass  # method
