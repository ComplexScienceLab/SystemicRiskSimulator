"""资不抵债银行间违约损失传染算法"""

<<<<<<< HEAD:PySystemicRiskLab/models/contents/algorithms_contents/content_InterBankInsolventContagion.py
from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.operations.executer import Executer
=======
from SystemicRiskSimulator import np
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.operations.executer import Executer
>>>>>>> dev:SystemicRiskSimulator/models/contents/algorithms_contents/content_InterBankInsolventContagion.py

pass  # end import


def content_InterBankInsolventContagion(A: SystemicRiskAgent, para: dict, env: dict):
    """
    资不抵债银行间违约损失传染算法

    Args:
        A ():
        para ():
        env ():

    Returns:

    """

    # env['stage_name'] = "资不抵债银行间违约损失传染算法"

    for i in np.where(A.BB.isv[:, 0])[0]:  # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击
        A.IB.Shock_IB_def[A.IB.cre_isv[i], i] = np.abs(A.IB.Z_IB[i, A.IB.cre_isv[i]] * A.BB.Shock_IB_def_s[i] / A.BB.Z_IB_all[i])  # BUG `A.IB.cre` 被改成 `A.IB.cre_isv`；
        A.IB.Z_IB[i, A.IB.cre_isv[i]] -= A.IB.Shock_IB_def[A.IB.cre_isv[i], i]
        pass
    ## NOTE 本来是在每个变量更新后就更新的，但是现在放到上述变量一批次计算完之后更新，以便提升性能。
    Executer.step_update('Z_IB', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_IB')
    Executer.step_update('Shock_IB_def', A, para, env)
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_def')

    return A, env
    pass  # function
