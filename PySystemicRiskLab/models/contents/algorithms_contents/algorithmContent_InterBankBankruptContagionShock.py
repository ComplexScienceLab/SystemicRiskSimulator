"""破产银行间挤兑流动传染冲击算法"""



from PySystemicRiskLab import logging, np, pd
# from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState

pass  # end import



def algorithmContent_InterBankBankruptContagionShock(BB: pd.Series, BI: pd.Series, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 破产银行间挤兑流动传染冲击
    # env['stage_name'] = "破产银行间挤兑流动传染冲击算法"
    
    BankState.update_B_state(BB, BI, target='bankrupt', source='any')
    BB.Shock_BI_run_br_s[BB.br] = BB.A_BI_all[BB.br]  # 计算应银行内冲击传导至银行间传染冲击
    Shock.update_B_Shock(BB, BI, b, ib, by_way='Shock_BI_run_br_s')  # 更新挤兑流动冲击源头变量Shock_run_s
    BB.Shock_P_run_s[BB.br] = BB.A_P[BB.br]  # 银行内冲击传导至银行厂商贷款传染冲击
    for i in np.where(BB.br)[0]:  # 破产银行计划收回资产，导致其对各债务银行之资产变动，造成破产银行间挤兑流动冲击
        BI.Shock_BI_run_br[BI.deb[i], i] = BI.A_BI[i, BI.deb[i]]
        pass
    Shock.update_B_Shock(BB, BI, b, ib, by_way='Shock_BI_run_br')  # 更新挤兑流动冲击目标变量Shock_run_t
    BankState.update_B_state(BB, BI, target='bankrupt', source='any')

    return BB, BI
    pass  # method
