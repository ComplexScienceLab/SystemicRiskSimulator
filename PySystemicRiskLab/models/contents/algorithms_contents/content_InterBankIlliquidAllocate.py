"""银行间挤兑流动分配借贷流量算法"""

##########################################
# 状态/使用
##########################################

from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial, SystemicRiskAgent
from PySystemicRiskLab.core.define.define_type import StateType
# from PySystemicRiskLab.core.functions.fun_finance import Finance
from PySystemicRiskLab.core.operations.executer import Executer

pass  # end import


def content_InterBankIlliquidAllocate(A: SystemicRiskAgent, para: dict, env: dict):
    ## # 流动性短缺银行间挤兑流动分配借贷流量算法

    Executer.step_update('enabled collect A_P', A, para, env)  # 计算是否可以偿还银行间借款状态
# Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='enabled collect A_P')  # 计算是否可以偿还银行间借款状态
    A.BB.Li_P[A.BB.is_enabled_LiP] = A.BB.Shock_P_run_s[A.BB.is_enabled_LiP]  # 计算银行收回厂商贷款流量
    Executer.step_update('Li_P', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Li_P')

    Executer.step_update('enabled repay Z_D', A, para, env)  # 计算是否需要偿还借款状态
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='enabled repay Z_D')  # 计算是否需要偿还借款状态
    Executer.step_update('enabled repay IB', A, para, env)  # 计算是否可以收回厂商贷款状态
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='enabled repay IB')  # 计算是否可以收回厂商贷款状态
    A.BB.Bo_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] = np.minimum(A.BB.A_Q[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD], A.BB.Shock_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD])  # 计算银行偿还借款总流量 #BUG
    A.BB.Bo_D[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] = A.BB.Shock_D_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] * (A.BB.Bo_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] / A.BB.Shock_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD])  # 计算银行偿还居民借款流量
    A.BB.Bo_IB_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] = A.BB.Shock_IB_run_ilq_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] * (A.BB.Bo_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] / A.BB.Shock_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD])  # 计算银行偿还银行间借款流量
    Executer.step_update('Bo_D', A, para, env)  # HACK 这个必须放在这里！
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Bo_D')  # HACK 这个必须放在这里！
    Executer.step_update('Bo_IB_all', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Bo_IB_all')
    for i in np.where(A.BB.is_enabled_BoIB)[0]:  # 计算银行可以偿还各债权银行的借款流量
        A.IB.Bo_IB[i, A.IB.cre_ilq[i]] = A.IB.Shock_IB_run_ilq[i, A.IB.cre_ilq[i]] * (A.BB.Bo_IB_all[i] / A.BB.Shock_IB_run_ilq_t[i])
        pass
    Executer.step_update('Bo_IB', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Bo_IB')

    return A.BB, A.IB
    pass  # method
