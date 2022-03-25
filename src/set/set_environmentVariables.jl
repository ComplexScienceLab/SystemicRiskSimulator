"程序：设置环境变量EnvironmentVariables"

## 程序：设置环境变量EnvironmentVariables


##########################################
#状态/开发
##########################################



######### 设置环境变量 #########
env.init_method = "set manually" # 初始化数据方式
env.filenameTypeOfExperiments = "datetime" # 设置实验文件夹命名方式
env.tau = 0 # 设置初始回合计次为0；
env.process_name = "" # 过程名称
env.is_end_round = false # 结束回合判断
env.max_num_tau = 1000 # 最大传染回合数
env.num_bank = 5 # 银行个数
env.num_assets = 3 # 资产种类数
env.test_tau = 4 # test变量，用于打断点。相关语句：env.tau>=env.test_tau







###########################



# end; # process





