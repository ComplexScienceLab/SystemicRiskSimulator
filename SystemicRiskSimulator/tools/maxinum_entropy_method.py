"""
# 最大熵值法计算边权重

基于《方意_荆中博_2022_外部冲击下系统性金融风险的生成机制》附录一：最大信息熵算法
"""

from SystemicRiskSimulator.external_packages import np, time
from SystemicRiskSimulator.core.functions.fun_adjast_bank_balanceSheet import adjust_A_IB_Z_IB_with_virtual_bank, adjust_A_IB_Z_IB_by_resize


def calculate_bilateral_exposure(A_IB: np.array, Z_IB: np.array, is_show_detal: bool = False, iteration_threshold: float = 1e-3, max_iteration: int = 30, denominator_precition_threshold: float = 1e-4):
    """
    通过各银行之银行间资产与银行间负债估算银行间双边敞口。

    基于《方意_荆中博_2022_外部冲击下系统性金融风险的生成机制》附录一：最大信息熵算法
    方意, 荆中博, 2022. 外部冲击下系统性金融风险的生成机制[J/OL]. 管理世界, 38(5): 19-35+102+36-46. DOI:10.19744/j.cnki.11-1235/f.2022.0077.


    Args:
        A_IB (np.array): 银行间资产邻接矩阵
        Z_IB (np.array): 银行间负债邻接矩阵
        is_show_detal (bool, optional): 是否显示迭代过程的热力图。默认值 False
        iteration_threshold (float, optional): 迭代阈值。默认值 1e-3
        max_iteration (int, optional): 最大迭代次数。默认值 30
        denominator_precition_threshold (float, optional): 分母精度阈值。默认值 1e-4
        
    Returns:
        A_IB_ij (np.array): 银行间资产邻接矩阵
        Z_IB_ij (np.array): 银行间负债邻接矩阵
    """

    is_add_virtual_bank = False  # 是否添加了虚拟银行

    # ## #NOTE 调整方案一：添加虚拟银行
    # A_IB, Z_IB, is_add_virtual_bank = adjust_A_IB_Z_IB_with_virtual_bank(A_IB, Z_IB)

    ## #NOTE 调整方案二：按照多出来的比例，压缩多出来的金额部分，使得二者相等。
    A_IB, Z_IB = adjust_A_IB_Z_IB_by_resize(A_IB, Z_IB)

    N = A_IB.shape[0]  # 获取银行数量
    A_IB_total = np.sum(A_IB)  # 计算银行间总资产
    Z_IB_total = np.sum(Z_IB)  # 计算银行间总负债

    A_IB_i_star = A_IB / np.max([A_IB, Z_IB])  # 标准化银行间资产负债矩阵
    Z_IB_i_star = Z_IB / np.max([A_IB, Z_IB])
    X_ij_star = np.outer(A_IB_i_star, Z_IB_i_star)  # 初始化准双边敞口，通过外积计算

    if is_show_detal:  # 可视化初始的标准双边敞口矩阵为热力图
        import matplotlib.pyplot as plt
        import seaborn as sns
        # 可视化初始的标准双边敞口矩阵为热力图
        # 创建热力图的颜色映射方案
        cmap = sns.diverging_palette(255, 0, s=99, as_cmap=True)
        cmap.set_bad(color='white')
        # 可视化初始数据之热力图
        sns.heatmap(X_ij_star, cmap=cmap, vmin=0, vmax=X_ij_star.max(), cbar=True)
        fig = plt.figure()  # 创建图形对象
        ax = fig.add_subplot(111)  # 添加子图
        ax.set_title('Iteration: 0')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        # plt.show()
        time.sleep(0.25)
        pass  # if

    iteration = 1
    while iteration < max_iteration:
        X_ij_prev = X_ij_star.copy()  # 保存上一次迭代的双边敞口矩阵

        for i in range(N):
            if np.sum(X_ij_prev[:, i]) == 0:  # 行约束迭代
                X_ij_star[:, i] = 0
            else:
                denominator = np.sum(X_ij_prev[:, i]) if np.sum(X_ij_prev[:, i]) > denominator_precition_threshold else denominator_precition_threshold
                X_ij_star[:, i] = X_ij_prev[:, i] * Z_IB_i_star[i] / denominator

            if np.sum(X_ij_prev[i, :]) == 0:  # 列约束迭代
                X_ij_star[i, :] = 0
            else:
                denominator = np.sum(X_ij_prev[i, :]) if np.sum(X_ij_prev[i, :]) > denominator_precition_threshold else denominator_precition_threshold
                X_ij_star[i, :] = X_ij_prev[i, :] * A_IB_i_star[i] / denominator

        if is_show_detal:  # 可视化迭代数据之热力图
            # 可视化迭代数据之热力图
            # 清除子图内容
            ax.clear()
            # 创建热力图
            sns.heatmap(X_ij_star, cmap=cmap, vmin=0, vmax=X_ij_star.max(), cbar=True)
            # 添加小于0的黑色掩码
            mask = X_ij_star < 0
            sns.heatmap(mask, cmap='gray', alpha=0.3, cbar=False, mask=mask)
            # 设置标题和轴标签
            ax.set_title('Iteration: {}'.format(iteration))
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            # 显示图像
            plt.show()
            time.sleep(0.25)
            print(f"第{iteration}次迭代。精度：{np.max(np.abs(X_ij_star - X_ij_prev))}")
            pass  # if

        if np.allclose(X_ij_star, X_ij_prev, atol=iteration_threshold):  # 判断是否达到收敛
            break

        iteration += 1

        pass  # while

    A_IB_ij = X_ij_star / X_ij_star.sum() * np.max([A_IB_total, Z_IB_total])  # 计算最终的银行间资产矩阵
    Z_IB_ij = A_IB_ij.copy().T  # 计算最终的银行间负债矩阵

    print("计算最大熵值法计算边权重完成。")

    if is_add_virtual_bank:  # 如果添加了虚拟银行，则删除虚拟银行
        return A_IB_ij[:-1, :-1], Z_IB_ij[:-1, :-1]
    else:
        return A_IB_ij, Z_IB_ij

# ## 基于以下程序之 Stata 版本翻译成的 Python 版本： #HACK 感觉这个版本不太合适于自己的情况
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
