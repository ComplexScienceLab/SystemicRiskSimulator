

## 批处理主程序

## 主程序

##########################################
#状态/开发
##########################################

using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目


include("../include/include_exp_files.jl")

include("../../src/SystemicRiskSimulation.jl")

include("../../src/model/Models.jl")

# using SystemicRiskSimulation



## 设定参数组合

# list_combinationOfPara = @strdict model kappa_A_P kappa_BI


## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
list_combinationOfPara = dict_list(setOfValuesOfParameterVariables) # 完整名称为dict_paraValues。此处为了方便用于后续代码阅读，因此设置为p。

## 创建主文件夹用于本批次实验
env = setExperimentsFolders(env)
@test println("\n实验组名称：$(env[:foldernameOfExperimentsData])")

## 初始化参数变量
_, para = enumerate(list_combinationOfPara)

@test println("\n列出所有实验组：")
for (i, p) in enumerate(list_combinationOfPara)
    @test println("$(i): $(p);")
end

println("\n实验组开始：\n")

## 主循环
for (i, para) in enumerate(list_combinationOfPara)
    env[:id_experiment] = i # 设定当前实验编号
    # 重置环境变量
    env[:indexOfSchedulePosition] = []
    env[:step] = 0
    env[:tau] = 0
    env[:savedModelName] = ""
    env[:modelName] = ""
    env[:processName] = ""
    env[:savedProcessName] = ""
    env[:stageName] = ""
    env[:savedStageName] = ""
    env[:isStep] = true
    env[:isLoop] = true
    env[:isRound] = true
    env[:isStage] = true
    env[:isProcess] = true
    env[:isModel] = true
    env[:isExperiment] = true
    env[:stateOfSchedule] = :standing
    env[:stateOfSchedule] = :standing

    @test println("\n实验$(env[:id_experiment])/$(length(list_combinationOfPara))开始：")
    @test println("\n相关实验参数：$(para)")

    ## 调度：生成位置索引
    env[:indexOfSchedulePosition], env[:stateOfSchedule] = scheduler_indexing(para[:modelName], env[:stateOfSchedule])
    
    ## 进行实验
    makesim(para, env)

    @test println("本次实验结束，还剩下$(length(list_combinationOfPara)-env[:id_experiment])个实验。\n")
end # for

println("实验组结束。")


