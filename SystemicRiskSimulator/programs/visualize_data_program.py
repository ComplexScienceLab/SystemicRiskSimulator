# -*- coding: utf-8 -*-


def visualize_data_program(sgv: dict):
    """
    可视化结果程序。

    BUG 2023-07-11：
    改标注在图上的文本语言为英文。暂时不建议用中文标注在图上。因为如果使用中文，不能任意设置字体族；

    Args:
        sgv (dict): 模拟器全局变量

    Returns:
        None

    """

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

    ## NOTE 导入包
    from SystemicRiskSimulator.tools.visualization_tools import generate_one_interbank_matrix_heatmaps_data_info, draw_one_interbank_matrix_heatmaps, generate_one_interbank_graph_data_info, draw_one_interbank_flow_graph, generate_one_bank_accounts_data, draw_one_bank_BalanceSheet
    from SystemicRiskSimulator.external_packages import platform, Path, re, glob, pd, np, deepcopy
    from matplotlib import pyplot as plt
    import igraph as ig
    # import matplotlib.pyplot as plt
    import drawsvg as dw
    import fitz
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    import matplotlib.font_manager as fm
    from matplotlib.font_manager import FontProperties

    # from SystemicRiskSimulator.external_packages.visualization_packages import ig, plt, fitz, svg2rlg, renderPDF, FontProperties, fm, pdfmetrics, TTFont

    # %% ## NOTE 设置字体与绘图工具包的一些配置

    ### 设置绘图时的字体 #NOTE：如果想要自定义字体，那么请开启下面的一段代码
    if platform.system() == 'Darwin':  # MacOS系统
        zh_font_family = 'Songti SC'
        en_font_family = 'Times New Roman'
    elif platform.system() == 'Windows':  # Windows系统
        zh_font_family = 'STZhongsong'
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

    ### 处理相关导入导出文件夹

    # sgv['folderpath_experiments'] = Path(sgv['folderpath_project'], sgv['folderpath_root_experiments'], sgv['foldername_experiments'])
    sgv['folderpath_experiments_output_data'] = Path(sgv['folderpath_experiments'], sgv['foldername_experiments_output_data'])
    sgv['folderpath_plots'] = Path(sgv['folderpath_experiments_output_data'], sgv['foldername_plots'])
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

    # %% [markdown] # NOTE 预处理数据

    print("执行：")

    if (sgv['visulization_process']['导入Pandas格式的实验结果数据转换为面板形式再导出']):
        ## NOTE 导入Pandas格式的实验结果数据，然后转换为面板形式的数据，导出PKL、CSV格式数据。
        print("导入Pandas格式的实验结果数据转换为面板形式再导出")

        list_filepath_pkl_BB = glob.glob(str(sgv['folderpath_experiments_output_data'] / 'BB_exp*.pkl'))  # 获取实验组输出数据pkl格式之BB数据之文件列表

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

            filename_pkl_BB = filepath_pkl_BB.split('/')[-1]
            filename_pkl_BB_panel = filename_pkl_BB.replace('BB_', 'BB_panel_')
            filepath_pkl_BB_panal = Path(sgv['folderpath_plots'], filename_pkl_BB_panel)  # 面板数据文件路径
            df_BB_panel.to_pickle(Path(filepath_pkl_BB_panal))  # 导出为pkl格式
            df_BB_panel.to_csv(Path(str(filepath_pkl_BB_panal).split('.')[0] + '.csv'), index=False)  # 导出为csv格式；
            pass  # for

        list_filepath_pkl_IB = glob.glob(str(sgv['folderpath_experiments_output_data'] / 'IB_exp*.pkl'))  # 获取实验组输出数据pkl格式之IB数据之文件列表
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

            filename_pkl_IB = filepath_pkl_IB.split('/')[-1]
            filename_pkl_IB_panel = filename_pkl_IB.replace('IB_', 'IB_panel_')
            filepath_pkl_IB_panal = Path(sgv['folderpath_plots'], filename_pkl_IB_panel)  # 面板数据文件路径
            df_IB_panel.to_pickle(Path(filepath_pkl_IB_panal))  # 导出为pkl格式
            df_IB_panel.to_csv(Path(Path(str(filepath_pkl_IB_panal).split('.')[0] + '.csv')), index=False)  # 导出为csv格式；
            pass  # for

        pass  # if 导入Pandas格式的实验结果数据转换为面板形式再导出

    # %% [markdown] # 导入面板形式的CSV数据预处理（备选）

    if (sgv['visulization_process']['导入面板形式的CSV数据预处理']):

        # NOTE：如果需要读取CSV格式处理数据的话则使用该程序段。#BUG 可能已经过时尚未适配。不建议使用！

        print("导入面板形式的CSV数据预处理")

        list_filepath_csv_panel = glob.glob(str(sgv['folderpath_plots'] / f'*.csv'))  # 获取实验组输出数据csv格式的文件列表

        ## 排序，优先按照银行名称，其次按照时间。
        match_pattern_in_vertical_direction = r'(?<=[IB]B_panel_exp=).+?(?=[(\.csv)])'
        match_pattern_in_horizontal_direction = r'[IB]B'
        sorted_list_filepath_csv_panel = sorted(list_filepath_csv_panel, key=lambda name: (
            int(re.search(match_pattern_in_vertical_direction, name)[0]),
            re.search(match_pattern_in_horizontal_direction, name)[0],
        ))

        ## 获取所有实验之索引
        experiments_indices = []
        for filepath in sorted_list_filepath_csv_panel:
            match = re.search(r'exp=(\d+)', filepath)
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
                sgv['vis']['name_time'] = 'id_data'
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

    # %% [markdown] # NOTE 可视化

    if (sgv['visulization_process']['读取面板形式的PKL格式的文件']):
        # ##  NOTE 导入面板形式的PKL数据预处理
        # 依次读取面板形式的PKL格式的文件，预处理每次实验

        print("读取面板形式的PKL格式的文件")

        pkl_panel_file_list = glob.glob(str(sgv['folderpath_plots'] / '*_panel_*.pkl'))  # 获取实验组输出数据pkl格式之文件列表

        ## 排序，优先按照银行名称，其次按照时间。
        match_pattern_in_vertical_direction = r'(?<=[IB]B_panel_exp=).+?(?=[(\.pkl)])'
        match_pattern_in_horizontal_direction = r'[IB]B'
        sorted_pkl_panel_file_list = sorted(pkl_panel_file_list, key=lambda name: (
            int(re.search(match_pattern_in_vertical_direction, name)[0]),
            re.search(match_pattern_in_horizontal_direction, name)[0],
        ))

        ## 获取所有实验之索引
        experiments_indices = []
        for filepath in sorted_pkl_panel_file_list:
            match = re.search(r'exp=(\d+)', filepath)
            if match:
                experiments_indices.append(int(match.group(1)))
            pass  # for
        experiments_indices = sorted(list(set(experiments_indices)))  # 去重

        pass  # if 读取面板形式的PKL格式的文件

    ## NOTE 依次读取面板形式的PKL格式的文件，预处理每次实验

    if (sgv['visulization_process']['读取面板形式的PKL格式的文件'] or sgv['visulization_process']['导入面板形式的CSV数据预处理']):

        if (sgv['visulization_process']['绘制矩阵热图']):
            print("准备绘制矩阵热图")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_single_heatmaps'], sgv['is_auto_confirmation'])  # 删除并重建文件夹
        if (sgv['visulization_process']['拼接矩阵热图']):
            print("准备拼接矩阵热图")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_makeup_heatmaps'], sgv['is_auto_confirmation'])  # 删除并重建文件夹
        if (sgv['visulization_process']['绘制资金流网络图']):
            print("准备绘制资金流网络图")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_single_graphs'], sgv['is_auto_confirmation'])  # 删除并重建文件夹
        if (sgv['visulization_process']['拼接资金流网络图']):
            print("准备拼接资金流网络图")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_makeup_graphs'], sgv['is_auto_confirmation'])  # 删除并重建文件夹
        if (sgv['visulization_process']['绘制资产负债表']):
            print("准备绘制资产负债表")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_single_balanceSheets'], sgv['is_auto_confirmation'])  # 删除并重建文件夹
        if (sgv['visulization_process']['拼接资产负债表']):
            print("准备拼接资产负债表")
            Tools._delete_and_recreate_folder(sgv['folderpath_plots_makeup_balanceSheets'], sgv['is_auto_confirmation'])  # 删除并重建文件夹

        for i_exp in experiments_indices:  # FIXME
            pkl_BB_00 = pd.read_pickle(Path(sgv['folderpath_plots'], 'BB_panel_exp=' + str(i_exp) + '.pkl'))
            pkl_IB_00 = pd.read_pickle(Path(sgv['folderpath_plots'], 'IB_panel_exp=' + str(i_exp) + '.pkl'))

            ## 预处理数据表

            ## 去除空列、调整列顺序
            pkl_BB_10 = deepcopy(pkl_BB_00.loc[:, ~pkl_BB_00.columns.str.contains('^Unnamed')])
            pkl_IB_10 = deepcopy(pkl_IB_00.loc[:, ~pkl_IB_00.columns.str.contains('^Unnamed')])

            ## 提前列`row`、`col`
            cols_sorted_10 = ['id_agent']
            cols_sorted_10 = cols_sorted_10 + [s for s in pkl_BB_10.columns if not s in cols_sorted_10]
            df_BB_panel = pkl_BB_10[cols_sorted_10]
            cols_sorted_10 = ['row', 'col']
            cols_sorted_10 = cols_sorted_10 + [s for s in pkl_IB_10.columns if not s in cols_sorted_10]
            df_IB_panel = pkl_IB_10[cols_sorted_10]

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

            ## 可视化

            if (sgv['visulization_process']['绘制矩阵热图']):

                ## NOTE 绘制矩阵热图
                # 依次按照每个银行间数据类别、时间，分别绘制单独的银行间资金流网络图

                print("绘制矩阵热图：实验" + str(i_exp))

                sgv['vis']['zh_font_family'] = zh_font_family
                sgv['vis']['en_font_family'] = en_font_family

                df_data_types = pd.DataFrame(sgv['vis']['list_dataTypes_for_heatmaps'])

                ### 计算各银行主体之代表性的类型之数据之最大值和最小值
                sgv['vis']['max_BB_value_in_all_panel'] = df_BB_panel['A_all'].max()
                sgv['vis']['min_BB_value_in_all_panel'] = 0

                ### 计算各银行主体间之代表性的类型之数据之最大值和最小值
                sgv['vis']['max_IB_value_in_all_panel'] = df_IB_panel['A_IB'].max()
                sgv['vis']['min_IB_value_in_all_panel'] = 0

                ## 绘图
                for i, d in df_data_types.iterrows():
                    sgv['vis']['data_name'] = d['data_name']

                    for t in range(sgv['vis']['num_time']):
                        ## 生成相关的参数
                        sgv['vis']['process_name'] = df_BB_panel[df_BB_panel[sgv['vis']['name_time']] == t]['process_name'].values[0]
                        sgv['vis']['step'] = df_BB_panel[df_BB_panel[sgv['vis']['name_time']] == t]['step'].values[0]
                        sgv['vis']['round'] = df_BB_panel[df_BB_panel[sgv['vis']['name_time']] == t]['round'].values[0]
                        sgv['vis']['phase'] = df_BB_panel[df_BB_panel[sgv['vis']['name_time']] == t]['phase'].values[0]
                        ## 获取相关的节点与边信息
                        data_vis_one_time_heatmap = generate_one_interbank_matrix_heatmaps_data_info(df_BB_panel, df_IB_panel, df_data_types['colormap'].values[i], t, sgv['vis']['data_name'], sgv['vis'])
                        ## 用 matplotlib 绘制
                        fig_heatmap = draw_one_interbank_matrix_heatmaps(data_vis_one_time_heatmap, sgv['vis'])
                        fig_heatmap.savefig(Path(sgv['folderpath_plots_single_heatmaps'], 'IB_exp=' + str(i_exp) + '+data=' + sgv['vis']['data_name'][2] + '+' + sgv['vis']['name_time'] + '=' + str(t) + '.pdf'))  # 保存
                        pass  # for
                    pass  # for

                # pass  # for

                pass  # if 绘制矩阵热图

            if (sgv['visulization_process']['拼接矩阵热图']):
                ## NOTE 拼接矩阵热图
                # 导入各自的矩阵热图，按照横向数据类别纵向时间，拼接成大图

                print("拼接矩阵热图：实验" + str(i_exp))

                num_dataTypes_for_heatmap_figs = len(sgv['vis']['list_dataTypes_for_heatmaps'])  # 数据类别数

                ## 声明与定义变量
                match_pattern_of_data_name = fr"(?<=data=).+?(?=[\+(\.pdf)])"  # 匹配相关含义的变量之数据名称之正则表达式文本
                match_pattern_of_name_time = fr"(?<={sgv['vis']['name_time']}=).+?(?=[\+(\.pdf)])"  # 匹配相关含义的变量之时间名称之正则表达式文本
                num_figure_in_horizontal_direction: int = None  # 横向的图片数量
                num_figure_in_vertical_direction: int = None  # 纵向的图片数量
                max_num_of_figures_in_horizontal_direction_per_page: int = None  # 每页横向的最大图片数量
                max_num_of_figures_in_vertical_direction_per_page: int = None  # 每页纵向的最大图片数量
                match_pattern_in_vertical_direction: str = None  # 纵向需要匹配的文本
                match_pattern_in_horizontal_direction: str = None  # 横向需要匹配的文本
                num_figure_in_horizontal_direction_per_page: int = None  # 每页之横向之图片数量
                num_figure_in_vertical_direction_per_page: int = None  # 每页之纵向之图片数量
                num_figure_in_paging_direction: int = None  # 分页方向之图片数量
                num_figure_in_no_paging_direction: int = None  # 不分页方向之图片数量
                max_num_of_figures_in_paging_direction_per_page: int = None  # 每页之分页方向之最大图片数量
                max_num_of_figures_in_no_paging_direction_per_page: int = None  # 每页之不分页方向之最大图片数量
                match_pattern_in_paging_direction: str = None  # 分页方向需要匹配的文本
                match_pattern_in_no_paging_direction: str = None  # 不分页方向需要匹配的文本
                num_figure_in_paging_direction_per_page: int = None  # 每页之分页方向之图片数量
                num_figure_in_no_paging_direction_per_page: int = None  # 每页之不分页方向之图片数量
                single_plot_size_width: float = None  # 单个图之宽度
                single_plot_size_height: float = None  # 单个图之高度
                single_plot_size_in_paging_direction: float = None  # 单个图之在分页方向之尺寸
                single_plot_size_in_no_paging_direction: float = None  # 单个图之在不分页方向之尺寸

                ## 设置参数

                ### #NOTE 这组配置表示按照时间横向，按照数据类别纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
                # order_of_variable_mean_in_horizontal_and_vertical_direction = [sgv['vis']['num_time'], num_dataTypes_for_heatmap_figs]
                # order_of_paging_in_horizontal_and_vertical_direction = [6, None]
                # order_of_match_pattern_in_horizontal_and_vertical_direction = [match_pattern_of_name_time, match_pattern_of_data_name]

                ### #NOTE 这组配置表示按照数据类别横向，按照时间纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
                order_of_variable_mean_in_horizontal_and_vertical_direction = [num_dataTypes_for_heatmap_figs, sgv['vis']['num_time']]
                order_of_paging_in_horizontal_and_vertical_direction = [None, 6]
                order_of_match_pattern_in_horizontal_and_vertical_direction = [match_pattern_of_data_name, match_pattern_of_name_time]

                ## 赋值设置项
                num_figure_in_horizontal_direction, num_figure_in_vertical_direction = order_of_variable_mean_in_horizontal_and_vertical_direction[0], order_of_variable_mean_in_horizontal_and_vertical_direction[1]
                max_num_of_figures_in_horizontal_direction_per_page, max_num_of_figures_in_vertical_direction_per_page = order_of_paging_in_horizontal_and_vertical_direction[0], order_of_paging_in_horizontal_and_vertical_direction[1]  # `None`表示不限制。
                match_pattern_in_horizontal_direction, match_pattern_in_vertical_direction = order_of_match_pattern_in_horizontal_and_vertical_direction[0], order_of_match_pattern_in_horizontal_and_vertical_direction[1]

                ## 计算相关的变量
                pkl_panel_file_list = glob.glob(str(sgv['folderpath_plots_single_heatmaps'] / f'*exp={i_exp}*.pdf'))  # 获取所有当次实验文件列表
                single_plot_pdf = fitz.open(pkl_panel_file_list[0])
                single_plot_size_width = single_plot_pdf.load_page(0).rect[2]  # 获取单个图的尺寸（这里所有图的尺寸都是一样的）
                single_plot_size_height = single_plot_pdf.load_page(0).rect[3]
                single_plot_pdf.close()

                ## 判断分页的方向
                if max_num_of_figures_in_horizontal_direction_per_page is not None and max_num_of_figures_in_vertical_direction_per_page is None:
                    paging_direction = 'horizontal'
                elif max_num_of_figures_in_vertical_direction_per_page is not None and max_num_of_figures_in_horizontal_direction_per_page is None:
                    paging_direction = 'vertical'
                elif max_num_of_figures_in_vertical_direction_per_page is not None and max_num_of_figures_in_horizontal_direction_per_page is not None:
                    paging_direction = 'none'
                else:
                    raise ValueError('不可以双向都分页！')
                    pass  # if

                ## 根据分页的方向，赋值分页与不分页方向之相关变量
                if paging_direction == 'horizontal':
                    num_figure_in_paging_direction = num_figure_in_horizontal_direction
                    num_figure_in_no_paging_direction = num_figure_in_vertical_direction
                    max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
                    max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
                    match_pattern_in_paging_direction = match_pattern_in_horizontal_direction
                    match_pattern_in_no_paging_direction = match_pattern_in_vertical_direction
                    single_plot_size_in_paging_direction = single_plot_size_width
                    single_plot_size_in_no_paging_direction = single_plot_size_height
                    num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
                    num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
                    num_figure_in_horizontal_direction_per_page = num_figure_in_paging_direction_per_page
                    num_figure_in_vertical_direction_per_page = num_figure_in_no_paging_direction_per_page
                elif paging_direction == 'vertical':
                    num_figure_in_paging_direction = num_figure_in_vertical_direction
                    num_figure_in_no_paging_direction = num_figure_in_horizontal_direction
                    max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
                    max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
                    match_pattern_in_paging_direction = match_pattern_in_vertical_direction
                    match_pattern_in_no_paging_direction = match_pattern_in_horizontal_direction
                    single_plot_size_in_paging_direction = single_plot_size_height
                    single_plot_size_in_no_paging_direction = single_plot_size_width
                    num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
                    num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
                    num_figure_in_horizontal_direction_per_page = num_figure_in_no_paging_direction_per_page
                    num_figure_in_vertical_direction_per_page = num_figure_in_paging_direction_per_page
                elif paging_direction == 'none':  # 如果不分页，那么默认按照纵向分页的情况处理
                    num_figure_in_paging_direction = num_figure_in_vertical_direction
                    num_figure_in_no_paging_direction = num_figure_in_horizontal_direction
                    max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
                    max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
                    match_pattern_in_paging_direction = match_pattern_in_vertical_direction
                    match_pattern_in_no_paging_direction = match_pattern_in_horizontal_direction
                    single_plot_size_in_paging_direction = single_plot_size_height
                    single_plot_size_in_no_paging_direction = single_plot_size_width
                    num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
                    num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
                    num_figure_in_horizontal_direction_per_page = num_figure_in_no_paging_direction_per_page
                    num_figure_in_vertical_direction_per_page = num_figure_in_paging_direction_per_page
                    pass  # if

                total_figures_per_page = num_figure_in_horizontal_direction_per_page * num_figure_in_vertical_direction_per_page  # 每页最大总图数
                num_pages = int(np.ceil(len(pkl_panel_file_list) / total_figures_per_page))  # 最大总页数

                ## 排序，优先按照需要分页的方向，其次按照不需要分页的方向。
                sorted_pkl_panel_file_list = sorted(pkl_panel_file_list, key=lambda name: (
                    re.search(match_pattern_in_paging_direction, name)[0] if not re.search(match_pattern_in_paging_direction, name)[0].isdigit() else int(re.search(match_pattern_in_paging_direction, name)[0]),
                    re.search(match_pattern_in_no_paging_direction, name)[0] if not re.search(match_pattern_in_no_paging_direction, name)[0].isdigit() else int(re.search(match_pattern_in_no_paging_direction, name)[0]),
                ))

                ## 分页处理
                merged_pdf = fitz.open()  # 新建需要合并的pdf
                for page_idx in range(num_pages):

                    ## 创建一个新的分页
                    merged_pdf_page = merged_pdf.new_page(
                        # -1, # 这里不需要指定页码，fitz会自动分配
                        width=single_plot_size_width * num_figure_in_horizontal_direction_per_page,
                        height=single_plot_size_height * num_figure_in_vertical_direction_per_page,
                    )

                    ## 对于该新的分页，逐个导入单幅pdf，临时装订pdf
                    binded_pdf = fitz.open()  # 创建一个空白pdf用于装订单幅pdf
                    for i in range(total_figures_per_page):
                        idx = page_idx * total_figures_per_page + i
                        if idx >= len(pkl_panel_file_list):
                            break
                        filepath = sorted_pkl_panel_file_list[idx]
                        # svg_file = svg2rlg(filepath)
                        # renderPDF.drawToFile(svg_file, filepath.split('.')[0] + '.pdf')
                        # single_pdf_file = fitz.open(filepath.split('.')[0] + '.pdf')
                        single_pdf_file = fitz.open(filepath)
                        binded_pdf.insert_pdf(single_pdf_file)
                        single_pdf_file.close()
                        pass  # for

                    ## 设置装订的pdf之每个图在该新的分页之位置
                    page_content_positions = []
                    for i in range(num_figure_in_paging_direction_per_page):
                        if (
                                paging_direction != 'none'  # 如果是存在分页的情况
                                and page_idx == num_pages - 1  # 如果是最后一页
                                and num_figure_in_paging_direction % num_figure_in_paging_direction_per_page != 0  # 如果最后一页不是满页的情况
                                and i >= num_figure_in_paging_direction % num_figure_in_paging_direction_per_page  # 如果该索引处于空行或者空列
                        ):
                            break  # 需要分页方向跳过最后一页的空行或者空列
                            pass  # if
                        for j in range(num_figure_in_no_paging_direction_per_page):
                            if paging_direction == 'horizontal':
                                page_content_positions.append(
                                    fitz.Rect(single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * (i + 1), single_plot_size_in_no_paging_direction * (j + 1))
                                )
                            elif paging_direction == 'vertical':
                                page_content_positions.append(
                                    fitz.Rect(single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * (j + 1), single_plot_size_in_paging_direction * (i + 1))
                                )
                            elif paging_direction == 'none':
                                page_content_positions.append(
                                    fitz.Rect(single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * (j + 1), single_plot_size_in_paging_direction * (i + 1))
                                )
                                pass  # if
                            pass  # for
                        pass  # for

                    ## 将装订的pdf之每个图放到该新的分页之对应的位置
                    for i_fig, page in enumerate(binded_pdf):
                        merged_pdf_page.show_pdf_page(page_content_positions[i_fig], binded_pdf, page.number)
                        pass  # for

                    binded_pdf.close()
                    pass  # for

                ## 保存
                merged_pdf.save(Path(sgv['folderpath_plots_makeup_heatmaps'], 'IB_exp=' + str(i_exp) + '.pdf'))
                merged_pdf.close()

                pass  # if 拼接矩阵热图

            if (sgv['visulization_process']['绘制资金流网络图']):

                ## NOTE 绘制资金流网络图
                # 依次按照每个银行间数据类别、时间，分别绘制单独的银行间资金流网络图

                print("绘制资金流网络图：实验" + str(i_exp))

                # for i_exp in experiments_indices:

                sgv['vis']['zh_font_family'] = zh_font_family
                sgv['vis']['en_font_family'] = en_font_family

                ## 设置项

                ## 绘图
                for d in sgv['vis']['list_dataNames_for_graph_figs']:
                    sgv['vis']['data_name'] = d

                    ## 设置不同点集对应的属性
                    verticeTypes = d + '_all'

                    ## 设置不同边集对应的属性
                    list_data_edgeTypes = [
                        dict(
                            edge_type=d,
                            edge_color='#CCCCCC',
                            edge_width=5,
                        ),
                        dict(
                            edge_type='Shock_IB_run_ilq',
                            edge_color='#FF0000',
                            edge_width=3,
                        ),
                        dict(
                            edge_type='Bo_IB',
                            edge_color='#E7C300',
                            edge_width=1,
                        ),
                    ]

                    ### 计算各银行主体之代表性的类型之数据之最大值和最小值
                    sgv['vis']['max_BB_value_in_all_panel'] = df_BB_panel['A_all'].max()
                    sgv['vis']['min_BB_value_in_all_panel'] = 0

                    ### 计算各银行主体间之代表性的类型之数据之最大值和最小值
                    sgv['vis']['max_IB_value_in_all_panel'] = df_IB_panel['A_IB'].max()
                    sgv['vis']['min_IB_value_in_all_panel'] = 0

                    for t in range(sgv['vis']['num_time']):
                        ## 初始化参数
                        data_vis_one_time_graph = {}
                        data_vis_one_time_graph['edge_types'] = pd.DataFrame(list_data_edgeTypes)
                        data_vis_one_time_graph['vertices'] = pd.DataFrame()
                        data_vis_one_time_graph['edges'] = pd.DataFrame()

                        ## 生成相关的参数
                        sgv['vis']['process_name'] = df_BB_panel[df_BB_panel[sgv['vis']['name_time']] == t]['process_name'].values[0]
                        sgv['vis']['step'] = df_BB_panel[df_BB_panel[sgv['vis']['name_time']] == t]['step'].values[0]
                        sgv['vis']['round'] = df_BB_panel[df_BB_panel[sgv['vis']['name_time']] == t]['round'].values[0]
                        sgv['vis']['phase'] = df_BB_panel[df_BB_panel[sgv['vis']['name_time']] == t]['phase'].values[0]
                        ## 获取相关的节点与边信息
                        data_vis_one_time_graph = generate_one_interbank_graph_data_info(df_BB_panel, df_IB_panel, data_vis_one_time_graph, t, d, sgv['vis'])
                        ## 用 igraph 绘制
                        fig_graph = draw_one_interbank_flow_graph(data_vis_one_time_graph, sgv['vis'])
                        fig_graph.savefig(Path(sgv['folderpath_plots_single_graphs'], 'IB_exp=' + str(i_exp) + '+data=' + sgv['vis']['data_name'] + '+' + sgv['vis']['name_time'] + '=' + str(t) + '.pdf'))  # 保存
                        pass  # for
                    pass  # for

                # pass  # for

                pass  # if 绘制资金流网络图

            if (sgv['visulization_process']['拼接资金流网络图']):
                ## NOTE 拼接资金流网络图
                # 导入各自的网络图，按照横向数据类别纵向时间，拼接成大图

                print("拼接资金流网络图：实验" + str(i_exp))

                num_dataTypes_for_graph_figs = len(sgv['vis']['list_dataNames_for_graph_figs'])  # 数据类别数

                ## 声明与定义变量
                match_pattern_of_data_name = fr"(?<=data=).+?(?=[\+(\.pdf)])"  # 匹配相关含义的变量之数据名称之正则表达式文本
                match_pattern_of_name_time = fr"(?<={sgv['vis']['name_time']}=).+?(?=[\+(\.pdf)])"  # 匹配相关含义的变量之时间名称之正则表达式文本
                num_figure_in_horizontal_direction: int = None  # 横向的图片数量
                num_figure_in_vertical_direction: int = None  # 纵向的图片数量
                max_num_of_figures_in_horizontal_direction_per_page: int = None  # 每页横向的最大图片数量
                max_num_of_figures_in_vertical_direction_per_page: int = None  # 每页纵向的最大图片数量
                match_pattern_in_vertical_direction: str = None  # 纵向需要匹配的文本
                match_pattern_in_horizontal_direction: str = None  # 横向需要匹配的文本
                num_figure_in_horizontal_direction_per_page: int = None  # 每页之横向之图片数量
                num_figure_in_vertical_direction_per_page: int = None  # 每页之纵向之图片数量
                num_figure_in_paging_direction: int = None  # 分页方向之图片数量
                num_figure_in_no_paging_direction: int = None  # 不分页方向之图片数量
                max_num_of_figures_in_paging_direction_per_page: int = None  # 每页之分页方向之最大图片数量
                max_num_of_figures_in_no_paging_direction_per_page: int = None  # 每页之不分页方向之最大图片数量
                match_pattern_in_paging_direction: str = None  # 分页方向需要匹配的文本
                match_pattern_in_no_paging_direction: str = None  # 不分页方向需要匹配的文本
                num_figure_in_paging_direction_per_page: int = None  # 每页之分页方向之图片数量
                num_figure_in_no_paging_direction_per_page: int = None  # 每页之不分页方向之图片数量
                single_plot_size_width: float = None  # 单个图之宽度
                single_plot_size_height: float = None  # 单个图之高度
                single_plot_size_in_paging_direction: float = None  # 单个图之在分页方向之尺寸
                single_plot_size_in_no_paging_direction: float = None  # 单个图之在不分页方向之尺寸

                ## 设置参数

                ### #NOTE 这组配置表示按照时间横向，按照数据类别纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
                # order_of_variable_mean_in_horizontal_and_vertical_direction = [sgv['vis']['num_time'], num_dataTypes_for_graph_figs]
                # order_of_paging_in_horizontal_and_vertical_direction = [6, None]
                # order_of_match_pattern_in_horizontal_and_vertical_direction = [match_pattern_of_name_time, match_pattern_of_data_name]

                ### #NOTE 这组配置表示按照数据类别横向，按照时间纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
                order_of_variable_mean_in_horizontal_and_vertical_direction = [num_dataTypes_for_graph_figs, sgv['vis']['num_time']]
                order_of_paging_in_horizontal_and_vertical_direction = [None, 6]
                order_of_match_pattern_in_horizontal_and_vertical_direction = [match_pattern_of_data_name, match_pattern_of_name_time]

                ## 赋值设置项
                num_figure_in_horizontal_direction, num_figure_in_vertical_direction = order_of_variable_mean_in_horizontal_and_vertical_direction[0], order_of_variable_mean_in_horizontal_and_vertical_direction[1]
                max_num_of_figures_in_horizontal_direction_per_page, max_num_of_figures_in_vertical_direction_per_page = order_of_paging_in_horizontal_and_vertical_direction[0], order_of_paging_in_horizontal_and_vertical_direction[1]  # `None`表示不限制。
                match_pattern_in_horizontal_direction, match_pattern_in_vertical_direction = order_of_match_pattern_in_horizontal_and_vertical_direction[0], order_of_match_pattern_in_horizontal_and_vertical_direction[1]

                ## 计算相关的变量
                pkl_panel_file_list = glob.glob(str(sgv['folderpath_plots_single_graphs'] / f'*exp={i_exp}*.pdf'))  # 获取所有当次实验文件列表
                single_plot_pdf = fitz.open(pkl_panel_file_list[0])
                single_plot_size_width = single_plot_pdf.load_page(0).rect[2]  # 获取单个图的尺寸（这里所有图的尺寸都是一样的）
                single_plot_size_height = single_plot_pdf.load_page(0).rect[3]
                single_plot_pdf.close()

                ## 判断分页的方向
                if max_num_of_figures_in_horizontal_direction_per_page is not None and max_num_of_figures_in_vertical_direction_per_page is None:
                    paging_direction = 'horizontal'
                elif max_num_of_figures_in_vertical_direction_per_page is not None and max_num_of_figures_in_horizontal_direction_per_page is None:
                    paging_direction = 'vertical'
                elif max_num_of_figures_in_vertical_direction_per_page is not None and max_num_of_figures_in_horizontal_direction_per_page is not None:
                    paging_direction = 'none'
                else:
                    raise ValueError('不可以双向都分页！')
                    pass  # if

                ## 根据分页的方向，赋值分页与不分页方向之相关变量
                if paging_direction == 'horizontal':
                    num_figure_in_paging_direction = num_figure_in_horizontal_direction
                    num_figure_in_no_paging_direction = num_figure_in_vertical_direction
                    max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
                    max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
                    match_pattern_in_paging_direction = match_pattern_in_horizontal_direction
                    match_pattern_in_no_paging_direction = match_pattern_in_vertical_direction
                    single_plot_size_in_paging_direction = single_plot_size_width
                    single_plot_size_in_no_paging_direction = single_plot_size_height
                    num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
                    num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
                    num_figure_in_horizontal_direction_per_page = num_figure_in_paging_direction_per_page
                    num_figure_in_vertical_direction_per_page = num_figure_in_no_paging_direction_per_page
                elif paging_direction == 'vertical':
                    num_figure_in_paging_direction = num_figure_in_vertical_direction
                    num_figure_in_no_paging_direction = num_figure_in_horizontal_direction
                    max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
                    max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
                    match_pattern_in_paging_direction = match_pattern_in_vertical_direction
                    match_pattern_in_no_paging_direction = match_pattern_in_horizontal_direction
                    single_plot_size_in_paging_direction = single_plot_size_height
                    single_plot_size_in_no_paging_direction = single_plot_size_width
                    num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
                    num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
                    num_figure_in_horizontal_direction_per_page = num_figure_in_no_paging_direction_per_page
                    num_figure_in_vertical_direction_per_page = num_figure_in_paging_direction_per_page
                elif paging_direction == 'none':  # 如果不分页，那么默认按照纵向分页的情况处理
                    num_figure_in_paging_direction = num_figure_in_vertical_direction
                    num_figure_in_no_paging_direction = num_figure_in_horizontal_direction
                    max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
                    max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
                    match_pattern_in_paging_direction = match_pattern_in_vertical_direction
                    match_pattern_in_no_paging_direction = match_pattern_in_horizontal_direction
                    single_plot_size_in_paging_direction = single_plot_size_height
                    single_plot_size_in_no_paging_direction = single_plot_size_width
                    num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
                    num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
                    num_figure_in_horizontal_direction_per_page = num_figure_in_no_paging_direction_per_page
                    num_figure_in_vertical_direction_per_page = num_figure_in_paging_direction_per_page
                    pass  # if

                total_figures_per_page = num_figure_in_horizontal_direction_per_page * num_figure_in_vertical_direction_per_page  # 每页最大总图数
                num_pages = int(np.ceil(len(pkl_panel_file_list) / total_figures_per_page))  # 最大总页数

                ## 排序，优先按照需要分页的方向，其次按照不需要分页的方向。
                sorted_pkl_panel_file_list = sorted(pkl_panel_file_list, key=lambda name: (
                    re.search(match_pattern_in_paging_direction, name)[0] if not re.search(match_pattern_in_paging_direction, name)[0].isdigit() else int(re.search(match_pattern_in_paging_direction, name)[0]),
                    re.search(match_pattern_in_no_paging_direction, name)[0] if not re.search(match_pattern_in_no_paging_direction, name)[0].isdigit() else int(re.search(match_pattern_in_no_paging_direction, name)[0]),
                ))

                ## 分页处理
                merged_pdf = fitz.open()  # 新建需要合并的pdf
                for page_idx in range(num_pages):

                    ## 创建一个新的分页
                    merged_pdf_page = merged_pdf.new_page(
                        # -1, # 这里不需要指定页码，fitz会自动分配
                        width=single_plot_size_width * num_figure_in_horizontal_direction_per_page,
                        height=single_plot_size_height * num_figure_in_vertical_direction_per_page,
                    )

                    ## 对于该新的分页，逐个导入单幅pdf，临时装订pdf
                    binded_pdf = fitz.open()  # 创建一个空白pdf用于装订单幅pdf
                    for i in range(total_figures_per_page):
                        idx = page_idx * total_figures_per_page + i
                        if idx >= len(pkl_panel_file_list):
                            break
                        filepath = sorted_pkl_panel_file_list[idx]
                        single_pdf_file = fitz.open(filepath)
                        binded_pdf.insert_pdf(single_pdf_file)
                        single_pdf_file.close()
                        pass  # for

                    ## 设置装订的pdf之每个图在该新的分页之位置
                    page_content_positions = []
                    for i in range(num_figure_in_paging_direction_per_page):
                        if (
                                paging_direction != 'none'  # 如果是存在分页的情况
                                and page_idx == num_pages - 1  # 如果是最后一页
                                and num_figure_in_paging_direction % num_figure_in_paging_direction_per_page != 0  # 如果最后一页不是满页的情况
                                and i >= num_figure_in_paging_direction % num_figure_in_paging_direction_per_page  # 如果该索引处于空行或者空列
                        ):
                            break  # 需要分页方向跳过最后一页的空行或者空列
                            pass  # if
                        for j in range(num_figure_in_no_paging_direction_per_page):
                            if paging_direction == 'horizontal':
                                page_content_positions.append(
                                    fitz.Rect(single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * (i + 1), single_plot_size_in_no_paging_direction * (j + 1))
                                )
                            elif paging_direction == 'vertical':
                                page_content_positions.append(
                                    fitz.Rect(single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * (j + 1), single_plot_size_in_paging_direction * (i + 1))
                                )
                            elif paging_direction == 'none':
                                page_content_positions.append(
                                    fitz.Rect(single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * (j + 1), single_plot_size_in_paging_direction * (i + 1))
                                )
                                pass  # if
                            pass  # for
                        pass  # for

                    ## 将装订的pdf之每个图放到该新的分页之对应的位置
                    for i_fig, page in enumerate(binded_pdf):
                        merged_pdf_page.show_pdf_page(page_content_positions[i_fig], binded_pdf, page.number)
                        pass  # for

                    binded_pdf.close()
                    pass  # for

                ## 保存
                merged_pdf.save(Path(sgv['folderpath_plots_makeup_graphs'], 'IB_exp=' + str(i_exp) + '.pdf'))
                merged_pdf.close()

                pass  # if 拼接资金流网络图

            if (sgv['visulization_process']['绘制资产负债表']):

                ## NOTE 绘制资产负债表
                # 依次按照时间、银行，分别绘制单独的资产负债表（资产负债表尺寸不一样大，尺寸按照比例）

                print("绘制资产负债表：实验" + str(i_exp))

                # for i_exp in experiments_indices:

                sgv['vis']['zh_font_family'] = zh_font_family
                sgv['vis']['en_font_family'] = en_font_family

                ## NOTE：设置绘制资产负债表相关的数据
                ## 资产负债表账户数据（字典列表形式）
                list_accounts_data = [
                    dict(
                        data_type='asset',
                        level='level 3',
                        subject='A_P',
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
                        fill_color='#FFFF98',
                        stroke_color='gray',
                        stroke_width=1,
                        position=(0, 0),
                        size=(0, 0),
                    ),
                ]

                ## 冲击数据（字典列表形式）
                list_shocks_data = [
                    dict(
                        data_type='shock_def_t',
                        level='level 3',
                        subject='Shock_P_def_t',
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
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
                        value=0,
                        fill_color='#00FF00',
                        stroke_color='gray',
                        stroke_width=1,
                        side='asset',
                        align='A_all',
                        position=(0, 0),
                        size=(0, 0),
                    ),
                ]

                ### 计算各银行主体之代表性的类型之数据之最大值和最小值
                sgv['vis']['max_BB_value_in_all_panel'] = df_BB_panel['A_all'].max()
                sgv['vis']['min_BB_value_in_all_panel'] = 0

                for i in range(sgv['vis']['num_items_in_a_time_in_BB']):
                    for t in range(sgv['vis']['num_time']):
                        ## 初始化数据
                        data_vis_one_bank_BalanceSheet = {}
                        data_vis_one_bank_BalanceSheet['accounts'] = pd.DataFrame(list_accounts_data)
                        data_vis_one_bank_BalanceSheet['shocks'] = pd.DataFrame(list_shocks_data)

                        ## 生成绘制资产负债表所需的数据
                        data_vis_one_bank_BalanceSheet = generate_one_bank_accounts_data(df_BB_panel, data_vis_one_bank_BalanceSheet, t, i, sgv['vis'])
                        ## 生成相关的参数
                        sgv['vis']['bank_name'] = df_BB_panel[(df_BB_panel[sgv['vis']['name_time']] == t) & (df_BB_panel['id_agent'] == i)]['name'].values[0]
                        sgv['vis']['process_name'] = df_BB_panel[(df_BB_panel[sgv['vis']['name_time']] == t) & (df_BB_panel['id_agent'] == i)]['process_name'].values[0]
                        sgv['vis']['step'] = df_BB_panel[(df_BB_panel[sgv['vis']['name_time']] == t) & (df_BB_panel['id_agent'] == i)]['step'].values[0]
                        sgv['vis']['round'] = df_BB_panel[(df_BB_panel[sgv['vis']['name_time']] == t) & (df_BB_panel['id_agent'] == i)]['round'].values[0]
                        sgv['vis']['phase'] = df_BB_panel[(df_BB_panel[sgv['vis']['name_time']] == t) & (df_BB_panel['id_agent'] == i)]['phase'].values[0]
                        ## 用 drawsvg 绘制资产负债表
                        svg_one_bank_balanceSheet = draw_one_bank_BalanceSheet(data_vis_one_bank_BalanceSheet, sgv['vis'], width=sgv['vis']['one_bank_BalanceSheet_width'], height=sgv['vis']['one_bank_BalanceSheet_height'], title_height=sgv['vis']['one_bank_BalanceSheet_title_height'], border=sgv['vis']['one_bank_BalanceSheet_border'])
                        svg_one_bank_balanceSheet.save_svg(Path(sgv['folderpath_plots_single_balanceSheets'], 'BB_exp=' + str(i_exp) + '+name=' + sgv['vis']['bank_name'] + '+' + sgv['vis']['name_time'] + '=' + str(t) + '.svg'))  # 保存
                        pass  # for
                    pass  # for

                # pass  # for

                pass  # if 绘制资产负债表

            if (sgv['visulization_process']['拼接资产负债表']):
                ## NOTE 拼接资产负债表
                # 导入各自的资产负债表，按照横向时间纵向银行，拼接成大图

                print("拼接资产负债表：实验" + str(i_exp))

                # for i_exp in experiments_indices:

                ## 声明与定义变量
                match_pattern_of_agent_name = fr"(?<=name=).+?(?=[\+(\.svg)])"  # 匹配相关含义的变量之个体名称之正则表达式文本
                match_pattern_of_name_time = fr"(?<={sgv['vis']['name_time']}=).+?(?=[\+(\.svg)])"  # 匹配相关含义的变量之时间名称之正则表达式文本
                num_figure_in_horizontal_direction: int = None  # 横向的图片数量
                num_figure_in_vertical_direction: int = None  # 纵向的图片数量
                max_num_of_figures_in_horizontal_direction_per_page: int = None  # 每页横向的最大图片数量
                max_num_of_figures_in_vertical_direction_per_page: int = None  # 每页纵向的最大图片数量
                match_pattern_in_vertical_direction: str = None  # 纵向需要匹配的文本
                match_pattern_in_horizontal_direction: str = None  # 横向需要匹配的文本
                num_figure_in_horizontal_direction_per_page: int = None  # 每页之横向之图片数量
                num_figure_in_vertical_direction_per_page: int = None  # 每页之纵向之图片数量
                num_figure_in_paging_direction: int = None  # 分页方向之图片数量
                num_figure_in_no_paging_direction: int = None  # 不分页方向之图片数量
                max_num_of_figures_in_paging_direction_per_page: int = None  # 每页之分页方向之最大图片数量
                max_num_of_figures_in_no_paging_direction_per_page: int = None  # 每页之不分页方向之最大图片数量
                match_pattern_in_paging_direction: str = None  # 分页方向需要匹配的文本
                match_pattern_in_no_paging_direction: str = None  # 不分页方向需要匹配的文本
                num_figure_in_paging_direction_per_page: int = None  # 每页之分页方向之图片数量
                num_figure_in_no_paging_direction_per_page: int = None  # 每页之不分页方向之图片数量
                single_plot_size_width: float = None  # 单个图之宽度
                single_plot_size_height: float = None  # 单个图之高度
                single_plot_size_in_paging_direction: float = None  # 单个图之在分页方向之尺寸
                single_plot_size_in_no_paging_direction: float = None  # 单个图之在不分页方向之尺寸

                ## 设置参数

                ### #NOTE 这组配置表示按照时间横向，按照银行纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
                # order_of_variable_mean_in_horizontal_and_vertical_direction = [sgv['vis']['num_time'], sgv['vis']['num_items_in_a_time_in_BB']]
                # order_of_paging_in_horizontal_and_vertical_direction = [6, None]
                # order_of_match_pattern_in_horizontal_and_vertical_direction = [match_pattern_of_name_time, match_pattern_of_agent_name]

                ### #NOTE 这组配置表示按照银行横向，按照时间纵向。这里每页轴向的最大图片数量只能设置最多单个轴的，不能同时设置两个轴的，否则运行结果可能会错乱。
                order_of_variable_mean_in_horizontal_and_vertical_direction = [sgv['vis']['num_items_in_a_time_in_BB'], sgv['vis']['num_time']]
                order_of_paging_in_horizontal_and_vertical_direction = [None, 6]
                order_of_match_pattern_in_horizontal_and_vertical_direction = [match_pattern_of_agent_name, match_pattern_of_name_time]

                ## 赋值设置项
                num_figure_in_horizontal_direction, num_figure_in_vertical_direction = order_of_variable_mean_in_horizontal_and_vertical_direction[0], order_of_variable_mean_in_horizontal_and_vertical_direction[1]
                max_num_of_figures_in_horizontal_direction_per_page, max_num_of_figures_in_vertical_direction_per_page = order_of_paging_in_horizontal_and_vertical_direction[0], order_of_paging_in_horizontal_and_vertical_direction[1]  # `None`表示不限制。
                match_pattern_in_horizontal_direction, match_pattern_in_vertical_direction = order_of_match_pattern_in_horizontal_and_vertical_direction[0], order_of_match_pattern_in_horizontal_and_vertical_direction[1]

                ## 计算相关的变量
                pkl_panel_file_list = glob.glob(str(sgv['folderpath_plots_single_balanceSheets'] / f'*exp={i_exp}*.svg'))  # 获取所有当次实验文件列表
                single_plot_size_width = svg2rlg(pkl_panel_file_list[0]).width  # 获取单个图的尺寸（这里所有图的尺寸都是一样的）
                single_plot_size_height = svg2rlg(pkl_panel_file_list[0]).height

                ## 判断分页的方向
                if max_num_of_figures_in_horizontal_direction_per_page is not None and max_num_of_figures_in_vertical_direction_per_page is None:
                    paging_direction = 'horizontal'
                elif max_num_of_figures_in_vertical_direction_per_page is not None and max_num_of_figures_in_horizontal_direction_per_page is None:
                    paging_direction = 'vertical'
                elif max_num_of_figures_in_vertical_direction_per_page is not None and max_num_of_figures_in_horizontal_direction_per_page is not None:
                    paging_direction = 'none'
                else:
                    raise ValueError('不可以双向都分页！')
                    pass  # if

                ## 根据分页的方向，赋值分页与不分页方向之相关变量
                if paging_direction == 'horizontal':
                    num_figure_in_paging_direction = num_figure_in_horizontal_direction
                    num_figure_in_no_paging_direction = num_figure_in_vertical_direction
                    max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
                    max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
                    match_pattern_in_paging_direction = match_pattern_in_horizontal_direction
                    match_pattern_in_no_paging_direction = match_pattern_in_vertical_direction
                    single_plot_size_in_paging_direction = single_plot_size_width
                    single_plot_size_in_no_paging_direction = single_plot_size_height
                    num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
                    num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
                    num_figure_in_horizontal_direction_per_page = num_figure_in_paging_direction_per_page
                    num_figure_in_vertical_direction_per_page = num_figure_in_no_paging_direction_per_page
                elif paging_direction == 'vertical':
                    num_figure_in_paging_direction = num_figure_in_vertical_direction
                    num_figure_in_no_paging_direction = num_figure_in_horizontal_direction
                    max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
                    max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
                    match_pattern_in_paging_direction = match_pattern_in_vertical_direction
                    match_pattern_in_no_paging_direction = match_pattern_in_horizontal_direction
                    single_plot_size_in_paging_direction = single_plot_size_height
                    single_plot_size_in_no_paging_direction = single_plot_size_width
                    num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
                    num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
                    num_figure_in_horizontal_direction_per_page = num_figure_in_no_paging_direction_per_page
                    num_figure_in_vertical_direction_per_page = num_figure_in_paging_direction_per_page
                elif paging_direction == 'none':  # 如果不分页，那么默认按照纵向分页的情况处理  #HACK 应该处理成真正不分页的情况
                    num_figure_in_paging_direction = num_figure_in_vertical_direction
                    num_figure_in_no_paging_direction = num_figure_in_horizontal_direction
                    max_num_of_figures_in_paging_direction_per_page = max_num_of_figures_in_vertical_direction_per_page
                    max_num_of_figures_in_no_paging_direction_per_page = max_num_of_figures_in_horizontal_direction_per_page
                    match_pattern_in_paging_direction = match_pattern_in_vertical_direction
                    match_pattern_in_no_paging_direction = match_pattern_in_horizontal_direction
                    single_plot_size_in_paging_direction = single_plot_size_height
                    single_plot_size_in_no_paging_direction = single_plot_size_width
                    num_figure_in_paging_direction_per_page = min(num_figure_in_paging_direction, max_num_of_figures_in_paging_direction_per_page) if max_num_of_figures_in_paging_direction_per_page is not None else num_figure_in_paging_direction
                    num_figure_in_no_paging_direction_per_page = min(num_figure_in_no_paging_direction, max_num_of_figures_in_no_paging_direction_per_page) if max_num_of_figures_in_no_paging_direction_per_page is not None else num_figure_in_no_paging_direction
                    num_figure_in_horizontal_direction_per_page = num_figure_in_no_paging_direction_per_page
                    num_figure_in_vertical_direction_per_page = num_figure_in_paging_direction_per_page
                    pass  # if

                total_figures_per_page = num_figure_in_horizontal_direction_per_page * num_figure_in_vertical_direction_per_page  # 每页最大总图数
                num_pages = int(np.ceil(len(pkl_panel_file_list) / total_figures_per_page))  # 最大总页数

                ## 排序，优先按照需要分页的方向，其次按照不需要分页的方向。
                sorted_pkl_panel_file_list = sorted(pkl_panel_file_list, key=lambda name: (
                    re.search(match_pattern_in_paging_direction, name)[0] if not re.search(match_pattern_in_paging_direction, name)[0].isdigit() else int(re.search(match_pattern_in_paging_direction, name)[0]),
                    re.search(match_pattern_in_no_paging_direction, name)[0] if not re.search(match_pattern_in_no_paging_direction, name)[0].isdigit() else int(re.search(match_pattern_in_no_paging_direction, name)[0]),
                ))

                ## 分页处理
                merged_pdf = fitz.open()  # 新建需要合并的pdf
                for page_idx in range(num_pages):

                    ## 创建一个新的分页
                    merged_pdf_page = merged_pdf.new_page(
                        # -1, # 这里不需要指定页码，fitz会自动分配
                        width=single_plot_size_width * num_figure_in_horizontal_direction_per_page,
                        height=single_plot_size_height * num_figure_in_vertical_direction_per_page,
                    )

                    ## 对于该新的分页，逐个导入单幅svg文件，转换成单幅pdf，临时装订pdf
                    binded_pdf = fitz.open()  # 创建一个空白pdf用于装订单幅pdf
                    for i in range(total_figures_per_page):
                        idx = page_idx * total_figures_per_page + i
                        if idx >= len(pkl_panel_file_list):
                            break
                        filepath = sorted_pkl_panel_file_list[idx]
                        svg_file = svg2rlg(filepath)
                        renderPDF.drawToFile(svg_file, filepath.split('.')[0] + '.pdf')
                        single_pdf_file = fitz.open(filepath.split('.')[0] + '.pdf')
                        binded_pdf.insert_pdf(single_pdf_file)
                        single_pdf_file.close()
                        pass  # for

                    ## 设置装订的pdf之每个图在该新的分页之位置
                    page_content_positions = []
                    for i in range(num_figure_in_paging_direction_per_page):
                        if (
                                paging_direction != 'none'  # 如果是存在分页的情况
                                and page_idx == num_pages - 1  # 如果是最后一页
                                and num_figure_in_paging_direction % num_figure_in_paging_direction_per_page != 0  # 如果最后一页不是满页的情况
                                and i >= num_figure_in_paging_direction % num_figure_in_paging_direction_per_page  # 如果该索引处于空行或者空列
                        ):
                            break  # 需要分页方向跳过最后一页的空行或者空列
                            pass  # if
                        for j in range(num_figure_in_no_paging_direction_per_page):
                            if paging_direction == 'horizontal':
                                page_content_positions.append(
                                    fitz.Rect(single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * (i + 1), single_plot_size_in_no_paging_direction * (j + 1))
                                )
                            elif paging_direction == 'vertical':
                                page_content_positions.append(
                                    fitz.Rect(single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * (j + 1), single_plot_size_in_paging_direction * (i + 1))
                                )
                            elif paging_direction == 'none':
                                page_content_positions.append(
                                    fitz.Rect(single_plot_size_in_no_paging_direction * j, single_plot_size_in_paging_direction * i, single_plot_size_in_no_paging_direction * (j + 1), single_plot_size_in_paging_direction * (i + 1))
                                )
                                pass  # if
                            pass  # for
                        pass  # for

                    ## 将装订的pdf之每个图放到该新的分页之对应的位置
                    for i_fig, page in enumerate(binded_pdf):
                        merged_pdf_page.show_pdf_page(page_content_positions[i_fig], binded_pdf, page.number)
                        pass  # for

                    binded_pdf.close()
                    pass  # for

                ## 保存
                merged_pdf.save(Path(sgv['folderpath_plots_makeup_balanceSheets'], 'BB_exp=' + str(i_exp) + '.pdf'))
                merged_pdf.close()

                # pass  # for

                pass  # if 拼接资产负债表

            pass  # for  实验编号

        pass  # if  判断是否已经导入数据

    pass  # function
