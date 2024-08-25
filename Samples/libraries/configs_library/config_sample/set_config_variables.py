"""
程序：设置配置项变量 SimulatorGlobalVariables。

记得这里发生变更时，要手动检查`Operator.operate_experiment`相关设置是否要更新。
"""

######### 设置配置项变量 #########################################

set_config_variables = dict(

    simulator_version=r"v0.0.27_alpha",  # 模拟器版本号

    schedule_operation=dict(
        实验组模拟程序=True,  # 默认 True
        可视化结果程序=False,  # 默认 False
    ),
    init_data_method=r"import data",  # 初始化数据方式。初始化方式有如下："import data"、"set manually"、"randomly"、"only init"。默认"import data"；
    init_parameters_method=r"import data",  # 初始化参数方式。初始化方式有如下："import data"、"set manually"。默认"import data"；
    type_of_experiments_foldername=r"manually",  # 设置实验文件夹命名方式。默认"manually"；
    foldername_prefix_experiments=r"样例演示",  # 手动设置初始生成的实验文件夹前缀名。默认"default"；
    is_datetime=True,  # 是否使用日期时间作为实验文件夹名称的一部分。默认 True；
    foldername_outputData=r"SystemicRiskSimulator",  # 输出数据所在工程文件夹名称
    folderpath_realpath_outputData=r"../",  # 输出数据所在工程文件夹相对本实验项目根路径文件夹之相对路径
    folderpath_root_experiments=r"Samples/data/sims",  # 手动设置实验文件夹根路径。默认"Samples/data/sims/"；
    foldername_experiments_output_data=r"exp_output_data",  # 手动设置实验导出数据文件夹名称。默认"exp_output_data"；
    folderpath_models=r"Samples/libraries/models_library/IB1111_sample",  # 模型所在的文件夹
    folderpath_config=r"Samples/libraries/configs_library/config_sample",  # 配置项设置所在的文件夹
    folderpath_parameters=r"Samples/libraries/parameters_library/parameters_sample",  # 参数设置所在的文件夹
    folderpath_agents=r"Samples/libraries/agents_library/agents_sample",  # 个体众数据初始化所在的文件夹
    list_agents_yearName=['2012'],  # 设置 agents 初始数据列表（按照年份名称）
    running_mode=r"continue running mode",  # 运行模式。取值："continue running mode": 持续运行模式, "stepping running mode": 步进运行模式}，否则一路直接运行。默认"continue running mode"； #BUG 暂时还没有重构"stepping running mode"的情况，因此设置为该模式会出错
    step_size=1,  # 设置步进跨度；如果该数值设置较大，则相当于直接处理程序；
    list_idsExperiment_to_run=None,  # 设置要运行的实验编号列表。默认 None，表示运行所有实验。

    num_bank=5,  # 手动输入银行个数（NOTE：如果是手动设置数据，那么设置具体值的时候必须保证是正确的。如果设置为 None 或者不设置，那么就会忽略该变量的设置值，而是根据实际情况计算一个值）；
    num_assets=1,  # 资产种类数（NOTE：如果是手动设置数据，那么设置具体值的时候必须保证是正确的。如果设置为 None 或者不设置，那么就会忽略该变量的设置值，而是根据实际情况计算一个值）；
    is_auto_confirmation=False,  # 是否自动确认一些比较危险的操作例如删除、移动、复制文件等。默认 False；
    is_auto_open_outputlog=True,  # 是否自动打开输出日志文件。默认 True；

    ## 调试专用变量：
    is_maintain_model_files_in_simulator_when_develope_mode=True,  # 是否处于测试状态
    test_logging=10,  # 日志输出级别。调试级别是10，输出信息级别是20。具体见：[logging —— python的日志记录工具](https://docs.python.org/zh-cn/3.9/library/logging.html#levels)
    test_turn_for_test=4,  # test变量，用于打断点。相关语句：`sgv['turn']>=sgv['test_turn_for_test']`；
    test_max_num_of_turn=100,  # 最大运行轮次数（测试用）；



    ## 使用的模型类型类型设置：
    is_use_Gymnasium_model=False,  # 是否使用用于强化学习的环境模型。默认 False。

    ## 设置可视化：
    need_visualization=True,  # 是否需要可视化。默认 False；
    foldername_experiments=r'样例演示_20231227203220',  # 实验文件夹名称（NOTE：这个需要根据模拟程序运行完成之后自行查看相关的文件夹名称然后手动填入）
    foldername_plots=r'plots',  # 实验导出可视化的数据文件夹名称。
    foldername_plots_single_heatmaps=r'单个矩阵热力图',  # 实验导出可视化的单个矩阵热力图之文件夹之名称。
    foldername_plots_makeup_heatmaps=r'拼版矩阵热力图',  # 实验导出可视化的拼版矩阵热力图之文件夹之名称。
    foldername_plots_single_graphs=r'单个网络图',  # 实验导出可视化的单个网络图之文件夹之名称。
    foldername_plots_makeup_graphs=r'拼版网络图',  # 实验导出可视化的拼版网络图之文件夹之名称。
    foldername_plots_single_balanceSheets=r'单个资产负债表',  # 实验导出可视化的单个资产负债表之文件夹之名称。
    foldername_plots_makeup_balanceSheets=r'拼版资产负债表',  # 实验导出可视化的拼版资产负债表之文件夹之名称。

    visulization_process=dict(
        导入Pandas格式的实验结果数据转换为面板形式再导出=False,  # 默认True。NOTE：这个只需要运行一次即可。
        导入面板形式的CSV数据预处理=False,  # 默认False
        读取面板形式的PKL格式的文件=True,  # 默认True
        绘制矩阵热图=False,  # 默认True
        拼接矩阵热图=False,  # 默认True
        绘制资金流网络图=True,  # 默认True
        拼接资金流网络图=True,  # 默认True
        绘制资产负债表图=False,  # 默认True
        拼接资产负债表图=False,  # 默认True
    ),

    vis=dict(
        list_dataNames_for_graph_figs=['A_IB', 'Z_IB'],  # 数据类别
        time_granularity=r'步进粒度',  # 绘制的时间线粒度的粒度，有：'轮次粒度'、'步进粒度'；默认'步进粒度'。#DEBUG 还没有验证和适配'turn'。
        one_bank_BalanceSheet_width=600,  # 单个银行资产负债表的宽度
        one_bank_BalanceSheet_height=600,  # 单个银行资产负债表的高度
        one_bank_BalanceSheet_title_height=15,  # 单个银行资产负债表的标题高度
        one_bank_BalanceSheet_border=5,  # 单个银行资产负债表的边框宽度

        ## 设置各银行状态之颜色
        dict_state_colors={
            'hel': '#F1D0CB',  # 浅红色
            'isv': '#D9E8D6',  # 浅绿色
            'ilq': '#DDE8FA',  # 浅蓝色
            'ilq,isv': '#DFD6E6',  # 浅紫色
            # '-rr': '#FDF3D0',  # 浅黄色 # NOTE 后续可以根据需要自行添加新状态
            'br': '#CCCCCC',  # 灰色
            'off': '#999999',  # 深灰色
        },

        ## 设置不同数据对应的属性
        list_dataTypes_for_heatmaps=[
            dict(
                data_name=('A_IB_all', 'Z_IB_all', 'A_IB'),
                colormap=('#FFFFFF', '#FF00FF'),
            ),
            dict(
                data_name=('Shock_IB_def_t', 'Shock_IB_def_s', 'Shock_IB_def'),
                colormap=('#FFFFFF', '#FF0000'),
            ),
            dict(
                data_name=('Shock_IB_run_ilq_t', 'Shock_IB_run_ilq_s', 'Shock_IB_run_ilq'),
                colormap=('#FFFFFF', '#FF0000'),
            ),
            dict(
                data_name=('Shock_IB_run_br_t', 'Shock_IB_run_br_s', 'Shock_IB_run_br'),
                colormap=('#FFFFFF', '#FF0000'),
            ),
            dict(
                data_name=('Z_IB_all', 'A_IB_all', 'Z_IB'),
                colormap=('#FFFFFF', '#0000FF'),
            ),
            dict(
                data_name=('Bo_IB_all', 'Li_IB_all', 'Bo_IB'),
                colormap=('#FFFFFF', '#0000FF'),
            ),
            # NOTE 后续可以根据需要自行添加银行状态与债权债务关系网络
        ]

    ),
    ###########################

)
