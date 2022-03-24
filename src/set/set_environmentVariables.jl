"程序：设置环境变量EnvironmentVariables"

## 程序：设置环境变量EnvironmentVariables


##########################################
#状态/开发
##########################################

## 字典之于初始化数据方式
dict_initMethods = Dict(
    [(0, "only init"), (1, "randomly"), (2, "import data"), (3, "set manually")]
)


######### 设置环境变量 #########
env.init_method = dict_initMethods[3] # 初始化数据方式
env.tau = 0 # 设置初始回合计次为0；
env.process_name = "" # 过程名称
env.is_end_round = false # 结束回合判断
env.max_num_tau = 1000 # 最大传染回合数
env.num_bank = 5 # 银行个数
env.num_assets = 3 # 资产种类数
env.test_tau = 4 # test变量，用于打断点。相关语句：env.tau>=env.test_tau







###########################



# end; # process





