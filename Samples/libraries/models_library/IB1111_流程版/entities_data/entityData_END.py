"""
结束实体模型之初始态
"""

entityData_END = dict(
    attribute=dict(
        id="user9999",
        entity_name="END",
        text_name="结束过程",
        entity_type={"template entity"},
        structure_type={"process structure"},
        container_type={"leaf container"},
        process_type={"schedule process"},
        content_type={"model content"},
    ),
    execute="Processor.process_entity_by_process_and_container_component",
    process=None,
    container=None,
    condition=None,
    node=None,
    content=None,
)