## 批处理主程序

## 主程序

##########################################
# #状态/开发
##########################################


## 导入相关包
import os
import numpy as np
from enum import Enum
import pandas as pd


## 导入相关文件及其内容
import SystemicRisk as sr
from scripts.include.includpe_exp_files import *
# from SystemicRisk.include.SystemicRiskSimulation import *
# from SystemicRisk.include.Models import *

from SystemicRisk.core import dict_to_product_list,setOfValuesOfParameterVariables,BankState






os.getcwd()

root_path = os.getcwd()

if __name__ == "__main__":



    ## 设定参数组合

    # list_combinationOfPara = @strdict model kappa_A_P kappa_BI

    ## 创建主文件夹用于本批次实验

    env = sr.set_experiments_folders()

    ## 建立文件以记录log
    f = open(os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"),"w")


    # @testprintln "\n实验组名称：$(env['foldername_of_experiments'])"

    ## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
    list_combinationOfPara = dict_to_product_list(setOfValuesOfParameterVariables)  # 组合排列多结构体成为列表
    env['num_experiment'] = len(list_combinationOfPara)  # 获取实验组之实验个数
    df_combinationOfPara = pd.DataFrame(np.asarray(list_combinationOfPara),columns=setOfValuesOfParameterVariables.keys())  # 转换字典列表为数据框
    df_combinationOfPara.insert(loc=0,column='exp_id',value=np.repeat(list(range(1,env['num_experiment']+1)),repeats=env['num_bank'],axis=0)) # 添加实验组id
    df_combinationOfPara.insert(loc=0,column='id',value=list(range(1,len(df_combinationOfPara)+1)),axis=0) # 添加数据项id
    df_combinationOfPara.to_csv(os.path.join(env['folderpath_of_experiments_output_data'],"paras.csv"),df_combinationOfPara) # 导出字段列表为csv格式

    ## 初始化参数变量
    # @testprintln "\n列出所有实验组："
    for (idx_para, para) in enumerate(list_combinationOfPara)
        # @testprintln
        "$(idx_para): $(para);"
        modelContent = eval(Meta.parse("modelContent_" * para['model_name']))
        pass

    ## 构建本次实验组所需的所有模型
    model = buildModel(modelContent_BI1111)  # 根据基准模型BI1111预先初始化model变量
    if length(setOfValuesOfParameterVariables['model_name']) > 1
        for model_name in setOfValuesOfParameterVariables['model_name'][2:    pass]
            modelContent = eval(Meta.parse("modelContent_$(model_name)"))
            # if True: # FIXME如果不存在模型文件，则构建模型
            model = buildModel(modelContent)
            #     pass
            pass
        pass

    println("\n实验组开始：\n")

    ## 主循环
    for (i, para) in enumerate(list_combinationOfPara)
        env['id_experiment'] = i  # 设定当前实验编号
        # 重置环境变量
        env['index_of_schedule_position'] = []
        env['index_model'] = 1
        env['index_process'] = 1
        env['index_stage'] = 1
        env['saved_index_process'] = 1
        env['saved_index_stage'] = 1
        env['loadedIndexProcess'] = 1
        env['loadedIndexStage'] = 1
        env['step'] = 0
        env['tau'] = 0
        env['saved_model_name'] = ""
        env['model_name'] = model.functionName
        env['process_name'] = ""
        env['savedProcessName'] = ""
        env['stage_name'] = ""
        env['savedStageName'] = ""
        env['is_step'] = True
        env['is_loop'] = True
        env['is_round'] = True
        env['is_stage'] = True
        env['is_rocess'] = True
        env['is_model'] = True
        env['is_experiment'] = True
        env['state_of_schedule'] =StateOfSchedule.indexing
        env['state_of_process'] =:initializing

        ## 生成模型内容
        # modelComponent = eval(Meta.parse(para['model_name']))

        ## 调度：生成位置索引
        if env['state_of_schedule'] ==: indexing
        env['index_of_schedule_position'], env['state_of_schedule'] = scheduler_indexing(model)
        pass


    @testprintln


    "\n实验$(env['id_experiment'])/$(length(list_combinationOfPara))开始："


    @testprintln


    "\n相关实验参数：$(para)"

    ## 进行实验

    makesim(model, para, env)


    @testprintln


    "本次实验结束，还剩下$(length(list_combinationOfPara)-env['id_experiment'])个实验。\n"
        pass  # for

    println("实验组结束。")

    close(f)
