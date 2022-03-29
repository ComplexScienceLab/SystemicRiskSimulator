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
- processName::String: 过程名称
- isEndRound::Bool: 结束回合判断
- numBank::Int16: 银行个数
- numAssets::Int16: 资产总类数
- maxNumOfTau::Int16: 最大传染回合数
- tauForTest::Int16: test变量，用于打断点
"""

##########################################
#状态/可扩展
# 开发说明：[相关的修改项](file:///../define/define_environmentVariables.jl)
##########################################


######### 设置环境变量 #########################################

init_method = "set manually"; # 初始化数据方式；
foldernameTypeOfExperimentsData = "set manually"; # 设置实验数据文件夹命名方式。默认"default"；
foldernamePrefixOfExperimentsData = "test"; # 手动设置实验数据文件夹前缀名。默认"default"；
rootDirOfExperimentsData = projectdir() * "/data/sims/"; # 手动设置实验数据文件夹根路径。默认projectdir( * "/data/sims/"；
folderpathOfExperimentsData = ""; # 主文件夹路径之于实验。将由函数生成；


maxNumOfTau = 100; # 单个过程最大回合数；
numBank = 5; # 银行个数；
numAssets = 3; # 资产种类数；

tauForTest = 4 # test变量，用于打断点。相关语句：env[:tau]>=env[:tauForTest]；
isTest = true # 是否处于测试状态

###########################


######### 初始化环境变量（不要改动！） #########################################

step = 0; # 设置当前步伐值为0。不要改动
tau = 0; # 设置初始回合计次为0；
stageName = ""; # 设置当前阶段名称；
processName = ""; # 过程名称；
id_experiment = 1; # 设置当前实验组编号；

isEndStep = false; # 结束步进判断；
isEndStage = false; # 结束阶段判断；
isEndRound = false; # 结束回合判断；
isEndProcess = false; # 结束过程判断；
isEndModel = false; # 结束模型判断；



###########################



# end; # process





