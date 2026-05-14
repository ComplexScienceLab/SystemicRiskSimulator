"""
程序：设置配置项变量 SimulatorGlobalVariables。
"""
import sys

######### 设置配置项变量 #########################################

set_config_variables = dict(
    simulator_version=r"v0.2_alpha",  # 模拟器版本号

    schedule_operation=dict(
        实验组模拟程序=True,  # 默认 True
        预处理实验结果程序=True,  # 默认 True
        可视化结果程序=True,  # 默认 False
    ),

    list_agents_data_filename_para_01=['BB', 'DA', 'IB', 'IBA', 'note'],  # 设置 agents 初始数据列表
    list_agents_data_filename_para_02=['year', 'density_IB', 'density_IBA'],  # 设置 agents 初始数据列表文件名相关的参数
    init_data_method=r"import data",  # 初始化数据方式。初始化方式有如下："import data"、"set manually"、"randomly"、"only init"。默认"import data"；
    init_parameters_method=r"import data",  # 初始化参数方式。初始化方式有如下："import data"、"set manually"。默认"import data"；
    # type_of_experiments_foldername=r"default",  # 设置实验文件夹命名方式。取值："default"、"manually"。默认"default"；
    type_of_experiments_foldername=r"manually",  # 设置实验文件夹命名方式。取值："default"、"manually"。默认"default"；

    # # 手动设置生成的实验文件夹全名。用于 `type_of_experiments_foldername=r"manually"`；
    foldername_set_manually=r"sample_IB1211",
    foldername_prefix_experiments=r"sample_IB1211",  # 手动设置初始生成的实验文件夹前缀名。默认"default"。当设置实验文件夹命名方式取值 "default" 的时候激活；
    is_datetime=True,  # 是否使用日期时间作为实验文件夹名称的一部分。默认 True；
    foldername_outputData=r"SystemicRiskData",  # 输出数据总文件夹名称
    folderpath_realpath_outputData=r".",  # 从本实验项目根路径文件夹到输出数据所在总文件夹之相对路径。
    folderpath_root_experiments=r"data/sims_samples",  # 手动设置实验文件夹根路径。默认"data/sims/"；
    foldername_experiments_output_data=r"exp_output_data",  # 手动设置实验导出数据文件夹名称。默认"exp_output_data"；
    folderpath_models=r"Samples/libraries/models_library/model_sample_IB1211",  # 模型所在的文件夹
    folderpath_config=r"Samples/libraries/configs_library/config_sample_IB1211",  # 配置项设置所在的文件夹
    folderpath_parameters=r"Samples/libraries/parameters_library/parameters_sample_IB1211",  # 参数设置所在的文件夹
    folderpath_agents=r"Samples/libraries/agents_library/agents_sample_IB1211",  # 个体众数据初始化所在的文件夹
    # list_agents_yearName=['2012', '2013'],  # 设置 agents 初始数据列表（按照年份名称）
    list_agents_yearName=['2012'],  # 设置 agents 初始数据列表（按照年份名称） #DEBUG 调试专用
    running_mode=r"continue running mode",  # 运行模式。取值："continue running mode": 持续运行模式, "stepping running mode": 步进运行模式}，否则一路直接运行。默认"continue running mode"； #BUG 暂时还没有重构"stepping running mode"的情况，因此设置为该模式会出错
    step_size=1,  # 设置步进跨度；如果该数值设置较大，则相当于直接处理程序；

    is_enable_multiprocessing_for_run_model=False,  # 运行模型期间，是否启用的多进程。默认 False；
    percent_core_for_multiprocessing=0.75,  # 设置多进程的 CPU 核心数与该设备总的 CPU 核心数占比。默认 0.75；
    is_rerun_all_done_works_in_the_same_experiments=True,  # 是否重新运行所有已经完成的实验。默认 True。如果为 True，则在实验运行之前，重置该实验组当中所有的实验作业运行状态为 "RAW"。
    # is_rerun_all_done_works_in_the_same_experiments=False,  # 是否重新运行所有已经完成的实验。默认 True。如果为 True，则在实验运行之前，重置该实验组当中所有的实验作业运行状态为 "RAW"。
    is_use_sqlite_to_manage_experiments=False,  # 是否使用 SQLite 数据库来管理实验。默认 False；
    is_draw_color_band_distribution_before_experiments=False,  # 是否在实验运行之前绘制颜色带分布图，展示实验组 id 分布对应的实验组作业运行之前的作业完成状态信息。默认 False；
    # list_idsExperiment_to_run=None,  # 设置要运行的实验编号列表。默认 None，表示运行所有实验。
    list_idsExperiment_to_run=[46],  # 设置要运行的实验编号列表。默认 None，表示运行所有实验。#DEBUG 用于调试
    # list_idsExperiment_to_run=[4862, 4970],  # 设置要运行的实验编号列表。默认 None，表示运行所有实验。#DEBUG 用于调试
    # list_idsExperiment_to_run=list(range(4861, 5076 + 1)),  # 设置要运行的实验编号列表。默认 None，表示运行所有实验。#DEBUG 用于调试
    # list_idsExperiment_to_run=list(range(4861, 4870 + 1)),  # 设置要运行的实验编号列表。默认 None，表示运行所有实验。#DEBUG 用于调试
    # list_idsExperiment_to_run=[4880],  # 设置要运行的实验编号列表。默认 None，表示运行所有实验。#DEBUG 用于调试

    num_bank=5,  # 手动输入最大的银行个数（NOTE：如果是手动设置数据，那么设置具体值的时候必须保证是正确的。如果设置为 None 或者不设置，那么就会忽略该变量的设置值，而是根据实际情况计算一个值）；
    num_asset=4,  # 手动输入最大的资产种类数（NOTE：如果是手动设置数据，那么设置具体值的时候必须保证是正确的。如果设置为 None 或者不设置，那么就会忽略该变量的设置值，而是根据实际情况计算一个值）；

    is_auto_confirmation=True,  # 是否自动确认一些比较危险的操作例如删除、移动、复制文件等。默认 False；
    is_auto_open_outputlog=False,  # 是否自动打开输出日志文件。默认 False；
    system_platform=sys.platform,  # 获取系统信息

    # 开发、调试模型专用变量：
    # NOTE：开发优先改造后，默认不再依赖把资源复制到 `SystemicRiskSimulator/data/*` 固定目录。

    # NOTE：运行时资源策略（开发优先默认值）
    runtime_model_import_source='external',  # 'external' | 'simulator_data'
    runtime_copy_resources_into_simulator_data=False,  # 默认不复制 config/agents/parameters 到模拟器包内 data/*
    is_develope_mode=True,  # 是否处于开发状态。默认 False。默认情况下，模拟器通在子进程独立启用相关的程序。启用之后，在模拟器中，将通过函数调用的方式调用各个程序。启用之后，适合在 Python 3.11 开始的版本做断点调试。
    is_maintain_model_files_in_simulator_when_develope_mode=True,  # 如果 is_develope_mode == True ，那么启用是否保留模拟器里的模型？默认 False。运行的时候只会运行输出文件夹内已有的模型，而不会运行外部导入的模型，运行后也不会将其删除。如果你想直接运行输出文件夹内已有的模型，并且做开发模型相关的工作，建议开启此项。
    is_ignore_warning=True,  # 是否忽略警告。默认 False；
    test_logging=10,  # 日志输出级别。调试级别是10，输出信息级别是20。具体见：[logging —— python的日志记录工具](https://docs.python.org/zh-cn/3.9/library/logging.html#levels)
    test_turn_for_debug=4,  # test变量，用于打断点。相关语句：`sgv['turn']>=sgv['test_turn_for_debug']`；
    test_max_num_of_turn=1000,  # 最大运行轮次数（调试用）。默认 10000；

    # 其它配置
    is_compress_result_data=False,  # 是否压缩实验结果数据。默认 True。建议开启此项，尤其是一批次实验生成大量数据。

    # 收集数据设置
    is_collect=True,  # 是否收集当前的数据。默认 False 。
    collect=None,  # 收集数据设置。默认 None。可选值包括：'None'、具体的 Python 列表列出需要收集的变量。

    # 导出配置
    is_export_data_to_xlsx=True,  # 是否导出数据到 XLSX 文件。默认 False；
    is_export_data_to_csv=False,  # 是否导出数据到 CSV 文件。默认 False；

    # NOTE 使用的模型类型类型设置：
    is_use_Gym_environments=False,  # 是否使用 PettingZoo 环境框架。默认 True。
    is_use_RL_method=False,  # 是否使用强化学习方法。默认 True。

    # NOTE 手动设置后续处理用的实验文件夹名
    foldername_experiments=r'sample_IB1211',  # 实验文件夹名称

    # NOTE 设置预处理实验结果数据：
    # is_enable_multiprocessing_for_transform_output_data=True,  # 是否启用多进程。默认 False；
    is_enable_multiprocessing_for_transform_output_data=False,  # 是否启用多进程。默认 False；
    transform_data=dict(
        导入Pandas格式的实验结果数据转换为面板形式再导出=True,  # 默认 True。（NOTE：这个只需要运行一次即可。）
        导入Pandas格式的实验结果数据合并为一个文件=False,  # 默认 False。（NOTE：这个只需要运行一次即可。）
    ),

    # NOTE 设置 【导入Pandas格式的实验结果数据转换为面板形式再导出】 当中需要插入到主变量的 note 列。
    # 其中，三元组的第一个元素是需要插入的列名，第二个元素是需要插入的字段名的值，第三个元素是将新插入的列名移动到指定的列名的后面。
    columns_to_insert_into_panel_data=dict(
        BB=[
            ('fullName', 'fullName_bank', 'id_agent'),
        ],
        DA=[
            ('fullName', 'fullName_asset', 'id_agent'),
        ],
        IB=None,
        IBA=None,
    ),

    list_table_for_explode=['BB', 'DA', 'IB', 'IBA'],  # 列表，设置需要展开的表格名称。

    # NOTE 设置可视化：
    is_enable_multiprocessing_for_visualization=True,  # 可视化期间，是否启用多进程。默认 True；
    foldername_plots=r'plots',  # 实验导出可视化的数据文件夹名称。
    foldername_plots_single_heatmaps=r'单个矩阵热力图',  # 实验导出可视化的单个矩阵热力图之文件夹之名称。
    foldername_plots_makeup_heatmaps=r'拼版矩阵热力图',  # 实验导出可视化的拼版矩阵热力图之文件夹之名称。
    foldername_plots_single_balanceSheets=r'单个资产负债表图',  # 实验导出可视化的单个资产负债表图之文件夹之名称。
    foldername_plots_makeup_balanceSheets=r'拼版资产负债表图',  # 实验导出可视化的拼版资产负债表图之文件夹之名称。
    foldername_plots_single_graphs=r'单个网络图',  # 实验导出可视化的单个网络图之文件夹之名称。
    foldername_plots_makeup_graphs=r'拼版网络图',  # 实验导出可视化的拼版网络图之文件夹之名称。
    foldername_visualize_banksStates_table=r'银行状态表',  # 实验导出可视化的银行状态表格之文件夹之名称。

    visulization_process=dict(
        导入面板形式的CSV数据预处理=False,  # 默认 False
        绘制资产负债表图=True,  # 默认 True
        拼接资产负债表图=True,  # 默认 True
        绘制矩阵热图=True,  # 默认 True
        拼接矩阵热图=True,  # 默认 True
        绘制资金流网络图=False,  # 默认 True
        拼接资金流网络图=False,  # 默认 True
        银行状态表格可视化=False,  # 默认 True
    ),

    # #NOTE 设置可视化的选项
    vis=dict(
        # list_idsExperiment_to_vis=[46, 47, 48, 49, 50, 51, 56, 61, 67, 68],  # 设置要可视化的实验编号列表。默认 None，表示可视化所有实验组。
        # list_idsExperiment_to_vis=list(range(1, 68 + 1)),  # 设置要可视化的实验编号列表。默认 None，表示可视化所有实验组。
        list_idsExperiment_to_vis=[46],  # 设置要可视化的实验编号列表。默认 None，表示可视化所有实验组。

        time_granularity=r'步进粒度',  # 绘制的时间线粒度的粒度，有：'轮次粒度'、'步进粒度'；默认'步进粒度'。#DEBUG 还没有验证和适配'turn'。
        one_bank_BalanceSheet_width=600,  # 单个银行资产负债表的宽度
        one_bank_BalanceSheet_height=600,  # 单个银行资产负债表的高度
        one_bank_BalanceSheet_title_height=21,  # 单个银行资产负债表的标题高度
        one_bank_BalanceSheet_border=16,  # 单个银行资产负债表的边框宽度

        # 设置各银行状态之颜色
        dict_state_colors={
            'hel': '#F1D0CB',  # 浅红色
            'isv': '#D9E8D6',  # 浅绿色
            'br': '#CCCCCC',  # 灰色
            'exit': '#999999',  # 深灰色
        },

        # 设置各银行关系（包括债权债务关系）之颜色
        dict_relation_colors={
            'cre': '#E7C300',  # 黄色
            'deb': '#68ED8A',  # 绿色
        },

        # #NOTE 设置矩阵热力图不同数据对应的属性

        # 设置绘制矩阵热图子图行列值之数据、颜色映射、关系类型
        list_dataTypes_for_heatmaps=[
            dict(
                data_name=('A_IB_all', 'Z_IB_all', 'A_IB'),
                colormap=('#FFFFFF', '#FF00FF'),
                relations='deb',
            ),
            dict(
                data_name=('Shock_IB_def_s', 'Shock_IB_def_t', 'Shock_IB_def'),
                colormap=('#FFFFFF', '#FF0000'),
                relations='cre',
            ),
            # dict(
            #     data_name=('Loss_exIB_def_t', 'Default_D_def_s', 'Loss_IB_def'),
            #     colormap=('#FFFFFF', '#000000'),
            #     relations='deb',
            # ),
            dict(
                data_name=('Loss_IB_def_t', 'Default_IB_def_s', 'Loss_IB_def'),
                colormap=('#FFFFFF', '#000000'),
                relations='deb',
            ),
            dict(
                data_name=('Default_s', 'Loss_t', 'Default_IB'),
                colormap=('#FFFFFF', '#A78900'),
                relations='cre',
            ),
            dict(
                data_name=('Z_IB_all', 'A_IB_all', 'Z_IB'),
                colormap=('#FFFFFF', '#554EE6'),
                relations='cre',
            ),
            dict(
                data_name=('A_P', 'DA', 'IBA'),
                colormap=('#FFFFFF', '#FF00FF'),
                relations='deb',
            ),
            dict(
                data_name=('A_P', 'DA', 'IDA_exp_factor'),
                colormap=('#FFFFFF', '#FF00FF'),
                relations='deb',
            ),
            dict(
                data_name=('Loss_IBA_def_t', 'Shock_IBA_s', 'Loss_IBA'),
                colormap=('#FFFFFF', '#FF00FF'),
                relations='deb',
            ),
            # dict(
            #     data_name=('Shock_IBA_def_s', 'Shock_IBA_t', 'Shock_IBA_def'),
            #     colormap=('#FFFFFF', '#FF00FF'),
            #     relations='deb',
            # ),
            dict(
                data_name=('Shock_IBA_def_t', 'Shock_IBA_s', 'Shock_IBA_def'),
                colormap=('#FFFFFF', '#FF00FF'),
                relations='cre',
            ),
        ],

        # 个体状态数据类型。注意，这个数据存在优先级，暨越靠前的数据类型优先使用。
        set_dataTypes_for_agentsState=[
            'exit',
            'br',
            'isv',
            'hel',
        ],

        # 设置绘制资产负债表图柱子的一些配置
        config_data_to_vis_other_variables_for_one_bank_accounts=dict(
            df_dataName=['shocks', 'loss', 'default'],
            offsetScale_by_dataType=[1 / 13, 5 / 13, 5 / 13],
            text_offsetScale_x=[3, 3, 3],
            text_offsetScale_y=[3, 3, 3],
            text_fill=['blue', '#D6D6D6', '#F5DF5D']
        ),

        # #NOTE 设置资产负债表图不同数据对应的属性
        list_dataTypes_for_balanceSheets=dict(
            # 资产负债表账户数据（字典列表形式）
            accounts=[
                dict(
                    data_type='asset',
                    level='level 2',
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
                    level='level 2',
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
                    level='level 2',
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
                    level='level 2',
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
                    level='level 2',
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
            ],

            # 冲击数据（字典列表形式）
            shocks=[
                dict(
                    data_type='shock_def_t',
                    level='level 2',
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
                    data_type='shock_def_s',
                    level='level 2',
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
            ],

            # 损失数据
            loss=[
                dict(
                    data_type='loss',
                    level='level 2',
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
                    level='level 2',
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
            ],

            # 违约数据
            default=[
                dict(
                    data_type='default',
                    level='level 2',
                    subject='Default_D_def_s',
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
                    level='level 2',
                    subject='Default_IB_def_s',
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
            ],

        ),

        # #NOTE 设置 graph 数据类别
        list_dataNames_for_graph_figs=[
            'A_IB',
            'Z_IB'
        ],

        # 根据设置 graph 数据类别，设置不同边集对应的属性
        list_data_edgeTypes_for_graph_figs=[
            [
                dict(
                    edge_type='A_IB',
                    edge_color='#CCCCCC',
                    edge_width=5,
                ),
                dict(
                    edge_type='Shock_IB_def',
                    edge_color='#FF0000',
                    edge_width=5,
                ),
            ],
            [
                dict(
                    edge_type='Z_IB',
                    edge_color='#CCCCCC',
                    edge_width=5,
                ),
                dict(
                    edge_type='Shock_IB_def',
                    edge_color='#FF0000',
                    edge_width=5,
                ),
            ]
        ],

        # #NOTE 设置银行状态表格的一些配置
        # 状态相关的列名
        columns_states=[
            'exist',
            'exit',
            'hel',
            'isv',
            'br',
            'con',
            'inf',
        ],

        # 需要提取的列名
        columnsName_extract=[
            'id',
            'id_data',
            'process_name',
            'step',
            'turn',
            'phase',
            'id_agent',
            'abbr',
            'fullName',
            'exist',
            'exit',
            'hel',
            'isv',
            'br',
            'con',
            'inf',
        ],

        # 需要调整列边距的列名
        columnsName_adjust=[
            'id',
            'id_data',
            'step',
            'turn',
            'phase',
            'id_agent',
        ],

    ),
    ###########################

)
