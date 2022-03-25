

## 批处理主程序

## 主程序

##########################################
#状态/测试
####################.######################

using DataFrames
using DrWatson

include("../../src/include_files.jl")



## 设定参数组合

# list_combinationOfPara = @strdict model kappa_A_P kappa_BI


## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
list_combinationOfPara = dict_list(setOfParametersValues) # 完整名称为dict_paraValues。此处为了方便用于后续代码阅读，因此设置为p。

## 设置实验子文件夹，命名如下
if env.filenameTypeOf
    
end


## 主循环
## 初始化银行变量
BB, BI, BB_tau_0, BI_tau_0, BB_tau, BI_tau = init_B_variables(; init_method = env.init_method)

# global BB, global BI, global BB_tau_0, global BI_tau_0, global BB_tau, global BI_tau = init_B_variables(; init_method = env.init_method)
for (i, para) in enumerate(list_combinationOfPara)
    # makesim(BB, BI, para, env)
    makesim(BB, BI, para, env)
end # for
## BUG运行模型BI1111
# BB, BI, BB_tau, BI_tau, env = model_BI1111(BB, BI, para, env)
# using ./model_BI1111


