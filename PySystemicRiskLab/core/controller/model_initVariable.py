##########################################
# 状态/扩展
##########################################

# from PySystemicRiskLab.core import np, env, BankCommercial, BankInterbank, AgentDataCollection
import logging

from PySystemicRiskLab import np
from PySystemicRiskLab.core.controller.model_collector import ModelCollector
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_agents import SystemicRiskAgent
from PySystemicRiskLab.core.define.define_type import *
# from PySystemicRiskLab.models.models.model_content import *
from PySystemicRiskLab.core.define.define_agentsVariables import bankCommercial_dict, bankInterbank_dict
from PySystemicRiskLab.core.define.define_environment_variables import env
from PySystemicRiskLab.core.functions.fun_balanceSheet import BalanceSheet
from PySystemicRiskLab.core.functions.fun_shock import Shock
from PySystemicRiskLab.core.functions.fun_state import BankState

pass  # end import


class ModelInitVariable:
    """
    初始化模型之变量
    """

    A_data = AgentDataCollection([], [])

    # @property
    @classmethod
    def set_default_values_to_B_variables(cls):
        bank: BankCommercial = BankCommercial(
            id_agent=np.arange(1, env['num_bank'], step=1),  # agent 之编号 id
            abbr=np.full((env['num_bank'], 1), ""),  # 缩写 abbr
            name=np.full((env['num_bank'], 1), ""),  # 全名 name
            A_all=np.zeros((env['num_bank'], 1)),  # 总资产 A_all: $A_all=A_BI+A_exBI$
            A_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间资产加总 A_BI_all
            A_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
            A_P=np.zeros((env['num_bank'], 1)),  # 银行贷款给生产部门之资产（非流动性资产） A_P
            A_Q=np.zeros((env['num_bank'], 1)),  # 银行持有超额准备金（流动性资产） A_Q
            A_R=np.zeros((env['num_bank'], 1)),  # 银行持有法定准备金（非流动性资产） A_R
            A_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其它资产（非流动性资产） A_other
            Z_all=np.zeros((env['num_bank'], 1)),  # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
            Z_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间负债加总 Z_BI_all
            Z_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
            Z_D=np.zeros((env['num_bank'], 1)),  # 银行获得居民部门存款（非流动性负债） Z_D
            Z_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其他负债（非流动性负债） Z_other
            E_all=np.zeros((env['num_bank'], 1)),  # 所有者权益 E_all
            T_all=np.zeros((env['num_bank'], 1)),  # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
            Lo_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流出 Lo_BI_all
            Lo_BI_all=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
            Lo_exBI=np.zeros((env['num_bank'], 1)),  # 银行贷款流出给生产部门 Lo_P
            Lo_P=np.zeros((env['num_bank'], 1)),  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
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
            # FIXME 以下带注释部分，用于测试几种不同的形状之影响
            # on=np.full(env['num_bank'], True),  # 示性向量之于银行是否存在 isOn
            # off=np.full(env['num_bank'], False),  # 示性向量之于银行是否已退出不存在 isOff
            # hel=np.full(env['num_bank'], True),  # 示性向量之于银行是否健康 isHealthy
            # isv=np.full(env['num_bank'], False),  # 示性向量之于银行是否资不抵债 isInsolvent
            # ilq=np.full(env['num_bank'], False),  # 示性向量之于银行是否流动性短缺 isIlliquity
            # br=np.full(env['num_bank'], False),  # 示性向量之于银行是否破产 isBankrupt
            # nBoBI=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还借款 isNeededBoBI
            # eBoBI=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还借款 isEnabledBoBI
            # nBoD=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
            # eBoD=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
            # nLiP=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
            # eLiP=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP
            # isAllocatedShock=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
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
            isAllocatedShock=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
            listOfExist=np.full(env['num_bank'], list),  # 列表之于存在的银行编号 listOfExist
            listOfInsolvent=np.full(env['num_bank'], list),  # 列表之于资不抵债的银行编号 listOfInsolvent
            listOfIlliquity=np.full(env['num_bank'], list),  # 列表之于流动性短缺的银行编号 listOfIlliquity
            listOfBankrupt=np.full(env['num_bank'], list),  # 列表之于破产的银行编号 listOfBankrupt

            # id_agent=np.arange(1, env['num_bank'], step=1),  # agent 之编号 id
            # abbr=np.full(env['num_bank'], ""),  # 缩写 abbr
            # name=np.full(env['num_bank'], ""),  # 全名 name
            # A_all=np.zeros(env['num_bank']),  # 总资产 A_all: $A_all=A_BI+A_exBI$
            # A_BI_all=np.zeros(env['num_bank']),  # 银行间资产加总 A_BI_all
            # A_exBI=np.zeros(env['num_bank']),  # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
            # A_P=np.zeros(env['num_bank']),  # 银行贷款给生产部门之资产（非流动性资产） A_P
            # A_Q=np.zeros(env['num_bank']),  # 银行持有超额准备金（流动性资产） A_Q
            # A_R=np.zeros(env['num_bank']),  # 银行持有法定准备金（非流动性资产） A_R
            # A_other=np.zeros(env['num_bank']),  # 银行持有的其它资产（非流动性资产） A_other
            # Z_all=np.zeros(env['num_bank']),  # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
            # Z_BI_all=np.zeros(env['num_bank']),  # 银行间负债加总 Z_BI_all
            # Z_exBI=np.zeros(env['num_bank']),  # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
            # Z_D=np.zeros(env['num_bank']),  # 银行获得居民部门存款（非流动性负债） Z_D
            # Z_other=np.zeros(env['num_bank']),  # 银行持有的其他负债（非流动性负债） Z_other
            # E_all=np.zeros(env['num_bank']),  # 所有者权益 E_all
            # T_all=np.zeros(env['num_bank']),  # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
            # Lo_all=np.zeros(env['num_bank']),  # 银行间贷款流出 Lo_BI_all
            # Lo_BI_all=np.zeros(env['num_bank']),  # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
            # Lo_exBI=np.zeros(env['num_bank']),  # 银行贷款流出给生产部门 Lo_P
            # Lo_P=np.zeros(env['num_bank']),  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
            # Li_all=np.zeros(env['num_bank']),  # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
            # Li_BI_all=np.zeros(env['num_bank']),  # 银行间贷款流入 Li_BI_all
            # Li_exBI=np.zeros(env['num_bank']),  # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
            # Li_P=np.zeros(env['num_bank']),  # 银行贷款流入从生产部门 Li_P
            # Bi_all=np.zeros(env['num_bank']),  # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
            # Bi_BI_all=np.zeros(env['num_bank']),  # 银行间借款流入 Bi_BI_all
            # Bi_exBI=np.zeros(env['num_bank']),  # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
            # Bi_D=np.zeros(env['num_bank']),  # 银行借款流入从居民部门 Bi_D
            # Bo_all=np.zeros(env['num_bank']),  # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
            # Bo_BI_all=np.zeros(env['num_bank']),  # 银行间借款流出 Bo_BI_all
            # Bo_exBI=np.zeros(env['num_bank']),  # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
            # Bo_D=np.zeros(env['num_bank']),  # 银行借款流出给居民部门 Bo_D
            # Shock_t=np.zeros(env['num_bank']),  # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
            # Shock_s=np.zeros(env['num_bank']),  # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
            # Shock_def_t=np.zeros(env['num_bank']),  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exBI_def_t+Shock_BI_def_t$
            # Shock_def_s=np.zeros(env['num_bank']),  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
            # Shock_run_t=np.zeros(env['num_bank']),  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
            # Shock_run_s=np.zeros(env['num_bank']),  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
            # Shock_exBI_t=np.zeros(env['num_bank']),  # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
            # Shock_exBI_s=np.zeros(env['num_bank']),  # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
            # Shock_P_run_s=np.zeros(env['num_bank']),  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
            # Shock_P_def_t=np.zeros(env['num_bank']),  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
            # Shock_D_def_s=np.zeros(env['num_bank']),  # 银行存款违约损失冲击源头 Shock_D_def_s
            # Shock_D_run_t=np.zeros(env['num_bank']),  # 银行存款挤兑流动冲击目标 Shock_D_run_t
            # Shock_B=np.zeros(env['num_bank']),  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
            # Shock_B_A=np.zeros(env['num_bank']),  # 银行内资产负债之银行间资产端冲击 Shock_B_A
            # Shock_B_Z=np.zeros(env['num_bank']),  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
            # Shock_BI_s=np.zeros(env['num_bank']),  # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
            # Shock_BI_t=np.zeros(env['num_bank']),  # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
            # Shock_BI_def_s=np.zeros(env['num_bank']),  # 银行间违约损失冲击源头 Shock_BI_def_s
            # Shock_BI_def_t=np.zeros(env['num_bank']),  # 银行间违约损失冲击目标 Shock_BI_def_t
            # Shock_BI_run_s=np.zeros(env['num_bank']),  # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
            # Shock_BI_run_t=np.zeros(env['num_bank']),  # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
            # Shock_BI_run_ilq_s=np.zeros(env['num_bank']),  # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
            # Shock_BI_run_ilq_t=np.zeros(env['num_bank']),  # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
            # Shock_BI_run_br_s=np.zeros(env['num_bank']),  # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
            # Shock_BI_run_br_t=np.zeros(env['num_bank']),  # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
            # Loss_BI=np.zeros(env['num_bank']),  # 银行间市场冲击损失 Loss_BI
            # Loss_BI_def_t=np.zeros(env['num_bank']),  # 银行间资产负债违约冲击损失 Loss_BI_def_t
            # Loss_BI_run_t=np.zeros(env['num_bank']),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
            # on=np.full(env['num_bank'], True),  # 示性向量之于银行是否存在 isOn
            # off=np.full(env['num_bank'], False),  # 示性向量之于银行是否已退出不存在 isOff
            # hel=np.full(env['num_bank'], True),  # 示性向量之于银行是否健康 isHealthy
            # isv=np.full(env['num_bank'], False),  # 示性向量之于银行是否资不抵债 isInsolvent
            # ilq=np.full(env['num_bank'], False),  # 示性向量之于银行是否流动性短缺 isIlliquity
            # br=np.full(env['num_bank'], False),  # 示性向量之于银行是否破产 isBankrupt
            # nBoBI=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还借款 isNeededBoBI
            # eBoBI=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还借款 isEnabledBoBI
            # nBoD=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
            # eBoD=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
            # nLiP=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
            # eLiP=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP
            # isAllocatedShock=np.full(env['num_bank'], False),  # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
            # listOfExist=np.full(env['num_bank'], list),  # 列表之于存在的银行编号 listOfExist
            # listOfInsolvent=np.full(env['num_bank'], list),  # 列表之于资不抵债的银行编号 listOfInsolvent
            # listOfIlliquity=np.full(env['num_bank'], list),  # 列表之于流动性短缺的银行编号 listOfIlliquity
            # listOfBankrupt=np.full(env['num_bank'], list),  # 列表之于破产的银行编号 listOfBankrupt
        )

        interbank: BankInterbank = BankInterbank(
            id_agent=np.array(np.arange(1, env['num_bank'] * env['num_bank'] + 1).reshape((env['num_bank'], env['num_bank'])),dtype=TypeIds),  # agent 之间之关联编号 id
            A_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产邻接矩阵 A_BI
            Z_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间负债邻接矩阵 Z_BI
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
            Loss_BI_run=np.full((env['num_bank'], env['num_bank']), True),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run
            isExposure=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于是否有银行间敞口 isExposure
            on=np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间存在的 isOn
            off=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间已退出不存在的 isOff
            hel=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间健康的 isHealthy
            isv=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
            ilq=np.array([]),  # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
            br=np.array([]),  # 信息邻接矩阵之于银行间破产的 isBankrupt
            cre=np.array([]),  # 信息列表之于各银行之债权方银行编号 listOfCreditors
            deb=np.array([]),  # 信息列表之于各银行之债务方银行编号 listOfDebtors
            cre_isv=[],  # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
            deb_isv=[],  # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
            cre_ilq=[],  # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
            deb_ilq=[],  # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
            cre_br=[],  # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
            deb_br=[],  # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt
        )

        return bank, interbank
        pass  # fun

    @classmethod
    def set_randomly_values_to_Bank_variables(cls):
        # TODO """随机化初始化银行变量"""
        bank, interbank = cls.set_default_values_to_B_variables()
        pass

        pass

    @classmethod
    def set_imported_values_to_Bank_variables(cls):
        # TODO """导入数据以初始化银行变量"""
        bank, interbank = cls.set_default_values_to_B_variables
        pass

    @classmethod
    def set_manually_values_to_Bank_variables(cls):
        """手动设置以初始化银行变量"""  # FIXME 须提取手动初始化方式为单独的方式
        bank, interbank = cls.set_default_values_to_B_variables()

        bank.__dict__.update(bankCommercial_dict)
        interbank.__dict__.update(bankInterbank_dict)

        # ## 初始化商业银行群
        # bank: BankCommercial = BankCommercial(
        #     id_agent=np.arange(1, env['num_bank'] + 1, step=1),  # agent 之间之关联编号 id
        #     abbr=np.array(["1", "2", "3", "4", "5"]),  # 缩写 abbr
        #     name=np.array(["BK1", "BK2", "BK3", "BK4", "BK5"]),  # 全名 name
        #     A_all=np.zeros((env['num_bank'], 1)),  # 总资产 A_all: $A_all=A_BI+A_exBI$
        #     A_BI_all=np.array([[2185.24, 398.37, 730.99, 1357.75, 2717.39]]),  # 银行间资产加总 A_BI_all
        #     A_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间资产 A_exBI: $A_exBI=A_P+A_Q+A_R+A_other$
        #     A_P=np.array([[1631.73, 4303.24, 3379.72, 4351.47, 620.69]]),  # 银行贷款给生产部门之资产（非流动性资产） A_P
        #     A_Q=np.array([[477.125, 587.693, 513.847, 713.662, 417.257]]),  # 银行持有超额准备金（流动性资产） A_Q
        #     A_R=np.zeros((env['num_bank'], 1)),  # 银行持有法定准备金（非流动性资产） A_R
        #     A_other=np.zeros(env['num_bank']),  # 银行持有的其它资产（非流动性资产） A_other
        #     Z_all=np.zeros((env['num_bank'], 1)),  # 总负债 Z_all: $Z_total=Z_BI+Z_exBI$
        #     Z_BI_all=np.array([[959.6, 1844.24, 1253.34, 2851.85, 480.71]]),  # 银行间负债加总 Z_BI_all
        #     Z_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间负债 Z_exBI: $Z_exBI=Z_D+Z_other$
        #     Z_D=np.array([[3160.99, 3231.37, 3184.36, 3311.51, 3122.9]]),  # 银行获得居民部门存款（非流动性负债） Z_D
        #     Z_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其他负债（非流动性负债） Z_other
        #     E_all=np.array([[216.83, 267.13, 233.56, 324.39, 189.66]]),  # 所有者权益 E_all
        #     T_all=np.zeros((env['num_bank'], 1)),  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
        #     Lo_all=np.zeros((env['num_bank'], 1)),  # 总贷款流出 Lo_all: $Lo_all=Lo_BI_all+Lo_exBI$
        #     Lo_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流出 Lo_BI_all
        #     Lo_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流出 Lo_exBI: $Lo_exBI=Lo_P$
        #     Lo_P=np.zeros((env['num_bank'], 1)),  # 银行贷款流出给生产部门 Lo_P
        #     Li_all=np.zeros((env['num_bank'], 1)),  # 总贷款流入 Li_all: $Li_all=Li_BI_all+Li_exBI$
        #     Li_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流入 Li_BI_all
        #     Li_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流入 Li_exBI: $Li_exBI=Li_D$
        #     Li_P=np.zeros((env['num_bank'], 1)),  # 银行贷款流入从生产部门 Li_P
        #     Bi_all=np.zeros((env['num_bank'], 1)),  # 总借款流入 Bi_all: $Bi_all=Bi_BI_all+Bi_exBI$
        #     Bi_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流入 Bi_BI_all
        #     Bi_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间借款流入 Bi_exBI: $Bi_exBI=Bi_D$
        #     Bi_D=np.zeros((env['num_bank'], 1)),  # 银行借款流入从居民部门 Bi_D
        #     Bo_all=np.zeros((env['num_bank'], 1)),  # 总借款流出 Bo_all: $Bo_all=Bo_BI_all+Bo_exBI$
        #     Bo_BI_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流出 Bo_BI_all
        #     Bo_exBI=np.zeros((env['num_bank'], 1)),  # 非银行间借款流出 Bo_exBI: $Bo_exBI=Bo_P$
        #     Bo_D=np.zeros((env['num_bank'], 1)),  # 银行借款流出给居民部门 Bo_D
        #     Shock_t=np.zeros((env['num_bank'], 1)),  # 总冲击目标 Shock_t $Shock_t = Shock_exBI_t+Shock_BI_t$
        #     Shock_s=np.zeros((env['num_bank'], 1)),  # 总冲击源头 Shock_s $Shock_s = Shock_exBI_s+Shock_BI_s$
        #     Shock_def_t=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exBI_def_t+Shock_BI_def_t$
        #     Shock_def_s=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exBI_def_s+Shock_BI_def_s$
        #     Shock_run_t=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exBI_run_t+Shock_BI_run_t$
        #     Shock_run_s=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exBI_run_s+Shock_BI_run_s$
        #     Shock_exBI_t=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击目标 Shock_exBI_t $Shock_exBI_t = Shock_P_def_t+Shock_D_run_t$
        #     Shock_exBI_s=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击源头 Shock_exBI_s $Shock_exBI_s = Shock_P_run_s+Shock_D_def_s$
        #     Shock_P_run_s=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
        #     Shock_P_def_t=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
        #     Shock_D_def_s=np.zeros((env['num_bank'], 1)),  # 银行存款违约损失冲击源头 Shock_D_def_s
        #     Shock_D_run_t=np.zeros((env['num_bank'], 1)),  # 银行存款挤兑流动冲击目标 Shock_D_run_t
        #     Shock_B=np.zeros((env['num_bank'], 1)),  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
        #     Shock_B_A=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间资产端冲击 Shock_B_A
        #     Shock_B_Z=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
        #     Shock_BI_s=np.zeros((env['num_bank'], 1)),  # 银行间冲击源头 Shock_BI_s $Shock_BI_s=Shock_BI_def_s+Shock_BI_run_s$
        #     Shock_BI_t=np.zeros((env['num_bank'], 1)),  # 银行间冲击目标 Shock_BI_t $Shock_BI_t=Shock_BI_def_t+Shock_BI_run_t$
        #     Shock_BI_def_s=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击源头 Shock_BI_def_s
        #     Shock_BI_def_t=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击目标 Shock_BI_def_t
        #     Shock_BI_run_s=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击源头 Shock_BI_run_s $Shock_BI_run_s=Shock_BI_run_ilq_s+Shock_BI_run_br_s$
        #     Shock_BI_run_t=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击目标 Shock_BI_run_t $Shock_BI_run_t+Shock_BI_run_ilq_t+Shock_BI_run_br_t$
        #     Shock_BI_run_ilq_s=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击源头 Shock_BI_run_ilq_s
        #     Shock_BI_run_ilq_t=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击目标 Shock_BI_run_ilq_t
        #     Shock_BI_run_br_s=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击源头 Shock_BI_run_br_s
        #     Shock_BI_run_br_t=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击目标 Shock_BI_run_br_t
        #     Loss_BI=np.zeros((env['num_bank'], 1)),  # 银行间市场冲击损失 Loss_BI
        #     Loss_BI_def_t=np.zeros((env['num_bank'], 1)),  # 银行间资产负债违约冲击损失 Loss_BI_def_t
        #     Loss_BI_run_t=np.zeros((env['num_bank'], 1)),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run_t
        #     on=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否存在 isOn
        #     off=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已退出不存在 isOff
        #     hel=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否健康 isHealthy
        #     isv=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否资不抵债 isInsolvent
        #     ilq=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否流动性短缺 isIlliquity
        #     br=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否破产 isBankrupt
        #     nBoBI=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还借款 isNeededBoBI
        #     eBoBI=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还借款 isEnabledBoBI
        #     nBoD=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还居民部门存款 isNeededBoD
        #     eBoD=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还居民部门存款 isEnabledBoD
        #     nLiP=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要收回厂商贷款 isNeededLiP
        #     eLiP=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以收回厂商贷款 isEnabledLiP
        #     isAllocatedShock=np.full(env['num_bank'], False),  # 示性向量之于银行是否已经分配传染冲击 isAllocatedShock
        #     listOfExist=np.full(env['num_bank'], list),  # 列表之于存在的银行编号 listOfExist
        #     listOfInsolvent=np.full(env['num_bank'], list),  # 列表之于资不抵债的银行编号 listOfInsolvent
        #     listOfIlliquity=np.full(env['num_bank'], list),  # 列表之于流动性短缺的银行编号 listOnp.fulliquity
        #     listOfBankrupt=np.full(env['num_bank'], list)  # 列表之于破产的银行编号 listOfBankrupt
        # )
        #
        # ## 初始化银行间邻接矩阵
        # interbank = BankInterbank(
        #     id=np.arange(1, env['num_bank'] * env['num_bank'] + 1).reshape((env['num_bank'], env['num_bank'])),  # 编号
        #     A_BI=np.array([[0, 1728.55, 0, 134.46, 322.23], [109.35, 0, 289.02, 0, 0], [730.99, 0, 0, 0, 0], [119.26, 115.69, 964.32, 0, 158.48], [0, 0, 0, 2717.39, 0]]),  # 银行间资产邻接矩阵 A_BI
        #     Z_BI=np.array([[0, 1728.55, 0, 134.46, 322.23], [109.35, 0, 289.02, 0, 0], [730.99, 0, 0, 0, 0], [119.26, 115.69, 964.32, 0, 158.48], [0, 0, 0, 2717.39, 0]]).T,  # 银行间负债邻接矩阵 Z_BI
        #     Lo_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流出邻接矩阵 Lo_BI
        #     Li_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流入邻接矩阵 Li_BI
        #     Bo_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流入邻接矩阵 Bo_BI
        #     Bi_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流出邻接矩阵 Bi_BI
        #     Shock_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间冲击 Shock_BI: $Shock_BI=Shock_BI_def+Shock_BI_run$
        #     Shock_BI_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间违约损失冲击 Shock_BI_def
        #     Shock_BI_run=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间挤兑流动冲击 Shock_BI_run: $Shock_BI_run=Shock_BI_run_ilq+Shock_BI_run_br$
        #     Shock_BI_run_ilq=np.zeros((env['num_bank'], env['num_bank'])),  # 流动性短缺银行银行间挤兑流动冲击 Shock_BI_run_ilq
        #     Shock_BI_run_br=np.zeros((env['num_bank'], env['num_bank'])),  # 破产银行银行间挤兑流动冲击 Shock_BI_run_br
        #     Loss_BI=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间市场冲击损失 Loss_BI
        #     Loss_BI_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产负债违约冲击损失 Loss_BI_def
        #     Loss_BI_run=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间负债流动性挤兑冲击损失 Loss_BI_run
        #     isExposure=np.zeros((env['num_bank'], env['num_bank'])),  # 信息邻接矩阵之于是否有银行间敞口 isExposure
        #     on=np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间存在的 isOn
        #     off=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间已退出不存在的 isOff
        #     hel=np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间健康的 isHealthy
        #     isv=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间资不抵债的 isInsolvent
        #     ilq=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间流动性短缺的 isIlliquity
        #     br=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间破产的 isBankrupt
        #     cre=[],  # 信息列表之于各银行之债权方银行编号 listOfCreditors
        #     deb=[],  # 信息列表之于各银行之债务方银行编号 listOfDebtors
        #     cre_isv=[],  # 信息列表之于资不抵债的银行之债权方银行编号 listOfCreditorsInInsolvent
        #     deb_isv=[],  # 信息列表之于资不抵债的银行之债务方银行编号 listOfDebtorsInInsolvent
        #     cre_ilq=[],  # 信息列表之于流动性短缺的银行之债权方银行编号 listOfCreditorsInIlliquity
        #     deb_ilq=[],  # 信息列表之于流动性短缺的银行之债务方银行编号 listOfDebtorsInIlliquity
        #     cre_br=[],  # 信息列表之于破产的银行之债权方银行编号 listOfCreditorsInBankrupt
        #     deb_br=[],  # 信息列表之于破产的银行之债务方银行编号 listOfDebtorsInBankrupt
        # )

        return bank, interbank
        pass  # function

    # @classmethod
    def init_B_and_BI(self, init_method: str):
        """
        不同的初始化方式。

        参数init_method可选项：

        - ``only init``:  仅单纯初始化；

        - ``randomly``:  生成随机数据以初始化；

        - ``import data``:  导入数据以初始化

        - ``manually``:  手动设置以初始化；

        Args:
            init_method ():

        Returns: A, A_data

        """

        try:
            if init_method == "only init":
                BB, BI = self.set_default_values_to_B_variables()
            elif init_method == "randomly":
                BB, BI = self.set_randomly_values_to_Bank_variables()
            elif init_method == "import data":
                BB, BI, self.A_data.BB, self.A_data.BI = self.set_imported_values_to_Bank_variables()  # 导入数据以初始化银行变量
            elif init_method == "set manually":
                BB, BI = self.set_default_values_to_B_variables()
                BB, BI = self.set_manually_values_to_Bank_variables()  # 手动设置以初始化银行变量
            else:
                pass
        except KeyError:
            logging.error("关键词" + str(init_method) + "取值错误！")

        ## 构建Agent模型
        A = SystemicRiskAgent(
            1,  # 编号（必备的）
            BB,  # 商业银行群
            BI  # 银行间邻接矩阵
        )

        # 初始化带回合变量的商业银行实例数组、初始化带回合变量的银行间市场实例数组
        A_data = AgentDataCollection([], [])
        A_data = ModelCollector.collector(A, A_data, stateOfProcess=env['state_of_process'])

        ## 更新各银行之变量，在第一回合初始时
        b = (BB.on | BB.off).reshape(-1, 1)  # 临时设置BB示性变量
        ib = ((BB.on | BB.off).reshape(-1, 1) & (BB.on | BB.off).reshape(1, -1))  # 临时设置BI示性变量
        Shock.update_B_Shock(BB, BI, b, ib, byWay="all")  # 更新各银行之所有冲击变量，在第一回合开始时
        Shock.update_B_Shock(BB, BI, b, ib, byWay="all")  # 更新各银行之所有冲击变量，在第一回合开始时
        BalanceSheet.update_B_balanceSheet(BB, BI, b, ib, byWay="all")  # 更新各银行之资产负债表变量
        BankState.update_B_state(BB, BI, target="any", source="any")  # 更新各银行之状态示性变量

        ## 存储初始数据
        # A_data.BB_0 = deepcopy(BB)
        # A_data.BI_0 = deepcopy(BI)
        # A_data_0 = deepcopy(A)

        return A, A_data
        pass  # function

    pass  # class
