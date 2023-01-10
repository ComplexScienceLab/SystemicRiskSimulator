"""银行外部挤兑流动冲击算法"""

from PySystemicRiskLab import np, logging
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState

pass  # end import


def algorithmContent_ExBankIlliquidShock(BB: BankCommercial, BI: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):  # = BB_t1:BankCommercial, BI_t1:BankInterbank,  =#:
    ## # 银行外部挤兑流动冲击算法
    # env['stage_name'] = "银行外部挤兑流动冲击算法"

    BB.Shock_D_run_t = BB.Z_D * np.array([para['Shock_exBI_run_t_percentage']]).T  # 生成居民存款挤兑流动冲击
    Shock.update_B_Shock(BB, BI, b, ib, by_way='Shock_D_run_t')  # 居民存款挤兑流动冲击传导至银行内负债冲击
    BankState.update_B_state(BB, BI, target='illiquid', source='healthy')  # 更新各银行之状态，从健康到流动性短缺

    return BB, BI
    pass  # method
