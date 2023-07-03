"""外部资产违约损失冲击"""

from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank, SystemicRiskAgent
from PySystemicRiskLab.core.define.define_type import StateType
# from PySystemicRiskLab.core.functions.fun_finance import Finance
from PySystemicRiskLab.core.operations.executer import Executer
from PySystemicRiskLab.core.operations.scheduler import Scheduler

pass  # end import


def content_ExBankInsolventShock(A: SystemicRiskAgent, para: dict, env: dict):
    ## # 外部资产违约损失冲击算法
    # env['stage_name'] = "外部资产违约损失冲击算法"

    # NOW 改成每执行一步都搜集数据
    A.BB.Shock_P_def_t = A.BB.A_P * np.array([para['Shock_exIB_def_t_percentage']]).T  # 生成厂商贷款违约损失冲击
    # env['update']
    env = Executer.step_update('Shock_P_def_t', A, para, env)  # 厂商贷款违约损失冲击传导至银行内资产冲击
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_P_def_t')
    A.BB.A_P[A.b] = np.maximum(A.BB.A_P[A.b] - A.BB.Shock_P_def_t[A.b], 0.0)  # 银行之非银行间资产变动
    env = Executer.step_update('A_P', A, para, env)  # 厂商贷款违约损失冲击传导至银行内资产冲击
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_P')  # 厂商贷款违约损失冲击传导至银行内资产冲击

    return A.BB, A.IB
    pass  # method
