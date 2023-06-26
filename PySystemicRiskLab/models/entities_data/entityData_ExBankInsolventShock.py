"""
外部资产违约损失冲击过程初始态实体
"""

# import here

pass  # end import

entityData_ExBankInsolventShock = dict(
    attribute=dict(
        id="user2010",
        # id="user4010", BUG，用于测试是否能够正确检测出重复的id
        entity_name="entity_ExBankInsolventShock",
        text_name="外部资产违约损失冲击",
        node_type={"content node"},
        content_type={"algorithm content"},
    ),
    execute="content_ExBankInsolventShock",
    process=None,
    container=None,
    condition=None,
    node=None,
    content=None,
)
