"""
模型BI0000
"""
# from PySystemicRiskLab.models.entities.entities import *
# from PySystemicRiskLab.models.contents.processes_contents import *

modelEntityData_ModelBI0000 = dict(
    attribute=dict(
        id=2000,
        entity_name="modelEntity_ModelBI0000",
        text_name="模型BI0000",
        node_type={"process node"},
        content_type={"model content"},
    ),
    content="Processor.process_NodeProcess",
    container=list([
        "processEntity_ExBankInsolvent", # BUG 这个是为了凑数，防止出现遍历的时候只能遍历字符串的bug。
    ]),
    process=list([
        dict(
            condition=None,
            flow="processEntity_ExBankInsolvent",
        ),
    ]),
)
