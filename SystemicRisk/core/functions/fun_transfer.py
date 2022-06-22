"功能函数集：计算商业银行之资金转移。"

## 功能函数集：计算商业银行之资金转移。

##########################################
# 状态/使用
##########################################

from SystemicRisk.core import np, env, BankCommercial, BankInterbank, TypeState, TypeMoney


class BankTransfer:
    ## 函数区

    """
    转移资金（资金等量反向变化）。
    # Arguments
    `target`: 转移目的地；
    `source`: 转移源；
    `shock`: 相关冲击；
    `flow`: 流量；
    """

    def transfer_B_capital_reverse(target: TypeMoney, source: TypeMoney, shock: TypeMoney, flow: TypeMoney):
        target += flow
        source -= flow
        shock -= flow
        return target, source, shock
        pass

    """
    同减资金（资金等量同向减少）。
    # Arguments
    `target`: 转移目的地；
    `source`: 转移源；
    `shock`: 相关冲击；
    `flow`: 流量；
    """

    def transfer_B_capital_reduce(target: TypeMoney, source: TypeMoney, shock: TypeMoney, flow: TypeMoney):
        target -= flow
        source -= flow
        shock -= flow
        return target, source, shock
        pass

    "汇总各银行之总交易流量``T_{all}``。"

    def together_T_all(self, bank: BankCommercial, bankState: TypeState):
        bank.T_all[bankState] = bank.Lo_all[bankState] + bank.Bi_all[bankState] + bank.Bo_all[bankState] + bank.Li_all[bankState]
        pass

    "汇总各银行之总贷款流出``Lo_{B}``。"

    def together_transfer_B_Lo_all(self, bank: BankCommercial, bankState: TypeState):
        bank.Lo_all[bankState] = bank.Lo_BI_all[bankState] + bank.Lo_exBI[bankState]
        pass

    "汇总各银行之非银行间贷款流出``Lo_{-BI}``。"

    def together_transfer_B_Lo_exBI(self, bank: BankCommercial, bankState: TypeState):
        bank.Lo_exBI[bankState] = bank.Lo_P[bankState]
        pass

    "汇总各银行之总贷款流入``Li_{B}``。"

    def together_transfer_B_Li_all(self, bank: BankCommercial, bankState: TypeState):
        bank.Li_all[bankState] = bank.Li_BI_all[bankState] + bank.Li_exBI[bankState]
        pass

    "汇总各银行之非银行间贷款流入``Li_{-BI}``。"

    def together_transfer_B_Li_exBI(self, bank: BankCommercial, bankState: TypeState):
        bank.Li_exBI[bankState] = bank.Li_P[bankState]
        pass

    "汇总各银行之总借款流出``Bo_{B}``。"

    def together_transfer_B_Bo_all(self, bank: BankCommercial, bankState: TypeState):
        bank.Bo_all[bankState] = bank.Bo_BI_all[bankState] + bank.Bo_exBI[bankState]
        pass

    "汇总各银行之非银行间借款流出``Bo_{-BI}``。"

    def together_transfer_B_Bo_exBI(self, bank: BankCommercial, bankState: TypeState):
        bank.Bo_exBI[bankState] = bank.Bo_D[bankState]
        pass

    "汇总各银行之总借款流入``Bi_{B}``。"

    def together_transfer_B_Bi_all(self, bank: BankCommercial, bankState: TypeState):
        bank.Bi_all[bankState] = bank.Bi_BI_all[bankState] + bank.Bi_exBI[bankState]
        pass

    "汇总各银行之非银行间借款流入``Bi_{-BI}``。"

    def together_transfer_B_Bi_exBI(self, bank: BankCommercial, bankState: TypeState):
        bank.Bi_exBI[bankState] = bank.Bi_D[bankState]
        pass

    "转换银行间贷款流出``Lo_{BI}``为银行间借款流入``Bi_{BI}``。"

    def alter_transfer_Lo_BI(self, interbank: BankInterbank, interbankState: TypeState):
        interbank.Bi_BI = interbank.Lo_BI.T
        pass

    "转换银行间借款流入``Bi_{BI}``为银行间贷款流出``Lo_{BI}``。"

    def alter_transfer_Bi_BI(self, interbank: BankInterbank, interbankState: TypeState):
        interbank.Lo_BI = interbank.Bi_BI.T
        pass

    "转换银行间借款流出``Bo_{BI}``为银行间贷款流入``Li_{BI}``。"

    def alter_transfer_Bo_BI(self, interbank: BankInterbank, interbankState: TypeState):
        interbank.Li_BI = interbank.Bo_BI.T
        pass

    "转换银行间贷款流入``Li_{BI}``为银行间借款流出``Bo_{BI}``。"

    def alter_transfer_Li_BI(self, interbank: BankInterbank, interbankState: TypeState):
        interbank.Bo_BI = interbank.Li_BI.T
        pass

    "加总各银行之银行间借款流入``Bi_{B}``，通过银行间借款流入邻接矩阵``Bi_{BI}``。"

    def sum_transfer_Bi_BI(self, bank: BankCommercial, interbank: BankInterbank, bankState: TypeState, interbankState: TypeState):
        bank.Bi_BI_all[:] = np.sum(interbank.Bi_BI * interbankState, dims=2)
        pass

    "加总各银行之银行间贷款流入``Li_{B}``，通过银行间贷款流入邻接矩阵``Li_{BI}``。"

    def sum_transfer_Li_BI(self, bank: BankCommercial, interbank: BankInterbank, bankState: TypeState, interbankState: TypeState):
        bank.Li_BI_all[:] = np.sum(interbank.Li_BI * interbankState, dims=2)
        pass

    "清零所有流量变量值"

    def clear_all_transfer(self, bank: BankCommercial, interbank: BankInterbank, bankState: TypeState, interbankState: TypeState):
        bank.Lo_BI_all[bankState] = np.zeros(env['num_bank'])[bankState]
        bank.Lo_P[bankState] = np.zeros(env['num_bank'])[bankState]
        bank.Li_BI_all[bankState] = np.zeros(env['num_bank'])[bankState]
        bank.Li_P[bankState] = np.zeros(env['num_bank'])[bankState]
        bank.Bi_BI_all[bankState] = np.zeros(env['num_bank'])[bankState]
        bank.Bi_D[bankState] = np.zeros(env['num_bank'])[bankState]
        bank.Bo_BI_all[bankState] = np.zeros(env['num_bank'])[bankState]
        bank.Bo_D[bankState] = np.zeros(env['num_bank'])[bankState]
        interbank.Lo_BI[interbankState] = np.zeros(env['num_bank'], env['num_bank'])[interbankState]
        interbank.Bo_BI[interbankState] = np.zeros(env['num_bank'], env['num_bank'])[interbankState]
        pass

    def update_B_transfer(self, bank: BankCommercial, interbank: BankInterbank, bankState: TypeState, interbankState: TypeState, byWay: str = "all"):
        """
        更新各银行之借贷流量变量。
        # Arguments
        `byWay:str`:  参数，通过该参数指定的变量作为已知变量，驱动，以更新其他相关各变量。
        - `all`:  更新全部借贷流量变量；
        - `clear transfer all`:  清零所有不必要的借贷流量变量；
        - `Lo_P`:  已知``Lo_{B,P}``，更新其余借贷流量变量；
        - `Li_P`:  已知``Li_{B,P}``，更新其余借贷流量变量；
        - `Bi_D`:  已知``Bi_{B,D}``，更新其余借贷流量变量；
        - `Bo_D`:  已知``Bo_{B,D}``，更新其余借贷流量变量；
        - `Lo_BI_all`:  已知``Lo_{BI}[i,: ]``，更新其余借贷流量变量；
        - `Li_BI_all`:  已知``Li_{BI}[i,: ]``，更新其余借贷流量变量；
        - `Bi_BI_all`:  已知``Bi_{BI}[i,: ]``，更新其余借贷流量变量；
        - `Bo_BI_all`:  已知``Bo_{BI}[i,: ]``，更新其余借贷流量变量；
        - `Lo_BI`:  已知``Lo_{BI}``，更新其余借贷流量变量；
        - `Bi_BI`:  已知``Bi_{BI}``，更新其余借贷流量变量；
        - `Bo_BI`:  已知``Bo_{BI}``，更新其余借贷流量变量；
        - `Li_BI`:  已知``Li_{BI}``，更新其余借贷流量变量；
        """
        if byWay == "all":
            self.clear_all_transfer(bank, interbank, bankState, interbankState)
            self.alter_transfer_Lo_BI(interbank, interbankState)
            self.sum_transfer_Bi_BI(bank, interbank, bankState, interbankState)
            self.alter_transfer_Bo_BI(interbank, interbankState)
            self.sum_transfer_Li_BI(bank, interbank, bankState, interbankState)
            self.together_transfer_B_Lo_exBI(bank, bankState)
            self.together_transfer_B_Lo_all(bank, bankState)
            self.together_transfer_B_Li_exBI(bank, bankState)
            self.together_transfer_B_Li_all(bank, bankState)
            self.together_transfer_B_Bi_exBI(bank, bankState)
            self.together_transfer_B_Bi_all(bank, bankState)
            self.together_transfer_B_Bo_exBI(bank, bankState)
            self.together_transfer_B_Bo_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "clear transfer all":
            self.clear_all_transfer(bank, interbank, bankState, interbankState)
            self.alter_transfer_Lo_BI(interbank, TypeState((bank.on | bank.off) & (bank.on | bank.off).T))
            self.sum_transfer_Bi_BI(bank, interbank, TypeState(bank.on | bank.off), TypeState((bank.on | bank.off) & (bank.on | bank.off).T))
            self.alter_transfer_Bo_BI(interbank, TypeState((bank.on | bank.off) & (bank.on | bank.off).T))
            self.sum_transfer_Li_BI(bank, interbank, TypeState(bank.on | bank.off), TypeState((bank.on | bank.off) & (bank.on | bank.off).T))
            self.together_transfer_B_Lo_exBI(bank, TypeState(bank.on | bank.off))
            self.together_transfer_B_Lo_all(bank, TypeState(bank.on | bank.off))
            self.together_transfer_B_Li_exBI(bank, TypeState(bank.on | bank.off))
            self.together_transfer_B_Li_all(bank, TypeState(bank.on | bank.off))
            self.together_transfer_B_Bi_exBI(bank, TypeState(bank.on | bank.off))
            self.together_transfer_B_Bi_all(bank, TypeState(bank.on | bank.off))
            self.together_transfer_B_Bo_exBI(bank, TypeState(bank.on | bank.off))
            self.together_transfer_B_Bo_all(bank, TypeState(bank.on | bank.off))
            self.together_T_all(bank, TypeState(bank.on | bank.off))
        elif byWay == "Lo_P":
            self.together_transfer_B_Lo_exBI(bank, bankState)
            self.together_transfer_B_Lo_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Li_P":
            self.together_transfer_B_Li_exBI(bank, bankState)
            self.together_transfer_B_Li_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Bi_D":
            self.together_transfer_B_Bi_exBI(bank, bankState)
            self.together_transfer_B_Bi_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Bo_D":
            self.together_transfer_B_Bo_exBI(bank, bankState)
            self.together_transfer_B_Bo_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Lo_BI_all":
            self.together_transfer_B_Lo_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Li_BI_all":
            self.together_transfer_B_Li_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Bi_BI_all":
            self.together_transfer_B_Bi_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Bo_BI_all":
            self.together_transfer_B_Bo_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Lo_BI":
            self.alter_transfer_Lo_BI(interbank, interbankState)
            self.sum_transfer_Bi_BI(bank, interbank, bankState, interbankState)
            self.together_transfer_B_Bi_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Bi_BI":
            self.alter_transfer_Bi_BI(interbank, interbankState)
            self.sum_transfer_Bi_BI(bank, interbank, bankState, interbankState)
            self.together_transfer_B_Bi_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Bo_BI":
            self.alter_transfer_Bo_BI(interbank, interbankState)
            self.sum_transfer_Li_BI(bank, interbank, bankState, interbankState)
            self.together_transfer_B_Li_all(bank, bankState)
            self.together_T_all(bank, bankState)
        elif byWay == "Li_BI":
            self.alter_transfer_Li_BI(interbank, interbankState)
            self.sum_transfer_Li_BI(bank, interbank, bankState, interbankState)
            self.together_transfer_B_Li_all(bank, bankState)
            self.together_T_all(bank, bankState)
        else:
            pass
        pass

    pass  # class
