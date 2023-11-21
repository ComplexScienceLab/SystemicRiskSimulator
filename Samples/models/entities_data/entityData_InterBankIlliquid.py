"""流动性短缺银行间挤兑流动过程初始态实体"""

# import here

entityData_InterBankIlliquid = dict(
    attribute=dict(
        id="user2040",
        entity_name="InterBankIlliquid",
        text_name="流动性短缺银行间挤兑流动过程",
        node_type={"container node", "process node"},
        content_type={"algorithm content"},
    ),
    # execute="Processor.process_entity_by_node_component",
    execute="Processor.process_entity_by_process_and_container_component",
    # execute=None,
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
                content="entity_InterBankIlliquidContagionShock",
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
                content="entity_InterBankIlliquidAllocate",
                process=list([
                    dict(
                        arrow=dict(
                            condition="True",
                            direction="node_03",
                        ),
                    ),
                ]),
            ),
        ),
        dict(
            node=dict(
                name="node_03",
                content="entity_InterBankIlliquidRepay",
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
