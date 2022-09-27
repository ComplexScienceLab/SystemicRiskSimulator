"功能函数集：计算损失。"

## 功能函数集：计算损失。

##########################################
# 状态/开发
##########################################

from PySystemicRiskLab.core import np
pass  # end import


## 函数区


## 更新各银行与各银行间之损失


"计算各银行之银行间损失。"


def calc_B_Loss(interbank_Loss):
    np.sum(interbank_Loss, axis=1).reshape(-1,1)
    pass
