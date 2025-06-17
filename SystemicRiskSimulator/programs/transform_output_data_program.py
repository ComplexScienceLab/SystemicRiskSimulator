"""
预处理实验结果数据。

该程序有以下的独立任务：
- 导入Pandas格式的实验结果数据转换为面板形式再导出；
- 导入Pandas格式的实验结果数据合并为一个文件；


【导入Pandas格式的实验结果数据转换为面板形式再导出】思路：
1. 分别读取多个实验结果数据文件，然后依次转换为面板形式的数据。
2. 面板形式的数据依次导出为 PKL、CSV、xlsx 格式数据。

【导入Pandas格式的实验结果数据合并为一个文件】思路：
1. 依次读取多个实验结果数据文件，然后合并为一个文件。
2. 合并后的数据表导出为 PKL、CSV、xlsx 格式数据。


"""

# %% [markdown] # NOTE 导入Pandas格式的实验结果数据，然后转换为面板形式的数据，导出PKL、CSV、xlsx 格式数据。

# %%


# from dask import delayed, compute
# import dask.dataframe as dd
# from dask.diagnostics import ProgressBar
## NOTE 导入包

import platform
from pathlib import Path
import sqlite3
import re
import glob
import pandas as pd
import numpy as np
from copy import deepcopy
import sys
import pickle
import base64
from multiprocessing import Pool
import multiprocessing
import warnings
import logging
import json
import timeit
import os
# from multiprocessing import Lock

from SystemicRiskSimulator.tools.logging_tools import record_work_state

from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter


# import dask.dataframe as dd


# 创建一个全局锁
# lock = Lock()


def main(sgv):
    if sgv['is_ignore_warning']:
        warnings.filterwarnings("ignore")  # 忽略警告

    # %% 初始化
    from SystemicRiskSimulator.tools.tools import Tools
    list_transform_output_data_packages = ['openpyxl']  # 所需的第三方工具包 #NOTE 如果需要添加新的包，请在此处添加
    Tools._check_and_install_packages(list_transform_output_data_packages)  # 安装所需的第三方工具包。#BUG 如果没有安装成功，请手动安装。

    # %% [markdown] 预处理数据

    # %%
    print("执行：")

    if sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做训练':
        sgv['subfoldername_experiments_output_data'] = "RL_training"
        folderpath_experiments_output_data = sgv['folderpath_experiments_output_data'] / sgv['subfoldername_experiments_output_data']
    elif sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做应用':
        sgv['subfoldername_experiments_output_data'] = "RL_using"
        folderpath_experiments_output_data = sgv['folderpath_experiments_output_data'] / sgv['subfoldername_experiments_output_data']
    elif sgv['运行实验组的方式'] == '运行ABM实验组':
        sgv['exp_id_exp_output_data'] = ""
        sgv['subfoldername_experiments_output_data'] = "normal"
        folderpath_experiments_output_data = sgv['folderpath_experiments_output_data'] / sgv['subfoldername_experiments_output_data']
    else:
        raise ValueError(f"运行实验组的方式 {sgv['运行实验组的方式']} 不支持！")  # 如果运行实验组的方式不支持，则抛出异常
        pass  # if
    folderpath_experiments_output_data.mkdir(parents=True, exist_ok=True)

    num_files_BB = len(list(folderpath_experiments_output_data.glob('*v=BB-*.pkl')))  # 获取实验组输出数据pkl格式之BB数据之文件数量
    num_files_IB = len(list(folderpath_experiments_output_data.glob('*v=IB-*.pkl')))  # 获取实验组输出数据pkl格式之IB数据之文件数量
    print(f"BB 文件数等于 IB 文件数？：{num_files_BB == num_files_IB}")  # DEBUG


    if sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做训练':
        sgv['is_use_sqlite_to_manage_experiments'] = False  # 禁用 SQLite 数据库管理实验组作业状态，因为强化学习算法和ABM模型实验组做训练无需使用 SQLite 数据库管理实验组作业状态。
        pass  # if

    if sgv['is_use_sqlite_to_manage_experiments']:
        ## 连接 SQLite 数据库，统计实验组作业完成情况（#HACK #NOTE 只能用于串行处理模式）
        conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
        c = conn.cursor()
        # 如果没有列 status_预处理实验结果程序 ，那么添加该列
        c.execute("PRAGMA table_info(experiments)")
        if not any([v[1] == 'status_预处理实验结果程序' for v in c.fetchall()]):
            c.execute("ALTER TABLE experiments ADD COLUMN status_预处理实验结果程序 TEXT DEFAULT 'RAW'")
            conn.commit()
            pass  # if
        # 如果重新运行所有已经完成的实验，那么重置所有实验组作业状态为 "RAW"
        if sgv['is_rerun_all_done_works_in_the_same_experiments']:
            c.execute("UPDATE experiments SET status_预处理实验结果程序 = 'RAW' WHERE status_预处理实验结果程序 = 'DONE'")
            conn.commit()
            pass  # if
        # 检查实验组作业完成状态
        c.execute("SELECT exp_id, status_预处理实验结果程序 FROM experiments")
        rows = c.fetchall()
        list_idsExp_DOING = []
        list_idsExp_DONE = []
        list_idsExp_RAW = []
        for row in rows:
            exp_id, status_预处理实验结果程序 = row[0], row[1]
            if status_预处理实验结果程序 == "DOING":
                list_idsExp_DOING.append(exp_id)
            elif status_预处理实验结果程序 == "DONE":
                list_idsExp_DONE.append(exp_id)
            else:
                list_idsExp_RAW.append(exp_id)
                pass  # if
            pass  # for

        # 如果实验组作业状态表中没有实验组 id，那么添加实验组 id 列
        c.execute("PRAGMA table_info(experiments)")
        if not any([v[1] == 'exp_id' for v in c.fetchall()]):
            c.execute("ALTER TABLE experiments ADD COLUMN exp_id INTEGER")
            conn.commit()
            pass  # if

        pass  # if

    else:
        pass  # if

    # 读取实验组作业状态信息
    list_idsExp_DOING = []
    list_idsExp_DONE = []
    list_idsExp_RAW = []

    list_idsExp_PLAN = sgv['list_idsExperiment_to_run'] if sgv['list_idsExperiment_to_run'] is not None else list(range(0, num_files_BB))
    list_idsExp_TASK = [i for i in list_idsExp_PLAN if i not in list_idsExp_DONE]

    # 如果是运行强化学习算法和ABM模型实验组做训练，则不使用 SQLite 数据库管理实验组
    if sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做训练':
        sgv['is_use_sqlite_to_manage_experiments'] = False
        pass  # if

    if sgv['is_use_sqlite_to_manage_experiments']:

        # list_idsExp_PLAN = sgv['list_idsExperiment_to_run'] if sgv['list_idsExperiment_to_run'] is not None else list(range(0, num_files_BB))
        # list_idsExp_TASK = [i for i in list_idsExp_PLAN if i not in list_idsExp_DONE]
        # 保存实验组作业完成状态信息
        with open(Path(sgv['folderpath_experiments_output_log'], "outputlog_worksStatesBeforeThisExperiments.json"), 'w') as f:
            json.dump({
                "计划运行的实验组 id": list_idsExp_TASK,
                "未运行过的实验组 id": list_idsExp_RAW,
                "之前运行中被中断的实验组 id": list_idsExp_DOING,
                "已完成的实验组 id": list_idsExp_DONE,
                "完成率": len(list_idsExp_DONE) / num_files_BB,
                "中断率": len(list_idsExp_DOING) / num_files_BB,
            }, f)
            logging.info("实验组开始运行前，实验组作业完成状态情况如下:\n" + str({
                "之前运行中被中断的实验组 id": list_idsExp_DOING,
                "完成率": len(list_idsExp_DONE) / num_files_BB,
                "中断率": len(list_idsExp_DOING) / num_files_BB,
            }))
        # # 绘制色带分布图，展示实验组 id 分布对应的实验组作业运行之前的作业完成状态信息。
        # ids = [row[0] for row in rows]  # 获取实验组 id
        # status_预处理实验结果程序_运行状态 = [row[1] for row in rows]  # 获取实验组作业状态
        # Tools.draw_color_band_before_experiments(ids, status_预处理实验结果程序_运行状态, list_idsExp_PLAN, list_idsExp_TASK, Path(sgv['folderpath_experiments_output_log'], "color_band_distribution_before_预处理实验结果程序.png"))
        conn.close()
        pass  # if

    if not sgv['运行实验组的方式'] == '运行强化学习算法和ABM模型实验组做训练':
        ## 读取实验结果数据。根据 list_idsExp_TASK 中的实验组 id，读取实验结果数据。
        dict_filepath_pkl = dict()
        for para_01 in sgv['list_agents_data_filename_para_01']:
            list_filepath_pkl = []
            for id_exp in list_idsExp_TASK:
                list_filepath_pkl.extend(list(folderpath_experiments_output_data.glob(f'exp={id_exp}-v={para_01}-aid=*.pkl')))
                pass  # for
            dict_filepath_pkl[para_01] = list_filepath_pkl
            pass  # for

    else:  # 如果是是运行强化学习算法和ABM模型实验组做训练，那么读取所有实验组 id 的实验结果数据
        ## 读取实验结果数据。根据 list_idsExp_TASK 中的实验组 id，读取实验结果数据。
        dict_filepath_pkl = dict()
        for para_01 in sgv['list_agents_data_filename_para_01']:
            list_filepath_pkl = list(folderpath_experiments_output_data.glob(f'id=*-exp=*-v={para_01}-aid=*.pkl'))
            list_idsExp_TASK = [int(re.search(r'id=(\d+)-exp=(\d+)-v=', str(v)).group(2)) for v in list_filepath_pkl]  # 获取实验组 id
            # list_filepath_pkl = []
            # for id_exp in list_idsExp_TASK:
            #     list_filepath_pkl.extend(list(folderpath_experiments_output_data.glob(f'id=*-exp=*-v={para_01}-aid=*.pkl')))
            #     pass  # for
            dict_filepath_pkl[para_01] = list_filepath_pkl
            pass  # for
        pass  # if


    ## #NOTE 导入Pandas格式的实验结果数据转换为面板形式再导出
    if (sgv['transform_data']['导入Pandas格式的实验结果数据转换为面板形式再导出']):
        print("导入Pandas格式的实验结果数据转换为面板形式再导出")

        # 获取 agents 的 note 数据
        df_parameters = pd.read_pickle(sgv['folderpath_experiments_output_parameters'] / "parameters.pkl")  # 读取 parameters 数据表

        # # id=0-v=note-year=2007-density=0.10.pkl
        # with open(Path(sgv['folderpath_experiments_output_agents'] / "agents" / f"id={id_agent}-v=note-year={}-density={}.pkl"), 'r') as f:
        #     dict_worksStatesBeforeThisExperiments = json.load(f)
        #     pass
        # agents_data_paras = df_parameters[df_parameters['type'] == 'agents_data']  # 获取 agents 数据表

        folderpath_experiments_output_data_panel = Path(folderpath_experiments_output_data / "../../exp_output_data_panel").resolve()
        folderpath_experiments_output_data_panel.mkdir(parents=True, exist_ok=True)  # 创建面板数据文件夹

        if sgv['is_enable_multiprocessing_for_transform_output_data']:
            # #NOTE：并行处理，用 dask 延迟任务 #HACK 不建议用，因为速度没有显著提升

            # #NOTE：多进程并行处理
            num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
            works = []
            for para_01 in sgv['list_agents_data_filename_para_01']:
                if para_01 == "note":  # 如果是备注变量，则跳过。因为是作为辅助的，不需要转换
                    continue
                filepath_pkl = dict()
                for i, exp_id in enumerate(list_idsExp_TASK):
                    filepath_pkl[para_01] = dict_filepath_pkl[para_01][i]
                    filepath_note_pkl = dict_filepath_pkl['note'][i]
                    works.append((
                        exp_id,
                        filepath_pkl,
                        filepath_note_pkl,
                        sgv['columns_to_insert_into_panel_data'][para_01],
                        sgv['folderpath_experiments_output_log'],
                        folderpath_experiments_output_data_panel,
                        sgv['is_use_sqlite_to_manage_experiments'],
                    ))
                    pass  # for
                pass  # for

            # 并行运行作业
            with Pool(num_cores) as p:
                p.starmap(fun_导入Pandas格式的实验结果数据转换为面板形式再导出, works)
                pass  # with

        else:

            # #NOTE：串行处理
            for para_01 in sgv['list_agents_data_filename_para_01']:
                if para_01 == "note":  # 如果是备注变量，则跳过。因为是作为辅助的，不需要转换
                    continue
                filepath_pkl = dict()
                for i, exp_id in enumerate(list_idsExp_TASK):
                    filepath_pkl[para_01] = dict_filepath_pkl[para_01][i]
                    filepath_note_pkl = dict_filepath_pkl['note'][i]
                    print(f"para = {para_01}, exp_id = {exp_id}")
                    fun_导入Pandas格式的实验结果数据转换为面板形式再导出(
                        exp_id,
                        filepath_pkl,
                        filepath_note_pkl,
                        sgv['columns_to_insert_into_panel_data'][para_01],
                        sgv['folderpath_experiments_output_log'],
                        folderpath_experiments_output_data_panel,
                        sgv['is_use_sqlite_to_manage_experiments'],
                        sgv['list_table_for_explode'],
                    )
                    pass  # for
                pass  # for

            pass  # if

        pass  # if 导入Pandas格式的实验结果数据转换为面板形式再导出

    ## #NOTE 导入Pandas格式的实验结果数据合并为一个文件
    if (sgv['transform_data']['导入Pandas格式的实验结果数据合并为一个文件']):
        print("导入Pandas格式的实验结果数据合并为一个文件")

        ## #NOTE：用 Pandas 串行处理
        time_start = timeit.default_timer()  # 计时开始

        fun_导入Pandas格式的实验结果数据合并为一个文件(dict_filepath_pkl, list_idsExp_TASK)

        time_end = timeit.default_timer()  # 计时结束
        print(f"导入Pandas格式的实验结果数据合并为一个文件，耗时：{time_end - time_start} 秒")

        ## #NOTE：用 Dask 串行处理 #BUG 这个速度更慢，不采用
        #
        # time_start = timeit.default_timer()  # 计时开始
        #
        # BB_columns = pd.read_pickle(list_filepath_pkl_BB[0]).columns
        # IB_columns = pd.read_pickle(list_filepath_pkl_IB[0]).columns
        #
        # list_df_BB = []
        # list_df_IB = []
        # for i, exp_id in enumerate(list_idsExp_TASK):
        #     df_BB_origin = pd.read_pickle(list_filepath_pkl_BB[i])
        #     df_BB_origin['id_exp'] = int(exp_id)  # 添加子文件实验 id 列
        #     list_df_BB.append(dd.from_pandas(df_BB_origin, npartitions=10))
        #
        #     df_IB_origin = pd.read_pickle(list_filepath_pkl_IB[i])
        #     df_IB_origin['id_exp'] = int(exp_id)  # 添加子文件实验 id 列
        #     list_df_IB.append(dd.from_pandas(df_IB_origin, npartitions=10))
        #
        # # 一次性进行数据合并
        # df_BB_combined = dd.concat(list_df_BB, ignore_index=True)
        # df_IB_combined = dd.concat(list_df_IB, ignore_index=True)
        #
        # # 重置索引以创建总 id 列
        # df_BB_combined = df_BB_combined.reset_index().rename(columns={'index': 'id'})
        # df_IB_combined = df_IB_combined.reset_index().rename(columns={'index': 'id'})
        #
        # # 计算结果并将其转换回 pandas DataFrame
        # df_BB_combined = df_BB_combined.compute()
        # df_IB_combined = df_IB_combined.compute()
        #
        # time_end = timeit.default_timer()  # 计时结束
        # print(f"导入Pandas格式的实验结果数据合并为一个文件，耗时：{time_end - time_start} 秒")

        ## #NOTE 用 SQLite 处理 #BUG 这个不能处理一些数据类型
        # # 创建两个新的 SQLite 数据库
        # conn_BB = sqlite3.connect('combined_data_BB.db')
        # conn_IB = sqlite3.connect('combined_data_IB.db')
        #
        # time_start = timeit.default_timer()  # 计时开始
        #
        # list_idsExp_TASK = list_idsExp_TASK[0:100]  # DEBUG 仅用于测试性能
        #
        # for i, exp_id in enumerate(list_idsExp_TASK):
        #     # 读取 pickle 文件为 pandas DataFrame
        #     df_BB_origin = pd.read_pickle(list_filepath_pkl_BB[i])
        #     df_BB_origin['id_exp'] = int(exp_id)
        #
        #     df_IB_origin = pd.read_pickle(list_filepath_pkl_IB[i])
        #     df_IB_origin['id_exp'] = int(exp_id)
        #
        #     # 将 DataFrame 转换为 SQL 表并存储在 SQLite 数据库中
        #     df_BB_origin.to_sql(f'BB_{exp_id}', conn_BB, if_exists='replace', index=False)
        #     df_IB_origin.to_sql(f'IB_{exp_id}', conn_IB, if_exists='replace', index=False)
        #
        # # 使用 SQL 查询将所有的表合并为一个大表
        # query_BB = 'SELECT * FROM ' + ' UNION ALL SELECT * FROM '.join([f'BB_{exp_id}' for exp_id in list_idsExp_TASK])
        # query_IB = 'SELECT * FROM ' + ' UNION ALL SELECT * FROM '.join([f'IB_{exp_id}' for exp_id in list_idsExp_TASK])
        #
        # df_BB_combined = pd.read_sql_query(query_BB, conn_BB)
        # df_IB_combined = pd.read_sql_query(query_IB, conn_IB)
        #
        # # 重置索引以创建总 id 列
        # df_BB_combined.reset_index(inplace=True)
        # df_BB_combined.rename(columns={'index': 'id'}, inplace=True)
        #
        # df_IB_combined.reset_index(inplace=True)
        # df_IB_combined.rename(columns={'index': 'id'}, inplace=True)
        #
        # # 关闭数据库连接
        # conn_BB.close()
        # conn_IB.close()
        #
        # time_end = timeit.default_timer()  # 计时结束
        # print(f"导入Pandas格式的实验结果数据合并为一个文件，耗时：{time_end - time_start} 秒")

        pass  # if 导入Pandas格式的实验结果数据合并为一个文件

    if sgv['is_use_sqlite_to_manage_experiments']:

        ## 连接 SQLite 数据库，统计实验组之本次作业之完成情况
        conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
        c = conn.cursor()
        # 检查实验组作业完成状态
        c.execute("SELECT exp_id, status_预处理实验结果程序 FROM experiments")
        rows = c.fetchall()
        list_idsExp_DOING = []
        list_idsExp_DONE = []
        list_idsExp_RAW = []
        for row in rows:
            exp_id, status_预处理实验结果程序 = row
            if status_预处理实验结果程序 == "DOING":
                list_idsExp_DOING.append(exp_id)
            elif status_预处理实验结果程序 == "DONE":
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
                "完成率": len(list_idsExp_DONE) / num_files_BB,
                "中断率": len(list_idsExp_DOING) / num_files_BB,
            }, f)
            logging.info("实验组开始运行前，实验组作业完成状态情况如下:\n" + str({
                "之前运行中被中断的实验组 id": list_idsExp_DOING,
                "完成率": len(list_idsExp_DONE) / num_files_BB,
                "中断率": len(list_idsExp_DOING) / num_files_BB,
            }))
            pass  # with

        # # 绘制色带分布图，展示实验组 id 分布对应的实验组作业运行之后的作业完成状态信息。
        # ids = [row[0] for row in rows]  # 获取实验组 id
        # status_预处理实验结果程序_运行状态 = [row[1] for row in rows]  # 获取实验组作业状态
        # Tools.draw_color_band_after_experiments(ids, status_预处理实验结果程序_运行状态, Path(sgv['folderpath_experiments_output_log'], "color_band_distribution_after_预处理实验结果程序.png"))

        conn.close()  # 关闭数据库连接
        pass  # if


    pass  # main


def fun_导入Pandas格式的实验结果数据转换为面板形式再导出(exp_id: int, filepath_pkl: dict, filepath_note_pkl: dict, columns_to_insert_into_panel_data: dict, folderpath_experiments_output_log: Path, folderpath_experiments_output_data_panel: Path, is_use_sqlite_to_manage_experiments: bool, list_table_for_explode: list):
    """
    预处理单次实验之各实验结果数据

    Args:
        exp_id: int: 实验组 id
        filepath_pkl: dict: 实验结果数据文件路径
        filepath_note_pkl: Path: 实验结果数据之 note 文件路径
        columns_to_insert_into_panel_data: list: 需要插入到面板数据的字段。每一个元素是一个元组。第一个元素是需要插入的列名，第二个元素是需要插入的字段名的值，第三个元素是将新插入的列名移动到指定的列名的后面。
        folderpath_experiments_output_log: Path: 实验组输出日志文件夹路径
        folderpath_exp_output_data: Path: 面板数据文件夹路径
        is_use_sqlite_to_manage_experiments: bool: 是否使用 SQLite 数据库管理实验组
        list_table_for_explode: list: 需要展平的表格列表。每一个元素是一个字符串，表示需要展平的表格名。

    Returns:
        None
    """

    if is_use_sqlite_to_manage_experiments:
        record_work_state(exp_id, 'status_预处理实验结果程序', 'DOING', folderpath_experiments_output_log)  # 记录本次实验作业的完成状态为 "DOING"

    # 打开 exp_id 对应的 note 数据文件
    with open(filepath_note_pkl, 'rb') as f:
        series_note = pickle.load(f)  # 导入 note 数据
        pass  # with

    for para_01 in filepath_pkl.keys():
        # 根据文件名前缀判断数据类型  #BUG 这个存在风险，因为文件名前缀可能不遵循约定，后续扩展可能会有变化
        if not para_01.startswith('I'):  # 说明是 1D 的数据

            # 根据 filepath_pkl[para_01] 复制一个新文件，以免修改原始文件
            df_1D_original = pd.read_pickle(filepath_pkl[para_01])
            # filename_pkl_1D = Path(filepath_pkl[para_01]).name
            # filename_pkl_1D_panel = filename_pkl_1D.replace(f'{para_01}-', f'{para_01}_panel-')
            # #HACK 以上两行暂时用不到了，无用。
            filename_pkl_1D = Path(filepath_pkl[para_01]).stem
            filename_pkl_1D_panel = filename_pkl_1D + '-form=panel.pkl'
            filepath_pkl_1D_panal = (folderpath_experiments_output_data_panel / filename_pkl_1D_panel).resolve()  # 面板数据文件路径
            filepath_pkl_1D_panal.parent.mkdir(parents=True, exist_ok=True)
            df_1D_original.to_pickle(Path(filepath_pkl_1D_panal))  # 导出为 pkl 格式
            df_1D_original = pd.read_pickle(filepath_pkl_1D_panal)  # 重新读取 pkl 文件，对该文件直接修改

            if para_01 in list_table_for_explode:
                is_value_a_vector = True
            else:
                is_value_a_vector = False

            if is_value_a_vector:
                num_size = df_1D_original[df_1D_original.columns[-1]][0].shape[0]  # 获取个体数 #HACK 如果这里报错，那么最常见的可能是因为数据文件内容是空的。需要查看运行程序是否有配置因此正确导出数据
            else:
                num_size = df_1D_original[df_1D_original.columns[-1]][0].size

            df_1D = df_1D_original.map(lambda x: x.flatten() if hasattr(x, 'flatten') else x)  # 压平二维数组

            # 添加 note 里面的值作为整列
            for v in columns_to_insert_into_panel_data if columns_to_insert_into_panel_data is not None else []:
                df_1D[v[0]] = pd.Series([series_note[v[1]]] * len(df_1D))
                col = df_1D.pop(v[0])
                df_1D.insert(df_1D.columns.get_loc(v[2]) + 1, v[0], col)

            if is_value_a_vector:
                ## 转换数据格式为 numpy 字符串格式
                list_columns_for_transform_datatype = [
                    v for i, v in enumerate(df_1D.columns) if (
                            df_1D[v].dtype == np.dtype('object')
                            and type(df_1D[v][0]) == str
                    )
                ]
                for i in range(df_1D.__len__()):
                    df_1D.at[i, list_columns_for_transform_datatype[0]] = np.str_(df_1D[list_columns_for_transform_datatype[0]][i])
                    pass  # for

                ## 展平为面板形式
                list_columns_for_explode = [
                    v for i, v in enumerate(df_1D.columns) if (
                            df_1D[v].dtype == np.dtype('object')
                            and df_1D[v][0].size == num_size
                    )
                ]  # 获取需要展平的列

                df_1D_panel = df_1D.explode('id_agent')  # 只展开 'id_agent' 列
                for col in list_columns_for_explode:  # 遍历其他需要展开的列，并将它们的元素展开以匹配 'id_agent' 列的行数
                    if col != 'id_agent':
                        # df_1D_panel[col] = df_BB.apply(lambda row: pd.Series(row[col]), axis=1).stack(dropna=False).reset_index(level=1, drop=True)
                        df_1D_panel[col] = df_1D.apply(lambda row: pd.Series(row[col]), axis=1).stack(dropna=False).values
                        pass  # if
                    pass  # for
            else:
                df_1D_panel = df_1D
                pass  # if
            df_1D_panel = df_1D_panel.reset_index(drop=True)  # 重置索引

            df_1D_panel.insert(0, 'id', range(len(df_1D_panel)))  # 添加id列
            df_1D_panel.insert(1, 'id_data', np.repeat(range(len(df_1D_panel) // num_size), num_size))  # 添加id_data列

            df_1D_panel = df_1D_panel.reset_index(drop=True)  # 重置索引

            ## 导出为 pkl 格式，保存为 csv、xlsx 格式，然后对 xlsx 格式的文件做进一步处理 #NOTE 有需要再启用以下代码
            df_1D_panel.to_pickle(Path(filepath_pkl_1D_panal))  # 导出为 pkl 格式
            df_1D_panel.to_csv(Path(str(filepath_pkl_1D_panal).split('.')[0] + '.csv'), index=False)  # 导出为 csv 格式；
            with pd.ExcelWriter(Path(str(filepath_pkl_1D_panal).split('.')[0] + '.xlsx')) as writer:  # 导出为 xlsx 格式
                df_1D_panel.to_excel(writer, sheet_name=f'{para_01}_panel')
                pass  # with

            ## 重新读取 xlsx 格式然后格式化
            ### 需要调整列边距的列名
            columnsName_adjust = [
                'id',
                'id_data',
                'step',
                'turn',
                'phase',
                'id_agent',
            ]

            wb_1D_panel = load_workbook(Path(str(filepath_pkl_1D_panal).split('.')[0] + '.xlsx'))  # 使用 openpyxl 打开面板形式的 Excel 文件
            sheet_1D_panel = wb_1D_panel.active

            sheet_1D_panel.freeze_panes = "J2"  # 冻结窗格

            col_indices = [df_1D_panel.columns.get_loc(col_name) + 1 for col_name in columnsName_adjust]  # 调整列宽
            for col_index in col_indices:
                col_letter = get_column_letter(col_index)
                sheet_1D_panel.column_dimensions[col_letter].width = 5

            # 对于列 'id_data'，其单元格的值每间隔指定的行，对应的单元格背景色就变色。改变的颜色按照无色、浅灰色交替循环。
            fill = PatternFill(start_color="EEEEEE", end_color="EEEEEE", fill_type="solid")
            for i, row in enumerate(sheet_1D_panel.iter_rows(min_row=2)):  # 跳过第一行表头
                if i % (2 * num_size) < num_size:  # 每间隔指定的行填充一次背景色 #BUG 如果设置的银行数量不正确，那么绘制不符合预期。
                    for cell in row:
                        cell.fill = fill  # 将该行的背景色设置为浅灰色

            # for col in columns_states:  # 遍历每一列
            #     col_index = df_1D_panel.columns.get_loc(col) + 1
            #     col_letter = get_column_letter(col_index)
            #     rng = sheet_1D_panel[col_letter]
            #     for cell in rng:  # 遍历每一个单元格
            #         if cell.value == True:
            #             cell.fill = PatternFill(start_color="FFBBBB", end_color="FFBBBB", fill_type="solid")  # 根据单元格的值设置背景颜色

            wb_1D_panel.save(Path(str(filepath_pkl_1D_panal).split('.')[0] + '.xlsx'))  # 保存 Excel 文件

        else:  # 说明是 2D 的数据

            # 根据 filepath_pkl[para_01] 复制一个新文件，以免修改原始文件
            # filename_pkl_2D = Path(filepath_pkl[para_01]).name
            # filename_pkl_2D_panel = filename_pkl_2D.replace(f'{para_01}-', f'{para_01}_panel-')
            # #HACK 以上两行暂时用不到了，无用。
            filename_pkl_2D = Path(filepath_pkl[para_01]).stem
            filename_pkl_2D_panel = filename_pkl_2D + '-form=panel.pkl'
            df_2D_original = pd.read_pickle(filepath_pkl[para_01])
            filepath_pkl_2D_panal = (folderpath_experiments_output_data_panel / filename_pkl_2D_panel).resolve()  # 面板数据文件路径
            df_2D_original.to_pickle(Path(filepath_pkl_2D_panal))  # 导出为 pkl 格式
            df_2D_original = pd.read_pickle(filepath_pkl_2D_panal)  # 重新读取 pkl 文件，对该文件直接修改

            (num_row, num_col) = df_2D_original['id_agent'][0].shape
            df_IB = deepcopy(df_2D_original)

            ## 转换数据格式为numpy字符串格式
            list_columns_for_transform_datatype = [
                v for i, v in enumerate(df_IB.columns) if (
                        df_IB[v].dtype == np.dtype('object')
                        and type(df_IB[v][0]) == str
                )
            ]
            for i in range(df_IB.__len__()):
                df_IB.at[i, list_columns_for_transform_datatype[0]] = np.str_(df_IB[list_columns_for_transform_datatype[0]][i])

            ## 转换信息列表为矩阵形式，插入数据框  #HACK 能否用现成的功能函数代替？
            list_columns_for_transform = [
                v for i, v in enumerate(df_IB.columns) if (
                        df_IB[v].dtype == np.dtype('object')
                        and df_IB[v][0].dtype == np.dtype('object')
                )
            ]
            for v1 in list_columns_for_transform:  # HACK 这个功能似乎无用
                for i2 in range(df_IB[v1].size):
                    m = np.full((num_row, num_col), False)
                    if df_IB.loc[i2, v1] is []:
                        df_IB.loc[i2, v1] = np.nan
                        continue
                    for i3, v3 in enumerate(df_IB.loc[i2, v1]):
                        if v3 is []:
                            m[i3, :] = False
                            continue
                            pass  # if
                        for i4 in v3:
                            if i4 in v3:
                                m[i3, i4] = True
                            else:
                                m[i3, i4] = False
                                pass  # if
                            pass  # for
                        pass  # for
                    df_IB[v1][i2] = m  # 赋值矩阵给数据框之元素，于数据框之相应的位置
                    pass  # for
                pass  # for

            ## 生成agent矩阵之坐标，以矩阵形式，插入数据框
            row_coord, col_coord = np.mgrid[0:num_row:1, 0:num_col:1]
            df_IB.insert(loc=df_IB.columns.get_loc('id_agent') + 1, column="col", value=np.dtype('object'))
            for i, _ in enumerate(df_IB.col):
                df_IB.at[i, 'col'] = col_coord.astype('int16')
            df_IB.insert(loc=df_IB.columns.get_loc('id_agent') + 1, column="row", value=np.dtype('object'))
            for i, _ in enumerate(df_IB.row):
                df_IB.at[i, 'row'] = row_coord.astype('int16')

                ## 展平为面板形式
            list_columns_for_explode = [
                v for i, v in enumerate(df_IB.columns) if (
                        df_IB[v].dtype == np.dtype('object')
                        and df_IB[v][0].size == (num_row * num_col)
                )
            ]  # 获取需要展平的列

            df_2D_panel = (df_IB.explode('id_agent')).explode('id_agent')  # 只展开 'id_agent' 列，对于二维数组需要展开两次
            # df_2D_panel = df_IB['id_agent'].apply(lambda x: pd.Series(x.flatten())).stack().reset_index(level=1, drop=True).to_frame('id_agent')  # 只展开 'id_agent' 列，对于二维数组需要展开两次
            for col in list_columns_for_explode:  # 遍历其他需要展开的列，并将它们的元素展开以匹配 'id_agent' 列的行数
                if col != 'id_agent':
                    # df_2D_panel[col] = df_IB[col].apply(lambda x: pd.Series(x.flatten())).stack().reset_index(level=0, drop=True).reset_index(drop=True)  # 对于二维数组需要展开两次
                    # df_2D_panel[col] = df_IB[col].apply(lambda x: pd.Series(x.flatten())).stack(dropna=False).reset_index(level=1, drop=True)  # 对于二维数组需要展开两次
                    df_2D_panel[col] = df_IB[col].apply(lambda x: pd.Series(x.flatten())).stack(dropna=False).values  # 对于二维数组需要展开两次
                    pass  # if
                pass  # for
            df_2D_panel = df_2D_panel.reset_index(drop=True)  # 重置索引

            df_2D_panel.insert(0, 'id', range(len(df_2D_panel)))  # 添加id列
            df_2D_panel.insert(1, 'id_data', np.repeat(range(len(df_2D_panel) // (num_row * num_col)), (num_row * num_col)))  # 添加id_data列

            df_2D_panel = df_2D_panel.reset_index(drop=True)  # 重置索引

            ## 导出为 pkl 格式，保存为 csv、xlsx 格式，然后对 xlsx 格式的文件做进一步处理 #NOTE 有需要再启用以下代码
            df_2D_panel.to_pickle(Path(filepath_pkl_2D_panal))  # 导出为 pkl 格式
            df_2D_panel.to_csv(Path(Path(str(filepath_pkl_2D_panal).split('.')[0] + '.csv')), index=False)  # 导出为 csv 格式；
            with pd.ExcelWriter(Path(str(filepath_pkl_2D_panal).split('.')[0] + '.xlsx')) as writer:  # 导出为 xlsx 格式
                df_2D_panel.to_excel(writer, sheet_name=f'{para_01}_panel')
                pass  # with

            ## 重新读取 xlsx 格式然后格式化
            ### 需要调整列边距的列名
            columnsName_adjust = [
                'id',
                'id_data',
                'process_name',
                'step',
                'turn',
                'phase',
                'id_agent',
                'row',
                'col',
            ]

            wb_2D_panel = load_workbook(Path(str(filepath_pkl_2D_panal).split('.')[0] + '.xlsx'))  # 使用 openpyxl 打开面板形式的 Excel 文件
            sheet_2D_panel = wb_2D_panel.active

            sheet_2D_panel.freeze_panes = "K2"  # 冻结窗格

            col_indices = [df_2D_panel.columns.get_loc(col_name) + 1 for col_name in columnsName_adjust]  # 调整列宽
            for col_index in col_indices:
                col_letter = get_column_letter(col_index)
                sheet_2D_panel.column_dimensions[col_letter].width = 5

            # 对于列 'id_data'，其单元格的值每间隔指定的行，对应的单元格背景色就变色。改变的颜色按照无色、浅灰色交替循环。
            fill = PatternFill(start_color="EEEEEE", end_color="EEEEEE", fill_type="solid")
            for i, row in enumerate(sheet_2D_panel.iter_rows(min_row=2)):  # 跳过第一行表头
                if i % (2 * (num_row * num_col)) < (num_row * num_col):  # 每间隔指定的行填充一次背景色 #BUG 如果设置的银行数量不正确，那么绘制不符合预期。
                    for cell in row:
                        cell.fill = fill  # 将该行的背景色设置为浅灰色

            # for col in columns_states:  # 遍历每一列
            #     col_index = df_1D_panel.columns.get_loc(col) + 1
            #     col_letter = get_column_letter(col_index)
            #     rng = sheet_2D_panel[col_letter]
            #     for cell in rng:  # 遍历每一个单元格
            #         if cell.value == True:
            #             cell.fill = PatternFill(start_color="FFBBBB", end_color="FFBBBB", fill_type="solid")  # 根据单元格的值设置背景颜色

            wb_2D_panel.save(Path(str(filepath_pkl_2D_panal).split('.')[0] + '.xlsx'))  # 保存 Excel 文件

            pass  # if

        pass  # for

    if is_use_sqlite_to_manage_experiments:
        record_work_state(exp_id, 'status_预处理实验结果程序', 'DONE', folderpath_experiments_output_log)  # 记录本次实验作业的完成状态为 "DONE"

    pass  # function


def fun_导入Pandas格式的实验结果数据合并为一个文件(list_filepath_pkl_BB, list_filepath_pkl_IB, list_idsExp_TASK):
    """
    导入Pandas格式的实验结果数据合并为一个文件  #FIXME 未适配除了 BB、IB 之外的各种 agents。暂时无法使用

    Args:
        list_filepath_pkl_BB: List[Path]: BB 实验结果数据文件路径列表
        list_filepath_pkl_IB: List[Path]: IB 实验结果数据文件路径列表
        list_idsExp_TASK: List[int]: 实验组 id 列表

    Returns:
        df_BB_combined: DataFrame: 合并后的 BB 实验结果数据
        df_IB_combined: DataFrame: 合并后的 IB 实验结果数据
    """

    BB_columns = pd.read_pickle(list_filepath_pkl_BB[0]).columns
    IB_columns = pd.read_pickle(list_filepath_pkl_IB[0]).columns

    df_BB_combined = pd.DataFrame(columns=['id_exp'] + list(BB_columns))
    df_IB_combined = pd.DataFrame(columns=['id_exp'] + list(IB_columns))
    for i, exp_id in enumerate(list_idsExp_TASK):
        df_BB_origin = pd.read_pickle(list_filepath_pkl_BB[i])
        df_BB_origin['id_exp'] = int(exp_id)
        df_BB_combined = pd.concat([df_BB_combined, df_BB_origin], ignore_index=True)
        df_IB_origin = pd.read_pickle(list_filepath_pkl_IB[i])
        df_IB_origin['id_exp'] = int(exp_id)
        df_IB_combined = pd.concat([df_IB_combined, df_IB_origin], ignore_index=True)

    # 重置索引以创建总 id 列
    df_BB_combined.reset_index(inplace=True)
    df_BB_combined.rename(columns={'index': 'id'}, inplace=True)

    df_IB_combined.reset_index(inplace=True)
    df_IB_combined.rename(columns={'index': 'id'}, inplace=True)

    return df_BB_combined, df_IB_combined


# def fun_导入Pandas格式的实验结果数据合并为一个文件(exp_id: int, filepath_pkl_BB: Path, filepath_pkl_IB: Path, folderpath_experiments_output_log: Path, folderpath_exp_output_data: Path):
#     """
#     预处理单次实验之各实验结果数据
#
#     Args:
#         exp_id: int: 实验组 id
#         filepath_pkl_BB: Path: BB 实验结果数据文件路径
#         filepath_pkl_IB: Path: IB 实验结果数据文件路径
#         folderpath_experiments_output_log: Path: 实验组输出日志文件夹路径
#         folderpath_exp_output_data: Path: 面板数据文件夹路径
#
#     Returns:
#         None
#     """
#     pass  # function

if __name__ == '__main__':
    # 从命令行参数获取配置字典
    sgv_base64 = sys.argv[1]
    sgv_pkl = base64.b64decode(sgv_base64)
    sgv = pickle.loads(sgv_pkl)

    main(sgv)
