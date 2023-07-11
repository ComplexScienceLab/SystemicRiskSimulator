"""资不抵债银行间违约损失过程初始态实体"""

# import here

entityData_InterBankInsolvent = dict(
    attribute=dict(
        id="user2020",
        entity_name="InterBankInsolvent",
        text_name="资不抵债银行间违约损失过程",
        node_type={"container node", "process node"},
        content_type={"algorithm content"},
    ),
    # execute="Processor.process_entity_by_node_component",
    execute="Processor.process_entity_by_process_and_container_component",
    # execute=None,
    process="content_InterBankInsolvent",
    container=dict({
        "node_START": "START",
        "node_01": "InterBankInsolventContagion",
        "node_02": "InterBankInsolventShock",
        "node_END": "END",
    }),
    condition=None,
    content=None,
    node=list([
        dict(
            node=dict(
                name="node_START",
                content="entity_START",
                process=list([
                    dict(
                        arrow=dict(
                            condition="True",
                            direction="node_01",
                        ),
                    ),
                ]),
            ),
        ),
        dict(
            node=dict(
                name="node_01",
                content="entity_InterBankInsolventContagion",
                process=list([
                    dict(
                        arrow=dict(
                            condition="True",
                            direction="node_02",
                        ),
                    ),
                ]),
            ),
        ),
        dict(
            node=dict(
                name="node_02",
                content="entity_InterBankInsolventShock",
                process=list([
                    dict(
                        arrow=dict(
                            condition="True",
                            direction="node_END",
                        ),
                    ),
                ]),
            ),
        ),
        dict(
            node=dict(
                name="node_END",
                content="entity_END",
                process=list([
                    dict(
                        arrow=None,
                    ),
                ]),
            ),
        ),
    ]),
)
