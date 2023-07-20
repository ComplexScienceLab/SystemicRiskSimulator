"程序：定义模型及其相关的结构体"

from PySystemicRiskLab.core.define.define_type import *

pass  # end import


class Module:  # TODO 无用，其术语【模块】已经发生变动，不再适用现在的定义。
    """
    定义模块
    """
    id: ItemIdType  # 编号 id
    functionName: ItemFunctionNameType  # 函数名称 name
    textName: ItemTextNameType  # 文本名称 name
    contentType: str  # 内容之类型
    content: ContentComponentType  # 内容
    execute: None  # 执行

    def __init__(self, id, function_name, text_name, content_type, content, execute):
        self.id = id
        self.functionName = function_name
        self.textName = text_name
        self.contentType = content_type
        self.content = content
        self.execute = execute
        pass

    pass  # class
