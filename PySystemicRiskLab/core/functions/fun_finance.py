from PySystemicRiskLab import deepcopy, Union
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_type import StateType, MoneyType, ListType
from PySystemicRiskLab.core.functions.fun_transfer import BankTransfer
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState


class Finance:
    """
    财务相关的功能NOW
    """

    @classmethod
    def update_finance_calculation(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType, update_type='auto', by_way: str = 'all', target: str = 'any', source: str = 'any'):
        """
        更新财务计算。

        遍历哪个变量数据发生了变化，然后以那个变量为起点按照关联式子，链式更新，直到关联末端的变量更新完为止。

        Returns:

        """

        ## 监测财务变量变化。只能产生一个变动的变量
        # global update_variable_name
        update_variable_name: str
        update_variable_value: Union[MoneyType, StateType, ListType]
        bank_last = deepcopy(bank)
        interbank_last = deepcopy(interbank)
        for k, v in bank.__dict__.items():
            if v.any() != bank_last[k].any():
                update_variable_name, update_variable_value = k, v
        for k, v in interbank.__dict__.items():
            if v.any() != interbank_last[k].any():
                update_variable_name, update_variable_value = k, v
            pass  # for

        ## 按照`update_type`类型更新财务变量
        if update_type == 'auto':  # 按照变动变量自动更新财务变量
            ## 更新交易
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way=update_variable_name)
            ## 更新冲击
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way=update_variable_name)
            ## 更新资产负债表
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way=update_variable_name)
            ## 更新状态
            BankState.update_B_state(bank, interbank, target='any', source='any')
        if update_type == 'any':
            ## 更新交易
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新冲击
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新资产负债表
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新状态
            BankState.update_B_state(bank, interbank, target='any', source='any')
        elif update_type == 'transfer':
            ## 更新交易
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way=by_way)
            ## 更新冲击
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新资产负债表
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新状态
            BankState.update_B_state(bank, interbank, target='any', source='any')
        elif update_type == 'shock':
            ## 更新交易
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新冲击
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way=by_way)
            ## 更新资产负债表
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新状态
            BankState.update_B_state(bank, interbank, target='any', source='any')
        elif update_type == 'balance sheet':
            ## 更新交易
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新冲击
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新资产负债表
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way=by_way)
            ## 更新状态
            BankState.update_B_state(bank, interbank, target='any', source='any')
        elif update_type == 'state':
            ## 更新交易
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新冲击
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新资产负债表
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')
            ## 更新状态
            BankState.update_B_state(bank, interbank, target=target, source=source)
        else:
            raise Exception("关键词update_type取词错误".format(update_type))
            pass

        pass
