"""破产银行应偿还负债冲击算法""" # HACK冗余，可以替代以？



from PySystemicRiskLab import logging
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_state import BankState

pass  # end import



# from PySystemicRiskLab.models_entities.algorithms_contents import *

def content_BankruptRepayShock(BB: BankCommercial, BI: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 破产银行遭受偿还冲击
    
    BankState.update_B_state(BB, BI, target='bankrupt', source='any')
    BB.Shock_D_run_t[BB.br] = BB.Z_D[BB.br]  # 计算破产银行遭受偿还居民存款冲击
    BB.Shock_BI_t[BB.br] = BB.Z_BI_all[BB.br]  # 计算破产银行遭受偿还银行间负债冲击

    return BB, BI
    pass  # method
