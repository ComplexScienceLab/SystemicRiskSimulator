##########################################
# 状态/使用
##########################################

import numpy as np

from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_environment_variables import env
from PySystemicRiskLab.core.define.define_type import TypeState, TypeMoney

pass  # end import


class BankTransfer:
    """计算商业银行之资金转移。"""

    @classmethod
    def transfer_B_capital_reverse(cls, target: TypeMoney, source: TypeMoney, shock: TypeMoney, flow: TypeMoney):
        """
        转移资金（资金等量反向变化）。

        Args:
            target (): 转移目的地；
            source (): 转移源；
            shock (): 相关冲击；
            flow (): 流量；

        Returns:
            target, source, shock

        """
        target += flow
        source -= flow
        shock -= flow
        return target, source, shock
        pass

    @classmethod
    def transfer_B_capital_reduce(cls, target: TypeMoney, source: TypeMoney, shock: TypeMoney, flow: TypeMoney):
        """
        同减资金（资金等量同向减少）。

        Args:
            target (): 转移目的地；
            source (): 转移源；
            shock (): 相关冲击；
            flow (): 流量；

        Returns:target, source, shock

        """

        target -= flow
        source -= flow
        shock -= flow
        return target, source, shock
        pass

    @classmethod
    def together_T_all(cls, bank: BankCommercial, bankState: TypeState):
        """汇总各银行之总交易流量``T_{all}``。"""
        bank.T_all[bankState] = bank.Lo_all[bankState] + bank.Bi_all[bankState] + bank.Bo_all[bankState] + bank.Li_all[bankState]
        pass

    @classmethod
    def together_transfer_B_Lo_all(cls, bank: BankCommercial, bankState: TypeState):
        """汇总各银行之总贷款流出``Lo_{B}``。"""
        bank.Lo_all[bankState] = bank.Lo_BI_all[bankState] + bank.Lo_exBI[bankState]
        pass

    @classmethod
    def together_transfer_B_Lo_exBI(cls, bank: BankCommercial, bankState: TypeState):
        """汇总各银行之非银行间贷款流出``Lo_{-BI}``。"""
        bank.Lo_exBI[bankState] = bank.Lo_P[bankState]
        pass

    @classmethod
    def together_transfer_B_Li_all(cls, bank: BankCommercial, bankState: TypeState):
        """汇总各银行之总贷款流入``Li_{B}``。"""
        bank.Li_all[bankState] = bank.Li_BI_all[bankState] + bank.Li_exBI[bankState]
        pass

    @classmethod
    def together_transfer_B_Li_exBI(cls, bank: BankCommercial, bankState: TypeState):
        """汇总各银行之非银行间贷款流入``Li_{-BI}``。"""
        bank.Li_exBI[bankState] = bank.Li_P[bankState]
        pass

    @classmethod
    def together_transfer_B_Bo_all(cls, bank: BankCommercial, bankState: TypeState):
        """汇总各银行之总借款流出``Bo_{B}``。"""
        bank.Bo_all[bankState] = bank.Bo_BI_all[bankState] + bank.Bo_exBI[bankState]
        pass

    @classmethod
    def together_transfer_B_Bo_exBI(cls, bank: BankCommercial, bankState: TypeState):
        """汇总各银行之非银行间借款流出``Bo_{-BI}``。"""
        bank.Bo_exBI[bankState] = bank.Bo_D[bankState]
        pass

    @classmethod
    def together_transfer_B_Bi_all(cls, bank: BankCommercial, bankState: TypeState):
        """汇总各银行之总借款流入``Bi_{B}``。"""
        bank.Bi_all[bankState] = bank.Bi_BI_all[bankState] + bank.Bi_exBI[bankState]
        pass

    @classmethod
    def together_transfer_B_Bi_exBI(cls, bank: BankCommercial, bankState: TypeState):
        """汇总各银行之非银行间借款流入``Bi_{-BI}``。"""
        bank.Bi_exBI[bankState] = bank.Bi_D[bankState]
        pass

    @classmethod
    def alter_transfer_Lo_BI(cls, interbank: BankInterbank, interbankState: TypeState):
        """转换银行间贷款流出``Lo_{BI}``为银行间借款流入``Bi_{BI}``。"""
        interbank.Bi_BI = interbank.Lo_BI.T
        pass

    @classmethod
    def alter_transfer_Bi_BI(cls, interbank: BankInterbank, interbankState: TypeState):
        """转换银行间借款流入``Bi_{BI}``为银行间贷款流出``Lo_{BI}``。"""
        interbank.Lo_BI = interbank.Bi_BI.T
        pass

    @classmethod
    def alter_transfer_Bo_BI(cls, interbank: BankInterbank, interbankState: TypeState):
        """转换银行间借款流出``Bo_{BI}``为银行间贷款流入``Li_{BI}``。"""
        interbank.Li_BI = interbank.Bo_BI.T
        pass

    @classmethod
    def alter_transfer_Li_BI(cls, interbank: BankInterbank, interbankState: TypeState):
        """转换银行间贷款流入``Li_{BI}``为银行间借款流出``Bo_{BI}``。"""
        interbank.Bo_BI = interbank.Li_BI.T
        pass

    @classmethod
    def sum_transfer_Bi_BI(cls, bank: BankCommercial, interbank: BankInterbank, bankState: TypeState, interbankState: TypeState):
        """加总各银行之银行间借款流入``Bi_{B}``，通过银行间借款流入邻接矩阵``Bi_{BI}``。"""
        bank.Bi_BI_all[:] = np.sum(interbank.Bi_BI * interbankState, axis=1).reshape(-1, 1)
        pass

    @classmethod
    def sum_transfer_Li_BI(cls, bank: BankCommercial, interbank: BankInterbank, bankState: TypeState, interbankState: TypeState):
        """加总各银行之银行间贷款流入``Li_{B}``，通过银行间贷款流入邻接矩阵``Li_{BI}``。"""
        bank.Li_BI_all[:] = np.sum(interbank.Li_BI * interbankState, axis=1).reshape(-1, 1)
        pass

    @classmethod
    def clear_all_transfer(cls, bank: BankCommercial, interbank: BankInterbank, bankState: TypeState, interbankState: TypeState):
        """清零所有流量变量值"""
        bank.Lo_BI_all[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Lo_P[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Li_BI_all[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Li_P[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Bi_BI_all[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Bi_D[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Bo_BI_all[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Bo_D[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        interbank.Lo_BI[interbankState] = np.zeros((env['num_bank'], env['num_bank']))[interbankState]
        interbank.Bo_BI[interbankState] = np.zeros((env['num_bank'], env['num_bank']))[interbankState]
        pass

    @classmethod
    def update_B_transfer(cls, bank: BankCommercial, interbank: BankInterbank, bankState: TypeState, interbankState: TypeState, byWay: str = "all"):
        """
        更新各银行之借贷流量变量。

        参数``byWay``可选项：

        - ``all``:  更新全部借贷流量变量；
        - ``clear transfer all``:  清零所有不必要的借贷流量变量；
        - ``Lo_P``:  已知``Lo_{B,P}``，更新其余借贷流量变量；
        - ``Li_P``:  已知``Li_{B,P}``，更新其余借贷流量变量；
        - ``Bi_D``:  已知``Bi_{B,D}``，更新其余借贷流量变量；
        - ``Bo_D``:  已知``Bo_{B,D}``，更新其余借贷流量变量；
        - ``Lo_BI_all``:  已知``Lo_{BI}[i,: ]``，更新其余借贷流量变量；
        - ``Li_BI_all``:  已知``Li_{BI}[i,: ]``，更新其余借贷流量变量；
        - ``Bi_BI_all``:  已知``Bi_{BI}[i,: ]``，更新其余借贷流量变量；
        - ``Bo_BI_all``:  已知``Bo_{BI}[i,: ]``，更新其余借贷流量变量；
        - ``Lo_BI``:  已知``Lo_{BI}``，更新其余借贷流量变量；
        - ``Bi_BI``:  已知``Bi_{BI}``，更新其余借贷流量变量；
        - ``Bo_BI``:  已知``Bo_{BI}``，更新其余借贷流量变量；
        - ``Li_BI``:  已知``Li_{BI}``，更新其余借贷流量变量；

        Args:
            bank (): 商业银行众
            interbank (): 商业银行间市场
            bankState (): 银行之状态
            interbankState (): 银行间市场之状态
            byWay (): 参数，通过该参数指定的变量作为已知变量，驱动，以更新其他相关各变量。

        Returns:

        """

        if byWay == "all":
            cls.clear_all_transfer(bank, interbank, bankState, interbankState)
            cls.alter_transfer_Lo_BI(interbank, interbankState)
            cls.sum_transfer_Bi_BI(bank, interbank, bankState, interbankState)
            cls.alter_transfer_Bo_BI(interbank, interbankState)
            cls.sum_transfer_Li_BI(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Lo_exBI(bank, bankState)
            cls.together_transfer_B_Lo_all(bank, bankState)
            cls.together_transfer_B_Li_exBI(bank, bankState)
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_transfer_B_Bi_exBI(bank, bankState)
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_transfer_B_Bo_exBI(bank, bankState)
            cls.together_transfer_B_Bo_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "clear transfer all":
            cls.clear_all_transfer(bank, interbank, bankState, interbankState)
            cls.alter_transfer_Lo_BI(interbank, ((bank.on | bank.off) & (bank.on | bank.off).T))
            cls.sum_transfer_Bi_BI(bank, interbank, (bank.on | bank.off), ((bank.on | bank.off) & (bank.on | bank.off).T))
            cls.alter_transfer_Bo_BI(interbank, ((bank.on | bank.off) & (bank.on | bank.off).T))
            cls.sum_transfer_Li_BI(bank, interbank, (bank.on | bank.off), ((bank.on | bank.off) & (bank.on | bank.off).T))
            cls.together_transfer_B_Lo_exBI(bank, (bank.on | bank.off))
            cls.together_transfer_B_Lo_all(bank, (bank.on | bank.off))
            cls.together_transfer_B_Li_exBI(bank, (bank.on | bank.off))
            cls.together_transfer_B_Li_all(bank, (bank.on | bank.off))
            cls.together_transfer_B_Bi_exBI(bank, (bank.on | bank.off))
            cls.together_transfer_B_Bi_all(bank, (bank.on | bank.off))
            cls.together_transfer_B_Bo_exBI(bank, (bank.on | bank.off))
            cls.together_transfer_B_Bo_all(bank, (bank.on | bank.off))
            cls.together_T_all(bank, (bank.on | bank.off))
        elif byWay == "Lo_P":
            cls.together_transfer_B_Lo_exBI(bank, bankState)
            cls.together_transfer_B_Lo_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Li_P":
            cls.together_transfer_B_Li_exBI(bank, bankState)
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Bi_D":
            cls.together_transfer_B_Bi_exBI(bank, bankState)
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Bo_D":
            cls.together_transfer_B_Bo_exBI(bank, bankState)
            cls.together_transfer_B_Bo_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Lo_BI_all":
            cls.together_transfer_B_Lo_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Li_BI_all":
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Bi_BI_all":
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Bo_BI_all":
            cls.together_transfer_B_Bo_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Lo_BI":
            cls.alter_transfer_Lo_BI(interbank, interbankState)
            cls.sum_transfer_Bi_BI(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Bi_BI":
            cls.alter_transfer_Bi_BI(interbank, interbankState)
            cls.sum_transfer_Bi_BI(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Bo_BI":
            cls.alter_transfer_Bo_BI(interbank, interbankState)
            cls.sum_transfer_Li_BI(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        elif byWay == "Li_BI":
            cls.alter_transfer_Li_BI(interbank, interbankState)
            cls.sum_transfer_Li_BI(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_T_all(bank, bankState)
        else:
            raise Exception("关键词byWay取词错误".format(byWay))
            pass
        pass  # function

    pass  # class
