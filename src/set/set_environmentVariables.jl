"""
程序：设置环境变量EnvironmentVariables
# Items: 
- init_method::String: 
  - "default": 默认，仅初始化；
  - "randomly": 随机生成；
  - "import data": 导入外部数据；
  - "set manually": 手动设置；
- foldernameTypeOfExperimentsData::String: 设置实验数据文件夹命名方式。默认"default"；
  - default: 默认，固定命名方式
  - set manually: 手动设置名称
- foldernamePrefixOfExperimentsData::String: 手动设置实验数据文件夹前缀名。默认"default"；
- rootDirOfExperimentsData::String: 手动设置实验数据文件夹根路径。默认projectdir() * "/data/sims/"；
- tau::Int16: 回合计数
- process_name::String: 过程名称
- is_end_round::Bool: 结束回合判断
- num_bank::Int16: 银行个数
- num_assets::Int16: 资产总类数
- max_num_tau::Int16: 最大传染回合数
- test_tau::Int16: test变量，用于打断点
"""

##########################################
#状态/可扩展
##########################################


init_method = "set manually"; # 初始化数据方式；
foldernameTypeOfExperimentsData = "set manually"; # 设置实验数据文件夹命名方式。默认"default"；
foldernamePrefixOfExperimentsData = "test"; # 手动设置实验数据文件夹前缀名。默认"default"；
rootDirOfExperimentsData = projectdir() * "/data/sims/"; # 手动设置实验数据文件夹根路径。默认projectdir( * "/data/sims/"；
folderpathOfExperimentsData = ""; # 主文件夹路径之于实验。将由函数生成；
tau = 0; # 设置初始回合计次为0；
process_name = ""; # 过程名称；
is_end_round = false; # 结束回合判断；
max_num_tau = 1000; # 最大回合数；
num_bank = 5; # 银行个数；
num_assets = 3; # 资产种类数；
test_tau = 4 # test变量，用于打断点。相关语句：env[:tau]>=env[:test_tau]；


###########################



# end; # process





