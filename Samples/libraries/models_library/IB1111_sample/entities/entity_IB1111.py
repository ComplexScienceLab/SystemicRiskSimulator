"""
模型IB1111之初始态
"""
# import here

entity_IB1111 = dict(
    attribute=dict(
        id="user2000",
        entity_name="IB1111_sample",
        text_name="模型IB1111之非流程多函数版",
        entity_type={"template entity"},
        structure_type={"content structure"},
        container_type={"root container"},
        process_type={"executive process"},
        content_type={"model content"},
    ),
    execute="content_IB1111",
    # execute="Processor.process_entity_by_process_and_container_component",
    process=None,
    # process="content_IB1111",
    container=None,
    # container=dict({
    #     "node_START": "START",
    #     "node_01": "ExBankInsolventShock",
    #     "node_02": "InterBankInsolventContagion",
    #     "node_03": "InterBankInsolventShock",
    #     "node_04": "ExBankIlliquidShock",
    #     "node_05": "InterBankIlliquidContagionShock",
    #     "node_06": "InterBankIlliquidAllocate",
    #     "node_07": "InterBankIlliquidRepay",
    #     "node_END": "END",
    # }),
    condition=None,
    # condition=dict({
    #     "node_01_condition_01": r"(A.BB.isv != A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].isv).any()",  # BUG
    #     "node_01_condition_02": r"(A.BB.isv == A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].isv).all()",
    #     "node_03_condition_01": r"(A.BB.isv != A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].isv).any()",
    #     "node_03_condition_02": r"(A.BB.isv == A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].isv).all()",
    #     "node_04_condition_01": r"(A.BB.ilq != A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].ilq).any()",
    #     "node_04_condition_02": r"(A.BB.ilq == A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].ilq).all()",
    #     "node_07_condition_01": r"(A.BB.ilq != A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].ilq).any()",
    #     "node_07_condition_02": r"(A.BB.ilq == A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].ilq).all()",
    # }),
    content=None,
    node=None,
)
