"结构体：定义待收集数据类型"
from SystemicRiskSimulator import pd
# from SystemicRiskSimulator.core.define.define_agents import BankCommercial, BankInterbank

pass  # end import


class AgentDataCollection:
    """
    定义待收集数据类型

    Args:
        BB (pd.DataFrame): 银行个体众；
        IB (pd.DataFrame): 银行间个体众；

    """
    BB: pd.DataFrame
    IB: pd.DataFrame

    # @classmethod
    def __init__(self, BB: pd.DataFrame, IB: pd.DataFrame):
        self.BB = BB
        self.IB = IB
        pass  # function

    pass  # class
