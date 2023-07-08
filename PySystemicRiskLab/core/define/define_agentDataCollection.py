"结构体：定义待收集数据类型"

from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank

pass  # end import


class AgentDataCollection:
    """
    定义待收集数据类型

    Args:
        BB (BankCommercial): 银行个体众；
        IB (BankInterbank): 银行间个体众；

    """
    BB: list
    IB: list

    # @classmethod
    def __init__(self, BB: BankCommercial, IB: BankInterbank):
        self.BB = BB
        self.IB = IB
        pass  # def

    pass  # class
