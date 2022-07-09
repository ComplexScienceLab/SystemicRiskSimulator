## 函数：资不抵债银行间违约损失传染阶段

##########################################
# 状态/使用
##########################################

import numpy as np

from SystemicRisk.core.define.define_type import TypeState
from SystemicRisk.core.define.define_agents import BankInterbank, BankCommercial
from SystemicRisk.core.functions.fun_shock import Shock
from SystemicRisk.core.functions.fun_balanceSheet import BalanceSheet
pass  # end import

"函数：资不抵债银行间违约损失传染阶段"


def stage_interBank_insolvent_contagion(self, BB: BankCommercial, BI: BankInterbank, b: TypeState, ib: TypeState, para: dict, env: dict):
    ## # 资不抵债银行间违约损失传染阶段
    # env['stage_name'] = "资不抵债银行间违约损失传染阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    for i in np.where(BB.isv):  # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击
        BI.Shock_BI_def[BI.cre[i], i] = abs(BI.Z_BI[i, BI.cre[i]] * BB.Shock_BI_def_s[i] / BB.Z_BI_all[i])
        BI.Z_BI[i, BI.cre[i]] -= BI.Shock_BI_def[BI.cre[i], i]
        pass
    # HACK以下部分是否提取出来在阶段1结束之前使用
    BalanceSheet.cupdate_B_balanceSheet(BB, BI, b, ib, byWay="alter to A_BI from Z_BI")  # 转换银行间资产负债邻接矩阵
    Shock.update_B_Shock(BB, BI, b, ib, byWay="Shock_BI_def")  # 更新违约损失冲击目标变量Shock_def_t

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass  # functions
