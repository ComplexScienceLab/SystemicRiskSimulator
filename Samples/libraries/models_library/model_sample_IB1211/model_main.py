"""
模型IB1211
"""

import numpy as np
import logging
from dataclasses import dataclass
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection
from SystemicRiskSimulator.core.operations.executer import Executer
from .model_finance import ModelFinance
from .model_define import ModelAgent


class ModelMain:
    """
    模型IB1211
    """

    model_finance: ModelFinance

    def __init__(self, model_finance: ModelFinance):
        self.model_finance = model_finance
        pass  # function

    def model_content(self, A: ModelAgent, A_data: AgentDataCollection, para: dict, sgv: dict):
        """
        模型IB1211

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

        A.DA.Shock_DA_def_t = A.DA.DA * np.array(para['Shock_DA_def_t_percentage'])  # 贷款资产之外生违约损失冲击

        A.DA.inf = A.DA.Shock_DA_def_t > 0.0  # 示性向量之贷款资产当前轮次遭受传染

        A.DA.p[A.DA.inf] = (A.DA.DA[A.DA.inf] - A.DA.Shock_DA_def_t[A.DA.inf]) / A.DA.DA[A.DA.inf]  # 贷款资产单位价格变动

        A.IBA.Shock_IBA_def[:, A.DA.inf] = A.IBA.IBA[:, A.DA.inf] * (1 - A.DA.p[A.DA.inf])  # 计算银行持有共同贷款类资产之违约损失冲击
        Executer.update_variableStep(self.model_finance, 'Shock_IBA_def', A, A_data, para, sgv)

        # 计算银行持有共同资产之损失量
        A.IBA.Loss_IBA += A.IBA.Shock_IBA_def
        A.BB.Loss_IBA_def_t += A.BB.Shock_IBA_def_t

        A.BB.Shock_P_def_t[A.BB.exist] = A.BB.Shock_IBA_def_t[A.BB.exist]  # 银行持有贷款类资产之违约损失冲击
        Executer.update_variableStep(self.model_finance, 'Shock_P_def_t', A, A_data, para, sgv)  # 厂商贷款违约损失冲击传导至银行内资产冲击

        A.BB.inf = ~A.BB.br & (A.BB.Shock_P_def_t > 0.0)
        logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}，银行遭受感染情况：{A.BB.inf}")

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

        ## node_015 外部资产违约损失冲击
        IDA_exp_factor = np.zeros((sgv['num_bank'], sgv['num_asset']))  # 银行持有贷款类资产之指数传染因子
        IDA_exp_factor[np.ix_(A.BB.inf, A.DA.inf)] = np.exp(-para['kappa_BA'] * A.IBA.IBA[np.ix_(A.BB.inf, A.DA.inf)] / np.maximum(np.sum(A.IBA.IBA[:, A.DA.inf], axis=0), 0.0001))  # 计算银行持有贷款类资产之指数传染因子

        A.BB.con = ~A.BB.br & (A.BB.Shock_IB_def_s > 0.0)
        logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}，银行传染出去情况：{A.BB.con}")
        A.BB.br |= A.BB.isv  # 更新破产银行

        Executer.update_variableStep(self.model_finance, 'clear all Shock_target', A, A_data, para, sgv)  # 清零所有冲击目标变量 Shock_target
        Executer.update_variableStep(self.model_finance, 'clear all Shock_interbank', A, A_data, para, sgv)  # 清零所有银行间冲击变量 Shock_IB

        while (A.BB.inf.any() and sgv['is_continue_process']):

            ## node_020 资不抵债银行间违约损失传染 InterBankInsolventContagion
            # # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击

            sgv['process_name'] = "InterBankInsolventContagionShock"
            sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
            sgv['phase'] = 1  # 逐相复位（起始为1）
            logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

            ####################################################################################################

            # 计算 Shock_IB_def
            A.IB.Shock_IB_def[A.BB.con, :] = np.where(
                A.BB.Z_IB_all[A.BB.con][:, np.newaxis] != 0,
                np.abs(A.BB.Shock_IB_def_s[A.BB.con, np.newaxis] * A.IB.Z_IB[A.BB.con, :] / A.BB.Z_IB_all[A.BB.con, np.newaxis]),
                0
            )
            # A.IB.Shock_IB_def[A.BB.isv, :] = np.where(np.abs(A.IB.Shock_IB_def[A.BB.isv, :]) > 1.0e0, A.IB.Shock_IB_def[A.BB.isv, :], 0.0)  # 如果出现冲击值很小，小于一个阈值的时候，那么就设置为0
            Executer.update_variableStep(self.model_finance, 'Shock_IB_def', A, A_data, para, sgv)

            Executer.update_variableStep(self.model_finance, 'clear all Shock_source', A, A_data, para, sgv)  # 清零所有冲击源头变量 Shock_source

            A.BB.inf = ~A.BB.br & (A.BB.Shock_IB_def_t > 0.0)
            logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}，银行遭受传染情况：{A.BB.inf}")

            if sgv['step'] >= sgv['test_max_num_of_turn']:
                if sgv['is_develope_mode']:  # #HACK 只有在开发模式下才开启这个判断
                    logging.error(f"实验{sgv['id_experiment']}，模型第{sgv['step']}步，模型未能收敛。请检查模型逻辑是否正确！！！")
                    sgv['is_continue_process'] = False
                else:
                    assert False, f"实验{sgv['id_experiment']}，模型第{sgv['step']}步，模型未能收敛，程序以非正常方式退出。"  # #BUG 如果遇到并行运行模式，会出现什么情况？
                    pass  # if
                pass  # if
            if not (A.BB.inf.any() and sgv['is_continue_process']):
                break
                pass  # if

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
            logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}，银行传染出去情况：{A.BB.con}")
            A.BB.br |= A.BB.isv  # 更新破产银行

            Executer.update_variableStep(self.model_finance, 'clear all Shock_target', A, A_data, para, sgv)  # 清零所有冲击目标变量 Shock_target
            Executer.update_variableStep(self.model_finance, 'clear all Shock_interbank', A, A_data, para, sgv)  # 清零所有银行间冲击变量 Shock_IB

            ## node_030 持有共同贷款资产价格损失冲击

            sgv['process_name'] = "HoldingCoLoanAssetPriceContagionShock"
            sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
            sgv['phase'] = 1  # 逐相复位（起始为1）
            logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}")

            # 计算银行持有贷款类资产之指数传染因子，从而得到银行持有贷款类资产之单价变动

            Executer.update_variableStep(self.model_finance, 'Shock_IBA_def', A, A_data, para, sgv)  # 计算银行持有共同贷款资产违约损失冲击目标

            A.IBA.IDA_exp_factor = np.zeros((sgv['num_bank'], sgv['num_asset']))  # 银行持有贷款类资产单价变动后的值
            A.IBA.IDA_exp_factor[np.ix_(A.BB.inf, A.DA.inf)] = np.exp(-para['kappa_BA'] * (A.IBA.IBA[np.ix_(A.BB.inf, A.DA.inf)] / A.DA.DA[A.DA.inf]))  # 计算银行持有贷款类资产之指数传染因子

            # 计算银行受到持有共同贷款资产价格损失冲击
            A.BB.Shock_IBA_def_t = np.zeros(sgv['num_bank'])
            A.IBA.Shock_IBA_def[:, A.DA.inf] = A.IBA.IBA[:, A.DA.inf] * (1 - A.IBA.IDA_exp_factor[np.ix_(A.BB.inf, A.DA.inf)]).sum(axis=0)  # 计算银行持有贷款类资产之冲击
            Executer.update_variableStep(self.model_finance, 'Shock_IBA_def', A, A_data, para, sgv)  # 更新银行持有共同贷款资产违约损失冲击

            # 计算银行持有共同资产之损失量
            A.IBA.Loss_IBA += A.IBA.Shock_IBA_def
            A.BB.Loss_IBA_def_t += A.BB.Shock_IBA_def_t

            A.IBA.IBA[:, A.DA.inf] = A.IBA.IBA[:, A.DA.inf] * np.prod(A.IBA.IDA_exp_factor[np.ix_(A.BB.inf, A.DA.inf)], axis=0)  # 计算银行持有贷款类资产

            Executer.update_variableStep(self.model_finance, 'IBA', A, A_data, para, sgv)  # 更新银行持有共同贷款资产

            # 更新示性向量之于银行当前轮次是否传染出去
            A.BB.con = ~A.BB.br & (A.BB.Shock_t > 0.0)
            logging.debug(f"          轮次 {sgv['turn']}：模型 {sgv['process_name']}，银行传染出去情况：{A.BB.con}")

            ###############################################################################################

            pass  # while

        ## node_END

        pass  # function

    pass  # class
