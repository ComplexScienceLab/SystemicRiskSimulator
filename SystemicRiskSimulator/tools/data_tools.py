"""
@File   ：data_tools.py
@Desc   : 一些常用的数据处理工具
"""

from SystemicRiskSimulator.external_packages import np


def check_risk_exposure_matrix_constraints(A_IB: np.ndarray, A_IB_all: np.ndarray, Z_IB_all: np.ndarray):
    """
    检查生成的结果风险敞口矩阵与对应的行和、列和约束的差异情况

    Args:
        A_IB (np.ndarray): 风险敞口矩阵
        A_IB_all (np.ndarray): 风险敞口矩阵的行和约束数据（列向量）
        Z_IB_all (np.ndarray): 风险敞口矩阵的列和约束数据（行向量）

    Returns:
        diff_of_A_IB_all_and_Z_IB_all (float): 行和约束、列和约束总和的差别
        diff_of_row_sum (np.ndarray): 生成的矩阵之行和与行和约束的差别
        diff_of_col_sum (np.ndarray): 生成的矩阵之列和与列和约束的差别
        diff_of_total_sum (float): 生成的矩阵值总和与总和约束的差别
    """
    # 检查 A_IB_all、Z_IB_all 差别
    diff_of_A_IB_all_and_Z_IB_all = A_IB_all.sum() / Z_IB_all.sum()  # 计算行和约束、列和约束总和的差别

    # 行和约束
    A_IB_sum = A_IB.sum(axis=1)
    row_conditions = (A_IB_all == 0) & (A_IB_sum == 0)
    diff_of_row_sum = np.where(row_conditions, r"零/零", np.where(A_IB_all == 0, rf"{A_IB_sum}/零", A_IB_sum / A_IB_all))

    # 列和约束
    Z_IB_sum = A_IB.sum(axis=0)
    col_conditions = (Z_IB_all == 0) & (Z_IB_sum == 0)
    diff_of_col_sum = np.where(col_conditions, r"零/零", np.where(Z_IB_all == 0, rf"{Z_IB_sum}/零", Z_IB_sum / Z_IB_all))

    # 总和约束
    A_IB_sum_1 = A_IB.sum().sum()
    A_IB_sum_0 = A_IB_all.sum()
    total_conditions = (A_IB_sum_0 == 0) & (A_IB_sum_1 == 0)
    diff_of_total_sum = np.where(total_conditions, r"零/零", np.where(A_IB_sum_0 == 0, rf"{A_IB_sum_1}/零", A_IB_sum_1 / A_IB_sum_0))

    return diff_of_A_IB_all_and_Z_IB_all, diff_of_row_sum, diff_of_col_sum, diff_of_total_sum

    pass  # function
