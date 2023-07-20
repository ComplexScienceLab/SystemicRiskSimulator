"""银行间挤兑流动执行借贷流量算法"""

from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial, SystemicRiskAgent
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_finance import Finance
from PySystemicRiskLab.core.operations.executer import Executer

pass  # end import


def content_InterBankIlliquidRepay(A: SystemicRiskAgent, para: dict, env: dict):
    ## # 流动性短缺银行间挤兑流动执行借贷流量算法
    # env['stage_name'] = "银行间挤兑流动执行借贷流量算法"

    A.BB.A_Q[A.b], A.BB.A_P[A.b], A.BB.Shock_P_run_s[A.b] = Finance.transfer_B_capital_reverse(A.BB.A_Q[A.b], A.BB.A_P[A.b], A.BB.Shock_P_run_s[A.b], A.BB.Li_P[A.b])  # 流动资产变动，因收回厂商贷款
    # A.BB.A_Q[A.b] *= (1 - paras['kappa_A_P']) #HACK 暂时还不用！
    Executer.step_update('A_Q', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_Q')
    Executer.step_update('A_P', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_P')
    Executer.step_update('Shock_P_run_s', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_P_run_s')

    A.BB.Z_D[A.b], A.BB.A_Q[A.b], A.BB.Shock_D_run_t[A.b] = Finance.transfer_B_capital_reduce(A.BB.Z_D[A.b], A.BB.A_Q[A.b], A.BB.Shock_D_run_t[A.b], A.BB.Bo_D[A.b])  # 流动资产变动，因偿还居民存款
    Executer.step_update('Z_D', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_D')
    Executer.step_update('A_Q', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_Q')
    Executer.step_update('Shock_D_run_t', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_D_run_t')

    A.IB.Shock_IB_run_ilq[A.ib] -= A.IB.Bo_IB[A.ib]  # 各银行间挤兑流动冲击变动，当偿还相应的银行间借款时
    Executer.step_update('Shock_IB_run_ilq', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq')
    A.BB.Shock_IB_run_ilq_s[A.b] -= A.BB.Li_IB_all[A.b]  # 各银行之银行间挤兑流动冲击源头变动，当收回相应的银行间贷款时
    Executer.step_update('Shock_IB_run_ilq_s', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq_s')
    A.IB.Z_IB[A.ib] -= A.IB.Bo_IB[A.ib]  # 各银行间负债变动，当偿还相应的银行间借款时
    Executer.step_update('Z_IB', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_IB')
    # # A.IB.A_IB[A.ib] += A.IB.Li_IB[A.ib]' # 各银行间资产变动，当收回相应的银行间贷款时
    A.BB.A_Q[A.b] += (A.BB.Li_IB_all[A.b] - A.BB.Bo_IB_all[A.b])  # 各银行流动资金变动，当收回相应的银行间贷款、偿还相应的银行间借款时
    Executer.step_update('A_Q', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_Q')

    Executer.step_update('clear transfer all', A, para, env)  # 清零所有不必要的借贷流量变量；#BUG这个是否有必要？
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='clear transfer all')  # 清零所有不必要的借贷流量变量；#BUG这个是否有必要？

    return A, env
    pass  # method
