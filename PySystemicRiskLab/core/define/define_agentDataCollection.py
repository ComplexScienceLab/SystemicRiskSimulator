"结构体：定义待收集数据类型"

from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank

pass  # end import


class AgentDataCollection:
    """
    #TODO 定义待收集数据类型
    """
    BB: list
    BI: list

    # # @classmethod
    # def __init__(self):
    #     self.BB = []
    #     self.BI = []
    #     pass

    # @classmethod
    def __init__(self, BB: BankCommercial, BI: BankInterbank):
        self.BB = BB
        self.BI = BI
        pass

    pass
