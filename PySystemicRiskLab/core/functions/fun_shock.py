"功能函数集：计算冲击。"

from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_environmentVariables import env
from PySystemicRiskLab.core.define.define_type import StateType

pass  # end import


## 更新各银行与各银行间之冲击


class Shock:

    ## 函数区

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

    @classmethod
    def update_B_Shock(cls, bank: BankCommercial, interbank: BankInterbank, bankState, interbankState, by_way: str = 'all'):
        """
        更新各银行之冲击。
        
        参数``by_way``可选值：
        
            ``all``:  更新全部冲击变量；
                    
            ``clear Shock_IB and Shock_exIB``:  清零本回合结束时，除了``Shock_{B}``系列的变量以外的，所有不必要的冲击变量，暨所有``Shock_{IB}``系列的变量、``Shock_{exIB}``系列的变量；
            
            ``clear Shock_B_A and Shock_B_Z``:  清零银行内资产负债冲击变量；#HACK无用
            
            ``Shock_P_def_t``:  已知``Shock_{P,def}[i]``，更新其余冲击变量；
            
            ``Shock_P_run_s``:  已知``Shock_{P,run}[i]``，更新其余冲击变量；
            
            ``Shock_D_run_t``:  已知``Shock_{D,run}[i]``，更新其余冲击变量；
            
            ``Shock_D_def_s``:  已知``Shock_{D,def}[i]``，更新其余冲击变量；
            
            ``Shock_B_A``:  已知``Shock_{B,b}``，更新其余冲击变量；
            
            ``Shock_B_Z``:  已知``Shock_{B,Z}``，更新其余冲击变量；
            
            ``Shock_IB_def_s``:  已知``Shock_{IB,def}[: ,i_{isv}]``，更新其余冲击变量；
            
            ``Shock_IB_run_ilq_s``:  已知``Shock_{IB,run}[: ,i_{ilq}]``，更新其余冲击变量；
            
            ``Shock_IB_run_br_s``:  已知``Shock_{IB,run}[: ,i_{br}]``，更新其余冲击变量；
            
            ``Shock_IB_def``:  已知``Shock_{IB,def}[j,i_{isv}]``，更新其余冲击变量；
            
            ``Shock_IB_run_ilq``:  已知``Shock_{IB,run}[j,i_{ilq}]``，更新其余冲击变量；
            
            ``Shock_IB_run_br``:  已知``Shock_{IB,run}[j,i_{br}]``，更新其余冲击变量；
            
            ``Shock_IB_def_t``:  已知``Shock_{IB,def}[j,: }],:  \\in i_{isv}``，更新其余冲击变量；
            
            ``Shock_IB_run_ilq_t``:  已知``Shock_{IB,run}[j,: }],:  \\in i_{ilq}``，更新其余冲击变量；
            
            ``Shock_IB_run_br_t``:  已知``Shock_{IB,run}[j,: }],:  \\in i_{br}``，更新其余冲击变量；
            

        Args:
            by_way:str:  参数，通过该参数指定的变量作为已知变量，驱动，以更新其他相关各变量。

        """
        if by_way == 'all':
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
        else:
            raise Exception("关键词by_way取词错误".format(by_way))
            pass

        pass

    pass  # class
