"""
描述多主体相关的功能
"""

import numpy as np
from dataclasses import dataclass
from SystemicRiskSimulator.core.define.define_type import StateType, MoneyType, IdsType, AbbrType, NameType


@dataclass
class BankCommercial:
    """
    商业银行群
    """
    id_agent: IdsType = np.nan  # agent 之编号 id
    abbr: AbbrType = np.nan  # 缩写 abbr
    fullName: NameType = np.nan  # 全名 fullName
    A_all = MoneyType  # 总资产 A_all: $A_all=A_IB+A_exIB$
    A_IB_all = MoneyType  # 银行间资产加总 A_IB_all
    A_P = MoneyType  # 银行贷款给非金融部门（非银行金融部门）之资产（非流动性资产） A_P
    A_Q = MoneyType  # 银行持有超额准备金（流动性资产） A_Q
    A_R = MoneyType  # 银行持有法定准备金（非流动性资产） A_R
    A_other = MoneyType  # 银行持有的其它资产（NOTE 包括：研究不涉及的资产科目、会计科目之其他资产、不重要且不明确的资产科目） A_other
    Z_all = MoneyType  # 总负债 Z_all: $Z_total=Z_IB+Z_exIB$
    Z_IB_all = MoneyType  # 银行间负债加总 Z_IB_all
    Z_CB = MoneyType  # 持有央行之负债 Z_CB
    Z_D = MoneyType  # 银行获得居民部门存款（非流动性负债） Z_D
    Z_other = MoneyType  # 银行持有的其他负债（NOTE 包括：研究不涉及的负债科目、会计科目之其他负债、不重要且不明确的负债科目） Z_other
    E_all = MoneyType  # 所有者权益 E_all
    Shock_t = MoneyType  # 总冲击目标 Shock_t $Shock_t = Shock_exIB_t+Shock_IB_t$
    Shock_s = MoneyType  # 总冲击源头 Shock_s $Shock_s = Shock_exIB_s+Shock_IB_s$
    Shock_P_def_t = MoneyType  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
    Shock_D_def_s = MoneyType  # 银行存款违约损失冲击源头 Shock_D_def_s
    Shock_IB_def_s = MoneyType  # 银行间违约损失冲击源头 Shock_IB_def_s
    Shock_IB_def_t = MoneyType  # 银行间违约损失冲击目标 Shock_IB_def_t
    Shock_IBA_def_t = MoneyType  # 银行持有共同贷款类资产违约损失冲击目标 Shock_DA_def_t
    Shock_IBA_def_s = MoneyType  # 银行持有共同贷款类资产违约损失冲击源头 Shock_DA_def_s
    Loss_t = MoneyType  # 银行总损失目标 Loss_t
    Loss_exIB_def_t = MoneyType  # 非银行间资产负债违约损失冲击损失目标 Loss_exIB_def_t
    Loss_IB_def_t = MoneyType  # 银行间资产负债违约损失冲击损失目标 Loss_IB_def_t
    Loss_IBA_def_t = MoneyType  # 银行间资产负债违约损失冲击损失目标 Loss_IB_def_t
    Default_s = MoneyType  # 银行总违约量 Default_s
    Default_IB_def_s = MoneyType  # 银行间在违约损失冲击的违约量 Default_IB_s
    Default_D_def_s = MoneyType  # 非银行间在违约损失冲击的存款违约量 Default_D_def_s
    exist = np.nan  # 示性向量之于银行是否存在 is_exist
    exit = np.nan  # 示性向量之于银行是否已退出不存在 is_exit
    hel = np.nan  # 示性向量之于银行是否健康 is_healthy
    isv = np.nan  # 示性向量之于银行是否资不抵债 is_insolvent
    br = np.nan  # 示性向量之于银行是否破产 is_bankrupt
    con = np.nan  # 示性向量之于银行当前轮次是否传染出去 is_contagion
    inf = np.nan  # 示性向量之于银行当前轮次是否遭受感染 is_infect

    def __init__(self, *args, **kwargs):
        for index, key in enumerate(self.__dir__()):
            if not key.startswith('__'):
                setattr(self, key, kwargs[key])
                pass
            pass
        pass  # function

    pass  # class


@dataclass
class DebtAssets:
    """
    贷款资产群
    """
    id_agent: IdsType = np.nan  # agent 之编号 id
    abbr: AbbrType = np.nan  # 缩写 abbr
    fullName: NameType = np.nan  # 全名 fullName
    p: MoneyType = np.nan  # 资产价格 p
    DA: MoneyType = np.nan  # 贷款资产 DA
    Shock_DA_def_t: MoneyType = np.nan  # 贷款资产违约损失冲击目标 Shock_DA_t
    Shock_IBA_t: MoneyType = np.nan  # 银行持有贷款类资产冲击目标 Shock_IBA_t
    Shock_IBA_s: MoneyType = np.nan  # 银行持有贷款类资产冲击源头 Shock_IBA_s
    con = np.nan  # 示性向量之于资产当前轮次是否传染出去 is_contagion
    inf = np.nan  # 示性向量之于资产当前轮次是否遭受感染 is_infect

    def __init__(self, *args, **kwargs):
        for index, key in enumerate(self.__dir__()):
            if not key.startswith('__'):
                setattr(self, key, kwargs[key])
                pass
            pass
        pass  # function

    pass  # class


@dataclass()
class BankInterbank:
    """
    银行间邻接矩阵
    """
    id_agent: IdsType = np.nan  # agent 之间之关联编号 id
    A_IB = MoneyType  # 银行间资产邻接矩阵 A_IB
    Z_IB = MoneyType  # 银行间负债邻接矩阵 Z_IB
    Shock_IB = MoneyType  # 银行间冲击 Shock_IB: $Shock_IB=Shock_IB_def+Shock_IB_run$
    Shock_IB_def = MoneyType  # 银行间违约损失冲击 Shock_IB_def
    Loss_IB = MoneyType  # 银行间市场冲击损失 Loss_IB
    Loss_IB_def = MoneyType  # 银行间资产负债违约冲击损失 Loss_IB_def
    Default_IB = MoneyType  # 银行间违约量 Default_IB
    exist = np.nan  # 示性邻接矩阵之于银行间存在的 is_exist
    exit = np.nan  # 示性邻接矩阵之于银行间已退出不存在的 is_exit
    hel = np.nan  # 示性邻接矩阵之于银行间健康的 is_healthy
    isv = np.nan  # 示性邻接矩阵之于银行间资不抵债的 is_insolvent
    br = np.nan  # 示性邻接矩阵之于银行间破产的 is_bankrupt

    def __init__(self, *args, **kwargs):
        for index, key in enumerate(self.__dir__()):
            if not key.startswith('__'):
                setattr(self, key, kwargs[key])
                pass
            pass
        pass  # function

    pass  # class


@dataclass()
class BanksDebtAssets:
    """
    银行持有贷款资产邻接矩阵
    """
    id_agent: IdsType = np.nan  # agent 之间之关联编号 id
    IBA = MoneyType  # 银行持有贷款类资产邻接矩阵 IBA (NxM)
    IDA_exp_factor = MoneyType  # 银行持有贷款类资产单价变动后的值 IDA_exp_factor (NxM)
    Shock_IBA_def = MoneyType  # 银行持有贷款类资产冲击 Shock_IB: $Shock_IB=Shock_IB_def+Shock_IB_run$
    Loss_IBA = MoneyType  # 银行共同持有贷款类资产冲击损失 Loss_IB
    exist = np.nan  # 示性邻接矩阵之于银行持有贷款资产邻接矩阵存在的 is_exist
    exit = np.nan  # 示性邻接矩阵之于银行持有贷款资产邻接矩阵已退出不存在的 is_exit

    def __init__(self, *args, **kwargs):
        for index, key in enumerate(self.__dir__()):
            if not key.startswith('__'):
                setattr(self, key, kwargs[key])
                pass
            pass
        pass  # function

    pass  # class


@dataclass
class ModelAgent:
    """
    综合 ModelAgent 类型
    """
    id_agent: int  # 编号（必备的）
    BB: BankCommercial  # 商业银行群
    DA: DebtAssets  # 贷款资产群
    IBA: BanksDebtAssets  # 银行持有贷款类资产群
    IB: BankInterbank  # 银行间邻接矩阵

    def __init__(self, id_agent, BB: BankCommercial, IB: BankInterbank, DA: DebtAssets, IBA: BanksDebtAssets):
        self.id_agent = id_agent
        self.BB = BB
        self.IB = IB
        self.DA = DA
        self.IBA = IBA
        pass  # function

    def __getitem__(self, item):
        return getattr(self, item)

    pass  # class
