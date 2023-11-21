"""
开始实体
"""

entityData_START = dict(
    attribute=dict(
        id="user0000",
        entity_name="START",
        text_name="开始过程",
        node_type={"process node"},
        content_type={"process content"},
    ),
    # execute="Processor.process_entity_by_node_component",
    execute="Processor.process_entity_by_process_and_container_component",
    # execute=None,
    process=None,
    container=None,
    condition=None,
    content=None,
    node=None,
)
