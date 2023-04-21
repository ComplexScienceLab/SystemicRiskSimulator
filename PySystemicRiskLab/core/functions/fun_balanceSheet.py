"功能函数集：计算商业银行之资产负债表结构。"

## 功能函数集：计算商业银行之资产负债表结构。


from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_consts import LESS1
from PySystemicRiskLab.core.define.define_type import StateType

pass  # end import


class BalanceSheet:
    ## 函数区

    @classmethod
    def together_B_A_all(cls, bank: BankCommercial, bankList: StateType):
        """汇总各银行之总资产。"""
        bank.A_all[bankList] = bank.A_IB_all[bankList] + bank.A_exIB[bankList]
        pass

    @classmethod
    def sum_B_A_IB(cls, bank: BankCommercial, interbank: BankInterbank, bankList: StateType, interbankList: StateType):
        """加总各银行之银行间总资产，通过银行间资产邻接矩阵。"""
        bank.A_IB_all[:] = np.sum(interbank.A_IB * interbankList, axis=1).reshape(-1, 1)
        pass

    @classmethod
    def together_B_A_exIB(cls, bank: BankCommercial, bankList: StateType):
        """汇总各银行之非银行间资产``A_{-IB}``。"""
        bank.A_exIB[bankList] = bank.A_P[bankList] + bank.A_Q[bankList] + bank.A_R[bankList] + bank.A_other[bankList]
        pass

    # "更新各银行之银行总负债``Z_{B}``。" #HACK无用
    # functions update_B_Z_all(bank:BankCommercial, interbank:BankInterbank, by_way:str='all')
    #     if by_way == 'all':
    #         together_B_Z_exIB(bank,bankList)
    #         together_B_Z_IB(bank, interbank,bankList,interbankList)
    #     elif by_way == 'Z_exIB' | by_way == 'Z_D':
    #         together_B_Z_exIB(bank,bankList)
    #     elif by_way == 'Z_IB':
    #         together_B_Z_IB(bank, interbank,bankList,interbankList)
    #     else:
    #         throw(DomainError(by_way, "关键词取值错误！"))
    #         pass
    #     together_B_Z_all(bank,bankList)
    #     pass

    @classmethod
    def together_B_Z_all(cls, bank: BankCommercial, bankList: StateType):
        """汇总各银行之总负债。"""
        bank.Z_all[bankList] = bank.Z_IB_all[bankList] + bank.Z_exIB[bankList]
        pass

    @classmethod
    def sum_B_Z_IB(cls, bank: BankCommercial, interbank: BankInterbank, bankList: StateType, interbankList: StateType):
        """加总各银行之银行间总负债，通过银行间负债邻接矩阵。"""
        bank.Z_IB_all[:] = np.sum(interbank.Z_IB * interbankList, axis=1).reshape(-1, 1)
        pass

    @classmethod
    def together_B_Z_exIB(cls, bank: BankCommercial, bankList: StateType):
        """汇总各银行之非银行间负债``Z_{-IB}``。"""
        bank.Z_exIB[bankList] = bank.Z_D[bankList] + bank.Z_other[bankList]
        pass

    @classmethod
    def calc_B_E_all(cls, bank: BankCommercial, bankList: StateType):  # BUG是否考虑E_all负数？还是手动计算？
        """计算各银行之所有者权益``E_{B}``，通过总资产与总负债差值。"""
        bank.E_all[bankList] = bank.A_all[bankList] - bank.Z_all[bankList] - LESS1[bankList] # 允许E_all为负数
        # bank.E_all[bankList] = np.maximum(bank.A_all[bankList] - bank.Z_all[bankList] - LESS1[bankList], 0.0)
        pass

    # @classmethod
    # def calc_B_E_all_at_all_bank(cls, bank: BankCommercial, bankList: StateType):  # HACK没有用到过
    #     """计算银行体系内包括已退出银行在内的所有各银行之所有者权益``E_{B}``，通过总资产与总负债差值。"""
    #     bank.E_all[:] = bank.A_all - bank.Z_all - LESS1
    #     # bank.E_all[:] = np.maximum(bank.A_all - bank.Z_all - LESS1, 0.0)
    #     pass

    # @classmethod
    # def calc_B_A_all(cls, bank: BankCommercial, bankList: StateType):  # HACK没有用到过
    #     """计算各银行之总资产``A_{B}``，通过所有者权益和总负债。"""
    #     bank.A_all[bankList] = bank.E_all[bankList] + bank.Z_all[bankList]
    #     pass

    # @classmethod
    # def calc_B_Z_all(cls, bank: BankCommercial, bankList: StateType):  # HACK没有用到过
    #     """计算各银行之总负债``Z_{B}``，通过所有者权益和总资产。"""
    #     bank.Z_all[bankList] = bank.A_all[bankList] - bank.E_all[bankList]
    #     pass

    @classmethod
    def alter_Z_IB(cls, interbank: BankInterbank):
        """转换银行间负债为资产。"""
        interbank.A_IB = interbank.Z_IB.T
        pass

    @classmethod
    def alter_A_IB(cls, interbank: BankInterbank):
        """转换银行间资产为负债。"""
        interbank.Z_IB = interbank.A_IB.T
        pass

    @classmethod
    def update_B_balance_sheet(cls, bank: BankCommercial, interbank: BankInterbank, bankList: StateType, interbankList: StateType, by_way: str):
        """
        更新各银行之资产负债表变量。

        参数``by_way``之可选项：

        - ``all``:  更新各银行之所有资产负债表变量；
        - ``A_exIB``:  已知``A_{-IB}``，更新各银行之其余相关的资产负债表变量；
        - ``A_P``:  已知``L_{-IB}``，更新各银行之其余相关的资产负债表变量；
        - ``A_Q``:  已知``Q_{B}``，更新各银行之其余相关的资产负债表变量；
        - ``A_R``:  已知``R_{B}``，更新各银行之其余相关的资产负债表变量；
        - ``A_other``:  已知``A_{other}``，更新各银行之其余相关的资产负债表变量；
        - ``A_IB_all``:  已知``A_{IB}[i,: ]``，更新各银行之其余相关的资产负债表变量；
        - ``Z_exIB``:  已知``Z_{exIB}``，更新各银行之其余相关的资产负债表变量；
        - ``Z_D``:  已知``D_{B}``，更新各银行之其余相关的资产负债表变量；
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
            bank (): 商业银行众
            interbank (): 商业银行间市场
            bankList (): 银行列表
            interbankList (): 银行间市场列表
            by_way (): 参数，通过该参数指定的变量作为已知变量，更新其他相关各变量。

        Returns:

        """
        if by_way == 'all':
            cls.together_B_A_exIB(bank, bankList)
            cls.sum_B_A_IB(bank, interbank, bankList, interbankList)
            cls.together_B_A_all(bank, bankList)
            cls.together_B_Z_exIB(bank, bankList)
            cls.sum_B_Z_IB(bank, interbank, bankList, interbankList)
            cls.together_B_Z_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        elif by_way == 'A_exIB' or by_way == 'A_P' or by_way == 'A_Q' or by_way == 'A_R' or by_way == 'A_other':
            cls.together_B_A_exIB(bank, bankList)
            cls.together_B_A_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        elif by_way == 'A_IB_all':
            cls.together_B_A_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        elif by_way == 'Z_exIB' or by_way == 'Z_D' or by_way == 'Z_other':
            cls.together_B_Z_exIB(bank, bankList)
            cls.together_B_Z_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        elif by_way == 'Z_IB_all':
            cls.together_B_Z_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        # elif by_way == 'E_all and Z_all': #HACK似乎没有用到过
        #     cls.calc_B_A_all(bank, bankList)
        # elif by_way == 'E_all and A_all':#HACK似乎没有用到过
        #     cls.calc_B_Z_all(bank, bankList)
        # elif by_way == 'calc all E_all': #HACK似乎没有用到过
        #     cls.calc_B_E_all_at_all_bank(bank, bankList)
        elif by_way == 'A_IB':
            cls.alter_A_IB(interbank)
            cls.sum_B_A_IB(bank, interbank, bankList, interbankList)
            cls.together_B_A_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        elif by_way == 'Z_IB':
            cls.alter_Z_IB(interbank)
            cls.sum_B_Z_IB(bank, interbank, bankList, interbankList)
            cls.together_B_Z_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        elif by_way == 'sum A_IB':
            cls.sum_B_A_IB(bank, interbank, bankList, interbankList)
            cls.together_B_A_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        elif by_way == 'sum Z_IB':
            cls.sum_B_Z_IB(bank, interbank, bankList, interbankList)
            cls.together_B_Z_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        elif by_way == 'alter to Z_IB from A_IB':#HACK似乎冗余。
            # sum_B_A_IB(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。
            # together_B_A_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。
            cls.alter_A_IB(interbank)
            # sum_B_Z_IB(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。
            # together_B_Z_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。
        elif by_way == 'alter to A_IB from Z_IB':#HACK似乎冗余。
            # sum_B_Z_IB(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。
            # together_B_Z_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。
            cls.alter_Z_IB(interbank)
            # sum_B_A_IB(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。
            # together_B_A_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。
        else:
            raise Exception("关键词by_way取词错误".format(by_way))
            pass
        pass

        # functions update_B_balance_sheet(bank:BankCommercial, interbank:BankInterbank; by_way:str)
        #     update_B_A_all(bank, interbank, by_way = by_way)
        #     update_B_Z_all(bank, interbank, by_way = by_way)
        #     update_B_E_all(bank,by_way=by_way)
        #     pass

        # "更新各银行之银行总资产``A_{B}``。"
        # functions update_B_A_all(bank:BankCommercial, interbank:BankInterbank; by_way:str='all')
        #     if by_way == 'all':
        #     elif by_way == 'A_exIB' | by_way == 'A_P' | by_way == 'A_Q' | by_way == 'A_R':
        #         together_B_A_exIB(bank,bankList)
        #     elif by_way == 'A_IB':
        #         together_B_A_IB(bank, interbank,bankList,interbankList)
        #     else:
        #         throw(DomainError(by_way, "关键词取值错误！"))
        #         pass
        #     together_B_A_all(bank,bankList)
        #     pass

    pass  # class
