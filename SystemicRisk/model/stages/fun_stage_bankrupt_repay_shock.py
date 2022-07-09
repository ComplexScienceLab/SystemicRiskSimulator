## 函数：破产银行应偿还负债冲击阶段

##########################################
# 状态/开发
##########################################

"函数：破产银行应偿还负债冲击阶段"  # HACK冗余，可以替代以

import numpy as np

from SystemicRisk.core.define.define_type import TypeState
from SystemicRisk.core.define.define_agents import BankInterbank, BankCommercial
from SystemicRisk.core.functions.fun_state import BankState
pass  # end import



# from SystemicRisk.model.stages import *

def stage_bankrupt_repay_shock(BB: BankCommercial, BI: BankInterbank, b: TypeState, ib: TypeState, para: dict, env: dict):
    ## # 破产银行遭受偿还冲击
    # @testprintln "开始阶段$(env['stage_name'])："

    BankState.update_B_state(BB, BI, target="bankrupt", source="any")
    BB.Shock_D_run_t[BB.br] = BB.Zm_D[BB.br]  # 计算破产银行遭受偿还居民存款冲击
    BB.Shock_BI_t[BB.br] = BB.Z_BI_all[BB.br]  # 计算破产银行遭受偿还银行间负债冲击

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass  # functions
