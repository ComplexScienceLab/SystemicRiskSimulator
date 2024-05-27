"""
@File   ：fun_adjast_bank_balanceSheet.py
调整银行资产负债表
"""

from SystemicRiskSimulator.external_packages import np


def adjust_A_IB_Z_IB_with_virtual_bank(A_IB, Z_IB):
    """
    如果 A_IB 和 Z_IB 的总资产与总负债不相等,则添加虚拟银行以平衡总资产与总负债。

    Args:
        A_IB (np.ndarray): 银行间资产邻接矩阵
        Z_IB (np.ndarray): 银行间负债邻接矩阵

    Returns:
        np.ndarray, np.ndarray: 调整后的 A_IB 和 Z_IB
    """
    N = A_IB.shape[0]  # 获取银行数量
    A_IB_total = np.sum(A_IB)  # 计算银行间总资产
    Z_IB_total = np.sum(Z_IB)  # 计算银行间总负债

    if A_IB_total != Z_IB_total:  # 如果总资产不等于总负债
        diff = np.abs(A_IB_total - Z_IB_total)
        A_IB_adjasted = np.append(A_IB, diff if Z_IB_total > A_IB_total else 0)  # 创建虚拟银行以平衡总资产和总负债
        Z_IB_adjasted = np.append(Z_IB, diff if A_IB_total > Z_IB_total else 0)
        N += 1  # 银行数量加1
        is_add_virtual_bank = True  # 标记是否添加了虚拟银行
    else:
        A_IB_adjasted = A_IB
        Z_IB_adjasted = Z_IB
        is_add_virtual_bank = False

    return A_IB_adjasted, Z_IB_adjasted, is_add_virtual_bank


def adjust_A_IB_Z_IB_by_resize(A_IB, Z_IB):
    """
    如果 A_IB 和 Z_IB 的总资产与总负债不相等,则按比例压缩多的那部分使得其总量与少的那部分总量相等。

    Args:
        A_IB (np.ndarray): 银行间资产邻接矩阵
        Z_IB (np.ndarray): 银行间负债邻接矩阵

    Returns:
        np.ndarray, np.ndarray: 调整后的 A_IB 和 Z_IB
    """
    N = A_IB.shape[0]  # 获取银行数量
    A_IB_total = np.sum(A_IB)  # 计算银行间总资产
    Z_IB_total = np.sum(Z_IB)  # 计算银行间总负债

    if A_IB_total != Z_IB_total:  # 如果总资产不等于总负债
        diff = np.abs(A_IB_total - Z_IB_total)
        resize_radios = np.minimum(A_IB_total, Z_IB_total) / np.maximum(A_IB_total, Z_IB_total)
        A_IB_adjasted = A_IB * resize_radios if A_IB_total > Z_IB_total else A_IB
        Z_IB_adjasted = Z_IB * resize_radios if A_IB_total < Z_IB_total else Z_IB
    else:
        A_IB_adjasted = A_IB
        Z_IB_adjasted = Z_IB

    # 再进一步微调，使得总资产和总负债相等
    if A_IB_adjasted.sum() != Z_IB_adjasted.sum():
        diff = np.abs(A_IB_adjasted.sum() - Z_IB_adjasted.sum())
        if A_IB_adjasted.sum() > Z_IB_adjasted.sum():
            A_IB_adjasted[0] = A_IB_adjasted[0] - diff
        else:
            Z_IB_adjasted[0] = Z_IB_adjasted[0] - diff

    # DEBUG 查看二者是否相等
    print(np.sum(A_IB_adjasted) == np.sum(Z_IB_adjasted))
    print(np.sum(A_IB_adjasted) - np.sum(Z_IB_adjasted))

    return A_IB_adjasted, Z_IB_adjasted
