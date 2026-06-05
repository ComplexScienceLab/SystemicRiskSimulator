"""
@File   ：data_tools.py
@Desc   : 一些常用的数据处理工具
"""

import numpy as np
import pandas as pd
import logging


def check_risk_exposure_matrix_constraints(A_IB: np.ndarray, A_IB_all: np.ndarray, Z_IB_all: np.ndarray, **kwargs):
    """
    检查生成的结果风险敞口矩阵与对应的行和、列和约束的差异情况

    Args:
        A_IB (np.ndarray): 风险敞口矩阵
        A_IB_all (np.ndarray): 风险敞口矩阵的行和约束数据（列向量）
        Z_IB_all (np.ndarray): 风险敞口矩阵的列和约束数据（行向量）
        **kwargs: 额外参数

    Returns:
        diff_of_A_IB_all_and_Z_IB_all (float): 行和约束、列和约束总和的差别
        diff_of_row_sum (np.ndarray): 生成的矩阵之行和与行和约束的差别
        diff_of_col_sum (np.ndarray): 生成的矩阵之列和与列和约束的差别
        diff_of_total_sum (float): 生成的矩阵值总和与总和约束的差别
        is_valid (bool): 是否有效
    """
    is_valid = True  # TODO 这个还没有开发

    # 检查 A_IB_all、Z_IB_all 差别
    diff_of_A_IB_all_and_Z_IB_all = A_IB_all.sum() / Z_IB_all.sum()  # 计算行和约束、列和约束总和的差别

    # 行和约束差别
    A_IB_sum = A_IB.sum(axis=1)
    row_conditions = (A_IB_all == 0) & (A_IB_sum == 0)
    diff_of_row_sum = np.where(row_conditions, r"零/零", np.where(A_IB_all == 0, rf"{A_IB_sum}/零", A_IB_sum / A_IB_all))

    # 列和约束差别
    Z_IB_sum = A_IB.sum(axis=0)
    col_conditions = (Z_IB_all == 0) & (Z_IB_sum == 0)
    diff_of_col_sum = np.where(col_conditions, r"零/零", np.where(Z_IB_all == 0, rf"{Z_IB_sum}/零", Z_IB_sum / Z_IB_all))

    # 总和约束差别
    A_IB_sum_1 = A_IB.sum().sum()
    A_IB_sum_0 = A_IB_all.sum()
    total_conditions = (A_IB_sum_0 == 0) & (A_IB_sum_1 == 0)
    diff_of_total_sum = np.where(total_conditions, r"零/零", np.where(A_IB_sum_0 == 0, rf"{A_IB_sum_1}/零", A_IB_sum_1 / A_IB_sum_0))

    logging.info(
        f"""
    \n
    年份: {kwargs['year']}、连接密度: {kwargs['density']}\n
    A_IB_all、Z_IB_all 总和的差别: {diff_of_A_IB_all_and_Z_IB_all}\n
    行和约束的差别: {diff_of_row_sum}\n
    列和约束的差别: {diff_of_col_sum}\n
    总和约束的差别: {diff_of_total_sum}\n
    """
    )

    return diff_of_A_IB_all_and_Z_IB_all, diff_of_row_sum, diff_of_col_sum, diff_of_total_sum, is_valid

    pass  # function


def fun_根据索引示性向量获取银行资产负债表表格相关信息(idxs_ind: np.ndarray, var_val: np.ndarray = None, df: pd.DataFrame = None) -> pd.DataFrame:
    """
    根据索引值获取银行中文简称

    Args:
        idxs_ind (np.ndarray): 索引的示性向量
        var_val (np.ndarray): 变量值
        df (pd.DataFrame, optional): 银行资产负债表表格。默认是 【df_所需银行资产负债表表格】

    Returns:
        pd.DataFrame: 返回一个 DataFrame，包含异常值的相关信息：
            - idx: 索引
            - 异常值: 变量值
            - 银行代码: 银行代码
            - 银行名称: 银行名称
            - 年份: 年份
            - 报表类型: 报表类型
    """
    idxs = np.where(idxs_ind)[0]
    var_val = var_val[idxs]
    银行代码 = df['基本：银行代码'].values[idxs]
    银行名称 = df['基本：银行中文简称'].values[idxs]
    年份 = df['基本：会计期间'].values[idxs]
    报表类型 = df['基本：报表类型编码'].values[idxs]

    print(f"银行：{df['基本：银行中文简称'].values}、会计期间{df['基本：会计期间'].values}、报表类型编码{df['基本：报表类型编码'].values}")

    return pd.DataFrame({
        'idx': idxs,
        '异常值': var_val,
        '银行代码': 银行代码,
        '银行名称': 银行名称,
        '年份': 年份,
        '报表类型': 报表类型,
    })
    pass  # function


def fun_根据资产负债表科目计算模型银行变量(list_subject: list, df_balanceSheet: pd.DataFrame, money_unit):
    """
    根据资产负债表科目计算模型银行变量

    Args:
        list_subject: list, 需要计算的科目列表
        df_balanceSheet: DataFrame, 银行资产负债数据表
        money_unit: int, 金额单位

    Returns:
        v: np.ndarray, 银行变量
    """
    df_var_val = df_balanceSheet[list_subject]
    v = df_var_val.sum(axis=1).values / money_unit
    return v
    pass  # function


def check_bank_names_in_list(bank_names: list, data_table: pd.DataFrame, name_column: str = '基本：银行中文简称') -> dict:
    """
    检查银行名称是否在数据表中

    Args:
        bank_names (list): 要检查的银行名称列表
        data_table (pd.DataFrame): 数据表
        name_column (str): 银行名称所在的列名，默认为 '基本：银行中文简称'

    Returns:
        dict: 包含检查结果的字典
            - found: 找到的银行名称列表
            - not_found: 未找到的银行名称列表
            - all_found: 是否所有银行都找到了
    """
    if name_column not in data_table.columns:
        raise ValueError(f"数据表中不存在列: {name_column}")

    available_names = set(data_table[name_column].unique())
    found = [name for name in bank_names if name in available_names]
    not_found = [name for name in bank_names if name not in available_names]

    return {
        'found': found,
        'not_found': not_found,
        'all_found': len(not_found) == 0
    }


def check_bank_id_in_list(bank_ids: list, data_table: pd.DataFrame, id_column: str = '基本：银行代码') -> dict:
    """
    检查银行ID是否在数据表中

    Args:
        bank_ids (list): 要检查的银行ID列表
        data_table (pd.DataFrame): 数据表
        id_column (str): 银行ID所在的列名，默认为 '基本：银行代码'

    Returns:
        dict: 包含检查结果的字典
            - found: 找到的银行ID列表
            - not_found: 未找到的银行ID列表
            - all_found: 是否所有银行ID都找到了
    """
    if id_column not in data_table.columns:
        raise ValueError(f"数据表中不存在列: {id_column}")

    available_ids = set(data_table[id_column].unique())
    found = [bank_id for bank_id in bank_ids if bank_id in available_ids]
    not_found = [bank_id for bank_id in bank_ids if bank_id not in available_ids]

    return {
        'found': found,
        'not_found': not_found,
        'all_found': len(not_found) == 0
    }


def fun_根据对接的科目检测处理异常值(
        method_处理异常值: str,
        var_name: str,
        list_subject: list,
        df_balanceSheet: pd.DataFrame,
        dict_异常值: dict,
        money_unit,
        year,
        density,
        list_agents_networkDensity
):
    """
    根据对接的科目检测、处理异常值。

    Args:
        method_处理异常值: str, 处理异常值的方法。可选项包括：

          - '剔除'
          - '设置为零'

        list_subject: list, 需要计算的科目列表
        df_balanceSheet: DataFrame, 银行资产负债数据表
        dict_异常值: dict, 异常值字典
        money_unit: int, 金额单位
        year: int, 年份
        density: float, 网络连接密度
        list_agents_networkDensity: list, 网络连接密度列表

    Returns:
        v: np.ndarray, 银行变量
    """

    ## 检测、处理异常值
    list_相关的基本信息 = [
        '基本：银行代码',
        '基本：银行中文简称',
    ]

    df_v = df_balanceSheet[list_相关的基本信息 + list_subject]

    # 找到【df_v】 当中所有科目列都是缺失值的或者加总为 0 或者很小的银行的所有行
    df_v_异常值 = df_v[
        df_v[list_subject].isnull().all(axis=1)
        | (df_v[list_subject].sum(axis=1) < 1 / money_unit)
        ]

    # 处理 A_IB_all 涉及到的科目当中，列全部是 NaN 值或者加总为 0 或者很小的银行
    if len(df_v_异常值) > 0:
        df_v_历年_合并期末_全部缺失值 = df_v[df_v[list_subject].isnull().all(axis=1)]
        list_异常值银行代码 = df_v_异常值['基本：银行代码'].unique().tolist()
        list_异常值银行名称 = df_v['基本：银行中文简称'][df_v[list_subject].isnull().all(axis=1)].unique()
        logging.warning(f"年份 {year} 的变量 {var_name} 中，以下银行的在异常值：{list_异常值银行名称}")
        list_index = df_balanceSheet.index[df_balanceSheet['基本：银行代码'].isin(list_异常值银行代码)]
        if len(list_index) != len(list_异常值银行代码):
            raise ValueError(f"年份 {year} 的变量 {var_name} 中，剔除异常值后，银行数量不一致！")
        if method_处理异常值 == '剔除':
            # #NOTE 方案一：剔除 A_IB_all 或 Z_IB_all 中的异常值对应的银行，继续分析
            list_某一年份所需银行代码 = list(set(df_balanceSheet['基本：银行代码'].unique()) - set(list_异常值银行代码))  # 更新 list_某一年份所需银行代码
            df_balanceSheet = df_balanceSheet[df_balanceSheet['基本：银行代码'].isin(list_某一年份所需银行代码)]  # 更新 df_某一年份所需银行资产负债数据表_剔除NaN
            logging.warning(f"年份 {year} 的变量 {var_name} 中，剔除异常值后，剩余可用的银行数量：{len(list_某一年份所需银行代码)}")
        elif method_处理异常值 == '设置为零':
            # NOTE 方案二：不剔除 A_IB_all 或 Z_IB_all 中的异常值对应的银行，但是异常值设置为 0 ，调整指定的密度值。
            list_某一年份所需银行代码 = df_balanceSheet['基本：银行代码'].unique()  # 更新 list_某一年份所需银行代码
            df_balanceSheet.loc[df_balanceSheet['基本：银行代码'].isin(list_异常值银行代码), list_subject] = 0
        else:
            raise ValueError(f"未知的处理异常值的方法：{method_处理异常值}！")
    else:
        list_某一年份所需银行代码 = df_balanceSheet['基本：银行代码'].unique().tolist()
        pass  # if

    dict_异常值[var_name] = df_v_异常值

    return df_balanceSheet, list_某一年份所需银行代码, dict_异常值

    pass  # function
