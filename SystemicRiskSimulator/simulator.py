"""
系统性风险模拟器入口
"""


def simulator(config: dict):
    """
    系统性风险模拟器入口

    Args:
        config (dict): 配置项

    Returns:
        None

    """

    global sgv, para

    # %% 首先导入相关包
    from SystemicRiskSimulator import os, platform, logging, warnings, Path
    from SystemicRiskSimulator.tools.tools import Tools

    # %% 初始化
    ## 获取项目路径、模拟器工具路径
    config['folderpath_simulator'] = Tools.get_project_rootpath(config['foldername_simulator'], config['folderpath_realpath_simulator'])
    config['folderpath_project'] = Tools.get_project_rootpath()
    # 如果 settings 之 config 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
    Tools._delete_and_recreate_folder(Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=False)
    Tools._copy_files_from_other_folders(Path(config['folderpath_project'], config['folderpath_config']), Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=False)
    from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

    ## 生成实验相关的文件夹用于本批次实验
    (
        sgv['foldername_experiments'],
        sgv['folderpath_project'],
        sgv['folderpath_simulator'],
        sgv['folderpath_experiments'],
        sgv['folderpath_experiments_output_data'],
        sgv['folderpath_models'],
        sgv['folderpath_config'],
        sgv['folderpath_parameters'],
        sgv['folderpath_agents'],
    ) = Tools.set_experiments_folders(
        foldername_prefix_experiments=sgv['foldername_prefix_experiments'],
        foldername_experiments_output_data=sgv['foldername_experiments_output_data'],
        str_folderpath_root_experiments=sgv['folderpath_root_experiments'],
        str_foldername_simulator=config['foldername_simulator'],
        str_folderpath_realpath_simulator=config['folderpath_realpath_simulator'],
        str_folderpath_models=sgv['folderpath_models'],
        str_folderpath_config=sgv['folderpath_config'],
        str_folderpath_parameters=sgv['folderpath_parameters'],
        str_folderpath_agents=sgv['folderpath_agents'],
        type_of_experiments_foldername=sgv['type_of_experiments_foldername'],
        is_datetime=True,
    )

    Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/parameters"), is_auto_confirmation=sgv['is_auto_confirmation'])
    Tools._copy_files_from_other_folders(sgv['folderpath_parameters'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/parameters"), is_auto_confirmation=sgv['is_auto_confirmation'])
    from SystemicRiskSimulator.core.define.define_parameterVariables import para

    Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])
    Tools._copy_files_from_other_folders(sgv['folderpath_agents'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])
    # from SystemicRiskSimulator.core.define.define_agentsVariables import dict_bankCommercial, dict_bankInterbank

    from SystemicRiskSimulator.core.operations.operator import Operator

    ## 设置日志
    logger = logging.getLogger()
    logger.setLevel(sgv['test_logging'])
    log_file_handler = logging.FileHandler(Path(sgv['folderpath_experiments_output_data'], "outputlog.txt"))
    logger.addHandler(log_file_handler)
    log_console_handler = logging.StreamHandler()
    logger.addHandler(log_console_handler)
    logging.debug("\n实验组名称：%s", sgv['foldername_experiments'])

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

    # %% 清理
    ## 删除设置文件夹、模型文件夹内的所有文件，但是保留文件夹
    Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=sgv['is_auto_confirmation'])
    Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/parameters"), is_auto_confirmation=sgv['is_auto_confirmation'])
    Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])
    Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/models"), is_auto_confirmation=sgv['is_auto_confirmation'])

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
