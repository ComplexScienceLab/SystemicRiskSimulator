"""
资不抵债银行间违约损失过程模型之初始态
"""

# import here

entity_InterBankInsolvent = dict(
    attribute=dict(
        id="user2020",
        entity_name="InterBankInsolvent",
        text_name="资不抵债银行间违约损失过程",
        entity_type={"template entity"},
        structure_type={"container structure", "process structure"},
        container_type={"branch container"},
        process_type={"executive process"},
        content_type={"model content"},
    ),
    execute="Processor.process_entity_by_process_and_container_component",
    process="content_InterBankInsolvent",
    container=dict({
        "node_START": "START",
        "node_01": "InterBankInsolventContagion",
        "node_02": "InterBankInsolventShock",
        "node_END": "END",
    }),
    condition=None,
    content=None,
    node=None,
)
