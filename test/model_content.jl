"变量：模型列表"

## 列出各模型结构体实例

##########################################
#状态/可扩展
##########################################

# model_BI1111 = ModelContent(
#     1, # 编号 id
#     :model_BI1111, # 函数名称 functionName
#     "模型BI1111", # 文本名称 textName
#     [
#         :process_exBank_insolvent,
#         :process_interBank_insolvent,
#         :process_exBank_illiquity,
#         :process_interBank_illiquity,
#         :process_interBank_bankrupt
#     ] # 过程列表 listProcess
# )

model_BI1111 = ModelContent(
    1, # 编号 id
    :model_BI1111, # 函数名称 functionName
    "模型BI1111", # 文本名称 textName
    [
        process_exBank_insolvent,
        process_interBank_insolvent,
        process_exBank_illiquity,
        process_interBank_illiquity,
        process_interBank_bankrupt
    ] # 过程列表 listProcess
)





