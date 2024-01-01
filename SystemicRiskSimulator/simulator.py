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
    from SystemicRiskSimulator.external_packages import os, platform, logging, warnings, Path, shutil
    from SystemicRiskSimulator.tools.tools import Tools

    # %% 初始化
    ## 获取项目路径、模拟器工具路径
    config['folderpath_project'] = Tools.get_project_rootpath()
    config['folderpath_simulator'] = Tools.get_project_rootpath(config['foldername_simulator'], config['folderpath_realpath_simulator'])
    # 如果 settings 之 config 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
    Tools._delete_and_recreate_folder(Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=config['is_auto_confirmation'])
    Tools._copy_files_from_other_folders(Path(config['folderpath_project'], config['folderpath_config']), Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=config['is_auto_confirmation'])
    from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

    ## 设置相关的实验文件夹名称
    if sgv['schedule_operation']['实验组模拟程序'] is True:
        sgv['foldername_experiments'] = Tools.set_foldername_experiments(sgv['foldername_prefix_experiments'], sgv['foldername_set_manually'], sgv['is_datetime'], sgv['type_of_experiments_foldername'])
        pass  # if

    ## 生成实验相关的文件夹用于本批次运作
    (
        sgv['folderpath_project'],
        sgv['folderpath_simulator'],
        sgv['folderpath_experiments'],
        sgv['folderpath_experiments_output_data'],
        sgv['folderpath_experiments_output_log'],
        sgv['folderpath_experiments_output_config'],
        sgv['folderpath_experiments_output_parameters'],
        sgv['folderpath_experiments_output_agents'],
        sgv['folderpath_experiments_output_models'],
        sgv['folderpath_models'],
        sgv['folderpath_config'],
        sgv['folderpath_parameters'],
        sgv['folderpath_agents'],
    ) = Tools.set_experiments_folders(
        foldername_experiments_output_data=sgv['foldername_experiments_output_data'],
        foldername_experiments=sgv['foldername_experiments'],
        str_folderpath_root_experiments=sgv['folderpath_root_experiments'],
        str_foldername_simulator=config['foldername_simulator'],
        str_folderpath_realpath_simulator=config['folderpath_realpath_simulator'],
        str_foldername_outputData=sgv['foldername_outputData'],
        str_folderpath_realpath_outputData=sgv['folderpath_realpath_outputData'],
        str_folderpath_models=sgv['folderpath_models'],
        str_folderpath_config=sgv['folderpath_config'],
        str_folderpath_parameters=sgv['folderpath_parameters'],
        str_folderpath_agents=sgv['folderpath_agents'],
    )

    # from SystemicRiskSimulator.core.operations.operator import Operator

    # %% 是否运作实验程序
    if sgv['schedule_operation']['实验组模拟程序']:
        ## 导入相关数据
        Tools._copy_files_from_other_folders(sgv['folderpath_config'], sgv['folderpath_experiments_output_config'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出一份到输出文件夹

        Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/parameters"), is_auto_confirmation=sgv['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(sgv['folderpath_parameters'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/parameters"), is_auto_confirmation=sgv['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(sgv['folderpath_parameters'], sgv['folderpath_experiments_output_parameters'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出一份到输出文件夹
        # shutil.copy(Path(sgv['folderpath_parameters'], r"set_parameters_variables.py"), sgv['folderpath_experiments_output_parameters'])  # 导出一份生成参数的代码文件到输出文件夹
        from SystemicRiskSimulator.core.define.define_parameterVariables import para

        Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(sgv['folderpath_agents'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])
        Tools._copy_files_from_other_folders(sgv['folderpath_agents'], sgv['folderpath_experiments_output_agents'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出一份到输出文件夹
        # from SystemicRiskSimulator.core.define.define_agentsVariables import dict_bankCommercial, dict_bankInterbank

        ## 设置日志
        logger = logging.getLogger()
        logger.setLevel(sgv['test_logging'])
        if Path(sgv['folderpath_experiments_output_log'], "outputlog.txt").exists():
            os.remove(Path(sgv['folderpath_experiments_output_log'], "outputlog.txt"))  # 如果原来的日志存在，那么就删除重建
            pass  # if
        log_file_handler = logging.FileHandler(Path(sgv['folderpath_experiments_output_log'], "outputlog.txt"))
        logger.addHandler(log_file_handler)
        log_console_handler = logging.StreamHandler()
        logger.addHandler(log_console_handler)

        if sgv['is_develope_model']:
            logging.info("\n------------ 开发与调试模式！ ---------------\n")
            pass  # if
        logging.info("\n实验组名称：" + sgv['foldername_experiments'] + "\n")
        logging.info("\n模拟器 simulator 版本：" + sgv['simulator_version'] + "\n")
        logging.info("\n相关实验配置项 config 文件夹：" + sgv['folderpath_config'].name + "\n")
        logging.info("\n相关实验 models 文件夹：" + sgv['folderpath_models'].name + "\n")
        logging.info("\n相关实验 agents 数据文件夹：" + sgv['folderpath_agents'].name + "\n")
        logging.info("\n相关实验数据 experiments output data 文件夹：" + sgv['folderpath_experiments'].name + "\n")
        logging.info("\n相关实验参数 parameters 文件夹：" + sgv['folderpath_parameters'].name + "\n")

        ## 运行实验组模拟程序
        from SystemicRiskSimulator.programs.experiments_program import experiments_program
        experiments_program(sgv, para)

        ## 关闭日志
        logger.removeHandler(log_file_handler)
        pass  # if

    # %% 是否可视化结果程序
    if sgv['schedule_operation']['可视化结果程序']:
        from SystemicRiskSimulator.programs.visualize_data_program import visualize_data_program
        visualize_data_program(sgv)
        pass  # if

    # %% 清理
    ## 删除设置文件夹、模型文件夹内的所有文件，但是保留文件夹
    Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=sgv['is_auto_confirmation'])
    Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/parameters"), is_auto_confirmation=sgv['is_auto_confirmation'])
    Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])
    if not sgv['is_develope_model']:
        Tools._delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/models"), is_auto_confirmation=sgv['is_auto_confirmation'])
        pass  # if
