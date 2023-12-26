"""
结构体：定义各类Agents，基于模式3-1
"""
import numpy as np

from SystemicRiskSimulator.core.define.define_type import *

pass  # end import


class BaseAgents:
    """
    Agents节点基类
    """
    id: IdsType
    abbr: AbbrType
    name: NameType
    pass


class BaseInterAgents:
    """
    Agents间节点基类
    """
    id: IdsType
    abbr: AbbrType
    name: NameType
    pass


class BankCommercial(BaseAgents):  # TODO有必要改成动态创建类属性
    """
    商业银行群复合类
    """
    id_agent: IdsType = np.NaN  # = deepcopy(RANGE1) agent 之编号 id
    abbr = np.NaN  # = np.full(sgv['num_bank'], "")
    name = np.NaN  # = np.full(sgv['num_bank'], "")
    A_all = np.NaN  # = deepcopy(ZEROS1)  # 总资产 A_all: $A_all=A_IB+A_exIB$
    A_IB_all = np.NaN  # = deepcopy(ZEROS1)  # 银行间资产加总 A_IB_all
    A_exIB = np.NaN  # = deepcopy(ZEROS1)  # 非银行间资产 A_exIB: $A_exIB=A_P+A_Q+A_R+A_other$
    A_P = np.NaN  # = deepcopy(ZEROS1)  # 银行贷款给非金融部门（非银行金融部门）之资产（非流动性资产） A_P
    A_Q = np.NaN  # = deepcopy(ZEROS1)  # 银行持有超额准备金（流动性资产） A_Q
    A_R = np.NaN  # = deepcopy(ZEROS1)  # 银行持有法定准备金（非流动性资产） A_R
    A_other = np.NaN  # = deepcopy(ZEROS1)  # 银行持有的其它资产（NOTE 包括：研究不涉及的资产科目、会计科目之其他资产、不重要且不明确的资产科目） A_other
    Z_all = np.NaN  # = deepcopy(ZEROS1)  # 总负债 Z_all: $Z_total=Z_IB+Z_exIB$
    Z_IB_all = np.NaN  # = deepcopy(ZEROS1)  # 银行间负债加总 Z_IB_all
    Z_exIB = np.NaN  # = deepcopy(ZEROS1)  # 非银行间负债 Z_exIB: $Z_exIB=Z_D+Z_CB+Z_other$
    Z_CB = np.NaN  # = deepcopy(ZEROS1)  # 持有央行之负债 Z_CB
    Z_D = np.NaN  # = deepcopy(ZEROS1)  # 银行获得居民部门存款（非流动性负债） Z_D
    Z_other = np.NaN  # = deepcopy(ZEROS1)  # 银行持有的其他负债（NOTE 包括：研究不涉及的负债科目、会计科目之其他负债、不重要且不明确的负债科目） Z_other
    E_all = np.NaN  # = deepcopy(ZEROS1)  # 所有者权益 E_all
    T_all = np.NaN  # = deepcopy(ZEROS1)  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
    Lo_all = np.NaN  # = deepcopy(ZEROS1)  # 总贷款流出（贷款方发款出去） Lo_all: $Lo_all=Lo_IB_all+Lo_exIB$
    Lo_IB_all = np.NaN  # = deepcopy(ZEROS1)  # 银行间贷款流出 Lo_IB_all
    Lo_exIB = np.NaN  # = deepcopy(ZEROS1)  # 非银行间贷款流出 Lo_exIB: $Lo_exIB=Lo_P$
    Lo_P = np.NaN  # = deepcopy(ZEROS1)  # 银行贷款流出给生产部门 Lo_P
    Li_all = np.NaN  # = deepcopy(ZEROS1)  # 总贷款流入（贷款方收款回来） Li_all: $Li_all=Li_IB_all+Li_exIB$
    Li_IB_all = np.NaN  # = deepcopy(ZEROS1)  # 银行间贷款流入 Li_IB_all
    Li_exIB = np.NaN  # = deepcopy(ZEROS1)  # 非银行间贷款流入 Li_exIB: $Li_exIB=Li_D$
    Li_P = np.NaN  # = deepcopy(ZEROS1)  # 银行贷款流入从生产部门 Li_P
    Bi_all = np.NaN  # = deepcopy(ZEROS1)  # 总借款流入（借款方借款进来） Bi_all: $Bi_all=Bi_IB_all+Bi_exIB$
    Bi_IB_all = np.NaN  # = deepcopy(ZEROS1)  # 银行间借款流入 Bi_IB_all
    Bi_exIB = np.NaN  # = deepcopy(ZEROS1)  # 非银行间借款流入 Bi_exIB: $Bi_exIB=Bi_D$
    Bi_D = np.NaN  # = deepcopy(ZEROS1)  # 银行借款流入从居民部门 Bi_D
    Bo_all = np.NaN  # = deepcopy(ZEROS1)  # 总借款流出（借款方还款出去） Bo_all: $Bo_all=Bo_IB_all+Bo_exIB$
    Bo_IB_all = np.NaN  # = deepcopy(ZEROS1)  # 银行间借款流出 Bo_IB_all
    Bo_exIB = np.NaN  # = deepcopy(ZEROS1)  # 非银行间借款流出 Bo_exIB: $Bo_exIB=Bo_P$
    Bo_D = np.NaN  # = deepcopy(ZEROS1)  # 银行借款流出给居民部门 Bo_D
    Shock_t = np.NaN  # = deepcopy(ZEROS1)  # 总冲击目标 Shock_t $Shock_t = Shock_exIB_t+Shock_IB_t$
    Shock_s = np.NaN  # = deepcopy(ZEROS1)  # 总冲击源头 Shock_s $Shock_s = Shock_exIB_s+Shock_IB_s$
    Shock_def_t = np.NaN  # = deepcopy(ZEROS1)  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_P_def_t+Shock_D_run_t$
    Shock_def_s = np.NaN  # = deepcopy(ZEROS1)  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exIB_def_s+Shock_IB_def_s$
    Shock_run_t = np.NaN  # = deepcopy(ZEROS1)  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exIB_run_t+Shock_IB_run_t$
    Shock_run_s = np.NaN  # = deepcopy(ZEROS1)  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exIB_run_s+Shock_IB_run_s$
    Shock_exIB_t = np.NaN  # = deepcopy(ZEROS1)  # 非银行间借贷冲击目标 Shock_exIB_t $Shock_exIB_t = Shock_P_def_t+Shock_D_run_t$
    Shock_exIB_s = np.NaN  # = deepcopy(ZEROS1)  # 非银行间借贷冲击源头 Shock_exIB_s $Shock_exIB_s = Shock_P_run_s+Shock_D_def_s$
    Shock_P_run_s = np.NaN  # = deepcopy(ZEROS1)  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
    Shock_P_def_t = np.NaN  # = deepcopy(ZEROS1)  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
    Shock_D_def_s = np.NaN  # = deepcopy(ZEROS1)  # 银行存款违约损失冲击源头 Shock_D_def_s
    Shock_D_run_t = np.NaN  # = deepcopy(ZEROS1)  # 银行存款挤兑流动冲击目标 Shock_D_run_t
    Shock_B = np.NaN  # = deepcopy(ZEROS1)  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$  #HACK无用
    Shock_B_A = np.NaN  # = deepcopy(ZEROS1)  # 银行内资产负债之银行间资产端冲击 Shock_B_A  #HACK无用
    Shock_B_Z = np.NaN  # = deepcopy(ZEROS1)  # 银行内资产负债之银行间负债端冲击 Shock_B_Z  #HACK无用
    Shock_IB_s = np.NaN  # = deepcopy(ZEROS1)  # 银行间冲击源头 Shock_IB_s $Shock_IB_s=Shock_IB_def_s+Shock_IB_run_s$
    Shock_IB_t = np.NaN  # = deepcopy(ZEROS1)  # 银行间冲击目标 Shock_IB_t $Shock_IB_t=Shock_IB_def_t+Shock_IB_run_t$
    Shock_IB_def_s = np.NaN  # = deepcopy(ZEROS1)  # 银行间违约损失冲击源头 Shock_IB_def_s
    Shock_IB_def_t = np.NaN  # = deepcopy(ZEROS1)  # 银行间违约损失冲击目标 Shock_IB_def_t
    Shock_IB_run_s = np.NaN  # = deepcopy(ZEROS1)  # 银行间挤兑流动冲击源头 Shock_IB_run_s $Shock_IB_run_s=Shock_IB_run_ilq_s+Shock_IB_run_br_s$
    Shock_IB_run_t = np.NaN  # = deepcopy(ZEROS1)  # 银行间挤兑流动冲击目标 Shock_IB_run_t $Shock_IB_run_t+Shock_IB_run_ilq_t+Shock_IB_run_br_t$
    Shock_IB_run_ilq_s = np.NaN  # = deepcopy(ZEROS1)  # 银行间流动性短缺挤兑流动冲击源头 Shock_IB_run_ilq_s
    Shock_IB_run_ilq_t = np.NaN  # = deepcopy(ZEROS1)  # 银行间流动性短缺挤兑流动冲击目标 Shock_IB_run_ilq_t
    Shock_IB_run_br_s = np.NaN  # = deepcopy(ZEROS1)  # 银行间倒闭挤兑流动冲击源头 Shock_IB_run_br_s
    Shock_IB_run_br_t = np.NaN  # = deepcopy(ZEROS1)  # 银行间倒闭挤兑流动冲击目标 Shock_IB_run_br_t
    Loss_t = np.NaN  # = deepcopy(ZEROS1)  # 银行总损失目标 Loss_t
    # Loss_s = np.NaN  # = deepcopy(ZEROS1)  # 银行总损失源头 Loss_s
    Loss_exIB_t = np.NaN  # = deepcopy(ZEROS1)  # 非银行间资产负债总损失目标 Loss_exIB_t
    # Loss_exIB_s =  np.NaN  # = deepcopy(ZEROS1)  # 非银行间资产负债总损失源头 Loss_exIB_s
    Loss_exIB_def_t = np.NaN  # = deepcopy(ZEROS1)  # 非银行间资产负债违约损失冲击损失目标 Loss_exIB_def_t
    # Loss_exIB_def_s =  np.NaN  # = deepcopy(ZEROS1)  # 非银行间资产负债违约损失冲击损失源头 Loss_exIB_def_s
    Loss_exIB_run_t = np.NaN  # = deepcopy(ZEROS1)  # 非银行间负债流动性挤兑冲击损失目标 Loss_exIB_run_t
    # Loss_exIB_run_s =  np.NaN  # = deepcopy(ZEROS1)  # 非银行间负债流动性挤兑冲击损失源头 Loss_exIB_run_s
    Loss_def_t = np.NaN  # = deepcopy(ZEROS1)  # 银行资产负债违约总损失目标 Loss_def_t
    # Loss_def_s = np.NaN  # = deepcopy(ZEROS1)  # 银行资产负债违约总损失源头 Loss_def_s
    Loss_run_t = np.NaN  # = deepcopy(ZEROS1)  # 银行负债流动性挤兑总损失目标 Loss_run_t
    # Loss_run_s = np.NaN  # = deepcopy(ZEROS1)  # 银行负债流动性挤兑总损失源头 Loss_run_s
    Loss_IB_t = np.NaN  # = deepcopy(ZEROS1)  # 银行间市场冲击损失目标 Loss_IB_t
    # Loss_IB_s = np.NaN  # = deepcopy(ZEROS1)  # 银行间市场冲击损失源头 Loss_IB_s
    Loss_IB_def_t = np.NaN  # = deepcopy(ZEROS1)  # 银行间资产负债违约损失冲击损失目标 Loss_IB_def_t
    # Loss_IB_def_s = np.NaN  # = deepcopy(ZEROS1)  # 银行间资产负债违约损失冲击损失源头 Loss_IB_def_s
    Loss_IB_run_t = np.NaN  # = deepcopy(ZEROS1)  # 银行间负债流动性挤兑冲击损失目标 Loss_IB_run_t
    # Loss_IB_run_s = np.NaN  # = deepcopy(ZEROS1)  # 银行间负债流动性挤兑冲击损失源头 Loss_IB_run_s
    on = np.NaN  # = deepcopy(TRUE1)  # 示性向量之于银行是否存在 is_on
    off = np.NaN  # = deepcopy(FALSE1)  # 示性向量之于银行是否已退出不存在 is_off
    hel = np.NaN  # = deepcopy(TRUE1)  # 示性向量之于银行是否健康 is_healthy
    isv = np.NaN  # = deepcopy(FALSE1)  # 示性向量之于银行是否资不抵债 is_insolvent
    ilq = np.NaN  # = deepcopy(FALSE1)  # 示性向量之于银行是否流动性短缺 is_illiquid
    br = np.NaN  # = deepcopy(FALSE1)  # 示性向量之于银行是否破产 is_bankrupt
    is_needed_BoIB = np.NaN  # = deepcopy(FALSE1)  # 示性向量之于银行是否需要偿还银行间借款 is_needed_BoIB
    is_enabled_BoIB = np.NaN  # = deepcopy(TRUE1)  # 示性向量之于银行是否可以偿还银行间借款 is_enabled_BoIB
    is_needed_BoD = np.NaN  # = deepcopy(FALSE1)  # 示性向量之于银行是否需要偿还居民部门存款 is_needed_BoD
    is_enabled_BoD = np.NaN  # = deepcopy(TRUE1)  # 示性向量之于银行是否可以偿还居民部门存款 is_enabled_BoD
    is_needed_LiP = np.NaN  # = deepcopy(FALSE1)  # 示性向量之于银行是否需要收回厂商贷款 is_needed_LiP
    is_enabled_LiP = np.NaN  # = deepcopy(TRUE1)  # 示性向量之于银行是否可以收回厂商贷款 is_enabled_LiP
    is_allocated_Shock = np.NaN  # = deepcopy(FALSE1)  # 示性向量之于银行是否已经分配传染冲击 is_allocated_Shock
    list_exist = np.NaN  # = np.full((sgv['num_bank'], 1), list)  # 列表之于存在的银行编号 list_exist
    list_insolvent = np.NaN  # = np.full((sgv['num_bank'], 1), list)  # 列表之于资不抵债的银行编号 list_insolvent
    list_illiquid = np.NaN  # = np.full((sgv['num_bank'], 1), list)  # 列表之于流动性短缺的银行编号 list_illiquid
    list_bankrupt = np.NaN  # = np.full((sgv['num_bank'], 1), list)  # 列表之于破产的银行编号 list_bankrupt

    # TODO 增加监管约束之状态；

    def __init__(self, *args, **kwargs):
        for index, key in enumerate(self.__dir__()):
            if not key.startswith('__'):
                setattr(self, key, kwargs[key])
                pass
            pass
        pass  # function

    pass  # class


class BankInterbank(BaseInterAgents):
    """
    银行间邻接矩阵复合类
    """
    id_agent = np.NaN  # agent 之间之关联编号 id
    A_IB = np.NaN  # 银行间资产邻接矩阵 A_IB
    Z_IB = np.NaN  # 银行间负债邻接矩阵 Z_IB
    Lo_IB = np.NaN  # 银行间贷款流出邻接矩阵 Lo_IB
    Li_IB = np.NaN  # 银行间贷款流入邻接矩阵 Li_IB
    Bo_IB = np.NaN  # 银行间借款流入邻接矩阵 Bo_IB
    Bi_IB = np.NaN  # 银行间借款流出邻接矩阵 Bi_IB
    Shock_IB = np.NaN  # 银行间冲击 Shock_IB: $Shock_IB=Shock_IB_def+Shock_IB_run$
    Shock_IB_def = np.NaN  # 银行间违约损失冲击 Shock_IB_def
    Shock_IB_run = np.NaN  # 银行间挤兑流动冲击 Shock_IB_run: $Shock_IB_run=Shock_IB_run_ilq+Shock_IB_run_br$
    Shock_IB_run_ilq = np.NaN  # 流动性短缺银行银行间挤兑流动冲击 Shock_IB_run_ilq
    Shock_IB_run_br = np.NaN  # 破产银行银行间挤兑流动冲击 Shock_IB_run_br
    Loss_IB = np.NaN  # 银行间市场冲击损失 Loss_IB
    Loss_IB_def = np.NaN  # 银行间资产负债违约冲击损失 Loss_IB_def
    Loss_IB_run = np.NaN  # 银行间负债流动性挤兑冲击损失 Loss_IB_run
    is_exposure = np.NaN  # 信息邻接矩阵之于是否有银行间敞口 is_exposure
    on = np.NaN  # 信息邻接矩阵之于银行间存在的 is_on
    off = np.NaN  # 信息邻接矩阵之于银行间已退出不存在的 is_off
    hel = np.NaN  # 信息邻接矩阵之于银行间健康的 is_healthy
    isv = np.NaN  # 信息邻接矩阵之于银行间资不抵债的 is_insolvent
    ilq = np.NaN  # 信息邻接矩阵之于银行间流动性短缺的 is_illiquid
    br = np.NaN  # 信息邻接矩阵之于银行间破产的 is_bankrupt
    cre = np.NaN  # 信息列表之于各银行之债权方银行编号 list_creditors
    deb = np.NaN  # 信息列表之于各银行之债务方银行编号 list_debtors
    cre_isv = np.NaN  # 信息列表之于资不抵债的银行之债权方银行编号 list_creditors_in_insolvent
    deb_isv = np.NaN  # 信息列表之于资不抵债的银行之债务方银行编号 list_debtors_in_insolvent
    cre_ilq = np.NaN  # 信息列表之于流动性短缺的银行之债权方银行编号 list_creditors_in_illiquid
    deb_ilq = np.NaN  # 信息列表之于流动性短缺的银行之债务方银行编号 list_debtors_in_illiquid
    cre_br = np.NaN  # 信息列表之于破产的银行之债权方银行编号 list_creditors_in_bankrupt
    deb_br = np.NaN  # 信息列表之于破产的银行之债务方银行编号 list_debtors_in_bankrupt

    def __init__(self, *args, **kwargs):
        for index, key in enumerate(self.__dir__()):
            if not key.startswith('__'):
                setattr(self, key, kwargs[key])
                pass
            pass
        pass  # function

    pass  # class


class SystemicRiskAgent:
    """
    综合SystemicRiskAgents类型
    """
    id_agent: int  # 编号（必备的）
    BB: BankCommercial  # 商业银行群
    b: StateType  # 商业银行群示性向量
    IB: BankInterbank  # 银行间邻接矩阵
    ib: StateType  # 银行间邻接矩阵示性矩阵

    def __init__(self, id_agent, BB: BankCommercial, b: StateType, IB: BankInterbank, ib: StateType):
        self.id_agent = id_agent
        self.BB = BB
        self.b = b
        self.IB = IB
        self.ib = ib
        pass

    pass
