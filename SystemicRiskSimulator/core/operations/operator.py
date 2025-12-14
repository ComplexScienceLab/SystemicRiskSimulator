"""
运作 #TODO 可以简化掉这个类，将其功能整合到`core.py`之中
"""

from pathlib import Path
import timeit
import os
import datetime
import logging
from copy import deepcopy
import json
from typing import Any, Optional
import pickle
import sqlite3
import numpy as np
import pandas as pd

from SystemicRiskSimulator.tools.logging_tools import log_message, record_work_state

from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.operations.collector import Collector

from SystemicRiskSimulator.tools.tools import Tools

pass  # end import


class Operator:
    """
    运作。包括安装数据、初始化数据等
    """

    # A_data = AgentDataCollection([], [])

    @classmethod
    def operate_installing(cls, sgv, para: Optional[dict] = None):
        """
        运作安装

        Args:
            sgv (dict): 模拟器全局变量
            para (Optional[dict]): 参数变量。默认为 None。如果 `init_parameters_method` 为 "set manually"，那么就需要设置此参数。

        Returns:

        """

        ## 设置参数作业列表

        # if sgv['init_parameters_method'] == "import data":

        # 如果是运行强化学习算法和ABM模型实验组做训练，则不使用 SQLite 数据库管理实验组
        if sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做训练':
            sgv['is_use_sqlite_to_manage_experiments'] = False
            pass  # if

        if sgv['is_use_sqlite_to_manage_experiments']:
            with open(Path(sgv['folderpath_parameters'], "parameters.pkl"), 'rb') as f:
                parameters_works = pd.read_pickle(f)
                pass  # with

            num_parameters_works = len(parameters_works)

            # 根据配置项从参数库中获取参数
            if sgv['list_idsExperiment_to_run'] is None:  # 如果没有设置实验组 id 列表，那么就设置计划运行所有的实验组
                list_idsExp_PLAN = list(range(0, num_parameters_works))
            elif isinstance(sgv['list_idsExperiment_to_run'], list):  # 如果设置了实验组 id 列表，那么就设置计划列表内的实验组
                list_idsExp_PLAN = sgv['list_idsExperiment_to_run']
            elif isinstance(sgv['list_idsExperiment_to_run'], str):  # 如果设置了实验组运行条件文本，那么就解析文本信息，作为查询条件，设置计划符合条件的实验组
                query_text = sgv['list_idsExperiment_to_run']
                try:
                    # 使用 eval 解析文本信息，作为查询条件
                    # parameters_works_filter = parameters_works.query(query_text)
                    parameters_works_filter = parameters_works[eval(query_text)]
                    list_idsExp_PLAN = parameters_works_filter['exp_id'].tolist()
                except Exception as e:
                    raise Exception(f"实验组运行条件文本解析错误！！！")
            else:
                list_idsExp_PLAN = []
                pass  # if

            ## SQLite 数据库统计实验组之上一次的作业之完成情况
            time_start_统计实验组作业情况 = timeit.default_timer()  # #DEBUG
            # 如果参数库当中的参数文件夹中的参数文件有更新，那么就要在后续删除原有的作业数据库再重建
            if os.path.exists(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db")):
                is_exist_experiments_works_status_db = True
                mtime_of_file_parameters_pkl = Path(sgv['folderpath_parameters'], "parameters.pkl").resolve().stat().st_mtime
                mtime_of_file_experimentsWorksStatus_db = Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db").resolve().stat().st_mtime
                if mtime_of_file_parameters_pkl > mtime_of_file_experimentsWorksStatus_db:
                    is_mtime_of_file_parameters_pkl_changed = True
                else:
                    is_mtime_of_file_parameters_pkl_changed = False
                    pass  # if
            else:
                is_exist_experiments_works_status_db = False
                is_mtime_of_file_parameters_pkl_changed = True
                pass  # if

            if sgv['is_rerun_all_done_works_in_the_same_experiments'] or is_mtime_of_file_parameters_pkl_changed:
                is_recreate_experiments_works_status_db = True
                if is_exist_experiments_works_status_db:
                    is_remove_experiments_works_status_db = True
                else:
                    is_remove_experiments_works_status_db = False
                    pass  # if
            else:
                is_recreate_experiments_works_status_db = False
                is_remove_experiments_works_status_db = False
                pass  # if

            if is_remove_experiments_works_status_db:
                os.remove(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
                pass  # if

            if is_recreate_experiments_works_status_db:  # 创建数据库并初始化表格
                conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
                c = conn.cursor()
                c.execute(
                    """CREATE TABLE IF NOT EXISTS experiments
                       (
                           exp_id
                           INTEGER
                           PRIMARY
                           KEY,
                           status_实验组模拟程序
                           TEXT
                       )"""
                )
                # 根据实验组总数量，生成实验组作业状态信息。其中，所有实验组作业状态为 "RAW"
                for i in range(1, num_parameters_works + 1):
                    c.execute("INSERT INTO experiments (exp_id, status_实验组模拟程序) VALUES (?, ?)", (i, "RAW"))
                    pass  # for
                conn.commit()
                is_exist_experiments_works_status_db = True
                is_recreate_experiments_works_status_db = False
            else:
                # 连接现有数据库
                conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
                c = conn.cursor()
                if sgv['is_rerun_all_done_works_in_the_same_experiments']:
                    c.execute("UPDATE experiments SET status_实验组模拟程序 = 'RAW'")
                    conn.commit()
                    pass  # if
                pass  # if
            # 检查实验组作业完成状态
            c.execute("SELECT exp_id, status_实验组模拟程序 FROM experiments")
            rows = c.fetchall()
            list_idsExp_DOING = []
            list_idsExp_DONE = []
            list_idsExp_RAW = []
            for row in rows:
                exp_id, status_实验组模拟程序 = row[0], row[1]
                if status_实验组模拟程序 == "DOING":
                    list_idsExp_DOING.append(exp_id)
                elif status_实验组模拟程序 == "DONE":
                    list_idsExp_DONE.append(exp_id)
                else:
                    list_idsExp_RAW.append(exp_id)
                    pass  # if
                pass  # for
            list_idsExp_TASK = [i for i in list_idsExp_PLAN if i not in list_idsExp_DONE]
            # 保存实验组作业完成状态信息
            with open(Path(sgv['folderpath_experiments_output_log'], "outputlog_worksStatesBeforeThisExperiments.json"), 'w') as f:
                json.dump(
                    {
                        "计划运行的实验组 id": list_idsExp_TASK,
                        "未运行过的实验组 id": list_idsExp_RAW,
                        "之前运行中被中断的实验组 id": list_idsExp_DOING,
                        "已完成的实验组 id": list_idsExp_DONE,
                        "完成率": len(list_idsExp_DONE) / num_parameters_works,
                        "中断率": len(list_idsExp_DOING) / num_parameters_works,
                    }, f
                )
                logging.info(
                    "实验组开始运行前，实验组作业完成状态情况如下:\n" + str(
                        {
                            "之前运行中被中断的实验组 id": list_idsExp_DOING,
                            "完成率": len(list_idsExp_DONE) / num_parameters_works,
                            "中断率": len(list_idsExp_DOING) / num_parameters_works,
                        }
                    )
                )

            ## 绘制色带分布图，展示实验组 id 分布对应的实验组作业运行之前的作业完成状态信息。#BUG 如果实验组很多，那么绘制图像会占用大量的内存与时间！可以考虑注释不运行这段。
            if sgv['is_draw_color_band_distribution_before_experiments']:
                ids = [row[0] for row in rows]  # 获取实验组 id
                status_实验组模拟程序_运行状态 = [row[1] for row in rows]  # 获取实验组作业状态
                logging.info("绘制实验组作业状态色带分布图...")
                Tools.draw_color_band_before_experiments(ids, status_实验组模拟程序_运行状态, list_idsExp_PLAN, list_idsExp_TASK, Path(sgv['folderpath_experiments_output_log'], "color_band_distribution_before_实验组模拟程序.png"))

            time_end_统计实验组作业情况 = timeit.default_timer()  # #DEBUG
            logging.debug(f"统计参数数据完成，用时：{time_end_统计实验组作业情况 - time_start_统计实验组作业情况} 秒。")  # #DEBUG

            conn.close()  # 关闭数据库连接



        else:

            with open(Path(sgv['folderpath_parameters'], "parameters.pkl"), 'rb') as f:
                parameters_works = pd.read_pickle(f)
                pass  # with

            num_parameters_works = len(parameters_works)

            # 根据配置项从参数库中获取参数
            if sgv['list_idsExperiment_to_run'] is None:  # 如果没有设置实验组 id 列表，那么就设置计划运行所有的实验组
                list_idsExp_PLAN = list(range(0, num_parameters_works))
            elif isinstance(sgv['list_idsExperiment_to_run'], list):  # 如果设置了实验组 id 列表，那么就设置计划列表内的实验组
                list_idsExp_PLAN = sgv['list_idsExperiment_to_run']
            elif isinstance(sgv['list_idsExperiment_to_run'], str):  # 如果设置了实验组运行条件文本，那么就解析文本信息，作为查询条件，设置计划符合条件的实验组
                query_text = sgv['list_idsExperiment_to_run']
                try:
                    # 使用 eval 解析文本信息，作为查询条件
                    # parameters_works_filter = parameters_works.query(query_text)
                    parameters_works_filter = parameters_works[eval(query_text)]
                    list_idsExp_PLAN = parameters_works_filter['exp_id'].tolist()
                except Exception as e:
                    raise Exception(f"实验组运行条件文本解析错误！！！")
            else:
                list_idsExp_PLAN = []
                pass  # if

            list_idsExp_TASK = [i for i in list_idsExp_PLAN]

            pass  # if

        Collector.export_parameter_data(sgv, parameters_works)  # 导出控制参数数据

        sgv['num_experiments_to_run'] = len(list_idsExp_TASK)  # 获取实验组数量
        sgv['num_unfinished_experiments_to_run'] = len(list_idsExp_TASK)  # 未完成的实验组数量

        ## 构建本次实验组所需的所有模型

        ### 判断属于什么运行模式
        if not sgv['is_develope_mode'] or not sgv['is_maintain_model_files_in_simulator_when_develope_mode']:
            # 如果是应用实验状态，则复制模型数据与内容到输出文件夹下，另外导出一份到`SystemicRiskSimulator/models`文件夹下
            Tools.delete_and_recreate_folder(sgv['folderpath_experiments_output_models'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除并重新创建输出文件夹之模型文件夹
            Tools.copy_files_from_other_folders(sgv['folderpath_models'], sgv['folderpath_experiments_output_models'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出模型文件夹到输出文件夹之模型文件夹
            Tools.delete_and_recreate_folder(Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/model"), is_auto_confirmation=sgv['is_auto_confirmation'])  # 删除并重新创建模拟器之 data 文件夹之模型文件夹
            Tools.copy_files_from_other_folders(sgv['folderpath_models'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/model"), is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出模型文件夹到模拟器之 data 文件夹
        else:
            pass  # if

        ## 导入模型（以字典的形式表示模型相关的模块）
        model_dict = Tools.import_modules_from_package(str(Path(sgv['folderpath_simulator'], r'SystemicRiskSimulator/data/model')), r"[Mm]odel", sgv['folderpath_simulator'])

        pass  # if

        ## 导出配置数据
        Collector.export_config_data(sgv)

        return sgv, list_idsExp_TASK, parameters_works, model_dict

        pass  # function

    # @classmethod
    # def operate_run_experiment(cls, A, A_data: AgentDataCollection, sgv: dict, para: dict, model: Any):
    #     """
    #     运作运行实验。用于传统的 ABM 模型。
    #
    #     Args:
    #         A (ModelAgent): 多主体
    #         A_last (ModelAgent): 上一回合的多主体
    #         A_data (AgentDataCollection): 多主体之数据
    #         sgv (dict): 模拟器全局变量
    #         para (dict): 参数变量
    #         model (Any): 模型节点实体
    #
    #     Returns:
    #
    #     """
    #
    #     ## 运行实验
    #
    #     sgv['experiment_start_time'] = timeit.default_timer()  # 记录此次实验开始时间
    #
    #     # 计算个体数量
    #     sgv['num_bank'] = len(A.note['id_bank'])
    #
    #     model_Finance = model['model_finance'](sgv['num_bank'])  # 初始化 Content_Finance 之实例
    #     if 'model_strategy' in model.keys():  # 如果该模型有设计 model_Strategy
    #         model_Strategy = model['model_strategy'](np.array(para['Strategy_default']))  # 初始化 model_Strategy 之实例 #BUG 不能这样代入参数 #TODO 需要重新适配 IB2111 等原来的模型
    #         model_main = model['model_main'](model_Finance, model_Strategy)  # 初始化 model_main 之实例
    #     else:
    #         model_main = model['model_main'](model_Finance)  # 初始化 Content_Model 之实例
    #         pass  # if
    #
    #     if not sgv['is_enable_multiprocessing_for_run_model']:
    #         log_message(
    #             "    开始执行模型内容：",
    #             Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
    #             f"logger_{sgv['id_experiment']}",
    #             is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
    #         )
    #         pass  # if
    #
    #     # model_main.model_content(A, A_last, A_data, para, sgv)
    #     model_main.model_content(A, A_data, para, sgv)
    #
    #     pass  # function

    # @classmethod
    # def operate_reset_experiment_for_PettingZoo(cls, sgv: dict, para: dict):
    #     """
    #     运作初始化实验。用于使用基于 PettingZoo 、Gym 等强化学习环境工具包自定义的模型。
    #
    #     Args:
    #         sgv (dict): 模拟器全局变量
    #         para (dict): 参数变量
    #
    #     Returns:
    #         A, A_data, sgv, para
    #     """
    #     if sgv['is_use_sqlite_to_manage_experiments']:
    #         record_work_state(sgv['id_experiment'], "status_实验组模拟程序", "DOING", sgv['folderpath_experiments_output_log'])  # 记录本次实验作业的完成状态为 "DOING"
    #
    #     ## 重置模拟器全局变量
    #     sgv['turn'] = 0
    #     sgv['phase'] = 0
    #     sgv['step'] = 0
    #     sgv['process_name'] = "START"
    #     sgv['is_continue_process'] = True
    #
    #     logging.info("重置实验。实验ID " + str(sgv['id_experiment']) + " 开始：\n")
    #
    #     logging.info("\n相关实验参数：" + str(para) + "\n")
    #
    #     ## 初始化 agents 数据
    #     A = cls.install_data(init_data_method=sgv['init_data_method'], sgv=sgv, para=para)  # 安装本次实验所需的多主体数据
    #     logging.debug("                    初始化数据")
    #     A_data = Collector.init_agent_data_collection(A, sgv, para)
    #     # sgv['step'] += 1
    #
    #     return A, A_data, sgv, para
    #     pass  # function

    @classmethod
    def operate_reset_experiment(cls, sgv: dict, para: dict):
        """
        运作初始化实验。

        Args:
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns:
            A, A_data, sgv, para
        """

        # # 更新实验组作业状态为 "DOING"  #HACK 这个可以删除
        # conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
        # c = conn.cursor()
        # c.execute("INSERT OR REPLACE INTO experiments (exp_id, status_实验组模拟程序) VALUES (?, 'DOING')", (sgv['id_experiment'],))
        # conn.commit()
        # conn.close()
        if sgv['is_use_sqlite_to_manage_experiments']:
            record_work_state(sgv['id_experiment'], "status_实验组模拟程序", "DOING", sgv['folderpath_experiments_output_log'])  # 记录本次实验作业的完成状态为 "DOING"

        # modelEntity = model.content  # 获取节点实体对应的模型实体

        ## 重置模拟器全局变量

        sgv['turn'] = 0
        sgv['phase'] = 0
        sgv['step'] = 0
        sgv['process_name'] = "START"
        sgv['is_continue_process'] = True

        if (not sgv['is_enable_multiprocessing_for_run_model'] and not (sgv['is_use_RL_method'] and sgv['RL_state'] == 'training')):
            log_message(
                "重置实验。实验ID " + str(sgv['id_experiment']) + " 开始：\n" + "\n开始记录时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + "\n相关实验参数：" + str(para) + "\n",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
            )

        ## 初始化 agents 数据
        A = cls.install_data(init_data_method=sgv['init_data_method'], sgv=sgv, para=para)  # 安装本次实验所需的多主体数据
        # A_last = ModelAgent(2, deepcopy(A.BB), deepcopy(A.b), deepcopy(A.IB), deepcopy(A.ib))  # #BUG 这个有用吗

        if (not sgv['is_enable_multiprocessing_for_run_model'] and not (sgv['is_use_RL_method'] and sgv['RL_state'] == 'training')):
            log_message(
                "                    初始化数据",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
            )

        A_data = Collector.init_agent_data_collection(A, sgv, para)

        return A, A_data, sgv, para
        # return A, A_last, A_data, sgv, para
        pass  # function

    @classmethod
    def operate_reset_experiment_for_Gym(cls, A, A_data: AgentDataCollection, sgv: dict, para: dict):
        """
        运作初始化实验（用于Gym）。

        Args:
            A (ModelAgent): 多主体
            A_data (AgentDataCollection): 多主体之数据
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns:
            A, A_data, sgv, para
        """

        # # 更新实验组作业状态为 "DOING"  #HACK 这个可以删除
        # conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
        # c = conn.cursor()
        # c.execute("INSERT OR REPLACE INTO experiments (exp_id, status_实验组模拟程序) VALUES (?, 'DOING')", (sgv['id_experiment'],))
        # conn.commit()
        # conn.close()
        if sgv['is_use_sqlite_to_manage_experiments']:
            record_work_state(sgv['id_experiment'], "status_实验组模拟程序", "DOING", sgv['folderpath_experiments_output_log'])  # 记录本次实验作业的完成状态为 "DOING"

        # modelEntity = model.content  # 获取节点实体对应的模型实体

        ## 重置模拟器全局变量

        sgv['turn'] = 0
        sgv['phase'] = 0
        sgv['step'] = 0
        sgv['process_name'] = "START"
        sgv['is_continue_process'] = True

        if (not sgv['is_enable_multiprocessing_for_run_model'] and not (sgv['is_use_RL_method'] and sgv['RL_state'] == 'training')):
            log_message(
                "重置实验。实验ID " + str(sgv['id_experiment']) + " 开始：\n" + "\n开始记录时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + "\n相关实验参数：" + str(para) + "\n",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
            )

        ## 初始化 agents 数据
        A = cls.reset_data(A, A_data, sgv, para)  # 安装本次实验所需的多主体数据
        # A_last = ModelAgent(2, deepcopy(A.BB), deepcopy(A.b), deepcopy(A.IB), deepcopy(A.ib))  # #BUG 这个有用吗

        ## 计算银行数量
        sgv['num_bank'] = len(A.note['id_bank'])

        if (not sgv['is_enable_multiprocessing_for_run_model'] and not (sgv['is_use_RL_method'] and sgv['RL_state'] == 'training')):
            log_message(
                "                    初始化数据",
                Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
                f"logger_{sgv['id_experiment']}",
                is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
            )

        A_data = Collector.reset_agent_data_collection(A, A_data, sgv, para)

        return A, A_data, sgv, para
        # return A, A_last, A_data, sgv, para
        pass  # function

    # @classmethod
    # def operate_step_experiment(cls, A, A_data: AgentDataCollection, sgv: dict, para: dict, model: Any):
    #     """
    #     运作步进实验。用于使用强化学习环境工具包自定义的模型。
    #
    #     Args:
    #         A (ModelAgent): 多主体
    #         A_data (AgentDataCollection): 多主体之数据
    #         sgv (dict): 模拟器全局变量
    #         para (dict): 参数字典
    #         model (Any): 模型节点实体
    #
    #     Returns:
    #
    #     """
    #
    #     ## 运行实验
    #
    #     sgv['experiment_start_time'] = timeit.default_timer()  # 记录此次实验开始时间
    #
    #     modelEntity = model.content  # 获取节点实体对应的模型实体
    #
    #     if not sgv['is_enable_multiprocessing_for_run_model']:
    #         log_message(
    #             "    开始执行模型内容：",
    #             Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
    #             f"logger_{sgv['id_experiment']}",
    #             is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
    #         )
    #
    #     sgv['process_name'] = modelEntity.attribute.entity_name  # 执行的过程之名称（英文名称）
    #
    #     process = modelEntity.process
    #
    #     A, A_data, para, sgv = process(modelEntity, A, A_data, para, sgv)
    #
    #     return A, A_data, sgv, para
    #
    #     pass  # function

    # @classmethod
    # def operate_end_experiment(cls, A_data: AgentDataCollection, sgv: dict):
    #
    #     ## 收尾实验
    #
    #     # if True:  # #HACK 如果需要调试，请使用这个替换下面的
    #     if not sgv['is_enable_multiprocessing_for_run_model']:
    #         log_message(
    #             "    结束执行模型内容。",
    #             Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
    #             f"logger_{sgv['id_experiment']}",
    #             is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
    #         )
    #
    #     sgv['is_continue_process'] = False  # 不再继续运行过程
    #
    #     sgv['experiment_end_time'] = timeit.default_timer()  # 记录此次实验结束时间
    #     sgv['experiments_running_time'] += sgv['experiment_end_time'] - sgv['experiment_start_time']  # 累加此次实验运行时长
    #
    #     ## 导出数据之于已经收集的，然后结束本次实验
    #
    #     sgv['export_data_start_time'] = timeit.default_timer()  # 记录此次导出数据开始时间
    #
    #     if not sgv['is_enable_multiprocessing_for_run_model']:
    #         log_message(
    #             "                    导出数据",
    #             Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
    #             f"logger_{sgv['id_experiment']}",
    #             is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
    #         )
    #
    #     Collector.export_agent_data(A_data, sgv)
    #
    #     sgv['export_data_end_time'] = timeit.default_timer()  # 记录此次导出数据结束时间
    #     sgv['export_data_running_time'] += sgv['export_data_end_time'] - sgv['export_data_start_time']  # 累加此次导出数据运行时长
    #
    #     if sgv['is_use_sqlite_to_manage_experiments']:
    #         record_work_state(sgv['id_experiment'], "status_实验组模拟程序", "DONE", sgv['folderpath_experiments_output_log'])
    #
    #     if not sgv['is_enable_multiprocessing_for_run_model']:
    #         log_message(
    #             "本次实验结束，还剩下  " + str(sgv['num_unfinished_experiments_to_run']) + "  个实验。\n\n",
    #             Path(sgv['folderpath_experiments_output_log'], f"outputlog_{sgv['id_experiment']}_exp.txt"),
    #             f"logger_{sgv['id_experiment']}",
    #             is_enable_multiprocessing_for_run_model=sgv['is_enable_multiprocessing_for_run_model']
    #         )
    #
    #     pass  # function

    # @classmethod
    # def set_imported_values_to_Bank_variables(cls, para: dict, sgv: dict):
    #     """
    #     导入数据以初始化银行主体众、银行间主体众变量
    #
    #     Args:
    #         para (dict): 参数集
    #         sgv (dict): 模拟器全局变量
    #
    #     Returns:
    #         bank(BankCommercial): 银行主体众
    #         interbank(BankInterbank): 银行间主体众
    #     """
    #
    #     with open(Path(sgv['folderpath_agents'], 'agents', f"BB_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
    #         dict_bankCommercial = pickle.load(f)
    #     with open(Path(sgv['folderpath_agents'], 'agents', f"IB_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
    #         dict_bankInterbank = pickle.load(f)
    #
    #     # ## NOTE 当用对象字段数据结构时：
    #     # bank, interbank = cls.set_default_values_to_Bank_variables()
    #     # bank.__dict__ = deepcopy(dict_bankCommercial)
    #     # interbank.__dict__ = deepcopy(dict_bankInterbank)
    #
    #     ## NOTE 当用pandas数据结构时：
    #     bank = pd.Series()
    #     for k, v in deepcopy(dict_bankCommercial).items():
    #         bank[k] = v
    #     interbank = pd.Series()
    #     for k, v in deepcopy(dict_bankInterbank).items():
    #         interbank[k] = v
    #
    #     return bank, interbank
    #
    #     pass  # function

    @classmethod
    def install_data(cls, init_data_method: str, sgv: dict, para: dict):
        """
        不同的初始化方式。

        参数init_data_method可选项：

        - ``import data``:  导入数据以初始化

        注意：在模型中使用类似`BB.Z[b]`这样的形式，目的是为了提取每个变量字段内部的数值赋值处理。不直接使用`BB.Z`，这样仅仅处理字段自身。例如`BB.Z[b] = BB.A[b]`将`BB.A`内的数值赋值给`BB.Z`，而`BB.Z = BB.A`是将`BB.A`作为引用赋值给`BB.Z`，而不是将`BB.A`的数值赋值给`BB.Z`。这样的意义是保证各个字段数据不会引用错乱。

        Args:
            init_data_method (str): 初始化数据的方式
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns:
            A (pd.Series): 系统性风险个体众
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量


        """

        # if init_data_method == "import data":
        #     BB, IB = cls.set_imported_values_to_Bank_variables(para, sgv)  # 导入数据以初始化银行变量
        # else:
        #     raise ("关键词" + str(init_data_method) + "取值错误！")
        #     pass  # if

        # #HACK 改之前的加载 agents 数据文件代码，对于未适配的 set_config_variables.py 文件而言，如果没有
        # dict_agents_data = {}
        # for i, agents_data in enumerate(sgv['list_agents_data']):
        #     with open(Path(sgv['folderpath_agents'], 'agents', f"{agents_data}_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
        #         dict_agents_data[agents_data] = pickle.load(f)
        #     pass  # for

        # #HACK 改之后的加载 agents 数据文件代码
        dict_agents_data = {}
        sgv['id_agents'] = para['id_agents']
        for para_01 in sgv['list_agents_data_filename_para_01']:
            agents_filename = f"id={sgv['id_agents']}-v={para_01}"
            for para_02 in sgv['list_agents_data_filename_para_02']:
                if isinstance(para[para_02], float):
                    agents_filename += f"-{para_02}={float(para[para_02]):.2f}"
                else:
                    agents_filename += f"-{para_02}={para[para_02]}"
                pass  # for
            agents_filename += ".pkl"
            with open(Path(sgv['folderpath_agents'], 'agents', agents_filename), 'rb') as f:
                dict_agents_data[para_01] = pickle.load(f)
            pass  # for

        # with open(Path(sgv['folderpath_agents'], 'agents', f"IB_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
        #     dict_bankInterbank = pickle.load(f)

        # ## NOTE 当用对象字段数据结构时：
        # bank, interbank = cls.set_default_values_to_Bank_variables()
        # bank.__dict__ = deepcopy(dict_bankCommercial)
        # interbank.__dict__ = deepcopy(dict_bankInterbank)

        ## NOTE 当用pandas数据结构时：

        A = pd.Series()
        for k, v in dict_agents_data.items():
            A[k] = pd.Series()
            for k1, v1 in deepcopy(v).items():
                A[k][k1] = v1
            pass  # for

        # for k, v in dict_agents_data.items():
        #     if k == 'BB':
        #         BB = pd.Series()
        #         for k, v in deepcopy(v).items():
        #             BB[k] = v
        #     elif k == 'IB':
        #         IB = pd.Series()
        #         for k, v in deepcopy(v).items():
        #             IB[k] = v
        #     pass

        # BB = pd.Series()
        # for k, v in deepcopy(dict_bankCommercial).items():
        #     BB[k] = v
        # IB = pd.Series()
        # for k, v in deepcopy(dict_bankInterbank).items():
        #     IB[k] = v

        # sgv['num_bank'] = len(BB.exist)  # 获取 agents 之个体数量

        # # HACK 后续需要统一这两个变量的用法，防止混乱使用
        # b = (BB.exist | BB.exit)  # 临时设置A.BB示性变量
        # ib = ((BB.exist | BB.exit).reshape(-1, 1) & (BB.exist | BB.exit).reshape(1, -1))  # 临时设置IB示性变量

        ## 构建Agent模型
        # NOTE 注意这时候`b`、`ib`变量在后续过程中没有发生变动。

        ## HACK 当用pandas数据结构时：
        # A = pd.Series([BB, IB, b, ib], index=['BB', 'IB', 'b', 'ib'])

        # ## HACK 当用对象字段数据结构时。
        # A = ModelAgent(
        #     0,  # 编号（必备的）
        #     BB,  # 商业银行群
        #     b,  # 商业银行群示性变量
        #     IB,  # 银行间邻接矩阵
        #     ib,  # 银行间邻接矩阵示性变量
        # )

        return A
        pass  # function

    @classmethod
    def reset_data(cls, A, A_data: AgentDataCollection, sgv: dict, para: dict):
        """
        重置已有的个体数据。

        注意：在模型中使用类似`BB.Z[b]`这样的形式，目的是为了提取每个变量字段内部的数值赋值处理。不直接使用`BB.Z`，这样仅仅处理字段自身。例如`BB.Z[b] = BB.A[b]`将`BB.A`内的数值赋值给`BB.Z`，而`BB.Z = BB.A`是将`BB.A`作为引用赋值给`BB.Z`，而不是将`BB.A`的数值赋值给`BB.Z`。这样的意义是保证各个字段数据不会引用错乱。

        Args:
            A (ModelAgent): 多主体
            A_data (AgentDataCollection): 多主体之数据
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns:
            A (pd.Series): 系统性风险个体众
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量


        """

        # if init_data_method == "import data":
        #     BB, IB = cls.set_imported_values_to_Bank_variables(para, sgv)  # 导入数据以初始化银行变量
        # else:
        #     raise ("关键词" + str(init_data_method) + "取值错误！")
        #     pass  # if

        # #HACK 改之前的加载 agents 数据文件代码，对于未适配的 set_config_variables.py 文件而言，如果没有
        # dict_agents_data = {}
        # for i, agents_data in enumerate(sgv['list_agents_data']):
        #     with open(Path(sgv['folderpath_agents'], 'agents', f"{agents_data}_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
        #         dict_agents_data[agents_data] = pickle.load(f)
        #     pass  # for

        # #HACK 改之后的加载 agents 数据文件代码
        dict_agents_data = {}
        sgv['id_agents'] = para['id_agents']
        for para_01 in sgv['list_agents_data_filename_para_01']:
            agents_filename = f"id={sgv['id_agents']}-v={para_01}"
            for para_02 in sgv['list_agents_data_filename_para_02']:
                if isinstance(para[para_02], float):
                    agents_filename += f"-{para_02}={float(para[para_02]):.2f}"
                else:
                    agents_filename += f"-{para_02}={para[para_02]}"
                pass  # for
            agents_filename += ".pkl"
            with open(Path(sgv['folderpath_agents'], 'agents', agents_filename), 'rb') as f:
                dict_agents_data[para_01] = pickle.load(f)
            pass  # for

        # with open(Path(sgv['folderpath_agents'], 'agents', f"IB_year={para['year']}_density={para['density']:.2f}.pkl"), 'rb') as f:
        #     dict_bankInterbank = pickle.load(f)

        # ## NOTE 当用对象字段数据结构时：
        # bank, interbank = cls.set_default_values_to_Bank_variables()
        # bank.__dict__ = deepcopy(dict_bankCommercial)
        # interbank.__dict__ = deepcopy(dict_bankInterbank)

        ## NOTE 当用pandas数据结构时：
        for k, v in dict_agents_data.items():
            # A[k] = pd.Series()
            if k != 'note':
                for k1, v1 in deepcopy(v).items():
                    if isinstance(v1, np.ndarray):
                        # if (A[k][k1] != v1).any():
                        #     print(f"重置 {k} {k1}，旧值{A[k][k1]}，新值{v1}")  # DEBUG
                        A[k][k1][:] = v1[:]
                    else:
                        # if A[k][k1] != v1:
                        #     print(f"重置 {k} {k1}，旧值{A[k][k1]}，新值{v1}")  # DEBUG
                        A[k][k1] = v1
                        pass  # if
                    pass  # for
            else:
                for k1, v1 in deepcopy(v).items():
                    for k1, v1 in deepcopy(v).items():
                        if isinstance(v1, np.ndarray):
                            # if (A[k][k1] != v1).any():
                            #     print(f"重置 {k} {k1}，旧值{A[k][k1]}，新值{v1}")  # DEBUG
                            A[k][k1][:] = v1[:]
                        else:
                            # if A[k][k1] != v1:
                            #     print(f"重置 {k} {k1}，旧值{A[k][k1]}，新值{v1}")  # DEBUG
                            A[k][k1] = v1
                            pass  # if
                        pass  # for
            pass  # for

        # for k, v in dict_agents_data.items():
        #     if k == 'BB':
        #         BB = pd.Series()
        #         for k, v in deepcopy(v).items():
        #             BB[k] = v
        #     elif k == 'IB':
        #         IB = pd.Series()
        #         for k, v in deepcopy(v).items():
        #             IB[k] = v
        #     pass

        # BB = pd.Series()
        # for k, v in deepcopy(dict_bankCommercial).items():
        #     BB[k] = v
        # IB = pd.Series()
        # for k, v in deepcopy(dict_bankInterbank).items():
        #     IB[k] = v

        # sgv['num_bank'] = len(BB.exist)  # 获取 agents 之个体数量

        # # HACK 后续需要统一这两个变量的用法，防止混乱使用
        # b = (BB.exist | BB.exit)  # 临时设置A.BB示性变量
        # ib = ((BB.exist | BB.exit).reshape(-1, 1) & (BB.exist | BB.exit).reshape(1, -1))  # 临时设置IB示性变量

        ## 构建Agent模型
        # NOTE 注意这时候`b`、`ib`变量在后续过程中没有发生变动。

        ## HACK 当用pandas数据结构时：
        # A = pd.Series([BB, IB, b, ib], index=['BB', 'IB', 'b', 'ib'])

        # ## HACK 当用对象字段数据结构时。
        # A = ModelAgent(
        #     0,  # 编号（必备的）
        #     BB,  # 商业银行群
        #     b,  # 商业银行群示性变量
        #     IB,  # 银行间邻接矩阵
        #     ib,  # 银行间邻接矩阵示性变量
        # )

        return A
        pass  # function

    pass  # class
