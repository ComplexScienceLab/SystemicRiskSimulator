

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

    # 导入 R 中的 systemicrisk 包
    systemicrisk = importr('systemicrisk')

    # 将 NumPy 数组转换为 R 对象
    A_IB_r = ro.numpy2ri(A_IB)
    Z_IB_r = ro.numpy2ri(Z_IB)

    # 调用 R 中的 generate_interbank_exposure 函数
    reconstructed_L_r = systemicrisk.generate_interbank_exposure(A_IB_r, Z_IB_r, target_density, n_samples_calib, thin)

    # 将 R 对象转换为 NumPy 数组
    reconstructed_L = np.array(reconstructed_L_r)
    # Z_IB_ij = A_IB_ij.copy().T  # 计算最终的银行间负债矩阵  #TODO 加上转置的矩阵

    return reconstructed_L
