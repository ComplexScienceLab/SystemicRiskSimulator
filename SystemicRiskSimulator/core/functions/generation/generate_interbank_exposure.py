def generate_interbank_exposure(A_IB, Z_IB, target_density, n_samples_calib=10, thin=100):
    """
    调用 R 中的 generate_interbank_exposure 函数,并将结果转换为 NumPy 数组。

    Args:
        A_IB (np.ndarray): 银行间资产邻接矩阵
        Z_IB (np.ndarray): 银行间负债邻接矩阵
        target_density (float): 目标密度
        n_samples_calib (int, optional): 校准时生成的矩阵样本数量。默认为 10。
        thin (int, optional): 校准时的稀疏化参数。默认为 100。

    Returns:
        np.ndarray: 重构后的银行间资产负债矩阵
    """

    import numpy as np
    import rpy2.robjects as ro
    from rpy2.robjects.packages import importr
    from rpy2.robjects import numpy2ri

    ro.conversion.py2rpy = numpy2ri.py2rpy

    # 导入 R 中的 systemicrisk 包
    systemicrisk = importr('systemicrisk')

    # 因为 A_IB 与 Z_IB 的总资产与总负债可能不相等，所以需要添加虚拟银行以平衡总资产与总负债
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
        is_add_virtual_bank = False

    # 将 NumPy 数组转换为 R 对象
    A_IB_r = numpy2ri.py2rpy(A_IB_adjasted)
    Z_IB_r = numpy2ri.py2rpy(Z_IB_adjasted)

    # 调用 R 中的 generate_interbank_exposure 函数
    reconstructed_L_r = systemicrisk.calibrate_ER(A_IB_r, Z_IB_r, target_density, n_samples_calib, thin)

    # 将 R 对象转换为 NumPy 数组
    reconstructed_L = np.array(reconstructed_L_r)
    # Z_IB_ij = A_IB_ij.copy().T  # 计算最终的银行间负债矩阵  #TODO 加上转置的矩阵

    return reconstructed_L
