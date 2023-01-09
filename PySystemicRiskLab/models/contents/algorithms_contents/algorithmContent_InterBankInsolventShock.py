"""资不抵债银行间违约损失冲击算法"""



from PySystemicRiskLab import np, logging
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState

pass  # end import



def algorithmContent_InterBankInsolventShock(BB: BankCommercial, BI: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 资不抵债银行间违约损失冲击算法
    # env['stage_name'] = "资不抵债银行间违约损失冲击算法"
    
    BB.A_BI_all[b] = np.maximum(BB.A_BI_all[b] - BB.Shock_def_t[b], 0.0)  # 银行之银行间资产变动
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='A_BI_all')
    BB.E_all[BB.on] = np.maximum(BB.E_all[BB.on] - BB.Shock_def_t[BB.on], 0.0)  # 银行之所有者权益变动
    BankState.update_B_state(BB, BI, target='insolvent', source='healthy')  # 更新各银行之状态，从健康到资不抵债
    BB.Shock_BI_def_s[BB.isv] = abs((BB.Shock_def_t[BB.isv] - BB.E_all[BB.isv]) / (BB.Z_BI_all[BB.isv] + BB.Z_D[BB.isv]) * BB.Z_BI_all[BB.isv])  # 计算应银行内冲击传导至银行间传染冲击
    Shock.update_B_Shock(BB, BI, b, ib, by_way='Shock_BI_def_s')  # 更新违约损失冲击源头变量Shock_def_s
    BB.Shock_D_def_s[BB.isv] = abs((BB.Shock_def_t[BB.isv] - BB.E_all[BB.isv]) / (BB.Z_BI_all[BB.isv] + BB.Z_D[BB.isv]) * BB.Z_D[BB.isv])  # 计算应银行内冲击传导至银行存款传染冲击
    BB.Z_BI_all[BB.isv] -= BB.Shock_BI_def_s[BB.isv]  # 银行间负债变动，由于违约
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='Z_BI_all')  # 更新资产负债表，通过Z_D或Z_BI_all
    BB.Z_D[BB.isv] -= BB.Shock_D_def_s[BB.isv]  # 存款负债变动，由于违约
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='Z_D')  # 更新资产负债表，通过Z_D或Z_BI_all

    # update_B_Shock(BB, BI, b, ib, by_way = "clear Shock_B_A and Shock_B_Z") # 清零银行内资产负债冲击

    return BB, BI
    pass  # method
