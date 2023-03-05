"""
实体数据之模型IB1111
"""
# import here

entityData_IB1111 = dict(
    attribute=dict(
        id=2000,
        entity_name="entity_IB1111",
        text_name="模型算法IB1111",
        node_type={"container node", "process node"},
        content_type={"model content"},
    ),
    execute="Processor.process_entity",
    content="content_IB1111",
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
                content="entity_ExBankInsolvent",
                process=list([
                    dict(
                        arrow=dict(
                            condition="(A.BB.isv != A_data.BB[env['round']-1]['dataBB'].isv).any()",
                            direction="node_02",
                        ),
                    ),
                    dict(
                        arrow=dict(
                            condition="(A.BB.isv == A_data.BB[env['round']-1]['dataBB'].isv).all()",
                            direction="node_03",
                        ),
                    ),
                ]),
            ),
        ),
        dict(
            node=dict(
                name="node_02",
                content="entity_InterBankInsolvent",
                process=list([
                    dict(
                        arrow=dict(
                            condition="(A.BB.isv != A_data.BB[env['round']-1]['dataBB'].isv).any()",
                            direction="node_02",
                        ),
                    ),
                    dict(
                        arrow=dict(
                            condition="(A.BB.isv == A_data.BB[env['round']-1]['dataBB'].isv).all()",
                            direction="node_03",
                        ),
                    ),
                ]),
            ),
        ),
        dict(
            node=dict(
                name="node_03",
                content="entity_ExBankIlliquid",
                process=list([
                    dict(
                        arrow=dict(
                            condition="(A.BB.ilq != A_data.BB[env['round']-1]['dataBB'].ilq).any()",
                            direction="node_04",
                        ),
                    ),
                    dict(
                        arrow=dict(
                            condition="(A.BB.ilq == A_data.BB[env['round']-1]['dataBB'].ilq).all()",
                            direction="node_END",
                        ),
                    ),
                ]),
            ),
        ),
        dict(
            node=dict(
                name="node_04",
                content="entity_InterBankIlliquid",
                process=list([
                    dict(
                        arrow=dict(
                            condition="(A.BB.ilq != A_data.BB[env['round']-1]['dataBB'].ilq).any()",
                            direction="node_04",
                        ),
                    ),
                    dict(
                        arrow=dict(
                            condition="(A.BB.ilq == A_data.BB[env['round']-1]['dataBB'].ilq).all()",
                            direction="node_END",
                        ),
                    ),
                    # dict( #HACK 先暂时不考虑，因为这个过程还未完成。目前为了测试调度框架。
                    #     direction="entity_InterBankBankrupt",
                    #     condition=" TODO ",
                    # ),
                ]),
            ),
        ),
        # dict(#HACK 先暂时不考虑，因为这个过程还未完成。目前为了测试调度框架。
        #     node=dict(
        #         name="node_05",
        #         content="entity_InterBankBankrupt",
        #         process=list([
        #         ]),
        #     ),
        # ),
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
    ])
)
