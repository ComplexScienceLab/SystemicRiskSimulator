## 批处理主程序

## 主程序

##########################################
# #状态/开发
##########################################

## 导入相关文件及其内容
from scripts.include.includpe_exp_files import *
# from SystemicRisk.include.SystemicRiskSimulation import *
# from SystemicRisk.include.Models import *

import SystemicRisk as sr

# from SystemicRisk.core.functions.fun_state import  calc_listOfRelationInStateOfBanks



## 导入相关包
import os
import numpy as np
from enum import Enum

os.getcwd()

root_path = os.getcwd()

if __name__ == "__main__":



    ## 设定参数组合

    # list_combinationOfPara = @strdict model kappa_A_P kappa_BI

    ## 创建主文件夹用于本批次实验
    env = sr.set_experiments_folders()

    ## 建立文件以记录log
    f = open(joinpath(env[:folderpathOfExperimentsOutputData], "outputlog.txt"), "w")


    @testprintln


    "\n实验组名称：$(env[:foldernameOfExperiments])"

    ## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
    list_combinationOfPara = dict_list(setOfValuesOfParameterVariables)  # 组合排列多结构体成为列表
    env[:numExperiment] = length(list_combinationOfPara)  # 获取实验组之实验个数
    df_combinationOfPara = vcat(DataFrame.(list_combinationOfPara)...)  # 转换字典列表为数据框
    df_combinationOfPara[!, "expId"] = repeat(1: env[:numExperiment], inner = env[:numBank])  # 添加实验组id
    df_combinationOfPara[!, "id"] = collect(range(1, size(df_combinationOfPara)[1], step=1))  # 添加id
    CSV.write(datadir("$(env[:folderpathOfExperimentsOutputData])", "paras.csv"),
              list_combinationOfPara)  # 导出字段列表为csv格式


    ## 初始化参数变量
    @testprintln


    "\n列出所有实验组："
    for (idx_para, para) in enumerate(list_combinationOfPara)
        @testprintln


        "$(idx_para): $(para);"
        modelContent = eval(Meta.parse("modelContent_" * para[:modelName]))
        pass

    ## 构建本次实验组所需的所有模型
    model = buildModel(modelContent_BI1111)  # 根据基准模型BI1111预先初始化model变量
    if length(setOfValuesOfParameterVariables[:modelName]) > 1
        for modelName in setOfValuesOfParameterVariables[:modelName][2:    pass]
            modelContent = eval(Meta.parse("modelContent_$(modelName)"))
            # if True: # FIXME如果不存在模型文件，则构建模型
            model = buildModel(modelContent)
            #     pass
            pass
        pass

    println("\n实验组开始：\n")

    ## 主循环
    for (i, para) in enumerate(list_combinationOfPara)
        env[:id_experiment] = i  # 设定当前实验编号
        # 重置环境变量
        env[:indexOfSchedulePosition] = []
        env[:indexModel] = 1
        env[:indexProcess] = 1
        env[:indexStage] = 1
        env[:savedIndexProcess] = 1
        env[:savedIndexStage] = 1
        env[:loadedIndexProcess] = 1
        env[:loadedIndexStage] = 1
        env[:step] = 0
        env[:tau] = 0
        env[:savedModelName] = ""
        env[:modelName] = model.functionName
        env[:processName] = ""
        env[:savedProcessName] = ""
        env[:stageName] = ""
        env[:savedStageName] = ""
        env[:isStep] = True
        env[:isLoop] = True
        env[:isRound] = True
        env[:isStage] = True
        env[:isProcess] = True
        env[:isModel] = True
        env[:isExperiment] = True
        env[:stateOfSchedule] =:indexing
        env[:stateOfProcess] =:initializing

        ## 生成模型内容
        # modelComponent = eval(Meta.parse(para[:modelName]))

        ## 调度：生成位置索引
        if env[:stateOfSchedule] ==: indexing
        env[:indexOfSchedulePosition], env[:stateOfSchedule] = scheduler_indexing(model)
        pass


    @testprintln


    "\n实验$(env[:id_experiment])/$(length(list_combinationOfPara))开始："


    @testprintln


    "\n相关实验参数：$(para)"

    ## 进行实验
    makesim(model, para, env)


    @testprintln


    "本次实验结束，还剩下$(length(list_combinationOfPara)-env[:id_experiment])个实验。\n"
        pass  # for

    println("实验组结束。")

    close(f)
