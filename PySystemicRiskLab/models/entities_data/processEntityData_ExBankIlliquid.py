"""
银行外部挤兑流动过程初始态实体
"""
# from PySystemicRiskLab.models.entities.entities import *
# from PySystemicRiskLab.models.contents.processes_contents import *

processEntityData_ExBankIlliquid = dict(
    attribute=dict(
        id=2030,
        entity_name="processEntity_ExBankIlliquid",
        text_name="银行外部挤兑流动过程",
        node_type={"container node","process node"},
        content_type={"algorithm content"},
    ),
    content="Processor.process_NodeProcess",
    container=list([
        "algorithmEntity_ExBankIlliquidShock",
    ]),
    process=list([
        dict(
            condition="A.BB.ilq.any() != A_data.BB[env['round']-1]['dataBB'].ilq.any()",
            flow="processEntity_InterBankIlliquid",
        ),
        dict(
            condition="A.BB.ilq.all() == A_data.BB[env['round']-1]['dataBB'].ilq.all()",
            flow=None,
        ),
    ]),
)
