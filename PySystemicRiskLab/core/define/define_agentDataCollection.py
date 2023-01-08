"结构体：定义待收集数据类型"

from PySystemicRiskLab import pd
# from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank

pass  # end import


class AgentDataCollection:
    """
    个体众数据集
    """
    BB: pd.Series
    BI: pd.Series

    # # @classmethod
    # def __init__(self):
    #     self.BB = []
    #     self.BI = []
    #     pass

    # @classmethod
    def __init__(self, BB: pd.Series, BI: pd.Series):
        self.BB = BB
        self.BI = BI
        pass

    pass
