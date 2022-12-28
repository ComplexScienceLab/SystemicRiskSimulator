"定义类型"

## 定义类型，模式3-1


from PySystemicRiskLab import np, Union, Any

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
ContentAspectType = Union[str, list, Any]
AttributeAspectType = np.dtype({'names': ['id', 'entity_name', 'text_name', 'content_type'], 'formats': ['i4', 'U', 'U', 'U']})
NodeAspectType = Any
ContainerAspectType = np.dtype(list)
ProcessAspectType = np.dtype({'names': ['flow', 'condition'], 'formats': [np.void, 'U']})
EnvironmentVariableType = Union[dict, Any]  # 环境变量类型 #HACK暂时没用到，目前用的是dict。
ParameterVariableType = Union[dict, Any]  # 参数变量类型 #HACK暂时没用到，目前用的是dict。
