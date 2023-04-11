from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_environmentVariables import env
from PySystemicRiskLab.core.define.define_type import StateType, MoneyType

pass  # end import


class BankTransfer:
    """计算商业银行之资金转移。"""

    @classmethod
    def transfer_B_capital_reverse(cls, target: MoneyType, source: MoneyType, shock: MoneyType, flow: MoneyType):
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
    def transfer_B_capital_reduce(cls, target: MoneyType, source: MoneyType, shock: MoneyType, flow: MoneyType):
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
    def together_transfer_all(cls, bank: BankCommercial, bankState: StateType):
        """汇总各银行之总交易流量``T_{all}``。"""
        bank.T_all[bankState] = bank.Lo_all[bankState] + bank.Bi_all[bankState] + bank.Bo_all[bankState] + bank.Li_all[bankState]
        pass

    @classmethod
    def together_transfer_B_Lo_all(cls, bank: BankCommercial, bankState: StateType):
        """汇总各银行之总贷款流出（贷款方发款出去）``Lo_{B}``。"""
        bank.Lo_all[bankState] = bank.Lo_IB_all[bankState] + bank.Lo_exIB[bankState]
        pass

    @classmethod
    def together_transfer_B_Lo_exIB(cls, bank: BankCommercial, bankState: StateType):
        """汇总各银行之非银行间贷款流出``Lo_{-IB}``。"""
        bank.Lo_exIB[bankState] = bank.Lo_P[bankState]
        pass

    @classmethod
    def together_transfer_B_Li_all(cls, bank: BankCommercial, bankState: StateType):
        """汇总各银行之总贷款流入（贷款方收款回来）``Li_{B}``。"""
        bank.Li_all[bankState] = bank.Li_IB_all[bankState] + bank.Li_exIB[bankState]
        pass

    @classmethod
    def together_transfer_B_Li_exIB(cls, bank: BankCommercial, bankState: StateType):
        """汇总各银行之非银行间贷款流入``Li_{-IB}``。"""
        bank.Li_exIB[bankState] = bank.Li_P[bankState]
        pass

    @classmethod
    def together_transfer_B_Bo_all(cls, bank: BankCommercial, bankState: StateType):
        """汇总各银行之总借款流出（借款方还款出去）``Bo_{B}``。"""
        bank.Bo_all[bankState] = bank.Bo_IB_all[bankState] + bank.Bo_exIB[bankState]
        pass

    @classmethod
    def together_transfer_B_Bo_exIB(cls, bank: BankCommercial, bankState: StateType):
        """汇总各银行之非银行间借款流出``Bo_{-IB}``。"""
        bank.Bo_exIB[bankState] = bank.Bo_D[bankState]
        pass

    @classmethod
    def together_transfer_B_Bi_all(cls, bank: BankCommercial, bankState: StateType):
        """汇总各银行之总借款流入（借款方借款进来）``Bi_{B}``。"""
        bank.Bi_all[bankState] = bank.Bi_IB_all[bankState] + bank.Bi_exIB[bankState]
        pass

    @classmethod
    def together_transfer_B_Bi_exIB(cls, bank: BankCommercial, bankState: StateType):
        """汇总各银行之非银行间借款流入``Bi_{-IB}``。"""
        bank.Bi_exIB[bankState] = bank.Bi_D[bankState]
        pass

    @classmethod
    def alter_transfer_Lo_IB(cls, interbank: BankInterbank, interbankState: StateType):
        """转换银行间贷款流出``Lo_{IB}``为银行间借款流入``Bi_{IB}``。"""
        interbank.Bi_IB = interbank.Lo_IB.T
        pass

    @classmethod
    def alter_transfer_Bi_IB(cls, interbank: BankInterbank, interbankState: StateType):
        """转换银行间借款流入``Bi_{IB}``为银行间贷款流出``Lo_{IB}``。"""
        interbank.Lo_IB = interbank.Bi_IB.T
        pass

    @classmethod
    def alter_transfer_Bo_IB(cls, interbank: BankInterbank, interbankState: StateType):
        """转换银行间借款流出``Bo_{IB}``为银行间贷款流入``Li_{IB}``。"""
        interbank.Li_IB = interbank.Bo_IB.T
        pass

    @classmethod
    def alter_transfer_Li_IB(cls, interbank: BankInterbank, interbankState: StateType):
        """转换银行间贷款流入``Li_{IB}``为银行间借款流出``Bo_{IB}``。"""
        interbank.Bo_IB = interbank.Li_IB.T
        pass

    @classmethod
    def sum_transfer_Bi_IB(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """加总各银行之银行间借款流入``Bi_{B}``，通过银行间借款流入邻接矩阵``Bi_{IB}``。"""
        bank.Bi_IB_all[:] = np.sum(interbank.Bi_IB * interbankState, axis=1).reshape(-1, 1)
        pass

    @classmethod
    def sum_transfer_Li_IB(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """加总各银行之银行间贷款流入``Li_{B}``，通过银行间贷款流入邻接矩阵``Li_{IB}``。"""
        bank.Li_IB_all[:] = np.sum(interbank.Li_IB * interbankState, axis=1).reshape(-1, 1)
        pass

    @classmethod
    def clear_all_transfer(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """清零所有流量变量值"""
        bank.Lo_IB_all[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Lo_P[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Li_IB_all[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Li_P[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Bi_IB_all[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Bi_D[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Bo_IB_all[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        bank.Bo_D[bankState] = np.zeros((env['num_bank'], 1))[bankState]
        interbank.Lo_IB[interbankState] = np.zeros((env['num_bank'], env['num_bank']))[interbankState]
        interbank.Bo_IB[interbankState] = np.zeros((env['num_bank'], env['num_bank']))[interbankState]
        pass

    @classmethod
    def update_B_transfer(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType, by_way: str='all'):
        """
        更新各银行之借贷流量变量。

        参数``by_way``可选项：

        - ``all``:  更新全部借贷流量变量；
        - ``clear transfer all``:  清零所有不必要的借贷流量变量；
        - ``Lo_P``:  已知``Lo_{B,P}``，更新其余借贷流量变量；
        - ``Li_P``:  已知``Li_{B,P}``，更新其余借贷流量变量；
        - ``Bi_D``:  已知``Bi_{B,D}``，更新其余借贷流量变量；
        - ``Bo_D``:  已知``Bo_{B,D}``，更新其余借贷流量变量；
        - ``Lo_IB_all``:  已知``Lo_{IB}[i,: ]``，更新其余借贷流量变量；
        - ``Li_IB_all``:  已知``Li_{IB}[i,: ]``，更新其余借贷流量变量；
        - ``Bi_IB_all``:  已知``Bi_{IB}[i,: ]``，更新其余借贷流量变量；
        - ``Bo_IB_all``:  已知``Bo_{IB}[i,: ]``，更新其余借贷流量变量；
        - ``Lo_IB``:  已知``Lo_{IB}``，更新其余借贷流量变量；
        - ``Bi_IB``:  已知``Bi_{IB}``，更新其余借贷流量变量；
        - ``Bo_IB``:  已知``Bo_{IB}``，更新其余借贷流量变量；
        - ``Li_IB``:  已知``Li_{IB}``，更新其余借贷流量变量；

        Args:
            bank (): 商业银行众
            interbank (): 商业银行间市场
            bankState (): 银行之状态
            interbankState (): 银行间市场之状态
            by_way (): 参数，通过该参数指定的变量作为已知变量，驱动，以更新其他相关各变量。

        Returns:

        """

        if by_way == 'all':
            cls.alter_transfer_Lo_IB(interbank, interbankState)
            cls.sum_transfer_Bi_IB(bank, interbank, bankState, interbankState)
            cls.alter_transfer_Bo_IB(interbank, interbankState)
            cls.sum_transfer_Li_IB(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Lo_exIB(bank, bankState)
            cls.together_transfer_B_Lo_all(bank, bankState)
            cls.together_transfer_B_Li_exIB(bank, bankState)
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_transfer_B_Bi_exIB(bank, bankState)
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_transfer_B_Bo_exIB(bank, bankState)
            cls.together_transfer_B_Bo_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'clear transfer all':
            cls.clear_all_transfer(bank, interbank, bankState, interbankState)
            cls.alter_transfer_Lo_IB(interbank, ((bank.on | bank.off) & (bank.on | bank.off).T))
            cls.sum_transfer_Bi_IB(bank, interbank, (bank.on | bank.off), ((bank.on | bank.off) & (bank.on | bank.off).T))
            cls.alter_transfer_Bo_IB(interbank, ((bank.on | bank.off) & (bank.on | bank.off).T))
            cls.sum_transfer_Li_IB(bank, interbank, (bank.on | bank.off), ((bank.on | bank.off) & (bank.on | bank.off).T))
            cls.together_transfer_B_Lo_exIB(bank, (bank.on | bank.off))
            cls.together_transfer_B_Lo_all(bank, (bank.on | bank.off))
            cls.together_transfer_B_Li_exIB(bank, (bank.on | bank.off))
            cls.together_transfer_B_Li_all(bank, (bank.on | bank.off))
            cls.together_transfer_B_Bi_exIB(bank, (bank.on | bank.off))
            cls.together_transfer_B_Bi_all(bank, (bank.on | bank.off))
            cls.together_transfer_B_Bo_exIB(bank, (bank.on | bank.off))
            cls.together_transfer_B_Bo_all(bank, (bank.on | bank.off))
            cls.together_transfer_all(bank, (bank.on | bank.off))
        elif by_way == 'Lo_P':
            cls.together_transfer_B_Lo_exIB(bank, bankState)
            cls.together_transfer_B_Lo_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Li_P':
            cls.together_transfer_B_Li_exIB(bank, bankState)
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Bi_D':
            cls.together_transfer_B_Bi_exIB(bank, bankState)
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Bo_D':
            cls.together_transfer_B_Bo_exIB(bank, bankState)
            cls.together_transfer_B_Bo_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Lo_IB_all':
            cls.together_transfer_B_Lo_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Li_IB_all':
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Bi_IB_all':
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Bo_IB_all':
            cls.together_transfer_B_Bo_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Lo_IB':
            cls.alter_transfer_Lo_IB(interbank, interbankState)
            cls.sum_transfer_Bi_IB(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Bi_IB':
            cls.alter_transfer_Bi_IB(interbank, interbankState)
            cls.sum_transfer_Bi_IB(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Bi_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Bo_IB':
            cls.alter_transfer_Bo_IB(interbank, interbankState)
            cls.sum_transfer_Li_IB(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        elif by_way == 'Li_IB':
            cls.alter_transfer_Li_IB(interbank, interbankState)
            cls.sum_transfer_Li_IB(bank, interbank, bankState, interbankState)
            cls.together_transfer_B_Li_all(bank, bankState)
            cls.together_transfer_all(bank, bankState)
        else:
            raise Exception("关键词by_way取词错误".format(by_way))
            pass
        pass  # method

    pass  # class
