"""外生破产银行间挤兑流动冲击算法"""

##########################################
#状态/开发
##########################################

from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_finance import Finance
pass  # end import



# TODO"外生破产银行间挤兑流动冲击算法"
def content_ExBankBankruptContagion(BB: BankCommercial, IB: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 外生破产银行间挤兑流动传染
    # env['stage_name'] = "外生破产银行间挤兑流动冲击算法"
    
    BB.br[para['list_Shock_exIB_t']] = para['Shock_exIB_t'][para['list_Shock_exIB_t']]
    Finance.update_finance_variables(BB, IB, b, ib, by_way='bankrupt')

    return BB, IB

    pass  # method
