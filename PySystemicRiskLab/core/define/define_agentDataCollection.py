"结构体：定义待收集数据类型"

##########################################
# 状态/开发
##########################################

# from PySystemicRiskLab.core import BankCommercial, BankInterbank
pass  # end import

from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
pass  # end import


class AgentDataCollection:
    """
    #TODO 定义待收集数据类型
    """
    BB: list
    BI: list

    def __init__(self, BB: BankCommercial, BI: BankInterbank):
        self.BB = []
        self.BI = []
        pass

    pass
