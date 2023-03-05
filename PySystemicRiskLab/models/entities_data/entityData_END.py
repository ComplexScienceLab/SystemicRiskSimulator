"""
结束实体
"""

entityData_START = dict(
    attribute=dict(
        id=9999,
        entity_name="entity_END",
        text_name="结束",
        node_type={"process node"},
        content_type={"process content"},
    ),
    execute="Processor.process_entity",
    content=None,
    container=None,
)