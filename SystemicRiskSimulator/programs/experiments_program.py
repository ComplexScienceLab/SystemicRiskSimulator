"""
实验组模拟程序。用于运行实验组。

#BUG 如果运行的文件批量太大，可能存在内存泄露的问题。建议每次运行的文件批量不要超过 10000 个。
"""
import timeit
# -*- coding: utf-8 -*-


import warnings
import logging
import platform
from copy import deepcopy
import os
from pathlib import Path
import time
import sys
import sqlite3
import base64
import pickle
import multiprocessing
from multiprocessing import Pool
import json
import numpy as np
import pandas as pd
from tqdm import tqdm

import torch  # 添加对 torch 的导入

# from matplotlib import pyplot as plt
# from torch.distributions import Categorical

from SystemicRiskSimulator.core.operations.collector import Collector
from SystemicRiskSimulator.core.operations.operator import Operator
from SystemicRiskSimulator.tools.logging_tools import log_message, record_work_state
from SystemicRiskSimulator.tools.rl_utils import RlUtils


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
    log_file_handler = logging.FileHandler(Path(sgv['folderpath_experiments_output_log'], "outputlog.txt"), encoding='utf-8-sig')
    logger.addHandler(log_file_handler)
    log_console_handler = logging.StreamHandler()
    logger.addHandler(log_console_handler)

    # %% 预安装模型、数据，运行实验组

    if sgv['is_ignore_warning']:
        warnings.filterwarnings("ignore")  # 忽略警告

    ## 初始化、构建、安装模型
    sgv, list_idsExp_TASK, parameters_works, model_dict = Operator.operate_installing(sgv)

    ## 运行实验组
    logging.debug("\n\n\n实验组开始：\n\n")

    sgv['experiments_running_time'] = 0  # 初始化实验组运行总时长
    sgv['export_data_running_time'] = 0  # 初始化导出数据运行总时长

    # model = list(models.values())[0]  # 获取当前实验对应的模型

    # 如果是运行强化学习算法和ABM模型实验组做训练，则不使用 SQLite 数据库管理实验组
    if sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做训练':
        sgv['is_use_sqlite_to_manage_experiments'] = False
        pass  # if

    # 连接实验组作业管理数据库
    # 记录实验组运行状态
    if sgv['is_use_sqlite_to_manage_experiments']:
        conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
        c = conn.cursor()
        c.execute("SELECT id,status FROM experiments WHERE status='TASK'")
        rows = c.fetchall()
        sgv['list_idsExp_TASK'] = [row[0] for row in rows]  # 获取实际上需要运行的实验组 id 列表
    else:
        sgv['list_idsExp_TASK'] = list_idsExp_TASK
        pass  # if

    ## 通过设定的运行方式运行实验组
    match sgv['运行实验组的方式']:
        case '运行ABM实验组':
            ## #NOTE：运行ABM实验组
            paras = parameters_works[parameters_works['exp_id'].isin(sgv['list_idsExp_TASK'])]  # 获取实际上需要运行的实验组参数作业数据框  #HACK  #HACK 2025-04-14 移到此处

            ## #NOTE：多进程并行处理
            if sgv['is_enable_multiprocessing_for_run_model']:
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
                for i, para in paras.iterrows():
                    para = para.to_dict()
                    exp_id = int(para[ 'exp_id'])  # 获取当前实验编号
                    work = (exp_id, sgv, para, model_dict)
                    works.append(work)
                    pass  # for

                ## 并行运行实验作业
                with Pool(num_cores) as p:
                    p.starmap(fun_single_experiment_work, works)
                    pass  # with

                ## 并行处理之后，读取各个实验日志文件之内容追加到主进程日志文件之内容
                if sgv['is_enable_multiprocessing_for_run_model']:
                    with open(Path(sgv['folderpath_experiments_output_log'], "outputlog.txt"), 'a', encoding='utf-8-sig') as f:
                        for i, para in paras.iterrows():
                            if Path(sgv['folderpath_experiments_output_log'], f"outputlog_{i}_exp.txt").exists():
                                with open(Path(sgv['folderpath_experiments_output_log'], f"outputlog_{i}_exp.txt"), 'r', encoding='utf-8', errors='replace') as f_sub:
                                    f.write(f_sub.read())
                                    pass  # with
                                pass  # if
                            pass  # for
                        pass  # with
                    pass  # if

            ## #NOTE：串行处理
            else:

                sgv['simulator_start_time'] = time.time()  # 记录串行运行模式下，模拟器开始运行时刻

                for i, para in paras.iterrows():
                    para = para.to_dict()  # 将参数数据框转换为字典
                    # model = list(models.values())[0]  # 获取当前实验对应的模型
                    sgv['id_experiment'] = int(para['exp_id'])  # 设定当前实验编号
                    sgv['num_unfinished_experiments_to_run'] -= 1  # 更新未完成实验数
                    ## 运行一次实验作业
                    fun_single_experiment_work(sgv['id_experiment'], sgv, para, model_dict)
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

        case '运行Gym和ABM实验组':
            ## #NOTE：运行Gym和ABM实验组

            import gymnasium as gym

            sgv['simulator_start_time'] = time.time()  # 记录模拟器开始运行时刻

            ## # ----------------------------------------------------------------------------------

            # 注册 Gym 环境
            gym.register(
                id="gym_env",
                entry_point=sgv['Gym_register_entry_point'],
            )

            ## 运行固定的奖励函数参数
            np.random.seed(57)  # 随机选取一个奖励函数的参数 #TODO 后续改成从配置文件获取
            # alpha_reward = round(np.random.choice(parameters_works['alpha_reward'].unique()), 2)  # 随机选择一个奖励函数的参数
            alpha_reward = 0.60  # #DEBUG 调试专用
            grouped_parameters_works = parameters_works.groupby('alpha_reward')  # 根据 alpha_reward 列分组 parameters_works
            paras = grouped_parameters_works.get_group(alpha_reward)[grouped_parameters_works.get_group(alpha_reward)['exp_id'].isin(sgv['list_idsExp_TASK'])]  # 获取实际上需要运行的实验组参数作业数据框
            sgv['list_idsExp_TASK'] = grouped_parameters_works.get_group(alpha_reward)['exp_id'].tolist()  # 获取实验组 id 列表

            # 创建环境
            # exp_id = np.random.choice(sgv['list_idsExp_TASK'])  # 随机选择一个实验组
            exp_id = 955  # #DEBUG 调试专用
            para = paras[paras['exp_id'] == exp_id].squeeze().to_dict()  # 获取实验参数作业数据框并转换为字典
            A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para)  # 重置实验
            env = gym.make(
                sgv['gym_env_id'],
                A=A,
                A_data=A_data,
                para=para,
                sgv=sgv,
            )

            model_gymenv = env.unwrapped  # 解包之后的环境

            # 每一局，随机选取一个实验组运行。
            np.random.seed(114)  # 设置随机种子 #TODO 后续改成从配置文件获取
            sgv['episode'] = 0  # 初始化局数计数器
            while sgv['episode'] < sgv['max_num_episode']:
                sgv['episode'] += 1
                # exp_id = np.random.choice(sgv['list_idsExp_TASK'])  # 随机选择一个实验组
                exp_id = 956  # #DEBUG 调试专用

                para = paras[paras['exp_id'] == exp_id].squeeze().to_dict()  # 获取实验参数作业数据框并转换为字典
                logging.info(f"第 {sgv['episode']} 局开始")
                observations, infos = env.reset()  # #BUG 这个输出值如何利用起来？
                episode_over = False  # 是否结束本局
                # 对于本局，不断运行 env.step() 直到结束
                model_gymenv.M.model_content(A, A_data, para, sgv)  # 执行一次轮次级别的步进更新  #TODO 考虑把这个移到 env.reset() 当中。
                while not episode_over:
                    # 采样模型动作
                    # action = env.action_space.sample()  # 选择动作  #TODO 这行仅作为参考，可以删除
                    model_gymenv.M.model_action(A=model_gymenv.A, A_data=model_gymenv.A_data, para=model_gymenv.para, sgv=model_gymenv.sgv)
                    actions = dict(
                        id_agent=A.BB.id_agent,
                        theta_IB_def=A.IB.theta_IB_def,
                        con=A.BB.con,
                    )
                    actions_gym = model_gymenv.convert_actions_to_gym(actions)  # 转换成 Gym 动作
                    observations, rewards, terminated, truncated, infos = env.step(actions_gym)  # 执行动作
                    episode_over = np.array(terminated).all() or np.array(truncated).all()  # 检查是否结束
                    if episode_over:
                        logging.info(f"\n第 {sgv['episode']} 局结束\n")
                    pass  # while
                pass  # while
            ## # ----------------------------------------------------------------------------------

            sgv['simulator_end_time'] = time.time()  # 记录模拟器结束运行时刻
            sgv['simulator_running_time'] = sgv['simulator_end_time'] - sgv['simulator_start_time']  # 记录模拟器运行时长
            logging.info(f"实验组结束。\n实验组运行总时长：{sgv['experiments_running_time']} 秒。\n导出数据运行总时长：{sgv['export_data_running_time']} 秒。\n模拟器运行总时长：{sgv['simulator_running_time']}秒。")

            ## 默认程序打开输出文件查看
            if sgv['is_auto_open_outputlog']:
                system = platform.system()
                if system == 'Darwin':  # macOS
                    os.system(r"open " + str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))
                elif system == 'Windows':  # Windows
                    os.startfile(str(Path(sgv['folderpath_experiments_output_log'], r"outputlog.txt")))
                elif system == 'Linux':  # Linux
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

        case '运行强化学习算法和ABM模型实验组做应用':
            ## #NOTE：运行强化学习算法和ABM模型实验组做应用
            sgv['simulator_start_time'] = time.time()  # 记录模拟器开始运行时刻

            ## 运行固定的奖励函数参数
            np.random.seed(57)  # 随机选取一个奖励函数的参数 #TODO 后续改成从配置文件获取
            # alpha_reward = round(np.random.choice(parameters_works['alpha_reward'].unique()), 2)  # 随机选择一个奖励函数的参数
            alpha_reward = 0.50  # #DEBUG 调试专用
            grouped_parameters_works = parameters_works.groupby('alpha_reward')  # 根据 alpha_reward 列分组 parameters_works
            paras = grouped_parameters_works.get_group(alpha_reward)[grouped_parameters_works.get_group(alpha_reward)['exp_id'].isin(sgv['list_idsExp_TASK'])]  # 获取实际上需要运行的实验组参数作业数据框
            sgv['list_idsExp_TASK'] = grouped_parameters_works.get_group(alpha_reward)['exp_id'].tolist()  # 获取实验组 id 列表  # 这句是否重复？

            ## 创建环境
            sgv['id_experiment'] = np.random.choice(paras.exp_id)  # 随机选择一个实验组
            # sgv['id_experiment'] = np.random.choice(sgv['list_idsExp_TASK'])  # 随机选择一个实验组
            # sgv['id_experiment'] = 955  # #DEBUG 调试专用
            para = paras[paras['exp_id'] == sgv['id_experiment']].squeeze().to_dict()  # 获取实验参数作业数据框并转换为字典
            A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para)  # 重置实验
            M = model_dict['model_main'](model_dict, A, A_data, para, sgv)

            ## 加载训练好的模型和参数
            logging.info("加载训练好的模型和参数")
            for i in (M.A.note.strategy_method == "learning").nonzero()[0]:
                RlUtils.load_training_data(M.model_algorithm[i], M.sgv['folderpath_experiments'] / "RL" / f"{i}")  # 调用加载方法
                pass  # for

            ## 每一局，随机选取一个实验组运行。
            np.random.seed(114)  # 设置随机种子 #TODO 后续改成从配置文件获取
            M.sgv['id_episode'] = 0  # 初始化局数计数器
            for i_episode in range(sgv['num_episodes']):  # 每次迭代的局数
                M.sgv['id_episode'] = i_episode

                sgv['id_experiment'] = np.random.choice(paras.exp_id)  # 随机选择一个实验组
                # sgv['id_experiment'] = np.random.choice(sgv['list_idsExp_TASK'])  # 随机选择一个实验组
                # sgv['id_experiment'] = 955  # #DEBUG 调试专用
                para = paras[paras['exp_id'] == sgv['id_experiment']].squeeze().to_dict()  # 获取实验参数作业数据框并转换为字典 #BUG 为什么没用到？

                ## 重置环境
                M.A, M.A_data, M.sgv, M.para = Operator.operate_reset_experiment_for_Gym(M.A, M.A_data, M.sgv, para)

                ## 运行一局环境模拟
                M.model_process()

                # 保存实验组数据
                Collector.export_agent_data(M.A_data, sgv)

                pass  # for

        case '运行强化学习算法和ABM模型实验组做训练':

            ## #NOTE：运行强化学习算法和ABM模型实验组做训练
            sgv['simulator_start_time'] = time.time()  # 记录模拟器开始运行时刻

            ## 运行固定的奖励函数参数
            # np.random.seed(57)  # 随机选取一个奖励函数的参数 #TODO 后续改成从配置文件获取
            # alpha_reward = round(np.random.choice(parameters_works['alpha_reward'].unique()), 2)  # 随机选择一个奖励函数的参数
            alpha_reward = 0.50  # #DEBUG 调试专用
            grouped_parameters_works = parameters_works.groupby('alpha_reward')  # 根据 alpha_reward 列分组 parameters_works
            paras = grouped_parameters_works.get_group(alpha_reward)[grouped_parameters_works.get_group(alpha_reward)['exp_id'].isin(sgv['list_idsExp_TASK'])]  # 获取实际上需要运行的实验组参数作业数据框
            sgv['list_idsExp_TASK'] = grouped_parameters_works.get_group(alpha_reward)['exp_id'].tolist()  # 获取实验组 id 列表

            ## 创建环境
            sgv['id_experiment'] = np.random.choice(paras.exp_id)  # 随机选择一个实验组
            # sgv['id_experiment'] = 955  # #DEBUG 调试专用
            para = paras[paras['exp_id'] == sgv['id_experiment']].squeeze().to_dict()  # 获取实验参数作业数据框并转换为字典
            A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para)  # 重置实验
            M = model_dict['model_main'](model_dict, A, A_data, para, sgv)

            ## 每一局，随机选取一个实验组运行。
            np.random.seed(114)  # 设置随机种子 #TODO 后续改成从配置文件获取
            M.sgv['id_episode'] = 0  # 初始化局数计数器
            for i_training_iteration in range(sgv['num_training_iterations']):  # 进行指定次数的迭代
                M.sgv['training_iteration'] = i_training_iteration + 1
                with tqdm(total=int(sgv['num_episodes'] / sgv['num_training_iterations']), desc=f"迭代 {M.sgv['training_iteration']}") as pbar:  # 显示进度条
                    for i_episode in range(int(sgv['num_episodes'] / sgv['num_training_iterations'])):  # 每次迭代的局数
                        # M.sgv['episode'] = i_episode + 1

                        sgv['id_experiment'] = np.random.choice(paras.exp_id)  # 随机选择一个实验组
                        # sgv['id_experiment'] = 955  # #DEBUG 调试专用
                        para = paras[paras['exp_id'] == sgv['id_experiment']].squeeze().to_dict()  # 获取实验参数作业数据框并转换为字典 #BUG 为什么没用到？

                        ## 重置环境
                        M.A, M.A_data, M.sgv, M.para = Operator.operate_reset_experiment_for_Gym(M.A, M.A_data, M.sgv, para)

                        ## 运行一局环境模拟
                        M.model_process()

                        # if not M.sgv['is_continue_process']:
                        #     logging.info(f"第 {M.sgv['episode']} 局结束")
                        #     # logging.info(f"第 {M.sgv['episode']} 局结束，总奖励: {sum(M.A.AB.rewards['values'])}")
                        #     pass  # if

                        ## 完成一局之后的处理

                        # 转换为数据框
                        for i in range(M.sgv['num_bank']):
                            M.A.AB.observations[i] = pd.DataFrame(M.A.AB.observations[i])
                            M.A.AB.next_observations[i] = pd.DataFrame(M.A.AB.next_observations[i])
                            M.A.AB.actions[i] = pd.DataFrame(M.A.AB.actions[i])
                            M.A.AB.rewards[i] = pd.DataFrame(M.A.AB.rewards[i])
                            M.A.AB.dones[i] = pd.DataFrame(M.A.AB.dones[i])
                            M.A.AB.truncations[i] = pd.DataFrame(M.A.AB.truncations[i])
                            pass  # for

                        ## 预处理 M.A.AB 各个个体之不合理的部分
                        for i in range(M.sgv['num_bank']):
                            M.A.AB.observations[i] = M.A.AB.observations[i].iloc[:-1, :]  # 去掉最后一行
                            # M.A.AB.next_observations[i] = M.A.AB.next_observations[i].iloc[1:, :]  # 去掉第一行
                            pass  # for

                        ## 更新强化学习算法策略

                        ## 从数据框筛选出有效数据
                        for i in np.where(M.A.note.strategy_method == "learning")[0]:
                            dict_valid_data = dict()
                            for k1, v1 in M.A.AB.items():
                                if k1 != 'id_agent':
                                    for k2, v2 in v1[i].items():
                                        if k2 != 'mask':
                                            if len(v1[i][v1[i]['mask']][k2].values) > 0:
                                                dict_valid_data[k1] = np.stack(v1[i][v1[i]['mask']][k2].values)  # 从数据框筛选出有效数据
                                            else:  # 如果筛选的数据是空的，则赋值 0 值
                                                dict_valid_data[k1] = np.zeros((1, len(v1[i][k2].values[0])))
                                                pass  # if
                                            pass  # if
                                        pass  # for
                                    pass  # if
                                pass  # for

                            pass  # for

                            ## 更新强化学习算法策略
                            logging.debug(f"开始更新银行 {i} 的强化学习算法策略")
                            M.model_algorithm[i].update(dict_valid_data)
                            logging.debug(f"结束更新银行 {i} 的强化学习算法策略")
                            pass  # for

                            ## 更新进度条
                            if (i_episode + 1) % sgv['num_episodes_to_update_tqdm'] == 0:  # 每隔若干局数更新一次进度条
                                pbar.set_postfix({
                                    'episode':
                                        f"{(sgv['num_episodes'] / sgv['num_training_iterations'] * (M.sgv['training_iteration'] - 1) + i_episode):.0f}",
                                    # 'return':  #TODO 可以考虑加上其它信息，例如 rewards
                                    #     f'{np.mean(win_list[-100:]):.3f}'
                                })  # 显示当前局数
                            pbar.update(1)  # 更新进度条

                        pass  # while
                        # 保存实验组数据
                        Collector.export_agent_data(M.A_data, sgv)

                        M.sgv['id_episode'] += 1

                        pass  # for
                    pass  # with
                pass  # for

            ## 导出实验结果数据

            # 保存训练的数据
            for i in (M.A.note.strategy_method == "learning").nonzero()[0]:
                RlUtils.save_training_data(M.model_algorithm[i], M.sgv['folderpath_experiments_output_data'] / "RL" / f"{i}")
                pass  # for

        case '运行强化学习算法和Gym框架结合自定义ABM模型实验组做应用':  # #HACK  其实后续不打算用 Gym 相关的环境框架了
            pass  # TODO

        case '运行强化学习算法和Gym框架结合自定义ABM模型实验组做训练':  # #HACK  其实后续不打算用 Gym 相关的环境框架了

            ## #NOTE：运行强化学习和Gym和ABM模型实验组做训练

            import gymnasium as gym

            sgv['simulator_start_time'] = time.time()  # 记录模拟器开始运行时刻

            # 初始化 Gym 环境和自定义环境模型
            gym.register(
                id=sgv['gym_env_id'],
                entry_point=sgv['Gym_register_entry_point'],
            )

            ## ----------------------------------------------------------------------

            sgv['simulator_end_time'] = time.time()  # 记录模拟器结束运行时刻
            sgv['simulator_running_time'] = sgv['simulator_end_time'] - sgv['simulator_start_time']  # 记录模拟器运行时长
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

            pass  # match

    # 如果是运行强化学习算法和ABM模型实验组做训练，则不使用 SQLite 数据库管理实验组
    if sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做训练':
        sgv['is_use_sqlite_to_manage_experiments'] = False
        pass  # if

    # 记录实验组运行状态
    if sgv['is_use_sqlite_to_manage_experiments']:

        ## 连接 SQLite 数据库，统计实验组之本次作业之完成情况
        num_parameters_works = len(parameters_works)
        time_start_统计实验组作业情况 = time.time()
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
        with open(Path(sgv['folderpath_experiments_output_log'], "outputlog_worksStatesBeforeThisExperiments.json"), 'w', encoding='utf-8') as f:
            json.dump({
                "计划运行的实验组 id": sgv['list_idsExp_TASK'],
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

        time_end_统计实验组作业情况 = time.time()
        logging.debug(f"统计参数数据完成，用时：{time_end_统计实验组作业情况 - time_start_统计实验组作业情况} 秒。")

        conn.close()  # 关闭数据库连接

    else:
        logging.info("实验组运行方式不使用 SQLite 数据库管理实验组。默认所有的实验组作业都已完成。")
        sgv['list_idsExp_DONE'] = sgv['list_idsExp_TASK']

        pass  # if

    pass  # main


def fun_single_experiment_work(exp_id: int, sgv_original: dict, para, model_dict: dict):
    """
    实验模拟程序。用于运行单个实验。

    只使用模拟器自带的模型，不使用强化学习环境工具包自定义的模型

    Args:
        exp_id (int): 实验编号
        sgv_original (dict): 模拟器全局变量（原始的）
        para (pandas.Series): 实验参数
        model_dict (dict): 模型字典。键名是模型名称，键值是模型类。模型类需要被初始化为实例才能使用。

    Returns:
        None
    """
    sgv = deepcopy(sgv_original)  # 复制全局变量，保证不同实验的全局变量的独立性
    sgv['id_experiment'] = exp_id  # 设定当前实验编号

    ## 重置实验
    A, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para)

    ## 安装模型

    # model_Finance = model_dict['model_finance'](sgv['num_bank'])  # 初始化 Content_Finance 之实例
    if 'model_strategy' in model_dict.keys():  # 如果该模型有设计 model_Strategy
        # model_Strategy = model_dict['model_strategy'](np.array(para['Strategy_default']))  # 初始化 model_Strategy 之实例 #BUG 不能这样代入参数 #TODO 需要重新适配 IB2111 等原来的模型
        model_main = model_dict['model_main'](model_dict, A, A_data, para, sgv)  # 初始化 model_main 之实例
    else:
        model_main = model_dict['model_main'](model_dict, A, A_data, para, sgv)  # 初始化 model_main 之实例
        # model_main = model_dict['model_main'](model_Finance)  # 初始化 model_main 之实例
        pass  # if

    # A, A_last, A_data, sgv, para = Operator.operate_reset_experiment(sgv, para, model_dict)

    ## 运行实验
    sgv['experiment_start_time'] = timeit.default_timer()  # 记录此次实验开始时间

    # 计算个体数量
    sgv['num_bank'] = len(A.note['id_bank'])

    if not sgv['is_enable_multiprocessing_for_run_model']:
        log_message(
            "    开始执行模型内容：",
            Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
            f"logger_{sgv['id_experiment']}",
            is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
        )
        pass  # if

    # 运行一局模型之全过程
    model_main.model_process()

    ## 收尾实验
    # if True:  # #HACK 如果需要调试，请使用这个替换下面的
    if not sgv['is_enable_multiprocessing_for_run_model']:
        log_message(
            "    结束执行模型内容。",
            Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
            f"logger_{sgv['id_experiment']}",
            is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
        )

    sgv['is_continue_process'] = False  # 不再继续运行过程

    sgv['experiment_end_time'] = timeit.default_timer()  # 记录此次实验结束时间
    sgv['experiments_running_time'] += sgv['experiment_end_time'] - sgv['experiment_start_time']  # 累加此次实验运行时长

    ## 导出数据之于已经收集的，然后结束本次实验

    sgv['export_data_start_time'] = timeit.default_timer()  # 记录此次导出数据开始时间

    if not sgv['is_enable_multiprocessing_for_run_model']:
        log_message(
            "                    导出数据",
            Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
            f"logger_{sgv['id_experiment']}",
            is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
        )

    Collector.export_agent_data(A_data, sgv)

    sgv['export_data_end_time'] = timeit.default_timer()  # 记录此次导出数据结束时间
    sgv['export_data_running_time'] += sgv['export_data_end_time'] - sgv['export_data_start_time']  # 累加此次导出数据运行时长

    if sgv['is_use_sqlite_to_manage_experiments']:
        record_work_state(sgv['id_experiment'], "status_实验组模拟程序", "DONE", sgv['folderpath_experiments_output_log'])

    if not sgv['is_enable_multiprocessing_for_run_model']:
        log_message(
            "本次实验结束，还剩下  " + str(sgv['num_unfinished_experiments_to_run']) + "  个实验。\n\n",
            Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
            f"logger_{sgv['id_experiment']}",
            is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
        )

    pass  # function


if __name__ == '__main__':
    # 从命令行参数获取配置字典
    sgv_base64 = sys.argv[1]
    sgv_pkl = base64.b64decode(sgv_base64)
    sgv = pickle.loads(sgv_pkl)

    main(sgv)
