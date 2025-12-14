# %% [markdown]
# # 程序：设置参数变量数据记录 parameter_variables
#

# %% [markdown]
# > 注意：可能由于参数组合过多，导致生成的参数组合过多，从而导致内存溢出。或者运行时长过长。因此，需要根据实际情况来设置参数组合，并在运行之前自行估算参数组合数量。
#


# %% [markdown]
# ## 导入相关库

# %%
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import re
import pickle
import itertools
import time
from functools import reduce
import random
import logging
from SystemicRiskSimulator.tools.tools import Tools

# from dask.delayed import delayed
# import dask.dataframe as dd

pass  # end import


# %% [markdown]  使用 dask 实现的高性能版本的生成参数组合之函数

def _generate_all_parameter_combinations(list_agents_params, dict_list_combinations_Shock_exIB_def_t_percentage_in_agentsItems, dict_list_combinations_Strategy_default_in_agentsItems):
    inner_id = 0

    # @delayed
    def _generate_parameter_combinations(inner_id, id_agents, year, density_IB):
        combinations_for_each_agentsParam = list(
            itertools.product(
                dict_list_combinations_Shock_exIB_def_t_percentage_in_agentsItems[id_agents],
                dict_list_combinations_Strategy_default_in_agentsItems[id_agents]
            )
        )

        df_parameters_for_each_agentsPara = pd.DataFrame(
            columns=[  # #NOTE 以下位置填入你的列名
                'id_agents',
                'year',
                'density_IB',
                'inner_id',
                'Shock_exIB_def_t_percentage',
                'Strategy_default',
            ]
        )

        df_parameters_for_each_agentsPara['id_agents'] = [id_agents] * len(combinations_for_each_agentsParam)
        df_parameters_for_each_agentsPara['year'] = [year] * len(combinations_for_each_agentsParam)
        df_parameters_for_each_agentsPara['density_IB'] = [density_IB] * len(combinations_for_each_agentsParam)
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


# @delayed
# def _generate_strategy_combinations(idx_item, year, num_bank, dict_mat_deb, dict_num_bank_cre, dict_is_bank_deb):
#     print("方案 3：均匀分布随机违约")
#     num_random_choise = 1000
#     step_幂 = 2
#     single_bank_strategy_default = np.array([0, step_幂 ** 0, step_幂 ** 1, step_幂 ** 2, step_幂 ** 3, step_幂 ** 4])  # 生成单个银行之违约策略步长数组
#
#     num_random_choise_one_bank = num_random_choise // num_bank
#     list_combinations_single_bank_Strategy_default = []
#     for i, bank_deb in enumerate(dict_mat_deb[idx_item]):
#         if bank_deb.any():  # 如果该银行有债权银行,那么就继续,否则策略为空
#             generated_combinations = set()
#             # 生成随机的若干次次组合 #HACK 这个版本是生成要求数量的随机的可重复的组合。
#             list_combinations_single_bank_Strategy_default = random.choices(list(itertools.product(single_bank_strategy_default, repeat=dict_num_bank_cre[idx_item][i])), k=num_random_choise_one_bank)
#
#             # 生成随机的若干次次组合 #HACK 这个版本是生成要求数量的随机的不重复的组合。#BUG 缺陷是如果总的组合数少于要求生成的组合数，那么就会陷入死循环。
#             # for _ in range(num_random_choise_one_bank):
#             #     while True:
#             #         combination = tuple(np.random.choice(single_bank_strategy_default, dict_num_bank_cre[idx_item][i]))
#             #         str_combination = str(combination)
#             #         if str_combination not in generated_combinations:
#             #             generated_combinations.add(str_combination)
#             #             list_combinations_single_bank_Strategy_default.append(combination)
#             #             break
#             list_combinations_single_bank_Strategy_default = [np.array(x) for x in list_combinations_single_bank_Strategy_default]
#             for j, combination in enumerate(list_combinations_single_bank_Strategy_default):
#                 non_zero_elements = combination[combination > 0]
#                 if non_zero_elements.size != 0:
#                     gcd = reduce(np.gcd, non_zero_elements)
#                     list_combinations_single_bank_Strategy_default[j] //= gcd
#             list_combinations_single_bank_Strategy_default = [x for i, x in enumerate(list_combinations_single_bank_Strategy_default) if not any(np.array_equal(x, list_combinations_single_bank_Strategy_default[j]) for j in range(i))]
#             list_combinations_single_bank_Strategy_default = [x for x in list_combinations_single_bank_Strategy_default if np.count_nonzero(x) != 0]
#             list_combinations_single_bank_Strategy_default = [x / np.sum(x) for x in list_combinations_single_bank_Strategy_default]
#             for j, combination in enumerate(list_combinations_single_bank_Strategy_default):
#                 new_combination = np.zeros(num_bank)
#                 new_combination[bank_deb] = combination
#                 list_combinations_single_bank_Strategy_default[j] = new_combination
#         else:
#             list_combinations_single_bank_Strategy_default = np.zeros(num_bank)
#         list_combinations_banks_Strategy_default_03.append(list_combinations_single_bank_Strategy_default)
#     return list_combinations_banks_Strategy_default_03
#     pass  # function


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


def insert_combinations_to_indices(total_agents, combinations, idxs_combinations_agents):
    """
    将生成的组合插入到原来的所有个体索引中。

    如果所有个体的数量大于当前要处理的个体数量（即有些个体未被纳入当前参数组合），则需要把已生成的参数组合“嵌入”到所有个体的索引结构中。

    具体做法是：调用该函数，把当前的参数组合（只针对部分个体）插入到所有个体的索引位置，未涉及的个体位置补零。

    Args:
        total_agents (int): 所有个体个数
        combinations (list): 外生违约损失冲击权重百分比组合
        idxs_combinations_agents (np.ndarray): 个体集的索引组合

    Returns:
        list: 插入后的组合
    """
    combinations = np.array(combinations)
    agents_values = np.zeros((combinations.shape[0], total_agents), dtype=type(combinations.dtype))
    agents_values[:, idxs_combinations_agents] = combinations
    agents_values = agents_values.tolist()
    return agents_values


if __name__ == '__main__':

    # %% [markdown]
    # ## #NOTE 配置项
    # %%
    config = dict()

    # #NOTE 配置 agents 文件夹名称
    config['foldername_agents'] = "agents_sample_IB2111"

    # list_model_name = ['IB1111']  # 模型名称列表 #HACK 这个用不到
    # config['list_agents_yearName'] = ['2008', '2012']  # 年份名称列表  #DEBUG 仅调试用
    config['list_agents_yearName'] = ['2012']  # 年份名称列表  #DEBUG 仅调试用
    # config['list_agents_networkDensity_IB'] = [0.5, 1.0]  # 网络密度列表  #DEBUG 仅调试用
    config['list_agents_networkDensity_IB'] = [1.0]  # 网络密度列表  #DEBUG 仅调试用

    # 要处理的个体列表

    # 外生违约损失冲击权重百分比方案列表
    config['外生违约损失冲击权重百分比方案'] = [
        # '01',
        '02',
        '03',
        '04'
        # '05'
    ]

    # 银行间违约策略方案列表
    config['银行间违约策略方案'] = [
        '01',
        # '02',
        # '03',
        # '04',
    ]
    # 奖励函数
    config['list_alpha_reward'] = list(np.arange(0, 1, 0.1))
    # 是否保存为 SQLite 数据库文件、CSV 文件、Excel 文件
    config['is_save_to_pkl'] = True  # 这个是一般情况下，常用的
    config['is_save_to_excel'] = True  # 这个是生成后便于直接预览的
    config['is_save_to_sqlite'] = False  # 如果数据量过大，可以考虑这个
    config['is_save_to_csv'] = False  # 这个比较少用

    # 配置 logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # %%

    # 预设策略集合 #HACK 这个用不到
    preset_policy_style = [
        'Strategy_RL_PPO',
        'Strategy_等级完全相同',
        'Strategy_均匀分布随机',
        'Strategy_presetImported',
    ]

    # %%
    # 获取项目路径、模拟器工具路径
    config['folderpath_project'] = Tools.get_project_rootpath()

    sgv = dict()
    sgv.update(config)
    sgv['folderpath_agents'] = Path(sgv['folderpath_project'] / "libraries/agents_library" / sgv['foldername_agents'])  # agents 文件夹路径

    # 导入 agents 之参数
    df_agents_BB = pd.DataFrame(columns=['id_agents', 'yearName', 'networkDensity_IB', 'agentsData'])
    df_agents_IB = pd.DataFrame(columns=['id_agents', 'yearName', 'networkDensity_IB', 'agentsData'])
    df_agents_note = pd.DataFrame(columns=['id_agents', 'yearName', 'networkDensity_IB', 'agentsData'])

    # 根据 agents 文件名获取各相关变量的列表
    filenames_agents = sorted(sgv['folderpath_agents'].glob('agents/*.pkl'))
    list_agents_para = []
    # 读取 agents 文件名，提取其中的年份和密度。
    for filename in filenames_agents:
        match = re.search(r'id=(\d*?)-v=(.*?)-year=(\d{4})-density_IB=(\d+\.\d+)', str(filename))
        if match:
            id_agents = int(match.group(1))
            v = match.group(2)
            yearName = match.group(3)
            networkDensity_IB = float(match.group(4))
            list_agents_para.append((id_agents, v, yearName, networkDensity_IB))

    # 批量读取不同年份和网络密度下的 agents 数据文件（pkl 格式），并将其内容加载到对应的 DataFrame 中，以便后续参数组合和实验设计使用
    for (id_agents, v, yearName, networkDensity_IB) in list_agents_para:
        with open(Path(sgv['folderpath_agents'], 'agents', f"id={id_agents}-v={v}-year={yearName}-density_IB={networkDensity_IB:.2f}.pkl"), 'rb') as f:
            agentsData = pickle.load(f)
            new_row = pd.DataFrame({'id_agents': id_agents, 'yearName': yearName, 'networkDensity_IB': networkDensity_IB, 'agentsData': [agentsData]})
            if not new_row.empty and not new_row.isna().all().all():
                if v == 'BB':
                    df_agents_BB = pd.concat([df_agents_BB, new_row], ignore_index=True)
                elif v == 'IB':
                    df_agents_IB = pd.concat([df_agents_IB, new_row], ignore_index=True)
                elif v == 'note':
                    df_agents_note = pd.concat([df_agents_note, new_row], ignore_index=True)
                pass  # if
            pass  # with
        pass  # for

    # 重新排序
    df_agents_BB = df_agents_BB.sort_values(by=['id_agents']).reset_index(drop=True)
    df_agents_IB = df_agents_IB.sort_values(by=['id_agents']).reset_index(drop=True)
    df_agents_note = df_agents_note.sort_values(by=['id_agents']).reset_index(drop=True)

    # 获取 id_agents、yearName 和 networkDensity_IB 集合列表
    list_id_agents = df_agents_BB.id_agents.unique().tolist()
    list_yearName = df_agents_BB.yearName.unique().tolist()
    list_networkDensity_IB = df_agents_BB.networkDensity_IB.unique().tolist()

    # %%
    time_参数子组合 = time.time()  # #DEBUG

    num_bank = dict()  # 银行个数
    num_所需银行 = dict()  # 所需银行个数
    idxs_所需银行 = dict()  # 所需银行索引位置

    for yearName in list_yearName:
        num_bank[yearName] = df_agents_note[(df_agents_note['yearName'] == yearName) & (df_agents_note['networkDensity_IB'] == sgv['list_agents_networkDensity_IB'][0])]['agentsData'].values[0]['id_bank'].shape[0]
        num_所需银行[yearName] = num_bank[yearName]
        pass  # for


    # %% [markdown]
    # ## 设置参数变量

    # %%
    # 设置模型名称
    # list_combinations_model_name = list_model_name

    # 设置年份组合
    list_combinations_yearName = sgv['list_agents_yearName']

    # 设置 IB 网络密度组合
    list_combinations_networkDensity_IB = sgv['list_agents_networkDensity_IB']

    # 计算 df_agents_BB 之组合个数（表格行数）
    num_row_agents = len(df_agents_BB)

    # %% [markdown]
    # #NOTE 设置外生违约损失冲击权重百分比
    logging.debug("设置外生违约损失冲击权重百分比")
    dict_list_combinations_Shock_exIB_def_t_percentage_in_agents_items = dict()
    dict_list_description_Shock_exIB_def_t_percentage_in_agents_items = dict()

    for idx_item in range(num_row_agents):
        id_agents = df_agents_BB.iloc[idx_item]['id_agents']
        yearName = df_agents_BB.iloc[idx_item]['yearName']
        networkDensity_IB = df_agents_BB.iloc[idx_item]['networkDensity_IB']
        agentsData_BB = df_agents_BB.iloc[idx_item]['agentsData']
        agentsData_IB = df_agents_IB.iloc[idx_item]['agentsData']

        # %%
        # #NOTE 方案 1：各个个体步进组合（该方案与其他方案互斥）
        if '01' in sgv['外生违约损失冲击权重百分比方案']:
            logging.debug("方案 1：各个个体步进组合")
            step = 1.0
            Shock_exIB_def_t_percentage = np.arange(0.0, 1.0 + step, step)
            list_combinations_Shock_exIB_def_t_percentage_01 = np.array(np.meshgrid(*[Shock_exIB_def_t_percentage] * num_所需银行[yearName])).T.reshape(-1, num_所需银行[yearName])  # 生成所有可能的组合
            list_description_Shock_exIB_def_t_percentage_01 = [f"外生违约损失冲击权重百分比之各个个体步进组合"] * len(list_combinations_Shock_exIB_def_t_percentage_01)  # 添加组合描述
            pass  # if
        
        # %%
        # #NOTE 方案 2：各个个体对角线步进组合
        if '02' in sgv['外生违约损失冲击权重百分比方案']:
            logging.debug("方案 2：各个个体对角线步进组合")
            step = 0.10
            Shock_exIB_def_t_percentage = np.arange(0.0, 1.0 + step, step)
            list_combinations_Shock_exIB_def_t_percentage_02 = []  # 创建一个空列表来存储满足条件的组合
            # 对于每个可能的非零值，生成一个新的组合，其中该非零值在每个可能的位置上
            for value in Shock_exIB_def_t_percentage:
                if value != 0:  # 我们已经添加了所有元素都为零的组合
                    for position in range(num_所需银行[yearName]):
                        combination = [0.0] * num_所需银行[yearName]
                        combination[position] = value
                        list_combinations_Shock_exIB_def_t_percentage_02.append(tuple(combination))
                        pass  # for
                    pass  # if
                pass  # for
            list_description_Shock_exIB_def_t_percentage_02 = [f"外生违约损失冲击权重百分比之各个个体对角线步进组合"] * len(list_combinations_Shock_exIB_def_t_percentage_02)  # 添加组合描述
            pass  # if

        # %%
        # #NOTE 方案 3：所有个体步进组合
        if '03' in sgv['外生违约损失冲击权重百分比方案']:
            logging.debug("方案 3：所有个体步进组合")
            step = 0.10
            Shock_exIB_def_t_percentage = np.arange(0.0, 1.0 + step, step)
            list_combinations_Shock_exIB_def_t_percentage_03 = [(value,) * num_所需银行[yearName] for value in Shock_exIB_def_t_percentage]
            list_description_Shock_exIB_def_t_percentage_03 = [f"外生违约损失冲击权重百分比之所有个体步进组合"] * len(list_combinations_Shock_exIB_def_t_percentage_03)  # 添加组合描述
            pass  # if

        # %%
        # #NOTE 方案 4：随机组合
        if '04' in sgv['外生违约损失冲击权重百分比方案']:
            logging.debug("方案 4：随机组合")
            # 设置步长和范围
            step = 0.05
            Shock_exIB_def_t_percentage = np.arange(0.0, 1.0 + step, step)

            # 设置随机数种子
            random_seed = 41
            random.seed(random_seed)

            # 设置组合的数量和大小
            num_combinations_for_scheme_04 = 3
            combination_size = num_所需银行[yearName]
            list_combinations_Shock_exIB_def_t_percentage_04 = [random.choices(Shock_exIB_def_t_percentage, k=combination_size) for _ in range(num_combinations_for_scheme_04)]  # 生成随机组合
            list_combinations_Shock_exIB_def_t_percentage_04 = list(set(tuple(combination) for combination in list_combinations_Shock_exIB_def_t_percentage_04))  # 这些随机组合中，有些组合可能是重复的，我们需要去重
            # 这些随机组合中，排除前面的方案中的组合
            for scheme in list(set(sgv['外生违约损失冲击权重百分比方案']) - {'04'}):
                var_scheme = eval(f'list_combinations_Shock_exIB_def_t_percentage_{scheme}')
                list_combinations_Shock_exIB_def_t_percentage_04 = [x for x in list_combinations_Shock_exIB_def_t_percentage_04 if x not in var_scheme]
                pass  # for
            list_description_Shock_exIB_def_t_percentage_04 = [f"外生违约损失冲击权重百分比之随机组合"] * len(list_combinations_Shock_exIB_def_t_percentage_04)  # 添加组合描述
            pass  # if

        # %%
        # NOTE 方案 5：自定义组合  #FIXME 如果不同的 id_agents 之银行数量不同，则无效
        logging.debug("方案 5：自定义组合")
        if '05' in sgv['外生违约损失冲击权重百分比方案']:
            list_combinations_Shock_exIB_def_t_percentage_05 = [
                [1.0, 0.0, 0.0, 1.0],
                [1.0, 0.5, 0.5, 1.0],
            ]
            list_description_Shock_exIB_def_t_percentage_05 = [f"外生违约损失冲击权重百分比之自定义组合"] * len(list_combinations_Shock_exIB_def_t_percentage_05)  # 添加组合描述
            pass  # if

        # %%
        # 综合上述各个方案之组合
        list_combinations_Shock_exIB_def_t_percentage = []
        list_description_Shock_exIB_def_t_percentage = []
        for scheme in sgv['外生违约损失冲击权重百分比方案']:
            list_combinations_Shock_exIB_def_t_percentage.extend(eval(f'list_combinations_Shock_exIB_def_t_percentage_{scheme}'))
            list_description_Shock_exIB_def_t_percentage.extend(eval(f'list_description_Shock_exIB_def_t_percentage_{scheme}'))
            pass  # if

        # 检查是否有重复的组合，如果有则去重
        array_combinations = np.array(list_combinations_Shock_exIB_def_t_percentage)
        _, unique_indices = np.unique(array_combinations, axis=0, return_index=True)
        if len(unique_indices) < len(list_combinations_Shock_exIB_def_t_percentage):
            logging.debug(f"年{yearName}密度{networkDensity_IB:.2f}有重复组合")
        list_combinations_Shock_exIB_def_t_percentage = array_combinations[unique_indices].tolist()
        list_description_Shock_exIB_def_t_percentage = [list_description_Shock_exIB_def_t_percentage[i] for i in unique_indices]

        # 检查是否有全0的组合，如果有则去掉
        if any(np.count_nonzero(combination) == 0 for combination in list_combinations_Shock_exIB_def_t_percentage):
            logging.debug(f"年{yearName}密度{networkDensity_IB:.2f}有全 0 组合")
            idx_all_zero_combinations = [idx for idx, combination in enumerate(list_combinations_Shock_exIB_def_t_percentage) if np.count_nonzero(combination) == 0]  # 找到全 0 组合的索引
            list_combinations_Shock_exIB_def_t_percentage = [x for i, x in enumerate(list_combinations_Shock_exIB_def_t_percentage) if i not in idx_all_zero_combinations]  # 根据索引删除全 0 组合
            list_description_Shock_exIB_def_t_percentage = [x for i, x in enumerate(list_description_Shock_exIB_def_t_percentage) if i not in idx_all_zero_combinations]
            pass  # if

        # 将生成的组合插入到原来的所有资产索引中
        if num_bank[yearName] > num_所需银行[yearName]:
            list_combinations_Shock_exIB_def_t_percentage = insert_combinations_to_indices(num_bank[yearName], list_combinations_Shock_exIB_def_t_percentage, idxs_所需银行[yearName])
            pass  # if


        dict_list_combinations_Shock_exIB_def_t_percentage_in_agents_items[idx_item] = list_combinations_Shock_exIB_def_t_percentage
        dict_list_description_Shock_exIB_def_t_percentage_in_agents_items[idx_item] = list_description_Shock_exIB_def_t_percentage

        pass  # for

    # %% [markdown]
    # ### ## #NOTE 计算银行策略组合

    # %% [markdown]
    #
    # 获取策略步长列表

    # %% [markdown]
    # #NOTE 设置银行策略组合
    logging.debug("设置银行间违约策略组合")
    dict_mat_deb = dict()  # 债务掩码矩阵字典。每一个键名对应 df_agents_BB 之索引，键值对应一个债务掩码矩阵
    dict_num_bank_cre = dict()  # 每一个债务银行之债权银行数量
    dict_is_bank_deb = dict()  # 每一个银行是否是债务银行
    dict_list_combinations_Strategy_default_in_agents_items = dict()  # 存储每一个 agents 数据项之策略组合
    dict_list_description_Strategy_default_in_agents_items = dict()  # 存储每一个 agents 数据项之策略组合描述

    for idx_item in range(num_row_agents):
        id_agents = df_agents_BB.iloc[idx_item]['id_agents']
        yearName = df_agents_BB.iloc[idx_item]['yearName']
        networkDensity_IB = df_agents_BB.iloc[idx_item]['networkDensity_IB']
        agentsData_BB = df_agents_BB.iloc[idx_item]['agentsData']
        agentsData_IB = df_agents_IB.iloc[idx_item]['agentsData']

        dict_mat_deb[idx_item] = df_agents_IB.iloc[idx_item]['agentsData']['Z_IB'] > 0  # 计算每一个银行之债务掩码矩阵
        dict_num_bank_cre[idx_item] = np.sum(dict_mat_deb[idx_item], axis=1)  # 计算每一个银行之债权银行数量
        dict_is_bank_deb[idx_item] = dict_num_bank_cre[idx_item] > 0  # 计算历年之每一个银行是否是债务银行

        # %%
        # #NOTE 方案 1：各个个体步进组合（该方案与其他方案互斥）
        if '01' in sgv['银行间违约策略方案']:
            logging.debug("方案 1：各个个体步进组合")
            step_幂 = 2
            # single_bank_strategy_default = np.array([0, step_幂 ** 0])  # 生成单个银行之违约策略步长数组。 #HACK 如果启用这个，那么组合数一下子会爆炸！
            single_bank_strategy_default = np.array([step_幂 ** 0])  # 生成单个银行之违约策略步长数组。 #HACK 当使用这个设定的时候，相当于分配给所有个体之违约比例都一样。注意，这个并不等于分配等级相同策略！
            list_combinations_banks_Strategy_default_01 = []
            list_description_banks_Strategy_default_01 = []
            list_combinations_banks_Strategy_default_01_01 = []
            for i, bank_deb in enumerate(dict_mat_deb[idx_item]):
                if bank_deb.any():
                    list_combinations_single_bank_Strategy_default = list(itertools.product(single_bank_strategy_default, repeat=dict_num_bank_cre[idx_item][i]))
                    list_combinations_single_bank_Strategy_default = [np.array(combination) for combination in list_combinations_single_bank_Strategy_default]
                    for j, combination in enumerate(list_combinations_single_bank_Strategy_default):
                        non_zero_elements = combination[combination > 0]
                        if non_zero_elements.size != 0:
                            gcd = reduce(np.gcd, non_zero_elements)
                            list_combinations_single_bank_Strategy_default[j] //= gcd
                    list_combinations_single_bank_Strategy_default = [x for i, x in enumerate(list_combinations_single_bank_Strategy_default) if not any(np.array_equal(x, list_combinations_single_bank_Strategy_default[j]) for j in range(i))]
                    list_combinations_single_bank_Strategy_default = [x for x in list_combinations_single_bank_Strategy_default if np.count_nonzero(x) != 0]
                    list_combinations_single_bank_Strategy_default = [x / np.sum(x) for x in list_combinations_single_bank_Strategy_default]
                    for j, combination in enumerate(list_combinations_single_bank_Strategy_default):
                        new_combination = np.zeros(num_所需银行[yearName])
                        new_combination[bank_deb] = combination
                        list_combinations_single_bank_Strategy_default[j] = new_combination
                else:
                    list_combinations_single_bank_Strategy_default = [[0] * num_所需银行[yearName]]
                list_combinations_banks_Strategy_default_01_01.append(list_combinations_single_bank_Strategy_default)
            list_combinations_banks_Strategy_default_01 = list(itertools.product(*list_combinations_banks_Strategy_default_01_01))
            # list_combinations_banks_Strategy_default_01 = [np.array(combination) for combination in list_combinations_banks_Strategy_default_01]
            list_description_banks_Strategy_default_01 = [f"银行间违约策略之各个个体步进组合"] * len(list_combinations_banks_Strategy_default_01)  # 添加组合描述
            pass  # if

        # %%
        # #NOTE 方案 2：优先顺序违约 #HACK #TODO 这个只能用标记在参数，然后在模型中实现该策略。目前还未实现标记参数功能。
        if '02' in sgv['银行间违约策略方案']:
            logging.debug("方案 2：优先顺序违约")
            list_combinations_banks_Strategy_default_02 = []
            # for idx_item in range(num_row_agents):
            #     year = df_agents_BB.iloc[idx_item]['yearName']
            #     density_IB = df_agents_BB.iloc[idx_item]['networkDensity_IB']
            #     banksData = df_agents_BB.iloc[idx_item]['agentsData']
            #     interbankData = df_agents_IB.iloc[idx_item]['agentsData']
            #
            # for i, bank_deb in enumerate(dict_mat_deb[idx_item]):
            #     if bank_deb.any():
            #         # 计算欠的金额
            #         owed_amounts = interbankData['Z_IB'][i, bank_deb]
            #         # 排优先级，金额越小优先级越高
            #         priority_indices = np.argsort(owed_amounts)
            #         # 计算贷款金额减去流动资金之后的金额
            #         remaining_amounts = owed_amounts - banksData['liquidity'][i]
            #         remaining_amounts[remaining_amounts < 0] = 0  # 确保没有负值
            #         # 按照优先级依次计算违约值
            #         default_values = np.zeros_like(owed_amounts)
            #         for idx in priority_indices:
            #             if remaining_amounts[idx] > 0:
            #                 default_values[idx] = remaining_amounts[idx]
            #                 remaining_amounts[idx] = 0
            #         # 计算违约比例
            #         default_ratios = default_values / owed_amounts
            #         default_ratios[np.isnan(default_ratios)] = 0  # 处理除以零的情况
            #         new_combination = np.zeros(num_所需银行[year])
            #         new_combination[bank_deb] = default_ratios
            #         list_combinations_banks_Strategy_default_02.append(new_combination)
            #     else:
            #         list_combinations_banks_Strategy_default_02.append(np.zeros(num_所需银行[year]))
            list_description_banks_Strategy_default_02 = [f"银行间违约策略之优先顺序违约"] * len(list_combinations_banks_Strategy_default_02)  # 添加组合描述
            pass  # if

        # %%
        # #NOTE 方案 3：均匀分布随机违约
        if '03' in sgv['银行间违约策略方案']:
            logging.debug("方案 3：均匀分布随机违约")
            num_random_choise = 1
            step_幂 = 2
            single_bank_strategy_default = np.array([0, step_幂 ** 0, step_幂 ** 1, step_幂 ** 2, step_幂 ** 3, step_幂 ** 4])
            list_combinations_banks_Strategy_default_03 = []
            for idx_choise in range(num_random_choise):
                arr_combinations_banks_Strategy_default = np.zeros((num_所需银行[yearName], num_所需银行[yearName]))
                for i, bank_deb in enumerate(dict_mat_deb[idx_item]):
                    if bank_deb.any():
                        while True:
                            combination_single_bank_Strategy_default = random.choices(single_bank_strategy_default, k=dict_num_bank_cre[idx_item][i])
                            if np.count_nonzero(combination_single_bank_Strategy_default) != 0:
                                break
                        combination_single_bank_Strategy_default = np.asarray(combination_single_bank_Strategy_default)
                        non_zero_elements = combination_single_bank_Strategy_default[combination_single_bank_Strategy_default > 0]
                        if non_zero_elements.size != 0:
                            gcd = reduce(np.gcd, non_zero_elements)
                            combination_single_bank_Strategy_default //= gcd
                        combination_single_bank_Strategy_default = combination_single_bank_Strategy_default / np.sum(combination_single_bank_Strategy_default)
                        new_combination = np.zeros(num_所需银行[yearName])
                        new_combination[bank_deb] = combination_single_bank_Strategy_default
                        combination_single_bank_Strategy_default = new_combination
                    else:
                        combination_single_bank_Strategy_default = np.zeros(num_所需银行[yearName])
                    arr_combinations_banks_Strategy_default[i] = combination_single_bank_Strategy_default
                list_combinations_banks_Strategy_default_03.append(arr_combinations_banks_Strategy_default)
                pass  # for
            list_description_banks_Strategy_default_03 = [f"银行间违约策略之均匀分布随机违约"] * len(list_combinations_banks_Strategy_default_03)  # 添加组合描述
            pass  # if

        # %%
        # #NOTE 方案 4：自定义组合
        if '04' in sgv['银行间违约策略方案']:
            logging.debug("方案 4：自定义组合")
            list_combinations_banks_Strategy_default_04 = [
                # 添加自定义组合
            ]
            list_description_banks_Strategy_default_04 = [f"银行间违约策略之自定义组合"] * len(list_combinations_banks_Strategy_default_04)  # 添加组合描述
            pass  # if
        # %%
        # 综合上述各个方案之组合
        list_combinations_banks_Strategy_default = []
        list_description_banks_Strategy_default = []
        for scheme in sgv['银行间违约策略方案']:
            list_combinations_banks_Strategy_default.extend(eval(f'list_combinations_banks_Strategy_default_{scheme}'))
            list_description_banks_Strategy_default.extend(eval(f'list_description_banks_Strategy_default_{scheme}'))
            pass  # if

        dict_list_combinations_Strategy_default_in_agents_items[idx_item] = list_combinations_banks_Strategy_default
        dict_list_description_Strategy_default_in_agents_items[idx_item] = list_description_banks_Strategy_default
        pass  # for

    # ##### #NOTE 使用 dask 实现的高性能版本的 # BUG 已经未能适配 #BUG 存在缺陷无法运行起来

    # # time_参数子组合 = time.time()  # #DEBUG
    # #
    # # list_agents_params = df_agents_BB[['id_agents', 'yearName', 'networkDensity_IB']].values.tolist()
    # # tasks = [_generate_strategy_combinations(idx_item, year, num_所需银行[year], dict_mat_deb, dict_num_bank_cre, dict_is_bank_deb) for idx_item, year in enumerate(sgv['list_agents_yearName'])]
    # # list_combinations_banks_Strategy_default_list = dd.compute(*tasks)
    # #
    # # print(f"计算策略子组合耗时: {time.time() - time_参数子组合:.2f} 秒。")  # #DEBUG
    # #
    # # dict_list_combinations_Strategy_default_in_agents_items = {idx_item: list_combinations_banks_Strategy_default_list[idx_item] for idx_item in range(num_row_agents)}

    # %% [markdown]
    # ### 设置其它变量

    # %% [markdown]
    # ### ## #NOTE 计算奖励函数参数组合。这里假设奖励函数是同质的，暨所有个体的奖励函数参数都是一样的。
    logging.debug("设置奖励函数参数组合")
    dict_list_combinations_alpha_reward_in_agents_items = dict()  # 存储每一个 agents 数据项之奖励函数参数组合
    dict_list_description_alpha_reward_in_agents_items = dict()  # 存储每一个 agents 数据项之奖励函数参数组合描述
    dict_list_description_base_alpha_reward_in_agents_items = dict()  # 存储每一个 agents 数据项之奖励函数参数组合基础描述

    for idx_item in range(num_row_agents):
        id_agents = df_agents_BB.iloc[idx_item]['id_agents']
        yearName = df_agents_BB.iloc[idx_item]['yearName']
        networkDensity_IB = df_agents_BB.iloc[idx_item]['networkDensity_IB']
        agentsData_BB = df_agents_BB.iloc[idx_item]['agentsData']
        agentsData_IB = df_agents_IB.iloc[idx_item]['agentsData']

        # %%
        # #NOTE 方案 1：各个个体之各个参数步进组合（该方案与其他方案互斥）
        if '01' in sgv['银行奖励函数参数组合方案']:
            logging.debug("方案 1：各个个体之各个参数步进组合")
            list_combinations_banks_alpha_reward_01 = []
            list_description_banks_alpha_reward_01 = []
            for alpha_reward in config['list_alpha_reward']:
                alpha_reward = round(alpha_reward, 2)
                list_combinations_banks_alpha_reward_01.append(alpha_reward)
                list_description_banks_alpha_reward_01.append(f"奖励函数参数组合")  # 添加组合描述
                pass  # for
            pass  # if

        # %%
        # 综合上述各个方案之组合
        list_combinations_banks_alpha_reward = []
        list_description_banks_alpha_reward = []

        for alpha_reward in config['list_alpha_reward']:
            alpha_reward = round(alpha_reward, 2)
            list_combinations_banks_alpha_reward.append(alpha_reward)
            list_description_banks_alpha_reward.append(f"奖励函数参数之{alpha_reward}")  # 添加组合描述
            pass  # for
        dict_list_combinations_alpha_reward_in_agents_items[idx_item] = list_combinations_banks_alpha_reward
        dict_list_description_alpha_reward_in_agents_items[idx_item] = list_description_banks_alpha_reward
        pass  # for

    # %% [markdown]

    print(f"计算子组合耗时: {time.time() - time_参数子组合:.2f} 秒。")  # #DEBUG

    # %% [markdown]
    # 对于每一年，组合上述组合为一个实验组数据框。

    # 先估算组合之后的总数，暂停提示是否继续进行
    list_num_total_combinations_in_a_item = []
    for idx_item in range(num_row_agents):
        # 获取当前项的组合列表
        combinations = [
            dict_list_combinations_Shock_exIB_def_t_percentage_in_agents_items[idx_item],
            dict_list_combinations_Strategy_default_in_agents_items[idx_item],
            dict_list_combinations_alpha_reward_in_agents_items[idx_item],
        ]
        # 过滤掉空列表
        valid_combinations = [combo for combo in combinations if combo]
        # 如果有有效组合，则计算笛卡尔积的长度
        if valid_combinations:
            list_num_total_combinations_in_a_item.append(
                len(list(itertools.product(*valid_combinations)))
            )
        else:
            list_num_total_combinations_in_a_item.append(0)  # 如果没有有效组合，添加 0
            logging.warning(f"索引 {idx_item} 没有有效的参数组合！组合数为 0。")
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

            # 继续生成组合
            print("正在生成参数组合……")

            time_参数总组合 = time.time()  # #DEBUG

            # %% #NOTE 普通版本的生成参数组合
            list_agents_params = df_agents_BB[['id_agents', 'yearName', 'networkDensity_IB']].values.tolist()

            df_parameters = pd.DataFrame(
                columns=[  # #NOTE 以下位置填入你的列名
                    'id_agents',
                    'year',
                    'density_IB',
                    'inner_id',
                    'Shock_exIB_def_t_percentage',
                    'Strategy_default',
                    'alpha_reward',
                    'description',
                ]
            )

            for i, agentPara in enumerate(list_agents_params):
                id_agents = agentPara[0]
                yearName = agentPara[1]
                networkDensity_IB = agentPara[2]

                # 获取当前项的组合列表
                combinations = [
                    dict_list_combinations_Shock_exIB_def_t_percentage_in_agents_items[id_agents],
                    dict_list_combinations_Strategy_default_in_agents_items[id_agents],
                    dict_list_combinations_alpha_reward_in_agents_items[id_agents],
                ]

                descriptions = [
                    dict_list_description_Shock_exIB_def_t_percentage_in_agents_items[id_agents],
                    dict_list_description_Strategy_default_in_agents_items[id_agents],
                    dict_list_description_alpha_reward_in_agents_items[id_agents],
                ]

                # 过滤掉空列表
                valid_combinations = [combo for combo in combinations if combo]
                valid_descriptions = [desc for desc in descriptions if desc]

                # 如果有有效组合，则计算笛卡尔积
                if valid_combinations:
                    combinations_for_each_agentsParam = list(itertools.product(*valid_combinations))
                    combinations_for_each_description = list(itertools.product(*valid_descriptions))

                    df_parameters_for_each_agentsPara = pd.DataFrame()
                    df_parameters_for_each_agentsPara['id_agents'] = [id_agents] * len(combinations_for_each_agentsParam)
                    df_parameters_for_each_agentsPara['year'] = [yearName] * len(combinations_for_each_agentsParam)
                    df_parameters_for_each_agentsPara['density_IB'] = [networkDensity_IB] * len(combinations_for_each_agentsParam)
                    df_parameters_for_each_agentsPara['inner_id'] = list(range(len(combinations_for_each_agentsParam)))
                    df_parameters_for_each_agentsPara['Shock_exIB_def_t_percentage'] = [x[0] for x in combinations_for_each_agentsParam]
                    # df_parameters_for_each_agentsPara['Strategy_default'] = [x[2] for x in combinations_for_each_agentsParam]  # #HACK 如果没有用到这个，那么需要注释掉
                    # df_parameters_for_each_agentsPara['alpha_reward'] = [x[3] for x in combinations_for_each_agentsParam]  # #HACK 如果没有用到这个，那么需要注释掉
                    df_parameters_for_each_agentsPara['description'] = [
                            f"个体集{id_agents}年份{yearName}银行间密度{networkDensity_IB}之：" + "，".join(str(xx) for xx in x) + "。" for x in combinations_for_each_description
                    ]

                    if not df_parameters_for_each_agentsPara.empty and not df_parameters_for_each_agentsPara.isna().all().all():
                        df_parameters = pd.concat([df_parameters, df_parameters_for_each_agentsPara], ignore_index=True)
                    pass  # if
                pass  # for

            df_parameters['exp_id'] = np.arange(0, len(df_parameters) + 0)  # 在最后添加 exp_id 列
            df_parameters = df_parameters[['exp_id'] + [col for col in df_parameters.columns if col != 'exp_id']]  # exp_id 移到第一列

            # # %% #NOTE 使用 dask 实现的高性能版本的生成参数组合
            # list_agents_params = df_agents_BB[['id_agents', 'yearName', 'networkDensity_IB']].values.tolist()
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

            if sgv['is_save_to_pkl']:
                print("正在保存参数组合为数据框形式的 pkl 格式文件……")
                save_pkl = save_parameter_combinations(df_parameters, "./parameters.pkl")
                # # 等待所有保存操作完成
                # dd.compute(save_pkl)

            if sgv['is_save_to_csv']:
                print("正在保存参数组合为 csv 格式文件……")
                save_csv = df_parameters.to_csv("./parameters.csv", index=False)

            if sgv['is_save_to_excel']:
                print("正在保存参数组合为 xlsx 格式文件……")
                save_xlsx = df_parameters.to_excel("./parameters.xlsx", index=False)

            if sgv['is_save_to_sqlite']:
                print("正在保存参数组合为 SQLite 之 db 格式文件……")
                # 保存为 SQLite 数据库
                import sqlite3
                import json

                # 创建一个 SQLite 数据库连接
                conn = sqlite3.connect('parameters.db')

                # 创建一个游标对象
                cur = conn.cursor()

                # 创建一个新表
                cur.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS parameters
                    (
                        exp_id
                        INTEGER,
                        year
                        TEXT,
                        inner_id
                        INTEGER,
                        Shock_exIB_def_t_percentage
                        TEXT,
                        Strategy_default
                        TEXT,
                        alpha_reward
                        TEXT,
                        description
                        TEXT,
                    )
                    '''
                )

                # 将数据添加到表中
                for index, row in df_parameters.iterrows():
                    # 将复杂的数据类型序列化为字符串
                    Shock_exIB_def_t_percentage_str = json.dumps(list(row['Shock_exIB_def_t_percentage']))
                    Strategy_default_array = np.array(row['Strategy_default'])  # 将元组转换为 NumPy 数组
                    Strategy_default_list = Strategy_default_array.tolist()  # 将 NumPy 数组转换为列表
                    Strategy_default_str = json.dumps(Strategy_default_list)  # 将列表转换为 JSON 格式的字符串
                    alpha_reward_str = json.dumps(row['alpha_reward'])  # 将 alpha_reward 列转换为字符串
                    description_str = row['description']

                    # 插入数据  #NOTE 以下位置填入你的组合、列名
                    cur.execute(
                        '''
                        INSERT INTO parameters (exp_id, year, inner_id, Shock_exIB_def_t_percentage, Strategy_default, alpha_reward, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (row['exp_id'], row['year'], row['inner_id'], Shock_exIB_def_t_percentage_str, Strategy_default_str, alpha_reward_str, description_str)
                    )
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
    # import pandas as pd
    # print("正在打开生成的 pkl 文件查看数据……")
    # df_parameters_new = pd.read_pickle("./parameters.pkl")

    pass  # main

# %%
