"""
模型BI1111
"""
# from PySystemicRiskLab.models.entities.entities import *
# from PySystemicRiskLab.models.contents.processes_contents import *

modelEntityData_ModelBI1111 = dict(
    attribute=dict(
        id=2000,
        entity_name="modelEntity_ModelBI1111",
        text_name="模型BI1111",
        node_type={"process node"},
        content_type={"model content"},
    ),
    content="Processor.process_NodeProcess",
    container=list([
        "processEntity_ExBankInsolvent",
        "processEntity_InterBankInsolvent",
        "processEntity_ExBankIlliquid",
        "processEntity_InterBankIlliquid",
        # "processEntity_InterBankBankrupt" #HACK 先暂时不考虑，因为这个过程还未完成。目前为了测试调度框架。
    ]),
    process=list([
        dict(
            condition=None,
            flow="processEntity_ExBankInsolvent",
        ),
    ]),
)
