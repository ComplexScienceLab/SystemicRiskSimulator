"""
模型IB1111之初始态
"""
# import here

entityData_IB1111 = dict(
    attribute=dict(
        id="user2000",
        entity_name="IB1111",
        text_name="模型IB1111",
        entity_type={"template entity"},
        structure_type={"container structure", "process structure"},
        container_type={"root container"},
        process_type={"executive process"},
        content_type={"model content"},
    ),
    execute="Processor.process_entity_by_process_and_container_component",
    process="content_IB1111",
    container=dict({
        "node_START": "START",
        "node_01": "ExBankInsolvent",
        "node_02": "InterBankInsolvent",
        "node_03": "ExBankIlliquid",
        "node_04": "InterBankIlliquid",
        "node_END": "END",
    }),
    condition=dict({
        "node_01_condition_01": r"(A.BB.isv != A_data.BB[A_data.BB['round'] == env['round'] - 1].iloc[-1].isv).any()",  # BUG
        "node_01_condition_02": r"(A.BB.isv == A_data.BB[A_data.BB['round'] == env['round'] - 1].iloc[-1].isv).all()",
        "node_02_condition_01": r"(A.BB.isv != A_data.BB[A_data.BB['round'] == env['round'] - 1].iloc[-1].isv).any()",
        "node_02_condition_02": r"(A.BB.isv == A_data.BB[A_data.BB['round'] == env['round'] - 1].iloc[-1].isv).all()",
        "node_03_condition_01": r"(A.BB.ilq != A_data.BB[A_data.BB['round'] == env['round'] - 1].iloc[-1].ilq).any()",
        "node_03_condition_02": r"(A.BB.ilq == A_data.BB[A_data.BB['round'] == env['round'] - 1].iloc[-1].ilq).all()",
        "node_04_condition_01": r"(A.BB.ilq != A_data.BB[A_data.BB['round'] == env['round'] - 1].iloc[-1].ilq).any()",
        "node_04_condition_02": r"(A.BB.ilq == A_data.BB[A_data.BB['round'] == env['round'] - 1].iloc[-1].ilq).all()",
    }),
    content=None,
    node=None,
)
