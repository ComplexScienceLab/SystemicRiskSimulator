# -*- coding: utf-8 -*-


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
    for (i, para) in enumerate(sgv['list_combination_of_para']):
        model = models[f"model_{para['model_name']}"]  # 获取当前实验对应的模型
        sgv['id_experiment'] = i + 1  # 设定当前实验编号

        ## 进行实验
        Operator.operate_experiment(sgv, para, model)

        pass  # for
    logging.info("实验组结束。")

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
