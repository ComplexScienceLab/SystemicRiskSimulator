

## 批处理主程序

## 主程序

##########################################
#状态/测试
####################.######################


include("include_files.jl")



## 


## 主循环
## 初始化银行变量
BB, BI, BB_tau_0, BI_tau_0, BB_tau, BI_tau = init_B_variables(; init_method = para.init_method)

## BUG运行模型BI1111
BB, BI, BB_tau, BI_tau, env = model_BI1111(BB, BI, para, env)
# using ./model_BI1111

DataFrame(Dict(n=>[getfield(x, n) for x in xs] for n in fieldnames(BB)))

















