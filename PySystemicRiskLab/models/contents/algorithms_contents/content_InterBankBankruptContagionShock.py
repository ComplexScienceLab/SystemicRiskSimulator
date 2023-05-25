"""破产银行间挤兑流动传染冲击算法"""



from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState

pass  # end import



def content_InterBankBankruptContagionShock(BB: BankCommercial, IB: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 破产银行间挤兑流动传染冲击
    # env['stage_name'] = "破产银行间挤兑流动传染冲击算法"
    
    BankState.update_states(way='any')
    # BankState.update_B_state(BB, IB, target='bankrupt', source='any') #FIXME
    BB.Shock_IB_run_br_s[BB.br] = BB.A_IB_all[BB.br]  # 计算应银行内冲击传导至银行间传染冲击
    Shock.update_B_Shock(BB, IB, b, ib, by_way='Shock_IB_run_br_s')  # 更新挤兑流动冲击源头变量Shock_run_s
    BB.Shock_P_run_s[BB.br] = BB.A_P[BB.br]  # 银行内冲击传导至银行厂商贷款传染冲击
    for i in np.where(BB.br)[0]:  # 破产银行计划收回资产，导致其对各债务银行之资产变动，造成破产银行间挤兑流动冲击
        IB.Shock_IB_run_br[IB.deb[i], i] = IB.A_IB[i, IB.deb[i]]
        pass
    Shock.update_B_Shock(BB, IB, b, ib, by_way='Shock_IB_run_br')  # 更新挤兑流动冲击目标变量Shock_run_t
    BankState.update_states(way='bankrupt')
    # BankState.update_B_state(BB, IB, target='bankrupt', source='any') #FIXME

    return BB, IB
    pass  # method
