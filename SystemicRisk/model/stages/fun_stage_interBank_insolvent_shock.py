## 函数：资不抵债银行间违约损失冲击阶段

##########################################
# 状态/使用
##########################################

from SystemicRisk.core import np, TypeState, BankInterbank, BankCommercial, BankState, Shock, BalanceSheet

"函数：资不抵债银行间违约损失冲击阶段"


def stage_interBank_insolvent_shock(self, BB: BankCommercial, BI: BankInterbank, b: TypeState, ib: TypeState, para: dict, env: dict):
    ## # 资不抵债银行间违约损失冲击阶段
    # env['stage_name'] = "资不抵债银行间违约损失冲击阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    BB.A_BI_all[b] = np.max(BB.A_BI_all[b] - BB.Shock_def_t[b], 0.0)  # 银行之银行间资产变动
    BalanceSheet.update_B_balanceSheet(BB, BI, b, ib, byWay="A_BI_all")
    BB.E_all[BB.on] = np.max(BB.E_all[BB.on] - BB.Shock_def_t[BB.on], 0.0)  # 银行之所有者权益变动
    BankState.update_B_state(BB, BI, target="insolvent", source="healthy")  # 更新各银行之状态，从健康到资不抵债
    BB.Shock_BI_def_s[BB.isv] = abs((BB.Shock_def_t[BB.isv] - BB.E_all[BB.isv]) / (BB.Z_BI_all[BB.isv] + BB.Z_D[BB.isv]) * BB.Z_BI_all[BB.isv])  # 计算应银行内冲击传导至银行间传染冲击
    Shock.update_B_Shock(BB, BI, b, ib, byWay="Shock_BI_def_s")  # 更新违约损失冲击源头变量Shock_def_s
    BB.Shock_D_def_s[BB.isv] = abs((BB.Shock_def_t[BB.isv] - BB.E_all[BB.isv]) / (BB.Z_BI_all[BB.isv] + BB.Z_D[BB.isv]) * BB.Z_D[BB.isv])  # 计算应银行内冲击传导至银行存款传染冲击
    BB.Z_BI_all[BB.isv] -= BB.Shock_BI_def_s[BB.isv]  # 银行间负债变动，由于违约
    BalanceSheet.update_B_balanceSheet(BB, BI, b, ib, byWay="Z_BI_all")  # 更新资产负债表，通过Z_D或Z_BI_all
    BB.Z_D[BB.isv] -= BB.Shock_D_def_s[BB.isv]  # 存款负债变动，由于违约
    BalanceSheet.update_B_balanceSheet(BB, BI, b, ib, byWay="Z_D")  # 更新资产负债表，通过Z_D或Z_BI_all

    # update_B_Shock(BB, BI, b, ib, byWay = "clear Shock_B_A and Shock_B_Z") # 清零银行内资产负债冲击

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass  # functions
