"""资不抵债银行间违约损失过程初始态实体"""

# import here

entityData_InterBankInsolvent = dict(
    attribute=dict(
        id=2020,
        entity_name="entity_InterBankInsolvent",
        text_name="资不抵债银行间违约损失过程",
        node_type={"container node", "process node"},
        content_type={"algorithm content"},
    ),
    execute="Processor.process",
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
