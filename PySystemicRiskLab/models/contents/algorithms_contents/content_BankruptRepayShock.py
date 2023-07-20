"""破产银行应偿还负债冲击算法"""  # HACK冗余，可以替代以？

from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial, SystemicRiskAgent
from PySystemicRiskLab.core.define.define_type import StateType

pass  # end import


# from PySystemicRiskLab.models_entities.algorithms_contents import *

def content_BankruptRepayShock(A: SystemicRiskAgent, para: dict, env: dict):
    ## # 破产银行遭受偿还冲击

    BankState.update_states(way='bankrupt')
    # BankState.update_B_state(A.BB, A.IB, target='bankrupt', source='any') #FIXME
    A.BB.Shock_D_run_t[A.BB.br] = A.BB.Z_D[A.BB.br]  # 计算破产银行遭受偿还居民存款冲击
    A.BB.Shock_IB_t[A.BB.br] = A.BB.Z_IB_all[A.BB.br]  # 计算破产银行遭受偿还银行间负债冲击

    return A, env
    pass  # method
