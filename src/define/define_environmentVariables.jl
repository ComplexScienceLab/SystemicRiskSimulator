

"程序：定义环境变量EnvironmentVariables"

## 程序：定义环境变量EnvironmentVariables

##########################################
#状态/开发
##########################################

"环境变量EnvironmentVariables"
mutable struct EnvironmentVariables
    tau::Int16 # 回合计数
    process_name::String # 过程名称
    is_end_round::Bool # 结束回合判断
    num_bank::Int16 # 银行个数
    num_assets::Int16 # 资产总类数
    max_num_tau::Int16 # 最大传染回合数
    test_tau::Int16 # test变量，用于打断点
end


## 初始化
env = EnvironmentVariables(
    0, # 回合计数
    "", # 过程名称
    false, # 结束回合判断
    0, # 银行个数
    0, # 资产总类数
    1, # 最大传染回合数
    1 # test变量，用于打断点
)