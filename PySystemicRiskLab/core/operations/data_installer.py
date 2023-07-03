"""
安装、初始化数据机
"""

from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank, SystemicRiskAgent
from PySystemicRiskLab.core.define.define_environmentVariables import env
from PySystemicRiskLab.core.define.define_type import IdsType
from PySystemicRiskLab.core.define.define_agentDataCollection import AgentDataCollection
from PySystemicRiskLab.core.define.define_agentsVariables import dict_bankCommercial, dict_bankInterbank
from PySystemicRiskLab.core.functions.fun_finance import Finance
# from PySystemicRiskLab.core.operations.executer import Executer

pass  # end import


class DataInstaller:
    """
    安装、初始化数据机
    """

    A_data = AgentDataCollection([], [])

    # # @property
    # @classmethod
    # def set_default_values_to_B_variables(cls):
    #     bank: BankCommercial = BankCommercial(
    #         id_agent=np.arange(1, env['num_bank'], step=1),  # agent 之编号 id
    #         abbr=np.full((env['num_bank'], 1), ""),  # 缩写 abbr
    #         name=np.full((env['num_bank'], 1), ""),  # 全名 name
    #         A_all=np.zeros((env['num_bank'], 1)),  # 总资产 A_all: $A_all=A_IB+A_exIB$
    #         A_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间资产加总 A_IB_all
    #         A_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间资产 A_exIB: $A_exIB=A_P+A_Q+A_R+A_other$
    #         A_P=np.zeros((env['num_bank'], 1)),  # 银行贷款给生产部门之资产（非流动性资产） A_P
    #         A_Q=np.zeros((env['num_bank'], 1)),  # 银行持有超额准备金（流动性资产） A_Q
    #         A_R=np.zeros((env['num_bank'], 1)),  # 银行持有法定准备金（非流动性资产） A_R
    #         A_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其它资产（非流动性资产） A_other
    #         Z_all=np.zeros((env['num_bank'], 1)),  # 总负债 Z_all: $Z_total=Z_IB+Z_exIB$
    #         Z_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间负债加总 Z_IB_all
    #         Z_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间负债 Z_exIB: $Z_exIB=Z_D+Z_other$
    #         Z_D=np.zeros((env['num_bank'], 1)),  # 银行获得居民部门存款（非流动性负债） Z_D
    #         Z_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其他负债（非流动性负债） Z_other
    #         E_all=np.zeros((env['num_bank'], 1)),  # 所有者权益 E_all
    #         T_all=np.zeros((env['num_bank'], 1)),  # 总贷款流出（贷款方发款出去） Lo_all: $Lo_all=Lo_IB_all+Lo_exIB$
    #         Lo_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流出 Lo_IB_all
    #         Lo_IB_all=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流出 Lo_exIB: $Lo_exIB=Lo_P$
    #         Lo_exIB=np.zeros((env['num_bank'], 1)),  # 银行贷款流出给生产部门 Lo_P
    #         Lo_P=np.zeros((env['num_bank'], 1)),  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
    #         Li_all=np.zeros((env['num_bank'], 1)),  # 总贷款流入（贷款方收款回来） Li_all: $Li_all=Li_IB_all+Li_exIB$
    #         Li_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流入 Li_IB_all
    #         Li_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流入 Li_exIB: $Li_exIB=Li_D$
    #         Li_P=np.zeros((env['num_bank'], 1)),  # 银行贷款流入从生产部门 Li_P
    #         Bi_all=np.zeros((env['num_bank'], 1)),  # 总借款流入（借款方借款进来） Bi_all: $Bi_all=Bi_IB_all+Bi_exIB$
    #         Bi_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流入 Bi_IB_all
    #         Bi_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间借款流入 Bi_exIB: $Bi_exIB=Bi_D$
    #         Bi_D=np.zeros((env['num_bank'], 1)),  # 银行借款流入从居民部门 Bi_D
    #         Bo_all=np.zeros((env['num_bank'], 1)),  # 总借款流出（借款方还款出去） Bo_all: $Bo_all=Bo_IB_all+Bo_exIB$
    #         Bo_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流出 Bo_IB_all
    #         Bo_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间借款流出 Bo_exIB: $Bo_exIB=Bo_P$
    #         Bo_D=np.zeros((env['num_bank'], 1)),  # 银行借款流出给居民部门 Bo_D
    #         Shock_t=np.zeros((env['num_bank'], 1)),  # 总冲击目标 Shock_t $Shock_t = Shock_exIB_t+Shock_IB_t$
    #         Shock_s=np.zeros((env['num_bank'], 1)),  # 总冲击源头 Shock_s $Shock_s = Shock_exIB_s+Shock_IB_s$
    #         Shock_def_t=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exIB_def_t+Shock_IB_def_t$
    #         Shock_def_s=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exIB_def_s+Shock_IB_def_s$
    #         Shock_run_t=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exIB_run_t+Shock_IB_run_t$
    #         Shock_run_s=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exIB_run_s+Shock_IB_run_s$
    #         Shock_exIB_t=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击目标 Shock_exIB_t $Shock_exIB_t = Shock_P_def_t+Shock_D_run_t$
    #         Shock_exIB_s=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击源头 Shock_exIB_s $Shock_exIB_s = Shock_P_run_s+Shock_D_def_s$
    #         Shock_P_run_s=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
    #         Shock_P_def_t=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
    #         Shock_D_def_s=np.zeros((env['num_bank'], 1)),  # 银行存款违约损失冲击源头 Shock_D_def_s
    #         Shock_D_run_t=np.zeros((env['num_bank'], 1)),  # 银行存款挤兑流动冲击目标 Shock_D_run_t
    #         Shock_B=np.zeros((env['num_bank'], 1)),  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
    #         Shock_B_A=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间资产端冲击 Shock_B_A
    #         Shock_B_Z=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
    #         Shock_IB_s=np.zeros((env['num_bank'], 1)),  # 银行间冲击源头 Shock_IB_s $Shock_IB_s=Shock_IB_def_s+Shock_IB_run_s$
    #         Shock_IB_t=np.zeros((env['num_bank'], 1)),  # 银行间冲击目标 Shock_IB_t $Shock_IB_t=Shock_IB_def_t+Shock_IB_run_t$
    #         Shock_IB_def_s=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击源头 Shock_IB_def_s
    #         Shock_IB_def_t=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击目标 Shock_IB_def_t
    #         Shock_IB_run_s=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击源头 Shock_IB_run_s $Shock_IB_run_s=Shock_IB_run_ilq_s+Shock_IB_run_br_s$
    #         Shock_IB_run_t=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击目标 Shock_IB_run_t $Shock_IB_run_t+Shock_IB_run_ilq_t+Shock_IB_run_br_t$
    #         Shock_IB_run_ilq_s=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击源头 Shock_IB_run_ilq_s
    #         Shock_IB_run_ilq_t=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击目标 Shock_IB_run_ilq_t
    #         Shock_IB_run_br_s=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击源头 Shock_IB_run_br_s
    #         Shock_IB_run_br_t=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击目标 Shock_IB_run_br_t
    #         Loss_IB=np.zeros((env['num_bank'], 1)),  # 银行间市场冲击损失 Loss_IB
    #         Loss_IB_def_t=np.zeros((env['num_bank'], 1)),  # 银行间资产负债违约冲击损失 Loss_IB_def_t
    #         Loss_IB_run_t=np.zeros((env['num_bank'], 1)),  # 银行间负债流动性挤兑冲击损失 Loss_IB_run_t
    #         # FIXME 以下带注释部分，用于测试几种不同的形状之影响
    #         # on=np.full(env['num_bank'], True),  # 示性向量之于银行是否存在 is_on
    #         # off=np.full(env['num_bank'], False),  # 示性向量之于银行是否已退出不存在 is_off
    #         # hel=np.full(env['num_bank'], True),  # 示性向量之于银行是否健康 is_healthy
    #         # isv=np.full(env['num_bank'], False),  # 示性向量之于银行是否资不抵债 is_insolvent
    #         # ilq=np.full(env['num_bank'], False),  # 示性向量之于银行是否流动性短缺 is_illiquid
    #         # br=np.full(env['num_bank'], False),  # 示性向量之于银行是否破产 is_bankrupt
    #         # is_needed_BoIB=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还借款 is_needed_BoIB
    #         # is_enabled_BoIB=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还借款 is_enabled_BoIB
    #         # is_needed_BoD=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还居民部门存款 is_needed_BoD
    #         # is_enabled_BoD=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还居民部门存款 is_enabled_BoD
    #         # is_needed_LiP=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要收回厂商贷款 is_needed_LiP
    #         # is_enabled_LiP=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以收回厂商贷款 is_enabled_LiP
    #         # is_allocated_Shock=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已经分配传染冲击 is_allocated_Shock
    #         on=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否存在 is_on
    #         off=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已退出不存在 is_off
    #         hel=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否健康 is_healthy
    #         isv=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否资不抵债 is_insolvent
    #         ilq=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否流动性短缺 is_illiquid
    #         br=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否破产 is_bankrupt
    #         is_needed_BoIB=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还借款 is_needed_BoIB
    #         is_enabled_BoIB=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还借款 is_enabled_BoIB
    #         is_needed_BoD=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还居民部门存款 is_needed_BoD
    #         is_enabled_BoD=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还居民部门存款 is_enabled_BoD
    #         is_needed_LiP=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要收回厂商贷款 is_needed_LiP
    #         is_enabled_LiP=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以收回厂商贷款 is_enabled_LiP
    #         is_allocated_Shock=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已经分配传染冲击 is_allocated_Shock
    #         list_exist=np.full(env['num_bank'], list),  # 列表之于存在的银行编号 list_exist
    #         list_insolvent=np.full(env['num_bank'], list),  # 列表之于资不抵债的银行编号 list_insolvent
    #         list_illiquid=np.full(env['num_bank'], list),  # 列表之于流动性短缺的银行编号 list_illiquid
    #         list_bankrupt=np.full(env['num_bank'], list),  # 列表之于破产的银行编号 list_bankrupt
    #
    #     )
    #
    #     interbank: BankInterbank = BankInterbank(
    #         id_agent=np.array(np.arange(1, env['num_bank'] * env['num_bank'] + 1).reshape((env['num_bank'], env['num_bank'])), dtype=IdsType),  # agent 之间之关联编号 id
    #         A_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产邻接矩阵 A_IB
    #         Z_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间负债邻接矩阵 Z_IB
    #         Lo_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流出邻接矩阵 Lo_IB
    #         Li_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流入邻接矩阵 Li_IB
    #         Bo_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流入邻接矩阵 Bo_IB
    #         Bi_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流出邻接矩阵 Bi_IB
    #         Shock_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间冲击 Shock_IB: $Shock_IB=Shock_IB_def+Shock_IB_run$
    #         Shock_IB_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间违约损失冲击 Shock_IB_def
    #         Shock_IB_run=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间挤兑流动冲击 Shock_IB_run: $Shock_IB_run=Shock_IB_run_ilq+Shock_IB_run_br$
    #         Shock_IB_run_ilq=np.zeros((env['num_bank'], env['num_bank'])),  # 流动性短缺银行银行间挤兑流动冲击 Shock_IB_run_ilq
    #         Shock_IB_run_br=np.zeros((env['num_bank'], env['num_bank'])),  # 破产银行银行间挤兑流动冲击 Shock_IB_run_br
    #         Loss_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间市场冲击损失 Loss_IB
    #         Loss_IB_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产负债违约冲击损失 Loss_IB_def
    #         Loss_IB_run=np.full((env['num_bank'], env['num_bank']), True),  # 银行间负债流动性挤兑冲击损失 Loss_IB_run
    #         is_exposure=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于是否有银行间敞口 is_exposure
    #         on=np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间存在的 is_on
    #         off=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间已退出不存在的 is_off
    #         hel=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间健康的 is_healthy
    #         isv=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间资不抵债的 is_insolvent
    #         ilq=np.array([]),  # 信息邻接矩阵之于银行间流动性短缺的 is_illiquid
    #         br=np.array([]),  # 信息邻接矩阵之于银行间破产的 is_bankrupt
    #         cre=np.array([]),  # 信息列表之于各银行之债权方银行编号 list_creditors
    #         deb=np.array([]),  # 信息列表之于各银行之债务方银行编号 list_debtors
    #         cre_isv=[],  # 信息列表之于资不抵债的银行之债权方银行编号 list_creditors_in_insolvent
    #         deb_isv=[],  # 信息列表之于资不抵债的银行之债务方银行编号 list_debtors_in_insolvent
    #         cre_ilq=[],  # 信息列表之于流动性短缺的银行之债权方银行编号 list_creditors_in_illiquid
    #         deb_ilq=[],  # 信息列表之于流动性短缺的银行之债务方银行编号 list_debtors_in_illiquid
    #         cre_br=[],  # 信息列表之于破产的银行之债权方银行编号 list_creditors_in_bankrupt
    #         deb_br=[],  # 信息列表之于破产的银行之债务方银行编号 list_debtors_in_bankrupt
    #     )
    #
    #     return bank, interbank
    #     pass  # method

    @classmethod
    def set_default_values_to_B_variables(cls):

        bank: BankCommercial = BankCommercial(
            id_agent=np.arange(1, env['num_bank'], step=1),  # agent 之编号 id
            abbr=np.full((env['num_bank'], 1), ""),  # 缩写 abbr
            name=np.full((env['num_bank'], 1), ""),  # 全名 name
            A_all=np.zeros((env['num_bank'], 1)),  # 总资产 A_all: $A_all=A_IB+A_exIB$
            A_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间资产加总 A_IB_all
            A_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间资产 A_exIB: $A_exIB=A_P+A_Q+A_R+A_other$
            A_P=np.zeros((env['num_bank'], 1)),  # 银行贷款给生产部门之资产（非流动性资产） A_P
            A_Q=np.zeros((env['num_bank'], 1)),  # 银行持有超额准备金（流动性资产） A_Q
            A_R=np.zeros((env['num_bank'], 1)),  # 银行持有法定准备金（非流动性资产） A_R
            A_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其它资产（非流动性资产） A_other
            Z_all=np.zeros((env['num_bank'], 1)),  # 总负债 Z_all: $Z_total=Z_IB+Z_exIB$
            Z_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间负债加总 Z_IB_all
            Z_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间负债 Z_exIB: $Z_exIB=Z_D+Z_other$
            Z_D=np.zeros((env['num_bank'], 1)),  # 银行获得居民部门存款（非流动性负债） Z_D
            Z_other=np.zeros((env['num_bank'], 1)),  # 银行持有的其他负债（非流动性负债） Z_other
            E_all=np.zeros((env['num_bank'], 1)),  # 所有者权益 E_all
            T_all=np.zeros((env['num_bank'], 1)),  # 总贷款流出（贷款方发款出去） Lo_all: $Lo_all=Lo_IB_all+Lo_exIB$
            Lo_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流出 Lo_IB_all
            Lo_IB_all=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流出 Lo_exIB: $Lo_exIB=Lo_P$
            Lo_exIB=np.zeros((env['num_bank'], 1)),  # 银行贷款流出给生产部门 Lo_P
            Lo_P=np.zeros((env['num_bank'], 1)),  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
            Li_all=np.zeros((env['num_bank'], 1)),  # 总贷款流入（贷款方收款回来） Li_all: $Li_all=Li_IB_all+Li_exIB$
            Li_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间贷款流入 Li_IB_all
            Li_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间贷款流入 Li_exIB: $Li_exIB=Li_D$
            Li_P=np.zeros((env['num_bank'], 1)),  # 银行贷款流入从生产部门 Li_P
            Bi_all=np.zeros((env['num_bank'], 1)),  # 总借款流入（借款方借款进来） Bi_all: $Bi_all=Bi_IB_all+Bi_exIB$
            Bi_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流入 Bi_IB_all
            Bi_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间借款流入 Bi_exIB: $Bi_exIB=Bi_D$
            Bi_D=np.zeros((env['num_bank'], 1)),  # 银行借款流入从居民部门 Bi_D
            Bo_all=np.zeros((env['num_bank'], 1)),  # 总借款流出（借款方还款出去） Bo_all: $Bo_all=Bo_IB_all+Bo_exIB$
            Bo_IB_all=np.zeros((env['num_bank'], 1)),  # 银行间借款流出 Bo_IB_all
            Bo_exIB=np.zeros((env['num_bank'], 1)),  # 非银行间借款流出 Bo_exIB: $Bo_exIB=Bo_P$
            Bo_D=np.zeros((env['num_bank'], 1)),  # 银行借款流出给居民部门 Bo_D
            Shock_t=np.zeros((env['num_bank'], 1)),  # 总冲击目标 Shock_t $Shock_t = Shock_exIB_t+Shock_IB_t$
            Shock_s=np.zeros((env['num_bank'], 1)),  # 总冲击源头 Shock_s $Shock_s = Shock_exIB_s+Shock_IB_s$
            Shock_def_t=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exIB_def_t+Shock_IB_def_t$
            Shock_def_s=np.zeros((env['num_bank'], 1)),  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exIB_def_s+Shock_IB_def_s$
            Shock_run_t=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exIB_run_t+Shock_IB_run_t$
            Shock_run_s=np.zeros((env['num_bank'], 1)),  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exIB_run_s+Shock_IB_run_s$
            Shock_exIB_t=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击目标 Shock_exIB_t $Shock_exIB_t = Shock_P_def_t+Shock_D_run_t$
            Shock_exIB_s=np.zeros((env['num_bank'], 1)),  # 非银行间借贷冲击源头 Shock_exIB_s $Shock_exIB_s = Shock_P_run_s+Shock_D_def_s$
            Shock_P_run_s=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
            Shock_P_def_t=np.zeros((env['num_bank'], 1)),  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
            Shock_D_def_s=np.zeros((env['num_bank'], 1)),  # 银行存款违约损失冲击源头 Shock_D_def_s
            Shock_D_run_t=np.zeros((env['num_bank'], 1)),  # 银行存款挤兑流动冲击目标 Shock_D_run_t
            Shock_B=np.zeros((env['num_bank'], 1)),  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
            Shock_B_A=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间资产端冲击 Shock_B_A
            Shock_B_Z=np.zeros((env['num_bank'], 1)),  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
            Shock_IB_s=np.zeros((env['num_bank'], 1)),  # 银行间冲击源头 Shock_IB_s $Shock_IB_s=Shock_IB_def_s+Shock_IB_run_s$
            Shock_IB_t=np.zeros((env['num_bank'], 1)),  # 银行间冲击目标 Shock_IB_t $Shock_IB_t=Shock_IB_def_t+Shock_IB_run_t$
            Shock_IB_def_s=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击源头 Shock_IB_def_s
            Shock_IB_def_t=np.zeros((env['num_bank'], 1)),  # 银行间违约损失冲击目标 Shock_IB_def_t
            Shock_IB_run_s=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击源头 Shock_IB_run_s $Shock_IB_run_s=Shock_IB_run_ilq_s+Shock_IB_run_br_s$
            Shock_IB_run_t=np.zeros((env['num_bank'], 1)),  # 银行间挤兑流动冲击目标 Shock_IB_run_t $Shock_IB_run_t+Shock_IB_run_ilq_t+Shock_IB_run_br_t$
            Shock_IB_run_ilq_s=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击源头 Shock_IB_run_ilq_s
            Shock_IB_run_ilq_t=np.zeros((env['num_bank'], 1)),  # 银行间流动性短缺挤兑流动冲击目标 Shock_IB_run_ilq_t
            Shock_IB_run_br_s=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击源头 Shock_IB_run_br_s
            Shock_IB_run_br_t=np.zeros((env['num_bank'], 1)),  # 银行间倒闭挤兑流动冲击目标 Shock_IB_run_br_t
            Loss_IB=np.zeros((env['num_bank'], 1)),  # 银行间市场冲击损失 Loss_IB
            Loss_IB_def_t=np.zeros((env['num_bank'], 1)),  # 银行间资产负债违约冲击损失 Loss_IB_def_t
            Loss_IB_run_t=np.zeros((env['num_bank'], 1)),  # 银行间负债流动性挤兑冲击损失 Loss_IB_run_t
            # FIXME 以下带注释部分，用于测试几种不同的形状之影响
            # on=np.full(env['num_bank'], True),  # 示性向量之于银行是否存在 is_on
            # off=np.full(env['num_bank'], False),  # 示性向量之于银行是否已退出不存在 is_off
            # hel=np.full(env['num_bank'], True),  # 示性向量之于银行是否健康 is_healthy
            # isv=np.full(env['num_bank'], False),  # 示性向量之于银行是否资不抵债 is_insolvent
            # ilq=np.full(env['num_bank'], False),  # 示性向量之于银行是否流动性短缺 is_illiquid
            # br=np.full(env['num_bank'], False),  # 示性向量之于银行是否破产 is_bankrupt
            # is_needed_BoIB=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还借款 is_needed_BoIB
            # is_enabled_BoIB=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还借款 is_enabled_BoIB
            # is_needed_BoD=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要偿还居民部门存款 is_needed_BoD
            # is_enabled_BoD=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以偿还居民部门存款 is_enabled_BoD
            # is_needed_LiP=np.full(env['num_bank'], False),  # 示性向量之于银行是否需要收回厂商贷款 is_needed_LiP
            # is_enabled_LiP=np.full(env['num_bank'], True),  # 示性向量之于银行是否可以收回厂商贷款 is_enabled_LiP
            # is_allocated_Shock=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已经分配传染冲击 is_allocated_Shock
            on=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否存在 is_on
            off=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已退出不存在 is_off
            hel=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否健康 is_healthy
            isv=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否资不抵债 is_insolvent
            ilq=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否流动性短缺 is_illiquid
            br=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否破产 is_bankrupt
            is_needed_BoIB=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还借款 is_needed_BoIB
            is_enabled_BoIB=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还借款 is_enabled_BoIB
            is_needed_BoD=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要偿还居民部门存款 is_needed_BoD
            is_enabled_BoD=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以偿还居民部门存款 is_enabled_BoD
            is_needed_LiP=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否需要收回厂商贷款 is_needed_LiP
            is_enabled_LiP=np.full((env['num_bank'], 1), True),  # 示性向量之于银行是否可以收回厂商贷款 is_enabled_LiP
            is_allocated_Shock=np.full((env['num_bank'], 1), False),  # 示性向量之于银行是否已经分配传染冲击 is_allocated_Shock
            list_exist=np.full(env['num_bank'], list),  # 列表之于存在的银行编号 list_exist
            list_insolvent=np.full(env['num_bank'], list),  # 列表之于资不抵债的银行编号 list_insolvent
            list_illiquid=np.full(env['num_bank'], list),  # 列表之于流动性短缺的银行编号 list_illiquid
            list_bankrupt=np.full(env['num_bank'], list),  # 列表之于破产的银行编号 list_bankrupt

        )

        interbank: BankInterbank = BankInterbank(
            id_agent=np.array(np.arange(1, env['num_bank'] * env['num_bank'] + 1).reshape((env['num_bank'], env['num_bank'])), dtype=IdsType),  # agent 之间之关联编号 id
            A_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产邻接矩阵 A_IB
            Z_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间负债邻接矩阵 Z_IB
            Lo_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流出邻接矩阵 Lo_IB
            Li_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间贷款流入邻接矩阵 Li_IB
            Bo_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流入邻接矩阵 Bo_IB
            Bi_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间借款流出邻接矩阵 Bi_IB
            Shock_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间冲击 Shock_IB: $Shock_IB=Shock_IB_def+Shock_IB_run$
            Shock_IB_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间违约损失冲击 Shock_IB_def
            Shock_IB_run=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间挤兑流动冲击 Shock_IB_run: $Shock_IB_run=Shock_IB_run_ilq+Shock_IB_run_br$
            Shock_IB_run_ilq=np.zeros((env['num_bank'], env['num_bank'])),  # 流动性短缺银行银行间挤兑流动冲击 Shock_IB_run_ilq
            Shock_IB_run_br=np.zeros((env['num_bank'], env['num_bank'])),  # 破产银行银行间挤兑流动冲击 Shock_IB_run_br
            Loss_IB=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间市场冲击损失 Loss_IB
            Loss_IB_def=np.zeros((env['num_bank'], env['num_bank'])),  # 银行间资产负债违约冲击损失 Loss_IB_def
            Loss_IB_run=np.full((env['num_bank'], env['num_bank']), True),  # 银行间负债流动性挤兑冲击损失 Loss_IB_run
            is_exposure=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于是否有银行间敞口 is_exposure
            on=np.full((env['num_bank'], env['num_bank']), True),  # 信息邻接矩阵之于银行间存在的 is_on
            off=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间已退出不存在的 is_off
            hel=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间健康的 is_healthy
            isv=np.full((env['num_bank'], env['num_bank']), False),  # 信息邻接矩阵之于银行间资不抵债的 is_insolvent
            ilq=np.array([]),  # 信息邻接矩阵之于银行间流动性短缺的 is_illiquid
            br=np.array([]),  # 信息邻接矩阵之于银行间破产的 is_bankrupt
            cre=np.array([]),  # 信息列表之于各银行之债权方银行编号 list_creditors
            deb=np.array([]),  # 信息列表之于各银行之债务方银行编号 list_debtors
            cre_isv=[],  # 信息列表之于资不抵债的银行之债权方银行编号 list_creditors_in_insolvent
            deb_isv=[],  # 信息列表之于资不抵债的银行之债务方银行编号 list_debtors_in_insolvent
            cre_ilq=[],  # 信息列表之于流动性短缺的银行之债权方银行编号 list_creditors_in_illiquid
            deb_ilq=[],  # 信息列表之于流动性短缺的银行之债务方银行编号 list_debtors_in_illiquid
            cre_br=[],  # 信息列表之于破产的银行之债权方银行编号 list_creditors_in_bankrupt
            deb_br=[],  # 信息列表之于破产的银行之债务方银行编号 list_debtors_in_bankrupt
        )

        return bank, interbank
        pass  # method

    @classmethod
    def set_randomly_values_to_Bank_variables(cls):
        # TODO """随机化初始化银行变量"""
        # bank, interbank = cls.set_default_values_to_B_variables()
        pass

        pass

    @classmethod
    def set_imported_values_to_Bank_variables(cls):
        # TODO """导入数据以初始化银行变量"""
        # bank, interbank = cls.set_default_values_to_B_variables
        pass

    @classmethod
    def set_manually_values_to_Bank_variables(cls):
        """手动设置以初始化银行变量"""

        ## NOTE 当用对象字段数据结构时：
        bank, interbank = cls.set_default_values_to_B_variables()
        bank.__dict__.update(dict_bankCommercial)
        interbank.__dict__.update(dict_bankInterbank)

        # ## NOTE 当用pandas数据结构时：
        # bank = pd.Series()
        # for k, v in dict_bankCommercial.items():
        #     bank[k] = v
        # interbank = pd.Series()
        # for k, v in dict_bankInterbank.items():
        #     interbank[k] = v

        return bank, interbank
        pass  # method

    @classmethod
    def install_data(cls, init_method: str):
        """
        不同的初始化方式。

        参数init_method可选项：

        - ``only init``:  仅单纯初始化；

        - ``randomly``:  生成随机数据以初始化；

        - ``import data``:  导入数据以初始化

        - ``manually``:  手动设置以初始化；

        Args:
            init_method ():

        Returns: A

        """

        if init_method == "only init":
            BB, IB = cls.set_default_values_to_B_variables()
        elif init_method == "randomly":
            BB, IB = cls.set_randomly_values_to_Bank_variables()  # TODO 按需添加
        elif init_method == "import data":
            BB, IB, cls.A_data.BB, cls.A_data.IB = cls.set_imported_values_to_Bank_variables()  # 导入数据以初始化银行变量 #TODO 按需添加
        elif init_method == "set manually":
            BB, IB = cls.set_manually_values_to_Bank_variables()  # 手动设置以初始化银行变量
        else:
            raise ("关键词" + str(init_method) + "取值错误！")
            pass

        # ## NOTE 当用pandas数据结构时：
        # A = pd.Series([BB, IB], index=['BB', 'IB'])

        # # 初始化带回合变量的商业银行实例数组、初始化带回合变量的银行间市场实例数组 #HACK无用
        # A_data = Collector.collect(A, None, env)

        b = (BB.on | BB.off).reshape(-1, 1)  # 临时设置A.BB示性变量
        ib = ((BB.on | BB.off).reshape(-1, 1) & (BB.on | BB.off).reshape(1, -1))  # 临时设置IB示性变量

        ## 构建Agent模型
        ## NOTE 当用对象字段数据结构时。
        # HACK 注意这时候`b`、`ib`变量在后续过程中没有发生变动，几乎就是一个鸡肋的携带物。目前暂时保留，后续再处理。
        A = SystemicRiskAgent(
            1,  # 编号（必备的）
            BB,  # 商业银行群
            b,  # 商业银行群示性变量
            IB,  # 银行间邻接矩阵
            ib,  # 银行间邻接矩阵示性变量
        )
        cls.initialize_data(A)  # 更新各银行之变量，在第一回合初始时
        return A
        pass  # method

    @classmethod
    def initialize_data(cls, A):
        ## 更新各银行之变量，在第一回合初始时 # BUG
        # update=env['update']
        # @Executer.execute
        Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='clear transfer all')  # 更新各银行之所有交易变量，在第一回合开始时#BUG 删除后是否影响后续实验初始化数据？有影响！
        Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='all')  # 更新各银行之所有变量，在第一回合开始时
        return A
        pass

    pass  # class
