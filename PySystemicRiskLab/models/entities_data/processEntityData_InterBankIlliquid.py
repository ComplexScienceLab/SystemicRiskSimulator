"""流动性短缺银行间挤兑流动过程初始态实体"""

# from PySystemicRiskLab.models.entities.entities import *
# from PySystemicRiskLab.models.contents.processes_contents import *

proccssEntityData_InterBankIlliquid = dict(
    attribute=dict(
        id=2040,
        entity_name="processEntity_InterBankIlliquid",
        text_name="流动性短缺银行间挤兑流动过程",
        node_type={"container node","process node"},
        content_type={"algorithm content"},
    ),
    content="Processor.process_NodeProcess",
    container=list([
        "algorithmEntity_InterBankIlliquidContagionShock",
        "algorithmEntity_InterBankIlliquidAllocate",
        "algorithmEntity_InterBankIlliquidRepay",
    ]),
    process=list([
        dict(
            condition="A.BB.ilq.any() != A_data.BB.ilq[env['round']-1].any()",
            flow="processEntity_InterBankIlliquid",
        ),
        dict(
            condition="A.BB.ilq.all() == A_data.BB.ilq[env['round']-1].all()",
            flow=None,
        ),
        # dict( #HACK 先暂时不考虑，因为这个过程还未完成。目前为了测试调度框架。
        #     flow="processEntity_InterBankBankrupt",
        #     condition="TODO",
        # ),
    ]),
)
