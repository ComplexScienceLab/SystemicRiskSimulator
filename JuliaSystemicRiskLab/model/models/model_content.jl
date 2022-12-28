"变量：模型列表"

## 列出各模型结构体实例

##########################################
#状态/可扩展
##########################################

modelContent_BI1111 = ModelContent(
    1, # 编号 id
    :model_BI1111, # 函数名称 functionName
    "模型BI1111", # 文本名称 textName
    [
        processContent_exBank_insolvent,
        processContent_interBank_insolvent,
        processContent_exBank_illiquid,
        processContent_interBank_illiquid,
        # processContent_interBank_bankrupt #BUG 先暂时不考虑，因为这个过程还未完成。目前为了测试调度框架。
    ], # 过程内容列表 listContentProcess
)

# BUG 这个是为了凑数。
modelContent_BI1112 = ModelContent(
    2, # 编号 id
    :model_BI1112, # 函数名称 functionName
    "模型BI1112", # 文本名称 textName
    [
        processContent_exBank_insolvent,
        processContent_interBank_insolvent,
        # processContent_interBank_bankrupt #BUG 先暂时不考虑，因为这个过程还未完成。目前为了测试调度框架。
    ], # 过程内容列表 listContentProcess
)





