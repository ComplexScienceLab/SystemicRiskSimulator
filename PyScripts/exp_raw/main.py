## 批处理主程序

## 主程序

##########################################
# #状态/开发
##########################################
## 导入相关包

# import os
# import numpy as np
# import pandas as pd
from PySystemicRiskLab import *

## 导入相关文件及其内容
from PySystemicRiskLab.core.controller.fun_agentModel import AgentsModel
from PySystemicRiskLab.core.model.fun_model_skeleton import fun_model_skeleton
from PySystemicRiskLab.tools.fun_tools import Tools
from PySystemicRiskLab.core.define.define_parameterVariables import paras
from PySystemicRiskLab.core.define.define_environment_variables import env
from PyScripts.settings.set_environmentVariables import *
from PySystemicRiskLab.core.controller.model_runner import ModelRunner
from PySystemicRiskLab.core.controller.fun_scheduler import ModelScheduler
from PySystemicRiskLab.core.controller.model_builder import ModelBuilder
from PySystemicRiskLab.model.models.model_content import *  # 导入所有模型
from PySystemicRiskLab.core.controller.model_collector import ModelCollector

# end import

os.getcwd()

root_path = os.getcwd()


if __name__ == "__main__":



    ## 设定参数组合

    # list_combinationOfPara = @strdict models kappa_A_P kappa_BI

    ## 创建主文件夹用于本批次实验

    env['folderpath_project'] = Tools().get_project_rootpath()
    env = Tools().set_experiments_folders()

    ## 建立文件以记录log
    f = open(os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"), "w")

    # @testprintln "\n实验组名称：$(env['foldername_of_experiments'])"

    ## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验
    list_combinationOfPara = Tools().dict_to_product_list(paras)  # 组合排列多结构体成为列表
    # env['num_experiment'] = len(list_combinationOfPara)  # 获取实验组之实验个数
    # df_010 = pd.DataFrame(list_combinationOfPara, columns=paras.keys())  # 转换字典列表为数据框
    # li_010 = [df_010.apply(lambda x: pd.Series(x[i]), axis=1).stack().reset_index(level=1, drop=True) for i in range(df_010.columns.__len__())]
    # li_020 = [np.array(li_010[i]).repeat(repeats=env['num_bank']) for i in range(li_010.__len__())]
    # df_combinationOfPara = pd.DataFrame(li_020).T
    # df_combinationOfPara.columns=paras.keys()
    # df_combinationOfPara.insert(loc=0, column='exp_id', value=np.repeat(list(range(1, env['num_experiment'] + 1)), repeats=env['num_bank'], axis=0))  # 添加实验组id
    # df_combinationOfPara.insert(loc=0, column='id', value=list(range(1, len(df_combinationOfPara) + 1)), axis=0)  # 添加数据项id
    # df_combinationOfPara.to_csv(os.path.join(env['folderpath_of_experiments_output_data'], "paras.csv"), df_combinationOfPara)  # 导出字段列表为csv格式

    ModelCollector.exportParameterData(list_combinationOfPara=list_combinationOfPara)  # 导出控制参数数据

    ## 初始化参数变量
    # @testprintln "\n列出所有实验组："
    for (i, model_name) in enumerate(paras['model_name']):
        # @testprintln "$(i): $(model_name);"
        modelContent = eval("modelContent_" + model_name)
        pass

    ## 构建本次实验组所需的所有模型
    # model_builder = ModelBuilder()
    models = {}  # 构建模型列表集合
    # models.append(model_builder.buildModel(modelContent_BI1111))  # 根据基准模型BI1111预先初始化model变量
    # models = model_builder.buildModel(ModelBuilder,modelContent_BI1111)  # 根据基准模型BI1111预先初始化model变量
    # if len(model_name['model_name']) > 1:
    ## 获取list的集合，按原始顺序排列
    # setOfModel=list(set(list_combinationOfPara['model_name']))
    for (i, model_name) in enumerate(paras['model_name']):
        modelContent = eval("modelContent_" + model_name)
        model = ModelBuilder.buildModel(modelContent)
        models[model_name] = model
        pass

    print("\n实验组开始：\n")

    ## 主循环
    for (i, para) in enumerate(list_combinationOfPara):
        model = models[para['model_name']]  # 获取当前实验对应的模型
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
        env['state_of_schedule'] = StateOfScheduleEnum.indexing
        env['state_of_process'] = StateOfScheduleEnum.idle

        ## 生成模型内容
        # modelComponent = eval(Meta.parse(paras['model_name']))

        ## 调度：生成位置索引
        if env['state_of_schedule'] == StateOfScheduleEnum.indexing:
            env['index_of_schedule_position'], env['state_of_schedule'] = ModelScheduler.scheduler_indexing(model)
            pass

        # @testprintln    "\n实验$(env['id_experiment'])/$(length(list_combinationOfPara))开始："

        # @testprintln    "\n相关实验参数：$(paras)"

        ## 进行实验

        AgentsModel.makesim(model, para, env)

        # @testprintln    "本次实验结束，还剩下$(length(list_combinationOfPara)-env['id_experiment'])个实验。\n"
        pass  # for

    print("实验组结束。")

    f.close()
    pass  # main
