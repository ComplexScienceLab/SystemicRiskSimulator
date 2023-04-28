"""功能函数集：计算构建银行与银行间相关状态及其转换。"""

from PySystemicRiskLab import np
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_consts import LESS1
from PySystemicRiskLab.core.define.define_environmentVariables import env
from PySystemicRiskLab.core.define.define_type import StateType

pass  # end import


class BankState:
    bank: BankCommercial
    interbank: BankInterbank
    is_updated_states_list: bool
    ## 状态集合列表`states_list`
    states_list: list

    ## 计算状态函数集合列表`calc_state_functions_list`
    calc_state_functions_list: list

    # @property
    # def calc_state_functions_list(cls):
    #     calc_state_functions_list = [cls.calc_isOn, cls.calc_isHealthy, cls.calc_isInsolvent, cls.calc_isIlliquid, cls.calc_isBankrupt, cls.calc_isOff]
    #     return calc_state_functions_list
    #     pass  # def

    ## 状态关系集合列表`relation_states_list`
    relation_states_list: list

    ## 更新状态函数集合列表`update_state_functions_list`
    update_state_functions_list: list
    # @property
    # def update_state_functions_list(cls):
    #     return [cls.update_if_equity, cls.update_if_handle, cls.update_if_none, cls.update_if_uncertain, cls.update_if_parent, cls.update_if_child, cls.update_if_exclusive]
    #     pass  # def

    ## 状态关系邻接矩阵`relation_adjacent_matrix`
    relation_adjacent_matrix: list

    ## 计算状态函数字典`calc_states_dict`
    calc_states_dict: dict

    ## 更新状态函数字典`update_states_dict`
    update_states_dict: dict

    ## 状态关系索引表`relation_indices`
    relation_indices: list

    # @property
    # def relation_indices(self):
    #     xx, yy = np.meshgrid(self.states_list, self.states_list)
    #     self.relation_indices = np.column_stack([xx.ravel(), yy.ravel(), self.relation_adjacent_matrix.ravel()])
    #     return self.relation_indices
    #     pass  # def

    ## 状态对应更新关系字典列表`states_relation_adjacent_dict_list`
    states_relation_adjacent_dict_list: dict

    @classmethod
    def build_state_const_variables(cls):
        """
        构建各类状态常量变量。
        Returns:

        """

        ## 示性向量之各状态是否已经更新
        cls.is_updated_states_list = np.full((len(cls.states_list),len(cls.states_list)), False, dtype=bool)

        ## 设置状态集合列表`states_list`
        cls.states_list = [
            'on',
            'hel',
            'isv',
            'ilq',
            'br',
            'off',
        ]

        ## 计算状态函数集合列表`calc_state_functions_list`
        cls.calc_state_functions_list = [cls.calc_isOn, cls.calc_isHealthy, cls.calc_isInsolvent, cls.calc_isIlliquid, cls.calc_isBankrupt, cls.calc_isOff]

        ## 设置状态关系集合列表`relation_states_list`
        cls.relation_states_list = [
            '同',
            '手',
            '无',
            '惑',
            '父',
            '子',
            '斥',
        ]
        ## 构建待计算的状态字典列表`calc_states_dict`
        cls.calc_states_dict = [{i[0]: i[1]} for i in zip(cls.states_list, cls.calc_state_functions_list)]

        ## 设置状态关系邻接矩阵`relation_adjacent_matrix`
        cls.relation_adjacent_matrix = [
            ['同', '父', '父', '父', '父', '无', ],
            ['子', '同', '惑', '惑', '无', '无', ],
            ['子', '斥', '同', '无', '手', '无', ],
            ['子', '斥', '无', '同', '手', '无', ],
            ['子', '无', '惑', '惑', '同', '手', ],
            ['无', '无', '无', '无', '斥', '同', ],
        ]

        ## 构建状态关系索引表。
        xx, yy = np.meshgrid(cls.states_list, cls.states_list)
        cls.relation_indices = np.column_stack([xx.ravel(), yy.ravel(), np.asarray(cls.relation_adjacent_matrix).ravel()])

        ## 更新状态函数集合列表`update_state_functions_list`
        cls.update_state_functions_list = [cls.update_if_equity, cls.update_if_handle, cls.update_if_none, cls.update_if_uncertain, cls.update_if_parent, cls.update_if_child, cls.update_if_exclusive]

        ## 构建待更新的状态字典列表`update_states_dict`
        cls.update_states_dict = [{i[0]: i[1]} for i in zip(cls.relation_states_list, cls.update_state_functions_list)]

        ## 根据`relation_adjacent_matrix`构建待更新的状态计算方法列表
        for i, row in enumerate(cls.relation_adjacent_matrix):
            cls.states_relation_adjacent_dict_list[cls.states_list[i]] = np.array([cls.update_states_dict[j] for j in row])
            pass

        ## 构建状态转移字典列表
        cls.state_transitions_list = zip(cls.states_list, cls.states_list, cls.relation_adjacent_matrix)

        pass  # def

    @classmethod
    def calc_state(cls, state: StateType):
        """
        计算状态。#TODO

        Args:
            state (StateType): 待计算的状态

        Returns:

        """
        ## 根据状态计算相应的状态
        cls.calc_states_dict[state](cls.bank, cls.interbank)

        state_difference = None  # 状态变动部分
        return state_difference
        pass

    @classmethod
    def get_relation_of_states(cls, source_state: StateType, target_state: StateType):
        """
        获取两个状态之间的关系。

        同一种状态标记【同】；

	    手动更新标记【手】；

	    不存在直接关系标记【无】；

	    非确定的关系标记【惑】；

	    父子关系，分别标记【父】、【子】；

	    互相排斥关系，标记【斥】；

	    其它可以推导关系，标记【推】；
        """
        # return cls.relation_indices[(cls.relation_indices[:, 0] == source_state) & (cls.relation_indices[:, 1] == target_bank_state), 2]
        return cls.relation_indices[(cls.relation_indices[:, 0] == source_state), 2]
        pass  # def

    @classmethod
    def update_state(cls, state: [StateType]):
        """
        更新状态

        Args:
            state (StateType): 待更新的状态

        Returns:

        """
        ## 根据状态之间的关系更新相应的状态
        cls.update_states_dict[state](cls.bank, cls.interbank)

        pass  # def

    @classmethod
    def init_list_of_relation_in_state_of_banks(cls, bank: BankCommercial, interbank: BankInterbank):
        """
        初始化银行状态关系列表
        """
        interbank.cre = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="creditor")
        interbank.deb = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="debtor")
        pass

    @classmethod
    def update_state_to_target_from_source(cls, target_state: StateType, target_inter_state: StateType & StateType.T, source_state_difference: StateType):  # NOW
        # target_bank_state = ((~target_bank_state & source_state_difference) | (target_bank_state & ~source_state_difference)) & cls.bank.on  # NOTE和下面一行的语句实现结果是等价的，但是运算速度可能慢一点
        target_state[source_state_difference] = ~target_state[source_state_difference]
        target_inter_state[source_state_difference & source_state_difference.T] = ~target_inter_state[source_state_difference & source_state_difference.T]
        pass  # def

    @classmethod
    def calc_isHealthy(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行健康的。"""
        condition = ((bank.E_all >= LESS1) & (bank.A_Q >= LESS1) & (bank.Shock_def_t + LESS1 <= bank.E_all) & (bank.Shock_run_t + LESS1 <= bank.A_Q) & (bank.on))
        difference = (bank.hel != condition)
        if difference.any():
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            return difference
            pass
        pass

    @classmethod
    def calc_isInsolvent(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行资不抵债的。"""
        condition = (((bank.A_all < bank.Z_all + LESS1) | (bank.E_all < LESS1) | (bank.Shock_def_t + LESS1 > bank.E_all)) & bank.on)
        difference = (bank.isv != condition)
        if difference.any():
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="creditor")
            interbank.deb_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="debtor")
            return difference
            pass
        pass

    @classmethod
    def calc_isIlliquid(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行流动性短缺的。"""
        condition = (((bank.A_Q < LESS1) | (bank.Shock_run_t + LESS1 > bank.A_Q)) & bank.on)
        difference = (bank.ilq != condition)
        if difference.any():
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="creditor")
            interbank.deb_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="debtor")
            return difference
            pass
        pass

    @classmethod
    def calc_isBankrupt(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行破产的。"""
        condition = (bank.isv | bank.ilq)  # TODO 这个仅仅是目前基准算法简化的做法
        difference = (bank.br != condition)
        if difference.any():
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="creditor")
            interbank.deb_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="debtor")
            return difference
            pass
        pass

    @classmethod
    def is_updated_relation_of_states(cls, source_state: StateType, target_state: StateType):
        """判断是否有更新状态之关系"""
        pass  # def

    @classmethod
    def update_if_equity(cls, source_state: StateType, target_state: StateType):
        "当关系是【同】的时候，更新"
        pass  # def

    @classmethod
    def update_if_handle(cls, source_state: StateType, target_state: StateType):
        "当关系是【手】的时候，更新"
        pass  # def

    @classmethod
    def update_if_none(cls, source_state: StateType, target_state: StateType):
        "当关系是【无】的时候，更新"
        pass  # def

    @classmethod
    def update_if_uncertain(cls, source_state: StateType, target_state: StateType):
        "当关系是【惑】的时候，更新"
        pass  # def

    @classmethod
    def update_if_parent(cls, source_state: StateType, target_state: StateType):
        "当关系是【父】的时候，更新"
        pass  # def

    @classmethod
    def update_if_child(cls, source_state: StateType, target_state: StateType):
        "当关系是【子】的时候，更新"
        """汇总示性向量之于银行存在的。"""
        condition = (bank.hel | bank.isv | bank.ilq | bank.br)
        if (bank.on != condition).any():
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            # interbank.listOfCreditorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "creditor") #HACK，未定义，无用。
            # interbank.listOfDebtorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "debtor") #HACK，未定义，无用。
            pass

        pass  # def

    @classmethod
    def update_if_exclusive(cls, source_state: StateType, target_bank_state: StateType, target_interbank_state: (StateType & StateType.T), difference: StateType):
        "当关系是【斥】的时候，更新"
        """
        更新示性向量之于银行流动性短缺的，来自健康的。

        Args:
            cls ():
            bank (BankCommercial): 商业银行个体众
            interbank (BankInterbank): 商业银行间个体众
            difference (StateType): 源状态的变动示性向量

        Returns:

        """
        # bank.ilq = ((~bank.ilq & difference) | (bank.ilq & ~difference)) & bank.on  # NOTE和下面一行的语句实现结果是等价的，但是运算速度可能慢一点
        target_bank_state[difference] = ~target_bank_state[difference]
        target_interbank_state[difference & difference.T] = ~target_interbank_state[difference & difference.T]
        interbank.cre_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=target_bank_state, goal="creditor")
        interbank.deb_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=target_bank_state, goal="debtor")
        # return target_bank_state,target_interbank_state
        pass  # def

    @classmethod
    def update_all_cre_and_deb(cls):
        """更新银行间市场interbank之各状态下之信息列表之于各银行之债权方与债务方之银行编号。"""
        cls.interbank.cre_isv = cls.calc_list_of_relation_in_state_of_banks(cls.interbank, isState=cls.bank.isv, goal="creditor")
        cls.interbank.deb_isv = cls.calc_list_of_relation_in_state_of_banks(cls.interbank, isState=cls.bank.isv, goal="debtor")
        cls.interbank.cre_ilq = cls.calc_list_of_relation_in_state_of_banks(cls.interbank, isState=cls.bank.ilq, goal="creditor")
        cls.interbank.deb_ilq = cls.calc_list_of_relation_in_state_of_banks(cls.interbank, isState=cls.bank.ilq, goal="debtor")
        cls.interbank.cre_br = cls.calc_list_of_relation_in_state_of_banks(cls.interbank, isState=cls.bank.br, goal="creditor")
        cls.interbank.deb_br = cls.calc_list_of_relation_in_state_of_banks(cls.interbank, isState=cls.bank.br, goal="debtor")
        pass  # def

    @classmethod
    def together_isOn(cls, bank: BankCommercial, interbank: BankInterbank):  # HACK可以删除
        """汇总示性向量之于银行存在的。"""
        condition = (bank.hel | bank.isv | bank.ilq | bank.br)
        if (bank.on != condition).any():
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            # interbank.listOfCreditorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "creditor") #HACK，未定义，无用。
            # interbank.listOfDebtorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "debtor") #HACK，未定义，无用。
            pass
        pass

    @classmethod
    def calc_isOn(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行存在的。"""  # TODO
        condition = (bank.hel | bank.isv | bank.ilq | bank.br)
        if (bank.on != condition).any():
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            # interbank.listOfCreditorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "creditor") #HACK，未定义，无用。
            # interbank.listOfDebtorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "debtor") #HACK，未定义，无用。
            pass
        pass

    @classmethod
    def calc_isOff(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行退出的。"""
        condition = bank.br | bank.off
        if (bank.off != condition).any():
            bank.off = condition
            interbank.off = (bank.off & bank.off.T)
            pass
        pass

    @classmethod
    def calc_isNeededBoIB(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行需要偿还银行间负债的。"""
        bank.is_needed_BoIB = ((bank.Shock_IB_run_ilq_t > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledBoIB(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行能够偿还银行间负债的。"""
        bank.is_enabled_BoIB = ((bank.Shock_IB_run_ilq_t > 0) & (bank.A_Q > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledBoIB_from_isNeededBoIB(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行能够偿还银行间负债的，从需要偿还银行间负债的。"""
        bank.is_enabled_BoIB = (bank.is_needed_BoIB & (bank.A_Q > 0))
        pass

    @classmethod
    def calc_isNeededBoD(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行需要偿还居民部门存款的。"""
        bank.is_needed_BoD = ((bank.Shock_D_run_t > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledBoD(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行能够偿还居民部门存款的。"""
        bank.is_enabled_BoD = ((bank.Shock_D_run_t > 0) & (bank.A_Q > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledBoD_from_isNeededBoD(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行能够偿还居民部门存款的，从需要偿还居民部门存款的。"""
        bank.is_enabled_BoD = (bank.is_needed_BoD & (bank.A_Q > 0))
        pass

    @classmethod
    def calc_isNeededLiP(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行需要收回厂商贷款的。"""
        bank.is_needed_LiP = ((bank.Shock_P_run_s > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledLiP(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行能够收回厂商贷款的。"""
        bank.is_enabled_LiP = ((bank.Shock_P_run_s > 0) & bank.on)  # HACK后续可能会补充条件 & producer.A_Q > 0
        pass

    @classmethod
    def calc_isEnabledLiP_from_isNeededLiP(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行能够收回厂商贷款的，从需要收回厂商贷款的。"""
        bank.is_enabled_LiP = (bank.is_needed_LiP)  # HACK后续可能会补充条件 & producer.A_Q > 0
        pass

    @classmethod
    def calc_list_of_relation_in_state_of_banks(cls, interbank: BankInterbank, isState: StateType, goal: str):
        """
        计算信息列表之于各状态银行之各关联银行。

        参数``goal``可选项：
            - ``debtor``:  计算对应的债务方银行；
            - ``creditor``:  计算对应的债权方银行；

        Args:
            interbank (BankInterbank): BankInterbank
            isState ():
            goal (str): 参数，确定计算债务方或债权方。

        Returns: list_of_relation_in_state_of_banks

        """

        # 计算示性矩阵之于银行间风险敞口的
        if goal == "debtor":
            is_exposure = ((interbank.A_IB > 0.0) & isState)
        elif goal == "creditor":
            is_exposure = ((interbank.Z_IB > 0.0) & isState)
        else:
            pass
        list_of_relation_in_state_of_banks = np.array([np.array(None) for i in range(env['num_bank'])])
        for i in range(env['num_bank']):
            list_of_relation_in_state_of_banks[i] = np.where(is_exposure[i, :])[0]  # 获取对应状态下的债权或者债务关系的银行列表
            pass
        return list_of_relation_in_state_of_banks
        pass

    @classmethod
    def update_B_state(cls, way: str = 'any'):  # TODO
        """
        更新各银行之状态。

        参数``target``可选项：#TODO

        - ``any``:  到任意状态；
        - ``healthy``:  到健康状态；
        - ``insolvent``:  到资不抵债状态；
        - ``illiquid``:  到流动性短缺状态；
        - ``bankrupt``:  到破产状态；
        - ``off``:  到退出状态；
        - ``needed repay IB``:  到是否需要偿还银行间借款状态；
        - ``enabled repay IB``:  到是否可以偿还银行间借款状态；
        - ``needed repay Z_D``:  到是否需要偿还居民存款状态；
        - ``enabled repay Z_D``:  到是否需要偿还借款状态；
        - ``needed collect A_P``:  到是否可以收回厂商贷款状态；
        - ``enabled collect A_P``:  到是否可以收回厂商贷款状态；


        Args:
            bank ():
            interbank ():
            target (): 参数，转移状态目标；
            source (): 参数，转移状态源头；

        Returns:

        """

        ## 1. 指定而计算源状态；
        state_difference = cls.calc_state(way)
        cls.is_updated_states_list[np.where(way == cls.states_list)] = True

        ## 重复步骤2至3，直至无状态需要更新；
        while cls.is_updated_states_list.all()==True:
            ## 2. 决策是否更新向状态：根据状态关系表、是否自动更新情况、状态更新情况决策；
            relations = cls.get_relation_of_states(way)

            ## 3. 需要更新的状态，更新相应的向状态；
            cls.update_state(relations)
            cls.is_updated_states_list[]

            # cls.is_updated_states_list = np.array([False for i in range(len(cls.states_list))])
            # for i in range(len(cls.states_list)):
            #     cls.update_state(cls.states_list[i])
            #     pass
            # pass#HACK AI补全


        ## 更新银行间市场interbank之各状态下之信息列表之于各银行之债权方与债务方之银行编号。
        cls.update_all_cre_and_deb()
        pass  # def

        if target == 'any':  # FIXME 这个可能有缺陷:
            if source == 'any':
                cls.init_list_of_relation_in_state_of_banks(bank, interbank)
                _ = cls.calc_isInsolvent(bank, interbank)
                _ = cls.calc_isIlliquid(bank, interbank)
                _ = cls.calc_isHealthy(bank, interbank)
                _ = cls.calc_isBankrupt(bank, interbank)
                cls.together_isOn(bank, interbank)
                # calc_isOff(bank, interbank) # TODO后续添加
                # calc_isOn(bank, interbank) # TODO后续添加
            elif source == 'healthy':
                hel_difference = cls.calc_isHealthy(bank, interbank)
                _ = cls.calc_isInsolvent(bank, interbank)
                _ = cls.calc_isIlliquid(bank, interbank)
                cls.update_state_to_target_from_source(bank.hel, interbank.hel, isv_difference)
                ilq_difference = cls.calc_isIlliquid(bank, interbank)
                cls.update_state_to_target_from_source(bank.hel, interbank.hel, ilq_difference)
            elif source == 'insolvent':
                isv_difference = cls.calc_isInsolvent(bank, interbank)
                cls.update_state_to_target_from_source(bank.hel, interbank.hel, isv_difference)
                # br_difference = cls.calc_isBankrupt(bank, interbank)
            elif source == 'illiquid':
                ilq_difference = cls.calc_isIlliquid(bank, interbank)
                cls.update_state_to_target_from_source(bank.hel, interbank.hel, ilq_difference)
                # br_difference = cls.calc_isBankrupt(bank, interbank)
            elif source == 'bankrupt':
                cls.calc_isBankrupt(bank, interbank)
                # HACK是否需要加入破产到退出呢？
            elif source == 'off':
                off_difference = cls.calc_isOff(bank, interbank)
                cls.update_state_to_target_from_source(bank.br, interbank.br, off_difference)
                cls.together_isOn(bank, interbank)
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'healthy':
            if source == 'any':
                hel_difference = cls.calc_isHealthy(bank, interbank)
                cls.update_isInsolvent_from_isHealthy(bank, interbank)
                cls.update_isIlliquid_from_isHealthy(bank, interbank)
            elif source == 'healthy':
                # @testprintln "无须更新！"
                pass
            elif source == 'insolvent':
                cls.calc_isHealthy_from_isInsolvent(bank, interbank)
                cls.calc_isInsolvent_from_isHealthy(bank, interbank)
            elif source == 'illiquid':
                cls.calc_isHealthy_from_isIlliquid(bank, interbank)
                cls.update_isIlliquid_from_isHealthy(bank, interbank)
            elif source == 'bankrupt':
                # @testprintln "无须更新！"
                pass
            elif source == 'off':
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'insolvent':
            if source == 'any':
                cls.calc_isInsolvent(bank, interbank)
                cls.update_isHealthy_from_isInsolvent(bank, interbank)
            elif source == 'healthy':
                cls.calc_isInsolvent_from_isHealthy(bank, interbank)
                cls.update_isHealthy_from_isInsolvent(bank, interbank)
            elif source == 'insolvent':
                # @testprintln "无须更新！"
                pass
            elif source == 'illiquid':
                # calc_isIlliquid_from_isHealthy(bank, interbank) #FIXME 错误，可以删除！
                pass
                # calc_isHealthy_from_isIlliquid(bank, interbank) #FIXME 错误，可以删除！
                # calc_isHealthy_from_isInsolvent(bank, interbank) #FIXME 错误，可以删除！
                # calc_isInsolvent_from_isHealthy(bank, interbank) #FIXME 错误，可以删除！
                # @testprintln "无须更新！"
            elif source == 'bankrupt':
                # @testprintln "无须更新！"
                pass
            elif source == 'off':
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'illiquid':
            if source == 'any':
                cls.calc_isIlliquid(bank, interbank)
                cls.update_isHealthy_from_isIlliquid(bank, interbank)
            elif source == 'healthy':
                cls.calc_isIlliquid_from_isHealthy(bank, interbank)
                cls.update_isHealthy_from_isIlliquid(bank, interbank)
            elif source == 'insolvent':
                # calc_isHealthy_from_isInsolvent(bank, interbank) #FIXME 错误，可以删除！
                # update_isInsolvent_from_isHealthy(bank, interbank) #FIXME 错误，可以删除！
                # update_isIlliquid_from_isHealthy(bank, interbank) #FIXME 错误，可以删除！
                # @testprintln "无须更新！"
                pass
            elif source == 'illiquid':
                # @testprintln "无须更新！"
                pass
            elif source == 'bankrupt':
                # @testprintln "无须更新！"
                pass
            elif source == 'off':
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'bankrupt':
            if source == 'any':
                cls.calc_isBankrupt(bank, interbank)
            elif source == 'healthy':
                cls.calc_isInsolvent_from_isHealthy(bank, interbank)
                cls.update_isHealthy_from_isInsolvent(bank, interbank)
                cls.calc_isIlliquid(bank, interbank)
                cls.update_isHealthy_from_isIlliquid(bank, interbank)
                cls.calc_isBankrupt_from_isInsolvent(bank, interbank)
                cls.calc_isBankrupt_from_isIlliquid(bank, interbank)
            elif source == 'insolvent':
                cls.calc_isBankrupt_from_isInsolvent(bank, interbank)
            elif source == 'illiquid':
                cls.calc_isBankrupt_from_isIlliquid(bank, interbank)
            elif source == 'bankrupt':
                # @testprintln "无须更新！"
                pass
            elif source == 'off':
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'off':
            if source == 'any':
                cls.calc_isOff(bank, interbank)
                cls.update_isOn_from_isOff(bank, interbank)
            elif source == 'healthy':
                # @testprintln "无须更新！"
                pass
            elif source == 'insolvent':
                # @testprintln "无须更新！"
                pass
            elif source == 'illiquid':
                # @testprintln "无须更新！"
                pass
            elif source == 'bankrupt':
                cls.calc_isOff_from_isBankrupt(bank, interbank)
                cls.update_isOn_from_isOff(bank, interbank)
                cls.update_isBankrupt_from_isOff(bank, interbank)
                interbank.cre = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="creditor")
                interbank.deb = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="debtor")
            elif source == 'off':
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'on':
            if source == 'any':
                cls.together_isOn(bank, interbank)
                cls.update_isOff_from_isOn(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'needed repay IB':
            if source == 'any':
                cls.calc_isNeededBoIB(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'enabled repay IB':
            if source == 'any':
                cls.calc_isEnabledBoIB(bank, interbank)
            elif source == 'needed repay IB':
                cls.calc_isEnabledBoIB_from_isNeededBoIB(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'needed repay Z_D':
            if source == 'any':
                cls.calc_isNeededBoD(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'enabled repay Z_D':
            if source == 'any':
                cls.calc_isEnabledBoD(bank, interbank)
            elif source == 'needed repay Z_D':
                cls.calc_isEnabledBoD_from_isNeededBoD(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'needed collect A_P':
            if source == 'any':
                cls.calc_isNeededLiP(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'enabled collect A_P':
            if source == 'any':
                cls.calc_isEnabledLiP(bank, interbank)
            elif source == 'needed collect A_P':
                cls.calc_isEnabledLiP_from_isNeededLiP(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        else:
            raise Exception("关键词target取词错误".format(target))
            pass
        pass  # method

    pass  # class
