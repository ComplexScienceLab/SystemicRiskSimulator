"""
最大熵值法计算边权重
"""

## 基于《方意_荆中博_2022_外部冲击下系统性金融风险的生成机制》附录一：最大信息熵算法

from PySystemicRiskLab import np


def calculate_bilateral_exposure(A_IB, Z_IB):
    """
    通过各银行之银行间资产与银行间负债估算银行间双边敞口。

    基于《方意_荆中博_2022_外部冲击下系统性金融风险的生成机制》附录一：最大信息熵算法
    方意, 荆中博, 2022. 外部冲击下系统性金融风险的生成机制[J/OL]. 管理世界, 38(5): 19-35+102+36-46. DOI:10.19744/j.cnki.11-1235/f.2022.0077.


    Args:
        A_IB (): 各银行之银行间资产
        Z_IB (): 各银行之银行间负债

    Returns:
        A_IB_ij (): 银行间资产矩阵
        Z_IB_ij (): 银行间负债矩阵
    """
    iteration_threshold = 0.01  # 迭代阈值
    precition_threshold = 0.0000000000001  # 分母精度阈值

    N = A_IB.shape[0]  # 获取银行数量
    A_IB_total = np.sum(A_IB)  # 计算银行间总资产
    Z_IB_total = np.sum(Z_IB)  # 计算银行间总负债
    if A_IB_total != Z_IB_total:  # 如果总资产不等于总负债
        A_IB = np.append(A_IB, np.max(Z_IB_total - A_IB_total, 0))  # 创建虚拟银行以平衡总资产和总负债
        Z_IB = np.append(Z_IB, np.max(A_IB_total - Z_IB_total, 0))
        N += 1  # 银行数量加1

    A_IB_i_star = A_IB / np.max([A_IB, Z_IB])  # 标准化银行间资产负债矩阵
    Z_IB_i_star = Z_IB / np.max([A_IB, Z_IB])
    X_ij_star = np.outer(A_IB_i_star, Z_IB_i_star)  # 初始化准双边敞口，通过外积计算

    t = 1
    while True:
        X_ij_prev = X_ij_star.copy()  # 保存上一次迭代的双边敞口矩阵

        for i in range(N):
            if np.sum(X_ij_prev[:, i]) == 0:  # 行约束迭代
                X_ij_star[:, i] = 0
            else:
                denominator = np.sum(X_ij_prev[:, i]) if np.sum(X_ij_prev[:, i]) > precition_threshold else precition_threshold
                X_ij_star[:, i] = X_ij_prev[:, i] * Z_IB_i_star[i] / denominator

            if np.sum(X_ij_prev[i, :]) == 0:  # 列约束迭代
                X_ij_star[i, :] = 0
            else:
                denominator = np.sum(X_ij_prev[i, :]) if np.sum(X_ij_prev[i, :]) > precition_threshold else precition_threshold
                X_ij_star[i, :] = X_ij_prev[i, :] * A_IB_i_star[i] / denominator

        if np.allclose(X_ij_star, X_ij_prev, atol=iteration_threshold):  # 判断是否达到收敛
            break

        t += 1

    # X_ij = X_ij_star * np.max([A_IB_total, Z_IB_total])  # 计算最终的双边敞口矩阵
    A_IB_ij = X_ij_star * np.max([A_IB_total, Z_IB_total])  # 计算最终的银行间资产矩阵
    Z_IB_ij = A_IB_ij.T.copy()  # 计算最终的银行间负债矩阵
    return A_IB_ij, Z_IB_ij

# ## 基于以下程序之 Stata 版本翻译成的 Python 版本： #HACK 感觉这个版本不太合适
# 熵值法通用程序 *********
#
# *          设计者：周晶
#
# *          单  位：中南财经政法大学工商管理学院农业经济系
# *          电  邮：zhoucejing@126.com
#
# import numpy as np
#
# def szf(m, n, *args):
#     A = np.zeros((n, 3))
#
#     for i in range(n):
#         j = i + 1
#         b = args[i]
#         b_mean = np.mean(b)
#         b_std = np.std(b)
#         bss = (b - b_mean) / b_std
#         bss = bss + np.min(bss) + 1
#         bs = bss / np.sum(bss)
#         e = np.sum(-1/np.log(m) * bs * np.log(bs))
#         d = 1 - e
#         w = d / np.sum(d)
#         f = np.sum(np.array([w[j-1] * bs[i] for j in range(n)]))
#         A[i, :] = [f, d, w]
#
#     return A
#
# m = 100  # 样本个数
# n = 5  # 指标个数
# x1 = np.random.rand(m)
# x2 = np.random.rand(m)
# x3 = np.random.rand(m)
# x4 = np.random.rand(m)
# x5 = np.random.rand(m)
#
# result = szf(m, n, x1, x2, x3, x4, x5)
# print(result)
# print("This program was developed by Zhou Jing, Zhongnan University of Economics & Law, Wuhan, China")
# print("Email: zhoucejing@126.com")
