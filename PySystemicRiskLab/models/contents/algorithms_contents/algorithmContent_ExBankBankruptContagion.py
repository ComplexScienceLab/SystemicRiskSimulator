"""外生破产银行间挤兑流动冲击算法"""

##########################################
# 状态/暂时用不到
##########################################

from PySystemicRiskLab import logging, pd
# from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_state import BankState

pass  # end import


# TODO"外生破产银行间挤兑流动冲击算法"
def algorithmContent_ExBankBankruptContagion(BB: pd.Series, BI: pd.Series, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 外生破产银行间挤兑流动传染
    # env['stage_name'] = "外生破产银行间挤兑流动冲击算法"

    BB.br[para['list_Shock_exBI_t']] = para['Shock_exBI_t'][para['list_Shock_exBI_t']]
    BankState.update_B_state(BB, BI, target='bankrupt', source='any')

    return BB, BI

    pass  # method
