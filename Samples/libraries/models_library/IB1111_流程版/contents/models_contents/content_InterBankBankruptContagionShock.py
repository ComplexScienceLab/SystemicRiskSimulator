"""破产银行间挤兑流动传染冲击模型"""

from SystemicRiskSimulator import np
from SystemicRiskSimulator.core.define.define_agents import BankInterbank, BankCommercial, SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_type import StateType

pass  # end import


def content_InterBankBankruptContagionShock(A: SystemicRiskAgent, para: dict, sgv: dict):
    ## # 破产银行间挤兑流动传染冲击
    # sgv['stage_name'] = "破产银行间挤兑流动传染冲击模型"

    BankState.update_states(way='any')
    # BankState.update_B_state(A.BB, A.IB, target='bankrupt', source='any') #FIXME
    A.BB.Shock_IB_run_br_s[A.BB.br] = A.BB.A_IB_all[A.BB.br]  # 计算应银行内冲击传导至银行间传染冲击
    Shock.update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_br_s')  # 更新挤兑流动冲击源头变量Shock_run_s
    A.BB.Shock_P_run_s[A.BB.br] = A.BB.A_P[A.BB.br]  # 银行内冲击传导至银行厂商贷款传染冲击
    for i in np.where(A.BB.br)[0]:  # 破产银行计划收回资产，导致其对各债务银行之资产变动，造成破产银行间挤兑流动冲击
        A.IB.Shock_IB_run_br[A.IB.deb[i], i] = A.IB.A_IB[i, A.IB.deb[i]]
        pass
    Shock.update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_br')  # 更新挤兑流动冲击目标变量Shock_run_t
    BankState.update_states(way='bankrupt')
    # BankState.update_B_state(A.BB, A.IB, target='bankrupt', source='any') #FIXME

    return A, sgv
    pass  # function
