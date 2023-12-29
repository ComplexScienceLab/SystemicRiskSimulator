"""
安装、初始化数据机
"""

from SystemicRiskSimulator.external_packages import np, pd, deepcopy, pickle, Path
from SystemicRiskSimulator.core.define.define_agents import BankCommercial, BankInterbank
from SystemicRiskSimulator.core.define.define_consts import CONST
from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv
# from SystemicRiskSimulator.core.define.define_parameterVariables import para
from SystemicRiskSimulator.core.define.define_agentDataCollection import AgentDataCollection

# from SystemicRiskSimulator.core.functions.fun_finance import Finance

pass  # end import


class DataInstaller:
    """
    安装、初始化数据机
    """

    A_data = AgentDataCollection([], [])

    @classmethod
    def set_imported_values_to_Bank_variables(cls, para: dict):
        """
        导入数据以初始化银行主体众、银行间主体众变量

        Args:
            para (dict): 参数集

        Returns:
            bank(BankCommercial): 银行主体众
            interbank(BankInterbank): 银行间主体众

        """

        with open(Path(sgv['folderpath_agents'], "BankCommercial" + f"_year={para['year']}" + ".pkl"), 'rb') as f:
            dict_bankCommercial = pickle.load(f)
        with open(Path(sgv['folderpath_agents'], "BankInterbank" + f"_year={para['year']}" + ".pkl"), 'rb') as f:
            dict_bankInterbank = pickle.load(f)

        # ## NOTE 当用对象字段数据结构时：
        # bank, interbank = cls.set_default_values_to_Bank_variables()
        # bank.__dict__ = deepcopy(dict_bankCommercial)
        # interbank.__dict__ = deepcopy(dict_bankInterbank)

        ## NOTE 当用pandas数据结构时：
        bank = pd.Series()
        for k, v in deepcopy(dict_bankCommercial).items():
            bank[k] = v
        interbank = pd.Series()
        for k, v in deepcopy(dict_bankInterbank).items():
            interbank[k] = v

        return bank, interbank

        pass  # function

    @classmethod
    def set_manually_values_to_Bank_variables(cls):
        """手动设置以初始化银行变量"""

        from SystemicRiskSimulator.core.define.define_agentsVariables import dict_bankCommercial, dict_bankInterbank

        # ## NOTE 当用对象字段数据结构时：
        # bank, interbank = cls.set_default_values_to_Bank_variables()
        # bank.__dict__ = deepcopy(dict_bankCommercial)
        # interbank.__dict__ = deepcopy(dict_bankInterbank)

        ## NOTE 当用pandas数据结构时：
        bank = pd.Series()
        for k, v in deepcopy(dict_bankCommercial).items():
            bank[k] = v
        interbank = pd.Series()
        for k, v in deepcopy(dict_bankInterbank).items():
            interbank[k] = v

        return bank, interbank
        pass  # function

    # @classmethod
    # def set_randomly_values_to_Bank_variables(cls):
    #     # """随机化初始化银行变量 HACK 这个功能以后有需要再实现。"""
    #     # bank, interbank = cls.set_default_values_to_Bank_variables()
    #     pass  # function

    @classmethod
    def set_default_values_to_Bank_variables(cls):
        """
        设置默认值给银行主体众、银行间主体众变量。

        Returns:
            bank(BankCommercial): 银行主体众
            interbank(BankInterbank): 银行间主体众
        """
        bankCommercial: BankCommercial = BankCommercial(
            id_agent=CONST(sgv['num_bank']).RANGE1.copy(),  # agent 之编号 id
            abbr=np.full((sgv['num_bank'], 1), ""),  # 缩写 abbr
            name=np.full((sgv['num_bank'], 1), ""),  # 全名 name
            A_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总资产 A_all: $A_all=A_IB+A_exIB$
            A_IB_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间资产加总 A_IB_all
            A_exIB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间资产 A_exIB: $A_exIB=A_P+A_Q+A_R+A_other$
            A_P=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行贷款给非金融部门（非银行金融部门）之资产（非流动性资产） A_P
            A_Q=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行持有超额准备金（流动性资产） A_Q
            A_R=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行持有法定准备金（非流动性资产） A_R
            A_other=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行持有的其它资产（NOTE 包括：研究不涉及的资产科目、会计科目之其他资产、不重要且不明确的资产科目） A_other
            Z_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 总负债 Z_all: $Z_total=Z_IB+Z_exIB$
            Z_IB_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间负债加总 Z_IB_all
            Z_exIB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 非银行间负债 Z_exIB: $Z_exIB=Z_D+Z_CB+Z_other$
            Z_CB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 持有央行之负债 Z_CB
            Z_D=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行获得居民部门存款（非流动性负债） Z_D
            Z_other=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行持有的其他负债（NOTE 包括：研究不涉及的负债科目、会计科目之其他负债、不重要且不明确的负债科目） Z_other
            E_all=CONST(sgv['num_bank']).ZEROS1.copy(),  # 所有者权益 E_all
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
            Loss_IB=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间市场冲击损失 Loss_IB
            Loss_IB_def_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间资产负债违约冲击损失 Loss_IB_def_t
            Loss_IB_run_t=CONST(sgv['num_bank']).ZEROS1.copy(),  # 银行间负债流动性挤兑冲击损失 Loss_IB_run_t
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
            list_bankrupt=np.full(sgv['num_bank'], list),  # 列表之于破产的银行编号 list_bankrupt

        )

        bankInterbank: BankInterbank = BankInterbank(
            id_agent=CONST(sgv['num_bank']).RANGE2.copy(),  # agent 之间之关联编号 id
            A_IB=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间资产邻接矩阵 A_IB
            Z_IB=CONST(sgv['num_bank']).ZEROS2.copy(),  # 银行间负债邻接矩阵 Z_IB
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
            Loss_IB_run=CONST(sgv['num_bank']).TRUE2.copy(),  # 银行间负债流动性挤兑冲击损失 Loss_IB_run
            is_exposure=CONST(sgv['num_bank']).FALSE2.copy(),  # 信息邻接矩阵之于是否有银行间敞口 is_exposure
            on=CONST(sgv['num_bank']).TRUE2.copy(),  # 信息邻接矩阵之于银行间存在的 is_on
            off=CONST(sgv['num_bank']).FALSE2.copy(),  # 信息邻接矩阵之于银行间已退出不存在的 is_off
            hel=CONST(sgv['num_bank']).FALSE2.copy(),  # 信息邻接矩阵之于银行间健康的 is_healthy
            isv=CONST(sgv['num_bank']).FALSE2.copy(),  # 信息邻接矩阵之于银行间资不抵债的 is_insolvent
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

        ## 获取各 agents 之字段数据结构为字典变量
        dict_bankCommercial = vars(bankCommercial)
        dict_bankInterbank = vars(bankInterbank)

        # ## NOTE 当用对象字段数据结构时：
        # bank, interbank = cls.set_default_values_to_Bank_variables()
        # bank.__dict__ = deepcopy(dict_bankCommercial)
        # interbank.__dict__ = deepcopy(dict_bankInterbank)

        ## NOTE 当用pandas数据结构时：
        bank = pd.Series()
        for k, v in deepcopy(dict_bankCommercial).items():
            bank[k] = v
        interbank = pd.Series()
        for k, v in deepcopy(dict_bankInterbank).items():
            interbank[k] = v

        return bank, interbank
        pass  # function

    @classmethod
    def install_data(cls, init_data_method: str, sgv: dict, para: dict):
        """
        不同的初始化方式。

        参数init_data_method可选项：

        - ``import data``:  导入数据以初始化

        - ``manually``:  手动设置以初始化；

        - ``randomly``:  生成随机数据以初始化； #HACK 按需添加

        - ``only init``:  仅单纯初始化；

        在模型中使用类似`BB.Z[b]`这样的形式，目的是为了提取每个变量字段内部的数值做处理。不直接使用`BB.Z`，这样仅仅处理字段自身。例如`BB.Z[b] = BB.A[b]`将`BB.A`内的数值赋值给`BB.Z`，而`BB.Z = BB.A`是将`BB.A`作为引用赋值给`BB.Z`，而不是将`BB.A`的数值赋值给`BB.Z`。这样的意义是保证各个字段数据不会引用错乱。

        Args:
            init_data_method (): 初始化数据的方式
            sgv (dict): 模拟器全局变量
            para (dict): 参数变量

        Returns: A

        """

        if init_data_method == "import data":
            BB, IB = cls.set_imported_values_to_Bank_variables(para)  # 导入数据以初始化银行变量
        elif init_data_method == "set manually":
            BB, IB = cls.set_manually_values_to_Bank_variables()  # 手动设置以初始化银行变量
        elif init_data_method == "randomly":
            BB, IB = cls.set_randomly_values_to_Bank_variables()  # HACK 按需添加
        elif init_data_method == "only init":
            BB, IB = cls.set_default_values_to_Bank_variables()
        else:
            raise ("关键词" + str(init_data_method) + "取值错误！")
            pass  # if

        sgv['num_bank'] = len(BB.on)  # 获取 agents 之个体数量

        # HACK 后续需要统一这两个变量的用法，防止混乱使用
        b = (BB.on | BB.off).reshape(-1, 1)  # 临时设置A.BB示性变量
        ib = ((BB.on | BB.off).reshape(-1, 1) & (BB.on | BB.off).reshape(1, -1))  # 临时设置IB示性变量

        ## 构建Agent模型
        # NOTE 注意这时候`b`、`ib`变量在后续过程中没有发生变动。

        ## HACK 当用pandas数据结构时：
        A = pd.Series([BB, IB, b, ib], index=['BB', 'IB', 'b', 'ib'])

        # ## HACK 当用对象字段数据结构时。
        # A = SystemicRiskAgent(
        #     0,  # 编号（必备的）
        #     BB,  # 商业银行群
        #     b,  # 商业银行群示性变量
        #     IB,  # 银行间邻接矩阵
        #     ib,  # 银行间邻接矩阵示性变量
        # )

        # cls.initialize_data(A)  # 更新各银行之变量，在第一回合初始时 #HACK 无用可删除
        return A
        pass  # function

    # @classmethod
    # def initialize_data(cls, A):  #HACK 无用可删除
    #     ## 更新各银行之变量，在第一回合初始时
    #     # update=sgv['update']
    #     # @Executer.execute
    #     # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='clear transfer all')  # 更新各银行之所有交易变量，在第一回合开始时#BUG 删除后是否影响后续实验初始化数据？有影响！
    #     # Finance.update_finance_variables(A.BB, A.IB, A.b, A.ib, by_way='all')  # 更新各银行之所有变量，在第一回合开始时
    #     return A
    #     pass  # function

    pass  # class
