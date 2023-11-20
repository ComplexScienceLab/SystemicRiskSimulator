"""外部资产违约损失冲击"""

from SystemicRiskSimulator import np
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.operations.executer import Executer

pass  # end import


def content_ExBankInsolventShock(A: SystemicRiskAgent, para: dict, env: dict):
    """
    外部资产违约损失冲击算法

    Args:
        A ():
        para ():
        env ():

    Returns:

    """

    # env['stage_name'] = "外部资产违约损失冲击算法"

    A.BB.Shock_P_def_t = A.BB.A_P * np.array([para['Shock_exIB_def_t_percentage']]).T  # 生成厂商贷款违约损失冲击
    Executer.step_update('Shock_P_def_t', A, para, env)  # 厂商贷款违约损失冲击传导至银行内资产冲击
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_P_def_t')
    A.BB.A_P[A.BB.on] = np.maximum(A.BB.A_P[A.BB.on] - A.BB.Shock_P_def_t[A.BB.on], 0.0)  # 银行之非银行间资产变动
    Executer.step_update('A_P', A, para, env)  # 厂商贷款违约损失冲击传导至银行内资产冲击
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_P')  # 厂商贷款违约损失冲击传导至银行内资产冲击
    A.BB.E_all[A.BB.on] = np.maximum(A.BB.E_all[A.BB.on] - A.BB.Shock_def_t[A.BB.on], 0.0)  # 银行之所有者权益变动
    A.BB.Shock_IB_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_IB_all[A.BB.isv])  # 计算应银行内冲击传导至银行间传染冲击
    Executer.step_update('Shock_IB_def_s', A, para, env)  # 更新违约损失冲击源头变量Shock_def_s
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_def_s')  # 更新违约损失冲击源头变量Shock_def_s
    A.BB.Shock_D_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_D[A.BB.isv])  # 计算应银行内冲击传导至银行存款传染冲击
    Executer.step_update('Shock_D_def_s', A, para, env)  # 更新违约损失冲击源头变量Shock_def_s #BUG
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_D_def_s')  # 更新违约损失冲击源头变量Shock_def_s #BUG
    A.BB.Z_IB_all[A.BB.isv] -= A.BB.Shock_IB_def_s[A.BB.isv]  # 银行间负债变动，由于违约
    Executer.step_update('Z_IB_all', A, para, env)  # 更新资产负债表，通过Z_D或Z_IB_all
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_IB_all')  # 更新资产负债表，通过Z_D或Z_IB_all
    A.BB.Z_D[A.BB.isv] -= A.BB.Shock_D_def_s[A.BB.isv]  # 存款负债变动，由于违约
    Executer.step_update('Z_D', A, para, env)  # 更新资产负债表，通过Z_D或Z_IB_all
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_D')  # 更新资产负债表，通过Z_D或Z_IB_all

    return A, env
    pass  # function
