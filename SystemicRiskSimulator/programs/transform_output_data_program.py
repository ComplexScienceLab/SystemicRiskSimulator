"""
预处理实验结果数据

#NOTE 强烈建议用串行处理模式，暨 is_enable_multiprocessing = False。因为这样更安全、速度还更快一些。
"""

# %% [markdown] # NOTE 导入Pandas格式的实验结果数据，然后转换为面板形式的数据，导出PKL、CSV、xlsx 格式数据。

# %%

from SystemicRiskSimulator.tools.visualization_tools import generate_one_interbank_matrix_heatmaps_data_info, draw_one_interbank_matrix_heatmaps, generate_one_interbank_graph_data_info, draw_one_interbank_flow_graph, generate_one_bank_accounts_data, draw_one_bank_BalanceSheet, merged_and_bind_figs_to_a_pdf_file

from dask import delayed, compute
import dask.dataframe as dd
from dask.diagnostics import ProgressBar

from SystemicRiskSimulator.external_packages import platform, Path, sqlite3, re, glob, pd, np, deepcopy, sys, pickle, base64, Pool, multiprocessing, warnings, logging, json, sqlite3
from multiprocessing import Lock

from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv
from SystemicRiskSimulator.tools.logging_tools import record_work_state

## NOTE 导入包

if sgv['need_transformData']:
    from openpyxl import load_workbook
    from openpyxl.styles import PatternFill
    from openpyxl.utils import get_column_letter

# 创建一个全局锁
lock = Lock()


def main():
    # 从命令行参数获取配置字典
    sgv_base64 = sys.argv[1]
    sgv_pkl = base64.b64decode(sgv_base64)
    sgv = pickle.loads(sgv_pkl)

    if sgv['is_ignore_warning']:
        warnings.filterwarnings("ignore")  # 忽略警告

    # %% 初始化

    # from SystemicRiskSimulator.tools.tools import Tools
    # from SystemicRiskSimulator.external_packages import Path
    #
    # config = dict()
    # config['folderpath_config'] = r"Samples/libraries/configs_library/config_sample"  # 配置项文件夹路径
    # config['foldername_simulator'] = r"SystemicRiskSimulator"  # 模拟器所在工程文件夹名称
    # config['folderpath_realpath_simulator'] = r"../"  # 模拟器所在工程文件夹相对本实验项目文件夹之相对路径
    # config['is_auto_confirmation'] = True  # 是否自动确认一些比较危险的操作例如删除、移动、复制文件等。默认 False；
    #
    # ## 获取项目路径、模拟器工具路径
    # config['folderpath_simulator'] = Tools.get_project_rootpath(config['foldername_simulator'], config['folderpath_realpath_simulator'])
    # config['folderpath_project'] = Tools.get_project_rootpath()
    # # 如果 settings 之 config 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
    # Tools._delete_and_recreate_folder(Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=config['is_auto_confirmation'])
    # Tools._copy_files_from_other_folders(Path(config['folderpath_project'], config['folderpath_config']), Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=config['is_auto_confirmation'])
    # from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

    from SystemicRiskSimulator.tools.tools import Tools
    list_transform_output_data_packages = ['openpyxl']  # 所需的第三方工具包 #NOTE 如果需要添加新的包，请在此处添加
    Tools._check_and_install_packages(list_transform_output_data_packages)  # 安装所需的第三方工具包。#BUG 如果没有安装成功，请手动安装。

    # %% [markdown] 预处理数据

    # %%
    print("执行：")

    if (sgv['transform_data']['导入Pandas格式的实验结果数据转换为面板形式再导出']):
        print("导入Pandas格式的实验结果数据转换为面板形式再导出")

        # with open(Path(sgv['folderpath_parameters'], "parameters.pkl"), 'rb') as f:
        #     parameters_works = pd.read_pickle(f)

        list_filepath_pkl_BB = list(sgv['folderpath_experiments_output_data'].glob('BB_exp*.pkl'))  # 获取实验组输出数据pkl格式之BB数据之文件列表

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
        c.execute("SELECT id, status_预处理实验结果程序 FROM experiments")
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
        list_idsExp_PLAN = sgv['list_idsExperiment_to_run'] if sgv['list_idsExperiment_to_run'] is not None else list(range(1, len(list_filepath_pkl_BB) + 1))
        list_idsExp_TASK = [i for i in list_idsExp_PLAN if i not in list_idsExp_DONE]
        # 保存实验组作业完成状态信息
        with open(Path(sgv['folderpath_experiments_output_log'], "outputlog_worksStatesBeforeThisExperiments.json"), 'w') as f:
            json.dump({
                "计划运行的实验组 id": list_idsExp_TASK,
                "未运行过的实验组 id": list_idsExp_RAW,
                "之前运行中被中断的实验组 id": list_idsExp_DOING,
                "已完成的实验组 id": list_idsExp_DONE,
                "完成率": len(list_idsExp_DONE) / len(list_filepath_pkl_BB),
                "中断率": len(list_idsExp_DOING) / len(list_filepath_pkl_BB),
            }, f)
            logging.info("实验组开始运行前，实验组作业完成状态情况如下:\n" + str({
                "之前运行中被中断的实验组 id": list_idsExp_DOING,
                "完成率": len(list_idsExp_DONE) / len(list_filepath_pkl_BB),
                "中断率": len(list_idsExp_DOING) / len(list_filepath_pkl_BB),
            }))
        # # 绘制色带分布图，展示实验组 id 分布对应的实验组作业运行之前的作业完成状态信息。
        # ids = [row[0] for row in rows]  # 获取实验组 id
        # status_预处理实验结果程序_运行状态 = [row[1] for row in rows]  # 获取实验组作业状态
        # Tools.draw_color_band_before_experiments(ids, status_预处理实验结果程序_运行状态, list_idsExp_PLAN, list_idsExp_TASK, Path(sgv['folderpath_experiments_output_log'], "color_band_distribution_before_预处理实验结果程序.png"))
        conn.close()

        ## 预处理 BB 实验结果数据
        if sgv['is_enable_multiprocessing']:
            # #NOTE：并行处理，用 dask 延迟任务 #DEBUG
            # transform_BB_exp_files_delayed = delayed(transform_BB_exp_files)
            #
            # tasks_BB = []
            # for i, filepath_pkl_BB in enumerate(list_filepath_pkl_BB):
            #     exp_id = i + 1
            #     print(f"BB exp_id = {exp_id}")
            #     task_BB = transform_BB_exp_files_delayed(exp_id, filepath_pkl_BB, sgv['folderpath_experiments_output_log'], sgv['folderpath_experiments_output_data'])
            #     tasks_BB.append(task_BB)
            #     pass  # for
            #
            # with ProgressBar():
            #     results_BB = compute(*tasks_BB)

            # #NOTE：多进程并行处理 #DEBUG
            num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
            works = []
            for i, filepath_pkl_BB in enumerate(list_filepath_pkl_BB):
                exp_id = i + 1
                # print(f"BB exp_id = {exp_id}")
                works.append((exp_id, filepath_pkl_BB, sgv['folderpath_experiments_output_log'], sgv['folderpath_experiments_output_data']))
                pass  # for

            # 并行运行作业
            with Pool(num_cores) as p:
                p.starmap(transform_BB_exp_files, works)
                pass  # with

        else:

            # #NOTE：串行处理 #DEBUG
            for i, filepath_pkl_BB in enumerate(list_filepath_pkl_BB):
                exp_id = i + 1
                # print(f"BB exp_id = {exp_id}")
                transform_BB_exp_files(exp_id, filepath_pkl_BB, sgv['folderpath_experiments_output_log'], sgv['folderpath_experiments_output_data'])
                pass  # for

            pass  # if

        list_filepath_pkl_IB = list(sgv['folderpath_experiments_output_data'].glob('IB_exp*.pkl'))  # 获取实验组输出数据pkl格式之IB数据之文件列表
        if sgv['is_enable_multiprocessing']:

            # #NOTE：并行处理，用 dask 延迟任务 #DEBUG
            # transform_IB_exp_files_delayed = delayed(transform_IB_exp_files)
            # tasks_IB = []
            # for i, filepath_pkl_IB in enumerate(list_filepath_pkl_IB):
            #     exp_id = i + 1
            #     print(f"IB exp_id = {exp_id}")
            #     task_IB = transform_IB_exp_files_delayed(exp_id, filepath_pkl_IB, sgv['folderpath_experiments_output_log'], sgv['folderpath_experiments_output_data'])
            #     tasks_IB.append(task_IB)
            #     pass  # for
            # with ProgressBar():
            #     results_IB = compute(*tasks_IB)

            # #NOTE：多进程并行处理 #DEBUG
            num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
            works = []
            for i, filepath_pkl_IB in enumerate(list_filepath_pkl_IB):
                exp_id = i + 1
                # print(f"IB exp_id = {exp_id}")
                works.append((exp_id, filepath_pkl_IB, sgv['folderpath_experiments_output_log'], sgv['folderpath_experiments_output_data']))
                pass  # for

            # 并行运行作业
            with Pool(num_cores) as p:
                p.starmap(transform_IB_exp_files, works)
                pass  # with

        else:
            # #NOTE：串行处理  #DEBUG
            for i, filepath_pkl_IB in enumerate(list_filepath_pkl_IB):
                exp_id = i + 1
                # print(f"IB exp_id = {exp_id}")
                transform_IB_exp_files(exp_id, filepath_pkl_IB, sgv['folderpath_experiments_output_log'], sgv['folderpath_experiments_output_data'])
                pass  # for

            pass  # if

        pass  # if 导入Pandas格式的实验结果数据转换为面板形式再导出

    ## 连接 SQLite 数据库，统计实验组之本次作业之完成情况
    conn = sqlite3.connect(Path(sgv['folderpath_experiments_output_log'], "experiments_works_status.db"))
    c = conn.cursor()
    # 检查实验组作业完成状态
    c.execute("SELECT id, status_预处理实验结果程序 FROM experiments")
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
            "完成率": len(list_idsExp_DONE) / len(list_filepath_pkl_BB),
            "中断率": len(list_idsExp_DOING) / len(list_filepath_pkl_BB),
        }, f)
        logging.info("实验组开始运行前，实验组作业完成状态情况如下:\n" + str({
            "之前运行中被中断的实验组 id": list_idsExp_DOING,
            "完成率": len(list_idsExp_DONE) / len(list_filepath_pkl_BB),
            "中断率": len(list_idsExp_DOING) / len(list_filepath_pkl_BB),
        }))
        pass  # with

    # # 绘制色带分布图，展示实验组 id 分布对应的实验组作业运行之后的作业完成状态信息。
    # ids = [row[0] for row in rows]  # 获取实验组 id
    # status_预处理实验结果程序_运行状态 = [row[1] for row in rows]  # 获取实验组作业状态
    # Tools.draw_color_band_after_experiments(ids, status_预处理实验结果程序_运行状态, Path(sgv['folderpath_experiments_output_log'], "color_band_distribution_after_预处理实验结果程序.png"))

    conn.close()  # 关闭数据库连接

    pass  # main


def transform_BB_exp_files(exp_id: int, filepath_pkl_BB: Path, folderpath_experiments_output_log: Path, folderpath_exp_output_data: Path):
    """
    预处理 BB 实验结果数据

    Args:
        exp_id: int: 实验组 id
        filepath_pkl_BB: Path: BB 实验结果数据文件路径
        folderpath_experiments_output_log: Path: 实验组输出日志文件夹路径
        folderpath_exp_output_data: Path: 面板数据文件夹路径

    Returns:
        None
    """

    record_work_state(exp_id, 'status_预处理实验结果程序', 'DOING', folderpath_experiments_output_log)  # 记录本次实验作业的完成状态为 "DOING"

    df_BB_original = pd.read_pickle(filepath_pkl_BB)
    num_agent = df_BB_original['id_agent'][0].shape[0]  # 获取个体数 #BUG  如果这里报错，那么最常见的可能是因为数据文件内容是空的。需要查看运行程序是否有配置因此正确导出数据
    df_BB = df_BB_original.map(lambda x: x.flatten() if hasattr(x, 'flatten') else x)  # 压平二维数组

    ## 转换数据格式为numpy字符串格式
    list_columns_for_transform_datatype = [
        v for i, v in enumerate(df_BB.columns) if (
                df_BB[v].dtype == np.dtype('object')
                and type(df_BB[v][0]) == str
        )
    ]
    for i in range(df_BB.__len__()):
        df_BB.at[i, list_columns_for_transform_datatype[0]] = np.str_(df_BB[list_columns_for_transform_datatype[0]][i])  # BUG Pandas包警告

    ## 展平为面板形式
    list_columns_for_explode = [
        v for i, v in enumerate(df_BB.columns) if (
                df_BB[v].dtype == np.dtype('object')
                and df_BB[v][0].size == num_agent
        )
    ]  # 获取需要展平的列

    df_BB_panel = df_BB.explode('id_agent')  # 只展开 'id_agent' 列
    for col in list_columns_for_explode:  # 遍历其他需要展开的列，并将它们的元素展开以匹配 'id_agent' 列的行数
        if col != 'id_agent':
            df_BB_panel[col] = df_BB.apply(lambda row: pd.Series(row[col]), axis=1).stack().reset_index(level=1, drop=True)
            pass  # if
        pass  # for
    df_BB_panel = df_BB_panel.reset_index(drop=True)  # 重置索引

    df_BB_panel.insert(0, 'id', range(len(df_BB_panel)))  # 添加id列
    df_BB_panel.insert(1, 'id_data', np.repeat(range(len(df_BB_panel) // num_agent), num_agent))  # 添加id_data列

    df_BB_panel = df_BB_panel.reset_index(drop=True)  # 重置索引

    filename_pkl_BB = Path(filepath_pkl_BB).name
    filename_pkl_BB_panel = filename_pkl_BB.replace('BB_', 'BB_panel_')
    filepath_pkl_BB_panal = Path(folderpath_exp_output_data, filename_pkl_BB_panel)  # 面板数据文件路径
    df_BB_panel.to_pickle(Path(filepath_pkl_BB_panal))  # 导出为 pkl 格式

    ## 保存为 csv、xlsx 格式，然后对 xlsx 格式的文件做进一步处理 #NOTE 有需要再启用以下代码
    # df_BB_panel.to_csv(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.csv'), index=False)  # 导出为 csv 格式；
    # with pd.ExcelWriter(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.xlsx')) as writer:  # 导出为 xlsx 格式
    #     df_BB_panel.to_excel(writer, sheet_name='BB_panel')
    #     pass  # with
    #
    # ## 重新读取 xlsx 格式然后格式化
    # ### 需要调整列边距的列名
    # columnsName_adjust = [
    #     'id',
    #     'id_data',
    #     'step',
    #     'turn',
    #     'phase',
    #     'id_agent',
    # ]
    #
    # wb_BB_panel = load_workbook(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.xlsx'))  # 使用 openpyxl 打开面板形式的 Excel 文件
    # sheet_BB_panel = wb_BB_panel.active
    #
    # sheet_BB_panel.freeze_panes = "J2"  # 冻结窗格
    #
    # col_indices = [df_BB_panel.columns.get_loc(col_name) + 1 for col_name in columnsName_adjust]  # 调整列宽
    # for col_index in col_indices:
    #     col_letter = get_column_letter(col_index)
    #     sheet_BB_panel.column_dimensions[col_letter].width = 5
    #
    # # 对于列 'id_data'，其单元格的值每间隔指定的行，对应的单元格背景色就变色。改变的颜色按照无色、浅灰色交替循环。
    # fill = PatternFill(start_color="EEEEEE", end_color="EEEEEE", fill_type="solid")
    # for i, row in enumerate(sheet_BB_panel.iter_rows(min_row=2)):  # 跳过第一行表头
    #     if i % (2 * num_agent) < num_agent:  # 每间隔指定的行填充一次背景色 #BUG 如果设置的银行数量不正确，那么绘制不符合预期。
    #         for cell in row:
    #             cell.fill = fill  # 将该行的背景色设置为浅灰色
    #
    # # for col in columns_states:  # 遍历每一列
    # #     col_index = df_BB_panel.columns.get_loc(col) + 1
    # #     col_letter = get_column_letter(col_index)
    # #     rng = sheet_BB_panel[col_letter]
    # #     for cell in rng:  # 遍历每一个单元格
    # #         if cell.value == True:
    # #             cell.fill = PatternFill(start_color="FFBBBB", end_color="FFBBBB", fill_type="solid")  # 根据单元格的值设置背景颜色
    #
    # wb_BB_panel.save(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.xlsx'))  # 保存 Excel 文件

    record_work_state(exp_id, 'status_预处理实验结果程序', 'DONE', folderpath_experiments_output_log)  # 记录本次实验作业的完成状态为 "DONE"

    pass  # function


def transform_IB_exp_files(exp_id: int, filepath_pkl_IB: Path, folderpath_experiments_output_log: Path, folderpath_exp_output_data: Path):
    """
    预处理 IB 实验结果数据

    Args:
        exp_id: int: 实验组 id
        filepath_pkl_IB: Path: IB 实验结果数据文件路径
        folderpath_experiments_output_log: Path: 实验组输出日志文件夹路径
        folderpath_exp_output_data: Path: 面板数据文件夹路径

    Returns:
        None
    """

    record_work_state(exp_id, 'status_预处理实验结果程序', 'DOING', folderpath_experiments_output_log)  # 记录本次实验作业的完成状态为 "DOING"

    df_IB_original = pd.read_pickle(filepath_pkl_IB)
    num_agent = df_IB_original['id_agent'][0].shape[0]
    df_IB = deepcopy(df_IB_original)

    ## 转换数据格式为numpy字符串格式
    list_columns_for_transform_datatype = [
        v for i, v in enumerate(df_IB.columns) if (
                df_IB[v].dtype == np.dtype('object')
                and type(df_IB[v][0]) == str
        )
    ]
    for i in range(df_IB.__len__()):
        df_IB.at[i, list_columns_for_transform_datatype[0]] = np.str_(df_IB[list_columns_for_transform_datatype[0]][i])  # BUG Pandas包警告

    ## 转换信息列表为矩阵形式，插入数据框  #HACK 能否用现成的功能函数代替？
    list_columns_for_transform = [
        v for i, v in enumerate(df_IB.columns) if (
                df_IB[v].dtype == np.dtype('object')
                and df_IB[v][0].dtype == np.dtype('object')
        )
    ]
    for v1 in list_columns_for_transform:  # HACK 这个功能似乎无用
        for i2 in range(df_IB[v1].size):
            m = np.full((num_agent, num_agent), False)
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
    row_coord, col_coord = np.mgrid[0:num_agent:1, 0:num_agent:1]
    df_IB.insert(loc=df_IB.columns.get_loc('id_agent') + 1, column="col", value=np.dtype('object'))
    for i, _ in enumerate(df_IB.col):
        df_IB.at[i, 'col'] = col_coord.astype('int16')
    df_IB.insert(loc=df_IB.columns.get_loc('id_agent') + 1, column="row", value=np.dtype('object'))
    for i, _ in enumerate(df_IB.row):
        df_IB.at[i, 'row'] = row_coord.astype('int16')  # BUG Pandas包警告

    ## 展平为面板形式
    list_columns_for_explode = [
        v for i, v in enumerate(df_IB.columns) if (
                df_IB[v].dtype == np.dtype('object')
                and df_IB[v][0].size == num_agent ** 2
        )
    ]  # 获取需要展平的列

    df_IB_panel = (df_IB.explode('id_agent')).explode('id_agent')  # 只展开 'id_agent' 列，对于二维数组需要展开两次
    # df_IB_panel = df_IB['id_agent'].apply(lambda x: pd.Series(x.flatten())).stack().reset_index(level=1, drop=True).to_frame('id_agent')  # 只展开 'id_agent' 列，对于二维数组需要展开两次
    for col in list_columns_for_explode:  # 遍历其他需要展开的列，并将它们的元素展开以匹配 'id_agent' 列的行数
        if col != 'id_agent':
            df_IB_panel[col] = df_IB[col].apply(lambda x: pd.Series(x.flatten())).stack().reset_index(level=1, drop=True)  # 对于二维数组需要展开两次
            pass  # if
        pass  # for
    df_IB_panel = df_IB_panel.reset_index(drop=True)  # 重置索引

    df_IB_panel.insert(0, 'id', range(len(df_IB_panel)))  # 添加id列
    df_IB_panel.insert(1, 'id_data', np.repeat(range(len(df_IB_panel) // num_agent ** 2), num_agent ** 2))  # 添加id_data列

    df_IB_panel = df_IB_panel.reset_index(drop=True)  # 重置索引

    filename_pkl_IB = Path(filepath_pkl_IB).name
    filename_pkl_IB_panel = filename_pkl_IB.replace('IB_', 'IB_panel_')
    filepath_pkl_IB_panal = Path(folderpath_exp_output_data, filename_pkl_IB_panel)  # 面板数据文件路径
    df_IB_panel.to_pickle(Path(filepath_pkl_IB_panal))  # 导出为 pkl 格式

    ## 保存为 csv、xlsx 格式，然后对 xlsx 格式的文件做进一步处理 #NOTE 有需要再启用以下代码
    # df_IB_panel.to_csv(Path(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.csv')), index=False)  # 导出为 csv 格式；
    # with pd.ExcelWriter(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.xlsx')) as writer:  # 导出为 xlsx 格式
    #     df_IB_panel.to_excel(writer, sheet_name='IB_panel')
    #     pass  # with
    #
    # ## 重新读取 xlsx 格式然后格式化
    # ### 需要调整列边距的列名
    # columnsName_adjust = [
    #     'id',
    #     'id_data',
    #     'process_name',
    #     'step',
    #     'turn',
    #     'phase',
    #     'id_agent',
    #     'row',
    #     'col',
    # ]
    #
    # wb_IB_panel = load_workbook(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.xlsx'))  # 使用 openpyxl 打开面板形式的 Excel 文件
    # sheet_IB_panel = wb_IB_panel.active
    #
    # sheet_IB_panel.freeze_panes = "K2"  # 冻结窗格
    #
    # col_indices = [df_IB_panel.columns.get_loc(col_name) + 1 for col_name in columnsName_adjust]  # 调整列宽
    # for col_index in col_indices:
    #     col_letter = get_column_letter(col_index)
    #     sheet_IB_panel.column_dimensions[col_letter].width = 5
    #
    # # 对于列 'id_data'，其单元格的值每间隔指定的行，对应的单元格背景色就变色。改变的颜色按照无色、浅灰色交替循环。
    # fill = PatternFill(start_color="EEEEEE", end_color="EEEEEE", fill_type="solid")
    # for i, row in enumerate(sheet_IB_panel.iter_rows(min_row=2)):  # 跳过第一行表头
    #     if i % (2 * num_agent ** 2) < num_agent ** 2:  # 每间隔指定的行填充一次背景色 #BUG 如果设置的银行数量不正确，那么绘制不符合预期。
    #         for cell in row:
    #             cell.fill = fill  # 将该行的背景色设置为浅灰色
    #
    # # for col in columns_states:  # 遍历每一列
    # #     col_index = df_BB_panel.columns.get_loc(col) + 1
    # #     col_letter = get_column_letter(col_index)
    # #     rng = sheet_IB_panel[col_letter]
    # #     for cell in rng:  # 遍历每一个单元格
    # #         if cell.value == True:
    # #             cell.fill = PatternFill(start_color="FFBBBB", end_color="FFBBBB", fill_type="solid")  # 根据单元格的值设置背景颜色
    #
    # wb_IB_panel.save(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.xlsx'))  # 保存 Excel 文件

    record_work_state(exp_id, 'status_预处理实验结果程序', 'DONE', folderpath_experiments_output_log)  # 记录本次实验作业的完成状态为 "DONE"

    pass  # function


if __name__ == '__main__':
    main()
