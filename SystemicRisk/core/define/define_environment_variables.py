"程序：定义环境变量EnvironmentVariables"

## 程序：定义环境变量EnvironmentVariables

##########################################
# 状态/使用
# 备注：改成用字典表示
##########################################


from scripts.variables.set_environmentVariables import *

## 生成字典变量 #HACK 如何实现自动生成字典变量？
env = dict(
    init_method=init_method,
    foldernameTypeOfExperiments=foldernameTypeOfExperiments,
    foldernamePrefixOfExperiments=foldernamePrefixOfExperiments,
    rootDirOfExperiments=rootDirOfExperiments,
    folderpathOfExperiments=folderpathOfExperiments,
    stepSize=stepSize,
    maxNumOfTau=maxNumOfTau,
    numBank=numBank,
    numAssets=numAssets,
    tauForTest=tauForTest,
    isTest=isTest,
    foldernameOfExperiments=foldernameOfExperiments,
    foldernameOfExperimentsOutputData=foldernameOfExperimentsOutputData,
    folderpathOfExperimentsOutputData=folderpathOfExperimentsOutputData,
    dataId=dataId,
    step=step,
    tau=tau,
    id_experiment=id_experiment,
    numExperiment=numExperiment,
    stateOfSchedule=stateOfSchedule,
    stateOfProcess=stateOfProcess,
    isStep=isStep,
    isLoop=isLoop,
    isRound=isRound,
    isStage=isStage,
    isProcess=isProcess,
    isModel=isModel,
    isExperiment=isExperiment,
    indexOfSchedulePosition=indexOfSchedulePosition,
    indexModel=indexModel,
    modelName=modelName,
    savedModelName=savedModelName,
    indexProcess=indexProcess,
    processName=processName,
    savedIndexProcess=savedIndexProcess,
    indexStage=indexStage,
    stageName=stageName,
    savedIndexStage=savedIndexStage,
)

# env = environmentVariables # 别名
