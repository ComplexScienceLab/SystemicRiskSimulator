"""
开始实体
"""

entityData_START = dict(
    attribute=dict(
        id=0000,
        entity_name="entity_START",
        text_name="开始",
        node_type={"process node"},
        content_type={"process content"},
    ),
    execute="Processor.process_entity",
    content=None,
    container=None,
)
