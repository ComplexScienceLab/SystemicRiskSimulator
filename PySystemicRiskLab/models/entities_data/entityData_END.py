"""
结束实体
"""

entityData_END = dict(
    attribute=dict(
        id="user9999",
        entity_name="entity_END",
        text_name="结束过程",
        node_type={"process node"},
        content_type={"process content"},
    ),
    # execute="Processor.process_entity_by_node_component",
    execute="Processor.process_entity_by_process_and_container_component",
    # execute=None,
    process=None,
    container=None,
    condition=None,
    node=None,
    content=None,
)