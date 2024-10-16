"""
模型IB1111

NOTE 说明：这个模型仅作为样例进行展示。对于该模型的正确性并不做讨论。
FIXME 警告：这个模型已经过时，不一定能够运行成功。后续有时间的话将进行适配。
"""

from SystemicRiskSimulator.external_packages import np, logging
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.operations.executer import Executer
from SystemicRiskSimulator.core.functions.fun_finance import Finance


def content_IB1111(A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
    """
    模型IB1111

    Args:
        A ():
        A_data ():
        para ():
        sgv ():

    Returns:

    """

    ## node_START

    ## node_01
    A, sgv = ExBankInsolventShock(A, para, sgv)

    # if(A.BB.isv == A_data.BB[A_data.BB['turn'] == sgv['turn'] - 1].iloc[-1].isv).all():
    #     is_goto_node_04 = True

    while (A.BB.isv != A_data.BB[A_data.BB['turn'] == sgv['turn'] - 1].iloc[-1].isv).any():
        ## node_02
        A, sgv = InterBankInsolventContagion(A, para, sgv)

        ## node_03
        A, sgv = InterBankInsolventShock(A, para, sgv)

        pass  # while

    # Executer.update_variableStep('clear Shock_IB and Shock_exIB', A, para, sgv)

    ## node_04
    A, sgv = ExBankIlliquidShock(A, para, sgv)

    while (A.BB.ilq != A_data.BB[A_data.BB['turn'] == sgv['turn'] - 1].iloc[-1].ilq).any():
        ## node_05
        A, sgv = InterBankIlliquidContagionShock(A, para, sgv)

        ## node_06
        A, sgv = InterBankIlliquidAllocate(A, para, sgv)

        ## node_07
        A, sgv = InterBankIlliquidRepay(A, para, sgv)

        pass  # while

    ## node_END

    pass  # function


def ExBankInsolventShock(A: SystemicRiskAgent, para: dict, sgv: dict):
    """
    外部资产违约损失冲击模型

    Args:
        A ():
        para ():
        sgv ():

    Returns:

    """

    sgv['turn'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
    sgv['phase'] = 1  # 逐相复位（起始为1）
    sgv['process_name'] = "ExBankInsolventShock"

    logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

    # Executer.update_variableStep('clear all Shock_source', A, para, sgv)  # 清零所有冲击源头变量 Shock_source
    # Executer.update_variableStep('clear all Shock_IB', A, para, sgv)  # 清零所有银行间冲击变量 Shock_IB

    A.BB.Shock_P_def_t = A.BB.A_P * np.array([para['Shock_exIB_def_t_percentage']]).T  # 厂商贷款违约损失冲击
    Executer.update_variableStep('Shock_P_def_t', A, para, sgv)  # 厂商贷款违约损失冲击传导至银行内资产冲击

    A.BB.Loss_exIB_def_t[A.BB.on] = np.minimum(A.BB.E_all[A.BB.on], A.BB.Shock_P_def_t[A.BB.on])  # 非银行间违约损失冲击损失
    Executer.update_variableStep('Loss_exIB_def_t', A, para, sgv)
    A.BB.Loss_IB_def_t[A.BB.on] = np.maximum(0, A.BB.Shock_P_def_t[A.BB.on] - A.BB.E_all[A.BB.on])  # 银行间违约损失冲击损失
    Executer.update_variableStep('Loss_IB_def_t', A, para, sgv)

    A.BB.A_P[A.BB.on] = np.maximum(A.BB.A_P[A.BB.on] - A.BB.Shock_P_def_t[A.BB.on], 0.0)  # 银行之非银行间资产变动
    Executer.update_variableStep('A_P', A, para, sgv)  # 厂商贷款违约损失冲击传导至银行内资产冲击
    A.BB.E_all[A.BB.on] = np.maximum(A.BB.E_all[A.BB.on] - A.BB.Shock_def_t[A.BB.on], 0.0)  # 银行之所有者权益变动

    A.BB.Shock_IB_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_IB_all[A.BB.isv])  # 计算应银行内冲击传导至银行间传染冲击
    Executer.update_variableStep('Shock_IB_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s
    A.BB.Shock_D_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_D[A.BB.isv])  # 计算应银行内冲击传导至银行存款传染冲击
    Executer.update_variableStep('Shock_D_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s
    A.BB.Z_IB_all[A.BB.isv] -= A.BB.Shock_IB_def_s[A.BB.isv]  # 银行间负债变动，由于违约
    Executer.update_variableStep('Z_IB_all', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all
    A.BB.Z_D[A.BB.isv] -= A.BB.Shock_D_def_s[A.BB.isv]  # 存款负债变动，由于违约
    Executer.update_variableStep('Z_D', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all

    return A, sgv
    pass  # function


def InterBankInsolventContagion(A: SystemicRiskAgent, para: dict, sgv: dict):
    """
    资不抵债银行间违约损失传染模型

    Args:
        A ():
        para ():
        sgv ():

    Returns:

    """

    sgv['turn'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
    sgv['phase'] = 1  # 逐相复位（起始为1）
    sgv['process_name'] = "InterBankInsolventContagion"

    logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

    # Executer.update_variableStep('clear all Shock_target', A, para, sgv)  # 清零所有冲击目标变量 Shock_target

    for i in np.where(A.BB.isv[:, 0])[0]:  # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击
        A.IB.Shock_IB_def[A.IB.cre_isv[i], i] = np.abs(A.IB.Z_IB[i, A.IB.cre_isv[i]] * A.BB.Shock_IB_def_s[i] / A.BB.Z_IB_all[i])
        A.IB.Z_IB[i, A.IB.cre_isv[i]] -= A.IB.Shock_IB_def[A.IB.cre_isv[i], i]
        A.IB.Loss_IB_def[A.IB.cre_isv[i], i] = A.IB.Shock_IB_def[A.IB.cre_isv[i], i]  # 银行间违约损失冲击损失
        pass
    ## NOTE 本来是在每个变量更新后就更新的，但是现在放到上述变量一批次计算完之后更新，以便提升性能。
    Executer.update_variableStep('Z_IB', A, para, sgv)
    Executer.update_variableStep('Shock_IB_def', A, para, sgv)
    Executer.update_variableStep('Loss_IB_def', A, para, sgv)

    return A, sgv
    pass  # function


def InterBankInsolventShock(A: SystemicRiskAgent, para: dict, sgv: dict):
    """
    资不抵债银行资产违约损失冲击模型

    Args:
        A ():
        para ():
        sgv ():

    Returns:

    """

    sgv['turn'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
    sgv['phase'] = 1  # 逐相复位（起始为1）
    sgv['process_name'] = "InterBankInsolventShock"

    logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

    # Executer.update_variableStep('clear all Shock_source', A, para, sgv)  # 清零所有冲击源头变量 Shock_source
    # Executer.update_variableStep('clear all Shock_IB', A, para, sgv)  # 清零所有银行间冲击变量 Shock_IB

    A.BB.Loss_IB_def_t[A.BB.on] = np.maximum(0, A.BB.Shock_IB_def_t[A.BB.on] - A.BB.E_all[A.BB.on])  # 银行间违约损失冲击损失
    Executer.update_variableStep('Loss_IB_def_t', A, para, sgv)

    A.BB.A_IB_all[A.b] = np.maximum(A.BB.A_IB_all[A.b] - A.BB.Shock_def_t[A.b], 0.0)  # 银行之银行间资产变动
    Executer.update_variableStep('A_IB_all', A, para, sgv)  # 更新银行间资产
    A.BB.E_all[A.BB.on] = np.maximum(A.BB.E_all[A.BB.on] - A.BB.Shock_def_t[A.BB.on], 0.0)  # 银行之所有者权益变动
    A.BB.Shock_IB_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_IB_all[A.BB.isv])  # 计算应银行内冲击传导至银行间传染冲击
    Executer.update_variableStep('Shock_IB_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s
    A.BB.Shock_D_def_s[A.BB.isv] = abs((A.BB.Shock_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv]) / (A.BB.Z_IB_all[A.BB.isv] + A.BB.Z_D[A.BB.isv]) * A.BB.Z_D[A.BB.isv])  # 计算应银行内冲击传导至银行存款传染冲击
    Executer.update_variableStep('Shock_D_def_s', A, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s
    A.BB.Z_IB_all[A.BB.isv] -= A.BB.Shock_IB_def_s[A.BB.isv]  # 银行间负债变动，由于违约
    Executer.update_variableStep('Z_IB_all', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all
    A.BB.Z_D[A.BB.isv] -= A.BB.Shock_D_def_s[A.BB.isv]  # 存款负债变动，由于违约
    Executer.update_variableStep('Z_D', A, para, sgv)  # 更新资产负债表，通过Z_D或Z_IB_all

    # update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way = 'clear Shock_B_A and Shock_B_Z') # 清零银行内资产负债冲击

    return A, sgv
    pass  # function


def ExBankIlliquidShock(A: SystemicRiskAgent, para: dict, sgv: dict):
    """
    银行存款挤兑流动冲击模型

    Args:
        A ():
        para ():
        sgv ():

    Returns:

    """

    sgv['turn'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
    sgv['phase'] = 1  # 逐相复位（起始为1）
    sgv['process_name'] = "ExBankIlliquidShock"

    logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

    # Executer.update_variableStep('clear all Shock_source', A, para, sgv)  # 清零所有冲击源头变量 Shock_source
    # Executer.update_variableStep('clear all Shock_IB', A, para, sgv)  # 清零所有银行间冲击变量 Shock_IB

    A.BB.Shock_D_run_t = A.BB.Z_D * np.array([para['Shock_exIB_run_t_percentage']]).T  # 生成居民存款挤兑流动冲击
    Executer.update_variableStep('Shock_D_run_t', A, para, sgv)  # 居民存款挤兑流动冲击传导至银行内资产冲击

    A.BB.Shock_IB_run_ilq_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_IB_all[A.BB.ilq])  # 计算应银行内冲击传导至银行间传染冲击
    Executer.update_variableStep('Shock_IB_run_ilq_s', A, para, sgv)  # 更新挤兑流动冲击源头变量 Shock_run_t
    A.BB.Shock_P_run_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_P[A.BB.ilq])  # 银行内冲击传导至银行厂商贷款传染冲击

    Executer.update_variableStep('clear all Shock_target', A, para, sgv)  # 清零所有冲击目标变量 Shock_target

    A.BB.is_allocated_Shock |= A.BB.ilq  # 更新已经分配传染冲击的银行
    for i in np.where(A.BB.ilq)[0]:  # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
        A.IB.Shock_IB_run_ilq[A.IB.deb_ilq[i], i] = A.IB.A_IB[i, A.IB.deb_ilq[i]] * A.BB.Shock_IB_run_ilq_s[i] / A.BB.A_IB_all[i]
        pass
    Executer.update_variableStep('Shock_IB_run_ilq', A, para, sgv)  # 更新挤兑流动冲击源头变量Shock_run_s

    return A, sgv
    pass  # function


def InterBankIlliquidContagionShock(A: SystemicRiskAgent, para: dict, sgv: dict):
    """
    流动性短缺银行间挤兑流动传染

    Args:
        A ():
        para ():
        sgv ():

    Returns:

    """

    sgv['turn'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
    sgv['phase'] = 1  # 逐相复位（起始为1）
    sgv['process_name'] = "InterBankIlliquidContagionShock"

    logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

    ## DEBUG 方式一：每个银行只有一次分配传染冲击之行为。感觉这个比较简单。
    i_nas = (A.BB.ilq & ~A.BB.is_allocated_Shock)  # 临时设置示性变量，表示银行其未分配传染冲击。暨每个银行只有一次分配传染冲击之行为。
    A.BB.Shock_IB_run_ilq_s[i_nas] = abs((A.BB.Shock_run_t[i_nas] - A.BB.A_Q[i_nas]) / (A.BB.A_P[i_nas] + A.BB.A_IB_all[i_nas]) * A.BB.A_IB_all[i_nas])  # 计算应银行内冲击传导至银行间传染冲击
    Executer.update_variableStep('Shock_IB_run_ilq_s', A, para, sgv)  # 更新挤兑流动冲击源头变量Shock_run_t
    A.BB.Shock_P_run_s[i_nas] = abs((A.BB.Shock_run_t[i_nas] - A.BB.A_Q[i_nas]) / (A.BB.A_P[i_nas] + A.BB.A_IB_all[i_nas]) * A.BB.A_P[i_nas])  # 银行内冲击传导至银行厂商贷款传染冲击
    A.BB.is_allocated_Shock |= A.BB.ilq  # 更新已经分配传染冲击的银行
    for i in np.where(i_nas)[0]:  # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
        A.IB.Shock_IB_run_ilq[A.IB.deb_ilq[i], i] = A.IB.A_IB[i, A.IB.deb_ilq[i]] * A.BB.Shock_IB_run_ilq_s[i] / A.BB.A_IB_all[i]
        pass
    Executer.update_variableStep('Shock_IB_run_ilq', A, para, sgv)  # 更新挤兑流动冲击源头变量Shock_run_t

    # ##DEBUG 方式二：每个银行可以有多次分配传染冲击之行为。HACK 已经过时。没有适配。
    # A.BB.Shock_IB_run_ilq_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_IB_all[A.BB.ilq]) # 计算应银行内冲击传导至银行间传染冲击
    # update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way = 'Shock_IB_run_ilq_s') # 汇总各银行之流动性短缺流动性挤兑冲击
    # A.BB.Shock_P_run_s[A.BB.ilq] = abs((A.BB.Shock_run_t[A.BB.ilq] - A.BB.A_Q[A.BB.ilq]) / (A.BB.A_P[A.BB.ilq] + A.BB.A_IB_all[A.BB.ilq]) * A.BB.A_P[A.BB.ilq]) # 银行内冲击传导至银行厂商贷款传染冲击
    # for i in findall(A.BB.on) # 流动性短缺银行计划收回资产，导致其对各债务银行之资产变动，造成流动性短缺银行间挤兑流动冲击
    #     A.IB.Shock_IB_run_ilq[A.IB.deb[i], i] = A.IB.A_IB[i, A.IB.deb[i]] * A.BB.Shock_IB_run_ilq_s[i] / A.BB.A_IB_all[i]
    #     pass
    # update_B_Shock(A.BB, A.IB, A.b, A.ib, by_way = 'Shock_IB_run_ilq') # 加总各单个债务银行遭受总银行间挤兑流动冲击
    # update_states(target='illiquid', source='healthy') # 更新各银行之状态，从健康到流动性短缺

    return A, sgv
    pass  # function


def InterBankIlliquidAllocate(A: SystemicRiskAgent, para: dict, sgv: dict):
    """
    流动性短缺银行间挤兑流动分配借贷流量模型

    Args:
        A ():
        para ():
        sgv ():

    Returns:

    """

    sgv['turn'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
    sgv['phase'] = 1  # 逐相复位（起始为1）
    sgv['process_name'] = "InterBankIlliquidAllocate"

    logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

    Executer.update_variableStep('enabled collect A_P', A, para, sgv)  # 计算是否可以收回厂商贷款状态
    A.BB.Li_P[A.BB.is_enabled_LiP] = A.BB.Shock_P_run_s[A.BB.is_enabled_LiP]  # 计算银行收回厂商贷款流量
    Executer.update_variableStep('Li_P', A, para, sgv)

    Executer.update_variableStep('enabled repay Z_D', A, para, sgv)  # 计算是否需要偿还借款状态
    Executer.update_variableStep('enabled repay IB', A, para, sgv)  # 计算是否可以偿还银行间借款状态
    A.BB.Bo_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] = np.minimum(A.BB.A_Q[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD], A.BB.Shock_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD])  # 计算银行偿还借款总流量
    A.BB.Bo_D[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] = A.BB.Shock_D_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] * (A.BB.Bo_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] / A.BB.Shock_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD])  # 计算银行偿还居民借款流量
    A.BB.Bo_IB_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] = A.BB.Shock_IB_run_ilq_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] * (A.BB.Bo_all[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD] / A.BB.Shock_run_t[A.BB.is_enabled_BoIB | A.BB.is_enabled_BoD])  # 计算银行偿还银行间借款流量
    Executer.update_variableStep('Bo_D', A, para, sgv)  # HACK 这个必须放在这里！
    Executer.update_variableStep('Bo_IB_all', A, para, sgv)
    for i in np.where(A.BB.is_enabled_BoIB)[0]:  # 计算银行可以偿还各债权银行的借款流量
        A.IB.Bo_IB[i, A.IB.cre_ilq[i]] = A.IB.Shock_IB_run_ilq[i, A.IB.cre_ilq[i]] * (A.BB.Bo_IB_all[i] / A.BB.Shock_IB_run_ilq_t[i])
        pass
    Executer.update_variableStep('Bo_IB', A, para, sgv)

    return A, sgv
    pass  # function


def InterBankIlliquidRepay(A: SystemicRiskAgent, para: dict, sgv: dict):
    """
    流动性短缺银行间挤兑流动执行借贷流量模型

    Args:
        A ():
        para ():
        sgv ():

    Returns:

    """

    sgv['turn'] += 1  # 计次轮次数（由于开始轮次是`START`，所以记为0）
    sgv['phase'] = 1  # 逐相复位（起始为1）
    sgv['process_name'] = "InterBankIlliquidRepay"

    logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

    A.BB.A_Q[A.b], A.BB.A_P[A.b], A.BB.Shock_P_run_s[A.b] = Finance.transfer_B_capital_reverse(A.BB.A_Q[A.b], A.BB.A_P[A.b], A.BB.Shock_P_run_s[A.b], A.BB.Li_P[A.b])  # 流动资产变动，因收回厂商贷款
    Executer.update_variableStep('A_Q', A, para, sgv)
    Executer.update_variableStep('A_P', A, para, sgv)  # DEBUG 是否已经在自动更新功能计算过了，以至于重复计算了？
    Executer.update_variableStep('Shock_P_run_s', A, para, sgv)  # DEBUG 是否已经在自动更新功能计算过了，以至于重复计算了？

    A.BB.Z_D[A.b], A.BB.A_Q[A.b], A.BB.Shock_D_run_t[A.b] = Finance.transfer_B_capital_reduce(A.BB.Z_D[A.b], A.BB.A_Q[A.b], A.BB.Shock_D_run_t[A.b], A.BB.Bo_D[A.b])  # 流动资产变动，因偿还居民存款
    Executer.update_variableStep('Z_D', A, para, sgv)
    Executer.update_variableStep('A_Q', A, para, sgv)  # DEBUG 是否已经在自动更新功能计算过了，以至于重复计算了？
    Executer.update_variableStep('Shock_D_run_t', A, para, sgv)  # DEBUG 是否已经在自动更新功能计算过了，以至于重复计算了？

    A.IB.Shock_IB_run_ilq[A.ib] -= A.IB.Bo_IB[A.ib]  # 各银行间挤兑流动冲击变动，当偿还相应的银行间借款时
    Executer.update_variableStep('Shock_IB_run_ilq', A, para, sgv)
    A.BB.Shock_IB_run_ilq_s[A.b] -= A.BB.Li_IB_all[A.b]  # 各银行之银行间挤兑流动冲击源头变动，当收回相应的银行间贷款时
    Executer.update_variableStep('Shock_IB_run_ilq_s', A, para, sgv)
    A.IB.Z_IB[A.ib] -= A.IB.Bo_IB[A.ib]  # 各银行间负债变动，当偿还相应的银行间借款时
    Executer.update_variableStep('Z_IB', A, para, sgv)
    # # A.IB.A_IB[A.ib] += A.IB.Li_IB[A.ib]' # 各银行间资产变动，当收回相应的银行间贷款时
    A.BB.A_Q[A.b] += (A.BB.Li_IB_all[A.b] - A.BB.Bo_IB_all[A.b])  # 各银行流动资金变动，当收回相应的银行间贷款、偿还相应的银行间借款时
    Executer.update_variableStep('A_Q', A, para, sgv)

    # Executer.update_variableStep('clear transfer all', A, para, sgv)  # 清零所有不必要的借贷流量变量；

    return A, sgv
    pass  # function
