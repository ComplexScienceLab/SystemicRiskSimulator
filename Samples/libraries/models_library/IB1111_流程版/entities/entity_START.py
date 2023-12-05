"""
开始实体模型之初始态
"""

entity_START = dict(
    attribute=dict(
        id="user0000",
        entity_name="START",
        text_name="开始过程",
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
    content=None,
    node=None,
)
