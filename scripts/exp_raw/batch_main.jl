

## 批处理主程序

## 主程序

##########################################
#状态/开发
##########################################

using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目

include("../../src/include_files.jl")



## 设定参数组合

# list_combinationOfPara = @strdict model kappa_A_P kappa_BI


## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
list_combinationOfPara = dict_list(setOfValuesOfParameterVariables) # 完整名称为dict_paraValues。此处为了方便用于后续代码阅读，因此设置为p。

## 创建主文件夹用于本批次实验
env = setExperimentsFolders(env)

## 初始化参数变量
_, para = enumerate(list_combinationOfPara)

## 主循环
for (i, p) in enumerate(list_combinationOfPara)
    env[:id_experiment] = i # 设定当前实验编号
    para = copy(p)
    # 重置环境变量
    env[:step] = 0
    env[:processName] = ""
    env[:savedProcessName] = ""
    env[:stageName] = ""
    env[:savedStageName] = ""
    env[:isEndStep] = false
    env[:isEndStage] = false
    env[:isEndRound] = false
    env[:isEndProcess] = false
    env[:isEndModel] = false
    env[:isEndExperiment] = false
    env[:isLoading] = false

    @test println("实验$(env[:id_experiment])/$(length(list_combinationOfPara))开始：")
    @test println("相关实验参数：$(para)") #FIXME 这个输出是错误的
    makesim(p, env)
    @test println("本次实验结束，还剩下$(length(list_combinationOfPara)-env[:id_experiment])个实验。\n")
end # for



