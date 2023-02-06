"结构体：定义待收集数据类型"

from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank

pass  # end import


class AgentDataCollection:
    """
    #TODO 定义待收集数据类型
    """
    BB: list
    IB: list

    # # @classmethod
    # def __init__(self):
    #     self.BB = []
    #     self.IB = []
    #     pass

    # @classmethod
    def __init__(self, BB: BankCommercial, IB: BankInterbank):
        self.BB = BB
        self.IB = IB
        pass

    pass
