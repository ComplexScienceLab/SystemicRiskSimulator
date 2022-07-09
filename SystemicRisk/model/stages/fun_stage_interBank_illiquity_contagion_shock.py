## 函数：流动性短缺银行间挤兑流动传染冲击阶段

##########################################
# 状态/使用
##########################################

import numpy as np

from SystemicRisk.core.define.define_type import TypeState
from SystemicRisk.core.define.define_agents import BankInterbank, BankCommercial
from SystemicRisk.core.functions.fun_state import BankState
from SystemicRisk.core.functions.fun_shock import Shock
from SystemicRisk.core.functions.fun_balanceSheet import BalanceSheet
pass  # end import

"函数：流动性短缺银行间挤兑流动传染冲击阶段"


def stage_interBank_illiquity_contagion_shock(self, BB: BankCommercial, BI: BankInterbank, b: TypeState, ib: TypeState, para: dict, env: dict):
    ## # 流动性短缺银行间挤兑流动传染冲击
    # env['stage_name'] = "流动性短缺银行间挤兑流动传染冲击阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    ##BUG 方式一：每个银行只有一次分配传染冲击之行为。
    i_nas = (BB.ilq & ~BB.isAllocatedShock)  # 临时设置示性变量，表示银行其未分配传染冲击。暨每个银行只有一次分配传染冲击之行为。
    BB.Shock_BI_run_ilq_s[i_nas] = abs((BB.Shock_run_t[i_nas] - BB.A_Q[i_nas]) / (BB.A_P[i_nas] + BB.A_BI_all[i_nas]) * BB.A_BI_all[i_nas])  # 计算应银行内冲击传导至银行间传染冲击
    Shock.update_B_Shock(BB, BI, b, ib, byWay="Shock_BI_run_ilq_s")  # 更新挤兑流动冲击源头变量Shock_run_t
    BB.Shock_P_run_s[i_nas] = abs((BB.Shock_run_t[i_nas] - BB.A_Q[i_nas]) / (BB.A_P[i_nas] + BB.A_BI_all[i_nas]) * BB.A_P[i_nas])  # 银行内冲击传导至银行厂商贷款传染冲击
    BB.isAllocatedShock |= BB.ilq  # 更新已经分配传染冲击的银行
    for i in np.where(i_nas):  # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
        BI.Shock_BI_run_ilq[BI.deb[i], i] = BI.A_BI[i, BI.deb[i]] * BB.Shock_BI_run_ilq_s[i] / BB.A_BI_all[i]
        pass
    Shock.update_B_Shock(BB, BI, b, ib, byWay="Shock_BI_run_ilq")  # 更新挤兑流动冲击源头变量Shock_run_t
    BankState.update_B_state(BB, BI, target="illiquity", source="healthy")

    # ##BUG 方式二：每个银行可以有多次分配传染冲击之行为。
    # BB.Shock_BI_run_ilq_s[BB.ilq] = abs((BB.Shock_run_t[BB.ilq] - BB.A_Q[BB.ilq]) / (BB.A_P[BB.ilq] + BB.A_BI_all[BB.ilq]) * BB.A_BI_all[BB.ilq]) # 计算应银行内冲击传导至银行间传染冲击
    # update_B_Shock(BB, BI, b, ib, byWay = "Shock_BI_run_ilq_s") # 汇总各银行之流动性短缺流动性挤兑冲击
    # BB.Shock_P_run_s[BB.ilq] = abs((BB.Shock_run_t[BB.ilq] - BB.A_Q[BB.ilq]) / (BB.A_P[BB.ilq] + BB.A_BI_all[BB.ilq]) * BB.A_P[BB.ilq]) # 银行内冲击传导至银行厂商贷款传染冲击
    # for i in findall(BB.on) # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
    #     BI.Shock_BI_run_ilq[BI.deb[i], i] = BI.A_BI[i, BI.deb[i]] * BB.Shock_BI_run_ilq_s[i] / BB.A_BI_all[i]
    #     pass
    # update_B_Shock(BB, BI, b, ib, byWay = "Shock_BI_run_ilq") # 加总各单个债务银行遭受总银行间挤兑流动冲击
    # update_B_state(BB, BI, target = "illiquity", source = "healthy") # 更新各银行之状态，从健康到流动性短缺

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass  # functions
