"""
流动性短缺银行间挤兑流动过程模型之初始态
"""

# import here

entityData_InterBankIlliquid = dict(
    attribute=dict(
        id="user2040",
        entity_name="InterBankIlliquid",
        text_name="流动性短缺银行间挤兑流动过程",
        entity_type={"template entity"},
        structure_type={"container structure", "process structure"},
        container_type={"branch container"},
        process_type={"executive process"},
        content_type={"model content"},
    ),
    execute="Processor.process_entity_by_process_and_container_component",
    process="content_InterBankIlliquid",
    container=dict({
        "node_START": "START",
        "node_01": "InterBankIlliquidContagionShock",
        "node_02": "InterBankIlliquidAllocate",
        "node_03": "InterBankIlliquidRepay",
        "node_END": "END",
    }),
    condition=None,
    content=None,
    node=None,
)
