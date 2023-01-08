"""银行间挤兑流动执行借贷流量算法"""


from PySystemicRiskLab import logging, pd
# from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState
from PySystemicRiskLab.core.functions.fun_transfer import BankTransfer

pass  # end import




def algorithmContent_InterBankIlliquidRepay(BB: pd.Series, BI: pd.Series, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 流动性短缺银行间挤兑流动执行借贷流量算法
    # env['stage_name'] = "银行间挤兑流动执行借贷流量算法"
    
    BB.A_Q[b], BB.A_P[b], BB.Shock_P_run_s[b] = BankTransfer.transfer_B_capital_reverse(BB.A_Q[b], BB.A_P[b], BB.Shock_P_run_s[b], BB.Li_P[b])  # 流动资产变动，因收回厂商贷款
    # BB.A_Q[b] *= (1 - paras['kappa_A_P']) #HACK 暂时还不用！
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='A_Q')
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='A_P')
    Shock.update_B_Shock(BB, BI, b, ib, by_way='Shock_P_run_s')

    BB.Z_D[b], BB.A_Q[b], BB.Shock_D_run_t[b] = BankTransfer.transfer_B_capital_reduce(BB.Z_D[b], BB.A_Q[b], BB.Shock_D_run_t[b], BB.Bo_D[b])  # 流动资产变动，因偿还居民存款
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='A_Q')
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='Z_D')
    Shock.update_B_Shock(BB, BI, b, ib, by_way='Shock_D_run_t')

    BI.Shock_BI_run_ilq[ib] -= BI.Bo_BI[ib]  # 各银行间挤兑流动冲击变动，当偿还相应的银行间借款时
    Shock.update_B_Shock(BB, BI, b, ib, by_way='Shock_BI_run_ilq')
    BB.Shock_BI_run_ilq_s[b] -= BB.Li_BI_all[b]  # 各银行之银行间挤兑流动冲击源头变动，当收回相应的银行间贷款时
    Shock.update_B_Shock(BB, BI, b, ib, by_way='Shock_BI_run_ilq_s')
    BI.Z_BI[ib] -= BI.Bo_BI[ib]  # 各银行间负债变动，当偿还相应的银行间借款时
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='sum Z_BI')
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='alter to A_BI from Z_BI')
    # BI.A_BI[ib] += BI.Li_BI[ib]' # 各银行间资产变动，当收回相应的银行间贷款时
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='sum A_BI')
    BB.A_Q[b] += (BB.Li_BI_all[b] - BB.Bo_BI_all[b])  # 各银行流动资金变动，当收回相应的银行间贷款、偿还相应的银行间借款时
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='A_Q')

    BankState.update_B_state(BB, BI, target='healthy', source='illiquid')  # 更新银行状态之流动性短缺的与健康的

    BankTransfer.update_B_transfer(BB, BI, b, ib, by_way='clear transfer all')  # 清零所有不必要的借贷流量变量；

    return BB, BI
    pass  # method
