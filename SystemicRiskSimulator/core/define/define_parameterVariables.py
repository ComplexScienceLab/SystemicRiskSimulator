"程序：定义参数变量parameter_variables"

from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

pass  # end import

## 生成字典变量
if sgv['init_parameters_method'] == "set manually":
    from SystemicRiskSimulator.data.parameters.set_parameters_variables import set_parameters_variables
    para = set_parameters_variables  # 别名
else:
    para = None
