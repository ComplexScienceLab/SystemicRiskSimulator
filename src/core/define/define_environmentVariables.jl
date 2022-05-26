

"程序：定义环境变量EnvironmentVariables"

## 程序：定义环境变量EnvironmentVariables

##########################################
#状态/使用
# 备注：改成用字典表示
##########################################


## 生成字典变量 #TODO 如何实现自动生成字典变量？
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
  foldernameOfExperimentsData,
  dataId,
  step,
  tau,
  id_experiment,
  numExperiment,
  stateOfSchedule,
  stateOfProcess,
  isStep,
  isLoop,
  isRound,
  isStage,
  isProcess,
  isModel,
  isExperiment,
  indexOfSchedulePosition,
  indexModel,
  modelName,
  savedModelName,
  indexProcess,
  processName,
  savedIndexProcess,
  indexStage,
  stageName,
  savedIndexStage,
)

# env = environmentVariables # 别名
