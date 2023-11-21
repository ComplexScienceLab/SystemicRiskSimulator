"""
程序：设置环境变量EnvironmentVariables。

记得这里发生变更时，要手动检查`Operator.operate_experiment`相关位置是否要更新。
"""

######### 设置环境变量 #########################################

set_environments_variables = dict(

    init_method="set manually",  # 初始化数据方式；
    type_of_experiments_foldername="set manually",  # 设置实验文件夹命名方式。默认"set manually"；
    foldername_prefix_of_experiments="test",  # 手动设置实验文件夹前缀名。默认"default"；
    root_dir_of_experiments=r"data/sims",  # 手动设置实验文件夹根路径。默认"/data/sims/"；
    foldername_of_experiments_output_data="exp_output_data",  # 手动设置实验导出数据文件夹名称。
    folderpath_of_entityData=r"SystemicRiskSimulator/models/entities_data/__init__.py",  # 手动设置实体数据文件夹路径
    modulepath_of_entityData=r"SystemicRiskSimulator.models.entities_data",  # 手动设置实体数据模块路径
    folderpath_settings_environments=r"Samples/settings/environments",  # 设置项之环境设置所在的文件夹
    folderpath_settings_parameters=r"Samples/settings/parameters",  # 设置项之参数设置所在的文件夹
    folderpath_settings_agents=r"Samples/settings/agents",  # 设置项之个体众数据初始化所在的文件夹（#NOTE 仅用于`type_of_experiments_foldername = "set manually"`）
    folderpath_models=r"Samples/models",  # 模型所在的文件夹
    folderpath_data=r"Samples/data",  # 数据所在的文件夹
    running_mode="continue running mode",  # 运行模式。取值："continue running mode": 持续运行模式, "stepping running mode": 步进运行模式}，否则一路直接运行。默认"continue running mode"； #BUG 暂时还没有重构"stepping running mode"的情况，因此设置为该模式会出错
    step_size=1,  # 设置步进跨度；如果该数值设置较大，则相当于直接处理程序；

    num_bank=5,  # 银行个数；
    num_assets=1,  # 资产种类数；

    ## 调试专用变量：
    is_test=True,  # 是否处于测试状态
    test_logging=10,  # 日志输出级别。调试级别是10，输出信息级别是20。具体见：[logging —— python的日志记录工具](https://docs.python.org/zh-cn/3.9/library/logging.html#levels)
    test_round_for_test=4,  # test变量，用于打断点。相关语句：env['round']>=env['test_round_for_test']；
    test_max_num_of_round=24,  # 最大运行轮次数（测试用）；

    ## 使用的程序版本类型设置：
    is_use_simple_form_version_algorithm=True,  # 是否使用简化形式的版本的算法形式。默认True。如果是，则表示不采用带有多文件多模块的旧版本的算法表示形式，而是直接采用简化的单文件算法

    ###########################

)
