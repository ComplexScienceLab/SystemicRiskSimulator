"""
最大熵值法计算边权重
"""

## 基于《方意_荆中博_2022_外部冲击下系统性金融风险的生成机制》

import numpy as np

def calculate_bilateral_exposure(IA, IB, TOL):
    N = IA.shape[0]  # 获取银行数量
    IA = np.sum(IA)  # 计算银行间总资产
    IB = np.sum(IB)  # 计算银行间总负债
    if IA != IB:  # 如果总资产不等于总负债
        IA = np.append(IA, np.max(IB-IA, 0))  # 创建虚拟银行以平衡总资产和总负债
        IB = np.append(IB, np.max(IA-IB, 0))
        N += 1  # 银行数量加1

    IA_i_star = IA / np.max([IA, IB])  # 标准化银行间资产负债矩阵
    IB_i_star = IB / np.max([IA, IB])
    X_ij_star = np.outer(IA_i_star, IB_i_star)  # 初始化准双边敞口

    t = 1
    while True:
        X_ij_prev = X_ij_star.copy()  # 保存上一次迭代的双边敞口矩阵

        for i in range(N):
            if np.sum(X_ij_prev[:, i]) == 0:  # 行约束迭代
                X_ij_star[:, i] = 0
            else:
                X_ij_star[:, i] = X_ij_prev[:, i] * IB_i_star[i] / np.sum(X_ij_prev[:, i])

            if np.sum(X_ij_prev[i, :]) == 0:  # 列约束迭代
                X_ij_star[i, :] = 0
            else:
                X_ij_star[i, :] = X_ij_prev[i, :] * IA_i_star[i] / np.sum(X_ij_prev[i, :])

        if np.max(np.abs(X_ij_star - X_ij_prev)) <= TOL:  # 检查是否满足收敛条件
            break

        t += 1

    X_ij = X_ij_star * np.max([IA, IB])  # 计算最终的双边敞口矩阵
    return X_ij





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
