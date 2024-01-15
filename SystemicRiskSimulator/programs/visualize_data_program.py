"""
可视化结果程序。

BUG 2023-07-11：
改标注在图上的文本语言为英文。暂时不建议用中文标注在图上。因为如果使用中文，不能任意设置字体族；

Args:
    sgv: dict

Returns:
    None

"""

# from SystemicRiskSimulator.external_packages import sys, pickle, base64, Pool, multiprocessing
# from SystemicRiskSimulator.core.functions.fun_visualize_data import fun_visualize_data

from SystemicRiskSimulator.tools.visualization_tools import generate_one_interbank_matrix_heatmaps_data_info, draw_one_interbank_matrix_heatmaps, generate_one_interbank_graph_data_info, draw_one_interbank_flow_graph, generate_one_bank_accounts_data, draw_one_bank_BalanceSheet, merged_and_bind_figs_to_a_pdf_file
from SystemicRiskSimulator.external_packages import platform, Path, re, glob, pd, np, deepcopy, sys, pickle, base64, Pool, multiprocessing, warnings


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
    if sgv['need_visualization']:
        sgv['is_installed_packages_for_visualization'] = Tools._check_and_install_packages(sgv['visualization_packages'])  # 安装可视化所需的第三方工具包

    # %% [markdown] 预处理数据

    # %%

    ## NOTE 导入包
    from matplotlib import pyplot as plt
    import igraph as ig
    import matplotlib.pyplot as plt
    # import drawsvg as dw
    # import fitz
    # from svglib.svglib import svg2rlg
    # from reportlab.graphics import renderPDF
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    import matplotlib.font_manager as fm
    # from matplotlib.font_manager import FontProperties

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

    ### 配置 igraph
    ig.config['plotting.backend'] = 'matplotlib'
    ig.config.save()

    # %% ## NOTE 配置导入导出文件夹

    # %%

    ### 处理相关导入导出文件夹

    # sgv['folderpath_experiments'] = Path(sgv['folderpath_project'], sgv['folderpath_root_experiments'], sgv['foldername_experiments'])
    # sgv['folderpath_experiments_output_data'] = Path(sgv['folderpath_experiments'], sgv['foldername_experiments_output_data'])
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

    # %% [markdown] # NOTE 导入Pandas格式的实验结果数据，然后转换为面板形式的数据，导出PKL、CSV、xlsx 格式数据。

    # %%

    print("执行：")

    if (sgv['visulization_process']['导入Pandas格式的实验结果数据转换为面板形式再导出']):
        print("导入Pandas格式的实验结果数据转换为面板形式再导出")

        list_filepath_pkl_BB = list(sgv['folderpath_experiments_output_data'].glob('BB_exp*.pkl'))  # 获取实验组输出数据pkl格式之BB数据之文件列表
        for filepath_pkl_BB in list_filepath_pkl_BB:
            df_BB = pd.read_pickle(filepath_pkl_BB)
            num_agent = df_BB['id_agent'][0].shape[0]  # 获取个体数
            df_BB_panel = df_BB.applymap(lambda x: x.flatten() if hasattr(x, 'flatten') else x)  # 压平二维数组

            ## 转换数据格式为numpy字符串格式
            list_columns_for_transform_datatype = [
                v for i, v in enumerate(df_BB_panel.columns) if (
                        df_BB_panel[v].dtype == np.dtype('object') and
                        type(df_BB_panel[v][0]) == str
                )
            ]
            for i in range(df_BB_panel.__len__()):
                df_BB_panel[list_columns_for_transform_datatype[0]][i] = np.str_(df_BB_panel[list_columns_for_transform_datatype[0]][i])  # BUG Pandas包警告

            list_columns_for_explode = [
                v for i, v in enumerate(df_BB_panel.columns) if (
                        df_BB_panel[v].dtype == np.dtype('object') and
                        df_BB_panel[v][0].size == num_agent
                )
            ]  # 获取需要展平的列
            df_BB_panel = df_BB_panel.explode(list_columns_for_explode)  # 展平，面板化数据框

            df_BB_panel.insert(0, 'id', range(len(df_BB_panel)))  # 添加id列
            df_BB_panel.insert(1, 'id_data', np.repeat(range(len(df_BB_panel) // num_agent), num_agent))  # 添加id_data列

            df_BB_panel = df_BB_panel.reset_index(drop=True)  # 重置索引

            filename_pkl_BB = Path(filepath_pkl_BB).name
            filename_pkl_BB_panel = filename_pkl_BB.replace('BB_', 'BB_panel_')
            filepath_pkl_BB_panal = Path(sgv['folderpath_plots'], filename_pkl_BB_panel)  # 面板数据文件路径
            df_BB_panel.to_pickle(Path(filepath_pkl_BB_panal))  # 导出为 pkl 格式
            df_BB_panel.to_csv(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.csv'), index=False)  # 导出为 csv 格式；
            with pd.ExcelWriter(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.xlsx')) as writer:  # 导出为 xlsx 格式
                df_BB_panel.to_excel(writer, sheet_name='BB_panel')
                pass  # with
            pass  # for

        list_filepath_pkl_IB = list(sgv['folderpath_experiments_output_data'].glob('IB_exp*.pkl'))  # 获取实验组输出数据pkl格式之IB数据之文件列表
        for filepath_pkl_IB in list_filepath_pkl_IB:
            df_IB = pd.read_pickle(filepath_pkl_IB)
            df_IB_panel = deepcopy(df_IB)

            ## 转换数据格式为numpy字符串格式
            list_columns_for_transform_datatype = [
                v for i, v in enumerate(df_IB_panel.columns) if (
                        df_IB_panel[v].dtype == np.dtype('object') and
                        type(df_IB_panel[v][0]) == str
                )
            ]
            for i in range(df_IB_panel.__len__()):
                df_IB_panel[list_columns_for_transform_datatype[0]][i] = np.str_(df_IB_panel[list_columns_for_transform_datatype[0]][i])  # BUG Pandas包警告

            ## 转换信息列表为矩阵形式，插入数据框  #HACK 能否用现成的功能函数代替？
            list_columns_for_transform = [
                v for i, v in enumerate(df_IB_panel.columns) if (
                        df_IB_panel[v].dtype == np.dtype('object') and
                        df_IB_panel[v][0].dtype == np.dtype('object')
                )
            ]
            for v1 in list_columns_for_transform:  # BUG Pandas包警告
                for i2 in range(df_IB_panel[v1].size):
                    m = np.full((num_agent, num_agent), False)
                    if df_IB_panel.loc[i2, v1] is []:
                        df_IB_panel.loc[i2, v1] = np.nan
                        continue
                    for i3, v3 in enumerate(df_IB_panel.loc[i2, v1]):
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
                    df_IB_panel[v1][i2] = m  # 赋值矩阵给数据框之元素，于数据框之相应的位置
                    pass  # for
                pass  # for

            ## 生成agent矩阵之坐标，以矩阵形式，插入数据框
            row_coord, col_coord = np.mgrid[0:num_agent:1, 0:num_agent:1]
            df_IB_panel.insert(loc=df_IB_panel.columns.get_loc('id_agent') + 1, column="col", value=np.dtype('object'))
            for i, _ in enumerate(df_IB_panel.col):
                df_IB_panel.col[i] = col_coord.astype('int16')
            df_IB_panel.insert(loc=df_IB_panel.columns.get_loc('id_agent') + 1, column="row", value=np.dtype('object'))
            for i, _ in enumerate(df_IB_panel.row):
                df_IB_panel.row[i] = row_coord.astype('int16')

            list_columns_for_explode = [
                v for i, v in enumerate(df_IB_panel.columns) if (
                        df_IB_panel[v].dtype == np.dtype('object') and
                        df_IB_panel[v][0].size == num_agent ** 2
                )
            ]  # 获取需要展平的列
            df_IB_panel = df_IB_panel.explode(list_columns_for_explode).explode(list_columns_for_explode)  # 展平，面板化数据框

            df_IB_panel.insert(0, 'id', range(len(df_IB_panel)))  # 添加id列
            df_IB_panel.insert(1, 'id_data', np.repeat(range(len(df_IB_panel) // num_agent ** 2), num_agent ** 2))  # 添加id_data列

            df_IB_panel = df_IB_panel.reset_index(drop=True)  # 重置索引

            filename_pkl_IB = Path(filepath_pkl_IB).name
            filename_pkl_IB_panel = filename_pkl_IB.replace('IB_', 'IB_panel_')
            filepath_pkl_IB_panal = Path(sgv['folderpath_plots'], filename_pkl_IB_panel)  # 面板数据文件路径
            df_IB_panel.to_pickle(Path(filepath_pkl_IB_panal))  # 导出为 pkl 格式
            df_IB_panel.to_csv(Path(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.csv')), index=False)  # 导出为 csv 格式；
            with pd.ExcelWriter(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.xlsx')) as writer:  # 导出为 xlsx 格式
                df_IB_panel.to_excel(writer, sheet_name='IB_panel')
                pass  # with
            pass  # for

        pass  # if 导入Pandas格式的实验结果数据转换为面板形式再导出

    # %% [markdown] # NOTE 导入面板形式的CSV数据预处理（备选）

    # %%

    if (sgv['visulization_process']['导入面板形式的CSV数据预处理']):

        # NOTE：如果需要读取CSV格式处理数据的话则使用该程序段。#BUG 可能已经过时尚未适配。不建议使用！

        print("导入面板形式的CSV数据预处理")

        list_filepath_csv_panel = list(sgv['folderpath_plots'].glob('*.csv'))  # 获取实验组输出数据csv格式的文件列表

        ## 排序，优先按照银行名称，其次按照时间。
        match_pattern_in_vertical_direction = r'(?<=[IB]B_panel_exp=).+?(?=[(\.csv)])'
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
            csv_BB_00 = pd.read_csv(Path(sgv['folderpath_plots'], 'BB_panel_exp=' + str(i_exp) + '.csv'))
            csv_IB_00 = pd.read_csv(Path(sgv['folderpath_plots'], 'IB_panel_exp=' + str(i_exp) + '.csv'))

            ## 预处理数据表

            ## 去除空列、调整列顺序
            csv_BB_10 = deepcopy(csv_BB_00.loc[:, ~csv_BB_00.columns.str.contains('^Unnamed')])
            csv_IB_10 = deepcopy(csv_IB_00.loc[:, ~csv_IB_00.columns.str.contains('^Unnamed')])

            ## 提前列`row`、`col`
            cols_sorted_10 = ['id_agent']
            cols_sorted_10 = cols_sorted_10 + [s for s in csv_BB_10.columns if not s in cols_sorted_10]
            df_BB_panel = csv_BB_10[cols_sorted_10]
            cols_sorted_10 = ['row', 'col']
            cols_sorted_10 = cols_sorted_10 + [s for s in csv_IB_10.columns if not s in cols_sorted_10]
            df_IB_panel = csv_IB_10[cols_sorted_10]

            ## 一些变量
            num_BB_id = len(df_BB_panel)  # 数据表BB之行数
            num_IB_id = len(df_IB_panel)  # 数据表IB之行数
            num_idData = df_BB_panel['id_data'].max() + 1  # 数据表之数据id个数
            num_round = df_BB_panel['round'].max() + 1  # 总的轮次数（是从0开始计数的)
            num_step = num_idData  # 总的步进数（是从0开始计数的)

            ## 根据时间粒度参数，确定时间轴名称及其长度
            if sgv['vis']['time_granularity'] == '步进粒度':
                sgv['vis']['name_time'] = 'id_data'  # BUG 这个是否正确？是否应该改成 'step' ？
                sgv['vis']['num_time'] = num_step
            elif sgv['vis']['time_granularity'] == '轮次粒度':
                sgv['vis']['name_time'] = 'round'
                sgv['vis']['num_time'] = num_round
            else:
                raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                pass  # if
            sgv['vis']['num_items_in_a_time_in_BB'] = num_BB_id // num_idData  # BB之一个运行时间片之项目数
            sgv['vis']['num_items_in_a_time_in_IB'] = num_IB_id // num_idData  # IB之一个运行轮次之项目数
            num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
            num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

            pass  # for

        pass  # if 导入面板形式的CSV数据预处理

    # %% [markdown] ##  NOTE 导入面板形式的PKL数据预处理

    # %%

    if (sgv['visulization_process']['读取面板形式的PKL格式的文件']):
        # 依次读取面板形式的PKL格式的文件，预处理每次实验

        print("读取面板形式的PKL格式的文件")

        list_fig_files = list(sgv['folderpath_plots'].glob('*_panel_*.pkl'))  # 获取实验组输出数据pkl格式之文件列表

        ## 排序，优先按照银行名称，其次按照时间。
        match_pattern_in_vertical_direction = r'(?<=[IB]B_panel_exp=).+?(?=[(\.pkl)])'
        match_pattern_in_horizontal_direction = r'[IB]B'
        sorted_pkl_panel_file_list = sorted(list_fig_files, key=lambda name: (
            int(re.search(match_pattern_in_vertical_direction, str(name))[0]),
            re.search(match_pattern_in_horizontal_direction, str(name))[0],
        ))

        ## 获取所有实验之索引
        experiments_indices = []
        for filepath in sorted_pkl_panel_file_list:
            match = re.search(r'exp=(\d+)', str(filepath))
            if match:
                experiments_indices.append(int(match.group(1)))
            pass  # for
        experiments_indices = sorted(list(set(experiments_indices)))  # 去重

        ## 获取需要做的实验组之索引
        if sgv['vis']['list_idsExperiment_to_vis'] is None:
            experiments_indices_to_vis = experiments_indices
        else:
            experiments_indices_to_vis = sgv['vis']['list_idsExperiment_to_vis']
            pass

        pass  # if 读取面板形式的PKL格式的文件

    # %% [markdown] ## NOTE 绘制矩阵热图
    # 依次按照每个银行间数据类别、时间，分别绘制单独的银行间资金流网络图

    # %%

    if (sgv['visulization_process']['读取面板形式的PKL格式的文件'] or sgv['visulization_process']['导入面板形式的CSV数据预处理']):

        if (sgv['visulization_process']['绘制矩阵热图']):
            print("准备绘制矩阵热图")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_single_heatmaps'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

            # with Pool() as p:
            #     p.map(fun_visualize_data, [sgv])
            #     # fun_visualize_data(sgv)

            for i_exp in experiments_indices_to_vis:

                df_BB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'BB_panel_exp=' + str(i_exp) + '.pkl'))
                df_IB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'IB_panel_exp=' + str(i_exp) + '.pkl'))

                ## 一些变量
                num_BB_id = len(df_BB_panel)  # 数据表BB之行数
                num_IB_id = len(df_IB_panel)  # 数据表IB之行数
                num_idData = df_BB_panel['id_data'].max() + 1  # 数据表之数据id个数
                num_round = df_BB_panel['round'].max() + 1  # 总的轮次数（是从0开始计数的)
                num_step = num_idData  # 总的步进数（是从0开始计数的)
                ## 根据时间粒度参数，确定时间轴名称及其长度
                if sgv['vis']['time_granularity'] == '步进粒度':
                    sgv['vis']['name_time'] = 'step'
                    sgv['vis']['num_time'] = num_step
                elif sgv['vis']['time_granularity'] == '轮次粒度':
                    sgv['vis']['name_time'] = 'round'
                    sgv['vis']['num_time'] = num_round
                else:
                    raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                    pass  # if
                sgv['vis']['num_items_in_a_time_in_BB'] = num_BB_id // num_idData  # BB之一个运行时间片之项目数
                sgv['vis']['num_items_in_a_time_in_IB'] = num_IB_id // num_idData  # IB之一个运行轮次之项目数
                num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
                num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

                print("绘制矩阵热图：实验" + str(i_exp))

                sgv['vis']['zh_font_family'] = zh_font_family
                sgv['vis']['en_font_family'] = en_font_family

                df_data_types = pd.DataFrame(sgv['vis']['list_dataTypes_for_heatmaps'])

                ### 计算各银行主体之代表性的类型之数据之最大值和最小值
                sgv['vis']['max_BB_value_in_all_panel'] = df_BB_panel['A_IB_all'].max()
                sgv['vis']['min_BB_value_in_all_panel'] = 0

                ### 计算各银行主体间之代表性的类型之数据之最大值和最小值
                sgv['vis']['max_IB_value_in_all_panel'] = df_IB_panel['A_IB'].max()
                sgv['vis']['min_IB_value_in_all_panel'] = 0

                ## 创建一个任务列表，其中每个任务都是一个元组，包含所有需要传递给函数的参数
                tasks = []
                for i, d in df_data_types.iterrows():
                    for t in range(sgv['vis']['num_time']):
                        tasks.append((sgv, df_BB_panel, df_IB_panel, d, i_exp, t, i))
                        pass  # for
                    pass  # for

                ## 绘图
                if sgv['is_enable_multiprocessing']:  # 多进程并行处理
                    num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
                    with Pool(num_cores) as p:
                        p.map(process_one_heatmap, tasks)
                        pass  # with
                else:  # 串行处理
                    for i in range(len(tasks)):
                        process_one_heatmap(tasks[i])
                        pass  # for

                pass  # for

            pass  # if 绘制矩阵热图

        # %% [markdown] ## #NOTE 拼接矩阵热图
        # 导入各自的矩阵热图，按照横向数据类别纵向时间，拼接成大图

        # %%

        if (sgv['visulization_process']['拼接矩阵热图']):
            print("准备拼接矩阵热图")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_makeup_heatmaps'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

            for i_exp in experiments_indices_to_vis:

                df_BB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'BB_panel_exp=' + str(i_exp) + '.pkl'))
                df_IB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'IB_panel_exp=' + str(i_exp) + '.pkl'))

                ## 一些变量
                num_BB_id = len(df_BB_panel)  # 数据表BB之行数
                num_IB_id = len(df_IB_panel)  # 数据表IB之行数
                num_idData = df_BB_panel['id_data'].max() + 1  # 数据表之数据id个数
                num_round = df_BB_panel['round'].max() + 1  # 总的轮次数（是从0开始计数的)
                num_step = num_idData  # 总的步进数（是从0开始计数的)
                ## 根据时间粒度参数，确定时间轴名称及其长度
                if sgv['vis']['time_granularity'] == '步进粒度':
                    sgv['vis']['name_time'] = 'step'
                    sgv['vis']['num_time'] = num_step
                elif sgv['vis']['time_granularity'] == '轮次粒度':
                    sgv['vis']['name_time'] = 'round'
                    sgv['vis']['num_time'] = num_round
                else:
                    raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                    pass  # if
                sgv['vis']['num_items_in_a_time_in_BB'] = num_BB_id // num_idData  # BB之一个运行时间片之项目数
                sgv['vis']['num_items_in_a_time_in_IB'] = num_IB_id // num_idData  # IB之一个运行轮次之项目数
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

                list_fig_files = glob.glob(str(sgv['folderpath_plots_single_heatmaps'] / f'*exp={i_exp}*.pdf'))  # 获取所有当次实验文件列表

                merged_pdf = merged_and_bind_figs_to_a_pdf_file(order_of_variable_mean_in_horizontal_and_vertical_direction, order_of_paging_in_horizontal_and_vertical_direction, order_of_match_pattern_in_horizontal_and_vertical_direction, list_fig_files, i_exp)

                ## 保存
                merged_pdf.save(Path(sgv['folderpath_plots_makeup_heatmaps'], 'IB_exp=' + str(i_exp) + '.pdf'))
                merged_pdf.close()

                pass  # for

            pass  # if 拼接矩阵热图

        # %% [markdown] ## #NOTE 绘制资金流网络图
        # 依次按照每个银行间数据类别、时间，分别绘制单独的银行间资金流网络图

        # %%

        if (sgv['visulization_process']['绘制资金流网络图']):

            print("准备绘制资金流网络图")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_single_graphs'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

            for i_exp in experiments_indices_to_vis:

                df_BB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'BB_panel_exp=' + str(i_exp) + '.pkl'))
                df_IB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'IB_panel_exp=' + str(i_exp) + '.pkl'))

                ## 一些变量
                num_BB_id = len(df_BB_panel)  # 数据表BB之行数
                num_IB_id = len(df_IB_panel)  # 数据表IB之行数
                num_idData = df_BB_panel['id_data'].max() + 1  # 数据表之数据id个数
                num_round = df_BB_panel['round'].max() + 1  # 总的轮次数（是从0开始计数的)
                num_step = num_idData  # 总的步进数（是从0开始计数的)
                ## 根据时间粒度参数，确定时间轴名称及其长度
                if sgv['vis']['time_granularity'] == '步进粒度':
                    sgv['vis']['name_time'] = 'step'
                    sgv['vis']['num_time'] = num_step
                elif sgv['vis']['time_granularity'] == '轮次粒度':
                    sgv['vis']['name_time'] = 'round'
                    sgv['vis']['num_time'] = num_round
                else:
                    raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                    pass  # if
                sgv['vis']['num_items_in_a_time_in_BB'] = num_BB_id // num_idData  # BB之一个运行时间片之项目数
                sgv['vis']['num_items_in_a_time_in_IB'] = num_IB_id // num_idData  # IB之一个运行轮次之项目数
                num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
                num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

                print("绘制资金流网络图：实验" + str(i_exp))

                sgv['vis']['zh_font_family'] = zh_font_family
                sgv['vis']['en_font_family'] = en_font_family

                ### 计算各银行主体之代表性的类型之数据之最大值和最小值
                sgv['vis']['max_BB_value_in_all_panel'] = df_BB_panel['A_all'].max()
                sgv['vis']['min_BB_value_in_all_panel'] = 0

                ### 计算各银行主体间之代表性的类型之数据之最大值和最小值
                sgv['vis']['max_IB_value_in_all_panel'] = df_IB_panel['A_IB'].max()
                sgv['vis']['min_IB_value_in_all_panel'] = 0

                ## 创建一个任务列表，其中每个任务都是一个元组，包含所有需要传递给函数的参数
                tasks = []
                for d in sgv['vis']['list_dataNames_for_graph_figs']:
                    ## 设置不同边集对应的属性
                    list_data_edgeTypes = [
                        dict(
                            edge_type=d,
                            edge_color='#CCCCCC',
                            edge_width=5,
                        ),
                        dict(
                            edge_type='Shock_IB_def',
                            edge_color='#FF0000',
                            edge_width=5,
                        ),
                        dict(
                            edge_type='Shock_IB_run_ilq',
                            edge_color='#0000FF',
                            edge_width=5,
                        ),
                        dict(
                            edge_type='Shock_IB_run_br',
                            edge_color='#ED00FF',
                            edge_width=5,
                        ),
                        dict(
                            edge_type='Bo_IB',
                            edge_color='#E7C300',
                            edge_width=5,
                        ),
                    ]

                    for t in range(sgv['vis']['num_time']):
                        ## 初始化参数
                        data_vis_one_time_graph = {}
                        data_vis_one_time_graph['edge_types'] = pd.DataFrame(list_data_edgeTypes)
                        data_vis_one_time_graph['vertices'] = pd.DataFrame()
                        data_vis_one_time_graph['edges'] = pd.DataFrame()

                        tasks.append((sgv, df_BB_panel, df_IB_panel, data_vis_one_time_graph, i_exp, d, t))
                        pass  # for
                    pass  # for

                ## 绘图
                if sgv['is_enable_multiprocessing']:  # 多进程并行处理
                    num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
                    with Pool(num_cores) as p:
                        p.map(process_one_graph, tasks)
                        pass  # with
                else:  # 串行处理
                    for i in range(len(tasks)):
                        process_one_graph(tasks[i])
                        pass  # for

                pass  # for  实验编号

            pass  # if 绘制资金流网络图

        # %% [markdown] ## #NOTE 拼接资金流网络图
        # 导入各自的网络图，按照横向数据类别纵向时间，拼接成大图

        # %%

        if (sgv['visulization_process']['拼接资金流网络图']):
            print("准备拼接资金流网络图")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_makeup_graphs'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

            for i_exp in experiments_indices_to_vis:

                df_BB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'BB_panel_exp=' + str(i_exp) + '.pkl'))
                df_IB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'IB_panel_exp=' + str(i_exp) + '.pkl'))

                ## 一些变量
                num_BB_id = len(df_BB_panel)  # 数据表BB之行数
                num_IB_id = len(df_IB_panel)  # 数据表IB之行数
                num_idData = df_BB_panel['id_data'].max() + 1  # 数据表之数据id个数
                num_round = df_BB_panel['round'].max() + 1  # 总的轮次数（是从0开始计数的)
                num_step = num_idData  # 总的步进数（是从0开始计数的)
                ## 根据时间粒度参数，确定时间轴名称及其长度
                if sgv['vis']['time_granularity'] == '步进粒度':
                    sgv['vis']['name_time'] = 'step'
                    sgv['vis']['num_time'] = num_step
                elif sgv['vis']['time_granularity'] == '轮次粒度':
                    sgv['vis']['name_time'] = 'round'
                    sgv['vis']['num_time'] = num_round
                else:
                    raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                    pass  # if
                sgv['vis']['num_items_in_a_time_in_BB'] = num_BB_id // num_idData  # BB之一个运行时间片之项目数
                sgv['vis']['num_items_in_a_time_in_IB'] = num_IB_id // num_idData  # IB之一个运行轮次之项目数
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

                list_fig_files = glob.glob(str(sgv['folderpath_plots_single_graphs'] / f'*exp={i_exp}*.pdf'))  # 获取所有当次实验文件列表

                merged_pdf = merged_and_bind_figs_to_a_pdf_file(order_of_variable_mean_in_horizontal_and_vertical_direction, order_of_paging_in_horizontal_and_vertical_direction, order_of_match_pattern_in_horizontal_and_vertical_direction, list_fig_files, i_exp)

                ## 保存
                merged_pdf.save(Path(sgv['folderpath_plots_makeup_graphs'], 'IB_exp=' + str(i_exp) + '.pdf'))
                merged_pdf.close()

                pass  # for  实验编号

            pass  # if 拼接资金流网络图

        # %% [markdown] ## #NOTE 绘制资产负债表
        # 依次按照时间、银行，分别绘制单独的资产负债表（资产负债表尺寸不一样大，尺寸按照比例）

        # %%
        if (sgv['visulization_process']['绘制资产负债表']):

            print("准备绘制资产负债表")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_single_balanceSheets'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

            for i_exp in experiments_indices_to_vis:

                df_BB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'BB_panel_exp=' + str(i_exp) + '.pkl'))
                df_IB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'IB_panel_exp=' + str(i_exp) + '.pkl'))

                ## 一些变量
                num_BB_id = len(df_BB_panel)  # 数据表BB之行数
                num_IB_id = len(df_IB_panel)  # 数据表IB之行数
                num_idData = df_BB_panel['id_data'].max() + 1  # 数据表之数据id个数
                num_round = df_BB_panel['round'].max() + 1  # 总的轮次数（是从0开始计数的)
                num_step = num_idData  # 总的步进数（是从0开始计数的)
                ## 根据时间粒度参数，确定时间轴名称及其长度
                if sgv['vis']['time_granularity'] == '步进粒度':
                    sgv['vis']['name_time'] = 'step'
                    sgv['vis']['num_time'] = num_step
                elif sgv['vis']['time_granularity'] == '轮次粒度':
                    sgv['vis']['name_time'] = 'round'
                    sgv['vis']['num_time'] = num_round
                else:
                    raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                    pass  # if
                sgv['vis']['num_items_in_a_time_in_BB'] = num_BB_id // num_idData  # BB之一个运行时间片之项目数
                sgv['vis']['num_items_in_a_time_in_IB'] = num_IB_id // num_idData  # IB之一个运行轮次之项目数
                num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
                num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

                print("绘制资产负债表：实验" + str(i_exp))

                sgv['vis']['zh_font_family'] = zh_font_family
                sgv['vis']['en_font_family'] = en_font_family

                ## NOTE：设置绘制资产负债表相关的数据

                ### 资产负债表账户数据（字典列表形式）
                list_accounts_data = [
                    dict(
                        data_type='asset',
                        level='level 3',
                        subject='A_P',
                        value=0.0,
                        fill_color='#FBE7CF',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='asset',
                        level='level 3',
                        subject='A_Q',
                        value=0.0,
                        fill_color='#DDE8FA',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='asset',
                        level='level 3',
                        subject='A_R',
                        value=0.0,
                        fill_color='#DFC942',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='asset',
                        level='level 3',
                        subject='A_other',
                        value=0.0,
                        fill_color='#FFFFFF',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='asset',
                        level='level 3',
                        subject='A_IB_all',
                        value=0.0,
                        fill_color='#F1D0CD',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='asset',
                        level='level 2',
                        subject='A_exIB',
                        value=0.0,
                        fill_color='#F9F7EE',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='asset',
                        level='level 2',
                        subject='A_IB_all',
                        value=0.0,
                        fill_color='#F1D0CD',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='asset',
                        level='level 1',
                        subject='A_all',
                        value=0.0,
                        fill_color='#EEEEEE',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='liability',
                        level='level 3',
                        subject='Z_D',
                        value=0.0,
                        fill_color='#DFD6E6',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='liability',
                        level='level 3',
                        subject='Z_IB_all',
                        value=0.0,
                        fill_color='#D9E8D6',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='liability',
                        level='level 2',
                        subject='Z_exIB',
                        value=0.0,
                        fill_color='#DFD6E6',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='liability',
                        level='level 2',
                        subject='Z_IB_all',
                        value=0.0,
                        fill_color='#D9E8D6',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='liability',
                        level='level 1',
                        subject='Z_all',
                        value=0.0,
                        fill_color='#EEEEEE',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='equity',
                        level='level 3',
                        subject='E_all',
                        value=0.0,
                        fill_color='#FFFF98',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='equity',
                        level='level 2',
                        subject='E_all',
                        value=0.0,
                        fill_color='#FFFF98',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='equity',
                        level='level 1',
                        subject='E_all',
                        value=0.0,
                        fill_color='#FFFF98',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                ]

                ### 冲击数据（字典列表形式）
                list_shocks_data = [
                    dict(
                        data_type='shock_def_t',
                        level='level 3',
                        subject='Shock_P_def_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_P',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_def_t',
                        level='level 3',
                        subject='Shock_IB_def_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_def_t',
                        level='level 2',
                        subject='Shock_P_def_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_exIB',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_def_t',
                        level='level 2',
                        subject='Shock_IB_def_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_def_t',
                        level='level 1',
                        subject='Shock_def_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_t',
                        level='level 3',
                        subject='Shock_IB_run_ilq_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_t',
                        level='level 3',
                        subject='Shock_IB_run_br_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_t',
                        level='level 3',
                        subject='Shock_D_run_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_D',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_t',
                        level='level 2',
                        subject='Shock_IB_run_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_t',
                        level='level 2',
                        subject='Shock_D_run_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_exIB',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_t',
                        level='level 1',
                        subject='Shock_run_t',
                        value=0.0,
                        fill_color='#FF0000',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_def_s',
                        level='level 3',
                        subject='Shock_D_def_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_D',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_def_s',
                        level='level 3',
                        subject='Shock_IB_def_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_def_s',
                        level='level 2',
                        subject='Shock_D_def_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_exIB',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_def_s',
                        level='level 2',
                        subject='Shock_IB_def_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_def_s',
                        level='level 1',
                        subject='Shock_def_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_s',
                        level='level 3',
                        subject='Shock_P_run_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_P',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_s',
                        level='level 3',
                        subject='Shock_IB_run_ilq_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_s',
                        level='level 3',
                        subject='Shock_IB_run_br_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_s',
                        level='level 2',
                        subject='Shock_P_run_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_exIB',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_s',
                        level='level 2',
                        subject='Shock_IB_run_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='shock_run_s',
                        level='level 1',
                        subject='Shock_run_s',
                        value=0.0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                ]

                ### 损失数据
                list_losses_data = [
                    dict(
                        data_type='loss',
                        level='level 3',
                        subject='Loss_exIB_def_t',
                        value=0.0,
                        fill_color='#808080',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_P',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='loss',
                        level='level 3',
                        subject='Loss_IB_def_t',
                        value=0.0,
                        fill_color='#808080',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='loss',
                        level='level 2',
                        subject='Loss_def_t',
                        value=0.0,
                        fill_color='#808080',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_exIB',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='loss',
                        level='level 1',
                        subject='Loss_t',
                        value=0.0,
                        fill_color='#808080',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                ]

                ### 违约数据
                list_default_data = [
                    dict(
                        data_type='default',
                        level='level 3',
                        subject='Default_exIB_s',
                        value=0.0,
                        fill_color='#A68E17',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_D',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='default',
                        level='level 3',
                        subject='Default_IB_s',
                        value=0.0,
                        fill_color='#A68E17',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='default',
                        level='level 2',
                        subject='Default_exIB_s',
                        value=0.0,
                        fill_color='#A68E17',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_exIB',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='default',
                        level='level 2',
                        subject='Default_IB_s',
                        value=0.0,
                        fill_color='#A68E17',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_IB_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                    dict(
                        data_type='default',
                        level='level 1',
                        subject='Default_s',
                        value=0.0,
                        fill_color='#A68E17',
                        stroke_color='gray',
                        stroke_width=1,
                        side='liability',
                        align='Z_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                ]

                ### 计算各银行主体之代表性的类型之数据之最大值和最小值
                sgv['vis']['max_BB_value_in_all_panel'] = df_BB_panel['A_all'].max()
                sgv['vis']['min_BB_value_in_all_panel'] = 0

                ## 创建一个任务列表，其中每个任务都是一个元组，包含所有需要传递给函数的参数
                tasks = []
                for i in range(sgv['vis']['num_items_in_a_time_in_BB']):
                    for t in range(sgv['vis']['num_time']):
                        ## 初始化数据
                        data_vis_one_bank_BalanceSheet = {}
                        data_vis_one_bank_BalanceSheet['accounts'] = pd.DataFrame(list_accounts_data)
                        data_vis_one_bank_BalanceSheet['shocks'] = pd.DataFrame(list_shocks_data)
                        data_vis_one_bank_BalanceSheet['losses'] = pd.DataFrame(list_losses_data)
                        data_vis_one_bank_BalanceSheet['defaults'] = pd.DataFrame(list_default_data)

                        tasks.append((sgv, df_BB_panel, data_vis_one_bank_BalanceSheet, i_exp, i, t))
                        pass  # for
                    pass  # for

                ## 绘图
                if sgv['is_enable_multiprocessing']:  # 多进程并行处理
                    num_cores = int(multiprocessing.cpu_count() * sgv['percent_core_for_multiprocessing'])  # 用于计算的 CPU 核心数
                    with Pool(num_cores) as p:
                        p.map(process_one_balanceSheet, tasks)  # 使用多进程并行处理
                        pass  # with
                else:  # 串行处理
                    for i in range(len(tasks)):
                        process_one_balanceSheet(tasks[i])
                        pass  # for

                pass  # for  实验编号

            pass  # if 绘制资产负债表

        # %% [markdown] ## #NOTE 拼接资产负债表
        # 导入各自的资产负债表，按照横向时间纵向银行，拼接成大图

        # %%

        if (sgv['visulization_process']['拼接资产负债表']):
            print("准备拼接资产负债表")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_makeup_balanceSheets'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

            for i_exp in experiments_indices_to_vis:

                df_BB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'BB_panel_exp=' + str(i_exp) + '.pkl'))
                df_IB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'IB_panel_exp=' + str(i_exp) + '.pkl'))

                ## 一些变量
                num_BB_id = len(df_BB_panel)  # 数据表BB之行数
                num_IB_id = len(df_IB_panel)  # 数据表IB之行数
                num_idData = df_BB_panel['id_data'].max() + 1  # 数据表之数据id个数
                num_round = df_BB_panel['round'].max() + 1  # 总的轮次数（是从0开始计数的)
                num_step = num_idData  # 总的步进数（是从0开始计数的)
                ## 根据时间粒度参数，确定时间轴名称及其长度
                if sgv['vis']['time_granularity'] == '步进粒度':
                    sgv['vis']['name_time'] = 'step'
                    sgv['vis']['num_time'] = num_step
                elif sgv['vis']['time_granularity'] == '轮次粒度':
                    sgv['vis']['name_time'] = 'round'
                    sgv['vis']['num_time'] = num_round
                else:
                    raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                    pass  # if
                sgv['vis']['num_items_in_a_time_in_BB'] = num_BB_id // num_idData  # BB之一个运行时间片之项目数
                sgv['vis']['num_items_in_a_time_in_IB'] = num_IB_id // num_idData  # IB之一个运行轮次之项目数
                num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
                num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

                print("拼接资产负债表：实验" + str(i_exp))

                ## 声明与定义变量
                match_pattern_of_agent_name = fr"(?<=name=).+?(?=[\+(\.svg)])"  # 匹配相关含义的变量之个体名称之正则表达式文本
                match_pattern_of_name_time = fr"(?<={sgv['vis']['name_time']}=).+?(?=[\+(\.svg)])"  # 匹配相关含义的变量之时间名称之正则表达式文本

                ## 设置参数
                ### #NOTE 这组配置表示按照银行横向，按照时间纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
                order_of_variable_mean_in_horizontal_and_vertical_direction = (sgv['vis']['num_items_in_a_time_in_BB'], sgv['vis']['num_time'])
                order_of_paging_in_horizontal_and_vertical_direction = (None, 1)
                order_of_match_pattern_in_horizontal_and_vertical_direction = (match_pattern_of_agent_name, match_pattern_of_name_time)

                list_fig_files = glob.glob(str(sgv['folderpath_plots_single_balanceSheets'] / f'*exp={i_exp}*.svg'))  # 获取所有当次实验文件列表

                merged_pdf = merged_and_bind_figs_to_a_pdf_file(order_of_variable_mean_in_horizontal_and_vertical_direction, order_of_paging_in_horizontal_and_vertical_direction, order_of_match_pattern_in_horizontal_and_vertical_direction, list_fig_files, i_exp)

                ## 保存
                merged_pdf.save(Path(sgv['folderpath_plots_makeup_balanceSheets'], 'BB_exp=' + str(i_exp) + '.pdf'))
                merged_pdf.close()

                pass  # for  实验编号

            pass  # if 拼接资产负债表

        # %% [markdown] ## #NOTE 可视化银行状态表格
        # 导入各自的资产负债表，按照横向时间纵向银行，拼接成大图

        # %%

        if (sgv['visulization_process']['银行状态表格可视化']):

            from openpyxl import load_workbook
            from openpyxl.styles import PatternFill
            from openpyxl.utils import get_column_letter

            print("准备可视化银行状态表格")
            Tools._delete_and_recreate_folder(sgv['folderpath_visualize_banksStates_table'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

            for i_exp in experiments_indices_to_vis:
                df_BB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'BB_panel_exp=' + str(i_exp) + '.pkl'))
                df_IB_panel = pd.read_pickle(Path(sgv['folderpath_plots'], 'IB_panel_exp=' + str(i_exp) + '.pkl'))

                ## 一些变量
                num_BB_id = len(df_BB_panel)  # 数据表BB之行数
                num_IB_id = len(df_IB_panel)  # 数据表IB之行数
                num_idData = df_BB_panel['id_data'].max() + 1  # 数据表之数据id个数
                num_round = df_BB_panel['round'].max() + 1  # 总的轮次数（是从0开始计数的)
                num_step = num_idData  # 总的步进数（是从0开始计数的)
                ## 根据时间粒度参数，确定时间轴名称及其长度
                if sgv['vis']['time_granularity'] == '步进粒度':
                    sgv['vis']['name_time'] = 'step'
                    sgv['vis']['num_time'] = num_step
                elif sgv['vis']['time_granularity'] == '轮次粒度':
                    sgv['vis']['name_time'] = 'round'
                    sgv['vis']['num_time'] = num_round
                else:
                    raise ValueError("`time_granularity` 必须是 `'步进粒度'` 或 `'轮次粒度'`")
                    pass  # if
                sgv['vis']['num_items_in_a_time_in_BB'] = num_BB_id // num_idData  # BB之一个运行时间片之项目数
                sgv['vis']['num_items_in_a_time_in_IB'] = num_IB_id // num_idData  # IB之一个运行轮次之项目数
                num_agent = sgv['vis']['num_items_in_a_time_in_BB']  # 银行数
                num_interbank = sgv['vis']['num_items_in_a_time_in_IB']  # 银行间关系数

                print("可视化银行状态表格：实验" + str(i_exp))

                ##NOTE 设置相关数据

                ### 状态相关的列名
                columns_states = [
                    'on',
                    'off',
                    'hel',
                    'isv',
                    'ilq',
                    'br',
                    'is_needed_BoIB',
                    'is_enabled_BoIB',
                    'is_needed_BoD',
                    'is_enabled_BoD',
                    'is_needed_LiP',
                    'is_enabled_LiP',
                    'is_allocated_Shock',
                ]

                ### 需要提取的列名
                columnsName_ext = [
                    'id',
                    'id_data',
                    'process_name',
                    'step',
                    'round',
                    'phase',
                    'id_agent',
                    'abbr',
                    'name',
                    'on',
                    'off',
                    'hel',
                    'isv',
                    'ilq',
                    'br',
                    'is_needed_BoIB',
                    'is_enabled_BoIB',
                    'is_needed_BoD',
                    'is_enabled_BoD',
                    'is_needed_LiP',
                    'is_enabled_LiP',
                    'is_allocated_Shock',
                ]

                ### 需要调整列边距的列名
                columnsName_adjust = [
                    'id',
                    'id_data',
                    'step',
                    'round',
                    'phase',
                    'id_agent',
                ]

                df_BankStates = df_BB_panel[columnsName_ext]  # 提取所需列

                df_BankStates.to_excel(Path(sgv['folderpath_visualize_banksStates_table'], 'BB_exp=' + str(i_exp) + '.xlsx'), index=False)  # 将数据写入新的 Excel 文件

                wb_BankStates = load_workbook(Path(sgv['folderpath_visualize_banksStates_table'], 'BB_exp=' + str(i_exp) + '.xlsx'))  # 使用 openpyxl 打开新的 Excel 文件
                sheet_BankStates = wb_BankStates.active

                sheet_BankStates.freeze_panes = "J2"  # 冻结窗格

                col_indices = [df_BankStates.columns.get_loc(col_name) + 1 for col_name in columnsName_adjust]  # 调整列宽
                for col_index in col_indices:
                    col_letter = get_column_letter(col_index)
                    sheet_BankStates.column_dimensions[col_letter].width = 5

                # 对于列 'id_data'，其单元格的值每间隔指定的行，对应的单元格背景色就变色。改变的颜色按照无色、浅灰色交替循环。
                fill = PatternFill(start_color="EEEEEE", end_color="EEEEEE", fill_type="solid")
                for i, row in enumerate(sheet_BankStates.iter_rows(min_row=2)):  # 跳过第一行表头
                    if i % (2 * sgv['num_bank']) < sgv['num_bank']:  # 每间隔指定的行填充一次背景色
                        for cell in row:
                            cell.fill = fill  # 将该行的背景色设置为浅灰色

                for col in columns_states:  # 遍历每一列
                    col_index = df_BankStates.columns.get_loc(col) + 1
                    col_letter = get_column_letter(col_index)
                    rng = sheet_BankStates[col_letter]
                    for cell in rng:  # 遍历每一个单元格
                        if cell.value == True:
                            cell.fill = PatternFill(start_color="FFBBBB", end_color="FFBBBB", fill_type="solid")  # 根据单元格的值设置背景颜色

                wb_BankStates.save(Path(sgv['folderpath_visualize_banksStates_table'], 'BB_exp=' + str(i_exp) + '.xlsx'))  # 保存 Excel 文件

                pass  # for

            pass  # if

    else:
        print("没有可用的数据，无法进行可视化！程序退出。")
        pass  # if  判断是否已经导入数据

    if sgv['is_ignore_warning']:
        warnings.filterwarnings("default")  # 恢复警告

    pass  # function


def process_one_heatmap(args):
    """
    处理需要绘制的单个热力图。

    首先获取相关的节点与边信息，然后用 matplotlib 绘制，最后保存。

    参数元组 args 信息如下：
      - args[0]: sgv (dict): 一个字典，包含了所有的参数。
      - args[1]: df_BB_panel (pandas.DataFrame): 数据表BB。
      - args[2]: df_IB_panel (pandas.DataFrame): 数据表IB。
      - args[3]: df_data_types (pandas.DataFrame): 数据表data_types。
      - args[4]: i_exp (int): 实验编号。
      - args[5]: t (int): 时间。
      - args[6]: i (int): 数据类别编号。

    Args:
          args: 一个元组，包含了需要的参数。

    Returns:
        None

    """
    sgv, df_BB_panel, df_IB_panel, d, i_exp, t, i = args

    ## 获取相关的节点与边信息
    data_vis_one_time_heatmap = generate_one_interbank_matrix_heatmaps_data_info(df_BB_panel, df_IB_panel, d['colormap'], d['relations'], t, d['data_name'], sgv['vis'])

    ## 用 matplotlib 绘制
    fig_heatmap = draw_one_interbank_matrix_heatmaps(data_vis_one_time_heatmap, sgv['vis'])
    fig_heatmap.savefig(Path(sgv['folderpath_plots_single_heatmaps'], 'IB_exp=' + str(i_exp) + '+data=' + d['data_name'][2] + '+' + sgv['vis']['name_time'] + '=' + str(t) + '.pdf'))  # 保存

    pass  # function


def process_one_graph(args):
    """
    处理需要绘制的单个网络图。

    首先获取相关的节点与边信息，然后用 igraph 绘制，最后保存。

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

    ## 用 igraph 绘制
    fig_graph = draw_one_interbank_flow_graph(data_vis_one_time_graph)
    fig_graph.savefig(Path(sgv['folderpath_plots_single_graphs'], 'IB_exp=' + str(i_exp) + '+data=' + d + '+' + sgv['vis']['name_time'] + '=' + str(t) + '.pdf'))  # 保存

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

    ## 用 drawsvg 绘制资产负债表
    svg_one_bank_balanceSheet = draw_one_bank_BalanceSheet(data_vis_one_bank_BalanceSheet, sgv['vis'], width=sgv['vis']['one_bank_BalanceSheet_width'], height=sgv['vis']['one_bank_BalanceSheet_height'], title_height=sgv['vis']['one_bank_BalanceSheet_title_height'], border=sgv['vis']['one_bank_BalanceSheet_border'])
    svg_one_bank_balanceSheet.save_svg(Path(sgv['folderpath_plots_single_balanceSheets'], 'BB_exp=' + str(i_exp) + '+name=' + data_vis_one_bank_BalanceSheet['others']['bank_name'] + '+' + sgv['vis']['name_time'] + '=' + str(t) + '.svg'))  # 保存

    pass  # function


if __name__ == '__main__':
    main()
