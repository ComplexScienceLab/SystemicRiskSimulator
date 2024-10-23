"""
模型 sample 01
"""

from SystemicRiskSimulator.external_packages import np, logging
from SystemicRiskSimulator.core.define.define_agents import SystemicRiskAgent
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.operations.executer import Executer
from .content_finance import Content_Finance


class Content_Model:
    """
    模型 sample 01
    """

    content_Finance: Content_Finance

    def __init__(self, content_Finance: Content_Finance):
        self.content_Finance = content_Finance
        pass  # function

    def model_content(self, A: SystemicRiskAgent, A_last: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        模型 sample 01

        Args:
            A (SystemicRiskAgent): 多主体
            A_last (SystemicRiskAgent): 上一回合的多主体
            A_data (AgentDataCollection): 多主体之数据
            para (dict): 参数集
            sgv (dict): 模拟器全局变量

        Returns:
            None
        """

        ## node_START
        Executer.update_variableStep(self.content_Finance, 'all', A, A_data, para, sgv)  # 更新各银行之所有变量，在第一回合开始时

        # node_010
        isv_last = A.BB.isv.copy()
        Shock_IB_def_s_last = A.BB.Shock_IB_def_s.copy()
        A, _, sgv = Executer.update_turnStep_by_ABM(self.ExBankInsolventShock, A, A_data, para, sgv)

        is_states_isv_changed = (A.BB.isv != isv_last)  # 各资不抵债状态变化情况
        logging.debug(f"各资不抵债状态变化情况：{is_states_isv_changed}，总的资不抵债状态变化情况：{is_states_isv_changed.any()}")
        while (
                (
                        is_states_isv_changed.any() or
                        (A.BB.Shock_IB_def_s != Shock_IB_def_s_last).any()
                ) and
                sgv['is_continue_process']
        ):
            # node_020
            isv_last = A.BB.isv.copy()
            Shock_IB_def_s_last = A.BB.Shock_IB_def_s.copy()
            A, _, sgv = Executer.update_turnStep_by_ABM(self.InterBankInsolventContagionShock, A, A_data, para, sgv)

            is_states_isv_changed = (A.BB.isv != isv_last)  # 各资不抵债状态变化情况
            logging.debug(f"各资不抵债状态变化情况：{is_states_isv_changed}，总的资不抵债状态变化情况：{is_states_isv_changed.any()}")
            pass  # while

        ## node_END

        pass  # function

    def ExBankInsolventShock(self, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        外部资产违约损失冲击模型

        Args:
            A ():
            para ():
            sgv ():

        Returns:

        """

        sgv['process_name'] = "ExBankInsolventShock"

        logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

        A.BB.Shock_P_def_t = A.BB.A_P * np.array(para['Shock_exIB_def_t_percentage'])  # 厂商贷款违约损失冲击
        Executer.update_variableStep(self.content_Finance, 'Shock_P_def_t', A, A_data, para, sgv)  # 厂商贷款违约损失冲击传导至银行内资产冲击

        A.BB.Loss_exIB_def_t[A.BB.on] = A.BB.Shock_P_def_t[A.BB.on]  # 非银行间违约损失冲击损失
        Executer.update_variableStep(self.content_Finance, 'Loss_exIB_def_t', A, A_data, para, sgv)

        A.BB.Default_IB_def_s[A.BB.isv] += np.minimum(np.maximum(A.BB.Loss_def_t[A.BB.isv] - A.BB.E_all[A.BB.isv], 0), A.BB.Z_IB_all[A.BB.isv])  # 银行间违约量变动
        Executer.update_variableStep(self.content_Finance, 'Default_IB_def_s', A, A_data, para, sgv)  # 更新银行间违约量

        A.BB.Default_D_def_s[A.BB.isv] = np.maximum(A.BB.Loss_def_t[A.BB.isv] - (A.BB.E_all[A.BB.isv] + A.BB.Z_IB_all[A.BB.isv]), 0)  # 商业银行对居民存款应违约量变动
        Executer.update_variableStep(self.content_Finance, 'Default_D_def_s', A, A_data, para, sgv)  # 更新商业银行对居民存款应违约量

        A.BB.Shock_IB_def_s[A.BB.isv] = A.BB.Default_IB_s[A.BB.isv]  # 计算应银行内冲击传导至银行间传染冲击
        Executer.update_variableStep(self.content_Finance, 'Shock_IB_def_s', A, A_data, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s

        A.BB.is_allocated_Shock |= A.BB.isv  # 更新已经分配传染冲击的银行示性向量

        Executer.update_variableStep(self.content_Finance, 'clear all Shock_target', A, A_data, para, sgv)  # 清零所有冲击目标变量 Shock_target

        return A, sgv
        pass  # function

    def InterBankInsolventContagionShock(self, A: SystemicRiskAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        资不抵债银行间违约损失传染冲击模型

        Args:
            A ():
            para ():
            sgv ():

        Returns:

        """

        sgv['process_name'] = "InterBankInsolventContagionShock"

        logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

        # 资不抵债银行间违约损失传染模型 InterBankInsolventContagion
        # # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击

        # 计算 Shock_IB_def
        A.IB.Shock_IB_def[A.BB.isv, :] = np.where(
            A.BB.Z_IB_all[A.BB.isv][:, np.newaxis] != 0,
            np.abs(A.BB.Shock_IB_def_s[A.BB.isv, np.newaxis] * A.IB.Z_IB[A.BB.isv, :] / A.BB.Z_IB_all[A.BB.isv, np.newaxis]),
            0
        )
        # 如果出现冲击值很小，小于一个阈值的时候，那么就设置为0
        A.IB.Shock_IB_def[A.BB.isv, :] = np.where(np.abs(A.IB.Shock_IB_def[A.BB.isv, :]) > 1.0e0, A.IB.Shock_IB_def[A.BB.isv, :], 0.0)
        Executer.update_variableStep(self.content_Finance, 'Shock_IB_def', A, A_data, para, sgv)

        A.IB.Default_IB += A.IB.Shock_IB_def  # 更新 Default_IB

        A.IB.Loss_IB_def += A.IB.Shock_IB_def.T  # 计算 Loss_IB_def
        Executer.update_variableStep(self.content_Finance, 'Loss_IB_def_t', A, A_data, para, sgv)

        Executer.update_variableStep(self.content_Finance, 'clear all Shock_source', A, A_data, para, sgv)  # 清零所有冲击源头变量 Shock_source
        Executer.update_variableStep(self.content_Finance, 'clear all Shock_interbank', A, A_data, para, sgv)  # 清零所有银行间冲击变量 Shock_IB

        # 资不抵债银行资产违约损失冲击模型 InterBankInsolventShock

        A.BB.Loss_IB_def_t += A.BB.Shock_IB_def_t  # 银行间违约损失冲击损失
        Executer.update_variableStep(self.content_Finance, 'Loss_IB_def_t', A, A_data, para, sgv)

        i_isv_nas = A.BB.Shock_IB_def_t[A.BB.on] > 0.0  # 临时设置示性变量，表示某一轮次遭受传染冲击的银行集合。每个银行允许有多次分配传染冲击之行为。

        # 临时记录 A.BB.Default_IB_def_s 、A.BB.Default_D_def_s 变动前的值
        Default_IB_def_s_last = A.BB.Default_IB_def_s.copy()
        Default_D_def_s_last = A.BB.Default_D_def_s.copy()

        A.BB.Default_IB_def_s[i_isv_nas] = np.minimum(np.maximum(A.BB.Loss_def_t[i_isv_nas] - A.BB.E_all[i_isv_nas], 0), A.BB.Z_IB_all[i_isv_nas])  # 银行间违约量变动
        Executer.update_variableStep(self.content_Finance, 'Default_IB_def_s', A, A_data, para, sgv)  # 更新银行间违约量

        A.BB.Default_D_def_s[i_isv_nas] = np.maximum(A.BB.Loss_def_t[i_isv_nas] - (A.BB.E_all[i_isv_nas] + A.BB.Z_IB_all[i_isv_nas]), 0)  # 商业银行对居民存款应违约量变动
        Executer.update_variableStep(self.content_Finance, 'Default_D_def_s', A, A_data, para, sgv)

        A.BB.Shock_IB_def_s[i_isv_nas] = A.BB.Default_IB_def_s[i_isv_nas] - Default_IB_def_s_last[i_isv_nas]  # 计算银行内冲击传导至银行间传染冲击
        Executer.update_variableStep(self.content_Finance, 'Shock_IB_def_s', A, A_data, para, sgv)

        A.BB.Shock_D_def_s[i_isv_nas] = A.BB.Default_D_def_s[i_isv_nas] - Default_D_def_s_last[i_isv_nas]  # 计算应银行内冲击传导至居民存款传染冲击
        Executer.update_variableStep(self.content_Finance, 'Shock_D_def_s', A, A_data, para, sgv)

        Executer.update_variableStep(self.content_Finance, 'clear all Shock_target', A, A_data, para, sgv)  # 清零所有冲击目标变量 Shock_target

        return A, sgv
        pass  # function

    pass  # class
