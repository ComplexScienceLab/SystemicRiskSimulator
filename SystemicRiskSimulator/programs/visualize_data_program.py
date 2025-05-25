"""
可视化结果程序。

Args:
    sgv: dict

Returns:
    None

"""
import platform
from pathlib import Path
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
from SystemicRiskSimulator.tools.rl_utils import RlUtils
from SystemicRiskSimulator.tools.visualization_tools import generate_one_interbank_matrix_heatmaps_data_info, draw_one_interbank_matrix_heatmaps, generate_one_interbank_graph_data_info, draw_one_interbank_flow_graph, generate_one_bank_accounts_data, draw_one_bank_BalanceSheet, merged_and_bind_figs_to_a_pdf_file


def main(sgv):
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
    # Tools.delete_and_recreate_folder(Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=config['is_auto_confirmation'])
    # Tools.copy_files_from_other_folders(Path(config['folderpath_project'], config['folderpath_config']), Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=config['is_auto_confirmation'])
    # from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

    from SystemicRiskSimulator.tools.tools import Tools

    # %% [markdown] 预处理数据

    # %%

    ## NOTE 导入包
    from matplotlib import pyplot as plt
    # import igraph as ig
    import matplotlib.pyplot as plt
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    import matplotlib.font_manager as fm
    from openpyxl import load_workbook
    from openpyxl.styles import PatternFill
    from openpyxl.utils import get_column_letter

    # %% ## NOTE 设置字体与绘图工具包的一些配置

    # %%

    ### 设置绘图时的字体 #NOTE：如果想要自定义字体，那么请开启下面的一段代码
    if sgv['system_platform'] == 'Darwin':  # MacOS系统
        zh_font_family = 'Songti SC'
        en_font_family = 'Times New Roman'
    elif sgv['system_platform'] == 'Windows':  # Windows系统
        zh_font_family = 'SimHei'
        en_font_family = 'Times New Roman'
    else:  # 其他系统
        zh_font_family = 'Arial'
        en_font_family = 'Arial'
    zh_font_prop = fm.FontProperties(fname=fm.findfont(fm.FontProperties(family=zh_font_family)))
    # zh_font_prop = fm.FontProperties(family=zh_font_family, size=14)  # 使用指定中文字体和字号
    zh_font_path = zh_font_prop.get_file()
    en_font_prop = fm.FontProperties(fname=fm.findfont(fm.FontProperties(family=en_font_family)))
    # en_font_prop = fm.FontProperties(family=en_font_family, size=14)  # 使用指定英文字体和字号
    en_font_path = en_font_prop.get_file()

    # ### NOTE：如果想要恢复原来的字体，那么请开启下面的一段代码 #DEBUG 还未测试
    # import matplotlib as mpl
    # import reportlab.pdfbase.pdfmetrics as pdfmetrics
    # mpl.rcParams.update(mpl.rcParamsDefault)  # 恢复matplotlib的默认字体设置
    # pdfmetrics._fonts = {}  # 移除在reportlab中注册的字体
    # zh_font_family = fm.FontProperties(family='Songti SC').get_name()  # 获取默认的中文字体为 Songti SC
    # en_font_family = fm.FontProperties(family='Times New Roman').get_name()  # 获取默认的英文字体为 Times New Roman

    ### 配置 plt
    plt.rcParams['font.family'] = zh_font_family

    ### 配置 reportlab
    pdfmetrics.registerFont(TTFont(zh_font_family, zh_font_path))
    pdfmetrics.registerFont(TTFont(en_font_family, en_font_path))

    # ### 配置 igraph
    # ig.config['plotting.backend'] = 'matplotlib'
    # ig.config.save()

    # %% ## NOTE 配置导入导出文件夹

    # %%

    ### 处理相关导入导出文件夹

    if sgv['is_use_RL_method']:
        if sgv['RL_state'] == 'training':
            folderpath_experiments_output_data = sgv['folderpath_experiments_output_data'] / "RL_training"
        elif sgv['RL_state'] == 'using':
            folderpath_experiments_output_data = sgv['folderpath_experiments_output_data'] / "RL_using"
    else:
        folderpath_experiments_output_data = sgv['folderpath_experiments_output_data'] / "normal"
        pass  # if

    # #TODO 以下部分建议分散到具体的子程序里面
    # sgv['folderpath_experiments'] = Path(sgv['folderpath_project'], sgv['folderpath_root_experiments'], sgv['foldername_experiments'])
    sgv['folderpath_experiments_output_data'] = folderpath_experiments_output_data
    sgv['folderpath_experiments_output_data_panel'] = (sgv['folderpath_experiments'] / sgv['foldername_experiments_output_data'] / "normal" / '../exp_output_data_panel').resolve()
    sgv['folderpath_plots'] = Path(sgv['folderpath_experiments'], sgv['foldername_plots'])
    sgv['folderpath_plots'].mkdir(parents=True, exist_ok=True)
    sgv['folderpath_plots_single_heatmaps'] = Path(sgv['folderpath_plots'], sgv['foldername_plots_single_heatmaps'])
    sgv['folderpath_plots_single_heatmaps'].mkdir(parents=True, exist_ok=True)
    sgv['folderpath_plots_makeup_heatmaps'] = Path(sgv['folderpath_plots'], sgv['foldername_plots_makeup_heatmaps'])
    sgv['folderpath_plots_makeup_heatmaps'].mkdir(parents=True, exist_ok=True)
    sgv['folderpath_plots_single_graphs'] = Path(sgv['folderpath_plots'], sgv['foldername_plots_single_graphs'])
    sgv['folderpath_plots_single_graphs'].mkdir(parents=True, exist_ok=True)
    sgv['folderpath_plots_makeup_graphs'] = Path(sgv['folderpath_plots'], sgv['foldername_plots_makeup_graphs'])
    sgv['folderpath_plots_makeup_graphs'].mkdir(parents=True, exist_ok=True)
    sgv['folderpath_plots_single_balanceSheets'] = Path(sgv['folderpath_plots'], sgv['foldername_plots_single_balanceSheets'])
    sgv['folderpath_plots_single_balanceSheets'].mkdir(parents=True, exist_ok=True)
    sgv['folderpath_plots_makeup_balanceSheets'] = Path(sgv['folderpath_plots'], sgv['foldername_plots_makeup_balanceSheets'])
    sgv['folderpath_plots_makeup_balanceSheets'].mkdir(parents=True, exist_ok=True)
    sgv['folderpath_visualize_banksStates_table'] = Path(sgv['folderpath_plots'], sgv['foldername_visualize_banksStates_table'])
    sgv['folderpath_visualize_banksStates_table'].mkdir(parents=True, exist_ok=True)
    sgv['folderpath_visualize_强化学习收敛曲线'] = Path(sgv['folderpath_plots'], sgv['foldername_visualize_强化学习收敛曲线'])
    sgv['folderpath_visualize_强化学习收敛曲线'].mkdir(parents=True, exist_ok=True)

    ## 获取需要做的实验组之索引
    list_fig_files = list(sgv['folderpath_experiments_output_data_panel'].glob('*-form=panel.pkl'))  # 获取实验组输出数据pkl格式之文件列表
    if sgv['vis']['list_idsExperiment_to_vis'] is None:
        experiments_indices_to_vis = list(range(len(list_fig_files)))
    else:
        experiments_indices_to_vis = sgv['vis']['list_idsExperiment_to_vis']
        pass

    # # %% [markdown] # NOTE 导入Pandas格式的实验结果数据，然后转换为面板形式的数据，导出PKL、CSV、xlsx 格式数据。 #HACK 这个功能似乎无用
    #
    # # %%
    #
    # print("执行：")
    #
    # if (sgv['visulization_process']['导入Pandas格式的实验结果数据转换为面板形式再导出']):
    #     print("导入Pandas格式的实验结果数据转换为面板形式再导出")
    #
    #     list_filepath_pkl_BB = list(sgv['folderpath_experiments_output_data'].glob('BB_exp*.pkl'))  # 获取实验组输出数据pkl格式之BB数据之文件列表
    #     for filepath_pkl_BB in list_filepath_pkl_BB:
    #         df_BB_original = pd.read_pickle(filepath_pkl_BB)
    #         num_agent = df_BB_original['id_agent'][0].shape[0]  # 获取个体数 #BUG  如果这里报错，那么最常见的可能是因为数据文件内容是空的。需要查看运行程序是否有配置因此正确导出数据
    #         df_BB = df_BB_original.applymap(lambda x: x.flatten() if hasattr(x, 'flatten') else x)  # 压平二维数组
    #
    #         ## 转换数据格式为numpy字符串格式
    #         list_columns_for_transform_datatype = [
    #             v for i, v in enumerate(df_BB.columns) if (
    #                     df_BB[v].dtype == np.dtype('object')
    #                     and type(df_BB[v][0]) == str
    #             )
    #         ]
    #         for i in range(df_BB.__len__()):
    #             df_BB[list_columns_for_transform_datatype[0]][i] = np.str_(df_BB[list_columns_for_transform_datatype[0]][i])  # BUG Pandas包警告
    #
    #         ## 展平为面板形式
    #         list_columns_for_explode = [
    #             v for i, v in enumerate(df_BB.columns) if (
    #                     df_BB[v].dtype == np.dtype('object')
    #                     and df_BB[v][0].size == num_agent
    #             )
    #         ]  # 获取需要展平的列
    #
    #         df_1D_panel = df_BB.explode('id_agent')  # 只展开 'id_agent' 列
    #         for col in list_columns_for_explode:  # 遍历其他需要展开的列，并将它们的元素展开以匹配 'id_agent' 列的行数
    #             if col != 'id_agent':
    #                 df_1D_panel[col] = df_BB.apply(lambda row: pd.Series(row[col]), axis=1).stack().reset_index(level=1, drop=True)
    #                 pass  # if
    #             pass  # for
    #         df_1D_panel = df_1D_panel.reset_index(drop=True)  # 重置索引
    #
    #         df_1D_panel.insert(0, 'id', range(len(df_1D_panel)))  # 添加id列
    #         df_1D_panel.insert(1, 'id_data', np.repeat(range(len(df_1D_panel) // num_agent), num_agent))  # 添加id_data列
    #
    #         df_1D_panel = df_1D_panel.reset_index(drop=True)  # 重置索引
    #
    #         filename_pkl_BB = Path(filepath_pkl_BB).name
    #         filename_pkl_BB_panel = filename_pkl_BB.replace('BB_', 'BB_panel_')
    #         filepath_pkl_BB_panal = Path(sgv['folderpath_plots'], filename_pkl_BB_panel)  # 面板数据文件路径
    #         df_1D_panel.to_pickle(Path(filepath_pkl_BB_panal))  # 导出为 pkl 格式
    #         df_1D_panel.to_csv(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.csv'), index=False)  # 导出为 csv 格式；
    #         with pd.ExcelWriter(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.xlsx')) as writer:  # 导出为 xlsx 格式
    #             df_1D_panel.to_excel(writer, sheet_name='BB_panel')
    #             pass  # with
    #
    #         ## 重新读取 xlsx 格式然后格式化
    #         ### 需要调整列边距的列名
    #         columnsName_adjust = [
    #             'id',
    #             'id_data',
    #             'step',
    #             'turn',
    #             'phase',
    #             'id_agent',
    #         ]
    #
    #         wb_BB_panel = load_workbook(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.xlsx'))  # 使用 openpyxl 打开面板形式的 Excel 文件
    #         sheet_BB_panel = wb_BB_panel.active
    #
    #         sheet_BB_panel.freeze_panes = "J2"  # 冻结窗格
    #
    #         col_indices = [df_1D_panel.columns.get_loc(col_name) + 1 for col_name in columnsName_adjust]  # 调整列宽
    #         for col_index in col_indices:
    #             col_letter = get_column_letter(col_index)
    #             sheet_BB_panel.column_dimensions[col_letter].width = 5
    #
    #         # 对于列 'id_data'，其单元格的值每间隔指定的行，对应的单元格背景色就变色。改变的颜色按照无色、浅灰色交替循环。
    #         fill = PatternFill(start_color="EEEEEE", end_color="EEEEEE", fill_type="solid")
    #         for i, row in enumerate(sheet_BB_panel.iter_rows(min_row=2)):  # 跳过第一行表头
    #             if i % (2 * sgv['num_bank']) < sgv['num_bank']:  # 每间隔指定的行填充一次背景色 #BUG 如果设置的银行数量不正确，那么绘制不符合预期。
    #                 for cell in row:
    #                     cell.fill = fill  # 将该行的背景色设置为浅灰色
    #
    #         # for col in columns_states:  # 遍历每一列
    #         #     col_index = df_1D_panel.columns.get_loc(col) + 1
    #         #     col_letter = get_column_letter(col_index)
    #         #     rng = sheet_BB_panel[col_letter]
    #         #     for cell in rng:  # 遍历每一个单元格
    #         #         if cell.value == True:
    #         #             cell.fill = PatternFill(start_color="FFBBBB", end_color="FFBBBB", fill_type="solid")  # 根据单元格的值设置背景颜色
    #
    #         wb_BB_panel.save(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.xlsx'))  # 保存 Excel 文件
    #
    #         pass  # for
    #
    #     list_filepath_pkl_IB = list(sgv['folderpath_experiments_output_data'].glob('IB_exp*.pkl'))  # 获取实验组输出数据pkl格式之IB数据之文件列表
    #     for filepath_pkl_IB in list_filepath_pkl_IB:
    #         df_IB_original = pd.read_pickle(filepath_pkl_IB)
    #         df_IB = deepcopy(df_IB_original)
    #
    #         ## 转换数据格式为numpy字符串格式
    #         list_columns_for_transform_datatype = [
    #             v for i, v in enumerate(df_IB.columns) if (
    #                     df_IB[v].dtype == np.dtype('object')
    #                     and type(df_IB[v][0]) == str
    #             )
    #         ]
    #         for i in range(df_IB.__len__()):
    #             df_IB[list_columns_for_transform_datatype[0]][i] = np.str_(df_IB[list_columns_for_transform_datatype[0]][i])  # BUG Pandas包警告
    #
    #         ## 转换信息列表为矩阵形式，插入数据框  #HACK 能否用现成的功能函数代替？
    #         list_columns_for_transform = [
    #             v for i, v in enumerate(df_IB.columns) if (
    #                     df_IB[v].dtype == np.dtype('object')
    #                     and df_IB[v][0].dtype == np.dtype('object')
    #             )
    #         ]
    #         for v1 in list_columns_for_transform:  # BUG Pandas包警告 #HACK 这个功能似乎无用
    #             for i2 in range(df_IB[v1].size):
    #                 m = np.full((num_agent, num_agent), False)
    #                 if df_IB.loc[i2, v1] is []:
    #                     df_IB.loc[i2, v1] = np.nan
    #                     continue
    #                 for i3, v3 in enumerate(df_IB.loc[i2, v1]):
    #                     if v3 is []:
    #                         m[i3, :] = False
    #                         continue
    #                         pass  # if
    #                     for i4 in v3:
    #                         if i4 in v3:
    #                             m[i3, i4] = True
    #                         else:
    #                             m[i3, i4] = False
    #                             pass  # if
    #                         pass  # for
    #                     pass  # for
    #                 df_IB[v1][i2] = m  # 赋值矩阵给数据框之元素，于数据框之相应的位置
    #                 pass  # for
    #             pass  # for
    #
    #         ## 生成agent矩阵之坐标，以矩阵形式，插入数据框
    #         row_coord, col_coord = np.mgrid[0:num_agent:1, 0:num_agent:1]
    #         df_IB.insert(loc=df_IB.columns.get_loc('id_agent') + 1, column="col", value=np.dtype('object'))
    #         for i, _ in enumerate(df_IB.col):
    #             df_IB.col[i] = col_coord.astype('int16')
    #         df_IB.insert(loc=df_IB.columns.get_loc('id_agent') + 1, column="row", value=np.dtype('object'))
    #         for i, _ in enumerate(df_IB.row):
    #             df_IB.row[i] = row_coord.astype('int16')
    #
    #         ## 展平为面板形式
    #         list_columns_for_explode = [
    #             v for i, v in enumerate(df_IB.columns) if (
    #                     df_IB[v].dtype == np.dtype('object')
    #                     and df_IB[v][0].size == num_agent ** 2
    #             )
    #         ]  # 获取需要展平的列
    #
    #         df_2D_panel = (df_IB.explode('id_agent')).explode('id_agent')  # 只展开 'id_agent' 列，对于二维数组需要展开两次
    #         # df_2D_panel = df_IB['id_agent'].apply(lambda x: pd.Series(x.flatten())).stack().reset_index(level=1, drop=True).to_frame('id_agent')  # 只展开 'id_agent' 列，对于二维数组需要展开两次
    #         for col in list_columns_for_explode:  # 遍历其他需要展开的列，并将它们的元素展开以匹配 'id_agent' 列的行数
    #             if col != 'id_agent':
    #                 df_2D_panel[col] = df_IB[col].apply(lambda x: pd.Series(x.flatten())).stack().reset_index(level=1, drop=True)  # 对于二维数组需要展开两次
    #                 pass  # if
    #             pass  # for
    #         df_2D_panel = df_2D_panel.reset_index(drop=True)  # 重置索引
    #
    #         df_2D_panel.insert(0, 'id', range(len(df_2D_panel)))  # 添加id列
    #         df_2D_panel.insert(1, 'id_data', np.repeat(range(len(df_2D_panel) // num_agent ** 2), num_agent ** 2))  # 添加id_data列
    #
    #         df_2D_panel = df_2D_panel.reset_index(drop=True)  # 重置索引
    #
    #         filename_pkl_IB = Path(filepath_pkl_IB).name
    #         filename_pkl_IB_panel = filename_pkl_IB.replace('IB_', 'IB_panel_')
    #         filepath_pkl_IB_panal = Path(sgv['folderpath_plots'], filename_pkl_IB_panel)  # 面板数据文件路径
    #         df_2D_panel.to_pickle(Path(filepath_pkl_IB_panal))  # 导出为 pkl 格式
    #         df_2D_panel.to_csv(Path(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.csv')), index=False)  # 导出为 csv 格式；
    #         with pd.ExcelWriter(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.xlsx')) as writer:  # 导出为 xlsx 格式
    #             df_2D_panel.to_excel(writer, sheet_name='IB_panel')
    #             pass  # with
    #
    #         ## 重新读取 xlsx 格式然后格式化
    #         ### 需要调整列边距的列名
    #         columnsName_adjust = [
    #             'id',
    #             'id_data',
    #             'process_name',
    #             'step',
    #             'turn',
    #             'phase',
    #             'id_agent',
    #             'row',
    #             'col',
    #         ]
    #
    #         wb_IB_panel = load_workbook(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.xlsx'))  # 使用 openpyxl 打开面板形式的 Excel 文件
    #         sheet_IB_panel = wb_IB_panel.active
    #
    #         sheet_IB_panel.freeze_panes = "K2"  # 冻结窗格
    #
    #         col_indices = [df_2D_panel.columns.get_loc(col_name) + 1 for col_name in columnsName_adjust]  # 调整列宽
    #         for col_index in col_indices:
    #             col_letter = get_column_letter(col_index)
    #             sheet_IB_panel.column_dimensions[col_letter].width = 5
    #
    #         # 对于列 'id_data'，其单元格的值每间隔指定的行，对应的单元格背景色就变色。改变的颜色按照无色、浅灰色交替循环。
    #         fill = PatternFill(start_color="EEEEEE", end_color="EEEEEE", fill_type="solid")
    #         for i, row in enumerate(sheet_IB_panel.iter_rows(min_row=2)):  # 跳过第一行表头
    #             if i % (2 * sgv['num_bank'] ** 2) < sgv['num_bank'] ** 2:  # 每间隔指定的行填充一次背景色 #BUG 如果设置的银行数量不正确，那么绘制不符合预期。
    #                 for cell in row:
    #                     cell.fill = fill  # 将该行的背景色设置为浅灰色
    #
    #         # for col in columns_states:  # 遍历每一列
    #         #     col_index = df_1D_panel.columns.get_loc(col) + 1
    #         #     col_letter = get_column_letter(col_index)
    #         #     rng = sheet_IB_panel[col_letter]
    #         #     for cell in rng:  # 遍历每一个单元格
    #         #         if cell.value == True:
    #         #             cell.fill = PatternFill(start_color="FFBBBB", end_color="FFBBBB", fill_type="solid")  # 根据单元格的值设置背景颜色
    #
    #         wb_IB_panel.save(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.xlsx'))  # 保存 Excel 文件
    #
    #         pass  # for
    #
    #     pass  # if 导入Pandas格式的实验结果数据转换为面板形式再导出

    # %% [markdown] # NOTE 导入面板形式的CSV数据预处理（备选）

    # %%

    if (sgv['visulization_process']['导入面板形式的CSV数据预处理']):

        # NOTE：如果需要读取CSV格式处理数据的话则使用该程序段。#BUG 可能已经过时尚未适配。不建议使用！

        print("导入面板形式的CSV数据预处理")

        list_filepath_csv_panel = list(sgv['folderpath_plots'].glob('*.csv'))  # 获取实验组输出数据csv格式的文件列表

        ## 排序，优先按照银行名称，其次按照时间。
        match_pattern_in_vertical_direction = r'(?<=[IB]B-panel_exp=).+?(?=[(\.csv)])'
        match_pattern_in_horizontal_direction = r'[IB]B'
        sorted_list_filepath_csv_panel = sorted(list_filepath_csv_panel, key=lambda name: (
            int(re.search(match_pattern_in_vertical_direction, str(name))[0]),
            re.search(match_pattern_in_horizontal_direction, str(name))[0],
        ))

        ## 获取所有实验之索引
        experiments_indices = []
        for filepath in sorted_list_filepath_csv_panel:
            match = re.search(r'exp=(\d+)', str(filepath))
            if match:
                experiments_indices.append(int(match.group(1)))
            pass  # for
        experiments_indices = sorted(list(set(experiments_indices)))  # 去重

        ## 依次读取面板形式的CSV格式的文件，预处理每次实验
        for i_exp in experiments_indices:
            csv_BB_00 = pd.read_csv(Path(sgv['folderpath_experiments_output_data'], 'BB_panel-exp=' + str(i_exp) + '.csv'))
            csv_IB_00 = pd.read_csv(Path(sgv['folderpath_experiments_output_data'], 'IB_panel-exp=' + str(i_exp) + '.csv'))

            ## 预处理数据表

            ## 去除空列、调整列顺序
            csv_BB_10 = deepcopy(csv_BB_00.loc[:, ~csv_BB_00.columns.str.contains('^Unnamed')])
            csv_IB_10 = deepcopy(csv_IB_00.loc[:, ~csv_IB_00.columns.str.contains('^Unnamed')])

            ## 提前列`row`、`col`
            cols_sorted_10 = ['id_agent']
            cols_sorted_10 = cols_sorted_10 + [s for s in csv_BB_10.columns if not s in cols_sorted_10]
            df_1D_panel = csv_BB_10[cols_sorted_10]
            cols_sorted_10 = ['row', 'col']
            cols_sorted_10 = cols_sorted_10 + [s for s in csv_IB_10.columns if not s in cols_sorted_10]
            df_2D_panel = csv_IB_10[cols_sorted_10]

            ## 一些变量
            num_1D_row_id = len(df_1D_panel)  # 数据表BB之行数
            num_2D_id = len(df_2D_panel)  # 数据表IB之行数
            num_idData = df_1D_panel['id_data'].max() + 1  # 数据表之数据id个数
            num_turn = df_1D_panel['turn'].max() + 1  # 总的轮次数（是从0开始计数的)
            num_step = num_idData  # 总的步进数（是从0开始计数的)

            ## 根据时间粒度参数，确定时间轴名称及其长度
            if sgv['vis']['time_granularity'] == '步进粒度':
                sgv['vis']['name_time'] = 'id_data'  # BUG 这个是否正确？是否应该改成 'step' ？
                sgv['vis']['num_time'] = num_step
            elif sgv['vis']['time_granularity'] == '轮次粒度':
                sgv['vis']['name_time'] = 'turn'
                sgv['vis']['num_time'] = num_turn
            else:
                raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                pass  # if
            sgv['vis']['num_items_in_a_time_in_BB'] = num_1D_row_id // num_idData  # BB之一个运行时间片之项目数
            sgv['vis']['num_items_in_a_time_in_IB'] = num_2D_id // num_idData  # IB之一个运行轮次之项目数
            num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
            num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

            pass  # for

        pass  # if 导入面板形式的CSV数据预处理

    # %% [markdown] ## #NOTE 绘制资产负债表图
    # 依次按照时间、银行，分别绘制单独的资产负债表（资产负债表尺寸不一样大，尺寸按照比例）

    # %%
    if (sgv['visulization_process']['绘制资产负债表图']):

        print("准备绘制资产负债表")
        Tools.delete_and_recreate_folder(sgv['folderpath_plots_single_balanceSheets'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

        for i_exp in experiments_indices_to_vis:

            # id=0-v=note-year=2007-density=0.10.pkl
            # exp=107-v=BB-aid=0-form=panel.pkl

            df_1D_panel = pd.read_pickle(list(sgv['folderpath_experiments_output_data_panel'].glob(f'exp={i_exp}-v=BB-*-form=panel.pkl'))[0])
            df_2D_panel = pd.read_pickle(list(sgv['folderpath_experiments_output_data_panel'].glob(f'exp={i_exp}-v=IB-*-form=panel.pkl'))[0])

            ## 一些变量
            num_1D_row_id = len(df_1D_panel)  # 数据表BB之行数
            num_2D_id = len(df_2D_panel)  # 数据表IB之行数
            num_idData = df_1D_panel['id_data'].max() + 1  # 数据表之数据id个数
            num_turn = df_1D_panel['turn'].max() + 1  # 总的轮次数（是从0开始计数的)
            num_step = num_idData  # 总的步进数（是从0开始计数的)
            ## 根据时间粒度参数，确定时间轴名称及其长度
            if sgv['vis']['time_granularity'] == '步进粒度':
                sgv['vis']['name_time'] = 'step'
                sgv['vis']['num_time'] = num_step
            elif sgv['vis']['time_granularity'] == '轮次粒度':
                sgv['vis']['name_time'] = 'turn'
                sgv['vis']['num_time'] = num_turn
            else:
                raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                pass  # if
            sgv['vis']['num_items_in_a_time_in_BB'] = num_1D_row_id // num_idData  # BB之一个运行时间片之项目数
            sgv['vis']['num_items_in_a_time_in_IB'] = num_2D_id // num_idData  # IB之一个运行轮次之项目数
            num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
            num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

            print("绘制资产负债表图：实验" + str(i_exp))

            sgv['vis']['zh_font_family'] = zh_font_family
            sgv['vis']['en_font_family'] = en_font_family

            ### 计算各银行主体之代表性的类型之数据之最大值和最小值
            sgv['vis']['max_BB_value_in_all_panel'] = df_1D_panel['A_all'].max()
            sgv['vis']['min_BB_value_in_all_panel'] = 0

            ## 创建一个作业列表，其中每个作业都是一个元组，包含所有需要传递给函数的参数
            works = []
            for i in range(sgv['vis']['num_items_in_a_time_in_BB']):
                for t in range(sgv['vis']['num_time']):
                    ## 初始化数据
                    data_vis_one_bank_BalanceSheet = {}
                    # 遍历数据类型
                    for dataType_name in sgv['vis']['list_dataTypes_for_balanceSheets'].keys():
                        data_vis_one_bank_BalanceSheet[dataType_name] = pd.DataFrame(sgv['vis']['list_dataTypes_for_balanceSheets'][dataType_name])
                        pass  # for
                    works.append((sgv, df_1D_panel, data_vis_one_bank_BalanceSheet, i_exp, i, t))
                    pass  # for
                pass  # for

            ## 绘图
            if sgv['is_enable_multiprocessing_for_visualization']:  # 多进程并行处理
                num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
                with Pool(num_cores) as p:
                    p.map(process_one_balanceSheet, works)  # 使用多进程并行处理
                    pass  # with
            else:  # 串行处理
                for i in range(len(works)):
                    process_one_balanceSheet(works[i])
                    pass  # for

            pass  # for  实验编号

        pass  # if 绘制资产负债表图

    # %% [markdown] ## #NOTE 拼接资产负债表图
    # 导入各自的资产负债表，按照横向时间纵向银行，拼接成大图

    # %%

    if (sgv['visulization_process']['拼接资产负债表图']):
        print("准备拼接资产负债表图")
        Tools.delete_and_recreate_folder(sgv['folderpath_plots_makeup_balanceSheets'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

        for i_exp in experiments_indices_to_vis:

            df_1D_panel = pd.read_pickle(list(sgv['folderpath_experiments_output_data_panel'].glob(f'exp={i_exp}-v=BB-*-form=panel.pkl'))[0])
            df_2D_panel = pd.read_pickle(list(sgv['folderpath_experiments_output_data_panel'].glob(f'exp={i_exp}-v=IB-*-form=panel.pkl'))[0])

            ## 一些变量
            num_1D_row_id = len(df_1D_panel)  # 数据表BB之行数
            num_2D_id = len(df_2D_panel)  # 数据表IB之行数
            num_idData = df_1D_panel['id_data'].max() + 1  # 数据表之数据id个数
            num_turn = df_1D_panel['turn'].max() + 1  # 总的轮次数（是从0开始计数的)
            num_step = num_idData  # 总的步进数（是从0开始计数的)
            ## 根据时间粒度参数，确定时间轴名称及其长度
            if sgv['vis']['time_granularity'] == '步进粒度':
                sgv['vis']['name_time'] = 'step'
                sgv['vis']['num_time'] = num_step
            elif sgv['vis']['time_granularity'] == '轮次粒度':
                sgv['vis']['name_time'] = 'turn'
                sgv['vis']['num_time'] = num_turn
            else:
                raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                pass  # if
            sgv['vis']['num_items_in_a_time_in_BB'] = num_1D_row_id // num_idData  # BB之一个运行时间片之项目数
            sgv['vis']['num_items_in_a_time_in_IB'] = num_2D_id // num_idData  # IB之一个运行轮次之项目数
            num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
            num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

            print("拼接资产负债表图：实验" + str(i_exp))

            ## 声明与定义变量
            match_pattern_of_agent_name = fr"(?<=name=).+?(?=[\+(\.svg)])"  # 匹配相关含义的变量之个体名称之正则表达式文本
            match_pattern_of_name_time = fr"(?<={sgv['vis']['name_time']}=).+?(?=[\+(\.svg)])"  # 匹配相关含义的变量之时间名称之正则表达式文本

            ## 设置参数
            ### #NOTE 这组配置表示按照银行横向，按照时间纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
            order_of_variable_mean_in_horizontal_and_vertical_direction = (sgv['vis']['num_items_in_a_time_in_BB'], sgv['vis']['num_time'])
            order_of_paging_in_horizontal_and_vertical_direction = (None, 1)
            order_of_match_pattern_in_horizontal_and_vertical_direction = (match_pattern_of_agent_name, match_pattern_of_name_time)

            list_fig_files = glob.glob(str(sgv['folderpath_plots_single_balanceSheets'] / f'*exp={i_exp}+*.svg'))  # 获取所有当次实验文件列表

            merged_pdf = merged_and_bind_figs_to_a_pdf_file(order_of_variable_mean_in_horizontal_and_vertical_direction, order_of_paging_in_horizontal_and_vertical_direction, order_of_match_pattern_in_horizontal_and_vertical_direction, list_fig_files, i_exp)

            ## 保存
            merged_pdf.save(Path(sgv['folderpath_plots_makeup_balanceSheets'], 'BB-exp=' + str(i_exp) + '.pdf'))
            merged_pdf.close()

            pass  # for  实验编号

        pass  # if 拼接资产负债表图

    # %% [markdown] ## NOTE 绘制矩阵热图
    # 依次按照每个银行间数据类别、时间，分别绘制单独的银行间资金流网络图

    # %%
    if (sgv['visulization_process']['绘制矩阵热图']):
        print("准备绘制矩阵热图")
        Tools.delete_and_recreate_folder(sgv['folderpath_plots_single_heatmaps'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

        # with Pool() as p:
        #     p.map(fun_visualize_data, [sgv])
        #     # fun_visualize_data(sgv)

        df_data_types = pd.DataFrame(sgv['vis']['list_dataTypes_for_heatmaps'])

        for i_exp in experiments_indices_to_vis:
            dict_1D_panel = {}
            dict_2D_panel = {}
            for para_01 in sgv['list_agents_data_filename_para_01']:
                # 根据文件名前缀判断数据类型  #BUG 这个存在风险，因为文件名前缀可能不遵循约定，后续扩展可能会有变化
                if (para_01 == 'note' or para_01 == 'AB'):  # note 数据不需要处理
                    continue
                if not para_01.startswith('I'):  # 说明是 1D 的数据
                    v_1D = pd.read_pickle(list(sgv['folderpath_experiments_output_data_panel'].glob(f'exp={i_exp}-v={para_01}-*-form=panel.pkl'))[0])
                    dict_1D_panel[para_01] = v_1D
                    if para_01 == 'BB':
                        # 计算总的轮次数（是从0开始计数的)、总的步进数（是从0开始计数的)
                        num_turn = v_1D['turn'].max() + 1  # 总的轮次数（是从0开始计数的)
                        num_idData = v_1D['id_data'].max() + 1  # 数据表之数据id个数
                        num_step = num_idData  # 总的步进数（是从0开始计数的)
                        pass  # if
                else:  # 说明是 2D 的数据
                    df_2D_panel = pd.read_pickle(list(sgv['folderpath_experiments_output_data_panel'].glob(f'exp={i_exp}-v={para_01}-*-form=panel.pkl'))[0])
                    dict_2D_panel[para_01] = df_2D_panel
                    pass  # if
                pass  # for

            # 获取各个体、个体间一些信息
            list_num_1D_row_id = []  # 1D数据之行数
            list_num_1D_row_agent = []  # 1D数据之行数之个体数
            list_max_value_row_1D = []  # 1D数据之行数之最大值
            list_num_1D_col_id = []  # 1D数据之列数
            list_num_1D_col_agent = []  # 1D数据之列数之个体数
            list_max_value_col_1D = []  # 1D数据之列数之最大值
            list_num_2D_id = []  # 2D数据之行数
            list_num_2D_agent = []  # 2D数据之行数之个体数
            list_max_value_2D = []  # 2D数据之最大值
            for i, d in df_data_types.iterrows():
                for k_1D, v_1D in dict_1D_panel.items():
                    if d['data_name'][0] in v_1D.columns:
                        num_1D_row_agent = v_1D['id_agent'].max() + 1
                        list_num_1D_row_agent.append(num_1D_row_agent)
                        num_1D_row_id = len(v_1D)
                        list_num_1D_row_id.append(num_1D_row_id)
                        max_value_row_1D = v_1D[d['data_name'][0]].max()
                        list_max_value_row_1D.append(max_value_row_1D)
                        row_dataType_name = k_1D
                        pass  # if
                    if d['data_name'][1] in v_1D.columns:
                        num_1D_col_agent = v_1D['id_agent'].max() + 1
                        list_num_1D_col_agent.append(num_1D_col_agent)
                        num_1D_col_id = len(v_1D)
                        list_num_1D_col_id.append(num_1D_col_id)
                        max_value_col_1D = v_1D[d['data_name'][1]].max()
                        list_max_value_col_1D.append(max_value_col_1D)
                        col_dataType_name = k_1D
                        pass  # if
                for k_2D, v_2D in dict_2D_panel.items():
                    if d['data_name'][2] in v_2D.columns:
                        num_2D_agent = ((v_2D['row'].max() + 1), (v_2D['col'].max() + 1))
                        list_num_2D_agent.append(num_2D_agent)
                        num_2D_id = len(v_2D)
                        list_num_2D_id.append(num_2D_id)
                        max_value_2D = v_2D[d['data_name'][2]].max()
                        list_max_value_2D.append(max_value_2D)
                        matrix_dataType_name = k_2D
                        pass  # if
                    pass  # for
                pass  # for

            sgv['vis']['list_num_1D_row_id'] = list_num_1D_row_id
            sgv['vis']['list_num_1D_row_agent'] = list_num_1D_row_agent
            sgv['vis']['list_max_value_row_1D'] = list_max_value_row_1D
            sgv['vis']['row_dataType_name'] = row_dataType_name
            sgv['vis']['list_num_1D_col_id'] = list_num_1D_col_id
            sgv['vis']['list_num_1D_col_agent'] = list_num_1D_col_agent
            sgv['vis']['list_max_value_col_1D'] = list_max_value_col_1D
            sgv['vis']['col_dataType_name'] = col_dataType_name
            sgv['vis']['list_num_2D_id'] = list_num_2D_id
            sgv['vis']['list_num_2D_agent'] = list_num_2D_agent
            sgv['vis']['list_max_value_2D'] = list_max_value_2D
            sgv['vis']['matrix_dataType_name'] = matrix_dataType_name

            # 计算 list_num_2D_agent 里面行数和列数最大值，作为绘制矩阵热图规划画布布局的依据
            list_num_2D_agent_row = [i[0] for i in list_num_2D_agent]
            list_num_2D_agent_col = [i[1] for i in list_num_2D_agent]
            max_num_2D_agent_row = max(list_num_2D_agent_row)
            max_num_2D_agent_col = max(list_num_2D_agent_col)
            max_num_2D_agent = max(max_num_2D_agent_row, max_num_2D_agent_col)

            sgv['vis']['max_num_2D_agent'] = max_num_2D_agent

            # df_1D_panel = pd.read_pickle(Path(sgv['folderpath_experiments_output_data'], 'BB_panel-exp=' + str(i_exp) + '.pkl'))
            # df_2D_panel = pd.read_pickle(Path(sgv['folderpath_experiments_output_data'], 'IB_panel-exp=' + str(i_exp) + '.pkl'))

            # ## 一些变量
            # num_1D_id = len(df_1D_panel)  # 1D数据表之行数
            # # 遍历 dict_1D_panel，获取 1D 数据表之行数之最大值
            # num_1D_id = 0
            # for key in dict_1D_panel.keys():
            #     if len(dict_1D_panel[key]) > num_1D_id:
            #         num_1D_id = len(dict_1D_panel[key])
            #         pass
            #     pass  # for
            # # 遍历 dict_2D_panel，获取 1D 数据表之行数之最大值
            # num_2D_id = 0
            # for key in dict_2D_panel.keys():
            #     if len(dict_2D_panel[key]) > num_2D_id:
            #         num_2D_id = len(dict_2D_panel[key])
            #         pass
            #     pass
            # num_2D_id = len(df_2D_panel)  # 2D数据表之行数
            # num_idData = df_1D_panel['id_data'].max() + 1  # 数据表之数据id个数
            # num_turn = df_1D_panel['turn'].max() + 1  # 总的轮次数（是从0开始计数的)
            # num_step = num_idData  # 总的步进数（是从0开始计数的)

            ## 根据时间粒度参数，确定时间轴名称及其长度
            if sgv['vis']['time_granularity'] == '步进粒度':
                sgv['vis']['name_time'] = 'step'
                sgv['vis']['num_time'] = num_step
            elif sgv['vis']['time_granularity'] == '轮次粒度':
                sgv['vis']['name_time'] = 'turn'
                sgv['vis']['num_time'] = num_turn
            else:
                raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                pass  # if
            sgv['vis']['num_items_in_a_time_in_BB'] = num_1D_row_id // num_idData  # BB之一个运行时间片之项目数
            sgv['vis']['num_items_in_a_time_in_IB'] = num_2D_id // num_idData  # IB之一个运行轮次之项目数
            # num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
            # num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

            print("绘制矩阵热图：实验" + str(i_exp))

            sgv['vis']['zh_font_family'] = zh_font_family
            sgv['vis']['en_font_family'] = en_font_family

            ### 计算各 1D 个体之代表性的类型之数据之最大值和最小值
            sgv['vis']['min_1D_agent_value_in_all_panel'] = 0
            sgv['vis']['max_1D_agent_value_in_all_panel'] = 0
            for v in list_max_value_row_1D:
                if v > sgv['vis']['max_1D_agent_value_in_all_panel']:
                    sgv['vis']['max_1D_agent_value_in_all_panel'] = v
                    pass  # if
                pass  # for
            for v in list_max_value_col_1D:
                if v > sgv['vis']['max_1D_agent_value_in_all_panel']:
                    sgv['vis']['max_1D_agent_value_in_all_panel'] = v
                    pass  # if
                pass  # for

            ### 计算各 2D 个体之代表性的类型之数据之最大值和最小值
            sgv['vis']['min_2D_agent_value_in_all_panel'] = 0
            sgv['vis']['max_2D_agent_value_in_all_panel'] = 0
            for v in list_max_value_2D:
                if v > sgv['vis']['max_2D_agent_value_in_all_panel']:
                    sgv['vis']['max_2D_agent_value_in_all_panel'] = v
                    pass  # if
                pass  # for

            ## 创建一个作业列表，其中每个作业都是一个元组，包含所有需要传递给函数的参数
            works = []
            df_1D_panel_row = None
            df_1D_panel_col = None
            df_2D_panel = None
            # for i in range(sgv['vis']['num_items_in_a_time_in_BB']):
            for t in range(sgv['vis']['num_time']):
                for i, d in df_data_types.iterrows():
                    for k_1D, v_1D in dict_1D_panel.items():
                        if d['data_name'][0] in v_1D.columns:
                            df_1D_panel_row = v_1D[v_1D['id_data'] == t]
                            pass  # if
                        if d['data_name'][1] in v_1D.columns:
                            df_1D_panel_col = v_1D[v_1D['id_data'] == t]
                            pass  # if
                        pass  # for
                    for k_2D, v_2D in dict_2D_panel.items():
                        if d['data_name'][2] in v_2D.columns:
                            df_2D_panel = v_2D[v_2D['id_data'] == t]
                            pass  # if
                        pass  # for
                    works.append((sgv, df_1D_panel_row, df_1D_panel_col, df_2D_panel, d, i_exp, t, i))
                    pass  # for
                pass  # for

                # for t in range(sgv['vis']['num_time']):
                #     works.append((sgv, dict_1D_panel, dict_2D_panel, d, i_exp, t, i))
                #     pass  # for
                # pass  # for

            ## 绘图
            if sgv['is_enable_multiprocessing_for_visualization']:  # 多进程并行处理
                num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
                with Pool(num_cores) as p:
                    p.map(process_one_heatmap, works)
                    pass  # with
            else:  # 串行处理
                for i in range(len(works)):
                    process_one_heatmap(works[i])
                    pass  # for

            pass  # for

        pass  # if 绘制矩阵热图

    # %% [markdown] ## #NOTE 拼接矩阵热图
    # 导入各自的矩阵热图，按照横向数据类别纵向时间，拼接成大图

    # %%
    if (sgv['visulization_process']['拼接矩阵热图']):
        print("准备拼接矩阵热图")
        Tools.delete_and_recreate_folder(sgv['folderpath_plots_makeup_heatmaps'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

        for i_exp in experiments_indices_to_vis:

            # for para_01 in sgv['list_agents_data_filename_para_01']:
            #         if (para_01 == 'note' or para_01 == 'AB'):
            #         continue
            #     if not para_01.startswith('I'):  # 说明是 1D 的数据
            #         df_1D_panel = pd.read_pickle(list(sgv['folderpath_experiments_output_data_panel'].glob(f'exp={i_exp}-v={para_01}-*-form=panel.pkl'))[0])

            # #BUG 为什么这里不遍历 para_01，而是直接用 'BB' 和 'IB' ？
            df_1D_panel = pd.read_pickle(list(sgv['folderpath_experiments_output_data_panel'].glob(f'exp={i_exp}-v=BB-*-form=panel.pkl'))[0])
            df_2D_panel = pd.read_pickle(list(sgv['folderpath_experiments_output_data_panel'].glob(f'exp={i_exp}-v=IB-*-form=panel.pkl'))[0])

            ## 一些变量
            num_1D_row_id = len(df_1D_panel)  # 数据表BB之行数
            num_2D_id = len(df_2D_panel)  # 数据表IB之行数
            num_idData = df_1D_panel['id_data'].max() + 1  # 数据表之数据id个数
            num_turn = df_1D_panel['turn'].max() + 1  # 总的轮次数（是从0开始计数的)
            num_step = num_idData  # 总的步进数（是从0开始计数的)
            ## 根据时间粒度参数，确定时间轴名称及其长度
            if sgv['vis']['time_granularity'] == '步进粒度':
                sgv['vis']['name_time'] = 'step'
                sgv['vis']['num_time'] = num_step
            elif sgv['vis']['time_granularity'] == '轮次粒度':
                sgv['vis']['name_time'] = 'turn'
                sgv['vis']['num_time'] = num_turn
            else:
                raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                pass  # if
            sgv['vis']['num_items_in_a_time_in_BB'] = num_1D_row_id // num_idData  # BB之一个运行时间片之项目数
            sgv['vis']['num_items_in_a_time_in_IB'] = num_2D_id // num_idData  # IB之一个运行轮次之项目数
            num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
            num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

            print("拼接矩阵热图：实验" + str(i_exp))

            num_dataTypes_for_heatmap_figs = len(sgv['vis']['list_dataTypes_for_heatmaps'])  # 数据类别数

            ## 声明与定义变量
            match_pattern_of_data_name = fr"(?<=data=).+?(?=[\+(\.pdf)])"  # 匹配相关含义的变量之数据名称之正则表达式文本
            match_pattern_of_name_time = fr"(?<={sgv['vis']['name_time']}=).+?(?=[\+(\.pdf)])"  # 匹配相关含义的变量之时间名称之正则表达式文本

            ## 设置参数

            ### #NOTE 这组配置表示按照数据类别横向，按照时间纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
            order_of_variable_mean_in_horizontal_and_vertical_direction = (num_dataTypes_for_heatmap_figs, sgv['vis']['num_time'])
            order_of_paging_in_horizontal_and_vertical_direction = (None, 1)
            order_of_match_pattern_in_horizontal_and_vertical_direction = (match_pattern_of_data_name, match_pattern_of_name_time)

            list_fig_files = glob.glob(str(sgv['folderpath_plots_single_heatmaps'] / f'*exp={i_exp}+*.pdf'))  # 获取所有当次实验文件列表

            merged_pdf = merged_and_bind_figs_to_a_pdf_file(order_of_variable_mean_in_horizontal_and_vertical_direction, order_of_paging_in_horizontal_and_vertical_direction, order_of_match_pattern_in_horizontal_and_vertical_direction, list_fig_files, i_exp)

            ## 保存
            merged_pdf.save(Path(sgv['folderpath_plots_makeup_heatmaps'], 'IB-exp=' + str(i_exp) + '.pdf'))
            merged_pdf.close()

            pass  # for

        pass  # if 拼接矩阵热图

    # %% [markdown] ## #NOTE 绘制资金流网络图 #BUG 这里的代码没有适配，已经不能保证能够正常使用！
    # 依次按照每个银行间数据类别、时间，分别绘制单独的银行间资金流网络图

    # %%
    if (sgv['visulization_process']['绘制资金流网络图']):

        print("准备绘制资金流网络图")
        Tools.delete_and_recreate_folder(sgv['folderpath_plots_single_graphs'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

        for i_exp in experiments_indices_to_vis:

            df_1D_panel = pd.read_pickle(Path(sgv['folderpath_experiments_output_data_panel'], 'BB_panel-exp=' + str(i_exp) + '.pkl'))
            df_2D_panel = pd.read_pickle(Path(sgv['folderpath_experiments_output_data_panel'], 'IB_panel-exp=' + str(i_exp) + '.pkl'))

            ## 一些变量
            num_1D_row_id = len(df_1D_panel)  # 数据表BB之行数
            num_2D_id = len(df_2D_panel)  # 数据表IB之行数
            num_idData = df_1D_panel['id_data'].max() + 1  # 数据表之数据id个数
            num_turn = df_1D_panel['turn'].max() + 1  # 总的轮次数（是从0开始计数的)
            num_step = num_idData  # 总的步进数（是从0开始计数的)
            ## 根据时间粒度参数，确定时间轴名称及其长度
            if sgv['vis']['time_granularity'] == '步进粒度':
                sgv['vis']['name_time'] = 'step'
                sgv['vis']['num_time'] = num_step
            elif sgv['vis']['time_granularity'] == '轮次粒度':
                sgv['vis']['name_time'] = 'turn'
                sgv['vis']['num_time'] = num_turn
            else:
                raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                pass  # if
            sgv['vis']['num_items_in_a_time_in_BB'] = num_1D_row_id // num_idData  # BB之一个运行时间片之项目数
            sgv['vis']['num_items_in_a_time_in_IB'] = num_2D_id // num_idData  # IB之一个运行轮次之项目数
            num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
            num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

            print("绘制资金流网络图：实验" + str(i_exp))

            sgv['vis']['zh_font_family'] = zh_font_family
            sgv['vis']['en_font_family'] = en_font_family

            ### 计算各银行主体之代表性的类型之数据之最大值和最小值
            sgv['vis']['max_BB_value_in_all_panel'] = df_1D_panel['A_all'].max()
            sgv['vis']['min_BB_value_in_all_panel'] = 0

            ### 计算各银行主体间之代表性的类型之数据之最大值和最小值
            sgv['vis']['max_IB_value_in_all_panel'] = df_2D_panel['A_IB'].max()
            sgv['vis']['min_IB_value_in_all_panel'] = 0

            ## 创建一个作业列表，其中每个作业都是一个元组，包含所有需要传递给函数的参数
            works = []
            for i, d in enumerate(sgv['vis']['list_dataNames_for_graph_figs']):

                for t in range(sgv['vis']['num_time']):
                    ## 初始化参数
                    data_vis_one_time_graph = {}
                    data_vis_one_time_graph['edge_types'] = pd.DataFrame(sgv['vis']['list_data_edgeTypes_for_graph_figs'][i])
                    data_vis_one_time_graph['vertices'] = pd.DataFrame()
                    data_vis_one_time_graph['edges'] = pd.DataFrame()

                    works.append((sgv, df_1D_panel, df_2D_panel, data_vis_one_time_graph, i_exp, d, t))
                    pass  # for
                pass  # for

            ## 绘图
            if sgv['is_enable_multiprocessing_for_visualization']:  # 多进程并行处理
                num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
                with Pool(num_cores) as p:
                    p.map(process_one_graph, works)
                    pass  # with
            else:  # 串行处理
                for i in range(len(works)):
                    process_one_graph(works[i])
                    pass  # for

            pass  # for  实验编号

        pass  # if 绘制资金流网络图

    # %% [markdown] ## #NOTE 拼接资金流网络图
    # 导入各自的网络图，按照横向数据类别纵向时间，拼接成大图

    # %%
    if (sgv['visulization_process']['拼接资金流网络图']):
        print("准备拼接资金流网络图")
        Tools.delete_and_recreate_folder(sgv['folderpath_plots_makeup_graphs'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

        for i_exp in experiments_indices_to_vis:

            df_1D_panel = pd.read_pickle(Path(sgv['folderpath_experiments_output_data_panel'], 'BB_panel-exp=' + str(i_exp) + '.pkl'))
            df_2D_panel = pd.read_pickle(Path(sgv['folderpath_experiments_output_data_panel'], 'IB_panel-exp=' + str(i_exp) + '.pkl'))

            ## 一些变量
            num_1D_row_id = len(df_1D_panel)  # 数据表BB之行数
            num_2D_id = len(df_2D_panel)  # 数据表IB之行数
            num_idData = df_1D_panel['id_data'].max() + 1  # 数据表之数据id个数
            num_turn = df_1D_panel['turn'].max() + 1  # 总的轮次数（是从0开始计数的)
            num_step = num_idData  # 总的步进数（是从0开始计数的)
            ## 根据时间粒度参数，确定时间轴名称及其长度
            if sgv['vis']['time_granularity'] == '步进粒度':
                sgv['vis']['name_time'] = 'step'
                sgv['vis']['num_time'] = num_step
            elif sgv['vis']['time_granularity'] == '轮次粒度':
                sgv['vis']['name_time'] = 'turn'
                sgv['vis']['num_time'] = num_turn
            else:
                raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                pass  # if
            sgv['vis']['num_items_in_a_time_in_BB'] = num_1D_row_id // num_idData  # BB之一个运行时间片之项目数
            sgv['vis']['num_items_in_a_time_in_IB'] = num_2D_id // num_idData  # IB之一个运行轮次之项目数
            num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
            num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

            print("拼接资金流网络图：实验" + str(i_exp))

            num_dataTypes_for_graph_figs = len(sgv['vis']['list_dataNames_for_graph_figs'])  # 数据类别数

            ## 声明与定义变量
            match_pattern_of_data_name = fr"(?<=data=).+?(?=[\+(\.pdf)])"  # 匹配相关含义的变量之数据名称之正则表达式文本
            match_pattern_of_name_time = fr"(?<={sgv['vis']['name_time']}=).+?(?=[\+(\.pdf)])"  # 匹配相关含义的变量之时间名称之正则表达式文本

            ## 设置参数
            ### #NOTE 这组配置表示按照数据类别横向，按照时间纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
            order_of_variable_mean_in_horizontal_and_vertical_direction = (num_dataTypes_for_graph_figs, sgv['vis']['num_time'])
            order_of_paging_in_horizontal_and_vertical_direction = (None, 1)
            order_of_match_pattern_in_horizontal_and_vertical_direction = (match_pattern_of_data_name, match_pattern_of_name_time)

            list_fig_files = glob.glob(str(sgv['folderpath_plots_single_graphs'] / f'*exp={i_exp}+*.pdf'))  # 获取所有当次实验文件列表

            merged_pdf = merged_and_bind_figs_to_a_pdf_file(order_of_variable_mean_in_horizontal_and_vertical_direction, order_of_paging_in_horizontal_and_vertical_direction, order_of_match_pattern_in_horizontal_and_vertical_direction, list_fig_files, i_exp)

            ## 保存
            merged_pdf.save(Path(sgv['folderpath_plots_makeup_graphs'], 'IB-exp=' + str(i_exp) + '.pdf'))
            merged_pdf.close()

            pass  # for  实验编号

        pass  # if 拼接资金流网络图

    # %% [markdown] ## #NOTE 可视化银行状态表格 #BUG 这里的代码似乎没有适配，已经不能保证能够正常使用！
    # 单独提取银行状态数据，处理成高亮可视化表格

    # %%
    if (sgv['visulization_process']['银行状态表格可视化']):

        print("准备可视化银行状态表格")
        Tools.delete_and_recreate_folder(sgv['folderpath_visualize_banksStates_table'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

        for i_exp in experiments_indices_to_vis:
            df_1D_panel = pd.read_pickle(Path(sgv['folderpath_experiments_output_data_panel'], 'BB_panel-exp=' + str(i_exp) + '.pkl'))
            df_2D_panel = pd.read_pickle(Path(sgv['folderpath_experiments_output_data_panel'], 'IB_panel-exp=' + str(i_exp) + '.pkl'))

            ## 一些变量
            num_1D_row_id = len(df_1D_panel)  # 数据表BB之行数
            num_2D_id = len(df_2D_panel)  # 数据表IB之行数
            num_idData = df_1D_panel['id_data'].max() + 1  # 数据表之数据id个数
            num_turn = df_1D_panel['turn'].max() + 1  # 总的轮次数（是从0开始计数的)
            num_step = num_idData  # 总的步进数（是从0开始计数的)
            ## 根据时间粒度参数，确定时间轴名称及其长度
            if sgv['vis']['time_granularity'] == '步进粒度':
                sgv['vis']['name_time'] = 'step'
                sgv['vis']['num_time'] = num_step
            elif sgv['vis']['time_granularity'] == '轮次粒度':
                sgv['vis']['name_time'] = 'turn'
                sgv['vis']['num_time'] = num_turn
            else:
                raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                pass  # if
            sgv['vis']['num_items_in_a_time_in_BB'] = num_1D_row_id // num_idData  # BB之一个运行时间片之项目数
            sgv['vis']['num_items_in_a_time_in_IB'] = num_2D_id // num_idData  # IB之一个运行轮次之项目数
            num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
            num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

            print("可视化银行状态表格：实验" + str(i_exp))

            df_BankStates = df_1D_panel[sgv['vis']['columnsName_extract']]  # 提取所需列

            df_BankStates.to_excel(Path(sgv['folderpath_visualize_banksStates_table'], 'BB_panel-exp=' + str(i_exp) + '.xlsx'), index=False)  # 将数据写入新的 Excel 文件

            wb_BB_panel = load_workbook(Path(sgv['folderpath_visualize_banksStates_table'], 'BB_panel-exp=' + str(i_exp) + '.xlsx'))  # 使用 openpyxl 打开新的 Excel 文件
            sheet_BB_panel = wb_BB_panel.active

            sheet_BB_panel.freeze_panes = "J2"  # 冻结窗格  #BUG  后续这个直接设定的单元格地址可能存在问题

            col_indices = [df_BankStates.columns.get_loc(col_name) + 1 for col_name in sgv['vis']['columnsName_adjust']]  # 调整列宽
            for col_index in col_indices:
                col_letter = get_column_letter(col_index)
                sheet_BB_panel.column_dimensions[col_letter].width = 5

            # 对于列 'id_data'，其单元格的值每间隔指定的行，对应的单元格背景色就变色。改变的颜色按照无色、浅灰色交替循环。
            fill = PatternFill(start_color="EEEEEE", end_color="EEEEEE", fill_type="solid")
            for i, row in enumerate(sheet_BB_panel.iter_rows(min_row=2)):  # 跳过第一行表头
                if i % (2 * sgv['num_bank']) < sgv['num_bank']:  # 每间隔指定的行填充一次背景色
                    for cell in row:
                        cell.fill = fill  # 将该行的背景色设置为浅灰色

            for col in sgv['vis']['columns_states']:  # 遍历每一列
                col_index = df_BankStates.columns.get_loc(col) + 1
                col_letter = get_column_letter(col_index)
                rng = sheet_BB_panel[col_letter]
                for cell in rng:  # 遍历每一个单元格
                    if cell.value == True:
                        cell.fill = PatternFill(start_color="FFBBBB", end_color="FFBBBB", fill_type="solid")  # 根据单元格的值设置背景颜色

            wb_BB_panel.save(Path(sgv['folderpath_visualize_banksStates_table'], 'BB_panel-exp=' + str(i_exp) + '.xlsx'))  # 保存 Excel 文件

            pass  # for

        pass  # if

    # %% [markdown] ## #NOTE 绘制强化学习收敛曲线图

    # %%
    if (sgv['visulization_process']['绘制强化学习收敛曲线图']):
        print("准备绘制强化学习收敛曲线图")
        Tools.delete_and_recreate_folder(sgv['folderpath_visualize_强化学习收敛曲线'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

        for para_01 in sgv['list_agents_data_filename_para_01']:
            print(para_01)#DEBUG
            if (para_01 != 'AB'):
                continue

            ## 集中收集 rewards 数据
            df_v = pd.read_pickle(list((sgv['folderpath_experiments_output_data']).glob(f"id=0*-v={para_01}-*.pkl"))[0])
            sgv['num_agents'] = df_v['rewards_values'][df_v['step'] == df_v['step'].max()].values.size

            arr_episodes_agents_rewardsValues = np.empty((sgv['num_episodes'], sgv['num_agents']), dtype=object)  # 用于存储每个实验的每个代理的奖励数据
            arr_episodes_agents_rewardsMask = np.empty((sgv['num_episodes'], sgv['num_agents']), dtype=object)  # 用于存储每个实验的每个代理的奖励数据
            for sgv['id_episode'] in range(sgv['num_episodes']):
                # 这里只计算最后一轮的 rewards，这里的 rewards 不是序列，而是重复累计的。
                arr_episodes_agents_rewardsValues[sgv['id_episode'], :] = df_v['rewards_values'][df_v['step'] == df_v['step'].max()].values
                arr_episodes_agents_rewardsMask[sgv['id_episode'], :] = df_v['rewards_mask'][df_v['step'] == df_v['step'].max()].values
                pass  # for

            dict_agents_rewards = {}
            for i in range(sgv['num_agents']):
                # 创建 DataFrame，包含 id_episode, rewards_values, rewards_mask
                df_agent_rewards = pd.DataFrame({
                    'id_episode': np.arange(sgv['num_episodes']),
                    'rewards_values': [arr_episodes_agents_rewardsValues[episode, i] for episode in range(sgv['num_episodes'])],
                    'rewards_mask': [arr_episodes_agents_rewardsMask[episode, i] for episode in range(sgv['num_episodes'])],
                })
                dict_agents_rewards[i] = df_agent_rewards

            ## 绘制强化学习收敛曲线图
            for k, v in dict_agents_rewards.items():
                RlUtils.plot_convergence_curve(
                    arr_reward=v['rewards_values'].values,
                    save_path=sgv['folderpath_visualize_强化学习收敛曲线'],
                    agent_id=k,
                    use_moving_average=False,
                )

        # else:
        #     raise ValueError("`list_agents_data_filename_para_01` 必须包含 'AB' 选项")
        #     pass  # if

        pass  # if

    # %%
    if sgv['is_ignore_warning']:
        warnings.filterwarnings("default")  # 恢复警告

    pass  # function


def process_one_heatmap(args):
    """
    处理需要绘制的单个热力图。

    首先获取相关的节点与边信息，然后用 matplotlib 绘制，最后保存。

    参数元组 args 信息如下：
        - args[0]: sgv (dict): 一个字典，包含了所有的参数。
        - args[1]: df_1D_panel_row (pandas.DataFrame): 数据表1D之行。
        - args[2]: df_1D_panel_col (pandas.DataFrame): 数据表1D之列。
        - args[3]: df_2D_panel (pandas.DataFrame): 数据表2D。
        - args[4]: d (pandas.Series): 数据类别。
        - args[5]: i_exp (int): 实验编号。
        - args[6]: t (int): 时间。
        - args[7]: i (int): 数据类别编号。

    Args:
          args: 一个元组，包含了需要的参数。

    Returns:
        None

    """
    sgv, df_1D_panel_row, df_1D_panel_col, df_2D_panel, d, i_exp, t, i = args

    ## 获取相关的节点与边信息
    data_vis_one_time_heatmap = generate_one_interbank_matrix_heatmaps_data_info(df_1D_panel_row, df_1D_panel_col, df_2D_panel, d['colormap'], d['relations'], t, d['data_name'], sgv['vis'])

    ## 用 matplotlib 绘制
    fig_heatmap = draw_one_interbank_matrix_heatmaps(data_vis_one_time_heatmap, sgv['vis'])
    fig_heatmap.savefig(Path(sgv['folderpath_plots_single_heatmaps'], f"IB-exp={str(i_exp)}+data={d['data_name'][0]}_{d['data_name'][1]}_{d['data_name'][2]}+{sgv['vis']['name_time']}={str(t)}.pdf"))  # 保存

    pass  # function


def process_one_graph(args):
    """
    处理需要绘制的单个网络图。

    首先获取相关的节点与边信息，然后用 NetworkX 绘制，最后保存。

    参数元组 args 信息如下：
        - args[0]: sgv (dict): 一个字典，包含了所有的参数。
        - args[1]: df_BB_panel (pandas.DataFrame): 数据表BB。
        - args[2]: df_IB_panel (pandas.DataFrame): 数据表IB。
        - args[3]: data_vis_one_time_graph (dict): 用于绘制网络图的数据。
        - args[4]: i_exp (int): 实验编号。
        - args[5]: d (pandas.Series): 数据类别。
        - args[6]: t (int): 时间。

    Args:
        args: 一个元组，包含了需要的参数。

    Returns:
        None

    """
    sgv, df_BB_panel, df_IB_panel, data_vis_one_time_graph, i_exp, d, t = args

    ## 获取相关的节点与边信息
    data_vis_one_time_graph = generate_one_interbank_graph_data_info(df_BB_panel, df_IB_panel, data_vis_one_time_graph, t, d, sgv['vis'])

    ## 用 NetworkX 绘制
    fig_graph = draw_one_interbank_flow_graph(data_vis_one_time_graph)
    fig_graph.savefig(Path(sgv['folderpath_plots_single_graphs'], 'IB-exp=' + str(i_exp) + '+data=' + d + '+' + sgv['vis']['name_time'] + '=' + str(t) + '.pdf'))  # 保存

    pass  # function


def process_one_balanceSheet(args):
    """
    处理需要绘制的单个资产负债表。

    首先获取相关的节点与边信息，然后用 drawsvg 绘制，最后保存。

    参数元组 args 信息如下：
        - args[0]: sgv (dict): 一个字典，包含了所有的参数。
        - args[1]: df_BB_panel (pandas.DataFrame): 数据表BB。
        - args[2]: data_vis_one_bank_BalanceSheet (dict): 用于绘制资产负债表的数据。
        - args[3]: i_exp (int): 实验编号。
        - args[4]: i (int): 银行编号。
        - args[5]: t (int): 时间。

    Args:
        args: 一个元组，包含了需要的参数。

    Returns:
          None

    """

    sgv, df_BB_panel, data_vis_one_bank_BalanceSheet, i_exp, i, t = args

    ## 生成绘制资产负债表所需的数据
    data_vis_one_bank_BalanceSheet = generate_one_bank_accounts_data(df_BB_panel, data_vis_one_bank_BalanceSheet, t, i, sgv['vis'])

    ## 用 drawsvg 绘制资产负债表图
    svg_one_bank_balanceSheet = draw_one_bank_BalanceSheet(data_vis_one_bank_BalanceSheet, sgv['vis'], width=sgv['vis']['one_bank_BalanceSheet_width'], height=sgv['vis']['one_bank_BalanceSheet_height'], title_height=sgv['vis']['one_bank_BalanceSheet_title_height'], border=sgv['vis']['one_bank_BalanceSheet_border'])
    svg_one_bank_balanceSheet.save_svg(Path(sgv['folderpath_plots_single_balanceSheets'], 'BB-exp=' + str(i_exp) + '+name=' + data_vis_one_bank_BalanceSheet['others']['bank_name'] + '+' + sgv['vis']['name_time'] + '=' + str(t) + '.svg'))  # 保存

    pass  # function


if __name__ == '__main__':
    # 从命令行参数获取配置字典
    sgv_base64 = sys.argv[1]
    sgv_pkl = base64.b64decode(sgv_base64)
    sgv = pickle.loads(sgv_pkl)

    main(sgv)
