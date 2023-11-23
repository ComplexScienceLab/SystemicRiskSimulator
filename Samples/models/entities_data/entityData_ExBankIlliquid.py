"""
银行存款挤兑流动过程模型之初始态
"""

# import here

entityData_ExBankIlliquid = dict(
    attribute=dict(
        id="user2030",
        entity_name="ExBankIlliquid",
        text_name="银行存款挤兑流动过程",
        entity_type={"template entity"},
        structure_type={"container structure", "process structure"},
        container_type={"branch container"},
        process_type={"executive process"},
        content_type={"model content"},
    ),
    execute="Processor.process_entity_by_process_and_container_component",
    process="content_ExBankIlliquid",
    container=dict({
        "node_START": "START",
        "node_01": "ExBankIlliquidShock",
        "node_END": "END",
    }),
    condition=None,
    content=None,
    node=None,
)
