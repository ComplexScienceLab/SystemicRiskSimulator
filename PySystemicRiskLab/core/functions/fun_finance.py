from PySystemicRiskLab import np, deepcopy, Union
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_type import StateType, MoneyType, ListType
from PySystemicRiskLab.core.define.define_environmentVariables import env
from PySystemicRiskLab.core.functions.fun_transfer import BankTransfer
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState
from PySystemicRiskLab.core.define.define_consts import LESS1


class Finance:
    """
    财务相关的功能
    """

    ## NOTE：功能函数集：计算商业银行之资金转移。

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

    ## NOTE：功能函数集：计算冲击。

    # "汇总综合外生冲击。" #HACK无用
    # functions together_Shock_exIB(bank:BankCommercial, bankState:StateType)
    #     bank.Shock_exIB_t[bankState] = paras['theta_Shock_exIB_t'] * bank.Shock_P_def_t[bankState] + (1 - paras['theta_Shock_exIB_t']) * bank.Shock_D_run_t[bankState]
    #     pass

    @classmethod
    def together_Shock_target(cls, bank: BankCommercial, bankState: StateType):
        """汇总总冲击目标"""
        bank.Shock_t[bankState] = bank.Shock_exIB_t[bankState] + bank.Shock_IB_t[bankState]
        pass

    @classmethod
    def together_Shock_source(cls, bank: BankCommercial, bankState: StateType):
        """总总冲击源头"""
        bank.Shock_s[bankState] = bank.Shock_exIB_s[bankState] + bank.Shock_IB_s[bankState]
        pass

    @classmethod
    def together_Shock_exIB_target(cls, bank: BankCommercial, bankState: StateType):
        """总银行外冲击目标"""
        bank.Shock_exIB_t[bankState] = bank.Shock_P_def_t[bankState] + bank.Shock_D_run_t[bankState]
        pass

    @classmethod
    def together_Shock_exIB_source(cls, bank: BankCommercial, bankState: StateType):
        """总银行外冲击源头"""
        bank.Shock_exIB_s[bankState] = bank.Shock_P_run_s[bankState] + bank.Shock_D_def_s[bankState]
        pass

    @classmethod
    def together_Shock_def_target(cls, bank: BankCommercial, bankState: StateType):
        """总违约损失冲击目标"""
        bank.Shock_def_t[bankState] = bank.Shock_P_def_t[bankState] + bank.Shock_IB_def_t[bankState]
        pass

    @classmethod
    def together_Shock_def_source(cls, bank: BankCommercial, bankState: StateType):
        """总违约损失冲击源头"""
        bank.Shock_def_s[bankState] = bank.Shock_D_def_s[bankState] + bank.Shock_IB_def_s[bankState]
        pass

    @classmethod
    def together_Shock_run_target(cls, bank: BankCommercial, bankState: StateType):
        """总挤兑流动冲击目标"""
        bank.Shock_run_t[bankState] = bank.Shock_D_run_t[bankState] + bank.Shock_IB_run_t[bankState]
        pass

    @classmethod
    def together_Shock_run_source(cls, bank: BankCommercial, bankState: StateType):
        """总挤兑流动冲击源头"""
        bank.Shock_run_s[bankState] = bank.Shock_P_run_s[bankState] + bank.Shock_IB_run_s[bankState]
        pass

    @classmethod
    def together_Shock_IB_run_target(cls, bank: BankCommercial, bankState: StateType):
        """总银行间流动性冲击目标。"""
        bank.Shock_IB_run_t[bankState] = bank.Shock_IB_run_ilq_t[bankState] + bank.Shock_IB_run_br_t[bankState]
        pass

    @classmethod
    def together_Shock_IB_run_source(cls, bank: BankCommercial, bankState: StateType):
        """总银行间流动性冲击源头。"""
        bank.Shock_IB_run_s[bankState] = bank.Shock_IB_run_ilq_s[bankState] + bank.Shock_IB_run_br_s[bankState]
        pass

    @classmethod
    def together_Shock_B(cls, bank: BankCommercial, bankState: StateType):  # BUG这个做什么的？似乎没有被用到。
        """总银行内资产负债冲击。"""
        bank.Shock_B[bankState] = bank.Shock_B_A[bankState] + bank.Shock_B_Z[bankState]
        pass

    @classmethod
    def together_Shock_IB_source(cls, bank: BankCommercial, bankState: StateType):
        """总银行间冲击源头。"""
        bank.Shock_IB_s[bankState] = bank.Shock_IB_def_s[bankState] + bank.Shock_IB_run_s[bankState]
        pass

    @classmethod
    def together_Shock_IB_run(cls, interbank: BankInterbank, interbankState: StateType):
        """总银行间流动性冲击。"""
        interbank.Shock_IB_run[interbankState] = interbank.Shock_IB_run_ilq[interbankState] + interbank.Shock_IB_run_br[interbankState]
        pass

    @classmethod
    def together_Shock_IB(cls, interbank: BankInterbank, interbankState: StateType):
        """总银行间冲击。"""
        interbank.Shock_IB[interbankState] = interbank.Shock_IB_def[interbankState] + interbank.Shock_IB_run[interbankState]
        pass

    @classmethod
    def sum_Shock_IB_def_target(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总资不抵债银行之银行间违约损失冲击目标。"""
        bank.Shock_IB_def_t[bankState] = np.sum(interbank.Shock_IB_def * interbankState, axis=1).reshape(-1, 1)[bankState]
        pass

    @classmethod
    def sum_Shock_IB_run_ilq_target(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总流动性短缺银行之银行间流动性冲击目标。"""
        bank.Shock_IB_run_ilq_t[bankState] = np.sum(interbank.Shock_IB_run_ilq * interbankState, axis=1).reshape(-1, 1)[bankState]
        pass

    @classmethod
    def sum_Shock_IB_run_br_target(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):
        """总破产银行之银行间流动性冲击目标。"""
        bank.Shock_IB_run_br_t[bankState] = np.sum(interbank.Shock_IB_run_br * interbankState, axis=1).reshape(-1, 1)[bankState]
        pass

    @classmethod
    def together_Shock_IB_target(cls, bank: BankCommercial, bankState: StateType):
        """总银行间冲击目标。"""
        bank.Shock_IB_t[bankState] = bank.Shock_IB_def_t[bankState] + bank.Shock_IB_run_t[bankState]
        pass

    # @classmethod #TODO无用
    # def conduct_Shock_L_exIB(cls, bank: BankCommercial, bankState: StateType):
    #
    #     bank.Shock_B_A[bankState] = bank.Shock_P_def_t[bankState]
    #     pass

    @classmethod
    def conduct_Shock_D(cls, bank: BankCommercial, bankState: StateType):
        """传导存款损失外生冲击。"""  # HACK暂不使用。
        bank.Shock_B_Z[bankState] = bank.Shock_D_run_t[bankState]
        pass

    @classmethod
    def conduct_Shock_IB_def_t(cls, bank: BankCommercial, bankState: StateType):
        """传导银行间违约损失冲击。"""  # HACK暂不使用。
        bank.Shock_B_A[bankState] = bank.Shock_IB_def_t[bankState]
        pass

    @classmethod
    def conduct_Shock_IB_run_t(cls, bank: BankCommercial, bankState: StateType):
        """传导银行间挤兑流动冲击。"""  # HACK暂不使用。
        bank.Shock_B_A[bankState] = bank.Shock_IB_run_t[bankState]
        pass

    @classmethod
    def clear_Shock_IB_and_exIB(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType):  # BUG是否乱清零？
        """清零本回合结束时所有不必要的冲击变量"""
        bank.Shock_P_def_t = np.zeros(env['num_bank'])
        bank.Shock_D_run_t = np.zeros(env['num_bank'])
        bank.Shock_P_run_s = np.zeros(env['num_bank'])
        bank.Shock_D_def_s = np.zeros(env['num_bank'])
        bank.Shock_IB_def_s = np.zeros(env['num_bank'])
        bank.Shock_IB_run_ilq_s = np.zeros(env['num_bank'])
        bank.Shock_IB_run_br_s = np.zeros(env['num_bank'])
        interbank.Shock_IB_def = np.zeros(env['num_bank'], env['num_bank'])
        interbank.Shock_IB_run_ilq = np.zeros(env['num_bank'], env['num_bank'])
        interbank.Shock_IB_run_br = np.zeros(env['num_bank'], env['num_bank'])
        bank.Shock_IB_def_t = np.zeros(env['num_bank'])
        bank.Shock_IB_run_ilq_t = np.zeros(env['num_bank'])
        bank.Shock_IB_run_br_t = np.zeros(env['num_bank'])
        pass

    # @classmethod
    # def clear_Shock_inB(cls, bank: BankCommercial):
    #     """清零本回合中期所有不必要的冲击变量"""  # HACK无用
    #
    #     bank.Shock_B_A = np.zeros(env['num_bank'])
    #     bank.Shock_B_Z = np.zeros(env['num_bank'])
    #     pass

    ## NOTE：功能函数集：计算商业银行之资产负债表结构。

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
    #         together_B_Z_exIB(bank,bankState)
    #         together_B_Z_IB(bank, interbank,bankState,interbankState)
    #     elif by_way == 'Z_exIB' | by_way == 'Z_D':
    #         together_B_Z_exIB(bank,bankState)
    #     elif by_way == 'Z_IB':
    #         together_B_Z_IB(bank, interbank,bankState,interbankState)
    #     else:
    #         throw(DomainError(by_way, "关键词取值错误！"))
    #         pass
    #     together_B_Z_all(bank,bankState)
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
        bank.E_all[bankList] = bank.A_all[bankList] - bank.Z_all[bankList] - LESS1[bankList]  # 允许E_all为负数
        # bank.E_all[bankState] = np.maximum(bank.A_all[bankState] - bank.Z_all[bankState] - LESS1[bankState], 0.0)
        pass

    # @classmethod
    # def calc_B_E_all_at_all_bank(cls, bank: BankCommercial, bankState: StateType):  # HACK没有用到过
    #     """计算银行体系内包括已退出银行在内的所有各银行之所有者权益``E_{B}``，通过总资产与总负债差值。"""
    #     bank.E_all[:] = bank.A_all - bank.Z_all - LESS1
    #     # bank.E_all[:] = np.maximum(bank.A_all - bank.Z_all - LESS1, 0.0)
    #     pass

    # @classmethod
    # def calc_B_A_all(cls, bank: BankCommercial, bankState: StateType):  # HACK没有用到过
    #     """计算各银行之总资产``A_{B}``，通过所有者权益和总负债。"""
    #     bank.A_all[bankState] = bank.E_all[bankState] + bank.Z_all[bankState]
    #     pass

    # @classmethod
    # def calc_B_Z_all(cls, bank: BankCommercial, bankState: StateType):  # HACK没有用到过
    #     """计算各银行之总负债``Z_{B}``，通过所有者权益和总资产。"""
    #     bank.Z_all[bankState] = bank.A_all[bankState] - bank.E_all[bankState]
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
    
    
    ## NOTE 其他功能部分

    update_variable_name: str = None
    update_variable_value = None

    @classmethod
    def get_update_variable(cls, bank: BankCommercial, interbank: BankInterbank):
        ## 监测财务变量变化。只能产生一个变动的变量
        # global update_variable_name
        bank_last = deepcopy(bank)
        interbank_last = deepcopy(interbank)
        for k, v in bank.__dict__.items():
            if (v != bank_last.__dict__[k]).any():
                cls.update_variable_name, cls.update_variable_value = k, v
        for k, v in interbank.__dict__.items():
            if (v.dtype != list) and (v != interbank_last.__dict__[k]).any():
                cls.update_variable_name, cls.update_variable_value = k, v
            else:
                cls.update_variable_name, cls.update_variable_value = k, v
            pass  # for
        pass  # def

    @classmethod
    def update_states(cls, bank: BankCommercial, interbank: BankInterbank, by_way: str = 'all'):  # NOW
        """
        更新各状态。

        Args:
            bank (): 
            interbank (): 
            by_way (): 

        Returns:

        """


    # @classmethod
    # def update_finance_calculation(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType, update_type='auto', by_way: str = 'all', way: str = 'any'):
    #     """
    #     更新财务计算。
    # 
    #     遍历哪个变量数据发生了变化，然后以那个变量为起点按照关联式子，链式更新，直到关联末端的变量更新完为止。
    # 
    #     关键字如下：TODO
    # 
    #     Returns:
    # 
    #     """
    # 
    #     ## 按照`update_type`类型更新财务变量
    #     if update_type == 'auto':  # 按照变动变量自动更新财务变量
    #         cls.get_update_variable(bank, interbank)
    #         BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way=cls.update_variable_name)  # 更新交易
    #         Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way=cls.update_variable_name)  # 更新冲击
    #         BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way=cls.update_variable_name)  # 更新资产负债表
    #         BankState.update_states(way='any')  # 更新状态
    #     if update_type == 'all':
    #         BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')  # 更新交易
    #         Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')  # 更新冲击
    #         BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')  # 更新资产负债表
    #         BankState.update_states(way='any')  # 更新状态
    #     elif update_type == 'transfer':
    #         BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way=by_way)  # 更新交易
    #         Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')  # 更新冲击
    #         BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')  # 更新资产负债表
    #         BankState.update_states(way='any')  # 更新状态
    #     elif update_type == 'shock':
    #         Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way=by_way)  # 更新冲击
    #         BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')  # 更新交易
    #         BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')  # 更新资产负债表
    #         BankState.update_states(way='any')  # 更新状态
    #     elif update_type == 'balance sheet':
    #         BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way=by_way)  # 更新资产负债表
    #         BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')  # 更新交易
    #         Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')  # 更新冲击
    #         BankState.update_states(way='any')  # 更新状态
    #     elif update_type == 'state':
    #         BankState.update_states(way=way)  # 更新状态
    #         BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')  # 更新交易
    #         Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')  # 更新冲击
    #         BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')  # 更新资产负债表
    #     else:
    #         raise Exception("关键词update_type取词错误".format(update_type))
    #         pass
    #     pass  # method

    @classmethod
    def update_variables(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType, by_way: str = 'all'):  # NOW
        """
        更新各银行之借贷流量变量。

        - 总体部分：
            - ``all``:  更新全部借贷流量变量、冲击变量、各银行之所有资产负债表变量；

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

        - 商业银行之资产负债表部分：

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
            bankState (): 银行之状态
            interbankState (): 银行间市场之状态
            by_way (): 参数，通过该参数指定的变量作为已知变量，驱动，以更新其他相关各变量。

        Returns:

        """


        ## NOTE：功能函数集：更新商业银行之资金转移。
        if by_way == 'Lo_P':
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


        ## NOTE：功能函数集：更新冲击。
        elif by_way == 'Shock_P_def_t':
            cls.together_Shock_exIB_target(bank, bankState)
            cls.together_Shock_target(bank, bankState)
            cls.together_Shock_def_target(bank, bankState)
        elif by_way == 'Shock_P_run_s':
            cls.together_Shock_exIB_source(bank, bankState)
            cls.together_Shock_source(bank, bankState)
            cls.together_Shock_run_source(bank, bankState)
        elif by_way == 'Shock_D_run_t':
            cls.together_Shock_exIB_target(bank, bankState)
            cls.together_Shock_target(bank, bankState)
            cls.together_Shock_run_target(bank, bankState)
        elif by_way == 'Shock_D_def_s':
            cls.together_Shock_exIB_source(bank, bankState)
            cls.together_Shock_source(bank, bankState)
            cls.together_Shock_def_source(bank, bankState)
        # elif by_way == 'Shock_B_A' or by_way == 'Shock_B_Z': #HACK无用
        #     cls.together_Shock_B(bank, bankState)
        elif by_way == 'Shock_IB_def_s':
            cls.together_Shock_IB_source(bank, bankState)
            cls.together_Shock_source(bank, bankState)
            cls.together_Shock_def_source(bank, bankState)
        elif by_way == 'Shock_IB_run_ilq_s' or by_way == 'Shock_IB_run_br_s':
            cls.together_Shock_IB_run_source(bank, bankState)
            cls.together_Shock_IB_source(bank, bankState)
            cls.together_Shock_source(bank, bankState)
            cls.together_Shock_run_source(bank, bankState)
        elif by_way == 'Shock_IB_def':
            cls.together_Shock_IB(interbank, interbankState)
            cls.sum_Shock_IB_def_target(bank, interbank, bankState, interbankState)
            cls.together_Shock_IB_target(bank, bankState)
            cls.together_Shock_target(bank, bankState)
            cls.together_Shock_def_target(bank, bankState)
        elif by_way == 'Shock_IB_run_ilq':
            cls.together_Shock_IB_run(interbank, interbankState)
            cls.together_Shock_IB(interbank, interbankState)
            cls.sum_Shock_IB_run_ilq_target(bank, interbank, bankState, interbankState)
            cls.together_Shock_IB_run_target(bank, bankState)
            cls.together_Shock_IB_target(bank, bankState)
            cls.together_Shock_target(bank, bankState)
            cls.together_Shock_run_target(bank, bankState)
        elif by_way == 'Shock_IB_run_br':
            cls.together_Shock_IB_run(interbank, interbankState)
            cls.together_Shock_IB(interbank, interbankState)
            cls.sum_Shock_IB_run_br_target(bank, interbank, bankState, interbankState)
            cls.together_Shock_IB_run_target(bank, bankState)
            cls.together_Shock_IB_target(bank, bankState)
            cls.together_Shock_target(bank, bankState)
            cls.together_Shock_run_target(bank, bankState)
        elif by_way == 'Shock_IB_def_t':
            cls.together_Shock_IB_target(bank, bankState)
            cls.together_Shock_target(bank, bankState)
            cls.together_Shock_def_target(bank, bankState)
        elif by_way == 'Shock_IB_run_ilq_t' or by_way == 'Shock_IB_run_br_t':
            cls.together_Shock_IB_run_target(bank, bankState)
            cls.together_Shock_IB_target(bank, bankState)
            cls.together_Shock_target(bank, bankState)
            cls.together_Shock_run_target(bank, bankState)
        elif by_way == 'clear Shock_IB and Shock_exIB':
            cls.clear_Shock_IB_and_exIB(bank, interbank, bankState, interbankState)
            cls.together_Shock_IB_run_source(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_IB_source(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_exIB_source(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_source(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_def_source(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_run_source(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_IB_run(interbank, StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
            cls.together_Shock_IB(interbank, StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
            cls.sum_Shock_IB_def_target(bank, interbank, StateType((bank.on) | (bank.off)), StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
            cls.sum_Shock_IB_run_ilq_target(bank, interbank, StateType((bank.on) | (bank.off)), StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
            cls.sum_Shock_IB_run_br_target(bank, interbank, StateType((bank.on) | (bank.off)), StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
            cls.together_Shock_IB_run_target(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_IB_target(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_exIB_target(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_target(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_def_target(bank, StateType((bank.on) | (bank.off)))
            cls.together_Shock_run_target(bank, StateType((bank.on) | (bank.off)))
        # elif by_way == 'clear Shock_B_A and Shock_B_Z': #HACK无用
        #     cls.clear_Shock_inB(bank)
        #     cls.together_Shock_B(bank, StateType((bank.on) | (bank.off)))

        ## NOTE：功能函数集：更新商业银行之资产负债表结构。
        elif by_way == 'A_exIB' or by_way == 'A_P' or by_way == 'A_R' or by_way == 'A_other':
            cls.together_B_A_exIB(bank, bankState)
            cls.together_B_A_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)
            BankState.calc_state_insolvent()
        elif by_way == 'A_Q':
            cls.together_B_A_exIB(bank, bankState)
            cls.together_B_A_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)
            BankState.calc_state_illiquid()
        elif by_way == 'A_IB_all':
            cls.together_B_A_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)
        elif by_way == 'Z_exIB' or by_way == 'Z_D' or by_way == 'Z_other':
            cls.together_B_Z_exIB(bank, bankState)
            cls.together_B_Z_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)
        elif by_way == 'Z_IB_all':
            cls.together_B_Z_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)
        # elif by_way == 'E_all and Z_all': #HACK似乎没有用到过
        #     cls.calc_B_A_all(bank, bankState)
        # elif by_way == 'E_all and A_all':#HACK似乎没有用到过
        #     cls.calc_B_Z_all(bank, bankState)
        # elif by_way == 'calc all E_all': #HACK似乎没有用到过
        #     cls.calc_B_E_all_at_all_bank(bank, bankState)
        elif by_way == 'A_IB':
            cls.alter_A_IB(interbank)
            cls.sum_B_A_IB(bank, interbank, bankState, interbankState)
            cls.together_B_A_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)
        elif by_way == 'Z_IB':
            cls.alter_Z_IB(interbank)
            cls.sum_B_A_IB(bank, interbank, bankState, interbankState)
            cls.together_B_A_all(bank, bankState)
            cls.sum_B_Z_IB(bank, interbank, bankState, interbankState)
            cls.together_B_Z_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)  # BUG 检查是否正确。
        elif by_way == 'sum A_IB':
            cls.sum_B_A_IB(bank, interbank, bankState, interbankState)
            cls.together_B_A_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)
        elif by_way == 'sum Z_IB':
            cls.sum_B_Z_IB(bank, interbank, bankState, interbankState)
            cls.together_B_Z_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)
        elif by_way == 'alter to Z_IB from A_IB':  # HACK似乎冗余。
            # sum_B_A_IB(bank, interbank,bankState,interbankState) #HACK 冗余。不能调用，只能在外部手动计算。
            # together_B_A_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
            cls.alter_A_IB(interbank)
            # sum_B_Z_IB(bank, interbank,bankState,interbankState) #HACK 冗余。不能调用，只能在外部手动计算。
            # together_B_Z_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
            # calc_B_E_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
        elif by_way == 'alter to A_IB from Z_IB':  # HACK似乎冗余。
            # sum_B_Z_IB(bank, interbank,bankState,interbankState) #HACK 冗余。不能调用，只能在外部手动计算。
            # together_B_Z_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
            cls.alter_Z_IB(interbank)
            # sum_B_A_IB(bank, interbank,bankState,interbankState) #HACK 冗余。不能调用，只能在外部手动计算。
            # together_B_A_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
            # calc_B_E_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。

        ## NOTE 对于所有的进行更新。
        elif by_way == 'all':
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

            # cls.together_Shock_B(bank, bankState) #HACK无用
            cls.together_Shock_IB_run_source(bank, bankState)
            cls.together_Shock_IB_source(bank, bankState)
            cls.together_Shock_exIB_source(bank, bankState)
            cls.together_Shock_source(bank, bankState)
            cls.together_Shock_def_source(bank, bankState)
            cls.together_Shock_run_source(bank, bankState)
            cls.together_Shock_IB_run(interbank, interbankState)
            cls.together_Shock_IB(interbank, interbankState)
            cls.sum_Shock_IB_def_target(bank, interbank, bankState, interbankState)
            cls.sum_Shock_IB_run_ilq_target(bank, interbank, bankState, interbankState)
            cls.sum_Shock_IB_run_br_target(bank, interbank, bankState, interbankState)
            cls.together_Shock_IB_run_target(bank, bankState)
            cls.together_Shock_IB_target(bank, bankState)
            cls.together_Shock_exIB_target(bank, bankState)
            cls.together_Shock_target(bank, bankState)
            cls.together_Shock_def_target(bank, bankState)
            cls.together_Shock_run_target(bank, bankState)

            cls.together_B_A_exIB(bank, bankState)
            cls.sum_B_A_IB(bank, interbank, bankState, interbankState)
            cls.together_B_A_all(bank, bankState)
            cls.together_B_Z_exIB(bank, bankState)
            cls.sum_B_Z_IB(bank, interbank, bankState, interbankState)
            cls.together_B_Z_all(bank, bankState)
            cls.calc_B_E_all(bank, bankState)

    # if by_way == 'all':
        #     BankTransfer.alter_transfer_Lo_IB(interbank, interbankState)
        #     BankTransfer.sum_transfer_Bi_IB(bank, interbank, bankState, interbankState)
        #     BankTransfer.alter_transfer_Bo_IB(interbank, interbankState)
        #     BankTransfer.sum_transfer_Li_IB(bank, interbank, bankState, interbankState)
        #     BankTransfer.together_transfer_B_Lo_exIB(bank, bankState)
        #     BankTransfer.together_transfer_B_Lo_all(bank, bankState)
        #     BankTransfer.together_transfer_B_Li_exIB(bank, bankState)
        #     BankTransfer.together_transfer_B_Li_all(bank, bankState)
        #     BankTransfer.together_transfer_B_Bi_exIB(bank, bankState)
        #     BankTransfer.together_transfer_B_Bi_all(bank, bankState)
        #     BankTransfer.together_transfer_B_Bo_exIB(bank, bankState)
        #     BankTransfer.together_transfer_B_Bo_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        #
        #     # Shock.together_Shock_B(bank, bankState) #HACK无用
        #     Shock.together_Shock_IB_run_source(bank, bankState)
        #     Shock.together_Shock_IB_source(bank, bankState)
        #     Shock.together_Shock_exIB_source(bank, bankState)
        #     Shock.together_Shock_source(bank, bankState)
        #     Shock.together_Shock_def_source(bank, bankState)
        #     Shock.together_Shock_run_source(bank, bankState)
        #     Shock.together_Shock_IB_run(interbank, interbankState)
        #     Shock.together_Shock_IB(interbank, interbankState)
        #     Shock.sum_Shock_IB_def_target(bank, interbank, bankState, interbankState)
        #     Shock.sum_Shock_IB_run_ilq_target(bank, interbank, bankState, interbankState)
        #     Shock.sum_Shock_IB_run_br_target(bank, interbank, bankState, interbankState)
        #     Shock.together_Shock_IB_run_target(bank, bankState)
        #     Shock.together_Shock_IB_target(bank, bankState)
        #     Shock.together_Shock_exIB_target(bank, bankState)
        #     Shock.together_Shock_target(bank, bankState)
        #     Shock.together_Shock_def_target(bank, bankState)
        #     Shock.together_Shock_run_target(bank, bankState)
        #
        #     BalanceSheet.together_B_A_exIB(bank, bankState)
        #     BalanceSheet.sum_B_A_IB(bank, interbank, bankState, interbankState)
        #     BalanceSheet.together_B_A_all(bank, bankState)
        #     BalanceSheet.together_B_Z_exIB(bank, bankState)
        #     BalanceSheet.sum_B_Z_IB(bank, interbank, bankState, interbankState)
        #     BalanceSheet.together_B_Z_all(bank, bankState)
        #     BalanceSheet.calc_B_E_all(bank, bankState)
        #
        # ## NOTE：功能函数集：更新商业银行之资金转移。
        # elif by_way == 'clear transfer all':
        #     BankTransfer.clear_all_transfer(bank, interbank, bankState, interbankState)
        #     BankTransfer.alter_transfer_Lo_IB(interbank, ((bank.on | bank.off) & (bank.on | bank.off).T))
        #     BankTransfer.sum_transfer_Bi_IB(bank, interbank, (bank.on | bank.off), ((bank.on | bank.off) & (bank.on | bank.off).T))
        #     BankTransfer.alter_transfer_Bo_IB(interbank, ((bank.on | bank.off) & (bank.on | bank.off).T))
        #     BankTransfer.sum_transfer_Li_IB(bank, interbank, (bank.on | bank.off), ((bank.on | bank.off) & (bank.on | bank.off).T))
        #     BankTransfer.together_transfer_B_Lo_exIB(bank, (bank.on | bank.off))
        #     BankTransfer.together_transfer_B_Lo_all(bank, (bank.on | bank.off))
        #     BankTransfer.together_transfer_B_Li_exIB(bank, (bank.on | bank.off))
        #     BankTransfer.together_transfer_B_Li_all(bank, (bank.on | bank.off))
        #     BankTransfer.together_transfer_B_Bi_exIB(bank, (bank.on | bank.off))
        #     BankTransfer.together_transfer_B_Bi_all(bank, (bank.on | bank.off))
        #     BankTransfer.together_transfer_B_Bo_exIB(bank, (bank.on | bank.off))
        #     BankTransfer.together_transfer_B_Bo_all(bank, (bank.on | bank.off))
        #     BankTransfer.together_transfer_all(bank, (bank.on | bank.off))
        # elif by_way == 'Lo_P':
        #     BankTransfer.together_transfer_B_Lo_exIB(bank, bankState)
        #     BankTransfer.together_transfer_B_Lo_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Li_P':
        #     BankTransfer.together_transfer_B_Li_exIB(bank, bankState)
        #     BankTransfer.together_transfer_B_Li_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Bi_D':
        #     BankTransfer.together_transfer_B_Bi_exIB(bank, bankState)
        #     BankTransfer.together_transfer_B_Bi_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Bo_D':
        #     BankTransfer.together_transfer_B_Bo_exIB(bank, bankState)
        #     BankTransfer.together_transfer_B_Bo_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Lo_IB_all':
        #     BankTransfer.together_transfer_B_Lo_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Li_IB_all':
        #     BankTransfer.together_transfer_B_Li_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Bi_IB_all':
        #     BankTransfer.together_transfer_B_Bi_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Bo_IB_all':
        #     BankTransfer.together_transfer_B_Bo_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Lo_IB':
        #     BankTransfer.alter_transfer_Lo_IB(interbank, interbankState)
        #     BankTransfer.sum_transfer_Bi_IB(bank, interbank, bankState, interbankState)
        #     BankTransfer.together_transfer_B_Bi_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Bi_IB':
        #     BankTransfer.alter_transfer_Bi_IB(interbank, interbankState)
        #     BankTransfer.sum_transfer_Bi_IB(bank, interbank, bankState, interbankState)
        #     BankTransfer.together_transfer_B_Bi_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Bo_IB':
        #     BankTransfer.alter_transfer_Bo_IB(interbank, interbankState)
        #     BankTransfer.sum_transfer_Li_IB(bank, interbank, bankState, interbankState)
        #     BankTransfer.together_transfer_B_Li_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        # elif by_way == 'Li_IB':
        #     BankTransfer.alter_transfer_Li_IB(interbank, interbankState)
        #     BankTransfer.sum_transfer_Li_IB(bank, interbank, bankState, interbankState)
        #     BankTransfer.together_transfer_B_Li_all(bank, bankState)
        #     BankTransfer.together_transfer_all(bank, bankState)
        #
        # ## NOTE：功能函数集：更新冲击。
        # elif by_way == 'clear Shock_IB and Shock_exIB':
        #     Shock.clear_Shock_IB_and_exIB(bank, interbank, bankState, interbankState)
        #     Shock.together_Shock_IB_run_source(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_IB_source(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_exIB_source(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_source(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_def_source(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_run_source(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_IB_run(interbank, StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
        #     Shock.together_Shock_IB(interbank, StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
        #     Shock.sum_Shock_IB_def_target(bank, interbank, StateType((bank.on) | (bank.off)), StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
        #     Shock.sum_Shock_IB_run_ilq_target(bank, interbank, StateType((bank.on) | (bank.off)), StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
        #     Shock.sum_Shock_IB_run_br_target(bank, interbank, StateType((bank.on) | (bank.off)), StateType(((bank.on) | (bank.off)) & (bank.on | bank.off).T))
        #     Shock.together_Shock_IB_run_target(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_IB_target(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_exIB_target(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_target(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_def_target(bank, StateType((bank.on) | (bank.off)))
        #     Shock.together_Shock_run_target(bank, StateType((bank.on) | (bank.off)))
        # # elif by_way == 'clear Shock_B_A and Shock_B_Z': #HACK无用
        # #     Shock.clear_Shock_inB(bank)
        # #     Shock.together_Shock_B(bank, StateType((bank.on) | (bank.off)))
        # elif by_way == 'Shock_P_def_t':
        #     Shock.together_Shock_exIB_target(bank, bankState)
        #     Shock.together_Shock_target(bank, bankState)
        #     Shock.together_Shock_def_target(bank, bankState)
        # elif by_way == 'Shock_P_run_s':
        #     Shock.together_Shock_exIB_source(bank, bankState)
        #     Shock.together_Shock_source(bank, bankState)
        #     Shock.together_Shock_run_source(bank, bankState)
        # elif by_way == 'Shock_D_run_t':
        #     Shock.together_Shock_exIB_target(bank, bankState)
        #     Shock.together_Shock_target(bank, bankState)
        #     Shock.together_Shock_run_target(bank, bankState)
        # elif by_way == 'Shock_D_def_s':
        #     Shock.together_Shock_exIB_source(bank, bankState)
        #     Shock.together_Shock_source(bank, bankState)
        #     Shock.together_Shock_def_source(bank, bankState)
        # # elif by_way == 'Shock_B_A' or by_way == 'Shock_B_Z': #HACK无用
        # #     Shock.together_Shock_B(bank, bankState)
        # elif by_way == 'Shock_IB_def_s':
        #     Shock.together_Shock_IB_source(bank, bankState)
        #     Shock.together_Shock_source(bank, bankState)
        #     Shock.together_Shock_def_source(bank, bankState)
        # elif by_way == 'Shock_IB_run_ilq_s' or by_way == 'Shock_IB_run_br_s':
        #     Shock.together_Shock_IB_run_source(bank, bankState)
        #     Shock.together_Shock_IB_source(bank, bankState)
        #     Shock.together_Shock_source(bank, bankState)
        #     Shock.together_Shock_run_source(bank, bankState)
        # elif by_way == 'Shock_IB_def':
        #     Shock.together_Shock_IB(interbank, interbankState)
        #     Shock.sum_Shock_IB_def_target(bank, interbank, bankState, interbankState)
        #     Shock.together_Shock_IB_target(bank, bankState)
        #     Shock.together_Shock_target(bank, bankState)
        #     Shock.together_Shock_def_target(bank, bankState)
        # elif by_way == 'Shock_IB_run_ilq':
        #     Shock.together_Shock_IB_run(interbank, interbankState)
        #     Shock.together_Shock_IB(interbank, interbankState)
        #     Shock.sum_Shock_IB_run_ilq_target(bank, interbank, bankState, interbankState)
        #     Shock.together_Shock_IB_run_target(bank, bankState)
        #     Shock.together_Shock_IB_target(bank, bankState)
        #     Shock.together_Shock_target(bank, bankState)
        #     Shock.together_Shock_run_target(bank, bankState)
        # elif by_way == 'Shock_IB_run_br':
        #     Shock.together_Shock_IB_run(interbank, interbankState)
        #     Shock.together_Shock_IB(interbank, interbankState)
        #     Shock.sum_Shock_IB_run_br_target(bank, interbank, bankState, interbankState)
        #     Shock.together_Shock_IB_run_target(bank, bankState)
        #     Shock.together_Shock_IB_target(bank, bankState)
        #     Shock.together_Shock_target(bank, bankState)
        #     Shock.together_Shock_run_target(bank, bankState)
        # elif by_way == 'Shock_IB_def_t':
        #     Shock.together_Shock_IB_target(bank, bankState)
        #     Shock.together_Shock_target(bank, bankState)
        #     Shock.together_Shock_def_target(bank, bankState)
        # elif by_way == 'Shock_IB_run_ilq_t' or by_way == 'Shock_IB_run_br_t':
        #     Shock.together_Shock_IB_run_target(bank, bankState)
        #     Shock.together_Shock_IB_target(bank, bankState)
        #     Shock.together_Shock_target(bank, bankState)
        #     Shock.together_Shock_run_target(bank, bankState)
        #
        # ## NOTE：功能函数集：更新商业银行之资产负债表结构。
        # elif by_way == 'A_exIB' or by_way == 'A_P' or by_way == 'A_Q' or by_way == 'A_R' or by_way == 'A_other':
        #     BalanceSheet.together_B_A_exIB(bank, bankState)
        #     BalanceSheet.together_B_A_all(bank, bankState)
        #     BalanceSheet.calc_B_E_all(bank, bankState)
        #     BankState.calc_state_insolvent()
        # elif by_way == 'A_IB_all':
        #     BalanceSheet.together_B_A_all(bank, bankState)
        #     BalanceSheet.calc_B_E_all(bank, bankState)
        # elif by_way == 'Z_exIB' or by_way == 'Z_D' or by_way == 'Z_other':
        #     BalanceSheet.together_B_Z_exIB(bank, bankState)
        #     BalanceSheet.together_B_Z_all(bank, bankState)
        #     BalanceSheet.calc_B_E_all(bank, bankState)
        # elif by_way == 'Z_IB_all':
        #     BalanceSheet.together_B_Z_all(bank, bankState)
        #     BalanceSheet.calc_B_E_all(bank, bankState)
        # # elif by_way == 'E_all and Z_all': #HACK似乎没有用到过
        # #     BalanceSheet.calc_B_A_all(bank, bankState)
        # # elif by_way == 'E_all and A_all':#HACK似乎没有用到过
        # #     BalanceSheet.calc_B_Z_all(bank, bankState)
        # # elif by_way == 'calc all E_all': #HACK似乎没有用到过
        # #     BalanceSheet.calc_B_E_all_at_all_bank(bank, bankState)
        # elif by_way == 'A_IB':
        #     BalanceSheet.alter_A_IB(interbank)
        #     BalanceSheet.sum_B_A_IB(bank, interbank, bankState, interbankState)
        #     BalanceSheet.together_B_A_all(bank, bankState)
        #     BalanceSheet.calc_B_E_all(bank, bankState)
        # elif by_way == 'Z_IB':
        #     BalanceSheet.alter_Z_IB(interbank)
        #     BalanceSheet.sum_B_Z_IB(bank, interbank, bankState, interbankState)
        #     BalanceSheet.together_B_Z_all(bank, bankState)
        #     BalanceSheet.calc_B_E_all(bank, bankState)
        # elif by_way == 'sum A_IB':
        #     BalanceSheet.sum_B_A_IB(bank, interbank, bankState, interbankState)
        #     BalanceSheet.together_B_A_all(bank, bankState)
        #     BalanceSheet.calc_B_E_all(bank, bankState)
        # elif by_way == 'sum Z_IB':
        #     BalanceSheet.sum_B_Z_IB(bank, interbank, bankState, interbankState)
        #     BalanceSheet.together_B_Z_all(bank, bankState)
        #     BalanceSheet.calc_B_E_all(bank, bankState)
        # elif by_way == 'alter to Z_IB from A_IB':  # HACK似乎冗余。
        #     # sum_B_A_IB(bank, interbank,bankState,interbankState) #HACK 冗余。不能调用，只能在外部手动计算。
        #     # together_B_A_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
        #     BalanceSheet.alter_A_IB(interbank)
        #     # sum_B_Z_IB(bank, interbank,bankState,interbankState) #HACK 冗余。不能调用，只能在外部手动计算。
        #     # together_B_Z_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
        #     # calc_B_E_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
        # elif by_way == 'alter to A_IB from Z_IB':  # HACK似乎冗余。
        #     # sum_B_Z_IB(bank, interbank,bankState,interbankState) #HACK 冗余。不能调用，只能在外部手动计算。
        #     # together_B_Z_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
        #     BalanceSheet.alter_Z_IB(interbank)
        #     # sum_B_A_IB(bank, interbank,bankState,interbankState) #HACK 冗余。不能调用，只能在外部手动计算。
        #     # together_B_A_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。
        #     # calc_B_E_all(bank,bankState) #HACK 冗余。不能调用，只能在外部手动计算。

        else:
            raise Exception("关键词by_way取词错误".format(by_way))
            pass  # if

        pass  # method

        pass  # class
