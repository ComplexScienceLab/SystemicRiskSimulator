"""
计算双边敞口边权重

- 使用中心边缘连接算法（Center Peripheral Connection），通过各银行之银行间资产与银行间负债估算银行间双边敞口。
- 使用最大熵值法（Maximum Entropy），通过各银行之银行间资产与银行间负债估算银行间双边敞口。
"""

from SystemicRiskSimulator.external_packages import np, Path, time
from SystemicRiskSimulator.core.functions.fun_adjast_bank_balanceSheet import adjust_A_IB_Z_IB_with_virtual_bank, adjust_A_IB_Z_IB_by_resize


# from scipy import optimize

def calculate_bilateral_exposure_by_CP_algorithm(A_IB_all: np.array, Z_IB_all: np.array, array_idx_core_bank: np.array, num_core=20, is_show_detal: bool = False, is_add_virtual_bank=True, iteration_threshold: float = 1e-20, max_iteration: int = 1000, denominator_precition_threshold: float = 1e5):
    """
    使用中心边缘连接算法（Center Peripheral Connection），通过各银行之银行间资产与银行间负债估算银行间双边敞口。

    Args:
        A_IB_all (np.array): 各银行之银行间总资产。注意，在导入之前需要自行将中心银行排在前面。
        Z_IB_all (np.array): 各银行之银行间总负债。注意，在导入之前需要自行将中心银行排在前面。
        array_idx_core_bank (np.array): 核心银行集合之索引
        num_core (int): 核心银行数量。默认值 20
        is_show_detal (bool, optional): 是否显示迭代过程的热力图。默认值 False
        is_add_virtual_bank (bool, optional): 是否添加虚拟银行。默认值 True
        iteration_threshold (float, optional): 迭代阈值。默认值 1e-20
        max_iteration (int, optional): 最大迭代次数。默认值 1000
        denominator_precition_threshold (float, optional): 归一化阈值。默认值 1e5
    """

    import numpy as np
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
    A_IB_all, Z_IB_all = A_IB_all.flatten(), Z_IB_all.flatten()

    ## 调整银行资产负债表使得总资产与总负债相等

    ## #NOTE 调整方案〇：无需调整
    # A_IB_adjasted, Z_IB_adjasted = A_IB, Z_IB

    ## #NOTE 调整方案一：添加虚拟银行
    A_IB_adjasted, Z_IB_adjasted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB_all, Z_IB_all)

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

    if is_show_detal:  # 可视化初始的标准双边敞口矩阵为热力图
        import matplotlib.pyplot as plt
        # 可视化初始的标准双边敞口矩阵为热力图
        fig, ax = plt.subplots()
        cax = ax.matshow(A0, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_title('Iteration: 0')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        plt.show()
        time.sleep(0.50)
        pass  # if

    # while iteration_threshold > 0.0001:  # #BUG 如果一开始就满足条件，而不进入循环，会导致返回值有问题。因此需要在前面初始化 A_IB_ij
    iteration = 1
    while iteration < max_iteration:
        A_IB_ij = ras(A0)

        if is_show_detal:  # 可视化初始的标准双边敞口矩阵为热力图
            fig, ax = plt.subplots()
            cax = ax.matshow(A_IB_ij, cmap='coolwarm')
            fig.colorbar(cax)
            ax.set_title('Iteration: {}'.format(iteration))
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            plt.show()
            time.sleep(0.50)
            print(f"第{iteration}次迭代。精度：{np.max(np.abs(A_IB_ij - A0))}")
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

    print("中心边缘连接算法计算边权重完成。")

    if is_add_virtual_bank:  # 如果添加了虚拟银行，则删除虚拟银行
        return A_IB_ij[:-1, :-1], Z_IB_ij[:-1, :-1]
    else:
        return A_IB_ij, Z_IB_ij

    pass  # function


def calculate_bilateral_exposure_by_ME_algorithm(A_IB_all: np.array, Z_IB_all: np.array, target_density: float = 0.25, is_show_detal: bool = False, is_add_virtual_bank=True, iteration_threshold: float = 1e-20, max_iteration: int = 1000, denominator_precition_threshold: float = 1e-20):
    """
    使用最大熵值法（Maximum Entropy），通过各银行之银行间资产与银行间负债估算银行间双边敞口。

    基于《方意_荆中博_2022_外部冲击下系统性金融风险的生成机制》附录一：最大信息熵算法

    > 方意, 荆中博, 2022. 外部冲击下系统性金融风险的生成机制[J/OL]. 管理世界, 38(5): 19-35+102+36-46. DOI:10.19744/j.cnki.11-1235/f.2022.0077.


    Args:
        A_IB_all (np.array): 银行间资产邻接矩阵
        Z_IB_all (np.array): 银行间负债邻接矩阵
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
    import numpy as np

    ## 预处理维度
    A_IB_all, Z_IB_all = A_IB_all.flatten(), Z_IB_all.flatten()

    ## 调整银行资产负债表使得总资产与总负债相等

    ## #NOTE 调整方案〇：无需调整
    # A_IB_adjasted, Z_IB_adjasted = A_IB, Z_IB

    ## #NOTE 调整方案一：添加虚拟银行
    A_IB_adjasted, Z_IB_adjasted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB_all, Z_IB_all)

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
        # 可视化初始的标准双边敞口矩阵为热力图
        fig, ax = plt.subplots()
        cax = ax.matshow(X_ij_star, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_title('Iteration: 0')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        plt.show()
        time.sleep(0.50)
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
            fig, ax = plt.subplots()
            cax = ax.matshow(X_ij_star, cmap='coolwarm', vmin=0, vmax=X_ij_star.max())
            fig.colorbar(cax)
            mask = X_ij_mask
            ax.matshow(mask, cmap='gray', alpha=0.3)
            ax.set_title('Iteration: {}'.format(iteration))
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            plt.show()
            time.sleep(0.50)
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

    print("最大熵值法计算边权重完成。")

    if is_add_virtual_bank:  # 如果添加了虚拟银行，则删除虚拟银行
        return A_IB_ij[:-1, :-1], Z_IB_ij[:-1, :-1]
    else:
        return A_IB_ij, Z_IB_ij

    pass  # function


def calibrate_bilateral_exposure_by_ME_algorithm_by_R_package(A_IB, Z_IB, target_density, n_samples_calib=10, thin=100, folderpath_result: Path = None):
    """
    调用 R 语言之工具包 systemicrisk 之函数 calibrate_ER，校准银行间资产负债矩阵，到指定的密度。
    中的 calibrate_bilateral_exposure_by_ME_algorithm_by_R_package 函数,并将结果转换为 NumPy 数组。

    Args:
        A_IB (np.ndarray): 银行间资产
        Z_IB (np.ndarray): 银行间负债
        target_density (float): 目标密度
        n_samples_calib (int, optional): 校准时生成的矩阵样本数量。默认为 10。
        thin (int, optional): 校准时的稀疏化参数。默认为 100。
        folderpath_result (Path, optional): 结果文件夹路径。默认为 None。

    Returns:
        np.ndarray: 重构后的银行间资产负债矩阵
    """

    ## #NOTE 调用 R 函数方案一：使用 rpy2 直接调用
    import rpy2.robjects as ro
    from rpy2.robjects.packages import importr
    from rpy2.robjects import numpy2ri

    ro.conversion.py2rpy = numpy2ri.py2rpy

    # 导入 R 中的 systemicrisk 包
    systemicrisk = importr('systemicrisk')

    ## #NOTE 调整方案〇：无需调整
    # A_IB_adjasted, Z_IB_adjasted = A_IB, Z_IB

    # ## #NOTE 调整方案一：添加虚拟银行
    # A_IB_adjasted, Z_IB_adjasted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB, Z_IB)

    ## #NOTE 调整方案二：按照多出来的比例，压缩多出来的金额部分，使得二者相等。
    A_IB_adjasted, Z_IB_adjasted = adjust_A_IB_Z_IB_by_resize(A_IB, Z_IB)

    # 将 NumPy 数组转换为 R 对象
    A_IB_r = numpy2ri.py2rpy(A_IB_adjasted)
    Z_IB_r = numpy2ri.py2rpy(Z_IB_adjasted)

    # 调用 R 中的 calibrate_bilateral_exposure_by_ME_algorithm_by_R_package 函数
    if A_IB_adjasted.size != Z_IB_adjasted.size:  # 如果 A_IB 不是方阵，则使用 nonsquare 模型
        model = systemicrisk.calibrate_ER_nonsquare(A_IB_r, Z_IB_r, float(target_density), n_samples_calib, thin)
    else:
        model = systemicrisk.calibrate_ER(A_IB_r, Z_IB_r, float(target_density), n_samples_calib, thin)
        pass  # if

    # 使用重构的模型生成样本
    reconstructed_L_r = systemicrisk.sample_HierarchicalModel(l=A_IB_r, a=Z_IB_r, model=model, nsamples=1, thin=thin)

    # 将 R 对象转换为 NumPy 数组
    reconstructed_L = np.array(reconstructed_L_r)

    # 最终的银行间负债矩阵
    A_IB_ij = reconstructed_L[0][0]
    Z_IB_ij = A_IB_ij.copy().T

    return A_IB_ij, Z_IB_ij

    ## #HACK 调用 R 函数方案二：导出 csv 文件再通过命令行运行 R 函数，最后导入生成的 csv 文件  BUG 这个方案暂时无法运行成功。原因是传入数值失败。

    # ## #NOTE 调整方案〇：无需调整
    # # A_IB_adjasted, Z_IB_adjasted = A_IB, Z_IB
    #
    # # ## #NOTE 调整方案一：添加虚拟银行
    # # A_IB_adjasted, Z_IB_adjasted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB, Z_IB)
    #
    # ## #NOTE 调整方案二：按照多出来的比例，压缩多出来的金额部分，使得二者相等。
    # A_IB_adjasted, Z_IB_adjasted = adjust_A_IB_Z_IB_by_resize(A_IB, Z_IB)
    #
    # # 保存 A_IB 和 Z_IB 到 CSV 文件
    # np.savetxt("A_IB_all.csv", A_IB_adjasted, delimiter=",")
    # np.savetxt("Z_IB_all.csv", Z_IB_adjasted, delimiter=",")
    #
    # # 运行 R 脚本
    # # os.system(f"Rscript fun_calibrate_interbank_exposure.R -t {target_density} -i {folderpath_result} -o {Path(folderpath_result, 'reconstructed_L.csv')} -n {n_samples_calib} -l {thin}")
    # os.system(rf'Rscript {Path(Path(__file__).parent.resolve(), "fun_calibrate_interbank_exposure.R")} -d {target_density} -i "{str(folderpath_result)}" -o "{Path(folderpath_result, "reconstructed_L.csv")}" -n {n_samples_calib} -l {thin}')
    #
    # # 读取生成的 CSV 文件
    # reconstructed_L = pd.read_csv("reconstructed_L.csv", header=None).to_numpy()
    #
    # return reconstructed_L

# import numpy as np
# from scipy.optimize import fsolve
#
# def calibrate_ER(l, a, target_density, L_fixed=None, n_samples_calib=100, thin_calib=100):
#     """
#     根据给定的行和列总和,以及目标密度,校准 Erdos-Renyi (ER) 模型。
#
#     参数:
#     l (np.ndarray): 待重构矩阵的行总和
#     a (np.ndarray): 待重构矩阵的列总和
#     target_density (float): 期望的网络密度
#     L_fixed (np.ndarray, optional): 包含已知值的矩阵,NA表示未知。默认为None,表示没有已知值。
#     n_samples_calib (int, optional): 校准过程中生成的矩阵样本数量。默认为100。
#     thin_calib (int, optional): 校准过程中的稀疏化参数。默认为100。
#
#     返回:
#     Model: 校准后的ER模型,可用于生成样本。
#     """
#     n = len(l)
#     if L_fixed is not None:
#         n_free = np.sum(np.isnan(L_fixed))
#     else:
#         n_free = n * n
#     lambda_ = 1 / (np.sum(l) / (target_density * n_free))
#
#     def f(p):
#         print(f"p={p}")
#         model = Model_Indep_p_lambda(Model_p_constant(n, p), Model_lambda_constant(lambda_, n))
#         L_samples = sample_HierarchicalModel(l, a, L_fixed=L_fixed, model=model, n_samples=n_samples_calib, thin=100)
#         return np.mean([np.mean(x > 0) for x in L_samples["L"]] if L_fixed is None else
#                       [np.mean(np.where(~np.isnan(L_fixed), x > 0, np.nan), skipna=True) for x in L_samples["L"]]) - target_density
#
#     res = fsolve(f, 0.5, xtol=0.01, maxfev=20)
#     p = res[0]
#     print(f"p={p}")
#     return Model_Indep_p_lambda(Model_p_constant(n, p), Model_lambda_constant(lambda_, n))
#
# import numpy as np
#
# def sample_HierarchicalModel(l, a, L_fixed=None, model=None, n_samples=10000, thin=100, burn_in=None, matr_per_theta=None, silent=False, tol=np.sqrt(np.finfo(float).eps)):
#     """
#     从给定的行和列总和以及模型中采样矩阵。
#
#     参数:
#     l (np.ndarray): 每个节点的出度之和
#     a (np.ndarray): 每个节点的入度之和
#     L_fixed (np.ndarray, optional): 包含已知值的矩阵,NA表示未知。默认为None,表示没有已知值。
#     model (Model): 校准后的ER模型
#     n_samples (int): 要生成的样本数量
#     thin (int): 采样过程中的稀疏化参数
#     burn_in (int, optional): burn-in的迭代次数,默认为5%的采样次数
#     matr_per_theta (int, optional): 每次更新θ时更新矩阵的次数
#     silent (bool, optional): 是否抑制输出
#     tol (float, optional): 用于检查相等的容差
#
#     返回:
#     dict: 包含生成的样本矩阵和模型参数的字典
#     """
#     # 实现采样过程
#     pass
#
# if __name__ == '__main__':
#     import numpy as np
#
#     # 首先生成一个真实的网络
#     n = 10
#     p = 0.45
#     lam = 0.1
#     L = np.random.binomial(1, p, (n, n)) * np.random.exponential(1/lam, (n, n))
#
#     # 然后使用目标密度0.55重构网络
#     model = calibrate_ER(rowsum(L), colsum(L), 0.55, n_samples_calib=10)
#     L_samples = sample_HierarchicalModel(rowsum(L), colsum(L), model=model, n_samples=10, thin=100)
#
#     # 检查行总和
#     print(rowsum(L))
#     print(rowsum(L_samples["L"][-1]))
#
#     # 检查校准结果
#     print(np.mean(L_samples["L"][-1] > 0))
#
#     # 现在有一些固定的条目
#     L_fixed = L.copy()
#     L_fixed[:n//2, :] = np.nan
#     # 然后使用目标密度0.9重构网络
#     model = calibrate_ER(rowsum(L), colsum(L), 0.9, L_fixed=L_fixed, n_samples_calib=10)
#     L_samples = sample_HierarchicalModel(rowsum(L), colsum(L), L_fixed=L_fixed, model=model, n_samples=10, thin=100)
#     print(np.mean(L_samples["L"][-1][n//2:, :] > 0))  # 已知条目
#     print(np.mean(L_samples["L"][-1][:n//2, :] > 0))  # 重构的条目




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


if __name__ == "__main__":

    ## 测试 calculate_bilateral_exposure_by_CP_algorithm

    # 假设有 8 个中心银行和 24 个边缘银行
    num_core = 8
    num_peripheral = 24
    num_banks = num_core + num_peripheral

    # 随机生成银行间总资产和总负债矩阵
    np.random.seed(42)  # 固定随机种子以便复现结果
    A_IB_all = np.random.rand(num_banks) * 100
    A_IB_all[:num_core] = (np.random.rand(num_core) + 1) * 500
    Z_IB_all = np.random.rand(num_banks) * 100
    Z_IB_all[:num_core] = (np.random.rand(num_core) + 1) * 500
    Z_IB_all = A_IB_all.sum() / Z_IB_all.sum() * Z_IB_all  # A_IB_all 与 Z_IB_all 之和相等

    # 核心银行的索引
    array_idx_core_bank = np.arange(num_core)

    # 调用函数计算双边敞口
    A_IB_ij, Z_IB_ij = calculate_bilateral_exposure_by_CP_algorithm(
        A_IB_all=A_IB_all,
        Z_IB_all=Z_IB_all,
        array_idx_core_bank=array_idx_core_bank,
        num_core=num_core,
        is_show_detal=True,
        is_add_virtual_bank=False,
        iteration_threshold=1e-5,
        max_iteration=1000,
        denominator_precition_threshold=1e5
    )

    # 打印结果
    print("银行间资产矩阵 A_IB_ij:")
    print(A_IB_ij)
    print("\n银行间负债矩阵 Z_IB_ij:")
    print(Z_IB_ij)
    print(f"\n总元素和之误差：{round(A_IB_ij.sum() - A_IB_all.sum())}")
    print(f"\n行元素和之误差：{np.round(A_IB_ij.sum(axis=1) - A_IB_all)}")
    print(f"\n列元素和之误差：{np.round(A_IB_ij.sum(axis=0) - Z_IB_all)}")

    print("\n测试 calculate_bilateral_exposure_by_CP_algorithm 完成。\n\n\n")

    ## 测试 calculate_bilateral_exposure_by_ME_algorithm

    import numpy as np

    # 假设有 10 个银行
    num_banks = 10

    # 随机生成银行间总资产和总负债矩阵
    np.random.seed(42)  # 固定随机种子以便复现结果
    A_IB_all = np.random.rand(num_banks) * 100
    Z_IB_all = np.random.rand(num_banks) * 100
    Z_IB_all = A_IB_all.sum() / Z_IB_all.sum() * Z_IB_all  # A_IB_all 与 Z_IB_all 之和相等

    # 调用函数计算双边敞口
    A_IB_ij, Z_IB_ij = calculate_bilateral_exposure_by_ME_algorithm(
        A_IB_all=A_IB_all,
        Z_IB_all=Z_IB_all,
        target_density=0.25,
        is_show_detal=True,
        is_add_virtual_bank=False,
        iteration_threshold=1e-5,
        max_iteration=100,
        denominator_precition_threshold=1e-5
    )

    # 打印结果
    print("银行间资产矩阵 A_IB_ij:")
    print(A_IB_ij)
    print("\n银行间负债矩阵 Z_IB_ij:")
    print(Z_IB_ij)
    print(f"\n总元素和之误差：{round(A_IB_ij.sum() - A_IB_all.sum())}")
    print(f"\n行元素和之误差：{np.round(A_IB_ij.sum(axis=1) - A_IB_all)}")
    print(f"\n列元素和之误差：{np.round(A_IB_ij.sum(axis=0) - Z_IB_all)}")

    print("\n测试 calculate_bilateral_exposure_by_ME_algorithm 完成。\n\n\n")
