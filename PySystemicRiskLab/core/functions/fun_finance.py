from PySystemicRiskLab import deepcopy, Union
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_type import StateType, MoneyType, ListType
from PySystemicRiskLab.core.functions.fun_transfer import BankTransfer
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState


class Finance:
    """
    财务相关的功能
    """

    
    update_variable_name: str
    update_variable_value: Union[MoneyType, StateType, ListType]

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
    def update_finance_calculation(cls, bank: BankCommercial, interbank: BankInterbank, bankState: StateType, interbankState: StateType, update_type='auto', by_way: str = 'all', target: str = 'any', source: str = 'any'): #NOW
        """
        更新财务计算。

        遍历哪个变量数据发生了变化，然后以那个变量为起点按照关联式子，链式更新，直到关联末端的变量更新完为止。

        关键字如下：TODO

        Returns:

        """

        ## 按照`update_type`类型更新财务变量
        if update_type == 'auto':  # 按照变动变量自动更新财务变量
            cls.get_update_variable(bank,interbank)
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way=cls.update_variable_name)  # 更新交易
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way=cls.update_variable_name)  # 更新冲击
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way=cls.update_variable_name)  # 更新资产负债表
            BankState.update_B_state(bank, interbank, target='any', source='any')  # 更新状态
        if update_type == 'all':
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')  # 更新交易
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')  # 更新冲击
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')  # 更新资产负债表
            BankState.update_B_state(bank, interbank, target='any', source='any')  # 更新状态
        elif update_type == 'transfer':
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way=by_way)  # 更新交易
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')  # 更新冲击
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')  # 更新资产负债表
            BankState.update_B_state(bank, interbank, target='any', source='any')  # 更新状态
        elif update_type == 'shock':
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')  # 更新交易
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way=by_way)  # 更新冲击
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')  # 更新资产负债表
            BankState.update_B_state(bank, interbank, target='any', source='any')  # 更新状态
        elif update_type == 'balance sheet':
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')  # 更新交易
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')  # 更新冲击
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way=by_way)  # 更新资产负债表
            BankState.update_B_state(bank, interbank, target='any', source='any')  # 更新状态
        elif update_type == 'state':
            BankTransfer.update_B_transfer(bank, interbank, bankState, interbankState, by_way='all')  # 更新交易
            Shock.update_B_Shock(bank, interbank, bankState, interbankState, by_way='all')  # 更新冲击
            BalanceSheet.update_B_balance_sheet(bank, interbank, bankState, interbankState, by_way='all')  # 更新资产负债表
            BankState.update_B_state(bank, interbank, target=target, source=source)  # 更新状态
        else:
            raise Exception("关键词update_type取词错误".format(update_type))
            pass

        pass
