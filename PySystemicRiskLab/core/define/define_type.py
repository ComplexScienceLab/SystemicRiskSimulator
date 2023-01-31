"定义类型"

## 定义类型，模式3-1


from PySystemicRiskLab import np, Union, Any, Optional

pass  # end import

## 定义类型别名
IdsType = np.dtype([('id', np.int16)])  # 向量编号类型
AbbrType = np.dtype([('abbr', np.str)])  # 向量缩写类型
NameType = np.dtype([('name', np.str)])  # 向量名称类型
MoneyType = np.dtype([('money', np.float_)])  # 向量资金类型
StateType = np.dtype([('state', np.bool_)])  # 一维向量状态类型
ListType = np.dtype([('list', list)])  # 一维向量状态类型
ItemIdType = np.array(np.dtype(np.int8))
ItemFunctionNameType = np.array(np.dtype(np.str))
ItemTextNameType = np.array(np.dtype(np.str))
ContentComponentType = Union[str, list, Any]
AttributeComponentType = np.dtype({'names': ['id', 'entity_name', 'text_name', 'content_type'], 'formats': ['i4', 'U', 'U', 'U']})
NodeComponentType = Union[str, list, Any]  # HACK 可能需要修改
ArrowComponentType = Union[str, list, Any]
ContainerComponentType = Union[list, dict, str, Any]
ProcessComponentType = np.dtype({'names': ['flow', 'condition'], 'formats': [np.void, 'U']})
ExecuteComponentType = Union[str, list, Any]
EnvironmentVariableType = Union[dict, Any]  # 环境变量类型 #HACK暂时没用到，目前用的是dict。
ParameterVariableType = Union[dict, Any]  # 参数变量类型 #HACK暂时没用到，目前用的是dict。
