"功能函数集：构建测度指标"
##########################################
# 状态/开发
##########################################

from SystemicRiskSimulator.external_packages import np


# 构建测度指标

def SR_meansure(Loss_in_IB: np.array, E_all: np.array):
    """
    构建系统性风险测度指标 "SR"。

    Args:
        Loss_in_IB (np.array): 各时期各银行之银行间总损失
        E_all (np.array): 各时期各银行之资本

    Returns:
        测度结果

    """
    result = np.sum(Loss_in_IB) / np.sum(E_all)
    return result
    pass  # function

## TODO构建存贷比测度指标

## TODO构建准备金率测度指标
