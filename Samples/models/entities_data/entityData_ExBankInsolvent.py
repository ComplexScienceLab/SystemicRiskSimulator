"""
外部资产违约损失过程模型之初始态
"""

# import here

entityData_ExBankInsolvent = dict(

    attribute=dict(
        id="user2010",
        entity_name="ExBankInsolvent",
        text_name="外部资产违约损失过程",
        entity_type={"template entity"},
        structure_type={"container structure", "process structure"},
        container_type={"branch container"},
        process_type={"executive process"},
        content_type={"model content"},
    ),
    execute="Processor.process_entity_by_process_and_container_component",
    process="content_ExBankInsolvent",
    container=dict({
        "node_START": "START",
        "node_01": "ExBankInsolventShock",
        "node_END": "END",
    }),
    condition=None,
    content=None,
    node=None,
)
