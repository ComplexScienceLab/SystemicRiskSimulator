"""资不抵债银行间违约损失传染算法"""

from PySystemicRiskLab import np, logging
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import StateType
from PySystemicRiskLab.core.functions.fun_finance import Finance

pass  # end import


def content_InterBankInsolventContagion(BB: BankCommercial, IB: BankInterbank, b: StateType, ib: StateType, para: dict, env: dict):
    ## # 资不抵债银行间违约损失传染算法
    # env['stage_name'] = "资不抵债银行间违约损失传染算法"

    for i in np.where(BB.isv[:, 0])[0]:  # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击
        IB.Shock_IB_def[IB.cre_isv[i], i] = np.abs(IB.Z_IB[i, IB.cre_isv[i]] * BB.Shock_IB_def_s[i] / BB.Z_IB_all[i])  #BUG `IB.cre` 被改成 `IB.cre_isv`；
        IB.Z_IB[i, IB.cre_isv[i]] -= IB.Shock_IB_def[IB.cre_isv[i], i]
        pass
    ## NOTE 本来是在每个变量更新后就更新的，但是现在放到上述变量一批次计算完之后更新，以便提升性能。
    Finance.update_finance_variables(BB, IB, b, ib, by_way='Z_IB')
    Finance.update_finance_variables(BB, IB, b, ib, by_way='Shock_IB_def')

    return BB, IB
    pass  # method
