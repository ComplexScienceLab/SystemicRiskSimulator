"""
模型IB1111
"""

from SystemicRiskSimulator.external_packages import np, logging
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.operations.executer import Executer
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.functions.fun_finance import Finance


pass  # end import


def content_IB1111(A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
    ## node_START

    ## node_01 外部资产违约损失冲击模型 content_ExBankInsolventShock

    # sgv['stage_name'] = "外部资产违约损失冲击模型"

    A.BB.Shock_P_def_t = A.BB.A_P * np.array([para['Shock_exIB_def_t_percentage']]).T  # 生成厂商贷款违约损失冲击
    Executer.step_update('Shock_P_def_t', A, para, sgv)  # 厂商贷款违约损失冲击传导至银行内资产冲击
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_P_def_t')
    A.BB.A_P[A.BB.on] = np.maximum(A.BB.A_P[A.BB.on] - A.BB.Shock_P_def_t[A.BB.on], 0.0)  # 银行之非银行间资产变动
    Executer.step_update('A_P', A, para, sgv)  # 厂商贷款违约损失冲击传导至银行内资产冲击
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_P')  # 厂商贷款违约损失冲击传导至银行内资产冲击
    A.BB.E_all[A.BB.on] = np.maximum(A.BB.E_all[A.BB.on] - A.BB.Shock_def_t[A.BB.on], 0.0)  # 银行之所有者权益变动
    A.BB.Shock_IB_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_IB_all[A.BB.isv])  # 计算应银行内冲击传导至银行间传染冲击
    Executer.step_update('Shock_IB_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_def_s')  # 更新违约损失冲击源头变量Shock_def_s
    A.BB.Shock_D_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_D[A.BB.isv])  # 计算应银行内冲击传导至银行存款传染冲击
    Executer.step_update('Shock_D_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s #BUG
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_D_def_s')  # 更新违约损失冲击源头变量Shock_def_s #BUG
    A.BB.Z_IB_all[A.BB.isv] -= A.BB.Shock_IB_def_s[A.BB.isv]  # 银行间负债变动，由于违约
    Executer.step_update('Z_IB_all', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_IB_all')  # 更新资产负债表，通过Z_D或Z_IB_all
    A.BB.Z_D[A.BB.isv] -= A.BB.Shock_D_def_s[A.BB.isv]  # 存款负债变动，由于违约
    Executer.step_update('Z_D', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all
    # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_D')  # 更新资产负债表，通过Z_D或Z_IB_all

    ## node_01_condition_01
    if (A.BB.isv != A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].isv).any():

        ## node_02 资不抵债银行间违约损失传染模型 content_InterBankInsolventContagion

        # sgv['stage_name'] = "资不抵债银行间违约损失传染模型"

        for i in np.where(A.BB.isv[:, 0])[0]:  # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击
            A.IB.Shock_IB_def[A.IB.cre_isv[i], i] = np.abs(A.IB.Z_IB[i, A.IB.cre_isv[i]] * A.BB.Shock_IB_def_s[i] / A.BB.Z_IB_all[i])  # BUG `A.IB.cre` 被改成 `A.IB.cre_isv`；
            A.IB.Z_IB[i, A.IB.cre_isv[i]] -= A.IB.Shock_IB_def[A.IB.cre_isv[i], i]
            pass
        ## NOTE：本来是在每个变量更新后就更新的，但是现在放到上述变量一批次计算完之后更新，以便提升性能。
        Executer.step_update('Z_IB', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_IB')
        Executer.step_update('Shock_IB_def', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_def')

        ## node_03 资不抵债银行资产违约损失冲击模型 content_InterBankInsolventShock

        # sgv['stage_name'] = "资不抵债银行资产违约损失冲击模型"

        A.BB.A_IB_all[A.b] = np.maximum(A.BB.A_IB_all[A.b] - A.BB.Shock_def_t[A.b], 0.0)  # 银行之银行间资产变动
        Executer.step_update('A_IB_all', A, para, sgv)  # 更新银行间资产
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_IB_all')  # 更新银行间资产
        A.BB.E_all[A.BB.on] = np.maximum(A.BB.E_all[A.BB.on] - A.BB.Shock_def_t[A.BB.on], 0.0)  # 银行之所有者权益变动
        A.BB.Shock_IB_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_IB_all[A.BB.isv])  # 计算应银行内冲击传导至银行间传染冲击
        Executer.step_update('Shock_IB_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_def_s')  # 更新违约损失冲击源头变量Shock_def_s
        A.BB.Shock_D_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_D[A.BB.isv])  # 计算应银行内冲击传导至银行存款传染冲击
        Executer.step_update('Shock_D_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s #BUG
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_D_def_s')  # 更新违约损失冲击源头变量Shock_def_s #BUG
        A.BB.Z_IB_all[A.BB.isv] -= A.BB.Shock_IB_def_s[A.BB.isv]  # 银行间负债变动，由于违约
        Executer.step_update('Z_IB_all', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_IB_all')  # 更新资产负债表，通过Z_D或Z_IB_all
        A.BB.Z_D[A.BB.isv] -= A.BB.Shock_D_def_s[A.BB.isv]  # 存款负债变动，由于违约
        Executer.step_update('Z_D', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_D')  # 更新资产负债表，通过Z_D或Z_IB_all

        # update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way = 'clear Shock_B_A and Shock_B_Z') # 清零银行内资产负债冲击

    ## node_01_condition_02
    elif (A.BB.isv == A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].isv).any():

        ## node_04 银行存款挤兑流动冲击模型 content_ExBankIlliquidShock

        # sgv['stage_name'] = "银行存款挤兑流动冲击模型"

        A.BB.Shock_D_run_t = A.BB.Z_D * np.array([para['Shock_exIB_run_t_percentage']]).T  # 生成居民存款挤兑流动冲击
        Executer.step_update('Shock_D_run_t', A, para, sgv)  # 居民存款挤兑流动冲击传导至银行内资产冲击
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_D_run_t')  # 居民存款挤兑流动冲击传导至银行内资产冲击
        A.BB.Shock_IB_run_ilq_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_IB_all[A.BB.ilq])  # 计算应银行内冲击传导至银行间传染冲击
        Executer.step_update('Shock_IB_run_ilq_s', A, para, sgv)  # 更新挤兑流动冲击源头变量Shock_run_t
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq_s')  # 更新挤兑流动冲击源头变量Shock_run_t
        A.BB.Shock_P_run_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_P[A.BB.ilq])  # 银行内冲击传导至银行厂商贷款传染冲击
        A.BB.is_allocated_Shock |= A.BB.ilq  # 更新已经分配传染冲击的银行
        for i in np.where(A.BB.ilq)[0]:  # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
            A.IB.Shock_IB_run_ilq[A.IB.deb_ilq[i], i] = A.IB.A_IB[i, A.IB.deb_ilq[i]] * A.BB.Shock_IB_run_ilq_s[i] / A.BB.A_IB_all[i]
            pass
        Executer.step_update('Shock_IB_run_ilq', A, para, sgv)  # 更新挤兑流动冲击源头变量Shock_run_t

        pass  # node_01_condition

        if (A.BB.isv != A_data.BB[A_data.BB['round'] == sgv['round'] - 1].iloc[-1].isv).any():  ##node_03_condition_01 #FIXME

        ## node_05 流动性短缺银行间挤兑流动传染 content_InterBankIlliquidContagionShock

        # sgv['stage_name'] = "流动性短缺银行间挤兑流动传染模型"

        ## DEBUG 方式一：每个银行只有一次分配传染冲击之行为。感觉这个比较简单。
        i_nas = (A.BB.ilq & ~A.BB.is_allocated_Shock)  # 临时设置示性变量，表示银行其未分配传染冲击。暨每个银行只有一次分配传染冲击之行为。
        A.BB.Shock_IB_run_ilq_s[i_nas] = abs((A.BB.Shock_run_t[i_nas] - A.BB.A_Q[i_nas]) / (A.BB.A_P[i_nas] + A.BB.A_IB_all[i_nas]) * A.BB.A_IB_all[i_nas])  # 计算应银行内冲击传导至银行间传染冲击
        Executer.step_update('Shock_IB_run_ilq_s', A, para, sgv)  # 更新挤兑流动冲击源头变量Shock_run_t
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq_s')  # 更新挤兑流动冲击源头变量Shock_run_t
        A.BB.Shock_P_run_s[i_nas] = abs((A.BB.Shock_run_t[i_nas] - A.BB.A_Q[i_nas]) / (A.BB.A_P[i_nas] + A.BB.A_IB_all[i_nas]) * A.BB.A_P[i_nas])  # 银行内冲击传导至银行厂商贷款传染冲击
        A.BB.is_allocated_Shock |= A.BB.ilq  # 更新已经分配传染冲击的银行
        for i in np.where(i_nas)[0]:  # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
            A.IB.Shock_IB_run_ilq[A.IB.deb_ilq[i], i] = A.IB.A_IB[i, A.IB.deb_ilq[i]] * A.BB.Shock_IB_run_ilq_s[i] / A.BB.A_IB_all[i]
            pass
        Executer.step_update('Shock_IB_run_ilq', A, para, sgv)  # 更新挤兑流动冲击源头变量Shock_run_t
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq')  # 更新挤兑流动冲击源头变量Shock_run_t

        # ##DEBUG 方式二：每个银行可以有多次分配传染冲击之行为。
        # A.BB.Shock_IB_run_ilq_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_IB_all[A.BB.ilq]) # 计算应银行内冲击传导至银行间传染冲击
        # update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way = 'Shock_IB_run_ilq_s') # 汇总各银行之流动性短缺流动性挤兑冲击
        # A.BB.Shock_P_run_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_P[A.BB.ilq]) # 银行内冲击传导至银行厂商贷款传染冲击
        # for i in findall(A.BB.on) # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
        #     A.IB.Shock_IB_run_ilq[A.IB.deb[i], i] = A.IB.A_IB[i, A.IB.deb[i]] * A.BB.Shock_IB_run_ilq_s[i] / A.BB.A_IB_all[i]
        #     pass
        # update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way = 'Shock_IB_run_ilq') # 加总各单个债务银行遭受总银行间挤兑流动冲击
        # update_states(target='illiquid', source='healthy') # 更新各银行之状态，从健康到流动性短缺

        ## node_06 流动性短缺银行间挤兑流动分配借贷流量模型 content_InterBankIlliquidAllocate

        # sgv['stage_name'] = "流动性短缺银行间挤兑流动分配借贷流量模型"

        Executer.step_update('enabled collect A_P', A, para, sgv)  # 计算是否可以偿还银行间借款状态
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='enabled collect A_P')  # 计算是否可以偿还银行间借款状态
        A.BB.Li_P[A.BB.is_enabled_LiP] = A.BB.Shock_P_run_s[A.BB.is_enabled_LiP]  # 计算银行收回厂商贷款流量
        Executer.step_update('Li_P', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Li_P')

        Executer.step_update('enabled repay Z_D', A, para, sgv)  # 计算是否需要偿还借款状态
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='enabled repay Z_D')  # 计算是否需要偿还借款状态
        Executer.step_update('enabled repay IB', A, para, sgv)  # 计算是否可以收回厂商贷款状态
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='enabled repay IB')  # 计算是否可以收回厂商贷款状态
        A.BB.Bo_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] = np.minimum(A.BB.A_Q[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD], A.BB.Shock_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD])  # 计算银行偿还借款总流量 #BUG
        A.BB.Bo_D[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] = A.BB.Shock_D_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] * (A.BB.Bo_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] / A.BB.Shock_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD])  # 计算银行偿还居民借款流量
        A.BB.Bo_IB_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] = A.BB.Shock_IB_run_ilq_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] * (A.BB.Bo_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] / A.BB.Shock_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD])  # 计算银行偿还银行间借款流量
        Executer.step_update('Bo_D', A, para, sgv)  # HACK 这个必须放在这里！
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Bo_D')  # HACK 这个必须放在这里！
        Executer.step_update('Bo_IB_all', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Bo_IB_all')
        for i in np.where(A.BB.is_enabled_BoIB)[0]:  # 计算银行可以偿还各债权银行的借款流量
            A.IB.Bo_IB[i, A.IB.cre_ilq[i]] = A.IB.Shock_IB_run_ilq[i, A.IB.cre_ilq[i]] * (A.BB.Bo_IB_all[i] / A.BB.Shock_IB_run_ilq_t[i])
            pass
        Executer.step_update('Bo_IB', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Bo_IB')

        ## node_07 流动性短缺银行间挤兑流动执行借贷流量模型 content_InterBankIlliquidRepay

        # sgv['stage_name'] = "流动性短缺银行间挤兑流动执行借贷流量模型"

        A.BB.A_Q[A.b], A.BB.A_P[A.b], A.BB.Shock_P_run_s[A.b] = Finance.transfer_B_capital_reverse(A.BB.A_Q[A.b], A.BB.A_P[A.b], A.BB.Shock_P_run_s[A.b], A.BB.Li_P[A.b])  # 流动资产变动，因收回厂商贷款
        # A.BB.A_Q[A.b] *= (1 - paras['kappa_A_P']) #HACK 暂时还不用！
        Executer.step_update('A_Q', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_Q')
        Executer.step_update('A_P', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_P')
        Executer.step_update('Shock_P_run_s', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_P_run_s')

        A.BB.Z_D[A.b], A.BB.A_Q[A.b], A.BB.Shock_D_run_t[A.b] = Finance.transfer_B_capital_reduce(A.BB.Z_D[A.b], A.BB.A_Q[A.b], A.BB.Shock_D_run_t[A.b], A.BB.Bo_D[A.b])  # 流动资产变动，因偿还居民存款
        Executer.step_update('Z_D', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_D')
        Executer.step_update('A_Q', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_Q')
        Executer.step_update('Shock_D_run_t', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_D_run_t')

        A.IB.Shock_IB_run_ilq[A.ib] -= A.IB.Bo_IB[A.ib]  # 各银行间挤兑流动冲击变动，当偿还相应的银行间借款时
        Executer.step_update('Shock_IB_run_ilq', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq')
        A.BB.Shock_IB_run_ilq_s[A.b] -= A.BB.Li_IB_all[A.b]  # 各银行之银行间挤兑流动冲击源头变动，当收回相应的银行间贷款时
        Executer.step_update('Shock_IB_run_ilq_s', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Shock_IB_run_ilq_s')
        A.IB.Z_IB[A.ib] -= A.IB.Bo_IB[A.ib]  # 各银行间负债变动，当偿还相应的银行间借款时
        Executer.step_update('Z_IB', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='Z_IB')
        # # A.IB.A_IB[A.ib] += A.IB.Li_IB[A.ib]' # 各银行间资产变动，当收回相应的银行间贷款时
        A.BB.A_Q[A.b] += (A.BB.Li_IB_all[A.b] - A.BB.Bo_IB_all[A.b])  # 各银行流动资金变动，当收回相应的银行间贷款、偿还相应的银行间借款时
        Executer.step_update('A_Q', A, para, sgv)
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='A_Q')

        Executer.step_update('clear transfer all', A, para, sgv)  # 清零所有不必要的借贷流量变量；#BUG这个是否有必要？
        # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='clear transfer all')  # 清零所有不必要的借贷流量变量；#BUG这个是否有必要？

    pass  # function

########################################################################################################################

# import random
# from SystemicRiskSimulator.external_packages import logging
# from SystemicRiskSimulator.core.define.define_entity import Entity
# from SystemicRiskSimulator.core.operations.processor import Processor as p
# from SystemicRiskSimulator.core.operations.builder import Builder as b
#
# # from SystemicRiskSimulator.data.model.contents.models_contents.content_ExBankInsolventShock import content_ExBankInsolventShock
# # from SystemicRiskSimulator.data.model.contents.models_contents.content_ExBankIlliquidShock import content_ExBankIlliquidShock
# # from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankInsolventShock import content_InterBankInsolventShock
# # from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankInsolventContagion import content_InterBankInsolventContagion
# # from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankIlliquidContagionShock import content_InterBankIlliquidContagionShock
# # from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankIlliquidAllocate import content_InterBankIlliquidAllocate
# # from SystemicRiskSimulator.data.model.contents.models_contents.content_InterBankIlliquidRepay import content_InterBankIlliquidRepay
#
# pass  # end import
#
#
# content_IB1111 = \
#     """
#     define process entity_IB1111
#
#     execute content node_START
#
#     execute content node_01
#     if node_01_condition_01 goto node_02
#     if node_01_condition_02 goto node_04
#
#     execute content node_02
#
#     execute content node_03
#     if node_03_condition_01 goto node_02
#     if node_03_condition_02 goto node_04
#
#     execute content node_04
#     if node_04_condition_01 goto node_05
#     if node_04_condition_02 goto node_END
#
#     execute content node_05
#
#     execute content node_06
#
#     execute content node_07
#     if node_07_condition_01 goto node_05
#     if node_07_condition_02 goto node_END
#
#     execute content node_END
#
#     end define
#     """
#
