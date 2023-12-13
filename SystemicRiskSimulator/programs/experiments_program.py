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
    warnings.filterwarnings("ignore")
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

        ## 进行实验
        Operator.operate_experiment(sgv, para, model)

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
            os.system(r"open " + str(Path(sgv['folderpath_experiments_output_data'], r"outputlog.txt")))
        elif system == 'Windows':
            os.startfile(str(Path(sgv['folderpath_experiments_output_data'], r"outputlog.txt")))
        elif system == 'Linux':
            os.system('xdg-open ' + str(Path(sgv['folderpath_experiments_output_data'], r"outputlog.txt")))
        else:
            print("Unsupported operating system")
            pass  # if
        pass  # if

    pass  # function
