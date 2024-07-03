"功能函数集：构建测度指标"
##########################################
# 状态/开发
##########################################

from SystemicRiskSimulator.external_packages import np


# 构建测度指标

def SR_meansure(Loss_in_IB: np.array, E_all: np.array):
    """
    构建系统性风险测度指标 "SR"。
    注意：要考虑里面的损失变量是否是存量还是流量。如果是存量变量，那么实际计算的时候，只需要代入最后一个时期的存量值即可。

    $$
    SR := \dfrac{\sum \limits_{i \in \mathbb{B}}^{} \left( \sum \limits_{\tau \ge 2}^{} {Loss}_{IB}^{i,\tau} \right)}{\sum \limits_{i \in \mathbb{B}}{E}_{B}[i,\tau=0]}
    $$

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
