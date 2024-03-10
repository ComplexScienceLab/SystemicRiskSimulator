"""
设置多主体变量

NOTE 说明：这个初始数据全部是虚拟生成的数据，与真实数据无关，仅作为样例进行展示。虚拟数据生成的借鉴的来源：谭春枝所著的《基于复杂网络理论的银行间市场系统风险传染机制研究》
"""

from SystemicRiskSimulator.external_packages import Path, pickle
from SystemicRiskSimulator.core.define.define_consts import CONST
from SystemicRiskSimulator.core.define.define_type import *
from SystemicRiskSimulator.tools.tools import Tools

pass  # end import

folderpath_project = Tools.get_project_rootpath()

######### 设置模型变量 #########################################

sgv = {}
sgv['list_agents_yearName'] = ['2012']  # 设置 agents 初始数据列表
sgv['num_bank'] = 5

set_bankCommercial_variables = dict(

    ######### 设置模型变量 #########################################

    ## 初始化商业银行群 bank_commercial
    id_agent=CONST(sgv['num_bank']).RANGE1.copy() - 1,  # agent 之编号 id
    abbr=CONST(sgv['num_bank']).RANGE1.copy(),  # 缩写 abbr
    fullName=np.array(["Bank_1", "Bank_2", "Bank_3", "Bank_4", "Bank_5"]),  # 全名 fullName
    A_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总资产 A_all: $A_all=A_IB+A_exIB$
    A_IB_all=np.array([[2185.24, 398.37, 730.99, 1357.75, 2717.39]]).T,  # 银行间资产加总 A_IB_all
    A_exIB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间资产 A_exIB: $A_exIB=A_P+A_Q+A_R+A_other$
    A_P=np.array([[1631.73, 4303.24, 3379.72, 4351.47, 620.69]]).T,  # 银行贷款给非金融部门（非银行金融部门）之资产（非流动性资产） A_P
    A_Q=np.array([[477.125, 587.693, 513.847, 713.662, 417.257]]).T,  # 银行持有超额准备金（流动性资产） A_Q
    A_R=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行持有法定准备金（非流动性资产） A_R #NOTE 这里用准备金率计算得到。
    # A_R=np.zeros([[86.75, 106.85, 93.43, 129.76, 75.86]]),  # 银行持有法定准备金（非流动性资产） A_R #HACK这个调试用的临时数据是直接从谭春枝之《基于复杂网络理论的银行间市场系统风险传染机制研究》p61. 抄过来的。但是在这里仅作为记录，但并不用到。
    A_other=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行持有的其他资产（NOTE 包括：研究不涉及的资产科目、会计科目之其他资产、不重要且不明确的资产科目） A_other
    Z_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总负债 Z_all: $Z_total=Z_IB+Z_exIB$
    Z_IB_all=np.array([[959.6, 1844.24, 1253.34, 2851.85, 480.71]]).T,  # 银行间负债加总 Z_IB_all
    Z_exIB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间负债 Z_exIB: $Z_exIB=Z_D+Z_CB+Z_other$
    Z_CB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 持有央行之负债 Z_CB
    Z_D=np.array([[3160.99, 3231.37, 3184.36, 3311.51, 3122.9]]).T,  # 银行获得居民部门存款（非流动性负债） Z_D
    Z_other=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行持有的其他负债（NOTE 包括：研究不涉及的负债科目、会计科目之其他负债、不重要且不明确的负债科目） Z_other
    E_all=np.array([[173.505, 213.693, 186.857, 259.522, 151.727]]).T,  # 所有者权益 E_all
    T_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总交易流量 Transfer_all: $Transfer_all=Lo_all+Li_all+Bi_all+Bo_all$
    Lo_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总贷款流出（贷款方发款出去） Lo_all: $Lo_all=Lo_IB_all+Lo_exIB$
    Lo_IB_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间贷款流出 Lo_IB_all
    Lo_exIB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间贷款流出 Lo_exIB: $Lo_exIB=Lo_P$
    Lo_P=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行贷款流出给生产部门 Lo_P
    Li_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总贷款流入（贷款方收款回来） Li_all: $Li_all=Li_IB_all+Li_exIB$
    Li_IB_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间贷款流入 Li_IB_all
    Li_exIB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间贷款流入 Li_exIB: $Li_exIB=Li_D$
    Li_P=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行贷款流入从生产部门 Li_P
    Bi_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总借款流入（借款方借款进来） Bi_all: $Bi_all=Bi_IB_all+Bi_exIB$
    Bi_IB_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间借款流入 Bi_IB_all
    Bi_exIB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间借款流入 Bi_exIB: $Bi_exIB=Bi_D$
    Bi_D=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行借款流入从居民部门 Bi_D
    Bo_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总借款流出（借款方还款出去） Bo_all: $Bo_all=Bo_IB_all+Bo_exIB$
    Bo_IB_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间借款流出 Bo_IB_all
    Bo_exIB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间借款流出 Bo_exIB: $Bo_exIB=Bo_P$
    Bo_D=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行借款流出给居民部门 Bo_D
    Shock_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总冲击目标 Shock_t $Shock_t = Shock_exIB_t+Shock_IB_t$
    Shock_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总冲击源头 Shock_s $Shock_s = Shock_exIB_s+Shock_IB_s$
    Shock_def_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总违约损失冲击目标 Shock_def_t $Shock_def_t = Shock_exIB_def_t+Shock_IB_def_t$
    Shock_def_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总违约损失冲击源头 Shock_def_s $Shock_def_s = Shock_exIB_def_s+Shock_IB_def_s$
    Shock_run_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总挤兑流动冲击目标 Shock_run_t $Shock_run_t = Shock_exIB_run_t+Shock_IB_run_t$
    Shock_run_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总挤兑流动冲击源头 Shock_run_s $Shock_run_s = Shock_exIB_run_s+Shock_IB_run_s$
    Shock_exIB_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间借贷冲击目标 Shock_exIB_t $Shock_exIB_t = Shock_P_def_t+Shock_D_run_t$
    Shock_exIB_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间借贷冲击源头 Shock_exIB_s $Shock_exIB_s = Shock_P_run_s+Shock_D_def_s$
    Shock_P_run_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行之厂商贷款挤兑流动冲击源头 Shock_P_run_s
    Shock_P_def_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
    Shock_D_def_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行存款违约损失冲击源头 Shock_D_def_s
    Shock_D_run_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行存款挤兑流动冲击目标 Shock_D_run_t
    Shock_B=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行内资产负债冲击 Shock_B $Shock_B=Shock_B_A+Shock_B_Z$
    Shock_B_A=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行内资产负债之银行间资产端冲击 Shock_B_A
    Shock_B_Z=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行内资产负债之银行间负债端冲击 Shock_B_Z
    Shock_IB_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间冲击源头 Shock_IB_s $Shock_IB_s=Shock_IB_def_s+Shock_IB_run_s$
    Shock_IB_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间冲击目标 Shock_IB_t $Shock_IB_t=Shock_IB_def_t+Shock_IB_run_t$
    Shock_IB_def_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间违约损失冲击源头 Shock_IB_def_s
    Shock_IB_def_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间违约损失冲击目标 Shock_IB_def_t
    Shock_IB_run_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间挤兑流动冲击源头 Shock_IB_run_s $Shock_IB_run_s=Shock_IB_run_ilq_s+Shock_IB_run_br_s$
    Shock_IB_run_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间挤兑流动冲击目标 Shock_IB_run_t $Shock_IB_run_t+Shock_IB_run_ilq_t+Shock_IB_run_br_t$
    Shock_IB_run_ilq_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间流动性短缺挤兑流动冲击源头 Shock_IB_run_ilq_s
    Shock_IB_run_ilq_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间流动性短缺挤兑流动冲击目标 Shock_IB_run_ilq_t
    Shock_IB_run_br_s=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间倒闭挤兑流动冲击源头 Shock_IB_run_br_s
    Shock_IB_run_br_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间倒闭挤兑流动冲击目标 Shock_IB_run_br_t
    Loss_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行总损失目标 Loss_t
    # Loss_s = CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行总损失源头 Loss_s
    Loss_exIB_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 非银行间资产负债总损失目标 Loss_exIB_t
    # Loss_exIB_s = CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 非银行间资产负债总损失源头 Loss_exIB_s
    Loss_exIB_def_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 非银行间资产负债违约损失冲击损失目标 Loss_exIB_def_t
    # Loss_exIB_def_s = CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 非银行间资产负债违约损失冲击损失源头 Loss_exIB_def_s
    Loss_exIB_run_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 非银行间负债流动性挤兑冲击损失目标 Loss_exIB_run_t
    # Loss_exIB_run_s = CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 非银行间负债流动性挤兑冲击损失源头 Loss_exIB_run_s
    Loss_def_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行资产负债违约总损失目标 Loss_def_t
    # Loss_def_s = CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行资产负债违约总损失源头 Loss_def_s
    Loss_run_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行负债流动性挤兑总损失目标 Loss_run_t
    # Loss_run_s = CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行负债流动性挤兑总损失源头 Loss_run_s
    Loss_IB_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行间市场冲击损失目标 Loss_IB_t
    # Loss_IB_s = CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行间市场冲击损失源头 Loss_IB_s
    Loss_IB_def_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行间资产负债违约损失冲击损失目标 Loss_IB_def_t
    # Loss_IB_def_s = CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行间资产负债违约损失冲击损失源头 Loss_IB_def_s
    Loss_IB_run_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行间负债流动性挤兑冲击损失目标 Loss_IB_run_t
    # Loss_IB_run_s = CONST(sgv['num_bank']).ZEROS1.copy(),  # = deepcopy(ZEROS1)  # 银行间负债流动性挤兑冲击损失源头 Loss_IB_run_s
    on=CONST(sgv['num_bank']).TRUE1.copy(),  # 示性向量之于银行是否存在 is_on
    off=CONST(sgv['num_bank']).FALSE1.copy(),  # 示性向量之于银行是否已退出不存在 is_off
    hel=CONST(sgv['num_bank']).TRUE1.copy(),  # 示性向量之于银行是否健康 is_healthy
    isv=CONST(sgv['num_bank']).FALSE1.copy(),  # 示性向量之于银行是否资不抵债 is_insolvent
    ilq=CONST(sgv['num_bank']).FALSE1.copy(),  # 示性向量之于银行是否流动性短缺 is_illiquid
    br=CONST(sgv['num_bank']).FALSE1.copy(),  # 示性向量之于银行是否破产 is_bankrupt
    is_needed_BoIB=CONST(sgv['num_bank']).FALSE1.copy(),  # 示性向量之于银行是否需要偿还借款 is_needed_BoIB
    is_enabled_BoIB=CONST(sgv['num_bank']).TRUE1.copy(),  # 示性向量之于银行是否可以偿还借款 is_enabled_BoIB
    is_needed_BoD=CONST(sgv['num_bank']).FALSE1.copy(),  # 示性向量之于银行是否需要偿还居民部门存款 is_needed_BoD
    is_enabled_BoD=CONST(sgv['num_bank']).TRUE1.copy(),  # 示性向量之于银行是否可以偿还居民部门存款 is_enabled_BoD
    is_needed_LiP=CONST(sgv['num_bank']).FALSE1.copy(),  # 示性向量之于银行是否需要收回厂商贷款 is_needed_LiP
    is_enabled_LiP=CONST(sgv['num_bank']).TRUE1.copy(),  # 示性向量之于银行是否可以收回厂商贷款 is_enabled_LiP
    is_allocated_Shock=CONST(sgv['num_bank']).FALSE1.copy(),  # 示性向量之于银行是否已经分配传染冲击 is_allocated_Shock
    list_exist=np.full(sgv['num_bank'], list),  # 列表之于存在的银行编号 list_exist
    list_insolvent=np.full(sgv['num_bank'], list),  # 列表之于资不抵债的银行编号 list_insolvent
    list_illiquid=np.full(sgv['num_bank'], list),  # 列表之于流动性短缺的银行编号 list_illiquid
    list_bankrupt=np.full(sgv['num_bank'], list)  # 列表之于破产的银行编号 list_bankrupt
)

set_bankInterbank_variables = dict(

    ## 初始化银行间邻接矩阵 interbank
    id_agent=CONST(sgv['num_bank']).RANGE2 - 1,  # agent 之间之关联编号 id
    A_IB=np.array([[0, 1728.55, 0, 134.46, 322.23], [109.35, 0, 289.02, 0, 0], [730.99, 0, 0, 0, 0], [119.26, 115.69, 964.32, 0, 158.48], [0, 0, 0, 2717.39, 0]]),  # 银行间资产邻接矩阵 A_IB
    Z_IB=np.array([[0, 1728.55, 0, 134.46, 322.23], [109.35, 0, 289.02, 0, 0], [730.99, 0, 0, 0, 0], [119.26, 115.69, 964.32, 0, 158.48], [0, 0, 0, 2717.39, 0]]).T,  # 银行间负债邻接矩阵 Z_IB
    Lo_IB=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间贷款流出邻接矩阵 Lo_IB
    Li_IB=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间贷款流入邻接矩阵 Li_IB
    Bo_IB=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间借款流入邻接矩阵 Bo_IB
    Bi_IB=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间借款流出邻接矩阵 Bi_IB
    Shock_IB=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间冲击 Shock_IB: $Shock_IB=Shock_IB_def+Shock_IB_run$
    Shock_IB_def=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间违约损失冲击 Shock_IB_def
    Shock_IB_run=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间挤兑流动冲击 Shock_IB_run: $Shock_IB_run=Shock_IB_run_ilq+Shock_IB_run_br$
    Shock_IB_run_ilq=CONST(sgv['num_bank']).ZEROS2.copy(),  # 流动性短缺银行银行间挤兑流动冲击 Shock_IB_run_ilq
    Shock_IB_run_br=CONST(sgv['num_bank']).ZEROS2.copy(),  # 破产银行银行间挤兑流动冲击 Shock_IB_run_br
    Loss_IB=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间市场冲击损失 Loss_IB
    Loss_IB_def=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间资产负债违约冲击损失 Loss_IB_def
    Loss_IB_run=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间负债流动性挤兑冲击损失 Loss_IB_run
    is_exposure=CONST(sgv['num_bank']).ZEROS2.copy(),  # 信息邻接矩阵之于是否有银行间敞口 is_exposure
    on=CONST(sgv['num_bank']).TRUE2.copy(),  # 信息邻接矩阵之于银行间存在的 is_on
    off=CONST(sgv['num_bank']).FALSE2.copy(),  # 信息邻接矩阵之于银行间已退出不存在的 is_off
    hel=CONST(sgv['num_bank']).TRUE2.copy(),  # 信息邻接矩阵之于银行间健康的 is_healthy
    isv=CONST(sgv['num_bank']).FALSE2.copy(),  # 信息邻接矩阵之于银行间资不抵债的 is_insolvent
    ilq=CONST(sgv['num_bank']).FALSE2.copy(),  # 信息邻接矩阵之于银行间流动性短缺的 is_illiquid
    br=CONST(sgv['num_bank']).FALSE2.copy(),  # 信息邻接矩阵之于银行间破产的 is_bankrupt
    cre=np.array([np.array([], dtype=list) for _ in range(sgv['num_bank'])]),  # 信息列表之于各银行之债权方银行编号 list_creditors
    deb=np.array([np.array([], dtype=list) for _ in range(sgv['num_bank'])]),  # 信息列表之于各银行之债务方银行编号 list_debtors
    cre_isv=np.array([np.array([], dtype=list) for _ in range(sgv['num_bank'])]),  # 信息列表之于资不抵债的银行之债权方银行编号 list_creditors_in_insolvent
    deb_isv=np.array([np.array([], dtype=list) for _ in range(sgv['num_bank'])]),  # 信息列表之于资不抵债的银行之债务方银行编号 list_debtors_in_insolvent
    cre_ilq=np.array([np.array([], dtype=list) for _ in range(sgv['num_bank'])]),  # 信息列表之于流动性短缺的银行之债权方银行编号 list_creditors_in_illiquid
    deb_ilq=np.array([np.array([], dtype=list) for _ in range(sgv['num_bank'])]),  # 信息列表之于流动性短缺的银行之债务方银行编号 list_debtors_in_illiquid
    cre_br=np.array([np.array([], dtype=list) for _ in range(sgv['num_bank'])]),  # 信息列表之于破产的银行之债权方银行编号 list_creditors_in_bankrupt
    deb_br=np.array([np.array([], dtype=list) for _ in range(sgv['num_bank'])]),  # 信息列表之于破产的银行之债务方银行编号 list_debtors_in_bankrupt

    ###########################
)

# %% # 导出 agents 变量

for year in sgv['list_agents_yearName']:
    with open("./BankCommercial" + f"_year={year}" + ".pkl", 'wb') as f:
        pickle.dump(set_bankCommercial_variables, f)
    with open("./BankInterbank" + f"_year={year}" + ".pkl", 'wb') as f:
        pickle.dump(set_bankInterbank_variables, f)
