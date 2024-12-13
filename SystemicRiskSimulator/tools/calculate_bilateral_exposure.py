"""
计算双边敞口边权重

- 使用中心边缘连接算法（Center Peripheral Connection），通过各银行之银行间资产与银行间负债估算银行间双边敞口。
- 使用最大熵值法（Maximum Entropy），通过各银行之银行间资产与银行间负债估算银行间双边敞口。
"""

from SystemicRiskSimulator.external_packages import np, time
from SystemicRiskSimulator.core.functions.fun_adjast_bank_balanceSheet import adjust_A_IB_Z_IB_with_virtual_bank, adjust_A_IB_Z_IB_by_resize


# from scipy import optimize


def calculate_bilateral_exposure_by_CP_algorithm(A_IB: np.array, Z_IB: np.array, num_core=20, is_show_detal: bool = False, is_add_virtual_bank=True, iteration_threshold: float = 1e-20, max_iteration: int = 1000, denominator_precition_threshold: float = 1e5):
    """
    使用中心边缘连接算法（Center Peripheral Connection），通过各银行之银行间资产与银行间负债估算银行间双边敞口。

    Args:
        A_IB (np.array): 各银行之银行间总资产
        Z_IB (np.array): 各银行之银行间总负债
        num_core (int): 核心银行数量。默认值 20
        is_show_detal (bool, optional): 是否显示迭代过程的热力图。默认值 False
        is_add_virtual_bank (bool, optional): 是否添加虚拟银行。默认值 True
        iteration_threshold (float, optional): 迭代阈值。默认值 1e-20
        max_iteration (int, optional): 最大迭代次数。默认值 1000
        denominator_precition_threshold (float, optional): 归一化阈值。默认值 1e5
    """

    def ras(A0: np.array) -> np.array:
        """
        RAS 方法是一种矩阵调整技术，适用于已知行列总和约束的情境，通常用于平衡矩阵中的行、列总和以达到指定的边际值。在网络生成中，比如借贷矩阵生成时，我们可以使用 RAS 方法确保生成的矩阵符合银行的借入、借出总额约束。

        Args:
            A0 (numpy.ndarray): 输入矩阵。

        Returns:
            numpy.ndarray: 调整后的矩阵。
        """
        A = np.zeros_like(A0)
        A1 = np.zeros_like(A0)
        temp_x = A0.sum(axis=1)
        r_x = np.where(temp_x == 0, 1, A_IB_adjasted / temp_x)
        A1 = A0 * r_x[:, np.newaxis]
        temp_y = A1.sum(axis=0)
        r_y = np.where(temp_y == 0, 1, Z_IB_adjasted / temp_y)
        A = A1 * r_y[np.newaxis, :]
        return A
        pass  # function

    # is_add_virtual_bank = False  # 是否添加了虚拟银行

    ## 预处理维度
    A_IB, Z_IB = A_IB.flatten(), Z_IB.flatten()

    ## 调整银行资产负债表使得总资产与总负债相等

    ## #NOTE 调整方案〇：无需调整
    # A_IB_adjasted, Z_IB_adjasted = A_IB, Z_IB

    ## #NOTE 调整方案一：添加虚拟银行
    A_IB_adjasted, Z_IB_adjasted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB, Z_IB)

    # #NOTE 调整方案二：按照多出来的比例，压缩多出来的金额部分，使得二者相等。
    # A_IB_adjasted, Z_IB_adjasted = adjust_A_IB_Z_IB_by_resize(A_IB, Z_IB)

    N = A_IB_adjasted.shape[0]  # 获取银行数量

    N = N
    A_IB_adjasted = A_IB_adjasted
    Z_IB_adjasted = Z_IB_adjasted
    A_IB_adjasted = np.array(A_IB_adjasted)
    Z_IB_adjasted = np.array(Z_IB_adjasted)

    A0 = np.ones((N, N))
    A0 = np.outer(A_IB_adjasted, Z_IB_adjasted) / denominator_precition_threshold
    np.fill_diagonal(A0, 0)
    A0[num_core:, num_core:] = 0
    temp_j = np.random.choice(np.arange(num_core), N - num_core)
    temp_i = np.random.choice(np.arange(num_core), N - num_core)
    A0[num_core:, :num_core] = np.where(np.arange(num_core) == temp_j[:, np.newaxis], A0[num_core:, :num_core], 0)
    A0[:num_core, num_core:] = np.where(np.arange(num_core)[:, np.newaxis] == temp_i, A0[:num_core, num_core:], 0)

    # while iteration_threshold > 0.0001:  # #BUG 如果一开始就满足条件，而不进入循环，会导致返回值有问题。因此需要在前面初始化 A_IB_ij
    iteration = 1
    while iteration < max_iteration:
        A_IB_ij = ras(A0)

        if is_show_detal:  # 可视化初始的标准双边敞口矩阵为热力图
            import matplotlib.pyplot as plt
            import seaborn as sns
            # 可视化初始的标准双边敞口矩阵为热力图
            # 创建热力图的颜色映射方案
            cmap = sns.diverging_palette(255, 0, s=99, as_cmap=True)
            cmap.set_bad(color='white')
            # 可视化初始数据之热力图
            sns.heatmap(A_IB_ij, cmap=cmap, vmin=0, vmax=A_IB_ij.max(), cbar=True)
            fig = plt.figure()  # 创建图形对象
            ax = fig.add_subplot(111)  # 添加子图
            ax.set_title('Iteration: 0')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            # plt.show()
            time.sleep(0.25)
            pass  # if

        if np.allclose(A_IB_ij, A0, atol=iteration_threshold):  # 判断是否达到收敛
            break

        iteration += 1
        A0 = A_IB_ij.copy()

        pass  # while

    Z_IB_ij = A_IB_ij.copy().T

    # #DEBUG 测试是否正确
    print(f"总元素和：{round(A_IB_ij.sum() - A_IB_adjasted.sum())}")
    print(f"行元素和：{np.round(A_IB_ij.sum(axis=1) - A_IB_adjasted)}")
    print(f"列元素和：{np.round(A_IB_ij.sum(axis=0) - Z_IB_adjasted)}")

    print("计算最大熵值法计算边权重完成。")

    if is_add_virtual_bank:  # 如果添加了虚拟银行，则删除虚拟银行
        return A_IB_ij[:-1, :-1], Z_IB_ij[:-1, :-1]
    else:
        return A_IB_ij, Z_IB_ij

    pass  # function


def calculate_bilateral_exposure_by_ME_algorithm(A_IB: np.array, Z_IB: np.array, target_density: float = 0.25, is_show_detal: bool = False, is_add_virtual_bank=True, iteration_threshold: float = 1e-20, max_iteration: int = 1000, denominator_precition_threshold: float = 1e-20):
    """
    使用最大熵值法（Maximum Entropy），通过各银行之银行间资产与银行间负债估算银行间双边敞口。

    基于《方意_荆中博_2022_外部冲击下系统性金融风险的生成机制》附录一：最大信息熵算法

    > 方意, 荆中博, 2022. 外部冲击下系统性金融风险的生成机制[J/OL]. 管理世界, 38(5): 19-35+102+36-46. DOI:10.19744/j.cnki.11-1235/f.2022.0077.


    Args:
        A_IB (np.array): 银行间资产邻接矩阵
        Z_IB (np.array): 银行间负债邻接矩阵
        target_density (float): 邻接矩阵指定的密度。默认值 0.25
        is_show_detal (bool, optional): 是否显示迭代过程的热力图。默认值 False
        is_add_virtual_bank (bool, optional): 是否添加虚拟银行。默认值 True
        iteration_threshold (float, optional): 迭代阈值。默认值 1e-3
        max_iteration (int, optional): 最大迭代次数。默认值 30
        denominator_precition_threshold (float, optional): 分母精度阈值。默认值 1e-4
        
    Returns:
        A_IB_ij (np.array): 银行间资产邻接矩阵
        Z_IB_ij (np.array): 银行间负债邻接矩阵
    """

    ## 预处理维度
    A_IB, Z_IB = A_IB.flatten(), Z_IB.flatten()

    ## 调整银行资产负债表使得总资产与总负债相等

    ## #NOTE 调整方案〇：无需调整
    # A_IB_adjasted, Z_IB_adjasted = A_IB, Z_IB

    ## #NOTE 调整方案一：添加虚拟银行
    A_IB_adjasted, Z_IB_adjasted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB, Z_IB)

    # ## #NOTE 调整方案二：按照多出来的比例，压缩多出来的金额部分，使得二者相等。
    # A_IB_adjasted, Z_IB_adjasted = adjust_A_IB_Z_IB_by_resize(A_IB, Z_IB)

    N = A_IB_adjasted.shape[0]  # 获取银行数量

    ## 预置一些先验的元素值
    X_ij_fixedVal = np.full((N, N), np.nan)  # 使用np.nan表示没有被预置的元素

    # 预置规则 1：对角线为 0
    np.fill_diagonal(X_ij_fixedVal, 0)

    ## 根据预置的元素值，重新计算银行间资产负债矩阵之行和、列和
    X_ij_mask = np.isnan(X_ij_fixedVal)  # 预置的元素值的掩码
    A_IB_adjasted_prior = A_IB_adjasted - np.sum(np.where(X_ij_mask, 0, X_ij_fixedVal), axis=1)
    Z_IB_adjasted_prior = Z_IB_adjasted - np.sum(np.where(X_ij_mask, 0, X_ij_fixedVal), axis=0)

    A_IB_i_star = A_IB_adjasted / np.max([A_IB_adjasted_prior, Z_IB_adjasted_prior])  # 标准化银行间资产负债矩阵
    Z_IB_i_star = Z_IB_adjasted / np.max([A_IB_adjasted_prior, Z_IB_adjasted_prior])
    X_ij_star_0 = np.sqrt(np.outer(A_IB_i_star, Z_IB_i_star))  # 初始化准双边敞口，通过外积计算
    # X_ij_star_0 = np.outer(A_IB_i_star, Z_IB_i_star)  # 初始化准双边敞口，通过外积计算
    X_ij_star_prior_0 = np.zeros((N, N))  # 初始化准双边敞口
    X_ij_star_prior_0[X_ij_mask] = X_ij_star_0[X_ij_mask] * (X_ij_star_0.sum() / np.outer(A_IB_i_star, Z_IB_i_star)[X_ij_mask].sum())  # 初始化准双边敞口，通过外积计算
    X_ij_star_prior_0[~X_ij_mask] = X_ij_fixedVal[~X_ij_mask]
    X_ij_star = X_ij_star_prior_0.copy()  # 初始化标准双边敞口矩阵

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

        # ## #NOTE 考虑预置元素 #BUG 这个方案运行之后的结果误差很大，以至于无法使用。原因未知。
        # for i in range(N):
        #     X_j_mask = np.isnan(X_ij_fixedVal[:, i])
        #     if X_j_mask.any():
        #         X_j_prev = np.sum(X_ij_prev[:, i][X_j_mask])
        #         if X_j_prev == 0:  # 行约束迭代
        #             X_ij_star[:, i][X_j_mask] = 0
        #         else:
        #             denominator = X_j_prev if X_j_prev > denominator_precition_threshold else denominator_precition_threshold
        #             X_ij_star[:, i][X_j_mask] = X_ij_prev[:, i][X_j_mask] * Z_IB_i_star[i] / denominator
        #
        #     X_i_mask = np.isnan(X_ij_fixedVal[i, :])
        #     if X_i_mask.any():
        #         X_i_prev = np.sum(X_ij_prev[i, :][X_i_mask])
        #         if X_i_prev == 0:  # 列约束迭代
        #             X_ij_star[i, :][X_i_mask] = 0
        #         else:
        #             denominator = X_i_prev if X_i_prev > denominator_precition_threshold else denominator_precition_threshold
        #             X_ij_star[i, :][X_i_mask] = X_ij_prev[i, :][X_i_mask] * A_IB_i_star[i] / denominator

        ## NOTE 不考虑预置元素
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
            mask = X_ij_mask
            # mask = X_ij_star < 0
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

    ## #NOTE 计算不考虑预置值的最终的银行间资产矩阵
    A_IB_ij = X_ij_star / X_ij_star.sum() * np.max([A_IB_adjasted_prior.sum(), Z_IB_adjasted_prior.sum()])  # 计算最终的银行间资产矩阵
    Z_IB_ij = A_IB_ij.copy().T

    # ## #NOTE 计算预置值之后的最终的银行间资产矩阵、银行间负债矩阵  #BUG 这个方案运行之后的结果误差很大，以至于无法使用。原因未知。
    # A_IB_ij = np.zeros((N, N))
    # A_IB_ij[X_ij_mask] = X_ij_star[X_ij_mask] * (np.max([A_IB_adjasted_prior.sum(), Z_IB_adjasted_prior.sum()]) / X_ij_star[X_ij_mask].sum())
    # # A_IB_ij[X_ij_mask] = X_ij_star[X_ij_mask] / X_ij_star[X_ij_mask].sum() * np.max([A_IB_adjasted.sum(), Z_IB_adjasted.sum()])
    # A_IB_ij[~X_ij_mask] = X_ij_fixedVal[~X_ij_mask]  # 计算包括预置部分的最终的银行间资产矩阵、银行间负债矩阵
    # Z_IB_ij = A_IB_ij.copy().T

    # #DEBUG 测试是否正确
    print(f"总元素和：{round(A_IB_ij.sum() - A_IB_adjasted.sum())}")
    print(f"行元素和：{np.round(A_IB_ij.sum(axis=1) - A_IB_adjasted)}")
    print(f"列元素和：{np.round(A_IB_ij.sum(axis=0) - Z_IB_adjasted)}")

    print("计算最大熵值法计算边权重完成。")

    if is_add_virtual_bank:  # 如果添加了虚拟银行，则删除虚拟银行
        return A_IB_ij[:-1, :-1], Z_IB_ij[:-1, :-1]
    else:
        return A_IB_ij, Z_IB_ij

    pass  # function

# ## 基于以下程序之 Stata 版本翻译成的 Python 版本： #HACK 感觉这个版本不太合适于自己的情况
# # 熵值法通用程序 *********
# #
# # *          设计者：周晶
# #
# # *          单  位：中南财经政法大学工商管理学院农业经济系
# # *          电  邮：zhoucejing@126.com
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
