"定义类型"

## 定义类型，模式3-1


from PySystemicRiskLab import np, Union, Any, Optional

pass  # end import

## 定义类型别名
IdsType = np.dtype([('id', np.int16)])  # 向量编号类型
AbbrType = np.dtype([('abbr', np.str_)])  # 向量缩写类型
NameType = np.dtype([('name', np.str_)])  # 向量名称类型
MoneyType = np.dtype([('money', np.float_)])  # 向量资金类型
StateType = np.dtype([('state', np.bool_)])  # 一维向量状态类型
ListType = np.dtype([('list', list)])  # 一维向量状态类型
ItemIdType = np.array(np.dtype(np.int8))
ItemFunctionNameType = np.array(np.dtype(np.str_))
ItemTextNameType = np.array(np.dtype(np.str_))
ContentComponentType = Union[str, list, dict, None]
# AttributeComponentType = np.dtype({'names': ['id', 'entity_name', 'text_name', 'content_type'], 'formats': ['i4', 'U', 'U', 'U']})
# AttributeComponentType = Union[np.dtype({'names': ['id', 'entity_name', 'text_name', 'content_type'], 'formats': ['i4', 'U', 'U', 'U']}),dict, str, None]
AttributeComponentType = Union[dict, str, None]
NodeComponentType = Union[str, list, dict, None]  # HACK 可能需要修改
ConditionComponentType = Union[str, list, None]  # HACK 可能需要修改
ArrowComponentType = Union[str, list, None]
ContainerComponentType = Union[list, dict, str, None]
# ProcessComponentType = np.dtype({'names': ['flow', 'condition'], 'formats': [np.void, 'U']})
ProcessComponentType = Union[dict, str, None]
ExecuteComponentType = Union[str, list, None]
EnvironmentVariableType = Union[dict, Any]  # 环境变量类型 #HACK暂时没用到，目前用的是dict。
ParameterVariableType = Union[dict, Any]  # 参数变量类型 #HACK暂时没用到，目前用的是dict。
