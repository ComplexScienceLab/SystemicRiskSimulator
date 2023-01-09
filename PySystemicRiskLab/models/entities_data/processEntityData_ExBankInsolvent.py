"""
银行外部违约损失过程初始态实体
"""

# from PySystemicRiskLab.models.entities.entities import *
# from PySystemicRiskLab.models.contents.processes_contents import *

processEntityData_ExBankInsolvent = dict(
    attribute=dict(
        id=2010,
        entity_name="processEntity_ExBankInsolvent",
        text_name="银行外部违约损失过程",
        node_type={"container node","process node"},
        content_type={"algorithm content"},
    ),
    content="Processor.process_NodeProcess",
    container=list([
        "algorithmEntity_ExBankInsolventShock",
        # "algorithmEntity_InterBankInsolventContagion",
    ]),
    process=list([
        dict(
            condition="A.BB.isv.any() != A_data.BB[env['round']-1]['dataBB'].isv.any()",
            flow="processEntity_InterBankInsolvent",
        ),
        dict(
            condition="A.BB.isv.all() == A_data.BB[env['round']-1]['dataBB'].isv.all()",
            flow="processEntity_ExBankIlliquid",
        ),
    ]),
)
