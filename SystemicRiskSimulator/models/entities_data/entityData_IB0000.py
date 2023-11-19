# """
# 实体数据之模型IB0000
# """
# # import here
#
# entityData_IB0000 = dict(
#     attribute=dict(
#         id="user2000",
#         entity_name="entity_IB0000",
#         text_name="模型算法IB0000",
#         node_type={"container node", "process node"},
#         content_type={"model content"},
#     ),
#     execute="Processor.process",
#     content="content_IB0000",
#     node=list([
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
