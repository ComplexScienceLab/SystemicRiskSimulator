

## 批处理主程序

## 主程序

##########################################
#状态/开发
####################.######################

using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目

include("../../src/include_files.jl")



## 设定参数组合

# list_combinationOfPara = @strdict model kappa_A_P kappa_BI


## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
list_combinationOfPara = dict_list(setOfValuesOfParameterVariables) # 完整名称为dict_paraValues。此处为了方便用于后续代码阅读，因此设置为p。

## 创建主文件夹用于本批次实验
env = setExperimentsFolders(env)

## 初始化银行变量

# global BB, global BI, global BB_tau_0, global BI_tau_0, global BB_tau, global BI_tau = init_B_variables(; init_method = env[:init_method])
init_systemicRiskAgent!()
## 主循环
for (i, para) in enumerate(list_combinationOfPara)
    # makesim(BB, BI, para, env)
    makesim(agent, para, env)
end # for
## BUG运行模型BI1111
# BB, BI, BB_tau, BI_tau, env = model_BI1111(BB, BI, para, env)
# using ./model_BI1111


