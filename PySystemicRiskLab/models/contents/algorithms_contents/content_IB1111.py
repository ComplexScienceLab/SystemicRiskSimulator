"""
模型算法IB1111
"""

from PySystemicRiskLab import label
from PySystemicRiskLab.core.operations.processor import Processor as p
from PySystemicRiskLab.core.operations.builder import Builder as b

pass  # end import


# from PySystemicRiskLab.models_entities.algorithms_contents import *

def content_IB1111():  # TODO等需要的时候再写
    ## # 算法IB1111

    # TODO改成普通的循环形式处理

    # HACK 2023-05-22以前的版本
    process_START = b.build_process("START")
    process_ExBankInsolvent = b.build_process("entity_ExBankInsolvent")
    process_InterBankInsolvent = b.build_process("entity_InterBankInsolvent")
    process_ExBankIlliquid = b.build_process("entity_ExBankIlliquid")
    process_InterBankIlliquid = b.build_process("entity_InterBankIlliquid")
    process_InterBankBankrupt = b.build_process("entity_InterBankBankrupt")

    p.process_processEntity(process_START)
    p.process_processEntity(process_ExBankInsolvent)
    condition_01, out_flow_entity = p.process_conditionEntity(process_ExBankInsolvent)
    for c in condition_01:
        if c is True:
            p.process_processEntity("entity_ExBankInsolvent")

    label.process_InterBankInsolvent

    entity_InterBankInsolvent

    pass  # method
