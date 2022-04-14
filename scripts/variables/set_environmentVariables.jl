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
- maxNumOfTau::Int16: 最大回合数
- tauForTest::Int16: test变量，用于打断点
"""

##########################################
#状态/可扩展
# 开发说明：[相关的修改项](file:///../../src/core/define/define_environmentVariables.jl)
##########################################


######### 设置环境变量 #########################################

init_method = "set manually"; # 初始化数据方式；
foldernameTypeOfExperimentsData = "set manually"; # 设置实验数据文件夹命名方式。默认"default"；
foldernamePrefixOfExperimentsData = "test"; # 手动设置实验数据文件夹前缀名。默认"default"；
rootDirOfExperimentsData = projectdir() * "/data/sims/"; # 手动设置实验数据文件夹根路径。默认projectdir( * "/data/sims/"；
folderpathOfExperimentsData = ""; # 主文件夹路径之于实验。将由函数生成；



stepSize = 1; # 设置步进跨度；如果该数值设置较大，则相当于直接运行程序；
maxNumOfTau = 100; # 单个过程最大回合数；
numBank = 5; # 银行个数；
numAssets = 3; # 资产种类数；



tauForTest = 4 # test变量，用于打断点。相关语句：env[:tau]>=env[:tauForTest]；
isTest = true # 是否处于测试状态



###########################


######### 初始化环境变量（不要改动！） #########################################

foldernameOfExperimentsData = ""; # 实验数据文件夹名称

step = 0; # 当前步伐值为0。不要改动
tau = 0; # 初始回合计次为0；
id_experiment = 1; # 当前实验组编号；

stateOfSchedule = :idle; # 调度运作状态。状态符有以下几种：`:idle`：闲置状态、`:indexing`：索引状态、`:stepping`：步进状态、`:saving`：存储状态、`:loading`：读取状态、`:collecting`：收集数据状态、`:running`：运行状态；

isStep = true; # 是否处于步进状态；
isLoop = true; # 是否处于循环状态
isRound = true; # 是否处于回合状态；
isStage = true; # 是否处于阶段状态；
isProcess = true; # 是否处于过程状态；
isModel = true; # 是否处于模型状态；
isExperiment = true; # 是否处于当前状态的一次实验；

indexModel = 0; # 索引状态下，标记当前所在模型之位置; 
# modelName = ""; # 运行的模型之名称; 
# savedModelName = ""; # 存储的模型之名称; 
indexOfSchedulePosition = []; # 调度位置索引；
indexProcess = 0; # 索引状态下，标记当前所在过程之位置
processName = ""; # 运行的过程之名称；
savedIndexProcess = ""; # 存储的过程之位置；
loadedIndexProcess = ""; # 读取的过程之位置；
indexStage = 0; # 索引状态下，标记当前所在阶段之位置
stageName = ""; # 运行的阶段之名称；
savedIndexStage = ""; # 存储的当前阶段之位置；
loadedIndexStage = ""; # 读取的当前阶段之位置；



###########################








