"功能函数集：计算商业银行之资产负债表结构。"

## 功能函数集：计算商业银行之资产负债表结构。

##########################################
#状态/使用
##########################################

from SystemicRisk.core import np,BankCommercial,BankInterbank,TypeState,LESS1,env



class BalanceSheet:

    ## 函数区

    "汇总各银行之总资产。"
    def together_B_A_all(self, bank:BankCommercial, bankList:TypeState):
        bank.A_all[bankList] = bank.A_BI_all[bankList] + bank.A_exBI[bankList]
        pass


    "加总各银行之银行间总资产，通过银行间资产邻接矩阵。"
    def sum_B_A_BI(self, bank:BankCommercial, interbank:BankInterbank, bankList:TypeState, interbankList:TypeState):
        bank.A_BI_all[: ] = np.sum(interbank.A_BI * interbankList, dims = 2)
        pass

    "汇总各银行之非银行间资产``A_{-BI}``。"
    def together_B_A_exBI(self, bank:BankCommercial, bankList:TypeState):
        bank.A_exBI[bankList] = bank.A_P[bankList] + bank.A_Q[bankList] + bank.A_R[bankList] + bank.A_other[bankList]
        pass

    # "更新各银行之银行总负债``Z_{B}``。"
    # functions update_B_Z_all(bank:BankCommercial, interbank:BankInterbank, byWay:str = "all")
    #     if byWay == "all":
    #         together_B_Z_exBI(bank,bankList)
    #         together_B_Z_BI(bank, interbank,bankList,interbankList)
    #     elif byWay == "Z_exBI" | byWay == "Z_D":
    #         together_B_Z_exBI(bank,bankList)
    #     elif byWay == "Z_BI":
    #         together_B_Z_BI(bank, interbank,bankList,interbankList)
    #     else:
    #         throw(DomainError(byWay, "关键词取值错误！"))
    #         pass
    #     together_B_Z_all(bank,bankList)
    #     pass

    "汇总各银行之总负债。"
    def together_B_Z_all(self, bank:BankCommercial, bankList:TypeState):
        bank.Z_all[bankList] = bank.Z_BI_all[bankList] + bank.Z_exBI[bankList]
        pass

    "加总各银行之银行间总负债，通过银行间负债邻接矩阵。"
    def sum_B_Z_BI(self, bank:BankCommercial, interbank:BankInterbank, bankList:TypeState, interbankList:TypeState):
        bank.Z_BI_all[: ] = np.sum(interbank.Z_BI * interbankList, dims = 2)
        pass

    "汇总各银行之非银行间负债``Z_{-BI}``。"
    def together_B_Z_exBI(self, bank:BankCommercial, bankList:TypeState):
        bank.Z_exBI[bankList] = bank.Z_D[bankList] + bank.Z_other[bankList]
        pass

    "计算各银行之所有者权益``E_{B}``，通过总资产与总负债差值。"
    def calc_B_E_all(self, bank:BankCommercial, bankList:TypeState):
        bank.E_all[bankList] = np.max(bank.A_all[bankList] - bank.Z_all[bankList] - LESS1[bankList], 0.0)
        pass

    "计算银行体系内包括已退出银行在内的所有各银行之所有者权益``E_{B}``，通过总资产与总负债差值。"
    def calc_B_E_all_at_all_bank(self, bank:BankCommercial, bankList:TypeState):
        bank.E_all[: ] = np.max(bank.A_all - bank.Z_all - LESS1, 0.0)
        pass


    "计算各银行之总资产``A_{B}``，通过所有者权益和总负债。"
    def calc_B_A_all(self, bank:BankCommercial, bankList:TypeState):
        bank.A_all[bankList] = bank.E_all[bankList] + bank.Z_all[bankList]
        pass

    "计算各银行之总负债``Z_{B}``，通过所有者权益和总资产。"
    def calc_B_Z_all(self, bank:BankCommercial, bankList:TypeState):
        bank.Z_all[bankList] = bank.A_all[bankList] - bank.E_all[bankList]
        pass

    "转换银行间负债为资产。"
    def alter_Z_BI(self, interbank:BankInterbank):
        interbank.A_BI = interbank.Z_BI.T
        pass

    "转换银行间资产为负债。"
    def alter_A_BI(self, interbank:BankInterbank):
        interbank.Z_BI = interbank.A_BI.T
        pass



    ### #状态/停用 更新银行间变量
    """
    更新各银行间之资产负债矩阵。
    # Arguments
    `byWay:str`:  参数，通过该参数指定的变量作为已知变量，更新其他相关各变量。
    - `Z_BI`:  已知``Z_{BI}``，更新其余银行间资产负债变量；
    - `A_BI`:  已知``A_{BI}``，更新其余银行间资产负债变量；
    """
    def update_BI_balanceSheet(self, interbank:BankInterbank; byWay:str):
        if byWay == "Z_BI":
            interbank.A_BI = interbank.Z_BI'
        elif byWay == "A_BI":
            interbank.Z_BI = interbank.A_BI'
        else:
            throw(DomainError(byWay, "关键词取值错误！"))
            pass
        pass


    ### 更新各银行之资产负债表变量
    """
    更新各银行之资产负债表变量。
    # Arguments
    `byWay:str`:  参数，通过该参数指定的变量作为已知变量，更新其他相关各变量。
    - `all`:  更新各银行之所有资产负债表变量；
    - `A_exBI`:  已知``A_{-BI}``，更新各银行之其余相关的资产负债表变量；
    - `A_P`:  已知``L_{-BI}``，更新各银行之其余相关的资产负债表变量；
    - `A_Q`:  已知``Q_{B}``，更新各银行之其余相关的资产负债表变量；
    - `A_R`:  已知``R_{B}``，更新各银行之其余相关的资产负债表变量；
    - `A_other`:  已知``A_{other}``，更新各银行之其余相关的资产负债表变量；
    - `A_BI_all`:  已知``A_{BI}[i,: ]``，更新各银行之其余相关的资产负债表变量；
    - `Z_exBI`:  已知``Z_{exBI}``，更新各银行之其余相关的资产负债表变量；
    - `Z_D`:  已知``D_{B}``，更新各银行之其余相关的资产负债表变量；
    - `Z_other`:  已知``Z_{other}``，更新各银行之其余相关的资产负债表变量；
    - `Z_BI_all`:  已知``Z_{BI}[i,: ]``，更新各银行之其余相关的资产负债表变量；
    - `E_all and Z_all`:  已知``E_{B}``和``Z_{B}``，更新各银行之其余相关的资产负债表变量；
    - `E_all and A_all`:  已知``E_{B}``和``A_{B}``，更新各银行之其余相关的资产负债表变量；
    - `calc all E_all`:  已知``A_{B}``和``Z_{B}``，更新计算所有银行之所有者权益``E_{B}``；
    - `sum A_BI`:  已知``A_{BI}[i,j]``，加总各银行变量``A_{BI}[i,: ]``；
    - `sum Z_BI`:  已知``Z_{BI}[i,j]``，加总各银行变量``Z_{BI}[i,: ]``；
    - `alter to Z_BI from A_BI`:  已知``A_{BI}[i,j]``，转换得到``Z_{BI}[i,j]``；
    - `alter to A_BI from Z_BI`:  已知``Z_{BI}[i,j]``，转换得到``A_{BI}[i,j]``；
    """
    def update_B_balanceSheet(self, bank:BankCommercial, interbank:BankInterbank, bankList:TypeState, interbankList:TypeState; byWay:str):
        if byWay == "all":
            together_B_A_exBI(bank, bankList)
            sum_B_A_BI(bank, interbank, bankList, interbankList)
            together_B_A_all(bank, bankList)
            together_B_Z_exBI(bank, bankList)
            sum_B_Z_BI(bank, interbank, bankList, interbankList)
            together_B_Z_all(bank, bankList)
            calc_B_E_all(bank, bankList)
        elif byWay == "A_exBI" | byWay == "A_P" | byWay == "A_Q" | byWay == "A_R" | byWay == "A_other":
            together_B_A_exBI(bank, bankList)
            together_B_A_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif byWay == "A_BI_all":
            together_B_A_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif byWay == "Z_exBI" | byWay == "Z_D" | byWay == "Z_other":
            together_B_Z_exBI(bank, bankList)
            together_B_Z_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif byWay == "Z_BI_all":
            together_B_Z_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif byWay == "E_all and Z_all":
            calc_B_A_all(bank, bankList)
        elif byWay == "E_all and A_all":
            calc_B_Z_all(bank, bankList)
        elif byWay == "calc all E_all":
            calc_B_E_all_at_all_bank(bank, bankList)
        elif byWay == "sum A_BI":
            sum_B_A_BI(bank, interbank, bankList, interbankList)
            together_B_A_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif byWay == "sum Z_BI":
            sum_B_Z_BI(bank, interbank, bankList, interbankList)
            together_B_Z_all(bank, bankList)
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif byWay == "alter to Z_BI from A_BI":
            # sum_B_A_BI(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # together_B_A_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            alter_A_BI(interbank)
            # sum_B_Z_BI(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # together_B_Z_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        elif byWay == "alter to A_BI from Z_BI":
            # sum_B_Z_BI(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # together_B_Z_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            alter_Z_BI(interbank)
            # sum_B_A_BI(bank, interbank,bankList,interbankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # together_B_A_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
            # calc_B_E_all(bank,bankList) #HACK 冗余。不能调用，只能在外部手动计算。此处可以删除。
        else:
            throw(DomainError(byWay, "关键词取值错误！"))
            pass
        pass


        # functions update_B_balanceSheet(bank:BankCommercial, interbank:BankInterbank; byWay:str)
        #     update_B_A_all(bank, interbank, byWay = byWay)
        #     update_B_Z_all(bank, interbank, byWay = byWay)
        #     update_B_E_all(bank,byWay=byWay)
        #     pass




        # "更新各银行之银行总资产``A_{B}``。"
        # functions update_B_A_all(bank:BankCommercial, interbank:BankInterbank; byWay:str = "all")
        #     if byWay == "all":
        #     elif byWay == "A_exBI" | byWay == "A_P" | byWay == "A_Q" | byWay == "A_R":
        #         together_B_A_exBI(bank,bankList)
        #     elif byWay == "A_BI":
        #         together_B_A_BI(bank, interbank,bankList,interbankList)
        #     else:
        #         throw(DomainError(byWay, "关键词取值错误！"))
        #         pass
        #     together_B_A_all(bank,bankList)
        #     pass

    pass # class





