"""外部资产违约损失冲击"""

from SystemicRiskSimulator.external_packages import np
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.operations.executer import Executer

pass  # end import


def content_ExBankInsolventShock(A: SystemicRiskAgent, para: dict, sgv: dict):
    """
    外部资产违约损失冲击模型

    Args:
        A ():
        para ():
        sgv ():

    Returns:

    """

    # sgv['stage_name'] = "外部资产违约损失冲击模型"

    A.BB.Shock_P_def_t = A.BB.A_P * np.array([para['Shock_exIB_def_t_percentage']]).T  # 生成厂商贷款违约损失冲击
    Executer.step_update('Shock_P_def_t', A, para, sgv)  # 厂商贷款违约损失冲击传导至银行内资产冲击
    A.BB.A_P[A.BB.on] = np.maximum(A.BB.A_P[A.BB.on] - A.BB.Shock_P_def_t[A.BB.on], 0.0)  # 银行之非银行间资产变动
    Executer.step_update('A_P', A, para, sgv)  # 厂商贷款违约损失冲击传导至银行内资产冲击
    A.BB.E_all[A.BB.on] = np.maximum(A.BB.E_all[A.BB.on] - A.BB.Shock_def_t[A.BB.on], 0.0)  # 银行之所有者权益变动
    A.BB.Shock_IB_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_IB_all[A.BB.isv])  # 计算应银行内冲击传导至银行间传染冲击
    Executer.step_update('Shock_IB_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s
    A.BB.Shock_D_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_D[A.BB.isv])  # 计算应银行内冲击传导至银行存款传染冲击
    Executer.step_update('Shock_D_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s #BUG
    A.BB.Z_IB_all[A.BB.isv] -= A.BB.Shock_IB_def_s[A.BB.isv]  # 银行间负债变动，由于违约
    Executer.step_update('Z_IB_all', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all
    A.BB.Z_D[A.BB.isv] -= A.BB.Shock_D_def_s[A.BB.isv]  # 存款负债变动，由于违约
    Executer.step_update('Z_D', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all

    return A, sgv
    pass  # function
