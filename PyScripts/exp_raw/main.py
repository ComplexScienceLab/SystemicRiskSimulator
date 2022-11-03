## 批处理主程序

## 主程序

##########################################
# #状态/开发
##########################################
## 导入相关包

## 以下部分只能被启用于：当没有在项目根路径设置`.env`文件之PYTHONPATH环境时。
# import sys,os
# os.getcwd()
# root_path = os.getcwd()
# sys.path.append(os.path.join(root_path))
####

from PySystemicRiskLab import os, np, pd, logging

## 导入相关文件及其内容
from PySystemicRiskLab.core.controller.fun_agentModel import AgentsModel
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum, StateOfProcessEnum
from PySystemicRiskLab.core.model.fun_model_skeleton import ModelSkeleton
from PySystemicRiskLab.core.model.fun_process_skeleton import ProcessSkeleton
from PySystemicRiskLab.tools.fun_tools import Tools
from PySystemicRiskLab.core.define.define_parameterVariables import para
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

    ## 创建主文件夹用于本批次实验

    env['folderpath_project'] = Tools().get_project_rootpath()
    env = Tools().set_experiments_folders()

    ## 设置日志
    logging.basicConfig(
        level=10,
        filename=os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"),  # 建立文件以记录log
    )

    logging.debug("\n实验组名称：%s", env['foldername_of_experiments'])

    ## 设置字典列表，由setOfParametersValues各参数之各可能的取值排列组合而成。此将用于做实验

    env['list_combinationOfPara'] = Tools().dict_to_product_list(para)  # 组合排列多结构体成为列表

    ModelCollector.exportParameterData(list_combinationOfPara=env['list_combinationOfPara'])  # 导出控制参数数据

    ## 初始化参数变量
    # @testprintln "\n列出所有实验组："
    for (i, model_name) in enumerate(para['model_name']):
        modelContent = eval("modelContent_" + model_name)
        pass

    ## 构建本次实验组所需的所有模型
    models = {}  # 构建模型列表集合
    ## 获取list的集合，按原始顺序排列
    for (i, model_name) in enumerate(para['model_name']):
        modelContent = eval("modelContent_" + model_name)
        model = ModelBuilder.buildModel(modelContent)
        models[model_name] = model
        pass

    logging.debug("实验组开始：\n\n")

    ## 主循环
    for (i, para) in enumerate(env['list_combinationOfPara']):
        model = models[para['model_name']]  # 获取当前实验对应的模型
        env['id_experiment'] = i + 1  # 设定当前实验编号
        # 重置环境变量
        env['index_of_schedule_position'] = []
        env['index_model'] = 1
        env['index_process'] = 1
        env['index_stage'] = 1
        env['saved_index_process'] = 1
        env['saved_index_stage'] = 1
        env['loaded_index_process'] = 1
        env['loaded_index_stage'] = 1
        env['step'] = 0
        env['tau'] = 0
        env['saved_model_name'] = ""
        env['model_name'] = model.functionName
        env['process_name'] = ""
        env['stage_name'] = ""
        env['is_step'] = True
        env['is_loop'] = True
        env['is_round'] = True
        env['is_stage'] = True
        env['is_process'] = True
        env['is_model'] = True
        env['is_experiment'] = True
        env['state_of_schedule'] = StateOfScheduleEnum.indexing
        env['state_of_process'] = StateOfProcessEnum.initializing

        ## 调度：生成位置索引
        if env['state_of_schedule'] == StateOfScheduleEnum.indexing:
            env['index_of_schedule_position'], env['state_of_schedule'] = ModelScheduler.scheduler_indexing(model)
            pass

        logging.info("实验" + str(env['id_experiment']) + "/" + str(len(env['list_combinationOfPara'])) + "开始：\n")

        logging.info("相关实验参数：" + str(para) + "\n")

        ## 进行实验

        AgentsModel.makesim(model, para, env)

        logging.info("本次实验结束，还剩下" + str(len(env['list_combinationOfPara']) - env['id_experiment']) + "个实验。\n\n")
        pass  # for

    logging.info("实验组结束。")

    ## 默认程序打开输出文件查看
    os.system(r"open " + os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"))

    pass  # main
