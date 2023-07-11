"""
银行存款挤兑流动过程初始态实体
"""

# import here

entityData_ExBankIlliquid = dict(
    attribute=dict(
        id="user2030",
        entity_name="ExBankIlliquid",
        text_name="银行存款挤兑流动过程",
        node_type={"container node", "process node"},
        content_type={"algorithm content"},
    ),
    # execute="Processor.process_entity_by_node_component",
    execute="Processor.process_entity_by_process_and_container_component",
    # execute=None,
    process="content_ExBankIlliquid",
    container=dict({
        "node_START": "START",
        "node_01": "ExBankIlliquidShock",
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
                            direction="node_01"
                        ),
                    ),
                ]),
            ),
        ),
        dict(
            node=dict(
                name="node_01",
                content="entity_ExBankIlliquidShock",
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
