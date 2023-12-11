"""银行间挤兑流动执行借贷流量模型"""

from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.functions.fun_finance import Finance
from SystemicRiskSimulator.core.operations.executer import Executer

pass  # end import


def content_InterBankIlliquidRepay(A: SystemicRiskAgent, para: dict, sgv: dict):
    """
    流动性短缺银行间挤兑流动执行借贷流量模型

    Args:
        A ():
        para ():
        sgv ():

    Returns:

    """

    # sgv['stage_name'] = "流动性短缺银行间挤兑流动执行借贷流量模型"

    A.BB.A_Q[A.b], A.BB.A_P[A.b], A.BB.Shock_P_run_s[A.b] = Finance.transfer_B_capital_reverse(A.BB.A_Q[A.b], A.BB.A_P[A.b], A.BB.Shock_P_run_s[A.b], A.BB.Li_P[A.b])  # 流动资产变动，因收回厂商贷款
    # A.BB.A_Q[A.b] *= (1 - paras['kappa_A_P']) #HACK 暂时还不用！
    Executer.step_update('A_Q', A, para, sgv)
    Executer.step_update('A_P', A, para, sgv)
    Executer.step_update('Shock_P_run_s', A, para, sgv)

    A.BB.Z_D[A.b], A.BB.A_Q[A.b], A.BB.Shock_D_run_t[A.b] = Finance.transfer_B_capital_reduce(A.BB.Z_D[A.b], A.BB.A_Q[A.b], A.BB.Shock_D_run_t[A.b], A.BB.Bo_D[A.b])  # 流动资产变动，因偿还居民存款
    Executer.step_update('Z_D', A, para, sgv)
    Executer.step_update('A_Q', A, para, sgv)
    Executer.step_update('Shock_D_run_t', A, para, sgv)

    A.IB.Shock_IB_run_ilq[A.ib] -= A.IB.Bo_IB[A.ib]  # 各银行间挤兑流动冲击变动，当偿还相应的银行间借款时
    Executer.step_update('Shock_IB_run_ilq', A, para, sgv)
    A.BB.Shock_IB_run_ilq_s[A.b] -= A.BB.Li_IB_all[A.b]  # 各银行之银行间挤兑流动冲击源头变动，当收回相应的银行间贷款时
    Executer.step_update('Shock_IB_run_ilq_s', A, para, sgv)
    A.IB.Z_IB[A.ib] -= A.IB.Bo_IB[A.ib]  # 各银行间负债变动，当偿还相应的银行间借款时
    Executer.step_update('Z_IB', A, para, sgv)
    # # A.IB.A_IB[A.ib] += A.IB.Li_IB[A.ib]' # 各银行间资产变动，当收回相应的银行间贷款时
    A.BB.A_Q[A.b] += (A.BB.Li_IB_all[A.b] - A.BB.Bo_IB_all[A.b])  # 各银行流动资金变动，当收回相应的银行间贷款、偿还相应的银行间借款时
    Executer.step_update('A_Q', A, para, sgv)

    Executer.step_update('clear transfer all', A, para, sgv)  # 清零所有不必要的借贷流量变量；#BUG这个是否有必要？

    return A, sgv
    pass  # function
