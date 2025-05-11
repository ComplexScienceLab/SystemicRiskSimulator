import numpy as np
from copy import deepcopy
import logging
from .model_define import ModelAgent
from SystemicRiskSimulator.core.define.define_type import StateType


class ModelFinance:
    """
    财务相关的功能。
    """

    def __init__(self, num_bank: int):
        self.num_bank = num_bank
        pass

    ## NOTE：功能函数集：计算冲击。

    def together_Shock_target(self, A: ModelAgent):
        """汇总冲击目标"""
        # state = A.BB.exist | A.BB.exit
        A.BB.Shock_t[A.BB.exist] = A.BB.Shock_P_def_t[A.BB.exist] + A.BB.Shock_IB_def_t[A.BB.exist]
        logging.debug(f"                    together_Shock_target")
        pass  # function

    def together_Shock_source(self, A: ModelAgent):
        """汇总冲击源头"""
        # state = A.BB.exist | A.BB.exit
        A.BB.Shock_s[A.BB.exist] = A.BB.Shock_D_def_s[A.BB.exist]
        logging.debug(f"                    together_Shock_source")
        pass  # function

    def together_Shock_IB(self, A: ModelAgent):
        """汇总银行间冲击。"""
        # state = np.outer((A.BB.exist | A.BB.exit), (A.BB.exist | A.BB.exit))
        state = np.outer(A.BB.exist, A.BB.exist)
        A.IB.Shock_IB[state] = A.IB.Shock_IB_def[state]
        logging.debug(f"                    together_Shock_IB")
        pass  # function

    def sum_Shock_IB_def_target(self, A: ModelAgent):
        """汇总资不抵债银行之银行间违约损失冲击目标。"""
        A.BB.Shock_IB_def_t[A.BB.exist] = np.sum(A.IB.Shock_IB_def * A.IB.exist, axis=0)[A.BB.exist]
        logging.debug(f"                    sum_Shock_IB_def_target")
        pass  # function

    def clear_Shock_IB_and_exIB(self, A: ModelAgent):  # BUG是否会出现乱清零的麻烦？
        """清零本回合结束时所有不必要的冲击变量"""
        A.BB.Shock_P_def_t = np.zeros(self.num_bank)
        A.BB.Shock_D_def_s = np.zeros(self.num_bank)
        A.BB.Shock_IB_def_s = np.zeros(self.num_bank)
        A.IB.Shock_IB_def = np.zeros((self.num_bank, self.num_bank))
        A.BB.Shock_IB_def_t = np.zeros(self.num_bank)
        logging.debug(f"                    clear_Shock_IB_and_exIB")
        pass  # function

    def clear_Shock_target(self, A: ModelAgent):
        """清零所有不必要的目标冲击变量"""
        A.BB.Shock_IB_def_t = np.zeros(self.num_bank)
        A.BB.Shock_P_def_t = np.zeros(self.num_bank)
        logging.debug(f"                    clear_Shock_target")
        pass  # function

    def clear_Shock_source(self, A: ModelAgent):
        """清零所有不必要的源头冲击变量"""
        A.BB.Shock_D_def_s = np.zeros(self.num_bank)
        A.BB.Shock_IB_def_s = np.zeros(self.num_bank)
        logging.debug(f"                    clear_Shock_source")
        pass  # function

    def clear_Shock_IB(self, A: ModelAgent):
        """清零所有不必要的银行间冲击变量"""
        A.IB.Shock_IB_def = np.zeros((self.num_bank, self.num_bank))
        logging.debug(f"                    clear_Shock_IB")
        pass  # function

    def clear_Shock_inB(self, A: ModelAgent):
        """清零本回合中期所有不必要的冲击变量"""  # HACK无用
        A.BB.Shock_B_A = np.zeros(self.num_bank)
        A.BB.Shock_B_Z = np.zeros(self.num_bank)
        logging.debug(f"                    clear_Shock_inB")
        pass  # function

    ## NOTE：功能函数集：计算损失。

    def together_Loss_target(self, A: ModelAgent):
        """汇总各银行之总损失目标，通过部门类型"""
        A.BB.Loss_t[A.BB.exist] = A.BB.Loss_exIB_def_t[A.BB.exist] + A.BB.Loss_IB_def_t[A.BB.exist]
        logging.debug(f"                    together_Loss_target")
        pass  # function

    ## NOTE：功能函数集：计算违约。

    def together_Default_source(self, A: ModelAgent):
        """汇总银行之总违约源头"""
        A.BB.Default_s[A.BB.exist] = A.BB.Default_IB_def_s[A.BB.exist] + A.BB.Default_D_def_s[A.BB.exist]
        logging.debug(f"                    together_Default_source")
        pass  # function

    ## NOTE：功能函数集：计算商业银行之资产负债表结构。

    def together_B_A_all(self, A: ModelAgent):
        """汇总各银行之总资产。"""
        A.BB.A_all[A.BB.exist] = A.BB.A_IB_all[A.BB.exist] + A.BB.A_P[A.BB.exist] + A.BB.A_Q[A.BB.exist] + A.BB.A_R[A.BB.exist] + A.BB.A_other[A.BB.exist]
        logging.debug(f"                    together_B_A_all")
        pass  # function

    def sum_B_A_IB(self, A: ModelAgent):
        """加总各银行之银行间总资产，通过银行间资产邻接矩阵。"""
        # state = A.BB.exist | A.BB.exit
        # interstate = np.outer(state, state)
        state = np.outer(A.BB.exist, A.BB.exist)
        A.BB.A_IB_all[A.BB.exist] = np.sum(A.IB.A_IB * state, axis=1)
        logging.debug(f"                    sum_B_A_IB")
        pass  # function

    def together_B_Z_all(self, A: ModelAgent):
        """汇总各银行之总负债。"""
        A.BB.Z_all[A.BB.exist] = A.BB.Z_IB_all[A.BB.exist] + A.BB.Z_D[A.BB.exist] + A.BB.Z_CB[A.BB.exist] + A.BB.Z_other[A.BB.exist]
        logging.debug(f"                    together_B_Z_all")
        pass  # function

    def sum_B_Z_IB(self, A: ModelAgent):
        """加总各银行之银行间总负债，通过银行间负债邻接矩阵。"""
        # state = A.BB.exist | A.BB.exit
        # interstate = np.outer(state, state)
        state = np.outer(A.BB.exist, A.BB.exist)
        A.BB.Z_IB_all[A.BB.exist] = np.sum(A.IB.Z_IB * state, axis=1)
        logging.debug(f"                    sum_B_Z_IB")
        pass  # function

    def calc_B_E_all(self, A: ModelAgent):  # BUG是否考虑E_all负数？还是手动计算？
        """计算各银行之所有者权益``E_{B}``，通过总资产与总负债差值。#DEBUG"""
        A.BB.E_all[A.BB.exist] = A.BB.A_all[A.BB.exist] - A.BB.Z_all[A.BB.exist] - (np.zeros(self.num_bank) + 0.0001)[A.BB.exist]  # 允许E_all为负数
        logging.debug(f"                    calc_B_E_all")
        pass  # function

    def alter_Z_IB(self, A: ModelAgent):
        """转换银行间负债为资产。"""
        A.IB.A_IB = A.IB.Z_IB.T
        logging.debug(f"                    alter_Z_IB")
        pass  # function

    def alter_A_IB(self, A: ModelAgent):
        """转换银行间资产为负债。"""
        A.IB.Z_IB = A.IB.A_IB.T
        logging.debug(f"                    alter_A_IB")
        pass  # function

    ## NOTE：功能函数集：银行与银行间相关状态及其转换。

    def calc_state_exist(self, A: ModelAgent):
        """计算示性向量之于银行存在的。"""
        result = (A.BB.hel | A.BB.isv | A.BB.br)
        source_state_changes = (A.BB.exist != result)
        A.BB.exist = result
        A.IB.exist = np.outer(A.BB.exist, A.BB.exist)
        logging.debug(f"                    calc_state_exist")
        return source_state_changes
        pass  # function

    def calc_state_healthy(self, A: ModelAgent):
        """计算示性向量之于银行健康的。"""
        result = (
                (A.BB.E_all >= np.zeros(self.num_bank) + 0.0001) &
                (A.BB.A_Q >= np.zeros(self.num_bank) + 0.0001) &
                # (A.BB.Shock_def_t + (np.zeros(self.num_bank) + 0.0001) <= A.BB.E_all) &
                # (A.BB.Default + (np.zeros(self.num_bank) + 0.0001) <= A.BB.E_all) &
                (A.BB.Loss_t + (np.zeros(self.num_bank) + 0.0001) <= A.BB.E_all) &
                (A.BB.exist)
        )
        source_state_changes = (A.BB.hel != result)
        A.BB.hel = result
        A.IB.hel = np.outer(A.BB.hel, A.BB.hel)
        logging.debug(f"                    calc_state_healthy")
        return source_state_changes
        pass  # function

    def calc_state_insolvent(self, A: ModelAgent):
        """计算示性向量之于银行资不抵债的。#BUG"""
        result = (
                (
                        (A.BB.A_all < A.BB.Z_all + np.zeros(self.num_bank) + 0.0001) |
                        (A.BB.E_all < np.zeros(self.num_bank) + 0.0001) |
                        # (A.BB.Shock_def_t + (np.zeros(self.num_bank) + 0.0001) > A.BB.E_all) |
                        # (A.BB.Default + (np.zeros(self.num_bank) + 0.0001) > A.BB.E_all) |
                        (A.BB.Loss_t + (np.zeros(self.num_bank) + 0.0001) > A.BB.E_all)
                ) &
                (A.BB.exist)
        )
        source_state_changes = (A.BB.isv != result)
        A.BB.isv = result
        A.IB.isv = np.outer(A.BB.isv, A.BB.isv)
        logging.debug(f"                    calc_state_insolvent")
        return source_state_changes
        pass  # function

    def calc_state_bankrupt(self, A: ModelAgent):
        """计算示性向量之于银行破产的。"""
        result = (A.BB.isv)  # TODO 这个仅仅是目前基准模型简化的做法
        source_state_changes = (A.BB.br != result)
        A.BB.br = result
        A.IB.br = np.outer(A.BB.br, A.BB.br)
        logging.debug(f"                    calc_state_bankrupt")
        return source_state_changes
        pass  # function

    def calc_state_exit(self, A: ModelAgent):
        """计算示性向量之于银行退出的。"""
        result = A.BB.br | A.BB.exit
        source_state_changes = (A.BB.exit != result)
        A.BB.exit = result
        A.IB.exit = np.outer(A.BB.exit, A.BB.exit)
        logging.debug(f"                    calc_state_exit")
        return source_state_changes
        pass  # function

    ## NOTE：功能函数集：计算状态功能
    ## #NOTE 以下的几个计算函数将在模型内容中单独使用，不用于联动同步计算。

    def update_state_healthy_from_insolvent(self, A, source_state_changes: StateType):
        """更新示性向量之于银行健康的，从资不抵债的。"""
        A.BB.hel[source_state_changes] = ~(A.BB.isv[source_state_changes])
        A.IB.hel = np.outer(A.BB.hel, A.BB.hel)
        logging.debug(f"                    update_state_healthy_from_insolvent")
        pass  # function

    def update_state_exist_from_exit(self, A, source_state_changes: StateType):
        """更新示性向量之于银行存在的，从退出的。"""
        A.BB.exist[source_state_changes] = ~A.BB.exit[source_state_changes]
        A.IB.exist = np.outer(A.BB.exist, A.BB.exist)
        logging.debug(f"                    update_state_exist_from_exit")
        pass  # function

    def calc_list_of_creditor_in_state_of_banks(self, A, isState: StateType):
        """计算指定的状态的银行之债权方银行示性矩阵。"""

        # 计算示性矩阵之于银行间风险敞口的
        is_exposure_of_creditor_in_state_of_banks = ((A.IB.Z_IB > 0.0) & isState[:, np.newaxis])
        logging.debug(f"                    calc_list_of_creditor_in_state_of_banks")
        return is_exposure_of_creditor_in_state_of_banks
        pass  # function

    def calc_list_of_debtor_in_state_of_banks(self, A, isState: StateType):
        """计算指定的状态的银行之债务方银行示性矩阵。"""

        # 计算示性矩阵之于银行间风险敞口的
        is_exposure_of_debtor_in_state_of_banks = ((A.IB.A_IB > 0.0) & isState[:, np.newaxis])
        logging.debug(f"                    calc_list_of_debtor_in_state_of_banks")
        return is_exposure_of_debtor_in_state_of_banks

        pass  # function

    def update_relation_in_state_of_banks(self, A: ModelAgent):
        """更新银行间市场interbank之各状态下之信息列表之于各银行之债权方与债务方之银行编号。#BUG #HACK 这个没有用到"""
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.cre_br = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.br)
        A.IB.deb_br = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.br)
        logging.debug(f"                    update_relation_in_state_of_banks")
        pass  # function

    ## NOTE 其他功能部分

    ## NOTE：功能函数集：更新流之冲击变量。

    def update_by_Shock_P_def_t(self, A: ModelAgent):
        self.together_Shock_target(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_Shock_D_def_s(self, A: ModelAgent):
        self.together_Shock_source(A)
        pass  # function

    def update_by_Shock_IB_def_s(self, A: ModelAgent):
        self.together_Shock_source(A)
        pass  # function

    def update_by_Shock_IB_def(self, A: ModelAgent):
        self.together_Shock_IB(A)
        self.sum_Shock_IB_def_target(A)
        self.together_Shock_target(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_Shock_IB_def_t(self, A: ModelAgent):
        self.together_Shock_target(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_clear_Shock_IB_and_Shock_exIB(self, A: ModelAgent):
        self.clear_Shock_IB_and_exIB(A)
        self.together_Shock_source(A)
        self.together_Shock_IB(A)
        self.together_Shock_target(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        _ = self.calc_state_exist(A)  # by_way='all'
        _ = self.calc_state_healthy(A)
        _ = self.calc_state_insolvent(A)
        _ = self.calc_state_bankrupt(A)
        _ = self.calc_state_exit(A)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_clear_all_Shock_t(self, A: ModelAgent):
        self.clear_Shock_target(A)
        self.together_Shock_target(A)
        pass  # function

    def update_by_clear_all_Shock_s(self, A: ModelAgent):
        self.clear_Shock_source(A)
        self.together_Shock_source(A)
        pass  # function

    def update_by_clear_all_Shock_IB(self, A: ModelAgent):
        self.clear_Shock_IB(A)
        self.together_Shock_IB(A)
        pass  # function

    ## NOTE：功能函数集：更新流之损失变量。

    def update_by_Loss_exIB_def_t(self, A: ModelAgent):
        self.together_Loss_target(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        pass  # function

    def update_by_Loss_IB_def_t(self, A: ModelAgent):
        self.together_Loss_target(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        pass  # function

    ## NOTE：功能函数集：更新流之违约变量。

    def update_by_Default_D_def_s(self, A: ModelAgent):
        self.together_Default_source(A)
        pass  # function

    def update_by_Default_IB_def_s(self, A: ModelAgent):
        self.together_Default_source(A)
        pass  # function

    ## NOTE：功能函数集：计算流之商业银行之资产负债表变量。

    def update_by_A_P(self, A: ModelAgent):
        self.together_B_A_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_A_R(self, A: ModelAgent):
        self.together_B_A_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_A_other(self, A: ModelAgent):
        self.together_B_A_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_A_Q(self, A: ModelAgent):
        self.together_B_A_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_A_IB_all(self, A: ModelAgent):
        self.together_B_A_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        source_state_changes = self.calc_state_insolvent(A)
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_Z_D(self, A: ModelAgent):
        self.together_B_Z_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_Z_CB(self, A: ModelAgent):
        self.together_B_Z_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_Z_other(self, A: ModelAgent):
        self.together_B_Z_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_Z_IB_all(self, A: ModelAgent):
        self.together_B_Z_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_A_IB(self, A: ModelAgent):
        self.alter_A_IB(A)
        self.sum_B_A_IB(A)
        self.together_B_A_all(A)
        self.sum_B_Z_IB(A)
        self.together_B_Z_all(A)
        self.calc_B_E_all(A)
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    def update_by_Z_IB(self, A: ModelAgent):
        self.alter_Z_IB(A)
        self.sum_B_Z_IB(A)
        self.together_B_Z_all(A)
        self.sum_B_A_IB(A)
        self.together_B_A_all(A)
        self.calc_B_E_all(A)  # DEBUG 检查是否正确。
        source_state_changes = self.calc_state_insolvent(A)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(A, source_state_changes)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    ## NOTE：功能函数集：更新流之全部变量

    def update_by_all(self, A: ModelAgent):
        self.together_Shock_source(A)
        self.together_Shock_IB(A)
        self.sum_Shock_IB_def_target(A)
        self.together_Shock_target(A)
        self.sum_B_A_IB(A)
        self.together_B_A_all(A)
        self.sum_B_Z_IB(A)
        self.together_B_Z_all(A)
        self.calc_B_E_all(A)
        _ = self.calc_state_exist(A)  # by_way='all'
        _ = self.calc_state_healthy(A)
        _ = self.calc_state_insolvent(A)
        _ = self.calc_state_bankrupt(A)
        _ = self.calc_state_exit(A)
        A.IB.cre_isv = self.calc_list_of_creditor_in_state_of_banks(A, isState=A.BB.isv)
        A.IB.deb_isv = self.calc_list_of_debtor_in_state_of_banks(A, isState=A.BB.isv)
        pass  # function

    ## NOTE：功能函数集：其他

    def get_update_variable(self, A: ModelAgent):
        ## 监测财务变量变化。只能产生一个变动的变量 #HACK 似乎没有用
        # global update_variable_name
        bank_last = deepcopy(A.BB)
        interbank_last = deepcopy(A)
        for k, v in A.BB.__dict__.items():
            if (v != bank_last.__dict__[k]).any():
                self.update_variable_name, self.update_variable_value = k, v
        for k, v in A.IB.__dict__.items():
            if (v.dtype != list) and (v != interbank_last.__dict__[k]).any():
                self.update_variable_name, self.update_variable_value = k, v
            else:
                self.update_variable_name, self.update_variable_value = k, v
            pass  # for
        pass  # function

    ## NOTE 总的金融变量更新部分（主入口）

    def update_variables(self, A, by_way: str = 'all'):
        """
        更新各银行之借贷流量变量。

        - 总体部分：
            - ``all``:  更新全部冲击变量、各银行之所有资产负债表变量、各银行之状态变量；

        - 商业银行之冲击部分：

            - ``clear Shock_IB and Shock_exIB``:  清零本回合结束时，除了``Shock_{B}``系列的变量以外的，所有不必要的冲击变量，暨所有``Shock_{IB}``系列的变量、``Shock_{exIB}``系列的变量；
            - ``clear Shock_B_A and Shock_B_Z``:  清零银行内资产负债冲击变量；#HACK无用
            - ``Shock_P_def_t``:  已知``Shock_{P,def}[i]``，更新其余冲击变量；
            - ``Shock_D_def_s``:  已知``Shock_{D,def}[i]``，更新其余冲击变量；
            - ``Shock_B_A``:  已知``Shock_{B,b}``，更新其余冲击变量；
            - ``Shock_B_Z``:  已知``Shock_{B,Z}``，更新其余冲击变量；
            - ``Shock_IB_def_s``:  已知``Shock_{IB,def}[: ,i_{isv}]``，更新其余冲击变量；
            - ``Shock_IB_def``:  已知``Shock_{IB,def}[j,i_{isv}]``，更新其余冲击变量；
            - ``Shock_IB_def_t``:  已知``Shock_{IB,def}[j,: }],:  \\in i_{isv}``，更新其余冲击变量；
            - ``clear all Shock_target``:  清零所有的目标冲击变量；
            - ``clear all Shock_source``:  清零所有的源头冲击变量；
            - ``clear all Shock_interbank``:  清零所有的银行间冲击变量；

        - 商业银行之损失部分：

            - ``Loss_exIB_def_t``: 已知``Loss_{-IB,def}[i_{isv},:]``，更新相关的损失变量；
            - ``Loss_IB_def_t``: 已知``Loss_{IB,def}[i_{isv},:]``，更新相关的损失变量；
            - ``Loss_IB_t``: 已知``Loss_{IB}[i_{isv},:]``，更新相关的损失变量；
            - ``Loss_def_t``: 已知``Loss_{def}[i_{isv},:]``，更新相关的损失变量；

        - 商业银行之违约部分：

            - ``Default_IB_def_s``:  已知``Default_{IB,def}[i_{isv}]``，更新其余违约变量；

        - 商业银行之资产负债表部分：

            - ``A_exIB``:  已知``A_{-IB}``，更新各银行之其余相关的资产负债表变量；
            - ``A_P``:  已知``L_{-IB}``，更新各银行之其余相关的资产负债表变量；
            - ``A_Q``:  已知``Q_{B}``，更新各银行之其余相关的资产负债表变量；
            - ``A_R``:  已知``R_{B}``，更新各银行之其余相关的资产负债表变量；
            - ``A_other``:  已知``A_{other}``，更新各银行之其余相关的资产负债表变量；
            - ``A_IB_all``:  已知``A_{IB}[i,: ]``，更新各银行之其余相关的资产负债表变量；
            - ``Z_exIB``:  已知``Z_{exIB}``，更新各银行之其余相关的资产负债表变量；
            - ``Z_D``:  已知``D_{B}``，更新各银行之其余相关的资产负债表变量；
            - ``Z_CB``:  已知``Z_{CB}``，更新各银行之其余相关的资产负债表变量；
            - ``Z_other``:  已知``Z_{other}``，更新各银行之其余相关的资产负债表变量；
            - ``Z_IB_all``:  已知``Z_{IB}[i,: ]``，更新各银行之其余相关的资产负债表变量；
            - ``E_all and Z_all``:  已知``E_{B}``和``Z_{B}``，更新各银行之其余相关的资产负债表变量；
            - ``E_all and A_all``:  已知``E_{B}``和``A_{B}``，更新各银行之其余相关的资产负债表变量；
            - ``calc all E_all``:  已知``A_{B}``和``Z_{B}``，更新计算所有银行之所有者权益``E_{B}``；
            - ``sum A_IB``:  已知``A_{IB}[i,j]``，加总各银行变量``A_{IB}[i,: ]``；
            - ``sum Z_IB``:  已知``Z_{IB}[i,j]``，加总各银行变量``Z_{IB}[i,: ]``；
            - ``alter to Z_IB from A_IB``:  已知``A_{IB}[i,j]``，转换得到``Z_{IB}[i,j]``；
            - ``alter to A_IB from Z_IB``:  已知``Z_{IB}[i,j]``，转换得到``A_{IB}[i,j]``；

        Args:
            A (ModelAgent): 金融系统模型个体群，包含了金融系统的全部个体群变量。
            by_way (str): 参数，通过该参数指定的变量作为已知变量，驱动，以更新其他相关各变量。

        Returns:
            A (ModelAgent): 金融系统模型个体群，包含了金融系统的全部个体群变量。

        """

        dict_update_methods = {  # 创建一个字典，映射 by_way 的值到对应的方法
            ## NOTE：功能函数集：更新冲击、状态。
            'Shock_P_def_t': self.update_by_Shock_P_def_t,
            'Shock_D_def_s': self.update_by_Shock_D_def_s,
            'Shock_IB_def_s': self.update_by_Shock_IB_def_s,
            'Shock_IB_def': self.update_by_Shock_IB_def,
            'Shock_IB_def_t': self.update_by_Shock_IB_def_t,
            'clear Shock_IB and Shock_exIB': self.update_by_clear_Shock_IB_and_Shock_exIB,
            'clear all Shock_target': self.update_by_clear_all_Shock_t,
            'clear all Shock_source': self.update_by_clear_all_Shock_s,
            'clear all Shock_interbank': self.update_by_clear_all_Shock_IB,
            ## NOTE：功能函数集：更新损失。
            'Loss_exIB_def_t': self.update_by_Loss_exIB_def_t,
            'Loss_IB_def_t': self.update_by_Loss_IB_def_t,
            ## NOTE：功能函数集：更新违约。
            'Default_IB_def_s': self.update_by_Default_IB_def_s,
            'Default_D_def_s': self.update_by_Default_D_def_s,
            ## NOTE：功能函数集：更新商业银行之资产负债表结构。
            'A_P': self.update_by_A_P,
            'A_R': self.update_by_A_R,
            'A_other': self.update_by_A_other,
            'A_Q': self.update_by_A_Q,
            'A_IB_all': self.update_by_A_IB_all,
            'Z_D': self.update_by_Z_D,
            'Z_CB': self.update_by_Z_CB,
            'Z_other': self.update_by_Z_other,
            'Z_IB_all': self.update_by_Z_IB_all,
            'A_IB': self.update_by_A_IB,
            'Z_IB': self.update_by_Z_IB,
            ## NOTE 对于所有的进行更新。
            'all': self.update_by_all,
        }

        # 使用字典来调用对应的方法
        if by_way in dict_update_methods:
            dict_update_methods[by_way](A)
        else:
            raise Exception("关键词by_way取词错误".format(by_way))
            pass  # if
        return A
        pass  # function

    pass  # class
