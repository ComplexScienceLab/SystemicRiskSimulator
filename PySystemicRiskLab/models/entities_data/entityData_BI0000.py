# """
# 实体数据之模型BI0000
# """
# # import here
#
# entityData_BI0000 = dict(
#     attribute=dict(
#         id=2000,
#         entity_name="entity_BI0000",
#         text_name="模型算法BI0000",
#         node_type={"container node", "process node"},
#         content_type={"model content"},
#     ),
#     execute="Processor.process",
#     content="content_BI0000",
#     container=list([
#         dict(
#             node=dict(
#                 name="node_START",
#                 content="entity_START",
#                 process=list([
#                     dict(
#                         arrow=dict(
#                             condition="True",
#                             direction="node_END",
#                         ),
#                     ),
#                 ]),
#             ),
#         ),
#         dict(
#             node=dict(
#                 name="node_END",
#                 content="entity_END",
#                 process=list([
#                     dict(
#                         arrow=None,
#                     ),
#                 ]),
#             ),
#         ),
#     ])
# )
