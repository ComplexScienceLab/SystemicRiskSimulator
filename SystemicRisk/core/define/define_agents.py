"结构体：定义各类Agents，基于模式3-1"

## 程序：定义各类Agents，基于模式3-1

##########################################
# 状态/使用
##########################################

# from SystemicRisk.core import env
# from SystemicRisk.core.define.define_type import *
pass  # end import



from SystemicRisk.core.define.define_environment_variables import env
from SystemicRisk.core.define.define_type import *
pass  # end import





class BaseAgents:
    """
    Agents节点基类
    """
    id: TypeIds
    abbr: TypeAbbr
    name: TypeName
    pass


class BaseInterAgents:
    """
    Agents间节点基类
    """
    id: TypeIds
    abbr: TypeAbbr
    name: TypeName
    pass


# class BankCommercial:
class BankCommercial(BaseAgents):
    """
    商业银行群复合类
    """
    id: TypeIds
    abbr: TypeAbbr
    name: TypeName
    A_all: TypeMoney  # 总资产 A_all: $A_all=A_BI+A_exBI$
    A_BI_all: TypeMoney  # 银行间资产加总 A_BI_all
    A_exBI: TypeMoney  # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
    A_P: TypeMoney  # 银行贷款给生产部门之资产（非流动性资产） A_P
    A_Q: TypeMoney  # 银行持有超额准备金（流动性资产） A_Q
    A_R: TypeMoney  # 银行持有法定准备金（非流动性资产） A_R
    A_other: TypeMoney  # 银行持有的其它资产（非流动性资产） A_other
    Z_all: TypeMoney  # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
    Z_BI_all: TypeMoney  # 银行间负债加总 Z_BI_all
    Z_exBI: TypeMoney  # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
    Z_D: TypeMoney  # 银行获得居民部门存款（非流动性负债） Z_D
    Z_other: TypeMoney  # 银行持有的其他负债（非流动性负债） Z_other
    E_all: TypeMoney  # 所有者权益 E_all
    T_all: TypeMoney  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
    Lo_all: TypeMoney  # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
    Lo_BI_all: TypeMoney  # 银行间贷款流出 Lo_BI_all
    Lo_exBI: TypeMoney  # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
    Lo_P: TypeMoney  # 银行贷款流出给生产部门 Lo_P
    Li_all: TypeMoney  # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
    Li_BI_all: TypeMoney  # 银行间贷款流入 Li_BI_all
    Li_exBI: TypeMoney  # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
    Li_P: TypeMoney  # 银行贷款流入从生产部门 Li_P
    Bi_all: TypeMoney  # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
    Bi_BI_all: TypeMoney  # 银行间借款流入 Bi_BI_all
    Bi_exBI: TypeMoney  # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
    Bi_D: TypeMoney  # 银行借款流入从居民部门 Bi_D
    Bo_all: TypeMoney  # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
    Bo_BI_all: TypeMoney  # 银行间借款流出 Bo_BI_all
    Bo_exBI: TypeMoney  # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
    Bo_D: TypeMoney  # 银行借款流出给居民部门 Bo_D
    Shock_t: TypeMoney  # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
    Shock_s: TypeMoney  # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
    Shock_def_t: TypeMoney  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_P_def_t+Shock_D_run_t$
    Shock_def_s: TypeMoney  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
    Shock_run_t: TypeMoney  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
    Shock_run_s: TypeMoney  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
    Shock_exBI_t: TypeMoney  # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
    Shock_exBI_s: TypeMoney  # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
    Shock_P_run_s: TypeMoney  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
    Shock_P_def_t: TypeMoney  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
    Shock_D_def_s: TypeMoney  # 银行存款违约损失冲击源头 Shock_D_def_s
    Shock_D_run_t: TypeMoney  # 银行存款挤兑流动冲击目标 Shock_D_run_t
    Shock_B: TypeMoney  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
    Shock_B_A: TypeMoney  # 银行内资产负债之银行间资产端冲击 Shock_B_A
    Shock_B_Z: TypeMoney  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
    Shock_BI_s: TypeMoney  # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
    Shock_BI_t: TypeMoney  # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
    Shock_BI_def_s: TypeMoney  # 银行间违约损失冲击源头 Shock_BI_def_s
    Shock_BI_def_t: TypeMoney  # 银行间违约损失冲击目标 Shock_BI_def_t
    Shock_BI_run_s: TypeMoney  # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
    Shock_BI_run_t: TypeMoney  # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
    Shock_BI_run_ilq_s: TypeMoney  # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
    Shock_BI_run_ilq_t: TypeMoney  # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
    Shock_BI_run_br_s: TypeMoney  # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
    Shock_BI_run_br_t: TypeMoney  # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
    Loss_BI: TypeMoney  # 银行间市场冲击损失 Loss_BI
    Loss_BI_def_t: TypeMoney  # 银行间资产负债违约冲击损失 Loss_BI_def_t
    Loss_BI_run_t: TypeMoney  # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
    on: TypeState  # 示性向量之于银行是否存在 isOn
    off: TypeState  # 示性向量之于银行是否已退出不存在 isOff
    hel: TypeState  # 示性向量之于银行是否健康 isHealthy
    isv: TypeState  # 示性向量之于银行是否资不抵债 isInsolvent
    ilq: TypeState  # 示性向量之于银行是否流动性短缺 isIlliquity
    br: TypeState  # 示性向量之于银行是否破产 isBankrupt
    nBoBI: TypeState  # 示性向量之于银行是否需要偿还银行间借款 isNeededBoBI
    eBoBI: TypeState  # 示性向量之于银行是否可以偿还银行间借款 isEnabledBoBI
    nBoD: TypeState  # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
    eBoD: TypeState  # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
    nLiP: TypeState  # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
    eLiP: TypeState  # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP
    isAllocatedShock: TypeState  # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
    listOfExist: TypeList  # 列表之于存在的银行编号 listOfExist
    listOfInsolvent: TypeList  # 列表之于资不抵债的银行编号 listOfInsolvent
    listOfIlliquity: TypeList  # 列表之于流动性短缺的银行编号 listOfIlliquity
    listOfBankrupt: TypeList  # 列表之于破产的银行编号 listOfBankrupt

    # TODO 补充损失变量；
    # TODO 增加监管约束之状态；

    def __init__(self):
        self.id = np.arange(1, env['num_bank'], step=1),  # 编号 id
        self.abbr = np.full(env['num_bank'], ""),  # 缩写 abbr
        self.name = np.full(env['num_bank'], ""),  # 全名 name
        self.A_all = np.zeros((env['num_bank'])),  # 总资产 A_all: $A_all=A_BI+A_exBI$
        self.A_BI_all = np.zeros((env['num_bank'])),  # 银行间资产加总 A_BI_all
        self.A_exBI = np.zeros((env['num_bank'])),  # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
        self.A_P = np.zeros((env['num_bank'])),  # 银行贷款给生产部门之资产（非流动性资产） A_P
        self.A_Q = np.zeros((env['num_bank'])),  # 银行持有超额准备金（流动性资产） A_Q
        self.A_R = np.zeros((env['num_bank'])),  # 银行持有法定准备金（非流动性资产） A_R
        self.A_other = np.zeros((env['num_bank'])),  # 银行持有的其它资产（非流动性资产） A_other
        self.Z_all = np.zeros((env['num_bank'])),  # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
        self.Z_BI_all = np.zeros((env['num_bank'])),  # 银行间负债加总 Z_BI_all
        self.Z_exBI = np.zeros((env['num_bank'])),  # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
        self.Z_D = np.zeros((env['num_bank'])),  # 银行获得居民部门存款（非流动性负债） Z_D
        self.Z_other = np.zeros((env['num_bank'])),  # 银行持有的其他负债（非流动性负债） Z_other
        self.E_all = np.zeros((env['num_bank'])),  # 所有者权益 E_all
        self.T_all = np.zeros((env['num_bank'])),  # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
        self.Lo_all = np.zeros((env['num_bank'])),  # 银行间贷款流出 Lo_BI_all
        self.Lo_BI_all = np.zeros((env['num_bank'])),  # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
        self.Lo_exBI = np.zeros((env['num_bank'])),  # 银行贷款流出给生产部门 Lo_P
        self.Lo_P = np.zeros((env['num_bank'])),  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
        self.Li_all = np.zeros((env['num_bank'])),  # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
        self.Li_BI_all = np.zeros((env['num_bank'])),  # 银行间贷款流入 Li_BI_all
        self.Li_exBI = np.zeros((env['num_bank'])),  # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
        self.Li_P = np.zeros((env['num_bank'])),  # 银行贷款流入从生产部门 Li_P
        self.Bi_all = np.zeros((env['num_bank'])),  # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
        self.Bi_BI_all = np.zeros((env['num_bank'])),  # 银行间借款流入 Bi_BI_all
        self.Bi_exBI = np.zeros((env['num_bank'])),  # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
        self.Bi_D = np.zeros((env['num_bank'])),  # 银行借款流入从居民部门 Bi_D
        self.Bo_all = np.zeros((env['num_bank'])),  # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
        self.Bo_BI_all = np.zeros((env['num_bank'])),  # 银行间借款流出 Bo_BI_all
        self.Bo_exBI = np.zeros((env['num_bank'])),  # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
        self.Bo_D = np.zeros((env['num_bank'])),  # 银行借款流出给居民部门 Bo_D
        self.Shock_t = np.zeros((env['num_bank'])),  # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
        self.Shock_s = np.zeros((env['num_bank'])),  # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
        self.Shock_def_t = np.zeros((env['num_bank'])),  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exBI_def_t+Shock_BI_def_t$
        self.Shock_def_s = np.zeros((env['num_bank'])),  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
        self.Shock_run_t = np.zeros((env['num_bank'])),  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
        self.Shock_run_s = np.zeros((env['num_bank'])),  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
        self.Shock_exBI_t = np.zeros((env['num_bank'])),  # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
        self.Shock_exBI_s = np.zeros((env['num_bank'])),  # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
        self.Shock_P_run_s = np.zeros((env['num_bank'])),  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
        self.Shock_P_def_t = np.zeros((env['num_bank'])),  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
        self.Shock_D_def_s = np.zeros((env['num_bank'])),  # 银行存款违约损失冲击源头 Shock_D_def_s
        self.Shock_D_run_t = np.zeros((env['num_bank'])),  # 银行存款挤兑流动冲击目标 Shock_D_run_t
        self.Shock_B = np.zeros((env['num_bank'])),  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
        self.Shock_B_A = np.zeros((env['num_bank'])),  # 银行内资产负债之银行间资产端冲击 Shock_B_A
        self.Shock_B_Z = np.zeros((env['num_bank'])),  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
        self.Shock_BI_s = np.zeros((env['num_bank'])),  # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
        self.Shock_BI_t = np.zeros((env['num_bank'])),  # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
        self.Shock_BI_def_s = np.zeros((env['num_bank'])),  # 银行间违约损失冲击源头 Shock_BI_def_s
        self.Shock_BI_def_t = np.zeros((env['num_bank'])),  # 银行间违约损失冲击目标 Shock_BI_def_t
        self.Shock_BI_run_s = np.zeros((env['num_bank'])),  # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
        self.Shock_BI_run_t = np.zeros((env['num_bank'])),  # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
        self.Shock_BI_run_ilq_s = np.zeros((env['num_bank'])),  # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
        self.Shock_BI_run_ilq_t = np.zeros((env['num_bank'])),  # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
        self.Shock_BI_run_br_s = np.zeros((env['num_bank'])),  # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
        self.Shock_BI_run_br_t = np.zeros((env['num_bank'])),  # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
        self.Loss_BI = np.zeros((env['num_bank'])),  # 银行间市场冲击损失 Loss_BI
        self.Loss_BI_def_t = np.zeros((env['num_bank'])),  # 银行间资产负债违约冲击损失 Loss_BI_def_t
        self.Loss_BI_run_t = np.zeros((env['num_bank'])),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
        self.on = np.full(env['num_bank'], True),  # 示性向量之于银行是否存在 isOn
        self.off = np.full(env['num_bank'], False),  # 示性向量之于银行是否已退出不存在 isOff
        self.hel = np.full(env['num_bank'], True),  # 示性向量之于银行是否健康 isHealthy
        self.isv = np.full(env['num_bank'], False),  # 示性向量之于银行是否资不抵债 isInsolvent
        self.ilq = np.full(env['num_bank'], False),  # 示性向量之于银行是否流动性短缺 isIlliquity
        self.br = np.full(env['num_bank'], False),  # 示性向量之于银行是否破产 isBankrupt
        self.nBoBI = np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还借款 isNeededBoBI
        self.eBoBI = np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还借款 isEnabledBoBI
        self.nBoD = np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
        self.eBoD = np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
        self.nLiP = np.full(env['num_bank'], False),  # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
        self.eLiP = np.full(env['num_bank'], True),  # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP
        self.isAllocatedShock = np.full(env['num_bank'], False),  # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
        self.listOfExist = np.full(env['num_bank'], list),  # 列表之于存在的银行编号 listOfExist
        self.listOfInsolvent = np.full(env['num_bank'], list),  # 列表之于资不抵债的银行编号 listOfInsolvent
        self.listOfIlliquity = np.full(env['num_bank'], list),  # 列表之于流动性短缺的银行编号 listOfIlliquity
        self.listOfBankrupt = np.full(env['num_bank'], list)  # 列表之于破产的银行编号 listOfBankrupt
        pass # init

    pass # class


# class BankInterbank:
class BankInterbank(BaseInterAgents):
    """
    银行间邻接矩阵复合类
    """
    id: TypeIds
    abbr: TypeAbbr
    name: TypeName
    A_BI: TypeMoney  # 银行间资产邻接矩阵 A_BI
    Z_BI: TypeMoney  # 银行间负债邻接矩阵 Z_BI
    Lo_BI: TypeMoney  # 银行间贷款流出邻接矩阵 Lo_BI
    Li_BI: TypeMoney  # 银行间贷款流入邻接矩阵 Li_BI
    Bo_BI: TypeMoney  # 银行间借款流入邻接矩阵 Bo_BI
    Bi_BI: TypeMoney  # 银行间借款流出邻接矩阵 Bi_BI
    Shock_BI: TypeMoney  # 银行间冲击 Shock_BI: $Shock_BI=Shock_BI_def+Shock_BI_run$
    Shock_BI_def: TypeMoney  # 银行间违约损失冲击 Shock_BI_def
    Shock_BI_run: TypeMoney  # 银行间挤兑流动冲击 Shock_BI_run: $Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
    Shock_BI_run_ilq: TypeMoney  # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
    Shock_BI_run_br: TypeMoney  # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
    Loss_BI: TypeMoney  # 银行间市场冲击损失 Loss_BI
    Loss_BI_def: TypeMoney  # 银行间资产负债违约冲击损失 Loss_BI_def
    Loss_BI_run: TypeMoney  # 银行间负债流动性挤兑冲击损失 Loss_BI_run
    isExposure: TypeState  # 信息邻接矩阵之于是否有银行间敞口 isExposure
    on: TypeState  # 信息邻接矩阵之于银行间存在的 isOn
    off: TypeState  # 信息邻接矩阵之于银行间已退出不存在的 isOff
    hel: TypeState  # 信息邻接矩阵之于银行间健康的 isHealthy
    isv: TypeState  # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
    ilq: TypeState  # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
    br: TypeState  # 信息邻接矩阵之于银行间破产的 isBankrupt
    cre: TypeList  # 信息列表之于各银行之债权方银行编号 listOfCreditors
    deb: TypeList  # 信息列表之于各银行之债务方银行编号 listOfDebtors
    cre_isv: TypeList  # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
    deb_isv: TypeList  # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
    cre_ilq: TypeList  # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
    deb_ilq: TypeList  # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
    cre_br: TypeList  # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
    deb_br: TypeList  # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt

    def __init__(self):
        self.id = np.arange(1, env['num_bank'] * env['num_bank'] + 1).reshape((env['num_bank'], env['num_bank'])),  # 编号
        self.abbr = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产邻接矩阵 A_BI
        self.name = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间负债邻接矩阵 Z_BI
        self.A_BI = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流出邻接矩阵 Lo_BI
        self.Z_BI = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流入邻接矩阵 Li_BI
        self.Lo_BI = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流入邻接矩阵 Bo_BI
        self.Li_BI = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流出邻接矩阵 Bi_BI
        self.Bo_BI = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间冲击 Shock_BI: $Shock_BI=Shock_BI_def+Shock_BI_run$
        self.Bi_BI = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间违约损失冲击 Shock_BI_def
        self.Shock_BI = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间挤兑流动冲击 Shock_BI_run: $Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
        self.Shock_BI_def = np.zeros((env['num_bank'], env['num_bank'])),  # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
        self.Shock_BI_run = np.zeros((env['num_bank'], env['num_bank'])),  # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
        self.Shock_BI_run_ilq = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间市场冲击损失 Loss_BI
        self.Shock_BI_run_br = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产负债违约冲击损失 Loss_BI_def
        self.Loss_BI = np.zeros((env['num_bank'], env['num_bank'])),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run
        self.Loss_BI_def = np.zeros((env['num_bank'], env['num_bank'])),  # 信息邻接矩阵之于是否有银行间敞口 isExposure
        self.Loss_BI_run = np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间存在的 isOn
        self.isExposure = np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间已退出不存在的 isOff
        self.on = np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间健康的 isHealthy
        self.off = np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
        self.hel = np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
        self.isv = np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间破产的 isBankrupt
        self.ilq = [],  # 信息列表之于各银行之债权方银行编号 listOfCreditors
        self.br = [],  # 信息列表之于各银行之债务方银行编号 listOfDebtors
        self.cre = [],  # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
        self.deb = [],  # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
        self.cre_isv = [],  # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
        self.deb_isv = [],  # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
        self.cre_ilq = [],  # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
        self.deb_ilq = []  # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt
        pass # init

    pass # class


class SystemicRiskAgent:
    """
    综合SystemicRiskAgents类型
    """
    id: int  # 编号（必备的）
    BB: BankCommercial  # 商业银行群
    BI: BankInterbank  # 银行间邻接矩阵

    def __init__(BB: BankCommercial, BI: BankInterbank):
        self.id = 1
        self.BB = BB
        self.BI = BI
        pass

    pass
