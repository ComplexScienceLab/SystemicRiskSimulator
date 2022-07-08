## 函数：银行外部挤兑流动冲击阶段

##########################################
# 状态/使用
##########################################

import numpy as np

from SystemicRisk.core.define.define_type import TypeState
from SystemicRisk.core.define.define_agents import BankInterbank, BankCommercial
from SystemicRisk.core.functions.fun_state import BankState
from SystemicRisk.core.functions.fun_shock import Shock
pass  # end import


"函数：银行外部挤兑流动冲击阶段"


def stage_exBank_illiquity_shock(self, BB: BankCommercial, BI: BankInterbank, b: TypeState, ib: TypeState, para: dict, env: dict):  # = BB_t1:BankCommercial, BI_t1:BankInterbank,  =#:
    ## # 银行外部挤兑流动冲击阶段
    # env['stage_name'] = "银行外部挤兑流动冲击阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    BB.Shock_D_run_t[para['list_Shock_exBI_t']] = para['Shock_exBI_run_t'][para['list_Shock_exBI_t']]  # 生成居民存款挤兑流动冲击
    Shock.update_B_Shock(BB, BI, b, ib, byWay="Shock_D_run_t")  # 居民存款挤兑流动冲击传导至银行内负债冲击
    BankState.update_B_state(BB, BI, target="illiquity", source="healthy")  # 更新各银行之状态，从健康到流动性短缺

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass  # functions
