"""流动性短缺银行间挤兑流动传染算法"""

from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial, SystemicRiskAgent
from PySystemicRiskLab.core.define.define_type import StateType
# from PySystemicRiskLab.core.functions.fun_finance import Finance
from PySystemicRiskLab.core.operations.executer import Executer

pass  # end import


def content_InterBankIlliquidContagionShock(A: SystemicRiskAgent, para: dict, env: dict):
    ## # 流动性短缺银行间挤兑流动传染
    # env['stage_name'] = "流动性短缺银行间挤兑流动传染算法"

    ## BUG 方式一：每个银行只有一次分配传染冲击之行为。
    i_nas = (A.BB.ilq & ~A.BB.is_allocated_Shock)  # 临时设置示性变量，表示银行其未分配传染冲击。暨每个银行只有一次分配传染冲击之行为。
    A.BB.Shock_IB_run_ilq_s[i_nas] = abs((A.BB.Shock_run_t[i_nas] - A.BB.A_Q[i_nas]) / (A.BB.A_P[i_nas] + A.BB.A_IB_all[i_nas]) * A.BB.A_IB_all[i_nas])  # 计算应银行内冲击传导至银行间传染冲击
    Executer.step_update('Shock_IB_run_ilq_s', A, para, env)  # 更新挤兑流动冲击源头变量Shock_run_t
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq_s')  # 更新挤兑流动冲击源头变量Shock_run_t
    A.BB.Shock_P_run_s[i_nas] = abs((A.BB.Shock_run_t[i_nas] - A.BB.A_Q[i_nas]) / (A.BB.A_P[i_nas] + A.BB.A_IB_all[i_nas]) * A.BB.A_P[i_nas])  # 银行内冲击传导至银行厂商贷款传染冲击
    A.BB.is_allocated_Shock |= A.BB.ilq  # 更新已经分配传染冲击的银行
    for i in np.where(i_nas)[0]:  # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
        A.IB.Shock_IB_run_ilq[A.IB.deb_ilq[i], i] = A.IB.A_IB[i, A.IB.deb_ilq[i]] * A.BB.Shock_IB_run_ilq_s[i] / A.BB.A_IB_all[i]
        pass
    Executer.step_update('Shock_IB_run_ilq', A, para, env)  # 更新挤兑流动冲击源头变量Shock_run_t
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq')  # 更新挤兑流动冲击源头变量Shock_run_t

    # ##BUG 方式二：每个银行可以有多次分配传染冲击之行为。
    # A.BB.Shock_IB_run_ilq_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_IB_all[A.BB.ilq]) # 计算应银行内冲击传导至银行间传染冲击
    # update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way = 'Shock_IB_run_ilq_s') # 汇总各银行之流动性短缺流动性挤兑冲击
    # A.BB.Shock_P_run_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_P[A.BB.ilq]) # 银行内冲击传导至银行厂商贷款传染冲击
    # for i in findall(A.BB.on) # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
    #     A.IB.Shock_IB_run_ilq[A.IB.deb[i], i] = A.IB.A_IB[i, A.IB.deb[i]] * A.BB.Shock_IB_run_ilq_s[i] / A.BB.A_IB_all[i]
    #     pass
    # update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way = 'Shock_IB_run_ilq') # 加总各单个债务银行遭受总银行间挤兑流动冲击
    # update_states(target='illiquid', source='healthy') # 更新各银行之状态，从健康到流动性短缺

    return A, env
    pass  # method
