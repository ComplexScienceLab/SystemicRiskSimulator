

"程序：定义环境变量EnvironmentVariables"

## 程序：定义环境变量EnvironmentVariables

##########################################
#状态/使用
# 备注：改成用字典表示
##########################################


## 生成字典变量
env = @dict(
  init_method,
  foldernameTypeOfExperimentsData,
  foldernamePrefixOfExperimentsData,
  rootDirOfExperimentsData,
  folderpathOfExperimentsData,
  stepSize,
  maxNumOfTau,
  numBank,
  numAssets,
  tauForTest,
  isTest,
  step,
  tau,
  stageName,
  savedStageName,
  processName,
  savedProcessName,
  id_experiment,
  stateOfProcessStep,
  stateOfStageStep,
  isStep,
  isRound,
  isStage,
  isProcess,
  isModel,
  isExperiment,
)

# env = environmentVariables # 别名
