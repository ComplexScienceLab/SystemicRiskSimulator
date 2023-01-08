"""资不抵债银行间违约损失过程初始态实体"""

# from PySystemicRiskLab.models.entities.entities import *
# from PySystemicRiskLab.models.contents.processes_contents import *

processEntityData_InterBankInsolvent = dict(
    attribute=dict(
        id=2020,
        entity_name="processEntity_InterBankInsolvent",
        text_name="资不抵债银行间违约损失过程",
        node_type={"container node","process node"},
        content_type={"algorithm content"},
    ),
    content="Processor.process_NodeProcess",
    container=list([
        "algorithmEntity_InterBankInsolventContagion",
        "algorithmEntity_InterBankInsolventShock",
    ]),
    process=list([
        dict(
            condition="A.BB.isv.any() != A_data.BB.isv[env['round']-1].any()",
            flow="processEntity_InterBankInsolvent",
        ),
        dict(
            condition="A.BB.isv.all() == A_data.BB.isv[env['round']-1].all()",
            flow="processEntity_ExBankIlliquid",
        ),
    ]),
)
