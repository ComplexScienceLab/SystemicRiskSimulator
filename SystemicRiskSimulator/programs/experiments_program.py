# -*- coding: utf-8 -*-
import time

from SystemicRiskSimulator.external_packages import warnings, logging, platform, os, Path
from SystemicRiskSimulator.core.operations.operator import Operator


def experiments_program(sgv: dict, para: dict):
    """
    实验组模拟程序。用于运行实验组。

    Args:
        sgv (dict): 模拟器全局变量
        para (dict): 参数字典

    Returns:

    """

    # %% 预安装模型、数据，运行实验组

    if sgv['is_ignore_warning']:
        warnings.filterwarnings("ignore")  # 忽略警告

    ## 初始化、构建、安装模型
    sgv, models = Operator.operate_installing(sgv, para)
    ## 运行实验组
    logging.debug("\n\n\n实验组开始：\n\n")

    sgv['experiments_running_time'] = 0  # 初始化实验组运行总时长
    sgv['export_data_running_time'] = 0  # 初始化导出数据运行总时长

    sgv['simulator_start_time'] = time.time()  # 记录模拟器开始运行时刻

    for (i, para) in enumerate(sgv['list_combination_of_para']):
        model = models[f"model_{para['model_name']}"]  # 获取当前实验对应的模型
        sgv['id_experiment'] = i + 1  # 设定当前实验编号

        if (sgv['list_idsExperiment_to_run'] is None) or (sgv['id_experiment'] in sgv['list_idsExperiment_to_run']):
            ## 进行实验
            if sgv['is_use_PettingZoo_environments']:
                ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型 #DEBUG 正在测试中
                A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para)
                A, A_data, sgv, para = Operator.operate_step_experiment(A, A_data, sgv, para, model)
                # A, A_data, sgv, para, model = Operator.operate_step_experiment(sgv, para, model)
                Operator.operate_end_experiment(A_data, sgv)
            else:
                ## NOTE 如果使用模拟器自带的模型，不使用由强化学习环境工具包自定义的模型 #DEBUG 还没测试过
                Operator.operate_run_experiment(sgv, para, model)
                pass  # if

        pass  # for

    sgv['simulator_end_time'] = time.time()  # 记录模拟器结束运行时刻
    sgv['simulator_running_time'] = sgv['simulator_end_time'] - sgv['simulator_start_time']  # 记录模拟器运行时长

    logging.info(f"实验组结束。\n实验组运行总时长：{sgv['experiments_running_time']} 秒。\n导出数据运行总时长：{sgv['export_data_running_time']} 秒。\n模拟器运行总时长：{sgv['simulator_running_time']}秒。")

    # sgv['experiments_end_time'] = 0  # 记录实验组结束运行时刻
    # sgv['experiments_running_time'] = sgv['experiments_end_time'] - sgv['experiments_start_time']  # 记录实验组运行时长
    # logging.info(f"实验组运行总的时长：{sgv['experiments_running_time']}秒。")

    ## 默认程序打开输出文件查看
    if sgv['is_auto_open_outputlog']:
        system = platform.system()
        if system == 'Darwin':
            os.system(r"open " + str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))
        elif system == 'Windows':
            os.startfile(str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))
        elif system == 'Linux':
            os.system('xdg-open ' + str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))  #DEBUG 还没测试过
        else:
            print("Unsupported operating system")
            pass  # if
        pass  # if

    if sgv['is_ignore_warning']:
        warnings.filterwarnings("default")  # 恢复警告

    pass  # function
