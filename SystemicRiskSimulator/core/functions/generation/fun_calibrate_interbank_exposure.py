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
        A_IB (np.ndarray): 银行间资产邻接矩阵
        Z_IB (np.ndarray): 银行间负债邻接矩阵
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

    ## #NOTE 调整方案〇：假设事先已经调整过了，无需调整
    A_IB_adjasted, Z_IB_adjasted = A_IB, Z_IB

    # ## #NOTE 调整方案一：添加虚拟银行
    # A_IB_adjasted, Z_IB_adjasted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB, Z_IB)

    ## #NOTE 调整方案二：按照多出来的比例，压缩多出来的金额部分，使得二者相等。
    # A_IB_adjasted, Z_IB_adjasted = adjust_A_IB_Z_IB_by_resize(A_IB, Z_IB)




    # 将 NumPy 数组转换为 R 对象
    A_IB_r = numpy2ri.py2rpy(A_IB_adjasted)
    Z_IB_r = numpy2ri.py2rpy(Z_IB_adjasted)

    # 调用 R 中的 calibrate_interbank_exposure 函数
    model = systemicrisk.calibrate_ER(A_IB_r, Z_IB_r, target_density, n_samples_calib, thin)
    # 使用重构的模型生成样本
    reconstructed_L_r = systemicrisk.sample_HierarchicalModel(l=A_IB_r, a=Z_IB_r, model=model, nsamples=1, thin=thin)

    # 将 R 对象转换为 NumPy 数组
    reconstructed_L = np.array(reconstructed_L_r)

    # 最终的银行间负债矩阵
    A_IB_ij = reconstructed_L[0][0]
    Z_IB_ij = A_IB_ij.copy().T

    return A_IB_ij, Z_IB_ij

    ## #HACK 调用 R 函数方案二：导出 csv 文件再通过命令行运行 R 函数，最后导入生成的 csv 文件  BUG 这个方案暂时无法运行成功。原因是传入数值失败。

    # ## #NOTE 调整方案〇：假设事先已经调整过了，无需调整
    # A_IB_adjasted, Z_IB_adjasted = A_IB, Z_IB
    #
    # # ## #NOTE 调整方案一：添加虚拟银行
    # # A_IB_adjasted, Z_IB_adjasted, _ = adjust_A_IB_Z_IB_with_virtual_bank(A_IB, Z_IB)
    #
    # ## #NOTE 调整方案二：按照多出来的比例，压缩多出来的金额部分，使得二者相等。
    # # A_IB_adjasted, Z_IB_adjasted = adjust_A_IB_Z_IB_by_resize(A_IB, Z_IB)
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
