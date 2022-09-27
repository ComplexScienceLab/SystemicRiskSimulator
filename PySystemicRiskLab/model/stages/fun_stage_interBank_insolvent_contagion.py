## 函数：资不抵债银行间违约损失传染阶段

##########################################
# 状态/使用
##########################################

from PySystemicRiskLab import np, logging
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import TypeState
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock

pass  # end import

"函数：资不抵债银行间违约损失传染阶段"


def stage_interBank_insolvent_contagion(BB: BankCommercial, BI: BankInterbank, b: TypeState, ib: TypeState, para: dict, env: dict):
    ## # 资不抵债银行间违约损失传染阶段
    # env['stage_name'] = "资不抵债银行间违约损失传染阶段"
    logging.debug("开始阶段%s：", env['stage_name'])

    for i in np.where(BB.isv)[0]:  # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击
        BI.Shock_BI_def[BI.cre[i], i] = np.abs(BI.Z_BI[i, BI.cre[i]] * BB.Shock_BI_def_s[i] / BB.Z_BI_all[i])
        BI.Z_BI[i, BI.cre[i]] -= BI.Shock_BI_def[BI.cre[i], i]
        pass
    # HACK以下部分是否提取出来在阶段1结束之前使用
    BalanceSheet.update_B_balanceSheet(BB, BI, b, ib, byWay="alter to A_BI from Z_BI")  # 转换银行间资产负债邻接矩阵
    Shock.update_B_Shock(BB, BI, b, ib, byWay="Shock_BI_def")  # 更新违约损失冲击目标变量Shock_def_t

    logging.debug("结束阶段%s。", env['stage_name'])
    return BB, BI
    pass  # functions
