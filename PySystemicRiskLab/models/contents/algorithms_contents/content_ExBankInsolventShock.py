"""外部资产违约损失冲击"""

from PySystemicRiskLab import np, logging
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_finance import Finance
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState

pass  # end import


def content_ExBankInsolventShock(BB: BankCommercial, IB: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 外部资产违约损失冲击算法
    # env['stage_name'] = "外部资产违约损失冲击算法"

    # TODO BUG新的
    BB.Shock_P_def_t = BB.A_P * np.array([para['Shock_exIB_def_t_percentage']]).T  # 生成厂商贷款违约损失冲击
    Finance.update_variables(BB, IB, b, ib, by_way='Shock_P_def_t')  # 厂商贷款违约损失冲击传导至银行内资产冲击
    # Shock.update_B_Shock(BB, IB, b, ib, by_way='Shock_P_def_t')  # 厂商贷款违约损失冲击传导至银行内资产冲击
    BB.A_P[b] = np.maximum(BB.A_P[b] - BB.Shock_P_def_t[b], 0.0)  # 银行之非银行间资产变动
    Finance.update_variables(BB, IB, b, ib, by_way='A_P')  # 厂商贷款违约损失冲击传导至银行内资产冲击
    # BalanceSheet.update_B_balance_sheet(BB, IB, b, ib, by_way='A_P')
    # BankState.update_states(way='insolvent')
    # BankState.update_B_state(BB, IB, target='insolvent', source='healthy') #FIXME

    # BUG原来的
    # BB.Shock_P_def_t = BB.A_P * np.array([para['Shock_exIB_def_t_percentage']]).T  # 生成厂商贷款违约损失冲击
    # Shock.update_B_Shock(BB, IB, b, ib, by_way='Shock_P_def_t')  # 厂商贷款违约损失冲击传导至银行内资产冲击
    # # BB.A_P[b] -= BB.Shock_def_t[b]  # 银行之非银行间资产变动
    # BB.A_P[b] = np.maximum(BB.A_P[b] - BB.Shock_P_def_t[b], 0.0)  # 银行之非银行间资产变动
    # BalanceSheet.update_B_balance_sheet(BB, IB, b, ib, by_way='A_P')
    # BankState.update_states(way='insolvent')
    # # BankState.update_B_state(BB, IB, target='insolvent', source='healthy') #FIXME


    return BB, IB
    pass  # method
