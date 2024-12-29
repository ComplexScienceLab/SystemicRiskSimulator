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
        None
    """
    # 检查 A_IB_all、Z_IB_all 差别
    diff_of_A_IB_all_and_Z_IB_all = A_IB_all.sum() / Z_IB_all.sum()  # 计算行和约束、列和约束总和的差别

    # 行和约束
    diff_of_A_IB_all_and_A_IB = A_IB.sum(axis=1) / A_IB_all  # 计算行和约束的差别

    # 列和约束
    diff_of_A_IB_all_and_Z_IB_all = A_IB.sum(axis=0) / Z_IB_all  # 计算列和约束的差别

    # 总和约束
    diff_of_all = A_IB.sum().sum() / A_IB_all.sum()  # 计算总约束的差别

    return diff_of_A_IB_all_and_Z_IB_all, diff_of_A_IB_all_and_A_IB, diff_of_A_IB_all_and_Z_IB_all, diff_of_all

    pass  # function
