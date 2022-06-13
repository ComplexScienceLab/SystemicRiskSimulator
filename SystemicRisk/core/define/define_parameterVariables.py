"程序：定义参数变量ParameterVariables"

## 程序：定义参数变量ParameterVariables

##########################################
#状态/使用
##########################################

from scripts.variables.set_parameterVariables import *

## 生成字典变量
setOfValuesOfParameterVariables = dict(
    modelName=modelName,
    Shock_exBI_def_t=Shock_exBI_def_t,
    Shock_exBI_run_t=Shock_exBI_run_t,
    list_Shock_exBI_t=list_Shock_exBI_t,
    kappa_A_P=kappa_A_P,
    kappa_BI=kappa_BI,
)

# para = setOfValuesOfParameterVariables # 别名

