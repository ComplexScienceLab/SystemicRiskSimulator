from SystemicRiskSimulator.external_packages import np, deepcopy, logging
from SystemicRiskSimulator.core.define.define_agents import BankCommercial, BankInterbank
from SystemicRiskSimulator.core.define.define_type import StateType, MoneyType
from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv
from SystemicRiskSimulator.core.define.define_consts import CONST


class Content_Finance:
    """
    财务相关的功能。
    """

    ## NOTE：功能函数集：计算商业银行之资金转移。

    def transfer_B_capital_reverse(self, target: MoneyType, source: MoneyType, shock: MoneyType, flow: MoneyType):
        """
        资金变动之转移资金（资金等量反向变化）。

        NOTE：这个功能用于手动计算。

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
        logging.debug(f"                    transfer_B_capital_reverse")
        return target, source, shock
        pass  # function

    def transfer_B_capital_reduce(self, target: MoneyType, source: MoneyType, shock: MoneyType, flow: MoneyType):
        """
        资金变动之同减资金（资金等量同向减少）。

        NOTE：这个功能用于手动计算。

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
        logging.debug(f"                    transfer_B_capital_reduce")
        return target, source, shock
        pass  # function

    def together_transfer_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之总交易流量``T_{all}``。"""
        bank.T_all[bankState] = bank.Lo_all[bankState] + bank.Bi_all[bankState] + bank.Bo_all[bankState] + bank.Li_all[bankState]
        logging.debug(f"                    together_transfer_all")
        pass  # function

    def together_transfer_B_Lo_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之总贷款流出（贷款方发款出去）``Lo_{B}``。"""
        bank.Lo_all[bankState] = bank.Lo_IB_all[bankState] + bank.Lo_exIB[bankState]
        logging.debug(f"                    together_transfer_B_Lo_all")
        pass  # function

    def together_transfer_B_Lo_exIB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之非银行间贷款流出``Lo_{-IB}``。"""
        bank.Lo_exIB[bankState] = bank.Lo_P[bankState]
        logging.debug(f"                    together_transfer_B_Lo_exIB")
        pass  # function

    def together_transfer_B_Li_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之总贷款流入（贷款方收款回来）``Li_{B}``。"""
        bank.Li_all[bankState] = bank.Li_IB_all[bankState] + bank.Li_exIB[bankState]
        logging.debug(f"                    together_transfer_B_Li_all")
        pass  # function

    def together_transfer_B_Li_exIB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之非银行间贷款流入``Li_{-IB}``。"""
        bank.Li_exIB[bankState] = bank.Li_P[bankState]
        logging.debug(f"                    together_transfer_B_Li_exIB")
        pass  # function

    def together_transfer_B_Bo_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之总借款流出（借款方还款出去）``Bo_{B}``。"""
        bank.Bo_all[bankState] = bank.Bo_IB_all[bankState] + bank.Bo_exIB[bankState]
        logging.debug(f"                    together_transfer_B_Bo_all")
        pass  # function

    def together_transfer_B_Bo_exIB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之非银行间借款流出``Bo_{-IB}``。"""
        bank.Bo_exIB[bankState] = bank.Bo_D[bankState]
        logging.debug(f"                    together_transfer_B_Bo_exIB")
        pass  # function

    def together_transfer_B_Bi_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之总借款流入（借款方借款进来）``Bi_{B}``。"""
        bank.Bi_all[bankState] = bank.Bi_IB_all[bankState] + bank.Bi_exIB[bankState]
        logging.debug(f"                    together_transfer_B_Bi_all")
        pass  # function

    def together_transfer_B_Bi_exIB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之非银行间借款流入``Bi_{-IB}``。"""
        bank.Bi_exIB[bankState] = bank.Bi_D[bankState]
        logging.debug(f"                    together_transfer_B_Bi_exIB")
        pass  # function

    def alter_transfer_Lo_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """转换银行间贷款流出``Lo_{IB}``为银行间借款流入``Bi_{IB}``。"""
        interbank.Bi_IB = interbank.Lo_IB.T
        logging.debug(f"                    alter_transfer_Lo_IB")
        pass  # function

    def alter_transfer_Bi_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """转换银行间借款流入``Bi_{IB}``为银行间贷款流出``Lo_{IB}``。"""
        interbank.Lo_IB = interbank.Bi_IB.T
        logging.debug(f"                    alter_transfer_Bi_IB")
        pass  # function

    def alter_transfer_Bo_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """转换银行间借款流出``Bo_{IB}``为银行间贷款流入``Li_{IB}``。"""
        interbank.Li_IB = interbank.Bo_IB.T
        logging.debug(f"                    alter_transfer_Bo_IB")
        pass  # function

    def alter_transfer_Li_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """转换银行间贷款流入``Li_{IB}``为银行间借款流出``Bo_{IB}``。"""
        interbank.Bo_IB = interbank.Li_IB.T
        logging.debug(f"                    alter_transfer_Li_IB")
        pass  # function

    def sum_transfer_Bi_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """加总各银行之银行间借款流入``Bi_{B}``，通过银行间借款流入邻接矩阵``Bi_{IB}``。"""
        bank.Bi_IB_all[:] = np.sum(interbank.Bi_IB * interbankState, axis=1)
        logging.debug(f"                    sum_transfer_Bi_IB")
        pass  # function

    def sum_transfer_Li_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """加总各银行之银行间贷款流入``Li_{B}``，通过银行间贷款流入邻接矩阵``Li_{IB}``。"""
        bank.Li_IB_all[:] = np.sum(interbank.Li_IB * interbankState, axis=1)
        logging.debug(f"                    sum_transfer_Li_IB")
        pass  # function

    def clear_all_transfer(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """清零所有流量变量值"""
        bank.Lo_IB_all[bankState] = CONST(sgv['num_bank']).ZEROS1.copy()[bankState]
        bank.Lo_P[bankState] = CONST(sgv['num_bank']).ZEROS1.copy()[bankState]
        bank.Li_IB_all[bankState] = CONST(sgv['num_bank']).ZEROS1.copy()[bankState]
        bank.Li_P[bankState] = CONST(sgv['num_bank']).ZEROS1.copy()[bankState]
        bank.Bi_IB_all[bankState] = CONST(sgv['num_bank']).ZEROS1.copy()[bankState]
        bank.Bi_D[bankState] = CONST(sgv['num_bank']).ZEROS1.copy()[bankState]
        bank.Bo_IB_all[bankState] = CONST(sgv['num_bank']).ZEROS1.copy()[bankState]
        bank.Bo_D[bankState] = CONST(sgv['num_bank']).ZEROS1.copy()[bankState]
        interbank.Lo_IB[interbankState] = CONST(sgv['num_bank']).ZEROS2.copy()[interbankState]
        interbank.Bo_IB[interbankState] = CONST(sgv['num_bank']).ZEROS2.copy()[interbankState]
        logging.debug(f"                    clear_all_transfer")
        pass  # function

    ## NOTE：功能函数集：计算冲击。

    def together_Shock_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总总冲击目标"""
        bank.Shock_t[bankState] = bank.Shock_exIB_t[bankState] + bank.Shock_IB_t[bankState]
        logging.debug(f"                    together_Shock_target")
        pass  # function

    def together_Shock_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总总冲击源头"""
        bank.Shock_s[bankState] = bank.Shock_exIB_s[bankState] + bank.Shock_IB_s[bankState]
        logging.debug(f"                    together_Shock_source")
        pass  # function

    def together_Shock_exIB_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总银行外冲击目标"""
        bank.Shock_exIB_t[bankState] = bank.Shock_P_def_t[bankState] + bank.Shock_D_run_t[bankState]
        logging.debug(f"                    together_Shock_exIB_target")
        pass  # function

    def together_Shock_exIB_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总银行外冲击源头"""
        bank.Shock_exIB_s[bankState] = bank.Shock_P_run_s[bankState] + bank.Shock_D_def_s[bankState]
        logging.debug(f"                    together_Shock_exIB_source")
        pass  # function

    def together_Shock_def_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总违约损失冲击目标"""
        bank.Shock_def_t[bankState] = bank.Shock_P_def_t[bankState] + bank.Shock_IB_def_t[bankState]
        logging.debug(f"                    together_Shock_def_target")
        pass  # function

    def together_Shock_def_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总违约损失冲击源头"""
        bank.Shock_def_s[bankState] = bank.Shock_D_def_s[bankState] + bank.Shock_IB_def_s[bankState]
        logging.debug(f"                    together_Shock_def_source")
        pass  # function

    def together_Shock_run_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总挤兑流动冲击目标"""
        bank.Shock_run_t[bankState] = bank.Shock_D_run_t[bankState] + bank.Shock_IB_run_t[bankState]
        logging.debug(f"                    together_Shock_run_target")
        pass  # function

    def together_Shock_run_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总挤兑流动冲击源头"""
        bank.Shock_run_s[bankState] = bank.Shock_P_run_s[bankState] + bank.Shock_IB_run_s[bankState]
        logging.debug(f"                    together_Shock_run_source")
        pass  # function

    def together_Shock_IB_run_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总银行间流动性冲击目标。"""
        bank.Shock_IB_run_t[bankState] = bank.Shock_IB_run_ilq_t[bankState] + bank.Shock_IB_run_br_t[bankState]
        logging.debug(f"                    together_Shock_IB_run_target")
        pass  # function

    def together_Shock_IB_run_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总银行间流动性冲击源头。"""
        bank.Shock_IB_run_s[bankState] = bank.Shock_IB_run_ilq_s[bankState] + bank.Shock_IB_run_br_s[bankState]
        logging.debug(f"                    together_Shock_IB_run_source")
        pass  # function

    def together_Shock_B(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):  # BUG这个做什么的？似乎没有被用到。
        """总银行内资产负债冲击。"""
        bank.Shock_B[bankState] = bank.Shock_B_A[bankState] + bank.Shock_B_Z[bankState]
        logging.debug(f"                    together_Shock_B")
        pass  # function

    def together_Shock_IB_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总银行间冲击源头。"""
        bank.Shock_IB_s[bankState] = bank.Shock_IB_def_s[bankState] + bank.Shock_IB_run_s[bankState]
        logging.debug(f"                    together_Shock_IB_source")
        pass  # function

    def together_Shock_IB_run(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总银行间流动性冲击。"""
        interbank.Shock_IB_run[interbankState] = interbank.Shock_IB_run_ilq[interbankState] + interbank.Shock_IB_run_br[interbankState]
        logging.debug(f"                    together_Shock_IB_run")
        pass  # function

    def together_Shock_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总银行间冲击。"""
        interbank.Shock_IB[interbankState] = interbank.Shock_IB_def[interbankState] + interbank.Shock_IB_run[interbankState]
        logging.debug(f"                    together_Shock_IB")
        pass  # function

    def sum_Shock_IB_def_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总资不抵债银行之银行间违约损失冲击目标。"""
        bank.Shock_IB_def_t[bankState] = np.sum(interbank.Shock_IB_def * interbankState, axis=0)[bankState]
        logging.debug(f"                    sum_Shock_IB_def_target")
        pass  # function

    def sum_Shock_IB_run_ilq_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总流动性短缺银行之银行间流动性冲击目标。"""
        bank.Shock_IB_run_ilq_t[bankState] = np.sum(interbank.Shock_IB_run_ilq * interbankState, axis=0)[bankState]
        logging.debug(f"                    sum_Shock_IB_run_ilq_target")
        pass  # function

    def sum_Shock_IB_run_br_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总破产银行之银行间流动性冲击目标。"""
        bank.Shock_IB_run_br_t[bankState] = np.sum(interbank.Shock_IB_run_br * interbankState, axis=0)[bankState]
        logging.debug(f"                    sum_Shock_IB_run_br_target")
        pass  # function

    def together_Shock_IB_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总银行间冲击目标。"""
        bank.Shock_IB_t[bankState] = bank.Shock_IB_def_t[bankState] + bank.Shock_IB_run_t[bankState]
        logging.debug(f"                    together_Shock_IB_target")
        pass  # function

    def conduct_Shock_D(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """传导存款损失外生冲击。"""  # HACK暂不使用。
        bank.Shock_B_Z[bankState] = bank.Shock_D_run_t[bankState]
        logging.debug(f"                    conduct_Shock_D")
        pass  # function

    def conduct_Shock_IB_def_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """传导银行间违约损失冲击。"""  # HACK暂不使用。
        bank.Shock_B_A[bankState] = bank.Shock_IB_def_t[bankState]
        logging.debug(f"                    conduct_Shock_IB_def_t")
        pass  # function

    def conduct_Shock_IB_run_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """传导银行间挤兑流动冲击。"""  # HACK暂不使用。
        bank.Shock_B_A[bankState] = bank.Shock_IB_run_t[bankState]
        logging.debug(f"                    conduct_Shock_IB_run_t")
        pass  # function

    def clear_Shock_IB_and_exIB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):  # BUG是否会出现乱清零的麻烦？
        """清零本回合结束时所有不必要的冲击变量"""
        bank.Shock_P_def_t = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_D_run_t = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_P_run_s = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_D_def_s = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_def_s = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_run_ilq_s = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_run_br_s = CONST(sgv['num_bank']).ZEROS1.copy()
        interbank.Shock_IB_def = CONST(sgv['num_bank']).ZEROS2.copy()
        interbank.Shock_IB_run_ilq = CONST(sgv['num_bank']).ZEROS2.copy()
        interbank.Shock_IB_run_br = CONST(sgv['num_bank']).ZEROS2.copy()
        bank.Shock_IB_def_t = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_run_ilq_t = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_run_br_t = CONST(sgv['num_bank']).ZEROS1.copy()
        logging.debug(f"                    clear_Shock_IB_and_exIB")
        pass  # function

    def clear_Shock_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """清零所有不必要的目标冲击变量"""
        bank.Shock_IB_def_t = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_run_ilq_t = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_run_br_t = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_P_def_t = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_D_run_t = CONST(sgv['num_bank']).ZEROS1.copy()
        logging.debug(f"                    clear_Shock_target")
        pass  # function

    def clear_Shock_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """清零所有不必要的源头冲击变量"""
        bank.Shock_D_def_s = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_P_run_s = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_def_s = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_run_ilq_s = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_IB_run_br_s = CONST(sgv['num_bank']).ZEROS1.copy()
        logging.debug(f"                    clear_Shock_source")
        pass  # function

    def clear_Shock_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """清零所有不必要的银行间冲击变量"""
        interbank.Shock_IB_def = CONST(sgv['num_bank']).ZEROS2.copy()
        interbank.Shock_IB_run_ilq = CONST(sgv['num_bank']).ZEROS2.copy()
        interbank.Shock_IB_run_br = CONST(sgv['num_bank']).ZEROS2.copy()
        logging.debug(f"                    clear_Shock_IB")
        pass  # function

    def clear_Shock_inB(self, bank: BankCommercial):
        """清零本回合中期所有不必要的冲击变量"""  # HACK无用
        bank.Shock_B_A = CONST(sgv['num_bank']).ZEROS1.copy()
        bank.Shock_B_Z = CONST(sgv['num_bank']).ZEROS1.copy()
        logging.debug(f"                    clear_Shock_inB")
        pass  # function

    ## NOTE：功能函数集：计算损失。

    def together_Loss_exIB_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之非银行间损失目标"""
        bank.Loss_exIB_t[bankState] = bank.Loss_exIB_def_t[bankState]
        logging.debug(f"                    together_Loss_exIB_target")
        pass  # function

    def together_Loss_IB_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之银行间损失目标"""
        bank.Loss_IB_t[bankState] = bank.Loss_IB_def_t[bankState] + bank.Loss_IB_run_t[bankState]
        logging.debug(f"                    together_Loss_IB_target")
        pass  # function

    def together_Loss_def_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之资产违约损失目标"""
        bank.Loss_def_t[bankState] = bank.Loss_exIB_def_t[bankState] + bank.Loss_IB_def_t[bankState]
        logging.debug(f"                    together_Loss_def_target")
        pass  # function

    def together_Loss_run_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之挤兑流动损失目标"""
        bank.Loss_run_t[bankState] = bank.Loss_exIB_run_t[bankState] + bank.Loss_IB_run_t[bankState]
        logging.debug(f"                    together_Loss_run_target")
        pass  # function

    def together_Loss_target_by_kind_of_sector(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之总损失目标，通过部门类型"""
        bank.Loss_t[bankState] = bank.Loss_exIB_t[bankState] + bank.Loss_IB_t[bankState]
        logging.debug(f"                    together_Loss_target_by_kind_of_sector")
        pass  # function

    def together_Loss_target_by_kind_of_contagion(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之总损失目标，通过传染类型"""
        bank.Loss_t[bankState] = bank.Loss_def_t[bankState] + bank.Loss_run_t[bankState]
        logging.debug(f"                    together_Loss_target_by_kind_of_contagion")
        pass  # function

    ## NOTE：功能函数集：计算违约。

    def together_Default_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总银行之总违约源头"""
        bank.Default_s[bankState] = bank.Default_IB_s[bankState] + bank.Default_exIB_s[bankState]
        logging.debug(f"                    together_Default_source")
        pass  # function

    def together_Default_IB_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总银行之银行间违约源头"""
        bank.Default_IB_s[bankState] = bank.Default_IB_def_s[bankState] + bank.Default_IB_run_s[bankState]
        logging.debug(f"                    together_Default_IB_source")
        pass  # function

    def together_Default_exIB_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总银行之银行间违约源头"""
        bank.Default_exIB_s[bankState] = bank.Default_D_def_s[bankState] + bank.Default_D_run_s[bankState]
        logging.debug(f"                    together_Default_exIB_source")
        pass  # function

    ## NOTE：功能函数集：计算收回量。

    def together_Recover_run_source(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总银行之挤兑的收回量源头"""
        bank.Recover_run_s[bankState] = bank.Recover_IB_run_s[bankState] + bank.Recover_P_run_s[bankState]
        logging.debug(f"                    together_Recover_run_source")
        pass  # function

    ## NOTE：功能函数集：计算偿还量。

    def together_Repay_run_target(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总银行之挤兑的偿还量目标"""
        bank.Repay_run_t[bankState] = bank.Repay_IB_run_t[bankState] + bank.Repay_D_run_t[bankState]
        logging.debug(f"                    together_Repay_run_target")
        pass  # function

    ## NOTE：功能函数集：计算商业银行之资产负债表结构。

    def together_B_A_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之总资产。"""
        bank.A_all[bankState] = bank.A_IB_all[bankState] + bank.A_exIB[bankState]
        logging.debug(f"                    together_B_A_all")
        pass  # function

    def sum_B_A_IB(self, bank: BankCommercial, interbank: BankInterbank, bankList: StateType, interbankList: StateType):
        """加总各银行之银行间总资产，通过银行间资产邻接矩阵。"""
        bank.A_IB_all[:] = np.sum(interbank.A_IB * interbankList, axis=1)
        logging.debug(f"                    sum_B_A_IB")
        pass  # function

    def together_B_A_exIB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之非银行间资产``A_{-IB}``。"""
        bank.A_exIB[bankState] = bank.A_P[bankState] + bank.A_Q[bankState] + bank.A_R[bankState] + bank.A_other[bankState]
        logging.debug(f"                    together_B_A_exIB")
        pass  # function

    def together_B_Z_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之总负债。"""
        bank.Z_all[bankState] = bank.Z_IB_all[bankState] + bank.Z_exIB[bankState]
        logging.debug(f"                    together_B_Z_all")
        pass  # function

    def sum_B_Z_IB(self, bank: BankCommercial, interbank: BankInterbank, bankList: StateType, interbankList: StateType):
        """加总各银行之银行间总负债，通过银行间负债邻接矩阵。"""
        bank.Z_IB_all[:] = np.sum(interbank.Z_IB * interbankList, axis=1)
        logging.debug(f"                    sum_B_Z_IB")
        pass  # function

    def together_B_Z_exIB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """汇总各银行之非银行间负债``Z_{-IB}``。"""
        bank.Z_exIB[bankState] = bank.Z_D[bankState] + bank.Z_CB[bankState] + bank.Z_other[bankState]
        logging.debug(f"                    together_B_Z_exIB")
        pass  # function

    def calc_B_E_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):  # BUG是否考虑E_all负数？还是手动计算？
        """计算各银行之所有者权益``E_{B}``，通过总资产与总负债差值。#DEBUG"""
        bank.E_all[bankState] = bank.A_all[bankState] - bank.Z_all[bankState] - CONST(sgv['num_bank']).LESS1[bankState]  # 允许E_all为负数
        # bank.E_all[bankState] = np.maximum(bank.A_all[bankState] - bank.Z_all[bankState], 0.0)  # 不允许E_all为负数
        # bank.E_all[bankState] = bank.E_all[bankState]  # 这里改成了手动计算，并没有自动计算。请自行加入合理的计算逻辑表达式。
        logging.debug(f"                    calc_B_E_all")
        pass  # function

    def alter_Z_IB(self, interbank: BankInterbank):
        """转换银行间负债为资产。"""
        interbank.A_IB = interbank.Z_IB.T
        logging.debug(f"                    alter_Z_IB")
        pass  # function

    def alter_A_IB(self, interbank: BankInterbank):
        """转换银行间资产为负债。"""
        interbank.Z_IB = interbank.A_IB.T
        logging.debug(f"                    alter_A_IB")
        pass  # function

    ## NOTE：功能函数集：银行与银行间相关状态及其转换。

    def calc_state_on(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """
        计算示性向量之于银行存在的。
        Args:
            bank (BankCommercial): 银行个体众
            interbank (BankInterbank): 银行间个体众

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = (bank.hel | bank.isv | bank.ilq | bank.br)
        source_state_changes = (bank.on != result)
        bank.on = result
        interbank.on = np.outer(bank.on, bank.on)
        logging.debug(f"                    calc_state_on")
        return source_state_changes
        pass  # function

    def calc_state_healthy(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """
        计算示性向量之于银行健康的。
        Args:
            bank (BankCommercial): 银行个体众
            interbank (BankInterbank): 银行间个体众

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = (
                (bank.E_all >= CONST(sgv['num_bank']).LESS1) &
                (bank.A_Q >= CONST(sgv['num_bank']).LESS1) &
                # (bank.Shock_def_t + CONST(sgv['num_bank']).LESS1 <= bank.E_all) &
                # (bank.Shock_run_t + CONST(sgv['num_bank']).LESS1 <= bank.A_Q) &
                # (bank.Default_s + CONST(sgv['num_bank']).LESS1 <= bank.E_all) &
                (bank.Loss_t + CONST(sgv['num_bank']).LESS1 <= bank.E_all) &
                (bank.on)
        )
        source_state_changes = (bank.hel != result)
        bank.hel = result
        interbank.hel = np.outer(bank.hel, bank.hel)
        logging.debug(f"                    calc_state_healthy")
        return source_state_changes
        pass  # function

    def calc_state_insolvent(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """
        计算示性向量之于银行资不抵债的。#BUG
        Args:
            bank (BankCommercial): 银行个体众
            interbank (BankInterbank): 银行间个体众

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = (
                (
                        (bank.A_all < bank.Z_all + CONST(sgv['num_bank']).LESS1) |
                        (bank.E_all < CONST(sgv['num_bank']).LESS1) |
                        # (bank.Shock_def_t + CONST(sgv['num_bank']).LESS1 > bank.E_all) |
                        # (bank.Default_s + CONST(sgv['num_bank']).LESS1 > bank.E_all) |
                        (bank.Loss_t + CONST(sgv['num_bank']).LESS1 > bank.E_all)
                ) &
                (bank.on)
        )
        source_state_changes = (bank.isv != result)
        bank.isv = result
        interbank.isv = np.outer(bank.isv, bank.isv)
        logging.debug(f"                    calc_state_insolvent")
        return source_state_changes
        pass  # function

    def calc_state_illiquid(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """
        计算示性向量之于银行流动性短缺的。
        Args:
            bank (BankCommercial): 银行个体众
            interbank (BankInterbank): 银行间个体众

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = (
                (
                        (bank.A_Q < CONST(sgv['num_bank']).LESS1) |
                        (bank.Shock_run_t + CONST(sgv['num_bank']).LESS1 > bank.A_Q)
                ) &
                (bank.on)
        )
        source_state_changes = (bank.ilq != result)
        bank.ilq = result
        interbank.ilq = np.outer(bank.ilq, bank.ilq)
        logging.debug(f"                    calc_state_illiquid")
        return source_state_changes
        pass  # function

    def calc_state_bankrupt(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """
        计算示性向量之于银行破产的。
        Args:
            bank (BankCommercial): 银行个体众
            interbank (BankInterbank): 银行间个体众

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = (bank.isv | bank.ilq)  # TODO 这个仅仅是目前基准模型简化的做法
        source_state_changes = (bank.br != result)
        bank.br = result
        interbank.br = np.outer(bank.br, bank.br)
        logging.debug(f"                    calc_state_bankrupt")
        return source_state_changes
        pass  # function

    def calc_state_off(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """
        计算示性向量之于银行退出的。
        Args:
            bank (BankCommercial): 银行个体众
            interbank (BankInterbank): 银行间个体众

        Returns:
            result: 示性向量之计算后的。
            source_state_changes: 示性向量之源状态改变的。

        """
        result = bank.br | bank.off
        source_state_changes = (bank.off != result)
        bank.off = result
        interbank.off = np.outer(bank.off, bank.off)
        logging.debug(f"                    calc_state_off")
        return source_state_changes
        pass  # function

    ## NOTE：功能函数集：计算状态功能
    ## #NOTE 以下的几个计算函数将在模型内容中单独使用，不用于联动同步计算。

    def calc_state_isEnabledBoIB(self, bank: BankCommercial):
        """
        计算示性向量之于银行能够偿还银行间负债的。
        Args:
            bank (BankCommercial): 银行个体众
        """
        bank.is_enabled_BoIB = ((bank.Shock_IB_run_ilq_t > 0) & (bank.A_Q > 0) & bank.on)
        logging.debug(f"                    calc_state_isEnabledBoIB")
        pass  # function

    def calc_state_isEnabledBoD(self, bank: BankCommercial):
        """
        计算示性向量之于银行能够偿还居民部门存款的。

        这里的设定条件是，在计划偿还顺序的时候，优先偿还挤兑存款，然后偿还银行间借款，但是在执行偿还顺序的时候，优先偿还银行间借款，再偿还挤兑存款。

        Args:
            bank (BankCommercial): 银行个体众

        """

        bank.is_enabled_BoD = ((bank.Shock_D_run_t > 0) & (bank.A_Q - bank.Repay_IB_run_t > 0) & bank.on)
        logging.debug(f"                    calc_state_isEnabledBoD")
        pass  # function

    def calc_state_isEnabledLiP(self, bank: BankCommercial):
        """
        计算示性向量之于银行能够收回厂商贷款的。
        Args:
            bank (BankCommercial): 银行个体众

        """

        bank.is_enabled_LiP = ((bank.Shock_P_run_s > 0) & bank.on)
        logging.debug(f"                    calc_state_isEnabledLiP")
        pass  # function

    def update_state_healthy_from_insolvent(self, bank: BankCommercial, interbank: BankInterbank, source_state_changes: StateType):
        """
        更新示性向量之于银行健康的，从资不抵债的。

        Args:
            bank (BankCommercial): 银行个体众
            interbank (BankInterbank): 银行间个体众
            source_state_changes (StateType): 示性向量之源状态改变的。

        Returns:
            None

        """
        bank.hel[source_state_changes] = ~(bank.isv[source_state_changes] | bank.ilq[source_state_changes])
        interbank.hel = np.outer(bank.hel, bank.hel)
        logging.debug(f"                    update_state_healthy_from_insolvent")
        pass  # function

    def update_state_healthy_from_illiquid(self, bank: BankCommercial, interbank: BankInterbank, source_state_changes: StateType):
        """
        更新示性向量之于银行健康的，从流动性短缺的的。

        Args:
            bank (BankCommercial): 银行个体众
            interbank (BankInterbank): 银行间个体众
            source_state_changes (StateType): 示性向量之源状态改变的。

        Returns:
            None

        """
        bank.hel[source_state_changes] = ~(bank.isv[source_state_changes] | bank.ilq[source_state_changes])
        interbank.hel = np.outer(bank.hel, bank.hel)
        logging.debug(f"                    update_state_healthy_from_illiquid")
        pass  # function

    def update_state_on_from_off(self, bank: BankCommercial, interbank: BankInterbank, source_state_changes: StateType):
        """
        更新示性向量之于银行健康的，从流动性短缺的的。

        Args:
            bank (BankCommercial): 银行个体众
            interbank (BankInterbank): 银行间个体众
            source_state_changes (StateType): 示性向量之源状态改变的。

        Returns:
            None

        """
        bank.on[source_state_changes] = ~bank.off[source_state_changes]
        interbank.on = np.outer(bank.on, bank.on)
        logging.debug(f"                    update_state_on_from_off")
        pass  # function

    def calc_list_of_creditor_in_state_of_banks(self, interbank: BankInterbank, isState: StateType):
        """
        计算指定的状态的银行之债权方银行示性矩阵。

        Args:
            interbank (BankInterbank): BankInterbank
            isState (StateType): 示性向量之于银行指定的状态。

        Returns: is_exposure_of_creditor_in_state_of_banks

        """

        # 计算示性矩阵之于银行间风险敞口的
        is_exposure_of_creditor_in_state_of_banks = ((interbank.Z_IB > 0.0) & isState[:, np.newaxis])
        logging.debug(f"                    calc_list_of_creditor_in_state_of_banks")
        return is_exposure_of_creditor_in_state_of_banks

        # # 计算示性矩阵之于银行间风险敞口的
        # is_exposure_of_creditor_in_state_of_banks = np.where(
        #     (interbank.Z_IB > 0.0) & isState[:, np.newaxis]
        # )
        # return is_exposure_of_creditor_in_state_of_banks

        # list_of_relation_in_state_of_banks = np.array([np.array(None) for i in range(sgv['num_bank'])])  # TODO 无用
        # for i in range(sgv['num_bank']):
        #     list_of_relation_in_state_of_banks[i] = np.where(is_exposure_of_creditor_in_state_of_banks[i, :])[0]  # 获取对应状态下的债权或者债务关系的银行列表
        #     pass  # for
        # logging.debug(f"                    calc_list_of_relation_in_state_of_banks")
        # return list_of_relation_in_state_of_banks
        pass  # function

    def calc_list_of_debtor_in_state_of_banks(self, interbank: BankInterbank, isState: StateType):
        """
        计算指定的状态的银行之债务方银行示性矩阵。

        Args:
            interbank (BankInterbank): BankInterbank
            isState (StateType): 示性向量之于银行指定的状态。

        Returns: is_exposure_of_debtor_in_state_of_banks

        """

        # 计算示性矩阵之于银行间风险敞口的
        is_exposure_of_debtor_in_state_of_banks = ((interbank.A_IB > 0.0) & isState[:, np.newaxis])
        logging.debug(f"                    calc_list_of_debtor_in_state_of_banks")
        return is_exposure_of_debtor_in_state_of_banks

        pass  # function

    def update_relation_in_state_of_banks(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        ## 更新银行间市场interbank之各状态下之信息列表之于各银行之债权方与债务方之银行编号。#BUG
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.cre_br = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.br)
        interbank.deb_br = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.br)
        logging.debug(f"                    update_relation_in_state_of_banks")
        pass  # function

    ## NOTE 其他功能部分

    update_variable_name: str = None
    update_variable_value = None

    ## NOTE：功能函数集：更新流之商业银行之资金转移变量

    def update_by_Lo_P(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_transfer_B_Lo_exIB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Lo_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Li_P(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_transfer_B_Li_exIB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Li_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Bo_D(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_transfer_B_Bo_exIB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Bo_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Lo_IB_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_transfer_B_Lo_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Li_IB_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_transfer_B_Li_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Bi_IB_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_transfer_B_Bi_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Bo_IB_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_transfer_B_Bo_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Lo_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.alter_transfer_Lo_IB(bank, interbank, bankState, interbankState)
        self.sum_transfer_Bi_IB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Bi_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Bi_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.alter_transfer_Bi_IB(bank, interbank, bankState, interbankState)
        self.sum_transfer_Bi_IB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Bi_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Bo_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.alter_transfer_Bo_IB(bank, interbank, bankState, interbankState)
        self.sum_transfer_Li_IB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Li_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Li_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.alter_transfer_Li_IB(bank, interbank, bankState, interbankState)
        self.sum_transfer_Li_IB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Li_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Bi_D(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_transfer_B_Bi_exIB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Bi_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_clear_transfer_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.clear_all_transfer(bank, interbank, bankState, interbankState)
        self.alter_transfer_Lo_IB(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.sum_transfer_Bi_IB(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.alter_transfer_Bo_IB(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.sum_transfer_Li_IB(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.together_transfer_B_Lo_exIB(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.together_transfer_B_Lo_all(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.together_transfer_B_Li_exIB(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.together_transfer_B_Li_all(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.together_transfer_B_Bi_exIB(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.together_transfer_B_Bi_all(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.together_transfer_B_Bo_exIB(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.together_transfer_B_Bo_all(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        self.together_transfer_all(bank, interbank, (bank.on | bank.off), np.outer((bank.on | bank.off), (bank.on | bank.off)))
        pass  # function

    ## NOTE：功能函数集：更新流之冲击变量。

    def update_by_Shock_P_def_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_exIB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_def_target(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_Shock_P_run_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_exIB_source(bank, interbank, bankState, interbankState)
        self.together_Shock_source(bank, interbank, bankState, interbankState)
        self.together_Shock_run_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Shock_D_run_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_exIB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_run_target(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='illiquid')  # DEBUG
        source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)  # by_way='illiquid'
        self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        pass  # function

    def update_by_Shock_D_def_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_exIB_source(bank, interbank, bankState, interbankState)
        self.together_Shock_source(bank, interbank, bankState, interbankState)
        self.together_Shock_def_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Shock_IB_def_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_IB_source(bank, interbank, bankState, interbankState)
        self.together_Shock_source(bank, interbank, bankState, interbankState)
        self.together_Shock_def_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Shock_IB_run_ilq_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_IB_run_source(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_source(bank, interbank, bankState, interbankState)
        self.together_Shock_source(bank, interbank, bankState, interbankState)
        self.together_Shock_run_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Shock_IB_run_br_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_IB_run_source(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_source(bank, interbank, bankState, interbankState)
        self.together_Shock_source(bank, interbank, bankState, interbankState)
        self.together_Shock_run_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Shock_IB_def(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_IB(bank, interbank, bankState, interbankState)
        self.sum_Shock_IB_def_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_def_target(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_Shock_IB_run_ilq(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_IB_run(bank, interbank, bankState, interbankState)
        self.together_Shock_IB(bank, interbank, bankState, interbankState)
        self.sum_Shock_IB_run_ilq_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_run_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_run_target(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='illiquid')  # DEBUG
        source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)  # by_way='illiquid'
        self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        pass  # function

    def update_by_Shock_IB_run_br(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_IB_run(bank, interbank, bankState, interbankState)
        self.together_Shock_IB(bank, interbank, bankState, interbankState)
        self.sum_Shock_IB_run_br_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_run_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_run_target(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='illiquid')  # DEBUG
        source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)  # by_way='illiquid'
        self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        pass  # function

    def update_by_Shock_IB_def_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_IB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_def_target(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_Shock_IB_run_ilq_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_IB_run_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_run_target(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='illiquid')  # DEBUG
        source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)  # by_way='illiquid'
        self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        pass  # function

    def update_by_Shock_IB_run_br_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Shock_IB_run_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_run_target(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='illiquid')  # DEBUG
        source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)  # by_way='illiquid'
        self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        pass  # function

    def update_by_clear_Shock_IB_and_Shock_exIB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.clear_Shock_IB_and_exIB(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_run_source(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_IB_source(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_exIB_source(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_source(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_def_source(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_run_source(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_IB_run(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_IB(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_IB_run_target(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_IB_target(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_exIB_target(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_target(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        self.together_Shock_def_target(bank, interbank, StateType(bank.on | bank.off), StateType(np.outer((bank.on | bank.off), (bank.on | bank.off))))
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        self.together_Shock_run_target(bank, StateType(bank.on | bank.off))
        # self.update_states(bank, interbank, by_way='illiquid')  # DEBUG
        source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)  # by_way='illiquid'
        self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        # self.update_states(bank, interbank, by_way='all')  # DEBUG 是否多余
        _ = self.calc_state_on(bank, interbank, bankState, interbankState)  # by_way='all'
        _ = self.calc_state_healthy(bank, interbank, bankState, interbankState)
        _ = self.calc_state_insolvent(bank, interbank, bankState, interbankState)
        _ = self.calc_state_illiquid(bank, interbank, bankState, interbankState)
        _ = self.calc_state_bankrupt(bank, interbank, bankState, interbankState)
        _ = self.calc_state_off(bank, interbank, bankState, interbankState)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.cre_br = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.br)
        interbank.deb_br = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.br)
        pass  # function

    def update_by_clear_all_Shock_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.clear_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_run_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_exIB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_def_target(bank, interbank, bankState, interbankState)
        self.together_Shock_run_target(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_clear_all_Shock_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.clear_Shock_source(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_run_source(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_source(bank, interbank, bankState, interbankState)
        self.together_Shock_exIB_source(bank, interbank, bankState, interbankState)
        self.together_Shock_source(bank, interbank, bankState, interbankState)
        self.together_Shock_def_source(bank, interbank, bankState, interbankState)
        self.together_Shock_run_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_clear_all_Shock_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.clear_Shock_IB(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_run(bank, interbank, bankState, interbankState)
        self.together_Shock_IB(bank, interbank, bankState, interbankState)
        pass  # function

    ## NOTE：功能函数集：更新流之损失变量。

    def update_by_Loss_exIB_def_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Loss_exIB_target(bank, interbank, bankState, interbankState)
        self.together_Loss_def_target(bank, interbank, bankState, interbankState)
        self.together_Loss_target_by_kind_of_sector(bank, interbank, bankState, interbankState)
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        pass  # function

    def update_by_Loss_IB_def_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Loss_IB_target(bank, interbank, bankState, interbankState)
        self.together_Loss_def_target(bank, interbank, bankState, interbankState)
        self.together_Loss_target_by_kind_of_sector(bank, interbank, bankState, interbankState)
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        pass  # function

    def update_by_Loss_exIB_run_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Loss_exIB_target(bank, interbank, bankState, interbankState)
        self.together_Loss_run_target(bank, interbank, bankState, interbankState)
        self.together_Loss_target_by_kind_of_sector(bank, interbank, bankState, interbankState)
        source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)  # by_way='illiquid'
        self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
        pass  # function

    def update_by_Loss_IB_run_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Loss_IB_target(bank, interbank, bankState, interbankState)
        self.together_Loss_run_target(bank, interbank, bankState, interbankState)
        self.together_Loss_target_by_kind_of_sector(bank, interbank, bankState, interbankState)
        source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)  # by_way='illiquid'
        self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
        pass  # function

    ## NOTE：功能函数集：更新流之违约变量。

    def update_by_Default_D_run_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Default_exIB_source(bank, interbank, bankState, interbankState)
        self.together_Default_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Default_D_def_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Default_exIB_source(bank, interbank, bankState, interbankState)
        self.together_Default_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Default_IB_run_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Default_IB_source(bank, interbank, bankState, interbankState)
        self.together_Default_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Default_IB_def_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Default_IB_source(bank, interbank, bankState, interbankState)
        self.together_Default_source(bank, interbank, bankState, interbankState)
        pass  # function

    ## NOTE：功能函数集：更新流之收回变量。

    def update_by_Recover_IB_run_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Recover_run_source(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Recover_P_run_s(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Recover_run_source(bank, interbank, bankState, interbankState)
        pass  # function

    ## NOTE：功能函数集：更新流之偿还变量。

    def update_by_Repay_D_run_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Repay_run_target(bank, interbank, bankState, interbankState)
        pass  # function

    def update_by_Repay_IB_run_t(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_Repay_run_target(bank, interbank, bankState, interbankState)
        pass  # function

    ## NOTE：功能函数集：计算流之商业银行之资产负债表变量。

    def update_by_A_P(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_B_A_exIB(bank, interbank, bankState, interbankState)
        self.together_B_A_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_A_R(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_B_A_exIB(bank, interbank, bankState, interbankState)
        self.together_B_A_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_A_other(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_B_A_exIB(bank, interbank, bankState, interbankState)
        self.together_B_A_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_A_Q(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_B_A_exIB(bank, interbank, bankState, interbankState)
        self.together_B_A_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='illiquid')  # DEBUG
        source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)  # by_way='illiquid'
        self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_A_IB_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_B_A_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_Z_D(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_B_Z_exIB(bank, interbank, bankState, interbankState)
        self.together_B_Z_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_Z_CB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_B_Z_exIB(bank, interbank, bankState, interbankState)
        self.together_B_Z_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_Z_other(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_B_Z_exIB(bank, interbank, bankState, interbankState)
        self.together_B_Z_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_Z_IB_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.together_B_Z_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_A_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.alter_A_IB(interbank)
        self.sum_B_A_IB(bank, interbank, bankState, interbankState)
        self.together_B_A_all(bank, interbank, bankState, interbankState)
        self.sum_B_Z_IB(bank, interbank, bankState, interbankState)
        self.together_B_Z_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    def update_by_Z_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.alter_Z_IB(interbank)
        self.sum_B_Z_IB(bank, interbank, bankState, interbankState)
        self.together_B_Z_all(bank, interbank, bankState, interbankState)
        self.sum_B_A_IB(bank, interbank, bankState, interbankState)
        self.together_B_A_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)  # DEBUG 检查是否正确。
        # self.update_states(bank, interbank, by_way='insolvent')  # DEBUG
        source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)  # by_way='insolvent'
        self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        pass  # function

    ## NOTE：功能函数集：更新流之状态变量

    def update_by_enabled_collect_A_P(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.calc_state_isEnabledLiP(bank)  # by_way='enabled collect A_P'
        pass  # function

    def update_by_enabled_repay_Z_D(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.calc_state_isEnabledBoD(bank)  # by_way='enabled repay Z_D'
        pass  # function

    def update_by_enabled_repay_IB(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.calc_state_isEnabledBoIB(bank)  # by_way='enabled repay IB'
        pass  # function

    #
    # def update_states(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType, by_way: str = 'all'):
    #     """
    #     更新各状态。#HACK 已经无用，但是保留。因为有一些写好了但是没有用到，备用。
    #
    #     Args:
    #         bank (BankCommercial): 银行个体众
    #         interbank (BankInterbank): 银行间个体众
    #         by_way (str): 更新方式
    #
    #     by_way:
    #         - ``all``:  计算所有的状态；
    #         - ``healthy``:  从健康状态计算；
    #         - ``insolvent``:  从资不抵债状态计算；
    #         - ``illiquid``:  从流动性短缺状态计算；
    #         - ``bankrupt``:  从破产状态计算；
    #         - ``off``:  从退出状态计算；
    #         - ``enabled repay IB``:  从是否可以偿还银行间借款状态计算；
    #         - ``enabled repay Z_D``:  从是否需要偿还借款状态计算；
    #         - ``enabled collect A_P``:  从是否可以收回厂商贷款状态计算；
    #
    #
    #     Returns:
    #
    #     """
    #
    #     if by_way == 'insolvent':
    #         source_state_changes = self.calc_state_insolvent(bank, interbank, bankState, interbankState)
    #         self.update_state_healthy_from_insolvent(bank, interbank, source_state_changes)
    #         interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
    #         interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
    #     elif by_way == 'illiquid':
    #         source_state_changes = self.calc_state_illiquid(bank, interbank, bankState, interbankState)
    #         self.update_state_healthy_from_illiquid(bank, interbank, source_state_changes)
    #         interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
    #         interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
    #     elif by_way == 'bankrupt':
    #         _ = self.calc_state_bankrupt(bank, interbank, bankState, interbankState)
    #         interbank.cre_br = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.br)
    #         interbank.deb_br = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.br)
    #     elif by_way == 'off':
    #         source_state_changes = self.calc_state_off(bank, interbank, bankState, interbankState)
    #         self.update_state_on_from_off(bank, interbank, source_state_changes)
    #     elif by_way == 'healthy':
    #         _ = self.calc_state_healthy(bank, interbank, bankState, interbankState)
    #     elif by_way == 'on':
    #         _ = self.calc_state_on(bank, interbank, bankState, interbankState)
    #     elif by_way == 'enabled repay IB':
    #         self.calc_state_isEnabledBoIB(bank)
    #     elif by_way == 'enabled repay Z_D':
    #         self.calc_state_isEnabledBoD(bank)
    #     elif by_way == 'enabled collect A_P':
    #         self.calc_state_isEnabledLiP(bank)
    #     elif by_way == 'all':
    #         _ = self.calc_state_on(bank, interbank, bankState, interbankState)
    #         _ = self.calc_state_healthy(bank, interbank, bankState, interbankState)
    #         _ = self.calc_state_insolvent(bank, interbank, bankState, interbankState)
    #         _ = self.calc_state_illiquid(bank, interbank, bankState, interbankState)
    #         _ = self.calc_state_bankrupt(bank, interbank, bankState, interbankState)
    #         _ = self.calc_state_off(bank, interbank, bankState, interbankState)
    #         interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
    #         interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
    #         interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
    #         interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
    #         interbank.cre_br = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.br)
    #         interbank.deb_br = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.br)
    #         pass  # if
    #
    #     pass  # function

    ## NOTE：功能函数集：更新流之全部变量

    def update_by_all(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        self.clear_all_transfer(bank, interbank, bankState, interbankState)
        self.alter_transfer_Lo_IB(bank, interbank, bankState, interbankState)
        self.sum_transfer_Bi_IB(bank, interbank, bankState, interbankState)
        self.alter_transfer_Bo_IB(bank, interbank, bankState, interbankState)
        self.sum_transfer_Li_IB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Lo_exIB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Lo_all(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Li_exIB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Li_all(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Bi_exIB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Bi_all(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Bo_exIB(bank, interbank, bankState, interbankState)
        self.together_transfer_B_Bo_all(bank, interbank, bankState, interbankState)
        self.together_transfer_all(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_run_source(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_source(bank, interbank, bankState, interbankState)
        self.together_Shock_exIB_source(bank, interbank, bankState, interbankState)
        self.together_Shock_source(bank, interbank, bankState, interbankState)
        self.together_Shock_def_source(bank, interbank, bankState, interbankState)
        self.together_Shock_run_source(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_run(bank, interbank, bankState, interbankState)
        self.together_Shock_IB(bank, interbank, bankState, interbankState)
        self.sum_Shock_IB_def_target(bank, interbank, bankState, interbankState)
        self.sum_Shock_IB_run_ilq_target(bank, interbank, bankState, interbankState)
        self.sum_Shock_IB_run_br_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_run_target(bank, interbank, bankState, interbankState)
        self.together_Shock_IB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_exIB_target(bank, interbank, bankState, interbankState)
        self.together_Shock_target(bank, interbank, bankState, interbankState)
        self.together_Shock_def_target(bank, interbank, bankState, interbankState)
        self.together_Shock_run_target(bank, interbank, bankState, interbankState)
        self.together_B_A_exIB(bank, interbank, bankState, interbankState)
        self.sum_B_A_IB(bank, interbank, bankState, interbankState)
        self.together_B_A_all(bank, interbank, bankState, interbankState)
        self.together_B_Z_exIB(bank, interbank, bankState, interbankState)
        self.sum_B_Z_IB(bank, interbank, bankState, interbankState)
        self.together_B_Z_all(bank, interbank, bankState, interbankState)
        self.calc_B_E_all(bank, interbank, bankState, interbankState)
        _ = self.calc_state_on(bank, interbank, bankState, interbankState)  # by_way='all'
        _ = self.calc_state_healthy(bank, interbank, bankState, interbankState)
        _ = self.calc_state_insolvent(bank, interbank, bankState, interbankState)
        _ = self.calc_state_illiquid(bank, interbank, bankState, interbankState)
        _ = self.calc_state_bankrupt(bank, interbank, bankState, interbankState)
        _ = self.calc_state_off(bank, interbank, bankState, interbankState)
        interbank.cre_isv = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.deb_isv = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.isv)
        interbank.cre_ilq = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.deb_ilq = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.ilq)
        interbank.cre_br = self.calc_list_of_creditor_in_state_of_banks(interbank, isState=bank.br)
        interbank.deb_br = self.calc_list_of_debtor_in_state_of_banks(interbank, isState=bank.br)
        pass  # function

    ## NOTE：功能函数集：其他

    def get_update_variable(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        ## 监测财务变量变化。只能产生一个变动的变量 #HACK 似乎没有用
        # global update_variable_name
        bank_last = deepcopy(bank)
        interbank_last = deepcopy(interbank)
        for k, v in bank.__dict__.items():
            if (v != bank_last.__dict__[k]).any():
                self.update_variable_name, self.update_variable_value = k, v
        for k, v in interbank.__dict__.items():
            if (v.dtype != list) and (v != interbank_last.__dict__[k]).any():
                self.update_variable_name, self.update_variable_value = k, v
            else:
                self.update_variable_name, self.update_variable_value = k, v
            pass  # for
        pass  # function

    ## NOTE 总的金融变量更新部分（主入口）

    def update_variables(self, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType, by_way: str = 'all'):
        """
        更新各银行之借贷流量变量。

        - 总体部分：
            - ``all``:  更新全部借贷流量变量、冲击变量、各银行之所有资产负债表变量、各银行之状态变量；

        - 商业银行之资金转移部分：

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

        - 商业银行之冲击部分：

            - ``clear Shock_IB and Shock_exIB``:  清零本回合结束时，除了``Shock_{B}``系列的变量以外的，所有不必要的冲击变量，暨所有``Shock_{IB}``系列的变量、``Shock_{exIB}``系列的变量；
            - ``clear Shock_B_A and Shock_B_Z``:  清零银行内资产负债冲击变量；#HACK无用
            - ``Shock_P_def_t``:  已知``Shock_{P,def}[i]``，更新其余冲击变量；
            - ``Shock_P_run_s``:  已知``Shock_{P,run}[i]``，更新其余冲击变量；
            - ``Shock_D_run_t``:  已知``Shock_{D,run}[i]``，更新其余冲击变量；
            - ``Shock_D_def_s``:  已知``Shock_{D,def}[i]``，更新其余冲击变量；
            - ``Shock_B_A``:  已知``Shock_{B,b}``，更新其余冲击变量；
            - ``Shock_B_Z``:  已知``Shock_{B,Z}``，更新其余冲击变量；
            - ``Shock_IB_def_s``:  已知``Shock_{IB,def}[: ,i_{isv}]``，更新其余冲击变量；
            - ``Shock_IB_run_ilq_s``:  已知``Shock_{IB,run}[: ,i_{ilq}]``，更新其余冲击变量；
            - ``Shock_IB_run_br_s``:  已知``Shock_{IB,run}[: ,i_{br}]``，更新其余冲击变量；
            - ``Shock_IB_def``:  已知``Shock_{IB,def}[j,i_{isv}]``，更新其余冲击变量；
            - ``Shock_IB_run_ilq``:  已知``Shock_{IB,run}[j,i_{ilq}]``，更新其余冲击变量；
            - ``Shock_IB_run_br``:  已知``Shock_{IB,run}[j,i_{br}]``，更新其余冲击变量；
            - ``Shock_IB_def_t``:  已知``Shock_{IB,def}[j,: }],:  \\in i_{isv}``，更新其余冲击变量；
            - ``Shock_IB_run_ilq_t``:  已知``Shock_{IB,run}[j,: }],:  \\in i_{ilq}``，更新其余冲击变量；
            - ``Shock_IB_run_br_t``:  已知``Shock_{IB,run}[j,: }],:  \\in i_{br}``，更新其余冲击变量；
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
            - ``Default_IB_run_s``:  已知``Default_{IB,run}[i_{ilq}]``，更新其余违约变量；
            - ``Default_D_run_s``:  已知``Default_{-IB,run}[i_{ilq}]``，更新其余违约变量；

        - 商业银行之收回部分：

            - ``Recover_IB_run_s``:  已知``Recover_{IB,run}[i_{ilq}]``，更新其余收回变量；
            - ``Recover_P_run_s``:  已知``Recover_{-IB,run}[i_{ilq}]``，更新其余收回变量；

        - 商业银行之偿还部分：

            - ``Repay_IB_run_t``:  已知``Repay_{IB,run}[i_{ilq}]``，更新其余偿还变量；
            - ``Repay_D_run_t``:  已知``Repay_{-IB,run}[i_{ilq}]``，更新其余偿还变量；

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

        Args:content_finance.py
            bank (BankCommercial): 商业银行众
            interbank (BankInterbank): 商业银行间市场
            bankState (StateType): 银行之状态
            interbankState (StateType): 银行间市场之状态
            by_way (str): 参数，通过该参数指定的变量作为已知变量，驱动，以更新其他相关各变量。

        Returns:
            bank (BankCommercial): 商业银行众
            interbank (BankInterbank): 商业银行间市场

        """

        dict_update_methods = {  # 创建一个字典，映射 by_way 的值到对应的方法
            ## NOTE：功能函数集：更新商业银行之资金转移。
            'Lo_P': self.update_by_Lo_P,
            'Li_P': self.update_by_Li_P,
            'Bi_D': self.update_by_Bi_D,
            'Bo_D': self.update_by_Bo_D,
            'Lo_IB_all': self.update_by_Lo_IB_all,
            'Li_IB_all': self.update_by_Li_IB_all,
            'Bi_IB_all': self.update_by_Bi_IB_all,
            'Bo_IB_all': self.update_by_Bo_IB_all,
            'Lo_IB': self.update_by_Lo_IB,
            'Bi_IB': self.update_by_Bi_IB,
            'Bo_IB': self.update_by_Bo_IB,
            'Li_IB': self.update_by_Li_IB,
            'clear transfer all': self.update_by_clear_transfer_all,
            ## NOTE：功能函数集：更新冲击、状态。
            'Shock_P_def_t': self.update_by_Shock_P_def_t,
            'Shock_P_run_s': self.update_by_Shock_P_run_s,
            'Shock_D_run_t': self.update_by_Shock_D_run_t,
            'Shock_D_def_s': self.update_by_Shock_D_def_s,
            'Shock_IB_def_s': self.update_by_Shock_IB_def_s,
            'Shock_IB_run_ilq_s': self.update_by_Shock_IB_run_ilq_s,
            'Shock_IB_run_br_s': self.update_by_Shock_IB_run_br_s,
            'Shock_IB_def': self.update_by_Shock_IB_def,
            'Shock_IB_run_ilq': self.update_by_Shock_IB_run_ilq,
            'Shock_IB_run_br': self.update_by_Shock_IB_run_br,
            'Shock_IB_def_t': self.update_by_Shock_IB_def_t,
            'Shock_IB_run_ilq_t': self.update_by_Shock_IB_run_ilq_t,
            'Shock_IB_run_br_t': self.update_by_Shock_IB_run_br_t,
            'clear Shock_IB and Shock_exIB': self.update_by_clear_Shock_IB_and_Shock_exIB,
            'clear all Shock_target': self.update_by_clear_all_Shock_t,
            'clear all Shock_source': self.update_by_clear_all_Shock_s,
            'clear all Shock_interbank': self.update_by_clear_all_Shock_IB,
            ## NOTE：功能函数集：更新损失。
            'Loss_exIB_def_t': self.update_by_Loss_exIB_def_t,
            'Loss_IB_def_t': self.update_by_Loss_IB_def_t,
            'Loss_exIB_run_t': self.update_by_Loss_exIB_run_t,
            'Loss_IB_run_t': self.update_by_Loss_IB_run_t,
            # 'Loss_IB_def': self.update_by_Loss_IB_def,
            # 'Loss_IB_run': self.update_by_Loss_IB_run,
            ## NOTE：功能函数集：更新违约。
            'Default_IB_def_s': self.update_by_Default_IB_def_s,
            'Default_IB_run_s': self.update_by_Default_IB_run_s,
            'Default_D_def_s': self.update_by_Default_D_def_s,
            'Default_D_run_s': self.update_by_Default_D_run_s,
            ## NOTE：功能函数集：更新收回量。
            'Recover_IB_run_s': self.update_by_Recover_IB_run_s,
            'Recover_P_run_s': self.update_by_Recover_P_run_s,
            ## NOTE：功能函数集：更新偿还量。
            'Repay_IB_run_t': self.update_by_Repay_IB_run_t,
            'Repay_D_run_t': self.update_by_Repay_D_run_t,
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
            ## NOTE：功能函数集：更新银行之状态变量。
            'enabled collect A_P': self.update_by_enabled_collect_A_P,
            'enabled repay Z_D': self.update_by_enabled_repay_Z_D,
            'enabled repay IB': self.update_by_enabled_repay_IB,
            ## NOTE 对于所有的进行更新。
            'all': self.update_by_all,
        }

        # 使用字典来调用对应的方法
        if by_way in dict_update_methods:
            dict_update_methods[by_way](bank, interbank, bankState, interbankState)
        else:
            raise Exception("关键词by_way取词错误".format(by_way))
            pass  # if
        return bank, interbank
        pass  # function

    pass  # class
