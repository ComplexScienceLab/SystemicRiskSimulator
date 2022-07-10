## 函数：银行间挤兑流动分配借贷流量阶段

##########################################
#状态/使用
##########################################

import numpy as np

from PySystemicRiskLab.core.define.define_type import TypeState
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.functions.fun_state import BankState
from PySystemicRiskLab.core.functions.fun_transfer import BankTransfer
pass  # end import


"函数：银行间挤兑流动分配借贷流量阶段"
def stage_interBank_illiquity_allocate(self, BB:BankCommercial, BI:BankInterbank, b:TypeState, ib:TypeState, para:dict,env:dict):
    ## # 流动性短缺银行间挤兑流动分配借贷流量阶段
    # env['stage_name'] = "银行间挤兑流动分配借贷流量阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    BankState.update_B_state(BB, BI, target = "needed collect A_P", source = "any")
    BankState.update_B_state(BB, BI, target = "enabled collect A_P", source = "any")
    BB.Li_P[BB.eLiP] = BB.Shock_P_run_s[BB.eLiP] # 计算银行收回厂商贷款流量
    BankTransfer.update_B_transfer(BB, BI, b, ib, byWay = "Li_P")

    BankState.update_B_state(BB, BI, target = "needed repay Z_D", source = "any")
    BankState.update_B_state(BB, BI, target = "enabled repay Z_D", source = "any")
    BankState.update_B_state(BB, BI, target = "needed repay BI", source = "any")
    BankState.update_B_state(BB, BI, target = "enabled repay BI", source = "any")
    BB.Bo_all[BB.eBoBI|BB.eBoD] = min(BB.A_Q[BB.eBoBI|BB.eBoD], BB.Shock_run_t[BB.eBoBI|BB.eBoD]) # 计算银行偿还借款总流量
    BB.Bo_D[BB.eBoBI|BB.eBoD] = BB.Shock_D_run_t[BB.eBoBI|BB.eBoD] * (BB.Bo_all[BB.eBoBI|BB.eBoD] / BB.Shock_run_t[BB.eBoBI|BB.eBoD]) # 计算银行偿还居民借款流量
    BB.Bo_BI_all[BB.eBoBI|BB.eBoD] = BB.Shock_BI_run_ilq_t[BB.eBoBI|BB.eBoD] * (BB.Bo_all[BB.eBoBI|BB.eBoD] / BB.Shock_run_t[BB.eBoBI|BB.eBoD]) # 计算银行偿还银行间借款流量
    BankTransfer.update_B_transfer(BB, BI, b, ib, byWay = "Bo_D") #HACK 这个必须放在这里！
    BankTransfer.update_B_transfer(BB, BI, b, ib, byWay = "Bo_BI_all")
    for i in np.where(BB.eBoBI): # 计算银行偿还各债权银行借款流量
        BI.Bo_BI[i, BI.cre[i]] = BI.Shock_BI_run_ilq[i, BI.cre[i]] * (BB.Bo_BI_all[i] / BB.Shock_BI_run_ilq_t[i])
        pass
    BankTransfer.update_B_transfer(BB, BI, b, ib, byWay = "Bo_BI")

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass # functions
