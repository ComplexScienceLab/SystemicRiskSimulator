"""
模型 IB1111 之主文件
"""

# import gymnasium as gym
from copy import deepcopy
import numpy as np
import logging

from SystemicRiskSimulator.core.define.define_type import *
from SystemicRiskSimulator.core.operations.collector import Collector
from SystemicRiskSimulator.core.operations.executer import Executer
from SystemicRiskSimulator.tools.tools import Tools


class ModelMain:
    """
    模型 IB1111
    """

    def __init__(
            self,
            model_dict: dict,
            A,
            A_data,
            para: dict,
            sgv: dict,
    ):
        """
        初始化环境

        Args:
            model_dict (dict): 模型字典，包括：

              - 'model_define',
              - 'model_finance',
              - 'model_main',

            A (ModelAgent): 多主体
            A_data (AgentDataCollection): 多主体之数据
            para (dict): 参数集
            sgv (dict): 模拟器全局变量
            model_content (): 模型内容函数
        """
        self.sgv = sgv
        self.A = A
        self.A_data = A_data
        self.para = para
        self.model_finance = model_dict['model_finance'](A.note.num_bank)  # 初始化 Content_Finance 之实例

        pass  # function

    def model_content(self):
        """
        模型之步进内容
        """

        # 当 step > 0 且满足继续的条件时，才进行模型的计算
        # if sgv['turn'] > 1 and (self.A.BB.inf.any() and sgv['is_continue_process']):
        if self.sgv['turn'] > 0:

            self.sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
            self.sgv['phase'] = 1  # 逐相复位（起始为1）
            self.sgv['process_name'] = "InterBankInsolventContagionShock"
            logging.debug(f"          轮次 {self.sgv['turn']}：模型 {self.sgv['process_name']}")

            ####################################################################################################

            # 银行间传染冲击阶段

            # 计算 Shock_IB_def
            self.A.IB.Shock_IB_def[self.A.BB.con, :] = np.where(
                self.A.BB.Z_IB_all[self.A.BB.con][:, np.newaxis] != 0,
                np.abs(self.A.BB.Shock_IB_def_s[self.A.BB.con, np.newaxis] * self.A.IB.Z_IB[self.A.BB.con, :] / self.A.BB.Z_IB_all[self.A.BB.con, np.newaxis]),
                0
            )
            # self.A.IB.Shock_IB_def[self.A.BB.isv, :] = np.where(np.abs(self.A.IB.Shock_IB_def[self.A.BB.isv, :]) > 1.0e0, self.A.IB.Shock_IB_def[self.A.BB.isv, :], 0.0)  # 如果出现冲击值很小，小于一个阈值的时候，那么就设置为0
            Executer.update_variableStep(self.model_finance, 'Shock_IB_def', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])

            Executer.update_variableStep(self.model_finance, 'clear all Shock_source', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 清零所有冲击源头变量 Shock_source

            self.A.BB.inf = ~self.A.BB.br & (self.A.BB.Shock_IB_def_t > 0.0)

            self.A.IB.Default_IB += self.A.IB.Shock_IB_def  # 更新 Default_IB

            self.A.IB.Loss_IB_def += self.A.IB.Shock_IB_def.T  # 计算 Loss_IB_def
            Executer.update_variableStep(self.model_finance, 'Loss_IB_def_t', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])

            # Executer.update_variableStep(self.model_finance, 'clear all Shock_source', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 清零所有冲击源头变量 Shock_source
            # Executer.update_variableStep(self.model_finance, 'clear all Shock_interbank', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 清零所有银行间冲击变量 Shock_IB

            # 资不抵债银行资产违约损失冲击模型 InterBankInsolventShock

            self.A.BB.Loss_IB_def_t += self.A.BB.Shock_IB_def_t  # 银行间违约损失冲击损失
            Executer.update_variableStep(self.model_finance, 'Loss_IB_def_t', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])

            # 临时记录 self.A.BB.Default_IB_def_s 、self.A.BB.Default_D_def_s 变动前的值
            Default_IB_def_s_last = self.A.BB.Default_IB_def_s.copy()
            Default_D_def_s_last = self.A.BB.Default_D_def_s.copy()

            self.A.BB.Default_IB_def_s[self.A.BB.inf] = np.minimum(np.maximum(self.A.BB.Loss_exIB_def_t[self.A.BB.inf] + self.A.BB.Loss_IB_def_t[self.A.BB.inf] - self.A.BB.E_all[self.A.BB.inf], 0), self.A.BB.Z_IB_all[self.A.BB.inf])  # 银行间违约量变动
            Executer.update_variableStep(self.model_finance, 'Default_IB_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 更新银行间违约量

            self.A.BB.Default_D_def_s[self.A.BB.inf] = np.maximum(self.A.BB.Loss_exIB_def_t[self.A.BB.inf] + self.A.BB.Loss_IB_def_t[self.A.BB.inf] - (self.A.BB.E_all[self.A.BB.inf] + self.A.BB.Z_IB_all[self.A.BB.inf]), 0)  # 商业银行对居民存款应违约量变动
            Executer.update_variableStep(self.model_finance, 'Default_D_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])

            self.A.BB.Shock_IB_def_s[self.A.BB.inf] = self.A.BB.Default_IB_def_s[self.A.BB.inf] - Default_IB_def_s_last[self.A.BB.inf]  # 计算银行内冲击传导至银行间传染冲击
            Executer.update_variableStep(self.model_finance, 'Shock_IB_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])

            self.A.BB.Shock_D_def_s[self.A.BB.inf] = self.A.BB.Default_D_def_s[self.A.BB.inf] - Default_D_def_s_last[self.A.BB.inf]  # 计算应银行内冲击传导至居民存款传染冲击
            Executer.update_variableStep(self.model_finance, 'Shock_D_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])
            # Collector.collect_agent_data(self.A, self.A_data, self.sgv, self.para, collect=None)

            # self.A.BB.con = (self.A.BB.isv != isv_last) | (self.A.BB.Shock_IB_def_s != Shock_IB_def_s_last)
            # self.A.BB.con = ~self.A.BB.br & self.A.BB.isv
            self.A.BB.con = ~self.A.BB.br & (self.A.BB.Shock_IB_def_s > 0.0)
            # logging.debug(f"          轮次 {self.sgv['turn']}：模型 {self.sgv['process_name']}，银行传染出去情况：{self.A.BB.con}")

            self.A.BB.br |= self.A.BB.isv  # 更新破产银行

            Executer.update_variableStep(self.model_finance, 'clear all Shock_target', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 清零所有冲击目标变量 Shock_target
            Executer.update_variableStep(self.model_finance, 'clear all Shock_interbank', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 清零所有银行间冲击变量 Shock_IB

        elif self.sgv['turn'] == 0:
            # node_START
            Executer.update_variableStep(self.model_finance, 'all', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 更新各银行之所有变量，在第一回合开始时

            # node_010 外部资产违约损失冲击
            self.sgv['process_name'] = "ExBankInsolventShock"
            self.sgv['turn'] += 1  # 回合数计次轮次数（由于开始轮次是`START`，所以记为0）
            self.sgv['phase'] = 1  # 逐相复位（起始为1）
            logging.debug(f"          轮次 {self.sgv['turn']}：模型 {self.sgv['process_name']}")

            self.A.BB.Shock_P_def_t = self.A.BB.A_P * np.array(self.para['Shock_exIB_def_t_percentage'])  # 厂商贷款违约损失冲击
            Executer.update_variableStep(self.model_finance, 'Shock_P_def_t', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 厂商贷款违约损失冲击传导至银行内资产冲击

            self.A.BB.inf = ~self.A.BB.br & (self.A.BB.Shock_P_def_t > 0.0)
            # logging.debug(f"          轮次 {self.sgv['turn']}：模型 {self.sgv['process_name']}，银行遭受感染情况：{self.A.BB.inf}")

            # 不再对破产的银行进行传染
            # self.A.BB.Z_other[~self.A.BB.br] += self.A.BB.Z_other[~self.A.BB.br] + self.A.BB.Z_all[self.A.BB.br]  # 破产清算

            self.A.BB.Loss_exIB_def_t[self.A.BB.inf] = self.A.BB.Shock_P_def_t[self.A.BB.inf]  # 非银行间违约损失冲击损失
            Executer.update_variableStep(self.model_finance, 'Loss_exIB_def_t', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])

            self.A.BB.Default_IB_def_s[self.A.BB.inf] += np.minimum(np.maximum(self.A.BB.Loss_exIB_def_t[self.A.BB.inf] + self.A.BB.Loss_IB_def_t[self.A.BB.inf] - self.A.BB.E_all[self.A.BB.inf], 0), self.A.BB.Z_IB_all[self.A.BB.inf])  # 银行间违约量变动
            Executer.update_variableStep(self.model_finance, 'Default_IB_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 更新银行间违约量

            self.A.BB.Default_D_def_s[self.A.BB.inf] = np.maximum(self.A.BB.Loss_exIB_def_t[self.A.BB.inf] + self.A.BB.Loss_IB_def_t[self.A.BB.inf] - (self.A.BB.E_all[self.A.BB.inf] + self.A.BB.Z_IB_all[self.A.BB.inf]), 0)  # 商业银行对居民存款应违约量变动
            Executer.update_variableStep(self.model_finance, 'Default_D_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 更新商业银行对居民存款应违约量

            self.A.BB.Shock_IB_def_s[self.A.BB.inf] = self.A.BB.Default_IB_def_s[self.A.BB.inf]  # 计算应银行内冲击传导至银行间传染冲击
            Executer.update_variableStep(self.model_finance, 'Shock_IB_def_s', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 更新违约损失冲击源头变量Shock_def_s

            self.A.BB.con = ~self.A.BB.br & (self.A.BB.Shock_IB_def_s > 0.0)
            logging.debug(f"          轮次 {self.sgv['turn']}：模型 {self.sgv['process_name']}，银行传染出去情况：{self.A.BB.con}")
            self.A.BB.br |= self.A.BB.isv  # 更新破产银行

            # Collector.collect_agent_data(self.A, self.A_data, self.sgv, self.para, collect=None)

            Executer.update_variableStep(self.model_finance, 'clear all Shock_target', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 清零所有冲击目标变量 Shock_target
            Executer.update_variableStep(self.model_finance, 'clear all Shock_interbank', self.A, self.A_data, self.para, self.sgv, is_collect=self.sgv['is_collect'], collect=self.sgv['collect'])  # 清零所有银行间冲击变量 Shock_IB

        else:
            raise ValueError("模型错误，需要修复！")
            pass  # if

        # node_END

        pass  # function

    def model_process(self):
        """
        处理模型的主函数，用于在给定环境中运行指定次数的实验，并根据实验参数执行相应的动作。

        Returns:
            None: 该函数不返回任何值，它通过修改传入的参数来更新状态。
        """
        self.model_content()  # 执行首轮轮次级别的步进更新

        while self.sgv['is_continue_process']:

            # 运行每一轮的环境
            self.model_content()  # 执行一次轮次级别的步进更新

            # 判断是否结束
            self.calc_dones()

            pass  # while

        pass  # function

    def calc_dones(self):
        """
        计算并更新个体的完成状态。

        如果个体在倒闭状态列表中，则将其完成状态设置为 True。

        Args:
            None

        Returns:
            None: 该函数不返回任何值，仅更新内部状态。
        """

        # 如果个体处于倒闭状态，则 done 是 True，否则即使没有倒闭但是都没有感染的，则其余个体之 done 也为 True。
        dones = np.full(self.A.note.num_bank, False)  # 初始化 dones 数组为 False
        dones[self.A.BB.br] = True
        if not self.A.BB.inf.any():
            dones[~self.A.BB.br] = True
            pass  # if

        logging.debug(f"            个体完成状态：{dones}")

        # 当模型运行到最大步数时，中断模型的运行
        truncations = np.full(self.A.note.num_bank, False)  # 初始化 truncations 数组为 False
        if self.sgv['step'] >= self.sgv['test_max_num_of_turn']:
            if self.sgv['is_develope_mode']:  # #HACK 只有在开发模式下才开启这个判断
                logging.error(f"实验{self.sgv['id_experiment']}，模型第{self.sgv['step']}步，模型未能收敛。请检查模型逻辑是否正确！！！")
                truncations[:] = True
                self.sgv['is_continue_process'] = False
            else:
                assert False, f"实验{self.sgv['id_experiment']}，模型第{self.sgv['step']}步，模型未能收敛，程序以非正常方式退出。"  # #BUG 如果遇到并行运行模式，会出现什么情况？
                pass  # if
            pass  # if

        if truncations.all() or dones.all():
            self.sgv['is_continue_process'] = False

        pass  # function

    pass  # class
