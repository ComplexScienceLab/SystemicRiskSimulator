"功能函数集：计算商业银行之资产负债表结构。"

## 功能函数集：计算商业银行之资产负债表结构。


from PySystemicRiskLab import np, pd

# from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_consts import LESS1
from PySystemicRiskLab.core.define.define_type import StateType

pass  # end import


class BalanceSheet:
    ## 函数区

    @classmethod
    def together_B_A_all(cls, bank: pd.Series, bankList: StateType):
        """汇总各银行之总资产。"""
        bank.A_all[bankList] = bank.A_BI_all[bankList] + bank.A_exBI[bankList]
        pass

    @classmethod
    def sum_B_A_BI(cls, bank: pd.Series, interbank: pd.Series, bankList: StateType, interbankList: StateType):
        """加总各银行之银行间总资产，通过银行间资产邻接矩阵。"""
        bank.A_BI_all[:] = np.sum(interbank.A_BI * interbankList, axis=1).reshape(-1, 1)
        pass

    @classmethod
    def together_B_A_exBI(cls, bank: pd.Series, bankList: StateType):
        """汇总各银行之非银行间资产``A_{-BI}``。"""
        bank.A_exBI[bankList] = bank.A_P[bankList] + bank.A_Q[bankList] + bank.A_R[bankList] + bank.A_other[bankList]
        pass

    # "更新各银行之银行总负债``Z_{B}``。"
    # functions update_B_Z_all(bank: pd.Series, interbank: pd.Series, by_way:str = "all")
    #     if by_way == 'all':
    #         together_B_Z_exBI(bank,bankList)
    #         together_B_Z_BI(bank, interbank,bankList,interbankList)
    #     elif by_way == 'Z_exBI' | by_way == 'Z_D':
    #         together_B_Z_exBI(bank,bankList)
    #     elif by_way == 'Z_BI':
    #         together_B_Z_BI(bank, interbank,bankList,interbankList)
    #     else:
    #         throw(DomainError(by_way, "关键词取值错误！"))
    #         pass
    #     together_B_Z_all(bank,bankList)
    #     pass

    @classmethod
    def together_B_Z_all(cls, bank: pd.Series, bankList: StateType):
        """汇总各银行之总负债。"""
        bank.Z_all[bankList] = bank.Z_BI_all[bankList] + bank.Z_exBI[bankList]
        pass

    @classmethod
    def sum_B_Z_BI(cls, bank: pd.Series, interbank: pd.Series, bankList: StateType, interbankList: StateType):
        """加总各银行之银行间总负债，通过银行间负债邻接矩阵。"""
        bank.Z_BI_all[:] = np.sum(interbank.Z_BI * interbankList, axis=1).reshape(-1, 1)
        pass

    @classmethod
    def together_B_Z_exBI(cls, bank: pd.Series, bankList: StateType):
        """汇总各银行之非银行间负债``Z_{-BI}``。"""
        bank.Z_exBI[bankList] = bank.Z_D[bankList] + bank.Z_other[bankList]
        pass

    @classmethod
    def calc_B_E_all(cls, bank: pd.Series, bankList: StateType):
        """计算各银行之所有者权益``E_{B}``，通过总资产与总负债差值。"""
        bank.E_all[bankList] = np.maximum(bank.A_all[bankList] - bank.Z_all[bankList] - LESS1[bankList], 0.0)
        pass

    @classmethod
    def calc_B_E_all_at_all_bank(cls, bank: pd.Series, bankList: StateType):
        """计算银行体系内包括已退出银行在内的所有各银行之所有者权益``E_{B}``，通过总资产与总负债差值。"""
        bank.E_all[:] = np.maximum(bank.A_all - bank.Z_all - LESS1, 0.0)
        pass

    @classmethod
    def calc_B_A_all(cls, bank: pd.Series, bankList: StateType):
        """计算各银行之总资产``A_{B}``，通过所有者权益和总负债。"""
        bank.A_all[bankList] = bank.E_all[bankList] + bank.Z_all[bankList]
        pass

    @classmethod
    def calc_B_Z_all(cls, bank: pd.Series, bankList: StateType):
        """计算各银行之总负债``Z_{B}``，通过所有者权益和总资产。"""
        bank.Z_all[bankList] = bank.A_all[bankList] - bank.E_all[bankList]
        pass

    @classmethod
    def alter_Z_BI(cls, interbank: pd.Series):
        """转换银行间负债为资产。"""
        interbank.A_BI = interbank.Z_BI.T
        pass

    @classmethod
    def alter_A_BI(cls, interbank: pd.Series):
        """转换银行间资产为负债。"""
        interbank.Z_BI = interbank.A_BI.T
        pass

    @classmethod
    def update_B_balance_sheet(cls, bank: pd.Series, interbank: pd.Series, bankList: StateType, interbankList: StateType, by_way: str):
        """
        更新各银行之资产负债表变量。#状态/停用

        参数``by_way``之可选项：

        - ``all``:  更新各银行之所有资产负债表变量；
        - ``A_exBI``:  已知``A_{-BI}``，更新各银行之其余相关的资产负债表变量；
        - ``A_P``:  已知``L_{-BI}``，更新各银行之其余相关的资产负债表变量；
        - ``A_Q``:  已知``Q_{B}``，更新各银行之其余相关的资产负债表变量；
        - ``A_R``:  已知``R_{B}``，更新各银行之其余相关的资产负债表变量；
        - ``A_other``:  已知``A_{other}``，更新各银行之其余相关的资产负债表变量；
        - ``A_BI_all``:  已知``A_{BI}[i,: ]``，更新各银行之其余相关的资产负债表变量；
        - ``Z_exBI``:  已知``Z_{exBI}``，更新各银行之其余相关的资产负债表变量；
        - ``Z_D``:  已知``D_{B}``，更新各银行之其余相关的资产负债表变量；
        - ``Z_other``:  已知``Z_{other}``，更新各银行之其余相关的资产负债表变量；
        - ``Z_BI_all``:  已知``Z_{BI}[i,: ]``，更新各银行之其余相关的资产负债表变量；
        - ``E_all and Z_all``:  已知``E_{B}``和``Z_{B}``，更新各银行之其余相关的资产负债表变量；
        - ``E_all and A_all``:  已知``E_{B}``和``A_{B}``，更新各银行之其余相关的资产负债表变量；
        - ``calc all E_all``:  已知``A_{B}``和``Z_{B}``，更新计算所有银行之所有者权益``E_{B}``；
        - ``sum A_BI``:  已知``A_{BI}[i,j]``，加总各银行变量``A_{BI}[i,: ]``；
        - ``sum Z_BI``:  已知``Z_{BI}[i,j]``，加总各银行变量``Z_{BI}[i,: ]``；
        - ``alter to Z_BI from A_BI``:  已知``A_{BI}[i,j]``，转换得到``Z_{BI}[i,j]``；
        - ``alter to A_BI from Z_BI``:  已知``Z_{BI}[i,j]``，转换得到``A_{BI}[i,j]``；

        Args:
            bank (): 商业银行众
            interbank (): 商业银行间市场
            bankList (): 银行列表
            interbankList (): 银行间市场列表
            by_way (): 参数，通过该参数指定的变量作为已知变量，更新其他相关各变量。

        Returns:

        """
        if by_way == 'all':
            cls.together_B_A_exBI(bank, bankList)
            cls.sum_B_A_BI(bank, interbank, bankList, interbankList)
            cls.together_B_A_all(bank, bankList)
            cls.together_B_Z_exBI(bank, bankList)
            cls.sum_B_Z_BI(bank, interbank, bankList, interbankList)
            cls.together_B_Z_all(bank, bankList)
            cls.calc_B_E_all(bank, bankList)
        elif by_way == 'A_exBI' or by_way == 'A_P' or by_way == 'A_Q' or by_way == 'A_R' or by_way == 'A_other':
            cls.together_B_A_exBI(bank, bankList)
            cls.together_B_A_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif by_way == 'A_BI_all':
            cls.together_B_A_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif by_way == 'Z_exBI' or by_way == 'Z_D' or by_way == 'Z_other':
            cls.together_B_Z_exBI(bank, bankList)
            cls.together_B_Z_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif by_way == 'Z_BI_all':
            cls.together_B_Z_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif by_way == 'E_all and Z_all':
            cls.calc_B_A_all(bank, bankList)
        elif by_way == 'E_all and A_all':
            cls.calc_B_Z_all(bank, bankList)
        elif by_way == 'calc all E_all':
            cls.calc_B_E_all_at_all_bank(bank, bankList)
        elif by_way == 'sum A_BI':
            cls.sum_B_A_BI(bank, interbank, bankList, interbankList)
            cls.together_B_A_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif by_way == 'sum Z_BI':
            cls.sum_B_Z_BI(bank, interbank, bankList, interbankList)
            cls.together_B_Z_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif by_way == 'alter to Z_BI from A_BI':
            # sum_B_A_BI(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # together_B_A_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            cls.alter_A_BI(interbank)
            # sum_B_Z_BI(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # together_B_Z_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif by_way == 'alter to A_BI from Z_BI':
            # sum_B_Z_BI(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # together_B_Z_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            cls.alter_Z_BI(interbank)
            # sum_B_A_BI(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # together_B_A_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        else:
            raise Exception("关键词by_way取词错误".format(by_way))
            pass
        pass

        # functions update_B_balance_sheet(bank: pd.Series, interbank: pd.Series; by_way:str)
        #     update_B_A_all(bank, interbank, by_way = by_way)
        #     update_B_Z_all(bank, interbank, by_way = by_way)
        #     update_B_E_all(bank,by_way=by_way)
        #     pass

        # "更新各银行之银行总资产``A_{B}``。"
        # functions update_B_A_all(bank: pd.Series, interbank: pd.Series; by_way:str = "all")
        #     if by_way == 'all':
        #     elif by_way == 'A_exBI' | by_way == 'A_P' | by_way == 'A_Q' | by_way == 'A_R':
        #         together_B_A_exBI(bank,bankList)
        #     elif by_way == 'A_BI':
        #         together_B_A_BI(bank, interbank,bankList,interbankList)
        #     else:
        #         throw(DomainError(by_way, "关键词取值错误！"))
        #         pass
        #     together_B_A_all(bank,bankList)
        #     pass

    pass  # class
