"""银行间挤兑流动分配借贷流量算法"""

##########################################
# 状态/使用
##########################################

from PySystemicRiskLab import np, logging
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_state import BankState
from PySystemicRiskLab.core.functions.fun_transfer import BankTransfer

pass  # end import


def algorithmContent_InterBankIlliquidAllocate(BB: BankCommercial, BI: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 流动性短缺银行间挤兑流动分配借贷流量算法
    # env['stage_name'] = "银行间挤兑流动分配借贷流量算法"

    BankState.update_B_state(BB, BI, target='needed collect A_P', source='any')
    BankState.update_B_state(BB, BI, target='enabled collect A_P', source='any')
    BB.Li_P[BB.is_enabled_LiP] = BB.Shock_P_run_s[BB.is_enabled_LiP]  # 计算银行收回厂商贷款流量
    BankTransfer.update_B_transfer(BB, BI, b, ib, by_way="Li_P")

    BankState.update_B_state(BB, BI, target='needed repay Z_D', source='any')
    BankState.update_B_state(BB, BI, target='enabled repay Z_D', source='any')
    BankState.update_B_state(BB, BI, target='needed repay BI', source='any')
    BankState.update_B_state(BB, BI, target='enabled repay BI', source='any')
    BB.Bo_all[BB.is_enabled_BoBI | BB.is_enabled_BoD] = np.minimum(BB.A_Q[BB.is_enabled_BoBI | BB.is_enabled_BoD], BB.Shock_run_t[BB.is_enabled_BoBI | BB.is_enabled_BoD])  # 计算银行偿还借款总流量
    BB.Bo_D[BB.is_enabled_BoBI | BB.is_enabled_BoD] = BB.Shock_D_run_t[BB.is_enabled_BoBI | BB.is_enabled_BoD] * (BB.Bo_all[BB.is_enabled_BoBI | BB.is_enabled_BoD] / BB.Shock_run_t[BB.is_enabled_BoBI | BB.is_enabled_BoD])  # 计算银行偿还居民借款流量
    BB.Bo_BI_all[BB.is_enabled_BoBI | BB.is_enabled_BoD] = BB.Shock_BI_run_ilq_t[BB.is_enabled_BoBI | BB.is_enabled_BoD] * (BB.Bo_all[BB.is_enabled_BoBI | BB.is_enabled_BoD] / BB.Shock_run_t[BB.is_enabled_BoBI | BB.is_enabled_BoD])  # 计算银行偿还银行间借款流量
    BankTransfer.update_B_transfer(BB, BI, b, ib, by_way="Bo_D")  # HACK 这个必须放在这里！
    BankTransfer.update_B_transfer(BB, BI, b, ib, by_way="Bo_BI_all")
    for i in np.where(BB.is_enabled_BoBI)[0]:  # 计算银行偿还各债权银行借款流量
        BI.Bo_BI[i, BI.cre_ilq[i]] = BI.Shock_BI_run_ilq[i, BI.cre_ilq[i]] * (BB.Bo_BI_all[i] / BB.Shock_BI_run_ilq_t[i])
        pass
    BankTransfer.update_B_transfer(BB, BI, b, ib, by_way="Bo_BI")

    return BB, BI
    pass  # method
