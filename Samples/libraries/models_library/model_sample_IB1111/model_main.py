"""
模型 sample 01
"""

import numpy as np
import logging
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.operations.executer import Executer
from .model_finance import ModelFinance
from .model_define import ModelAgent


class ModelMain:
    """
    模型 sample 01
    """

    model_finance: ModelFinance

    def __init__(self, model_finance: ModelFinance):
        self.model_finance = model_finance
        pass  # function

    def model_content(self, A: ModelAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        模型 sample 01

        Args:
            A (ModelAgent): 多主体
            A_data (AgentDataCollection): 多主体之数据
            para (dict): 参数集
            sgv (dict): 模拟器全局变量

        Returns:
            None

        """

        ## node_START
        Executer.update_variableStep(self.model_finance, 'all', A, A_data, para, sgv)  # 更新各银行之所有变量，在第一回合开始时

        ## node_010 外部资产违约损失冲击
        isv_last = A.BB.isv.copy()
        Shock_IB_def_s_last = A.BB.Shock_IB_def_s.copy()

        sgv['process_name'] = "ExBankInsolventShock"

        sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
        sgv['phase'] = 1  # 逐相复位（起始为1）

        logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

        A.BB.Shock_P_def_t = A.BB.A_P * np.array(para['Shock_exIB_def_t_percentage'])  # 厂商贷款违约损失冲击
        Executer.update_variableStep(self.model_finance, 'Shock_P_def_t', A, A_data, para, sgv)  # 厂商贷款违约损失冲击传导至银行内资产冲击

        A.BB.inf = ~A.BB.br & (A.BB.Shock_P_def_t > 0.0)

        # 不再对破产的银行进行传染
        # A.BB.Z_other[~A.BB.br] += A.BB.Z_other[~A.BB.br] + A.BB.Z_all[A.BB.br]  # 破产清算

        A.BB.Loss_exIB_def_t[A.BB.inf] = A.BB.Shock_P_def_t[A.BB.inf]  # 非银行间违约损失冲击损失
        Executer.update_variableStep(self.model_finance, 'Loss_exIB_def_t', A, A_data, para, sgv)

        A.BB.Default_IB_def_s[A.BB.inf] += np.minimum(np.maximum(A.BB.Loss_exIB_def_t[A.BB.inf] + A.BB.Loss_IB_def_t[A.BB.inf] - A.BB.E_all[A.BB.inf], 0), A.BB.Z_IB_all[A.BB.inf])  # 银行间违约量变动
        Executer.update_variableStep(self.model_finance, 'Default_IB_def_s', A, A_data, para, sgv)  # 更新银行间违约量

        A.BB.Default_D_def_s[A.BB.inf] = np.maximum(A.BB.Loss_exIB_def_t[A.BB.inf] + A.BB.Loss_IB_def_t[A.BB.inf] - (A.BB.E_all[A.BB.inf] + A.BB.Z_IB_all[A.BB.inf]), 0)  # 商业银行对居民存款应违约量变动
        Executer.update_variableStep(self.model_finance, 'Default_D_def_s', A, A_data, para, sgv)  # 更新商业银行对居民存款应违约量

        A.BB.Shock_IB_def_s[A.BB.inf] = A.BB.Default_IB_def_s[A.BB.inf]  # 计算应银行内冲击传导至银行间传染冲击
        Executer.update_variableStep(self.model_finance, 'Shock_IB_def_s', A, A_data, para, sgv)  # 更新违约损失冲击源头变量Shock_def_s

        # A.BB.con = (A.BB.isv != isv_last) | (A.BB.Shock_IB_def_s != Shock_IB_def_s_last)
        # A.BB.con = ~A.BB.br & A.BB.isv
        A.BB.con = ~A.BB.br & (A.BB.Shock_IB_def_s > 0.0)
        A.BB.br |= A.BB.isv  # 更新破产银行

        Executer.update_variableStep(self.model_finance, 'clear all Shock_target', A, A_data, para, sgv)  # 清零所有冲击目标变量 Shock_target
        Executer.update_variableStep(self.model_finance, 'clear all Shock_interbank', A, A_data, para, sgv)  # 清零所有银行间冲击变量 Shock_IB

        # is_states_isv_changed = (A.BB.isv != isv_last)  # 各资不抵债状态变化情况
        # logging.debug(f"各资不抵债状态变化情况：{is_states_isv_changed}，总的资不抵债状态变化情况：{is_states_isv_changed.any()}")
        while (A.BB.inf.any() and sgv['is_continue_process']):

            if sgv['step'] >= sgv['test_max_num_of_turn']:
                if sgv['is_develope_mode']:  # #HACK 只有在开发模式下才开启这个判断
                    logging.error(f"实验{sgv['id_experiment']}，模型第{sgv['step']}步，模型未能收敛。请检查模型逻辑是否正确！！！")
                    sgv['is_continue_process'] = False
                else:
                    assert False, f"实验{sgv['id_experiment']}，模型第{sgv['step']}步，模型未能收敛，程序以非正常方式退出。"  # #BUG 如果遇到并行运行模式，会出现什么情况？
                    pass  # if
                pass  # if

            ## node_020 资不抵债银行间违约损失传染 InterBankInsolventContagion
            # # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击

            sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
            sgv['phase'] = 1  # 逐相复位（起始为1）

            # isv_last = A.BB.isv.copy()
            # Shock_IB_def_s_last = A.BB.Shock_IB_def_s.copy()

            sgv['process_name'] = "InterBankInsolventContagionShock"

            logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

            ####################################################################################################

            # 计算 Shock_IB_def
            A.IB.Shock_IB_def[A.BB.con, :] = np.where(
                A.BB.Z_IB_all[A.BB.con][:, np.newaxis] != 0,
                np.abs(A.BB.Shock_IB_def_s[A.BB.con, np.newaxis] * A.IB.Z_IB[A.BB.con, :] / A.BB.Z_IB_all[A.BB.con, np.newaxis]),
                0
            )
            Executer.update_variableStep(self.model_finance, 'Shock_IB_def', A, A_data, para, sgv)

            Executer.update_variableStep(self.model_finance, 'clear all Shock_source', A, A_data, para, sgv)  # 清零所有冲击源头变量 Shock_source

            A.BB.inf = ~A.BB.br & (A.BB.Shock_IB_def_t > 0.0)

            A.IB.Default_IB += A.IB.Shock_IB_def  # 更新 Default_IB

            A.IB.Loss_IB_def += A.IB.Shock_IB_def.T  # 计算 Loss_IB_def
            Executer.update_variableStep(self.model_finance, 'Loss_IB_def_t', A, A_data, para, sgv)

            # 资不抵债银行资产违约损失冲击模型 InterBankInsolventShock

            A.BB.Loss_IB_def_t += A.BB.Shock_IB_def_t  # 银行间违约损失冲击损失
            Executer.update_variableStep(self.model_finance, 'Loss_IB_def_t', A, A_data, para, sgv)

            # 临时记录 A.BB.Default_IB_def_s 、A.BB.Default_D_def_s 变动前的值
            Default_IB_def_s_last = A.BB.Default_IB_def_s.copy()
            Default_D_def_s_last = A.BB.Default_D_def_s.copy()

            A.BB.Default_IB_def_s[A.BB.inf] = np.minimum(np.maximum(A.BB.Loss_exIB_def_t[A.BB.inf] + A.BB.Loss_IB_def_t[A.BB.inf] - A.BB.E_all[A.BB.inf], 0), A.BB.Z_IB_all[A.BB.inf])  # 银行间违约量变动
            Executer.update_variableStep(self.model_finance, 'Default_IB_def_s', A, A_data, para, sgv)  # 更新银行间违约量

            A.BB.Default_D_def_s[A.BB.inf] = np.maximum(A.BB.Loss_exIB_def_t[A.BB.inf] + A.BB.Loss_IB_def_t[A.BB.inf] - (A.BB.E_all[A.BB.inf] + A.BB.Z_IB_all[A.BB.inf]), 0)  # 商业银行对居民存款应违约量变动
            Executer.update_variableStep(self.model_finance, 'Default_D_def_s', A, A_data, para, sgv)

            A.BB.Shock_IB_def_s[A.BB.inf] = A.BB.Default_IB_def_s[A.BB.inf] - Default_IB_def_s_last[A.BB.inf]  # 计算银行内冲击传导至银行间传染冲击
            Executer.update_variableStep(self.model_finance, 'Shock_IB_def_s', A, A_data, para, sgv)

            A.BB.Shock_D_def_s[A.BB.inf] = A.BB.Default_D_def_s[A.BB.inf] - Default_D_def_s_last[A.BB.inf]  # 计算应银行内冲击传导至居民存款传染冲击
            Executer.update_variableStep(self.model_finance, 'Shock_D_def_s', A, A_data, para, sgv)

            A.BB.con = ~A.BB.br & (A.BB.Shock_IB_def_s > 0.0)
            A.BB.br |= A.BB.isv  # 更新破产银行

            Executer.update_variableStep(self.model_finance, 'clear all Shock_target', A, A_data, para, sgv)  # 清零所有冲击目标变量 Shock_target
            Executer.update_variableStep(self.model_finance, 'clear all Shock_interbank', A, A_data, para, sgv)  # 清零所有银行间冲击变量 Shock_IB

            ###############################################################################################

            pass  # while

        ## node_END

        pass  # function

    pass  # class
