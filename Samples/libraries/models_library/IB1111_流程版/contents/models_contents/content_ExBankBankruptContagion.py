"""外生破产银行间挤兑流动冲击模型"""

##########################################
# 状态/开发
##########################################

from SystemicRiskSimulator.core.define.define_agents import BankInterbank, BankCommercial, SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_type import StateType
# from SystemicRiskSimulator.core.functions.fun_finance import Finance
from SystemicRiskSimulator.core.operations.executer import Executer
pass  # end import


# TODO"外生破产银行间挤兑流动冲击模型"
def content_ExBankBankruptContagion(A: SystemicRiskAgent, para: dict, env: dict):
    ## # 外生破产银行间挤兑流动传染
    # env['stage_name'] = "外生破产银行间挤兑流动冲击模型"

    A.BB.br[para['list_Shock_exIB_t']] = para['Shock_exIB_t'][para['list_Shock_exIB_t']]
    Executer.step_update('bankrupt', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='bankrupt')

    return A, env

    pass  # function
