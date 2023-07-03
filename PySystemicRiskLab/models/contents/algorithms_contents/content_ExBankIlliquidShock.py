"""银行存款挤兑流动冲击算法"""

from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial, SystemicRiskAgent
from PySystemicRiskLab.core.define.define_type import StateType
# from PySystemicRiskLab.core.functions.fun_finance import Finance
from PySystemicRiskLab.core.operations.executer import Executer

pass  # end import


def content_ExBankIlliquidShock(A: SystemicRiskAgent, para: dict, env: dict):  # = BB_t1:BankCommercial, IB_t1:BankInterbank,  =#:
    ## # 银行存款挤兑流动冲击算法
    # env['stage_name'] = "银行存款挤兑流动冲击算法"

    A.BB.Shock_D_run_t = A.BB.Z_D * np.array([para['Shock_exIB_run_t_percentage']]).T  # 生成居民存款挤兑流动冲击
    Executer.step_update('Shock_D_run_t', A, para, env)  # 居民存款挤兑流动冲击传导至银行内资产冲击
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_D_run_t')  # 居民存款挤兑流动冲击传导至银行内资产冲击

    return A.BB, A.IB
    pass  # method
