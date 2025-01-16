"""
@File   ：data_tools.py
@Desc   : 一些常用的数据处理工具
"""

from SystemicRiskSimulator.external_packages import np, pd, logging


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
