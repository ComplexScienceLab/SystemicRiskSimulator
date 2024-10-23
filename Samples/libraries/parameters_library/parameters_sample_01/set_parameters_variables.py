# %% [markdown]
# # 程序：设置参数变量数据记录 parameter_variables
#

# %% [markdown]
# > 注意：可能由于参数组合过多，导致生成的参数组合过多，从而导致内存溢出。或者运行时长过长。因此，需要根据实际情况来设置参数组合，并在运行之前自行估算参数组合数量。
#


# %% [markdown]
# ## 导入相关库

# %%
from SystemicRiskSimulator.external_packages import sys, Path, np, pd, pickle, itertools, time, reduce, random, logging
from SystemicRiskSimulator.tools.tools import Tools
from dask.delayed import delayed
import dask.dataframe as dd

pass  # end import


# %% [markdown]  使用 dask 实现的高性能版本的生成参数组合之函数

def _generate_all_parameter_combinations(list_agents_params, dict_list_combinations_Shock_exIB_def_t_percentage_in_agentsItems, dict_list_combinations_Strategy_default_in_agentsItems):
    inner_id = 0

    @delayed
    def _generate_parameter_combinations(inner_id, id_agents_para, year, density):
        combinations_for_each_agentsParam = list(
            itertools.product(
                dict_list_combinations_Shock_exIB_def_t_percentage_in_agentsItems[id_agents_para],
                dict_list_combinations_Strategy_default_in_agentsItems[id_agents_para]
            )
        )

        df_parameters_for_each_agentsPara = pd.DataFrame(columns=[  # #NOTE 以下位置填入你的列名
            'id_agentsPara',
            'year',
            'density',
            'inner_id',
            'Shock_exIB_def_t_percentage',
            'Strategy_default',
        ])

        df_parameters_for_each_agentsPara['id_agentsPara'] = [id_agents_para] * len(combinations_for_each_agentsParam)
        df_parameters_for_each_agentsPara['year'] = [year] * len(combinations_for_each_agentsParam)
        df_parameters_for_each_agentsPara['density'] = [density] * len(combinations_for_each_agentsParam)
        df_parameters_for_each_agentsPara['inner_id'] = list(range(len(combinations_for_each_agentsParam)))
        df_parameters_for_each_agentsPara['Shock_exIB_def_t_percentage'] = [x[0] for x in combinations_for_each_agentsParam]
        df_parameters_for_each_agentsPara['Strategy_default'] = [x[1] for x in combinations_for_each_agentsParam]

        return df_parameters_for_each_agentsPara

    # 生成所有任务
    # tasks = [_generate_parameter_combinations(*agentPara) for agentPara in list_agents_params]
    tasks = []
    for agentPara in list_agents_params:
        task = _generate_parameter_combinations(inner_id, *agentPara)
        inner_id += 1
        tasks.append(task)
        pass  # for

    # 并行计算所有任务
    df_parameters_list = dd.compute(*tasks)

    # 合并所有结果
    df_parameters = pd.concat(df_parameters_list, ignore_index=True)

    df_parameters['exp_id'] = np.arange(1, len(df_parameters) + 1)  # 在最后添加 exp_id 列
    df_parameters = df_parameters[['exp_id'] + [col for col in df_parameters.columns if col != 'exp_id']]  # exp_id 移到第一列

    return df_parameters
    pass  # function


@delayed
def save_parameter_combinations(df_parameters, filename):
    """
    异步保存参数组合
    """
    if filename.endswith('.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(df_parameters, f)
    elif filename.endswith('.csv'):
        df_parameters.to_csv(filename, index=False)
    elif filename.endswith('.xlsx'):
        df_parameters.to_excel(filename, index=False)
    else:
        raise ValueError(f"Unsupported file format: {filename}")
    return filename
    pass  # function


if __name__ == '__main__':

    # %% [markdown]
    # ## 配置项
    # 是否保存为 SQLite 数据库文件、CSV 文件、Excel 文件
    is_save_to_sqlite = False
    is_save_to_csv = False
    is_save_to_excel = True

    # %%
    config = dict()
    config['folderpath_config'] = r"libraries/configs_library/config_sample_01"  # 配置项文件夹路径
    config['foldername_simulator'] = r"SystemicRiskSimulator"  # 模拟器所在工程文件夹名称
    config['folderpath_realpath_simulator'] = r"../"  # 模拟器所在工程文件夹相对本实验项目根路径文件夹之相对路径。这里设定文件夹 "Samples" 是本样例项目根路径文件夹。
    config['is_auto_confirmation'] = True  # 是否自动确认一些比较危险的操作例如删除、移动、复制文件等。默认 False；#DEBUG #TODO 还需要改回默认值

    list_model_name = ['sample_01']  # 模型名称列表 #HACK 这个用不到
    list_agents_yearName = ['2012', '2013']  # 年份名称列表  #DEBUG 仅示例演示用。
    list_agents_networkDensity = [0.25, 1.0]  # 网络密度列表  #DEBUG 仅示例演示用。

    # %% [markdown]
    # ## 设置项

    # %%
    ## 获取项目路径、模拟器工具路径
    config['folderpath_project'] = Path(Tools.get_project_rootpath(), "Samples").resolve()  # 项目路径
    config['folderpath_simulator'] = Tools.get_project_rootpath(config['foldername_simulator'], config['folderpath_realpath_simulator'])
    # 如果 settings 之 config 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
    Tools.delete_and_recreate_folder(Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=config['is_auto_confirmation'])
    Tools.copy_files_from_other_folders(Path(config['folderpath_project'], config['folderpath_config']), Path(config['folderpath_simulator'], "SystemicRiskSimulator/data/config"), is_auto_confirmation=config['is_auto_confirmation'])
    from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

    sgv.update(config)

    ## 生成实验相关的文件夹用于本批次运作
    (
        # sgv['folderpath_project'],
        sgv['folderpath_simulator'],
        sgv['folderpath_experiments'],
        sgv['folderpath_experiments_output_data'],
        sgv['folderpath_experiments_output_log'],
        sgv['folderpath_experiments_output_config'],
        sgv['folderpath_experiments_output_parameters'],
        sgv['folderpath_experiments_output_agents'],
        sgv['folderpath_experiments_output_models'],
        sgv['folderpath_models'],
        sgv['folderpath_config'],
        sgv['folderpath_parameters'],
        sgv['folderpath_agents'],
    ) = Tools.set_experiments_folders(
        folderpath_project=sgv['folderpath_project'],
        foldername_experiments_output_data=sgv['foldername_experiments_output_data'],
        foldername_experiments=sgv['foldername_experiments'],
        str_folderpath_root_experiments=sgv['folderpath_root_experiments'],
        str_foldername_simulator=config['foldername_simulator'],
        str_folderpath_realpath_simulator=config['folderpath_realpath_simulator'],
        str_foldername_outputData=sgv['foldername_outputData'],
        str_folderpath_realpath_outputData=sgv['folderpath_realpath_outputData'],
        str_folderpath_models=sgv['folderpath_models'],
        str_folderpath_config=sgv['folderpath_config'],
        str_folderpath_parameters=sgv['folderpath_parameters'],
        str_folderpath_agents=sgv['folderpath_agents'],
    )

    Tools.copy_files_from_other_folders(sgv['folderpath_config'], sgv['folderpath_experiments_output_config'], is_auto_confirmation=sgv['is_auto_confirmation'])  # 导出一份到输出文件夹

    Tools.copy_files_from_other_folders(sgv['folderpath_agents'], Path(sgv['folderpath_simulator'], "SystemicRiskSimulator/data/agents"), is_auto_confirmation=sgv['is_auto_confirmation'])

    # 导入 agents 之参数
    df_agents_BB = pd.DataFrame(columns=['id_agents_para', 'yearName', 'networkDensity', 'agentsData'])
    df_agents_IB = pd.DataFrame(columns=['id_agents_para', 'yearName', 'networkDensity', 'agentsData'])
    id_agents_para = 0
    for year in list_agents_yearName:
        for density in list_agents_networkDensity:
            with open(Path(sgv['folderpath_agents'], 'agents', f"BB_year={year}_density={density:.2f}.pkl"), 'rb') as f:
                data = pickle.load(f)
                new_row = pd.DataFrame({'id_agents_para': id_agents_para, 'yearName': year, 'networkDensity': density, 'agentsData': [data]})
                df_agents_BB = pd.concat([df_agents_BB, new_row], ignore_index=True)
            with open(Path(sgv['folderpath_agents'], 'agents', f"IB_year={year}_density={density:.2f}.pkl"), 'rb') as f:
                data = pickle.load(f)
                new_row = pd.DataFrame({'id_agents_para': id_agents_para, 'yearName': year, 'networkDensity': density, 'agentsData': [data]})
                df_agents_IB = pd.concat([df_agents_IB, new_row], ignore_index=True)
            id_agents_para += 1
            pass  # for density
        pass  # for year

    # %%
    time_参数子组合 = time.time()  # #DEBUG

    num_bank = dict()  # 银行个数
    for year in list_agents_yearName:
        # num_bank_in_years[year] = dict_years_bankInterbank[year]['id_agent'].shape[0]
        num_bank[year] = df_agents_IB[(df_agents_IB['yearName'] == year) & (df_agents_IB['networkDensity'] == list_agents_networkDensity[0])]['agentsData'].values[0]['id_agent'].shape[0]

    # %% [markdown]
    # ## 设置参数变量

    # %%
    ## 设置模型名称
    list_combinations_model_name = list_model_name

    ## 设置年份组合
    list_combinations_yearName = list_agents_yearName

    ## 设置网络密度组合
    list_combinations_networkDensity = list_agents_networkDensity

    # 计算 agents 之组合个数
    num_agents_and_interagents = len(df_agents_BB)

    # %% [markdown]
    ### #NOTE 设置外生违约损失冲击权重百分比
    logging.debug("设置外生违约损失冲击权重百分比")
    dict_list_combinations_Shock_exIB_def_t_percentage_in_agents_items = dict()
    for idx_item in range(num_agents_and_interagents):

        year = df_agents_BB.iloc[idx_item]['yearName']
        density = df_agents_BB.iloc[idx_item]['networkDensity']
        banksData = df_agents_BB.iloc[idx_item]['agentsData']
        interbankData = df_agents_IB.iloc[idx_item]['agentsData']

        # %%
        # ### #NOTE 方案 1：各个个体步进组合（该方案与其他方案互斥）
        # logging.debug("方案 1：各个个体步进组合")
        # step = 0.1
        # Shock_exIB_def_t_percentage = np.arange(0.0, 1.0 + step, step)
        # list_combinations_Shock_exIB_def_t_percentage_01 = list(itertools.product(Shock_exIB_def_t_percentage, repeat=num_bank[year]))  # 生成所有可能的组合

        # %%

        ### #NOTE 方案 2：各个个体对角线步进组合
        logging.debug("方案 2：各个个体对角线步进组合")
        step = 0.1
        Shock_exIB_def_t_percentage = np.arange(0.0, 1.0 + step, step)
        list_combinations_Shock_exIB_def_t_percentage_02 = []  # 创建一个空列表来存储满足条件的组合
        # 对于每个可能的非零值，生成一个新的组合，其中该非零值在每个可能的位置上
        for value in Shock_exIB_def_t_percentage:
            if value != 0:  # 我们已经添加了所有元素都为零的组合
                for position in range(num_bank[year]):
                    combination = [0.0] * num_bank[year]
                    combination[position] = value
                    list_combinations_Shock_exIB_def_t_percentage_02.append(tuple(combination))

        # %%
        ### #NOTE 方案 3：所有个体步进组合
        logging.debug("方案 3：所有个体步进组合")
        step = 0.1
        Shock_exIB_def_t_percentage = np.arange(0.0, 1.0 + step, step)
        list_combinations_Shock_exIB_def_t_percentage_03 = [(value,) * num_bank[year] for value in Shock_exIB_def_t_percentage]

        # %%
        ### #NOTE 方案 4：随机组合
        logging.debug("方案 4：随机组合")
        # 设置步长和范围
        step = 0.05
        Shock_exIB_def_t_percentage = np.arange(0.0, 1.0 + step, step)

        # 设置随机数种子
        random_seed = 41
        random.seed(random_seed)

        # 设置组合的数量和大小
        num_combinations_for_scheme_04 = 5
        combination_size = num_bank[year]

        # 生成随机组合
        list_combinations_Shock_exIB_def_t_percentage_04 = [random.choices(Shock_exIB_def_t_percentage, k=combination_size) for _ in range(num_combinations_for_scheme_04)]

        # 这些随机组合中，有些组合可能是重复的，我们需要去重
        list_combinations_Shock_exIB_def_t_percentage_04 = list(set(tuple(combination) for combination in list_combinations_Shock_exIB_def_t_percentage_04))

        # 这些随机组合中，排除前面的方案中的组合
        # list_combinations_Shock_exIB_def_t_percentage_04 = [x for x in list_combinations_Shock_exIB_def_t_percentage_04 if x not in list_combinations_Shock_exIB_def_t_percentage_01]
        list_combinations_Shock_exIB_def_t_percentage_04 = [x for x in list_combinations_Shock_exIB_def_t_percentage_04 if x not in list_combinations_Shock_exIB_def_t_percentage_02]
        list_combinations_Shock_exIB_def_t_percentage_04 = [x for x in list_combinations_Shock_exIB_def_t_percentage_04 if x not in list_combinations_Shock_exIB_def_t_percentage_03]

        # %%
        ### #NOTE 方案 5：自定义组合
        logging.debug("方案 5：自定义组合")

        list_combinations_Shock_exIB_def_t_percentage_05 = [
            [1.0, 0.0, 0.0, 1.0, 0.0],
            [1.0, 0.5, 0.5, 1.0, 0.5],
        ]

        # %%
        ### 综合上述各个方案之组合
        list_combinations_Shock_exIB_def_t_percentage = []
        # list_combinations_Shock_exIB_def_t_percentage.extend(list_combinations_Shock_exIB_def_t_percentage_01)
        list_combinations_Shock_exIB_def_t_percentage.extend(list_combinations_Shock_exIB_def_t_percentage_02)
        list_combinations_Shock_exIB_def_t_percentage.extend(list_combinations_Shock_exIB_def_t_percentage_03)
        list_combinations_Shock_exIB_def_t_percentage.extend(list_combinations_Shock_exIB_def_t_percentage_04)
        list_combinations_Shock_exIB_def_t_percentage.extend(list_combinations_Shock_exIB_def_t_percentage_05)

        dict_list_combinations_Shock_exIB_def_t_percentage_in_agents_items[idx_item] = list_combinations_Shock_exIB_def_t_percentage
        pass  # for

    # %% [markdown]
    # ### 设置其它变量

    print(f"计算策略子组合耗时: {time.time() - time_参数子组合:.2f} 秒。")  # #DEBUG

    # %% [markdown]
    # 对于每一年，组合上述组合为一个实验组数据框。

    ## 先估算组合之后的总数，暂停提示是否继续进行
    list_num_total_combinations_in_a_item = []
    for idx_item in range(num_agents_and_interagents):
        list_num_total_combinations_in_a_item.append(
            len(
                list(
                    itertools.product(
                        dict_list_combinations_Shock_exIB_def_t_percentage_in_agents_items[idx_item],
                    )
                )
            )
        )
        pass  # for
    num_total_combinations = sum(list_num_total_combinations_in_a_item)

    try:
        print(f"估算总的组合数为: {num_total_combinations}")
        proceed = input("是否继续生成组合? (按下 Enter 键默认表示 'yes' 继续运行，输入其他表示 'no' 取消): ")
        if proceed.lower() not in ['', 'yes']:
            print("用户已经取消继续运行程序。")
            sys.exit()
        else:
            print("程序继续运行中。如果想要临时中断程序，请键入 Ctrl + C 中断。")

            ## 继续生成组合
            print("正在生成参数组合……")

            time_参数总组合 = time.time()  # #DEBUG

            # %% #NOTE 普通版本的生成参数组合
            list_agents_params = df_agents_BB[['id_agents_para', 'yearName', 'networkDensity']].values.tolist()

            df_parameters = pd.DataFrame(columns=[  # #NOTE 以下位置填入你的列名
                'id_agentsPara',
                'year',
                'density',
                'inner_id',
                'Shock_exIB_def_t_percentage',
            ])

            for agentPara in list_agents_params:
                id_agents_para = agentPara[0]
                year = agentPara[1]
                density = agentPara[2]
                combinations_for_each_agentsParam = list(
                    itertools.product(
                        dict_list_combinations_Shock_exIB_def_t_percentage_in_agents_items[id_agents_para],
                    )
                )

                df_parameters_for_each_agentsPara = pd.DataFrame()
                df_parameters_for_each_agentsPara['id_agentsPara'] = [id_agents_para] * len(combinations_for_each_agentsParam)
                df_parameters_for_each_agentsPara['year'] = [year] * len(combinations_for_each_agentsParam)
                df_parameters_for_each_agentsPara['density'] = [density] * len(combinations_for_each_agentsParam)
                df_parameters_for_each_agentsPara['inner_id'] = list(range(len(combinations_for_each_agentsParam)))
                df_parameters_for_each_agentsPara['Shock_exIB_def_t_percentage'] = [x[0] for x in combinations_for_each_agentsParam]

                df_parameters = pd.concat([df_parameters, df_parameters_for_each_agentsPara], ignore_index=True)
                pass  # for

            df_parameters['exp_id'] = np.arange(1, len(df_parameters) + 1)  # 在最后添加 exp_id 列
            df_parameters = df_parameters[['exp_id'] + [col for col in df_parameters.columns if col != 'exp_id']]  # exp_id 移到第一列

            # %% #NOTE 使用 dask 实现的高性能版本的生成参数组合
            # list_agents_params = df_agents_BB[['id_agents_para', 'yearName', 'networkDensity']].values.tolist()
            #
            # df_parameters = _generate_all_parameter_combinations(  # #NOTE 以下位置填入你的组合
            #     list_agents_params,
            #     dict_list_combinations_Shock_exIB_def_t_percentage_in_agents_items,
            #     dict_list_combinations_Strategy_default_in_agents_items
            # )

            pass  # if

            print(f"计算总组合耗时: {time.time() - time_参数总组合:.2f} 秒。")

            # %% [markdown]
            # 后处理，导出数据。清理无用的文件。

            # %% 保存参数组合为文件

            time_保存参数组合 = time.time()

            print("正在保存参数组合为数据框形式的 pkl 格式文件……")
            save_pkl = save_parameter_combinations(df_parameters, "./parameters.pkl")

            # 等待所有保存操作完成
            dd.compute(save_pkl)

            if is_save_to_csv:
                print("正在保存参数组合为 csv 格式文件……")
                save_csv = df_parameters.to_csv("./parameters.csv", index=False)
            if is_save_to_excel:
                print("正在保存参数组合为 xlsx 格式文件……")
                save_xlsx = df_parameters.to_excel("./parameters.xlsx", index=False)

            if is_save_to_sqlite:
                print("正在保存参数组合为 SQLite 之 db 格式文件……")
                # 保存为 SQLite 数据库
                import sqlite3
                import json

                # 创建一个 SQLite 数据库连接
                conn = sqlite3.connect('parameters.db')

                # 创建一个游标对象
                cur = conn.cursor()

                # 创建一个新表
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS parameters (
                        exp_id INTEGER,
                        year TEXT,
                        inner_id INTEGER,
                        Shock_exIB_def_t_percentage TEXT,
                    )
                ''')

                # 将数据添加到表中
                for index, row in df_parameters.iterrows():
                    # 将复杂的数据类型序列化为字符串
                    Shock_exIB_def_t_percentage_str = json.dumps(list(row['Shock_exIB_def_t_percentage']))

                    # 插入数据  #NOTE 以下位置填入你的组合、列名
                    cur.execute('''
                        INSERT INTO parameters (exp_id, year, inner_id, Shock_exIB_def_t_percentage)
                        VALUES (?, ?, ?, ?)
                    ''', (row['exp_id'], row['year'], row['inner_id'], Shock_exIB_def_t_percentage_str))

                # 提交事务
                conn.commit()

                # 关闭数据库连接
                conn.close()
                pass  # if

            print(f"保存参数组合耗时：{time.time() - time_保存参数组合:.2f} 秒。")  # #DEBUG

            # 打印参数组合数量
            print(f"参数组合数量：{len(df_parameters)}。")

            print("程序正常运行完毕！")
            pass  # if

    except KeyboardInterrupt:
        print("\n程序被用户中断。")
        sys.exit()
        pass  # try

    # %% [markdown] 打开 db 文件查看数据

    # ## 打开 db 文件查看数据 #DEBUG
    # conn = sqlite3.connect('parameters.db')
    # cur = conn.cursor()
    # cur.execute('SELECT * FROM parameters')

    # %% 打开生成的 pkl 文件查看数据 #DEBUG
    # df_parameters_new = pd.read_pickle("./parameters.pkl")

    pass  # main
