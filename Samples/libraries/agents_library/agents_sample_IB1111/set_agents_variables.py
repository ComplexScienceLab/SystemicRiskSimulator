"""
设置多主体变量
"""
from SystemicRiskSimulator.external_packages import pickle, Path
from SystemicRiskSimulator.core.define.define_type import *
from SystemicRiskSimulator.core.functions.generation.fun_calibrate_interbank_exposure import calibrate_bilateral_exposure_by_ME_algorithm_by_R_package

pass  # end import

# %% 预处理
# 删除 agents 内所有文件
Path(Path.cwd(), 'agents').mkdir(exist_ok=True)
folderpath_agents = Path(Path.cwd(), 'agents')
for file in folderpath_agents.iterdir():
    if file.is_file():
        file.unlink()

# %% #NOTE 设置项
# 设置金额单位
money_unit = MoneyType(1e9)  # 金额单位：十亿

list_年份 = ['2012', '2013']  # 设置 agents 初始数据列表
list_agents_networkDensity = [0.25, 1.0]  # 设置 agents 初始数据列表
num_bank = 5

for year in list_年份:
    for density in list_agents_networkDensity:
        # %% 设置银行个体变量
        set_bankCommercial_variables = dict(

            # 初始化商业银行群 bank_commercial
            id_agent=np.arange(num_bank),  # agent 之编号 id
            abbr=np.arange(num_bank).astype(AbbrType),  # 缩写 abbr
            fullName=np.array(["Bank_1", "Bank_2", "Bank_3", "Bank_4", "Bank_5"], dtype=NameType),  # 全名 fullName
            A_all=np.zeros(num_bank),  # 总资产 A_all: $A_all=A_IB+A_exIB$
            A_IB_all=np.array([2185.24, 398.37, 730.99, 1357.75, 2717.39], dtype=MoneyType),  # 银行间资产加总 A_IB_all
            A_P=np.array([1631.73, 4303.24, 3379.72, 4351.47, 620.69], dtype=MoneyType),  # 银行贷款给非金融部门（非银行金融部门）之资产（非流动性资产） A_P
            A_Q=np.array([477.125, 587.693, 513.847, 713.662, 417.257], dtype=MoneyType),  # 银行持有超额准备金（流动性资产） A_Q
            A_R=np.zeros(num_bank),  # 银行持有法定准备金（非流动性资产） A_R #NOTE 这里用准备金率计算得到。
            A_other=np.zeros(num_bank),  # 银行持有的其他资产（NOTE 包括：研究不涉及的资产科目、会计科目之其他资产、不重要且不明确的资产科目） A_other
            Z_all=np.zeros(num_bank),  # 总负债 Z_all: $Z_total=Z_IB+Z_exIB$
            Z_IB_all=np.array([959.6, 1844.24, 1253.34, 2851.85, 480.71], dtype=MoneyType),  # 银行间负债加总 Z_IB_all
            Z_CB=np.zeros(num_bank),  # 持有央行之负债 Z_CB
            Z_D=np.array([3160.99, 3231.37, 3184.36, 3311.51, 3122.9], dtype=MoneyType),  # 银行获得居民部门存款（非流动性负债） Z_D
            Z_other=np.zeros(num_bank),  # 银行持有的其他负债（NOTE 包括：研究不涉及的负债科目、会计科目之其他负债、不重要且不明确的负债科目） Z_other
            E_all=np.array([173.505, 213.693, 186.857, 259.522, 151.727], dtype=MoneyType),  # 所有者权益 E_all
            Shock_t=np.zeros(num_bank),  # 总冲击目标 Shock_t $Shock_t = Shock_exIB_t+Shock_IB_t$
            Shock_s=np.zeros(num_bank),  # 总冲击源头 Shock_s $Shock_s = Shock_exIB_s+Shock_IB_s$
            Shock_P_def_t=np.zeros(num_bank),  # 银行之厂商贷款违约损失冲击目标 Shock_P_def_t
            Shock_D_def_s=np.zeros(num_bank),  # 银行存款违约损失冲击源头 Shock_D_def_s
            Shock_IB_def_s=np.zeros(num_bank),  # 银行间违约损失冲击源头 Shock_IB_def_s
            Shock_IB_def_t=np.zeros(num_bank),  # 银行间违约损失冲击目标 Shock_IB_def_t
            Loss_t=np.zeros(num_bank),  # = deepcopy(ZEROS1)  # 银行总损失目标 Loss_t
            Loss_exIB_def_t=np.zeros(num_bank),  # = deepcopy(ZEROS1)  # 非银行间资产负债违约损失冲击损失目标 Loss_exIB_def_t
            Loss_IB_def_t=np.zeros(num_bank),  # = deepcopy(ZEROS1)  # 银行间资产负债违约损失冲击损失目标 Loss_IB_def_t
            Default_s=np.zeros(num_bank),  # = deepcopy(ZEROS1)  # 银行总违约量 Default_s
            Default_IB_def_s=np.zeros(num_bank),  # = deepcopy(ZEROS1)  # 银行间在违约损失冲击的违约量 Default_IB_s
            Default_D_def_s=np.zeros(num_bank),  # = deepcopy(ZEROS1)  # 非银行间在违约损失冲击的存款违约量 Default_D_def_s
            exist=np.full(num_bank, True),  # 示性向量之于银行是否存在 is_exist
            exit=np.full(num_bank, False),  # 示性向量之于银行是否已退出不存在 is_exit
            hel=np.full(num_bank, True),  # 示性向量之于银行是否健康 is_healthy
            isv=np.full(num_bank, False),  # 示性向量之于银行是否资不抵债 is_insolvent
            br=np.full(num_bank, False),  # 示性向量之于银行是否破产 is_bankrupt
            con=np.full(num_bank, False),  # 示性向量之于银行当前轮次是否传染出去 is_contagion
            inf=np.full(num_bank, False),  # 示性向量之于银行当前轮次是否遭受感染 is_infect
        )

        # %% 设置银行间邻接矩阵
        set_bankInterbank_variables = dict(

            # 初始化银行间邻接矩阵 interbank
            id_agent=(np.arange((num_bank * num_bank))).reshape(num_bank, num_bank),  # agent 之间之关联编号 id
            A_IB=np.array([
                [0, 1728.55, 0, 134.46, 322.23],
                [109.35, 0, 289.02, 0, 0],
                [730.99, 0, 0, 0, 0],
                [119.26, 115.69, 964.32, 0, 158.48],
                [0, 0, 0, 2717.39, 0]
            ], dtype=MoneyType),  # 银行间资产邻接矩阵 A_IB
            Z_IB=np.array([
                [0, 1728.55, 0, 134.46, 322.23],
                [109.35, 0, 289.02, 0, 0],
                [730.99, 0, 0, 0, 0],
                [119.26, 115.69, 964.32, 0, 158.48],
                [0, 0, 0, 2717.39, 0]
            ], dtype=MoneyType).T,  # 银行间负债邻接矩阵 Z_IB
            Shock_IB=np.zeros((num_bank, num_bank)),  # 银行间冲击 Shock_IB: $Shock_IB=Shock_IB_def$
            Shock_IB_def=np.zeros((num_bank, num_bank)),  # 银行间违约损失冲击 Shock_IB_def
            Loss_IB=np.zeros((num_bank, num_bank)),  # 银行间市场冲击损失 Loss_IB
            Loss_IB_def=np.zeros((num_bank, num_bank)),  # 银行间资产负债违约冲击损失 Loss_IB_def
            Default_IB=np.zeros((num_bank, num_bank)),  # 银行间违约量 Default_IB
            exist=np.full((num_bank, num_bank), True),  # 示性邻接矩阵之于银行间存在的 is_exist
            exit=np.full((num_bank, num_bank), False),  # 示性邻接矩阵之于银行间已退出不存在的 is_exit
            hel=np.full((num_bank, num_bank), True),  # 示性邻接矩阵之于银行间健康的 is_healthy
            isv=np.full((num_bank, num_bank), False),  # 示性邻接矩阵之于银行间资不抵债的 is_insolvent
            br=np.full((num_bank, num_bank), False),  # 示性邻接矩阵之于银行间破产的 is_bankrupt

            ###########################
        )

        # %% # 导出 agents 变量

        Path(Path.cwd(), 'agents').mkdir(exist_ok=True)
        folderpath_agents = Path(Path.cwd(), 'agents')

        with open(Path(folderpath_agents, f"BB-year={year}-density={density:.2f}.pkl"), 'wb') as f:
            pickle.dump(set_bankCommercial_variables, f)
        with open(Path(folderpath_agents, f"IB-year={year}-density={density:.2f}.pkl"), 'wb') as f:
            pickle.dump(set_bankInterbank_variables, f)

        pass  # for 网络连接密度
    pass  # for 年份

print("运行完毕！")
