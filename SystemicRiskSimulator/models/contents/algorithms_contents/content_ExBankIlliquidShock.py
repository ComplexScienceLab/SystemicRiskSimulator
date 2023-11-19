"""银行存款挤兑流动冲击算法"""

from SystemicRiskSimulator import np
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.operations.executer import Executer

pass  # end import


def content_ExBankIlliquidShock(A: SystemicRiskAgent, para: dict, env: dict):  # = BB_t1:BankCommercial, IB_t1:BankInterbank,  =#:
    """
    银行存款挤兑流动冲击算法

    Args:
        A ():
        para ():
        env ():

    Returns:

    """

    # env['stage_name'] = "银行存款挤兑流动冲击算法"

    A.BB.Shock_D_run_t = A.BB.Z_D * np.array([para['Shock_exIB_run_t_percentage']]).T  # 生成居民存款挤兑流动冲击
    Executer.step_update('Shock_D_run_t', A, para, env)  # 居民存款挤兑流动冲击传导至银行内资产冲击
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_D_run_t')  # 居民存款挤兑流动冲击传导至银行内资产冲击
    A.BB.Shock_IB_run_ilq_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_IB_all[A.BB.ilq])  # 计算应银行内冲击传导至银行间传染冲击
    Executer.step_update('Shock_IB_run_ilq_s', A, para, env)  # 更新挤兑流动冲击源头变量Shock_run_t
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq_s')  # 更新挤兑流动冲击源头变量Shock_run_t
    A.BB.Shock_P_run_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_P[A.BB.ilq])  # 银行内冲击传导至银行厂商贷款传染冲击
    A.BB.is_allocated_Shock |= A.BB.ilq  # 更新已经分配传染冲击的银行
    for i in np.where(A.BB.ilq)[0]:  # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
        A.IB.Shock_IB_run_ilq[A.IB.deb_ilq[i], i] = A.IB.A_IB[i, A.IB.deb_ilq[i]] * A.BB.Shock_IB_run_ilq_s[i] / A.BB.A_IB_all[i]
        pass
    Executer.step_update('Shock_IB_run_ilq', A, para, env)  # 更新挤兑流动冲击源头变量Shock_run_t

    return A, env
    pass  # method
