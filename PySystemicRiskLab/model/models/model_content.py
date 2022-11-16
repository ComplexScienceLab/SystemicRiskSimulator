"变量：模型列表"

## 列出各模型结构体实例

##########################################
# 状态/可扩展
##########################################

from PySystemicRiskLab.core.define.define_content import ModelContent
# from PySystemicRiskLab.models import processContent_exBank_insolvent, processContent_interBank_insolvent, processContent_exBank_illiquity, processContent_interBank_illiquity
from PySystemicRiskLab.model.processes import *

pass  # end import

modelContent_BI1111 = ModelContent(
    id=1,  # 编号 id
    function_name='model_BI1111',  # 函数名称 functionName
    text_name="模型BI1111",  # 文本名称 textName
    list_process_content=[
        processContent_exBank_insolvent,
        processContent_interBank_insolvent,
        processContent_exBank_illiquity,
        processContent_interBank_illiquity,
        # processContent_interBank_bankrupt #BUG 先暂时不考虑，因为这个过程还未完成。目前为了测试调度框架。
    ],  # 过程内容列表 listContentProcess
)

# BUG 这个是为了凑数，防止出现遍历的时候只能遍历字符串的bug。
modelContent_BI0000 = ModelContent(
    id=2,  # 编号 id
    function_name='model_BI0000',  # 函数名称 functionName
    text_name="模型BI0000",  # 文本名称 textName
    list_process_content=[
        processContent_exBank_insolvent,
        processContent_interBank_insolvent,
        # processContent_interBank_bankrupt
    ],  # 过程内容列表 listContentProcess
)
