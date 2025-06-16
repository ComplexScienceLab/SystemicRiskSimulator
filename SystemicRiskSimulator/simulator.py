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

    # global sgv, para

    # %%
    import platform
    import logging
    from pathlib import Path
    import shutil
    import datetime
    import time
    import subprocess
    import pickle
    import base64
    from SystemicRiskSimulator.tools.tools import Tools
    from SystemicRiskSimulator.core.operations.collector import Collector

    # %% 初始化
    ## 获取项目路径、模拟器工具路径
    config['folderpath_project'] = Tools.get_project_rootpath()
    config['folderpath_simulator'] = Tools.get_project_rootpath(config['foldername_simulator'], config['folderpath_realpath_simulator'])

    from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv
    sgv.update((Tools.import_modules_from_package(str(Path(config['folderpath_project'], config['folderpath_config'])), r'set_config_variables', config['folderpath_project']))['set_config_variables'])
    sgv.update(config)

    config.update(sgv)

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
        str_foldername_simulator=sgv['foldername_simulator'],
        str_folderpath_realpath_simulator=sgv['folderpath_realpath_simulator'],
        str_foldername_outputData=sgv['foldername_outputData'],
        str_folderpath_realpath_outputData=sgv['folderpath_realpath_outputData'],
        str_folderpath_models=sgv['folderpath_models'],
        str_folderpath_config=sgv['folderpath_config'],
        str_folderpath_parameters=sgv['folderpath_parameters'],
        str_folderpath_agents=sgv['folderpath_agents'],
    )

    # from SystemicRiskSimulator.core.operations.operator import Operator

    ## 设定实验组运行方式
    if sgv['is_use_Gym_environments'] is False and sgv['is_use_RL_method'] is False:
        logging.debug("\nexperiments_program.py : 只使用模拟器自带的模型，不使用强化学习环境工具包自定义的模型。\n")
        sgv['运行实验组的方式'] = '运行ABM实验组'
    elif sgv['is_use_Gym_environments'] is False and sgv['is_use_RL_method'] is True and sgv['RL_state'] == 'using':
        logging.debug("\nexperiments_program.py : 使用自定义的环境模型，并且使用强化学习算法对已经训练过的模型做运用。\n")
        sgv['运行实验组的方式'] = '运行强化学习算法和ABM模型实验组做应用'
    elif sgv['is_use_Gym_environments'] is False and sgv['is_use_RL_method'] is True and sgv['RL_state'] == 'training':
        logging.debug("\nexperiments_program.py : 使用自定义的环境模型，并且使用强化学习算法做训练。\n")
        sgv['运行实验组的方式'] = '运行强化学习算法和ABM模型实验组做训练'
    elif sgv['is_use_Gym_environments'] is True and sgv['is_use_RL_method'] is False:
        logging.debug("\nexperiments_program.py : 使用 Gymnasium 环境框架结合自定义的环境模型，但是没有用强化学习算法进行训练。\n")
        sgv['运行实验组的方式'] = '运行Gym和ABM实验组'
    elif sgv['is_use_Gym_environments'] is True and sgv['is_use_RL_method'] is True and sgv['RL_state'] == 'using':
        logging.debug("\nexperiments_program.py : 使用 Gymnasium 环境框架结合自定义的环境模型，并且使用强化学习算法已经训练过的模型做运用。\n")
        sgv['运行实验组的方式'] = '运行强化学习算法和Gym框架结合自定义ABM模型实验组做应用'
    elif sgv['is_use_Gym_environments'] is True and sgv['is_use_RL_method'] is True and sgv['RL_state'] == 'training':
        logging.debug("\nexperiments_program.py : 使用 Gymnasium 环境框架结合自定义的环境模型，并且使用强化学习算法做训练。\n")
        sgv['运行实验组的方式'] = '运行强化学习算法和Gym框架结合自定义ABM模型实验组做训练'
        pass  # if


    if sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做训练':
        sgv['subfoldername_experiments_output_data'] = "RL_training"
    elif sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做应用':
        sgv['subfoldername_experiments_output_data'] = "RL_using"
    elif sgv['运行实验组的方式'] == '运行ABM实验组':
        sgv['exp_id_exp_output_data'] = ""
        sgv['subfoldername_experiments_output_data'] = "normal"
    else:
        raise ValueError(f"运行实验组的方式 {sgv['运行实验组的方式']} 不支持！")  # 如果运行实验组的方式不支持，则抛出异常
        pass  # if


    # %% 是否运作实验程序
    if sgv['schedule_operation']['实验组模拟程序']:
        ## 导入相关数据
        Tools.delete_and_recreate_folder(sgv['folderpath_experiments_output_config'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除输出文件夹原来的 config 文件夹
        # Tools.copy_files_from_other_folders(sgv['folderpath_config'], sgv['folderpath_experiments_output_config'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出 config 文件夹到输出文件夹
        shutil.copyfile(sgv['folderpath_config'] / "set_config_variables.py", sgv['folderpath_experiments_output_config'] / "set_config_variables.py")

        Tools.delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除模拟器之 data 文件夹之原来的 config 文件夹
        # Tools.copy_files_from_other_folders(sgv['folderpath_config'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出一份 config 文件夹到模拟器之 data 文件夹
        shutil.copyfile(sgv['folderpath_config'] / "set_config_variables.py", sgv['folderpath_simulator'] / "SystemicRiskSimulator/data/config/set_config_variables.py")

        Tools.delete_and_recreate_folder(sgv['folderpath_experiments_output_agents'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除并重新创建输出文件夹原来的 agents 文件夹
        # Tools.copy_files_from_other_folders(sgv['folderpath_agents'], sgv['folderpath_experiments_output_agents'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出 agents 文件夹到输出文件夹
        shutil.copytree(sgv['folderpath_agents'] / "agents", sgv['folderpath_experiments_output_agents'] / "agents")
        shutil.copyfile(sgv['folderpath_agents'] / "logfile.log", sgv['folderpath_experiments_output_agents'] / "logfile.log")
        shutil.copyfile(sgv['folderpath_agents'] / "set_agents_variables.py", sgv['folderpath_experiments_output_agents'] / "set_agents_variables.py")

        Tools.delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除并重新创建模拟器之 data 文件夹之原来的 agents 文件夹
        # Tools.copy_files_from_other_folders(sgv['folderpath_agents'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出一份 agents 文件夹到模拟器之 data 文件夹
        shutil.copytree(sgv['folderpath_agents'] / "agents", sgv['folderpath_simulator'] / "SystemicRiskSimulator/data/agents/agents")  # 导出一份 agents 文件夹到模拟器之 data 文件夹

        ## 获取一些系统信息
        sgv['system_platform'] = platform.system()

        ## 设置日志

        if sgv['is_rerun_all_done_works_in_the_same_experiments']:
            # 删除原有的主日志文件
            for file in Path(sgv['folderpath_experiments_output_log']).glob("outputlog.txt"):
                file.unlink()
            # 删除原有的各子实验日志文件，但是保留作业状态标记日志文件。
            for file in Path(sgv['folderpath_experiments_output_log']).glob("outputlog_*exp.txt"):
                file.unlink()
            pass  # if

        logger = logging.getLogger()
        logger.setLevel(sgv['test_logging'])

        log_file_handler = logging.FileHandler(Path(sgv['folderpath_experiments_output_log'], "outputlog.txt"))
        logger.addHandler(log_file_handler)
        log_console_handler = logging.StreamHandler()
        logger.addHandler(log_console_handler)

        if sgv['is_develope_mode']:
            logging.info("\n------------ 开发与调试模式！ ---------------\n")
            pass  # if
        logging.info("\n开始记录时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        logging.info("\n实验组名称：" + sgv['foldername_experiments'] + "\n")
        logging.info("\n模拟器 simulator 版本：" + sgv['simulator_version'][0] + "\n")
        logging.info("\n相关实验配置项 config 文件夹：" + sgv['folderpath_config'].name + "\n")
        logging.info("\n相关实验 agents 数据文件夹：" + sgv['folderpath_agents'].name + "\n")
        logging.info("\n相关实验参数 parameters 文件夹：" + sgv['folderpath_parameters'].name + "\n")
        logging.info("\n相关实验 models 文件夹：" + sgv['folderpath_models'].name + "\n")
        logging.info("\n相关实验数据 experiments output data 文件夹：" + sgv['folderpath_experiments'].name + "\n")

        ## 关闭日志记录器
        log_file_handler.close()
        logger.removeHandler(log_file_handler)
        log_console_handler.close()
        logger.removeHandler(log_console_handler)

        ## 运行实验组模拟程序
        if not sgv['is_develope_mode']:
            sgv_pkl = pickle.dumps(sgv)
            sgv_base64 = base64.b64encode(sgv_pkl).decode('utf-8')
            # para_pkl = pickle.dumps(para)
            # para_base64 = base64.b64encode(para_pkl).decode('utf-8')
            start_time = time.time()
            subprocess.run(["python", str(Path(sgv['folderpath_simulator'], 'SystemicRiskSimulator/programs/experiments_program.py')), sgv_base64])
            # subprocess.run(["python", str(Path(sgv['folderpath_simulator'], 'SystemicRiskSimulator/programs/experiments_program.py')), sgv_base64, para_base64])
        else:
            from SystemicRiskSimulator.programs.experiments_program import main
            start_time = time.time()
            main(sgv)
            pass  # if

        ## 继续打开日志记录器
        logger.addHandler(log_file_handler)
        logger.addHandler(log_console_handler)

        end_time = time.time()
        logging.info(f"\n模拟器运行时长：{end_time - start_time} 秒。\n")

        ## 关闭日志记录器
        log_file_handler.close()
        logger.removeHandler(log_file_handler)
        log_console_handler.close()
        logger.removeHandler(log_console_handler)

        pass  # if

    # %% 是否运作预处理实验结果程序
    if sgv['schedule_operation']['预处理实验结果程序']:

        Tools.delete_and_recreate_folder(sgv['folderpath_experiments_output_config'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除输出文件夹原来的 config 文件夹
        Tools.copy_files_from_other_folders(sgv['folderpath_config'], sgv['folderpath_experiments_output_config'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出 config 文件夹到输出文件夹

        logger = logging.getLogger()
        logger.setLevel(sgv['test_logging'])

        log_file_handler = logging.FileHandler(Path(sgv['folderpath_experiments_output_log'], "outputlog.txt"))
        logger.addHandler(log_file_handler)
        log_console_handler = logging.StreamHandler()
        logger.addHandler(log_console_handler)

        if not sgv['is_develope_mode']:
            sgv_pkl = pickle.dumps(sgv)
            sgv_base64 = base64.b64encode(sgv_pkl).decode('utf-8')
            start_time = time.time()
            subprocess.run(["python", str(Path(sgv['folderpath_simulator'], 'SystemicRiskSimulator/programs/transform_output_data_program.py')), sgv_base64])
            end_time = time.time()
            print(f"\n预处理实验结果程序运行总时长：{end_time - start_time} 秒。\n")
        else:
            from SystemicRiskSimulator.programs.transform_output_data_program import main
            start_time = time.time()
            main(sgv)
            pass  # if

        ## 继续打开日志记录器
        logger.addHandler(log_file_handler)
        logger.addHandler(log_console_handler)

        end_time = time.time()
        logging.info(f"\n模拟器运行时长：{end_time - start_time} 秒。\n")

        ## 关闭日志记录器
        log_file_handler.close()
        logger.removeHandler(log_file_handler)
        log_console_handler.close()
        logger.removeHandler(log_console_handler)

        pass  # if

    # %% 是否可视化结果程序
    if sgv['schedule_operation']['可视化结果程序']:

        Tools.delete_and_recreate_folder(sgv['folderpath_experiments_output_config'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除输出文件夹原来的 config 文件夹
        Tools.copy_files_from_other_folders(sgv['folderpath_config'], sgv['folderpath_experiments_output_config'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出 config 文件夹到输出文件夹

        logger = logging.getLogger()
        # logger.setLevel(sgv['test_logging'])
        logger.setLevel('ERROR')  # #BUG 因为可视化程序出现大量的无意义的输出，需要后续解决。目前暂时屏蔽。

        log_file_handler = logging.FileHandler(Path(sgv['folderpath_experiments_output_log'], "outputlog.txt"))
        logger.addHandler(log_file_handler)
        # log_console_handler = logging.StreamHandler()
        # logger.addHandler(log_console_handler)

        ## 关闭日志记录器
        log_file_handler.close()
        logger.removeHandler(log_file_handler)
        # log_console_handler.close()
        # logger.removeHandler(log_console_handler)
        # del log_file_handler, log_console_handler, logger

        if not sgv['is_develope_mode']:
            sgv_pkl = pickle.dumps(sgv)
            sgv_base64 = base64.b64encode(sgv_pkl).decode('utf-8')
            start_time = time.time()
            subprocess.run(["python", str(Path(sgv['folderpath_simulator'], 'SystemicRiskSimulator/programs/visualize_data_program.py')), sgv_base64])
            end_time = time.time()
            print(f"\n可视化数据运行总时长：{end_time - start_time} 秒。\n")
        else:
            from SystemicRiskSimulator.programs.visualize_data_program import main
            start_time = time.time()
            main(sgv)
            pass  # if

        # ## 继续打开日志记录器
        # logger.addHandler(log_file_handler)
        # logger.addHandler(log_console_handler)
        #
        # end_time = time.time()
        # logging.info(f"\n模拟器运行时长：{end_time - start_time} 秒。\n")
        #
        # ## 关闭日志记录器
        # log_file_handler.close()
        # logger.removeHandler(log_file_handler)
        # log_console_handler.close()
        # logger.removeHandler(log_console_handler)

        pass  # if

    # %% 清理

    ## 导出最后的配置数据
    Collector.export_config_data(sgv)

    ## 删除设置文件夹、模型文件夹内的所有文件，但是保留文件夹  #HACK 无用，但是可以保留作为备用
    # Tools.delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=sgv['is_auto_confirmation'])
    # Tools.delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/parameters"), is_auto_confirmation=sgv['is_auto_confirmation'])
    # Tools.delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])
    # if not sgv['is_maintain_model_files_in_simulator_when_develope_mode']:
    #     Tools.delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/models"), is_auto_confirmation=sgv['is_auto_confirmation'])
    #     pass  # if

    # %% 结束
    print("运行完毕！")
    print(f"时间：{datetime.datetime.now()}")

    # #TODO 发送邮件通知

    pass  # function
