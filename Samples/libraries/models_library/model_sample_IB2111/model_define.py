"""
描述多主体相关的功能
"""

import numpy as np
from dataclasses import dataclass
from typing import Any
from SystemicRiskSimulator.core.define.define_type import StateType, MoneyType, IdsType, AbbrType, NameType


@dataclass
class Note:
    """
    信息备注。表示每一个个体的一些静态的备注信息。

    字段 note 表示各个个体单独的备注。可以是任意数据类型，如字符串、列表、字典等。

    字段 meta 表示元数据，表示整个备注。可以是任意数据类型，如字符串、列表、字典等。可以用于描述业务、实验、模型、算法、数据等的一些宏观的信息。

    如果是字典，那么数据结构建议如下：键名是一个属性，表示个体的备注类型，键值是一个数组，表示每一个银行对应的属性的备注。

    这里的个体主要是指银行、银行间个体等。
    """
    id_bank: IdsType = np.nan  # 银行编号
    id_interbank: IdsType = np.nan  # 银行间关联编号
    abbr_bank: AbbrType = np.nan  # 银行缩写
    fullName_bank: NameType = np.nan  # 银行全名

    strategy_method = np.nan  # 各银行之智库之策略方法。可选值 'preset'、'learning'。默认值 'preset'
    strategy_intelligence = np.nan  # 各银行之智库之策略智能度。可选值 'excellence'、'normal'。默认值 'normal' 。当`strategy_method == 'preset'` 的时候，只能使用 'normal'。
    strategy_Default_IB_def_s = np.nan  # 各银行之智库之银行间在违约损失冲击的违约策略。当 `strategy_method == 'learning'` 的时候生效

    num_bank: int = np.nan  # 银行数量 num_bank

    note: Any = np.nan  # 备注 note
    meta: Any = np.nan  # 元数据 meta

    def __init__(self, *args, **kwargs):
        for index, key in enumerate(self.__dir__()):
            if not key.startswith('__'):
                setattr(self, key, kwargs[key])
                pass
            pass
        pass  # function

    pass  # class


@dataclass
class BankCommercial:
    """
    商业银行群
    """
    id_agent = IdsType  # 编号 id_agent
    A_all = MoneyType  # 总资产 A_all: $A_all=A_IB+A_exIB$
    A_IB_all = MoneyType  # 银行间资产加总 A_IB_all
    A_P = MoneyType  # 银行贷款给非金融部门（非银行金融部门）之资产（非流动性资产） A_P
    A_Q = MoneyType  # 银行持有超额准备金（流动性资产） A_Q
    A_R = MoneyType  # 银行持有法定准备金（非流动性资产） A_R
    A_I = MoneyType  # 银行投资非金融部门之资产 A_I  #HACK 该模型未用到，相当于 A_other 的一部分
    A_other = MoneyType  # 银行持有的其它资产（NOTE 包括：研究不涉及的资产科目、会计科目之其他资产、不重要且不明确的资产科目） A_other
    Z_all = MoneyType  # 总负债 Z_all: $Z_total=Z_IB+Z_exIB$
    Z_IB_all = MoneyType  # 银行间负债加总 Z_IB_all
    Z_CB = MoneyType  # 持有央行之负债 Z_CB
    Z_D = MoneyType  # 银行获得居民部门存款（非流动性负债） Z_D
    Z_I = MoneyType  # 银行投资类负债 Z_I  #HACK 该模型未用到，相当于 Z_other 的一部分
    Z_other = MoneyType  # 银行持有的其他负债（NOTE 包括：研究不涉及的负债科目、会计科目之其他负债、不重要且不明确的负债科目） Z_other
    E_all = MoneyType  # 所有者权益 E_all
    Shock_t = MoneyType  # 总冲击目标 Shock_t $Shock_t = Shock_exIB_t+Shock_IB_t$
    Shock_s = MoneyType  # 总冲击源头 Shock_s $Shock_s = Shock_exIB_s+Shock_IB_s$
    Shock_P_def_t = MoneyType  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
    Shock_D_def_s = MoneyType  # 银行存款违约损失冲击源头 Shock_D_def_s
    Shock_IB_def_s = MoneyType  # 银行间违约损失冲击源头 Shock_IB_def_s
    Shock_IB_def_t = MoneyType  # 银行间违约损失冲击目标 Shock_IB_def_t
    Loss_t = MoneyType  # 银行总损失目标 Loss_t
    Loss_exIB_def_t = MoneyType  # 非银行间资产负债违约损失冲击损失目标 Loss_exIB_def_t
    Loss_IB_def_t = MoneyType  # 银行间资产负债违约损失冲击损失目标 Loss_IB_def_t
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


@dataclass()
class BankInterbank:
    """
    银行间邻接矩阵
    """
    id_agent = IdsType  # 编号 id_agent
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
    theta_IB_def = MoneyType  # 银行间资产负债违约分配比例 theta_IB_def
    strategy_default = np.nan  # 银行间违约策略 strategy_default

    def __init__(self, *args, **kwargs):
        for index, key in enumerate(self.__dir__()):
            if not key.startswith('__'):
                setattr(self, key, kwargs[key])
                pass
            pass
        pass  # function

    pass  # class


@dataclass
class AgentBased:
    """
    agent-based 类型

    除了id_agent，每一个字段数据结构是一个列表。列表为各个体。元素为字典，存储一个个体的数据。键名表示一个变量类型。一般而言，有一个变量类型是 mask ，表示该行轮次步进的值是否有效。键值是一个列表，列表每一个元素表示该变量在一次轮次步进的值。元素表示变量的值。元素的数据结构可以是 Numpy 数组，也可以是标量。

    在一局运行完之后，各个个体之字典数据会转换成一个数据框，以方便后续操作。每一列表示一个变量类型。一般而言，有一个变量类型是 mask ，表示该行轮次步进的值是否有效。元素表示变量的值。数据框每一行表示一次轮次步进。元素的数据结构可以是 Numpy 数组，也可以是标量。
    """
    id_agent: IdsType  # 编号 id_agent
    observations: list  # 各个体之观察值 observations
    actions: list  # 各个体之动作 actions
    rewards: list  # 各个体之奖励 rewards
    dones: list  # 各个体之是否正常结束运行值
    truncations: list  # 各个体之是否中断运行值


@dataclass
class ModelAgent:
    """
    综合 ModelAgent 类型
    """
    id_agent: int  # 编号（必备的）
    BB: BankCommercial  # 商业银行群
    IB: BankInterbank  # 银行间邻接矩阵
    AB: AgentBased  # agent-based 类型
    note: Note  # 备注

    def __init__(self, id_agent, BB: BankCommercial, IB: BankInterbank, AB: AgentBased, note: Note):
        self.id_agent = id_agent
        self.BB = BB
        self.IB = IB
        self.AB = AB
        self.note = note
        pass  # function

    def __getitem__(self, item):
        return getattr(self, item)

    pass  # class
