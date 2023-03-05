"""
银行存款挤兑流动过程初始态实体
"""

# import here

entityData_ExBankIlliquid = dict(
    attribute=dict(
        id=2030,
        entity_name="entity_ExBankIlliquid",
        text_name="银行存款挤兑流动过程",
        node_type={"container node", "process node"},
        content_type={"algorithm content"},
    ),
    execute="Processor.process_entity",
    content=None,  # TODO等需要的时候再写
    container=list([
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
