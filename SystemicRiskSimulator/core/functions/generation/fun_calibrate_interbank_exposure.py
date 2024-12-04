"""
生成银行间敞口
"""

from SystemicRiskSimulator.external_packages import np, os, pd, Path
from SystemicRiskSimulator.core.functions.fun_adjast_bank_balanceSheet import adjust_A_IB_Z_IB_with_virtual_bank, adjust_A_IB_Z_IB_by_resize


def calibrate_interbank_exposure(A_IB, Z_IB, target_density, n_samples_calib=10, thin=100, folderpath_result: Path = None):
    """
    调用 R 语言之工具包 systemicrisk 之函数 calibrate_ER，校准银行间资产负债矩阵，到指定的密度。
    中的 calibrate_interbank_exposure 函数,并将结果转换为 NumPy 数组。

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

    # 调用 R 中的 calibrate_interbank_exposure 函数
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
