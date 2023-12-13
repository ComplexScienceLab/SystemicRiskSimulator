"""
程序：设置配置项变量 SimulatorGlobalVariables。

记得这里发生变更时，要手动检查`Operator.operate_experiment`相关设置是否要更新。
"""

######### 设置配置项变量 #########################################

set_config_variables = dict(

    schedule_operation=dict(
        实验组模拟程序=True,  # 默认 True
        可视化结果程序=False,  # 默认 False
    ),
    # schedule_operation=dict(
    #     实验组模拟程序=False,  # 默认 True
    #     可视化结果程序=True,  # 默认 False
    # ),
    init_data_method=r"import data",  # 初始化数据方式。初始化方式有如下："import data"、"set manually"、"randomly"、"only init"。默认"import data"；
    init_parameters_method=r"import data",  # 初始化参数方式。初始化方式有如下："import data"、"set manually"。默认"import data"；
    type_of_experiments_foldername=r"set manually",  # 设置实验文件夹命名方式。默认"set manually"；
    foldername_prefix_experiments=r"test",  # 手动设置初始生成的实验文件夹前缀名。默认"default"；
    is_datetime=True,  # 是否使用日期时间作为实验文件夹名称的一部分。默认 True；
    foldername_experiments_output_data=r"exp_output_data",  # 手动设置实验导出数据文件夹名称。默认"exp_output_data"；
    folderpath_data=r"Samples/data",  # 数据所在的文件夹
    simulator_version=r"v0.0.23_alpha",  # 模拟器版本号
    folderpath_root_experiments=r"Samples/data/sims",  # 手动设置实验文件夹根路径。默认"Samples/data/sims/"；
    folderpath_models=r"Samples/libraries/models_library/IB1111_非流程多函数版",  # 模型所在的文件夹
    # folderpath_models=r"Samples/libraries/models_library/IB1111_扁平流程版",  # 模型所在的文件夹
    folderpath_config=r"Samples/libraries/configs_library/config_010",  # 配置项设置所在的文件夹
    folderpath_parameters=r"Samples/libraries/parameters_library/parameters_010",  # 参数设置所在的文件夹
    folderpath_agents=r"Samples/libraries/agents_library/agents_010",  # 个体众数据初始化所在的文件夹（#NOTE 仅用于`type_of_experiments_foldername = "set manually"`）
    running_mode=r"continue running mode",  # 运行模式。取值："continue running mode": 持续运行模式, "stepping running mode": 步进运行模式}，否则一路直接运行。默认"continue running mode"； #BUG 暂时还没有重构"stepping running mode"的情况，因此设置为该模式会出错
    step_size=1,  # 设置步进跨度；如果该数值设置较大，则相当于直接处理程序；
    # is_auto_confirmation=False,  # 是否自动确认一些比较危险的操作例如删除、移动、复制文件等。默认 False；
    is_auto_confirmation=True,  # 是否自动确认一些比较危险的操作例如删除、移动、复制文件等。默认 False；
    is_auto_open_outputlog=True,  # 是否自动打开输出日志文件。默认 True；

    num_bank=5,  # 手动输入银行个数（NOTE：如果设置具体值，必须保证是正确的。如果设置为 None 或者不设置，那么会自动计算该变量值然后覆盖设置值）；
    num_assets=1,  # 资产种类数；

    ## 调试专用变量：
    is_test=True,  # 是否处于测试状态
    test_logging=10,  # 日志输出级别。调试级别是10，输出信息级别是20。具体见：[logging —— python的日志记录工具](https://docs.python.org/zh-cn/3.9/library/logging.html#levels)
    test_round_for_test=4,  # test变量，用于打断点。相关语句：`sgv['round']>=sgv['test_round_for_test']`；
    test_max_num_of_round=24,  # 最大运行轮次数（测试用）；

    ## 使用的程序版本类型设置：
    is_use_flow_form_version_model=False,  # 是否使用流程形式的版本的模型形式。默认False。如果 False ，则表示不采用带有多文件多模块的旧版本的模型表示形式，而是直接采用简化的单文件模型。

    ## 设置可视化：
    need_visualization=True,  # 是否需要可视化。默认 False；
    foldername_experiments=r'test_20231208212020_尝试可视化结果',  # 实验文件夹名称
    foldername_plots=r'plots',  # 实验导出可视化的数据文件夹名称。
    foldername_plots_single_graphs=r'单个网络图',  # 实验导出可视化的单个网络图之文件夹之名称。
    foldername_plots_makeup_graphs=r'拼版网络图',  # 实验导出可视化的拼版网络图之文件夹之名称。
    foldername_plots_single_balanceSheets=r'单个资产负债表',  # 实验导出可视化的单个资产负债表之文件夹之名称。
    foldername_plots_makeup_balanceSheets=r'拼版资产负债表',  # 实验导出可视化的拼版资产负债表之文件夹之名称。
    list_data_name=['A_IB', 'Z_IB'],  # 数据类别
    time_granularity=r'步进粒度',  # 绘制的时间线粒度的粒度，有：'轮次粒度'、'步进粒度'；默认'步进粒度'。#TODO还没有验证和适配'round'。
    visulization_process=dict(
        导入Pandas格式的实验结果数据转换为面板形式再导出=True,  # 默认True
        导入面板形式的CSV数据预处理=False,  # 默认False
        读取面板形式的PKL格式的文件=True,  # 默认True
        绘制资产负债表=True,  # 默认True
        绘制资金流网络图=True,  # 默认True
        拼接资产负债表=True,  # 默认True
        拼接资金流网络图=True,  # 默认True
    ),
    ###########################

)
