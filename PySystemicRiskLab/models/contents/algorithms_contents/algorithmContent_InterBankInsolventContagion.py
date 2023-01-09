"""资不抵债银行间违约损失传染算法"""

from PySystemicRiskLab import np, logging
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock

pass  # end import


def algorithmContent_InterBankInsolventContagion(BB: BankCommercial, BI: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 资不抵债银行间违约损失传染算法
    # env['stage_name'] = "资不抵债银行间违约损失传染算法"

    for i in np.where(BB.isv[:, 0])[0]:  # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击
        BI.Shock_BI_def[BI.cre_isv[i], i] = np.abs(BI.Z_BI[i, BI.cre_isv[i]] * BB.Shock_BI_def_s[i] / BB.Z_BI_all[i])  #BUG `BI.cre` 被改成 `BI.cre_isv`；
        BI.Z_BI[i, BI.cre_isv[i]] -= BI.Shock_BI_def[BI.cre_isv[i], i]
        pass
    # HACK以下部分是否提取出来在算法1结束之前使用
    BalanceSheet.update_B_balance_sheet(BB, BI, b, ib, by_way='alter to A_BI from Z_BI')  # 转换银行间资产负债邻接矩阵
    Shock.update_B_Shock(BB, BI, b, ib, by_way='Shock_BI_def')  # 更新违约损失冲击目标变量Shock_def_t

    return BB, BI
    pass  # method
