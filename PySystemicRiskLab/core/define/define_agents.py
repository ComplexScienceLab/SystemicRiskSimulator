"结构体：定义各类Agents，基于模式3-1"

## 程序：定义各类Agents，基于模式3-1

##########################################
# 状态/使用
##########################################

from PySystemicRiskLab.core.define.define_environment_variables import env
from PySystemicRiskLab.core.define.define_type import *

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
    id = np.NaN  # = np.arange(1, env['num_bank'] + 1, step=1)
    abbr = np.NaN  # = np.full(env['num_bank'], "")
    name = np.NaN  # = np.full(env['num_bank'], "")
    A_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总资产 A_all: $A_all=A_BI+A_exBI$
    A_BI_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间资产加总 A_BI_all
    A_exBI = np.NaN  # = np.zeros((env['num_bank'], 1))  # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
    A_P = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行贷款给生产部门之资产（非流动性资产） A_P
    A_Q = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行持有超额准备金（流动性资产） A_Q
    A_R = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行持有法定准备金（非流动性资产） A_R
    A_other = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行持有的其它资产（非流动性资产） A_other
    Z_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
    Z_BI_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间负债加总 Z_BI_all
    Z_exBI = np.NaN  # = np.zeros((env['num_bank'], 1))  # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
    Z_D = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行获得居民部门存款（非流动性负债） Z_D
    Z_other = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行持有的其他负债（非流动性负债） Z_other
    E_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 所有者权益 E_all
    T_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
    Lo_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
    Lo_BI_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间贷款流出 Lo_BI_all
    Lo_exBI = np.NaN  # = np.zeros((env['num_bank'], 1))  # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
    Lo_P = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行贷款流出给生产部门 Lo_P
    Li_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
    Li_BI_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间贷款流入 Li_BI_all
    Li_exBI = np.NaN  # = np.zeros((env['num_bank'], 1))  # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
    Li_P = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行贷款流入从生产部门 Li_P
    Bi_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
    Bi_BI_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间借款流入 Bi_BI_all
    Bi_exBI = np.NaN  # = np.zeros((env['num_bank'], 1))  # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
    Bi_D = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行借款流入从居民部门 Bi_D
    Bo_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
    Bo_BI_all = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间借款流出 Bo_BI_all
    Bo_exBI = np.NaN  # = np.zeros((env['num_bank'], 1))  # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
    Bo_D = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行借款流出给居民部门 Bo_D
    Shock_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
    Shock_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
    Shock_def_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_P_def_t+Shock_D_run_t$
    Shock_def_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
    Shock_run_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
    Shock_run_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
    Shock_exBI_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
    Shock_exBI_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
    Shock_P_run_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
    Shock_P_def_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
    Shock_D_def_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行存款违约损失冲击源头 Shock_D_def_s
    Shock_D_run_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行存款挤兑流动冲击目标 Shock_D_run_t
    Shock_B = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
    Shock_B_A = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行内资产负债之银行间资产端冲击 Shock_B_A
    Shock_B_Z = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
    Shock_BI_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
    Shock_BI_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
    Shock_BI_def_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间违约损失冲击源头 Shock_BI_def_s
    Shock_BI_def_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间违约损失冲击目标 Shock_BI_def_t
    Shock_BI_run_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
    Shock_BI_run_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
    Shock_BI_run_ilq_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
    Shock_BI_run_ilq_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
    Shock_BI_run_br_s = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
    Shock_BI_run_br_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
    Loss_BI = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间市场冲击损失 Loss_BI
    Loss_BI_def_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间资产负债违约冲击损失 Loss_BI_def_t
    Loss_BI_run_t = np.NaN  # = np.zeros((env['num_bank'], 1))  # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
    on = np.NaN  # = np.full((env['num_bank'], 1), True)  # 示性向量之于银行是否存在 isOn
    off = np.NaN  # = np.full((env['num_bank'], 1), False)  # 示性向量之于银行是否已退出不存在 isOff
    hel = np.NaN  # = np.full((env['num_bank'], 1), True)  # 示性向量之于银行是否健康 isHealthy
    isv = np.NaN  # = np.full((env['num_bank'], 1), False)  # 示性向量之于银行是否资不抵债 isInsolvent
    ilq = np.NaN  # = np.full((env['num_bank'], 1), False)  # 示性向量之于银行是否流动性短缺 isIlliquity
    br = np.NaN  # = np.full((env['num_bank'], 1), False)  # 示性向量之于银行是否破产 isBankrupt
    nBoBI = np.NaN  # = np.full((env['num_bank'], 1), False)  # 示性向量之于银行是否需要偿还银行间借款 isNeededBoBI
    eBoBI = np.NaN  # = np.full((env['num_bank'], 1), True)  # 示性向量之于银行是否可以偿还银行间借款 isEnabledBoBI
    nBoD = np.NaN  # = np.full((env['num_bank'], 1), False)  # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
    eBoD = np.NaN  # = np.full((env['num_bank'], 1), True)  # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
    nLiP = np.NaN  # = np.full((env['num_bank'], 1), False)  # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
    eLiP = np.NaN  # = np.full((env['num_bank'], 1), True)  # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP
    isAllocatedShock = np.NaN  # = np.full((env['num_bank'], 1), False)  # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
    listOfExist = np.NaN  # = np.full((env['num_bank'], 1), list)  # 列表之于存在的银行编号 listOfExist
    listOfInsolvent = np.NaN  # = np.full((env['num_bank'], 1), list)  # 列表之于资不抵债的银行编号 listOfInsolvent
    listOfIlliquity = np.NaN  # = np.full((env['num_bank'], 1), list)  # 列表之于流动性短缺的银行编号 listOfIlliquity
    listOfBankrupt = np.NaN  # = np.full((env['num_bank'], 1), list)  # 列表之于破产的银行编号 listOfBankrupt

    # id = np.arange(1, env['num_bank'] + 1, step=1)
    # abbr = np.full(env['num_bank'], "")
    # name = np.full(env['num_bank'], "")
    # A_all = np.zeros((env['num_bank']))  # 总资产 A_all: $A_all=A_BI+A_exBI$
    # A_BI_all = np.zeros((env['num_bank']))  # 银行间资产加总 A_BI_all
    # A_exBI = np.zeros((env['num_bank']))  # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
    # A_P = np.zeros((env['num_bank']))  # 银行贷款给生产部门之资产（非流动性资产） A_P
    # A_Q = np.zeros((env['num_bank']))  # 银行持有超额准备金（流动性资产） A_Q
    # A_R = np.zeros((env['num_bank']))  # 银行持有法定准备金（非流动性资产） A_R
    # A_other = np.zeros((env['num_bank']))  # 银行持有的其它资产（非流动性资产） A_other
    # Z_all = np.zeros((env['num_bank']))  # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
    # Z_BI_all = np.zeros((env['num_bank']))  # 银行间负债加总 Z_BI_all
    # Z_exBI = np.zeros((env['num_bank']))  # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
    # Z_D = np.zeros((env['num_bank']))  # 银行获得居民部门存款（非流动性负债） Z_D
    # Z_other = np.zeros((env['num_bank']))  # 银行持有的其他负债（非流动性负债） Z_other
    # E_all = np.zeros((env['num_bank']))  # 所有者权益 E_all
    # T_all = np.zeros((env['num_bank']))  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
    # Lo_all = np.zeros((env['num_bank']))  # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
    # Lo_BI_all = np.zeros((env['num_bank']))  # 银行间贷款流出 Lo_BI_all
    # Lo_exBI = np.zeros((env['num_bank']))  # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
    # Lo_P = np.zeros((env['num_bank']))  # 银行贷款流出给生产部门 Lo_P
    # Li_all = np.zeros((env['num_bank']))  # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
    # Li_BI_all = np.zeros((env['num_bank']))  # 银行间贷款流入 Li_BI_all
    # Li_exBI = np.zeros((env['num_bank']))  # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
    # Li_P = np.zeros((env['num_bank']))  # 银行贷款流入从生产部门 Li_P
    # Bi_all = np.zeros((env['num_bank']))  # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
    # Bi_BI_all = np.zeros((env['num_bank']))  # 银行间借款流入 Bi_BI_all
    # Bi_exBI = np.zeros((env['num_bank']))  # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
    # Bi_D = np.zeros((env['num_bank']))  # 银行借款流入从居民部门 Bi_D
    # Bo_all = np.zeros((env['num_bank']))  # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
    # Bo_BI_all = np.zeros((env['num_bank']))  # 银行间借款流出 Bo_BI_all
    # Bo_exBI = np.zeros((env['num_bank']))  # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
    # Bo_D = np.zeros((env['num_bank']))  # 银行借款流出给居民部门 Bo_D
    # Shock_t = np.zeros((env['num_bank']))  # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
    # Shock_s = np.zeros((env['num_bank']))  # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
    # Shock_def_t = np.zeros((env['num_bank']))  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_P_def_t+Shock_D_run_t$
    # Shock_def_s = np.zeros((env['num_bank']))  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
    # Shock_run_t = np.zeros((env['num_bank']))  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
    # Shock_run_s = np.zeros((env['num_bank']))  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
    # Shock_exBI_t = np.zeros((env['num_bank']))  # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
    # Shock_exBI_s = np.zeros((env['num_bank']))  # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
    # Shock_P_run_s = np.zeros((env['num_bank']))  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
    # Shock_P_def_t = np.zeros((env['num_bank']))  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
    # Shock_D_def_s = np.zeros((env['num_bank']))  # 银行存款违约损失冲击源头 Shock_D_def_s
    # Shock_D_run_t = np.zeros((env['num_bank']))  # 银行存款挤兑流动冲击目标 Shock_D_run_t
    # Shock_B = np.zeros((env['num_bank']))  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
    # Shock_B_A = np.zeros((env['num_bank']))  # 银行内资产负债之银行间资产端冲击 Shock_B_A
    # Shock_B_Z = np.zeros((env['num_bank']))  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
    # Shock_BI_s = np.zeros((env['num_bank']))  # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
    # Shock_BI_t = np.zeros((env['num_bank']))  # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
    # Shock_BI_def_s = np.zeros((env['num_bank']))  # 银行间违约损失冲击源头 Shock_BI_def_s
    # Shock_BI_def_t = np.zeros((env['num_bank']))  # 银行间违约损失冲击目标 Shock_BI_def_t
    # Shock_BI_run_s = np.zeros((env['num_bank']))  # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
    # Shock_BI_run_t = np.zeros((env['num_bank']))  # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
    # Shock_BI_run_ilq_s = np.zeros((env['num_bank']))  # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
    # Shock_BI_run_ilq_t = np.zeros((env['num_bank']))  # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
    # Shock_BI_run_br_s = np.zeros((env['num_bank']))  # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
    # Shock_BI_run_br_t = np.zeros((env['num_bank']))  # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
    # Loss_BI = np.zeros((env['num_bank']))  # 银行间市场冲击损失 Loss_BI
    # Loss_BI_def_t = np.zeros((env['num_bank']))  # 银行间资产负债违约冲击损失 Loss_BI_def_t
    # Loss_BI_run_t = np.zeros((env['num_bank']))  # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
    # on = np.full(env['num_bank'], True)  # 示性向量之于银行是否存在 isOn
    # off = np.full(env['num_bank'], False)  # 示性向量之于银行是否已退出不存在 isOff
    # hel = np.full(env['num_bank'], True)  # 示性向量之于银行是否健康 isHealthy
    # isv = np.full(env['num_bank'], False)  # 示性向量之于银行是否资不抵债 isInsolvent
    # ilq = np.full(env['num_bank'], False)  # 示性向量之于银行是否流动性短缺 isIlliquity
    # br = np.full(env['num_bank'], False)  # 示性向量之于银行是否破产 isBankrupt
    # nBoBI = np.full(env['num_bank'], False)  # 示性向量之于银行是否需要偿还银行间借款 isNeededBoBI
    # eBoBI = np.full(env['num_bank'], True)  # 示性向量之于银行是否可以偿还银行间借款 isEnabledBoBI
    # nBoD = np.full(env['num_bank'], False)  # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
    # eBoD = np.full(env['num_bank'], True)  # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
    # nLiP = np.full(env['num_bank'], False)  # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
    # eLiP = np.full(env['num_bank'], True)  # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP
    # isAllocatedShock = np.full(env['num_bank'], False)  # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
    # listOfExist = np.full(env['num_bank'], list)  # 列表之于存在的银行编号 listOfExist
    # listOfInsolvent = np.full(env['num_bank'], list)  # 列表之于资不抵债的银行编号 listOfInsolvent
    # listOfIlliquity = np.full(env['num_bank'], list)  # 列表之于流动性短缺的银行编号 listOfIlliquity
    # listOfBankrupt = np.full(env['num_bank'], list)  # 列表之于破产的银行编号 listOfBankrupt

    # TODO 补充损失变量；
    # TODO 增加监管约束之状态；

    # @classmethod
    def __init__(self, *args, **kwargs):
        for index, key in enumerate(self.__dir__()):
            if not key.startswith('__'):
                setattr(self, key, kwargs[key])
                pass
            pass
        pass  # function

    pass  # class


# class BankInterbank:
class BankInterbank(BaseInterAgents):
    """
    银行间邻接矩阵复合类
    """
    id = np.arange(1, env['num_bank'] * env['num_bank'] + 1).reshape((env['num_bank'], env['num_bank']))  # 编号
    A_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间资产邻接矩阵 A_BI
    Z_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间负债邻接矩阵 Z_BI
    Lo_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间贷款流出邻接矩阵 Lo_BI
    Li_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间贷款流入邻接矩阵 Li_BI
    Bo_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间借款流入邻接矩阵 Bo_BI
    Bi_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间借款流出邻接矩阵 Bi_BI
    Shock_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间冲击 Shock_BI: $Shock_BI=Shock_BI_def+Shock_BI_run$
    Shock_BI_def = np.zeros((env['num_bank'], env['num_bank']))  # 银行间违约损失冲击 Shock_BI_def
    Shock_BI_run = np.zeros((env['num_bank'], env['num_bank']))  # 银行间挤兑流动冲击 Shock_BI_run: $Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
    Shock_BI_run_ilq = np.zeros((env['num_bank'], env['num_bank']))  # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
    Shock_BI_run_br = np.zeros((env['num_bank'], env['num_bank']))  # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
    Loss_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间市场冲击损失 Loss_BI
    Loss_BI_def = np.zeros((env['num_bank'], env['num_bank']))  # 银行间资产负债违约冲击损失 Loss_BI_def
    Loss_BI_run = np.full((env['num_bank'], env['num_bank']), True)  # 银行间负债流动性挤兑冲击损失 Loss_BI_run
    isExposure = np.full((env['num_bank'], env['num_bank']), False)  # 信息邻接矩阵之于是否有银行间敞口 isExposure
    on = np.full((env['num_bank'], env['num_bank']), True)  # 信息邻接矩阵之于银行间存在的 isOn
    off = np.full((env['num_bank'], env['num_bank']), False)  # 信息邻接矩阵之于银行间已退出不存在的 isOff
    hel = np.full((env['num_bank'], env['num_bank']), False)  # 信息邻接矩阵之于银行间健康的 isHealthy
    isv = np.full((env['num_bank'], env['num_bank']), False)  # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
    ilq = np.array([])  # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
    br = np.array([])  # 信息邻接矩阵之于银行间破产的 isBankrupt
    cre = np.array([])  # 信息列表之于各银行之债权方银行编号 listOfCreditors
    deb = np.array([])  # 信息列表之于各银行之债务方银行编号 listOfDebtors
    cre_isv = []  # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
    deb_isv = []  # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
    cre_ilq = []  # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
    deb_ilq = []  # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
    cre_br = []  # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
    deb_br = []  # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt

    # id = np.arange(1, env['num_bank'] * env['num_bank'] + 1).reshape((env['num_bank'], env['num_bank']))  # 编号
    # A_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间资产邻接矩阵 A_BI
    # Z_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间负债邻接矩阵 Z_BI
    # Lo_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间贷款流出邻接矩阵 Lo_BI
    # Li_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间贷款流入邻接矩阵 Li_BI
    # Bo_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间借款流入邻接矩阵 Bo_BI
    # Bi_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间借款流出邻接矩阵 Bi_BI
    # Shock_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间冲击 Shock_BI: $Shock_BI=Shock_BI_def+Shock_BI_run$
    # Shock_BI_def = np.zeros((env['num_bank'], env['num_bank']))  # 银行间违约损失冲击 Shock_BI_def
    # Shock_BI_run = np.zeros((env['num_bank'], env['num_bank']))  # 银行间挤兑流动冲击 Shock_BI_run: $Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
    # Shock_BI_run_ilq = np.zeros((env['num_bank'], env['num_bank']))  # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
    # Shock_BI_run_br = np.zeros((env['num_bank'], env['num_bank']))  # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
    # Loss_BI = np.zeros((env['num_bank'], env['num_bank']))  # 银行间市场冲击损失 Loss_BI
    # Loss_BI_def = np.zeros((env['num_bank'], env['num_bank']))  # 银行间资产负债违约冲击损失 Loss_BI_def
    # Loss_BI_run = np.full((env['num_bank'], env['num_bank']), True)  # 银行间负债流动性挤兑冲击损失 Loss_BI_run
    # isExposure = np.full((env['num_bank'], env['num_bank']), False)  # 信息邻接矩阵之于是否有银行间敞口 isExposure
    # on = np.full((env['num_bank'], env['num_bank']), True)  # 信息邻接矩阵之于银行间存在的 isOn
    # off = np.full((env['num_bank'], env['num_bank']), False)  # 信息邻接矩阵之于银行间已退出不存在的 isOff
    # hel = np.full((env['num_bank'], env['num_bank']), False)  # 信息邻接矩阵之于银行间健康的 isHealthy
    # isv = np.full((env['num_bank'], env['num_bank']), False)  # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
    # ilq = np.array([])  # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
    # br = np.array([])  # 信息邻接矩阵之于银行间破产的 isBankrupt
    # cre = np.array([])  # 信息列表之于各银行之债权方银行编号 listOfCreditors
    # deb = np.array([])  # 信息列表之于各银行之债务方银行编号 listOfDebtors
    # cre_isv = []  # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
    # deb_isv = []  # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
    # cre_ilq = []  # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
    # deb_ilq = []  # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
    # cre_br = []  # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
    # deb_br = []  # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt

    # @classmethod
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
    id: int  # 编号（必备的）
    BB: BankCommercial  # 商业银行群
    BI: BankInterbank  # 银行间邻接矩阵

    # @classmethod
    def __init__(self, id, BB: BankCommercial, BI: BankInterbank):
        self.id = id
        self.BB = BB
        self.BI = BI
        pass

    pass


if __name__ == "__main__":
    # bankCommercial = BankCommercial()
    # interbankCommercial = BankInterbank()
    bankCommercial = BankCommercial(
        id=np.arange(1, env['num_bank'] + 1, step=1),  # 编号 id
        abbr=np.array(["1", "2", "3", "4", "5"]),  # 缩写 abbr
        name=np.array(["BK1", "BK2", "BK3", "BK4", "BK5"]),  # 全名 name
        A_all=np.zeros((env['num_bank'], 1)),  # 总资产 A_all: $A_all=A_BI+A_exBI$
        A_BI_all=np.array([[2185.24, 398.37, 730.99, 1357.75, 2717.39]]),  # 银行间资产加总 A_BI_all
        A_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
        A_P=np.array([[1631.73, 4303.24, 3379.72, 4351.47, 620.69]]),  # 银行贷款给生产部门之资产（非流动性资产） A_P
        A_Q=np.array([[477.125, 587.693, 513.847, 713.662, 417.257]]),  # 银行持有超额准备金（流动性资产） A_Q
        A_R=np.zeros((env['num_bank'], 1)),  # 银行持有法定准备金（非流动性资产） A_R
        A_other=np.zeros(env['num_bank']),  # 银行持有的其它资产（非流动性资产） A_other
        Z_all=np.zeros((env['num_bank'], 1)),  # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
        Z_BI_all=np.array([[959.6, 1844.24, 1253.34, 2851.85, 480.71]]),  # 银行间负债加总 Z_BI_all
        Z_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
        Z_D=np.array([[3160.99, 3231.37, 3184.36, 3311.51, 3122.9]]),  # 银行获得居民部门存款（非流动性负债） Z_D
        Z_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其他负债（非流动性负债） Z_other
        E_all=np.array([[216.83, 267.13, 233.56, 324.39, 189.66]]),  # 所有者权益 E_all
        T_all=np.zeros((env['num_bank'], 1)),  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
        Lo_all=np.zeros((env['num_bank'], 1)),  # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
        Lo_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流出 Lo_BI_all
        Lo_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
        Lo_P=np.zeros((env['num_bank'], 1)),  # 银行贷款流出给生产部门 Lo_P
        Li_all=np.zeros((env['num_bank'], 1)),  # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
        Li_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流入 Li_BI_all
        Li_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
        Li_P=np.zeros((env['num_bank'], 1)),  # 银行贷款流入从生产部门 Li_P
        Bi_all=np.zeros((env['num_bank'], 1)),  # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
        Bi_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流入 Bi_BI_all
        Bi_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
        Bi_D=np.zeros((env['num_bank'], 1)),  # 银行借款流入从居民部门 Bi_D
        Bo_all=np.zeros((env['num_bank'], 1)),  # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
        Bo_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流出 Bo_BI_all
        Bo_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
        Bo_D=np.zeros((env['num_bank'], 1)),  # 银行借款流出给居民部门 Bo_D
        Shock_t=np.zeros((env['num_bank'], 1)),  # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
        Shock_s=np.zeros((env['num_bank'], 1)),  # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
        Shock_def_t=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exBI_def_t+Shock_BI_def_t$
        Shock_def_s=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
        Shock_run_t=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
        Shock_run_s=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
        Shock_exBI_t=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
        Shock_exBI_s=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
        Shock_P_run_s=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
        Shock_P_def_t=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
        Shock_D_def_s=np.zeros((env['num_bank'], 1)),  # 银行存款违约损失冲击源头 Shock_D_def_s
        Shock_D_run_t=np.zeros((env['num_bank'], 1)),  # 银行存款挤兑流动冲击目标 Shock_D_run_t
        Shock_B=np.zeros((env['num_bank'], 1)),  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
        Shock_B_A=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间资产端冲击 Shock_B_A
        Shock_B_Z=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
        Shock_BI_s=np.zeros((env['num_bank'], 1)),  # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
        Shock_BI_t=np.zeros((env['num_bank'], 1)),  # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
        Shock_BI_def_s=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击源头 Shock_BI_def_s
        Shock_BI_def_t=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击目标 Shock_BI_def_t
        Shock_BI_run_s=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
        Shock_BI_run_t=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
        Shock_BI_run_ilq_s=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
        Shock_BI_run_ilq_t=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
        Shock_BI_run_br_s=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
        Shock_BI_run_br_t=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
        Loss_BI=np.zeros((env['num_bank'], 1)),  # 银行间市场冲击损失 Loss_BI
        Loss_BI_def_t=np.zeros((env['num_bank'], 1)),  # 银行间资产负债违约冲击损失 Loss_BI_def_t
        Loss_BI_run_t=np.zeros((env['num_bank'], 1)),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
        on=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否存在 isOn
        off=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已退出不存在 isOff
        hel=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否健康 isHealthy
        isv=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否资不抵债 isInsolvent
        ilq=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否流动性短缺 isIlliquity
        br=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否破产 isBankrupt
        nBoBI=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还借款 isNeededBoBI
        eBoBI=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还借款 isEnabledBoBI
        nBoD=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
        eBoD=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
        nLiP=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
        eLiP=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP
        isAllocatedShock=np.full(env['num_bank'], False),  # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
        listOfExist=np.full(env['num_bank'], list),  # 列表之于存在的银行编号 listOfExist
        listOfInsolvent=np.full(env['num_bank'], list),  # 列表之于资不抵债的银行编号 listOfInsolvent
        listOfIlliquity=np.full(env['num_bank'], list),  # 列表之于流动性短缺的银行编号 listOnp.fulliquity
        listOfBankrupt=np.full(env['num_bank'], list)  # 列表之于破产的银行编号 listOfBankrupt
    )

    ## 初始化银行间邻接矩阵
    bankInterbank = BankInterbank(
        id=np.arange(1, env['num_bank'] * env['num_bank'] + 1).reshape((env['num_bank'], env['num_bank'])),  # 编号
        A_BI=np.array([[0, 1728.55, 0, 134.46, 322.23], [109.35, 0, 289.02, 0, 0], [730.99, 0, 0, 0, 0], [119.26, 115.69, 964.32, 0, 158.48], [0, 0, 0, 2717.39, 0]]),  # 银行间资产邻接矩阵 A_BI
        Z_BI=np.array([[0, 1728.55, 0, 134.46, 322.23], [109.35, 0, 289.02, 0, 0], [730.99, 0, 0, 0, 0], [119.26, 115.69, 964.32, 0, 158.48], [0, 0, 0, 2717.39, 0]]).T,  # 银行间负债邻接矩阵 Z_BI
        Lo_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流出邻接矩阵 Lo_BI
        Li_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流入邻接矩阵 Li_BI
        Bo_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流入邻接矩阵 Bo_BI
        Bi_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流出邻接矩阵 Bi_BI
        Shock_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间冲击 Shock_BI: $Shock_BI=Shock_BI_def+Shock_BI_run$
        Shock_BI_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间违约损失冲击 Shock_BI_def
        Shock_BI_run=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间挤兑流动冲击 Shock_BI_run: $Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
        Shock_BI_run_ilq=np.zeros((env['num_bank'], env['num_bank'])),  # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
        Shock_BI_run_br=np.zeros((env['num_bank'], env['num_bank'])),  # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
        Loss_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间市场冲击损失 Loss_BI
        Loss_BI_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产负债违约冲击损失 Loss_BI_def
        Loss_BI_run=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run
        isExposure=np.zeros((env['num_bank'], env['num_bank'])),  # 信息邻接矩阵之于是否有银行间敞口 isExposure
        on=np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间存在的 isOn
        off=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间已退出不存在的 isOff
        hel=np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间健康的 isHealthy
        isv=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
        ilq=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
        br=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间破产的 isBankrupt
        cre=[],  # 信息列表之于各银行之债权方银行编号 listOfCreditors
        deb=[],  # 信息列表之于各银行之债务方银行编号 listOfDebtors
        cre_isv=[],  # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
        deb_isv=[],  # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
        cre_ilq=[],  # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
        deb_ilq=[],  # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
        cre_br=[],  # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
        deb_br=[],  # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt
    )

    print(bankCommercial)
    print(bankInterbank)
