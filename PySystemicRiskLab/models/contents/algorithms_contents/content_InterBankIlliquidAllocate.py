"""银行间挤兑流动分配借贷流量算法"""

##########################################
# 状态/使用
##########################################

from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_finance import Finance

pass  # end import


def content_InterBankIlliquidAllocate(BB: BankCommercial, IB: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 流动性短缺银行间挤兑流动分配借贷流量算法

    Finance.update_finance_variables(BB, IB, b, ib, by_way='enabled collect A_P')  # 计算是否可以偿还银行间借款状态
    BB.Li_P[BB.is_enabled_LiP] = BB.Shock_P_run_s[BB.is_enabled_LiP]  # 计算银行收回厂商贷款流量
    Finance.update_finance_variables(BB, IB, b, ib, by_way='Li_P')

    Finance.update_finance_variables(BB, IB, b, ib, by_way='enabled repay Z_D')  # 计算是否需要偿还借款状态
    Finance.update_finance_variables(BB, IB, b, ib, by_way='enabled repay IB')  # 计算是否可以收回厂商贷款状态
    BB.Bo_all[BB.is_enabled_BoIB | BB.is_enabled_BoD] = np.minimum(BB.A_Q[BB.is_enabled_BoIB | BB.is_enabled_BoD], BB.Shock_run_t[BB.is_enabled_BoIB | BB.is_enabled_BoD])  # 计算银行偿还借款总流量 #BUG
    BB.Bo_D[BB.is_enabled_BoIB | BB.is_enabled_BoD] = BB.Shock_D_run_t[BB.is_enabled_BoIB | BB.is_enabled_BoD] * (BB.Bo_all[BB.is_enabled_BoIB | BB.is_enabled_BoD] / BB.Shock_run_t[BB.is_enabled_BoIB | BB.is_enabled_BoD])  # 计算银行偿还居民借款流量
    BB.Bo_IB_all[BB.is_enabled_BoIB | BB.is_enabled_BoD] = BB.Shock_IB_run_ilq_t[BB.is_enabled_BoIB | BB.is_enabled_BoD] * (BB.Bo_all[BB.is_enabled_BoIB | BB.is_enabled_BoD] / BB.Shock_run_t[BB.is_enabled_BoIB | BB.is_enabled_BoD])  # 计算银行偿还银行间借款流量
    Finance.update_finance_variables(BB, IB, b, ib, by_way='Bo_D')  # HACK 这个必须放在这里！
    Finance.update_finance_variables(BB, IB, b, ib, by_way='Bo_IB_all')
    for i in np.where(BB.is_enabled_BoIB)[0]:  # 计算银行可以偿还各债权银行的借款流量
        IB.Bo_IB[i, IB.cre_ilq[i]] = IB.Shock_IB_run_ilq[i, IB.cre_ilq[i]] * (BB.Bo_IB_all[i] / BB.Shock_IB_run_ilq_t[i])
        pass
    Finance.update_finance_variables(BB, IB, b, ib, by_way='Bo_IB')

    return BB, IB
    pass  # method
