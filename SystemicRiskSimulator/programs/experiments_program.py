"""
实验组模拟程序。用于运行实验组。

#BUG 如果运行的文件批量太大，可能存在内存泄露的问题。建议每次运行的文件批量不要超过 10000 个。
"""

# -*- coding: utf-8 -*-


from SystemicRiskSimulator.external_packages import warnings, logging, platform, deepcopy, os, Path, time, sys, sqlite3, base64, pickle, multiprocessing, Pool, json, np
from SystemicRiskSimulator.core.operations.operator import Operator


def main(sgv):
    """
    实验组模拟程序。用于运行实验组。
    """
    # # %% 设置工作目录。
    # # folderpath_settings=Tools.setup_working_directory()
    # if Path(sys.argv[0]).name == Path(__file__).name:
    #     # 在控制台运行，切换到脚本所在的文件夹
    #     folderpath = Path(__file__).resolve().parent
    #     os.chdir(folderpath)
    # else:
    #     # 通过其他脚本运行，执行特定的代码
    #     list_args = Tools.decode_args([*sys.argv[1:]])
    #     folderpath = list_args[0]
    #     pass  # if
    #
    # folderpath_parameters = folderpath

    # %% 预安装模型、数据，运行实验组

    ## 设置主进程日志
    logger = logging.getLogger()
    logger.setLevel(sgv['test_logging'])
    log_file_handler = logging.FileHandler(Path(sgv['folderpath_experiments_output_log'], "outputlog.txt"))
    logger.addHandler(log_file_handler)
    log_console_handler = logging.StreamHandler()
    logger.addHandler(log_console_handler)

    # %% 预安装模型、数据，运行实验组

    if sgv['is_ignore_warning']:
        warnings.filterwarnings("ignore")  # 忽略警告

    ## 初始化、构建、安装模型
    if sgv['init_parameters_method'] == 'import data':
        sgv, list_idsExp_TASK, parameters_works, model = Operator.operate_installing(sgv)
        pass  # if

    ## 运行实验组
    logging.debug("\n\n\n实验组开始：\n\n")

    sgv['experiments_running_time'] = 0  # 初始化实验组运行总时长
    sgv['export_data_running_time'] = 0  # 初始化导出数据运行总时长

    # model = list(models.values())[0]  # 获取当前实验对应的模型

    # # 连接实验组作业管理数据库
    # conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
    # c = conn.cursor()
    # c.execute("SELECT id,status FROM experiments WHERE status='TASK'")
    # rows = c.fetchall()
    # list_idsExp_TASK = [row[0] for row in rows]  # 获取实际上需要运行的实验组 id 列表
    parameters_works_TASK = parameters_works[parameters_works['exp_id'].isin(list_idsExp_TASK)]  # 获取实际上需要运行的实验组参数作业数据框

    if sgv['is_enable_multiprocessing_for_run_model']:
        ## #NOTE：多进程并行处理
        # para = para.to_dict()  # 将参数数据框转换为字典

        ## 并行计算时，关闭主进程日志记录器，改由子进程记录各自的日志
        log_file_handler.close()
        logger.removeHandler(log_file_handler)
        log_console_handler.close()
        logger.removeHandler(log_console_handler)

        num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 计算 CPU 核心数

        ## 生成作业组
        # sgv['id_experiment'] = 0  # 设定当前实验编号
        works = []
        for i, para in parameters_works_TASK.iterrows():
            exp_id = int(parameters_works_TASK.loc[i, 'exp_id'])  # 获取当前实验编号
            work = (exp_id, sgv, para, model)
            works.append(work)
            pass  # for

        ## 并行运行实验作业
        with Pool(num_cores) as p:
            p.starmap(fun_single_experiment_work, works)
            pass  # with

        ## 并行处理之后，读取各个实验日志文件之内容追加到主进程日志文件之内容
        if sgv['is_enable_multiprocessing_for_run_model']:
            with open(Path(sgv['folderpath_experiments_output_log'], "outputlog.txt"), 'a') as f:
                for i, para in parameters_works_TASK.iterrows():
                    if Path(sgv['folderpath_experiments_output_log'], f"outputlog_{i + 1}_exp.txt").exists():
                        with open(Path(sgv['folderpath_experiments_output_log'], f"outputlog_{i + 1}_exp.txt"), 'r') as f_sub:
                            f.write(f_sub.read())
                            pass  # with
                        pass  # if
                    pass  # for
                pass  # with
            pass  # if

    else:
        ## #NOTE：串行处理

        sgv['simulator_start_time'] = time.time()  # 记录串行运行模式下，模拟器开始运行时刻

        for i, para in parameters_works_TASK.iterrows():
            para = para.to_dict()  # 将参数数据框转换为字典
            # model = list(models.values())[0]  # 获取当前实验对应的模型
            model = model  # 获取当前实验对应的模型
            sgv['id_experiment'] = i + 1  # 设定当前实验编号

            ## 运行一次实验作业
            fun_single_experiment_work(sgv['id_experiment'], sgv, para, model)
            pass  # for

        sgv['simulator_end_time'] = time.time()  # 记录串行运行模式下，记录模拟器结束运行时刻
        sgv['simulator_running_time'] = sgv['simulator_end_time'] - sgv['simulator_start_time']  # 记录串行运行模式下，模拟器运行时长

        logging.info(f"实验组结束。\n实验组运行总时长：{sgv['experiments_running_time']} 秒。\n导出数据运行总时长：{sgv['export_data_running_time']} 秒。\n模拟器运行总时长：{sgv['simulator_running_time']}秒。")

        ## 默认程序打开输出文件查看
        if sgv['is_auto_open_outputlog']:
            system = platform.system()
            if system == 'Darwin':
                os.system(r"open " + str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))
            elif system == 'Windows':
                os.startfile(str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))
            elif system == 'Linux':
                os.system('xdg-open ' + str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))  # #BUG 还没测试过
            else:
                print("Unsupported operating system")
                pass  # if
            pass  # if

        if sgv['is_ignore_warning']:
            warnings.filterwarnings("default")  # 恢复警告
            pass  # if

        ## 关闭日志记录器
        log_file_handler.close()
        logger.removeHandler(log_file_handler)
        log_console_handler.close()
        logger.removeHandler(log_console_handler)

        pass  # if

    ## 连接 SQLite 数据库，统计实验组之本次作业之完成情况
    num_parameters_works = len(parameters_works)
    time_start_统计实验组作业情况 = time.time()  # #DEBUG
    conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
    c = conn.cursor()
    # 检查实验组作业完成状态
    c.execute("SELECT exp_id, status_实验组模拟程序 FROM experiments")
    rows = c.fetchall()
    list_idsExp_DOING = []
    list_idsExp_DONE = []
    list_idsExp_RAW = []
    for row in rows:
        exp_id, status_实验组模拟程序 = row
        if status_实验组模拟程序 == "DOING":
            list_idsExp_DOING.append(exp_id)
        elif status_实验组模拟程序 == "DONE":
            list_idsExp_DONE.append(exp_id)
        else:
            list_idsExp_RAW.append(exp_id)
            pass  # if
        pass  # for
    # 保存实验组作业完成状态信息
    with open(Path(sgv['folderpath_experiments_output_log'], "outputlog_worksStatesBeforeThisExperiments.json"), 'w') as f:
        json.dump({
            "计划运行的实验组 id": list_idsExp_TASK,
            "未运行过的实验组 id": list_idsExp_RAW,
            "之前运行中被中断的实验组 id": list_idsExp_DOING,
            "已完成的实验组 id": list_idsExp_DONE,
            "完成率": len(list_idsExp_DONE) / num_parameters_works,
            "中断率": len(list_idsExp_DOING) / num_parameters_works,
        }, f)
        logging.info("实验组开始运行前，实验组作业完成状态情况如下:\n" + str({
            "之前运行中被中断的实验组 id": list_idsExp_DOING,
            "完成率": len(list_idsExp_DONE) / num_parameters_works,
            "中断率": len(list_idsExp_DOING) / num_parameters_works,
        }))
        pass  # with

    time_end_统计实验组作业情况 = time.time()  # #DEBUG
    logging.debug(f"统计参数数据完成，用时：{time_end_统计实验组作业情况 - time_start_统计实验组作业情况} 秒。")  # #DEBUG

    conn.close()  # 关闭数据库连接

    pass  # main


def fun_single_experiment_work(exp_id: int, sgv_original: dict, para, model: dict):
    """
    实验模拟程序。用于运行单个实验。

    Args:
        exp_id (int): 实验编号
        sgv_original (dict): 模拟器全局变量（原始的）
        para (pandas.Series): 实验参数
        model (dict): 模型

    Returns:
        None
    """
    sgv = deepcopy(sgv_original)  # 复制全局变量，保证不同实验的全局变量的独立性
    sgv['id_experiment'] = exp_id  # 设定当前实验编号

    ## 进行实验作业
    if sgv['is_use_PettingZoo_environments'] is False and sgv['is_use_RLlib_frameworks'] is False:
        ## NOTE 如果只使用模拟器自带的模型，不使用强化学习环境工具包自定义的模型

        logging.debug("\nexperiments_program.py : 只使用模拟器自带的模型，不使用强化学习环境工具包自定义的模型。\n")  # DEBUG专用

        ## 重置实验
        A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para, model)
        # A, A_last, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para, model)

        ## 运行实验
        Operator.operate_run_experiment(A, A_data, sgv, para, model)
        # Operator.operate_run_experiment(A, A_last, A_data, sgv, para, model)

        ## 收尾实验
        Operator.operate_end_experiment(A_data, sgv)


    elif sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is False:
        ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型，但是没有用强化学习框架 RLlib 时
        logging.debug("\nexperiments_program.py : 使用 PettingZoo 环境框架结合自定义的环境模型，但是没有用强化学习框架 RLlib 进行训练。\n")  # DEBUG 专用

        ## 重置实验
        A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para, model)
        # A, A_last, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para, model)
        ## 步进式运行实验
        A, A_data, sgv, para = Operator.operate_step_experiment(A, A_data, sgv, para, model)
        # A, A_data, sgv, para, model = Operator.operate_step_experiment(sgv, para, model)
        ## 收尾实验
        Operator.operate_end_experiment(A_data, sgv)

    elif sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is True and sgv['RL_state'] == 'using':
        ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型，并且使用强化学习框架 RLlib ，并且强化学习状态是做应用时
        logging.debug("\nexperiments_program.py : 使用 PettingZoo 环境框架结合自定义的环境模型，并且使用强化学习框架 RLlib 已经训练过的模型做运用。\n")  # DEBUG 专用

        ## 重置实验
        A, A_last, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para, model)
        ## 步进式运行实验
        A, A_data, sgv, para = Operator.operate_step_experiment(A, A_data, sgv, para, model)
        # A, A_data, sgv, para, model = Operator.operate_step_experiment(sgv, para, model)
        ## 收尾实验
        Operator.operate_end_experiment(A_data, sgv)

    elif sgv['is_use_PettingZoo_environments'] is True and sgv['is_use_RLlib_frameworks'] is True and sgv['RL_state'] == 'training':
        ## #NOTE 如果使用 PettingZoo 环境框架结合自定义的环境模型，并且使用强化学习框架 RLlib ，并且强化学习状态是做训练时

        logging.debug("\nexperiments_program.py : 使用 PettingZoo 环境框架结合自定义的环境模型，并且使用强化学习框架 RLlib 进行训练。\n")  # DEBUG专用

        ## 重置实验
        A, A_last, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para, model)
        ## 步进式运行实验
        A, A_data, sgv, para = Operator.operate_step_experiment(A, A_data, sgv, para, model)
        # A, A_data, sgv, para, model = Operator.operate_step_experiment(sgv, para, model)
        ## 收尾实验
        Operator.operate_end_experiment(A_data, sgv)

        pass  # if

    pass  # if


pass  # function

if __name__ == '__main__':
    # 从命令行参数获取配置字典
    sgv_base64 = sys.argv[1]
    sgv_pkl = base64.b64decode(sgv_base64)
    sgv = pickle.loads(sgv_pkl)

    main(sgv)
