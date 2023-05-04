"""功能函数集：计算构建银行与银行间相关状态及其转换。"""

from PySystemicRiskLab import np, copy
from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_consts import LESS1, FALSE1, FALSE2
from PySystemicRiskLab.core.define.define_environmentVariables import env
from PySystemicRiskLab.core.define.define_type import StateType

pass  # end import


class BankState:
    is_changed_state_matrix = copy(FALSE2)
    target_interstates_grid_matrix = None
    bank: BankCommercial
    interbank: BankInterbank

    ## 是否变动状态列表`is_states_changed_array`
    is_states_changed_array: bool

    ## 状态集合列表`states_list`
    states_list: list

    ## 源状态网格矩阵（笛卡尔积矩阵）`source_states_grid_matrix`
    source_states_grid_matrix: np.array

    ## 汇状态网格矩阵（笛卡尔积矩阵）`target_states_grid_matrix`
    target_states_grid_matrix: np.array

    ## 状态数据集合列表`state_data_list`
    state_data_list: list

    ## 计算状态函数集合列表`calc_state_functions_list`
    calc_state_functions_list: list

    ## 计算状态函数集合字典列表`calc_state_functions_dicts`
    calc_state_functions_dicts: list

    ## 状态关系集合列表`state_relations_list`
    state_relations_list: list

    ## 状态关系邻接矩阵`state_relations_adjacent_matrix`
    state_relations_adjacent_matrix: np.array

    ## 更新状态函数集合列表`update_state_functions_list`
    update_state_functions_list: list

    ## 更新状态函数字典列表`update_state_functions_dicts`
    update_state_functions_dicts: list

    ## 更新状态关系函数邻接矩阵
    update_state_functions_adjacent_matrix: np.array

    ## 状态关系索引表`states_relations_indices_table`
    states_relations_indices_table: list

    ## 状态对应更新关系字典列表`update_state_functions_adjacent_dict_list`
    update_state_functions_adjacent_dict_list: dict

    @classmethod
    def build_state_const_variables(cls):
        """
        构建各类状态常量变量。
        Returns:

        """

        ## 示性向量之各状态是否已经更新
        cls.is_states_changed_array = copy(FALSE1)

        ## 设置状态集合列表`states_list`
        cls.states_list = [
            'on',
            'hel',
            'isv',
            'ilq',
            'br',
            'off',
        ]

        ## 设置状态集合数据列表`state_data_list`
        cls.state_data_list = [
            cls.bank.on,
            cls.bank.hel,
            cls.bank.isv,
            cls.bank.ilq,
            cls.bank.br,
            cls.bank.off,
        ]

        ## 计算状态函数集合列表`calc_state_functions_list`
        cls.calc_state_functions_list = [
            cls.calc_isOn,
            cls.calc_isHealthy,
            cls.calc_isInsolvent,
            cls.calc_isIlliquid,
            cls.calc_isBankrupt,
            cls.calc_isOff
        ]

        ## 构建状态函数集合列表字典`calc_state_functions_dicts`
        cls.calc_state_functions_dicts = [{i[0]: i[1]} for i in zip(cls.states_list, cls.calc_state_functions_list)]

        ## 构建状态数据列表字典`state_data_dict`
        cls.state_data_dict = [{i[0]: i[1]} for i in zip(cls.states_list, cls.state_data_list)]

        ## 构建源与汇状态数据网格矩阵（笛卡尔积矩阵）`states_data_grid_matrix`
        cls.source_states_data_grid_matrix, cls.target_states_data_grid_matrix = np.meshgrid(cls.state_data_list, cls.state_data_list)

        ## 设置状态关系集合列表`state_relations_list`
        ## 同一种状态标记【同】；
        ## 手动更新标记【手】；
        ## 不存在直接关系标记【无】；
        ## 非确定的关系标记【惑】；
        ## 父子关系，分别标记【父】、【子】；
        ## 互相排斥关系，标记【斥】；
        ## 其它可以推导关系，标记【推】；
        cls.state_relations_list = [
            '同',
            '手',
            '无',
            '惑',
            '父',
            '子',
            '斥',
        ]

        ## 设置状态关系邻接矩阵`state_relations_adjacent_matrix`
        cls.state_relations_adjacent_matrix = [
            ['同', '父', '父', '父', '父', '无', ],
            ['子', '同', '惑', '惑', '无', '无', ],
            ['子', '斥', '同', '无', '手', '无', ],
            ['子', '斥', '无', '同', '手', '无', ],
            ['子', '无', '惑', '惑', '同', '手', ],
            ['无', '无', '无', '无', '斥', '同', ],
        ]

        ## 构建源与汇状态网格矩阵（笛卡尔积矩阵）`state_grid_matrix`
        cls.source_states_grid_matrix, cls.target_states_grid_matrix = np.meshgrid(cls.states_list, cls.states_list)

        ## 构建状态关系索引表`states_relations_indices_table`
        cls.states_relations_indices_table = np.column_stack([cls.source_states_grid_matrix.ravel(), cls.target_states_grid_matrix.ravel(), np.asarray(cls.state_relations_adjacent_matrix).ravel()])

        ## 设置更新状态函数集合列表`update_state_functions_list`
        cls.update_state_functions_list = [
            cls.update_if_equity,
            cls.update_if_handle,
            cls.update_if_none,
            cls.update_if_uncertain,
            cls.update_if_parent,
            cls.update_if_child,
            cls.update_if_exclusive,
        ]

        ## 构建更新状态函数字典列表`update_state_functions_dicts`
        cls.update_state_functions_dicts = [{i[0]: i[1]} for i in zip(cls.state_relations_list, cls.update_state_functions_list)]

        ## 根据`state_relations_adjacent_matrix`构建更新状态关系函数各源状态对应的汇状态邻接数组字典。该数据顶层是字典数组，每个键是状态名，每个值是一个数组，其是该状态对应的状态关系邻接矩阵之一行之状态关系名对应的更新函数。
        for i, row in enumerate(cls.state_relations_adjacent_matrix):
            cls.update_state_functions_adjacent_dict_list[cls.states_list[i]] = np.array([cls.update_state_functions_dicts[j] for j in row])

        ## 根据`state_relations_adjacent_matrix`构建更新状态关系函数邻接矩阵。矩阵每个元素是一个更新状态函数，对应状态关系邻接矩阵之元素之状态关系名。
        for i, row in enumerate(cls.state_relations_adjacent_matrix):
            for j, col in enumerate(row):
                cls.update_state_functions_adjacent_matrix[i, j] = cls.update_state_functions_dicts[col]

        ## 构建源、汇交互状态网格矩阵（笛卡尔积矩阵）`source_inter_states_grid_matrix`、`target_inter_states_grid_matrix`#NOW
        cls.source_inter_states_grid_matrix, cls.target_inter_states_grid_matrix = np.meshgrid(cls.inter_states_list, cls.inter_states_list)
        pass  # def

    @classmethod
    def get_relation_of_states(cls, source_state: StateType, target_state: StateType, mode: str = 'all'):
        """
        获取两个状态之间的关系。

        同一种状态标记【同】；

        手动更新标记【手】；

        不存在直接关系标记【无】；

        非确定的关系标记【惑】；

        父子关系，分别标记【父】、【子】；

        互相排斥关系，标记【斥】；

        其它可以推导关系，标记【推】；

        Args:
            source_state (StateType): 源状态
            target_state (StateType): 目标状态
            mode (str, optional): 获取模式。可选值为`all`、`target`、`one`。默认为`all`，获取整个状态关系邻接矩阵；`target`，获取源状态与所有汇状态之间的关系；`one`，获取两个状态之间的关系。 默认是 'all'。

        Returns:
            如果`mode`为`all`，则返回整个状态关系邻接矩阵；如果`mode`为`target`，则返回源状态与所有汇状态之间的关系；如果`mode`为`one`，则返回两个状态之间的关系。
        """
        if mode == 'all':  # 直接获取整个状态关系邻接矩阵
            return cls.state_relations_adjacent_matrix
        elif mode == 'target':  # 获取源状态与所有汇状态之间的关系
            return cls.states_relations_indices_table[(cls.states_relations_indices_table[:, 0] == source_state), 2]
        elif mode == 'one':  # 获取两个状态之间的关系
            return cls.states_relations_indices_table[(cls.states_relations_indices_table[:, 0] == source_state) & (cls.states_relations_indices_table[:, 1] == target_state), 2]
        else:
            raise ValueError("参数`mode`的值不正确。")
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
    def calc_state(cls, state: StateType):
        """
        计算状态。#TODO

        Args:
            state (StateType): 待计算的状态

        Returns:
            计算前后的状态之变动的位置示性向量
        """
        ## 根据状态计算相应的状态
        return cls.calc_state_functions_dicts[state](cls.bank, cls.interbank)
        pass

    @classmethod
    def calc_isOn(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行存在的。"""  # TODO
        condition = (bank.hel | bank.isv | bank.ilq | bank.br)
        changes = (bank.on != condition)
        if changes.any():
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            # interbank.listOfCreditorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "creditor") #HACK，未定义，无用。
            # interbank.listOfDebtorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "debtor") #HACK，未定义，无用。
            return changes
            pass
        pass

    @classmethod
    def calc_isHealthy(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行健康的。"""
        condition = ((bank.E_all >= LESS1) & (bank.A_Q >= LESS1) & (bank.Shock_def_t + LESS1 <= bank.E_all) & (bank.Shock_run_t + LESS1 <= bank.A_Q) & (bank.on))
        changes = (bank.hel != condition)
        if changes.any():
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            return changes
            pass
        pass

    @classmethod
    def calc_isInsolvent(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行资不抵债的。"""
        condition = (((bank.A_all < bank.Z_all + LESS1) | (bank.E_all < LESS1) | (bank.Shock_def_t + LESS1 > bank.E_all)) & bank.on)
        changes = (bank.isv != condition)
        if changes.any():
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="creditor")
            interbank.deb_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="debtor")
            return changes
            pass
        pass

    @classmethod
    def calc_isIlliquid(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行流动性短缺的。"""
        condition = (((bank.A_Q < LESS1) | (bank.Shock_run_t + LESS1 > bank.A_Q)) & bank.on)
        changes = (bank.ilq != condition)
        if changes.any():
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="creditor")
            interbank.deb_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="debtor")
            return changes
            pass
        pass

    @classmethod
    def calc_isBankrupt(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行破产的。"""
        condition = (bank.isv | bank.ilq)  # TODO 这个仅仅是目前基准算法简化的做法
        changes = (bank.br != condition)
        if changes.any():
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="creditor")
            interbank.deb_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="debtor")
            return changes
            pass
        pass

    @classmethod
    def calc_isOff(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行退出的。"""
        condition = bank.br | bank.off
        changes = (bank.off != condition)
        if (bank.off != condition).any():
            bank.off = condition
            interbank.off = (bank.off & bank.off.T)
            return changes
            pass
        pass

    @classmethod
    def calc_isNeededBoIB(cls, bank: BankCommercial, interbank: BankInterbank):  # TODO
        """计算示性向量之于银行需要偿还银行间负债的。"""
        bank.is_needed_BoIB = ((bank.Shock_IB_run_ilq_t > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledBoIB(cls, bank: BankCommercial, interbank: BankInterbank):  # TODO
        """计算示性向量之于银行能够偿还银行间负债的。"""
        bank.is_enabled_BoIB = ((bank.Shock_IB_run_ilq_t > 0) & (bank.A_Q > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledBoIB_from_isNeededBoIB(cls, bank: BankCommercial, interbank: BankInterbank):  # TODO
        """计算示性向量之于银行能够偿还银行间负债的，从需要偿还银行间负债的。"""
        bank.is_enabled_BoIB = (bank.is_needed_BoIB & (bank.A_Q > 0))
        pass

    @classmethod
    def calc_isNeededBoD(cls, bank: BankCommercial, interbank: BankInterbank):  # TODO
        """计算示性向量之于银行需要偿还居民部门存款的。"""
        bank.is_needed_BoD = ((bank.Shock_D_run_t > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledBoD(cls, bank: BankCommercial, interbank: BankInterbank):  # TODO
        """计算示性向量之于银行能够偿还居民部门存款的。"""
        bank.is_enabled_BoD = ((bank.Shock_D_run_t > 0) & (bank.A_Q > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledBoD_from_isNeededBoD(cls, bank: BankCommercial, interbank: BankInterbank):  # TODO
        """计算示性向量之于银行能够偿还居民部门存款的，从需要偿还居民部门存款的。"""
        bank.is_enabled_BoD = (bank.is_needed_BoD & (bank.A_Q > 0))
        pass

    @classmethod
    def calc_isNeededLiP(cls, bank: BankCommercial, interbank: BankInterbank):  # TODO
        """计算示性向量之于银行需要收回厂商贷款的。"""
        bank.is_needed_LiP = ((bank.Shock_P_run_s > 0) & bank.on)
        pass

    @classmethod
    def calc_isEnabledLiP(cls, bank: BankCommercial, interbank: BankInterbank):  # TODO
        """计算示性向量之于银行能够收回厂商贷款的。"""
        bank.is_enabled_LiP = ((bank.Shock_P_run_s > 0) & bank.on)  # HACK后续可能会补充条件 & producer.A_Q > 0
        pass

    @classmethod
    def calc_isEnabledLiP_from_isNeededLiP(cls, bank: BankCommercial, interbank: BankInterbank):  # TODO
        """计算示性向量之于银行能够收回厂商贷款的，从需要收回厂商贷款的。"""
        bank.is_enabled_LiP = (bank.is_needed_LiP)  # HACK后续可能会补充条件 & producer.A_Q > 0
        pass

    # @classmethod #TODO无用可以删除
    # def is_updated_relation_of_states(cls, source_state: StateType, target_state: StateType):
    #     """判断是否有更新状态之关系"""
    #     pass  # def
    #
    # @classmethod
    # def update_state_to_target_from_source(cls, target_state: StateType, target_inter_state: StateType & StateType.T, source_state_changes: StateType):  # NOW
    #     # target_state = ((~target_state & source_state_changes) | (target_state & ~source_state_changes)) & cls.bank.on  # NOTE和下面一行的语句实现结果是等价的，但是运算速度可能慢一点
    #     target_state[source_state_changes] = ~target_state[source_state_changes]
    #     target_inter_state[source_state_changes & source_state_changes.T] = ~target_inter_state[source_state_changes & source_state_changes.T]
    #     pass  # def

    @classmethod
    def update_states(cls):
        """
        批量更新多个状态。

        Args:
            state (StateType): 待更新的状态

        Returns:

        """
        # 根据状态之间的关系更新相应的状态
        # cls.target_states_grid_matrix,cls.target_interstates_grid_matrix,cls.is_changed_state_matrix=cls.update_state_functions_adjacent_matrix[cls.source_states_grid_matrix, cls.target_states_grid_matrix](cls.bank, cls.interbank)

        results_1 = np.zeros((3, 3, 3, 3))
        results_2 = np.full((3, 3), '')

        for i in range(len(cls.states_list)):
            for j in range(len(cls.states_list)):
                cls.target_states_grid_matrix[i][j], cls.target_interstates_grid_matrix[i][j], cls.is_changed_state_matrix[i][j] = cls.update_state_functions_adjacent_matrix[i][j](cls.source_states_grid_matrix[i][j], cls.target_states_grid_matrix[i][j])

        is_states_changed_array = cls.is_changed_state_matrix.any(axis=0)
        # cls.update_state_functions_dicts[state](cls.bank, cls.interbank)
        # cls.update_state_functions_adjacent_matrix()
        pass

    @classmethod
    def update_state(cls, source_state: StateType, target_state: StateType):
        """
        更新单个状态。

        Args:
            state (StateType): 待更新的状态

        Returns:
            计算前后的状态之变动的位置示性向量
        """
        ## 根据状态之间的关系更新相应的状态
        # cls.update_state_functions_dicts[state](cls.bank, cls.interbank)
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
    def update_if_child(cls, source_state: StateType, target_state: StateType, changes: StateType):
        """
        当关系是【子】的时候，更新

        Args:
            source_state (StateType): 源状态
            target_state (StateType): 目标状态
            changes (StateType): 源状态的变动示性向量

        Returns:
            target_state (StateType): 计算后的目标状态
            target_interbank_state (StateType): 计算后的目标状态之银行间关系
            is_changed_state (bool): 是否有更新状态

        """
        # target_state= (~target_state & changes) | (target_state & ~changes)  # NOTE和下面一行的语句实现结果是等价的，但是运算速度可能慢一点
        is_changed_state = (target_state[changes] != source_state[changes]).any()
        if is_changed_state:
            target_state[changes] = source_state[changes]
            target_interbank_state = (target_state & target_state.T)
        return target_state, target_interbank_state, is_changed_state
        pass  # def

    @classmethod
    def update_if_exclusive(cls, source_state: StateType, target_state: StateType, changes: StateType):
        """
        当关系是【斥】的时候，更新

        Args:
            source_state (StateType): 源状态
            target_state (StateType): 目标状态
            changes (StateType): 源状态的变动示性向量

        Returns:
            target_state (StateType): 计算后的目标状态
            target_interbank_state (StateType): 计算后的目标状态之银行间关系
            is_changed_state (bool): 是否有更新状态

        """
        # target_state= (~target_state & changes) | (target_state & ~changes)  # NOTE和下面一行的语句实现结果是等价的，但是运算速度可能慢一点
        is_changed_state = (target_state[changes] != ~source_state[changes]).any()
        if is_changed_state:
            target_state[changes] = ~source_state[changes]
            target_interbank_state = (target_state & target_state.T)
        return target_state, target_interbank_state, is_changed_state
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
    def together_isOn(cls, bank: BankCommercial, interbank: BankInterbank):  # HACK虽然无用，但是可以先保留
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
    def update_B_state(cls, way: str = 'any'):  # TODO重命名成update_banks_states
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
        cls.is_states_changed_array = copy(FALSE1)
        state_changes = cls.calc_state(way)
        cls.is_states_changed_array[np.where(way == cls.states_list)] = state_changes.any()  # 记录是否有状态更新

        # ## 决策是否根据初始计算的源状态更新汇状态：根据状态关系表、是否自动更新情况、状态更新情况决策；
        # states_relations = cls.get_relation_of_states(way, mode='all')

        ## 根据需要更新的状态，更新相应的汇状态；
        # =cls.update_state_functions_adjacent_matrix[cls.source_states_grid_matrix,cls.target_states_grid_matrix](cls.bank, cls.interbank)
        cls.update_states()

        ## 重复更新状态，直至无状态需要更新；
        while cls.is_states_changed_array.any() == True:
            # ## 决策是否根据更新后的源状态更新汇状态：根据状态关系表、是否自动更新情况、状态更新情况决策；
            # states_relations = cls.get_relation_of_states(way, mode='all')
            #
            # ## 根据需要更新的状态，更新相应的汇状态；
            # for i, r in enumerate(states_relations):
            #     states_changes = cls.update_state(states_relations)
            #     cls.is_states_changed_array[np.where(way == cls.states_list)] = states_changes[i].any()  # 记录是否有状态更新

            ## 根据需要更新的状态，更新相应的汇状态
            cls.update_states()

            pass  # while

        ## 更新银行间市场interbank之各状态下之信息列表之于各银行之债权方与债务方之银行编号。
        cls.update_all_cre_and_deb()
        pass  # def

        # if target == 'any':  # FIXME 这个可能有缺陷:
        #     if source == 'any':
        #         cls.init_list_of_relation_in_state_of_banks(bank, interbank)
        #         _ = cls.calc_isInsolvent(bank, interbank)
        #         _ = cls.calc_isIlliquid(bank, interbank)
        #         _ = cls.calc_isHealthy(bank, interbank)
        #         _ = cls.calc_isBankrupt(bank, interbank)
        #         cls.together_isOn(bank, interbank)
        #         # calc_isOff(bank, interbank) # TODO后续添加
        #         # calc_isOn(bank, interbank) # TODO后续添加
        #     elif source == 'healthy':
        #         hel_changes = cls.calc_isHealthy(bank, interbank)
        #         _ = cls.calc_isInsolvent(bank, interbank)
        #         _ = cls.calc_isIlliquid(bank, interbank)
        #         cls.update_state_to_target_from_source(bank.hel, interbank.hel, isv_changes)
        #         ilq_changes = cls.calc_isIlliquid(bank, interbank)
        #         cls.update_state_to_target_from_source(bank.hel, interbank.hel, ilq_changes)
        #     elif source == 'insolvent':
        #         isv_changes = cls.calc_isInsolvent(bank, interbank)
        #         cls.update_state_to_target_from_source(bank.hel, interbank.hel, isv_changes)
        #         # br_changes = cls.calc_isBankrupt(bank, interbank)
        #     elif source == 'illiquid':
        #         ilq_changes = cls.calc_isIlliquid(bank, interbank)
        #         cls.update_state_to_target_from_source(bank.hel, interbank.hel, ilq_changes)
        #         # br_changes = cls.calc_isBankrupt(bank, interbank)
        #     elif source == 'bankrupt':
        #         cls.calc_isBankrupt(bank, interbank)
        #         # HACK是否需要加入破产到退出呢？
        #     elif source == 'off':
        #         off_changes = cls.calc_isOff(bank, interbank)
        #         cls.update_state_to_target_from_source(bank.br, interbank.br, off_changes)
        #         cls.together_isOn(bank, interbank)
        #         pass
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'healthy':
        #     if source == 'any':
        #         hel_changes = cls.calc_isHealthy(bank, interbank)
        #         cls.update_isInsolvent_from_isHealthy(bank, interbank)
        #         cls.update_isIlliquid_from_isHealthy(bank, interbank)
        #     elif source == 'healthy':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'insolvent':
        #         cls.calc_isHealthy_from_isInsolvent(bank, interbank)
        #         cls.calc_isInsolvent_from_isHealthy(bank, interbank)
        #     elif source == 'illiquid':
        #         cls.calc_isHealthy_from_isIlliquid(bank, interbank)
        #         cls.update_isIlliquid_from_isHealthy(bank, interbank)
        #     elif source == 'bankrupt':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'off':
        #         # @testprintln "无须更新！"
        #         pass
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'insolvent':
        #     if source == 'any':
        #         cls.calc_isInsolvent(bank, interbank)
        #         cls.update_isHealthy_from_isInsolvent(bank, interbank)
        #     elif source == 'healthy':
        #         cls.calc_isInsolvent_from_isHealthy(bank, interbank)
        #         cls.update_isHealthy_from_isInsolvent(bank, interbank)
        #     elif source == 'insolvent':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'illiquid':
        #         # calc_isIlliquid_from_isHealthy(bank, interbank) #FIXME 错误，可以删除！
        #         pass
        #         # calc_isHealthy_from_isIlliquid(bank, interbank) #FIXME 错误，可以删除！
        #         # calc_isHealthy_from_isInsolvent(bank, interbank) #FIXME 错误，可以删除！
        #         # calc_isInsolvent_from_isHealthy(bank, interbank) #FIXME 错误，可以删除！
        #         # @testprintln "无须更新！"
        #     elif source == 'bankrupt':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'off':
        #         # @testprintln "无须更新！"
        #         pass
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'illiquid':
        #     if source == 'any':
        #         cls.calc_isIlliquid(bank, interbank)
        #         cls.update_isHealthy_from_isIlliquid(bank, interbank)
        #     elif source == 'healthy':
        #         cls.calc_isIlliquid_from_isHealthy(bank, interbank)
        #         cls.update_isHealthy_from_isIlliquid(bank, interbank)
        #     elif source == 'insolvent':
        #         # calc_isHealthy_from_isInsolvent(bank, interbank) #FIXME 错误，可以删除！
        #         # update_isInsolvent_from_isHealthy(bank, interbank) #FIXME 错误，可以删除！
        #         # update_isIlliquid_from_isHealthy(bank, interbank) #FIXME 错误，可以删除！
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'illiquid':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'bankrupt':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'off':
        #         # @testprintln "无须更新！"
        #         pass
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'bankrupt':
        #     if source == 'any':
        #         cls.calc_isBankrupt(bank, interbank)
        #     elif source == 'healthy':
        #         cls.calc_isInsolvent_from_isHealthy(bank, interbank)
        #         cls.update_isHealthy_from_isInsolvent(bank, interbank)
        #         cls.calc_isIlliquid(bank, interbank)
        #         cls.update_isHealthy_from_isIlliquid(bank, interbank)
        #         cls.calc_isBankrupt_from_isInsolvent(bank, interbank)
        #         cls.calc_isBankrupt_from_isIlliquid(bank, interbank)
        #     elif source == 'insolvent':
        #         cls.calc_isBankrupt_from_isInsolvent(bank, interbank)
        #     elif source == 'illiquid':
        #         cls.calc_isBankrupt_from_isIlliquid(bank, interbank)
        #     elif source == 'bankrupt':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'off':
        #         # @testprintln "无须更新！"
        #         pass
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'off':
        #     if source == 'any':
        #         cls.calc_isOff(bank, interbank)
        #         cls.update_isOn_from_isOff(bank, interbank)
        #     elif source == 'healthy':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'insolvent':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'illiquid':
        #         # @testprintln "无须更新！"
        #         pass
        #     elif source == 'bankrupt':
        #         cls.calc_isOff_from_isBankrupt(bank, interbank)
        #         cls.update_isOn_from_isOff(bank, interbank)
        #         cls.update_isBankrupt_from_isOff(bank, interbank)
        #         interbank.cre = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="creditor")
        #         interbank.deb = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="debtor")
        #     elif source == 'off':
        #         # @testprintln "无须更新！"
        #         pass
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'on':
        #     if source == 'any':
        #         cls.together_isOn(bank, interbank)
        #         cls.update_isOff_from_isOn(bank, interbank)
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'needed repay IB':
        #     if source == 'any':
        #         cls.calc_isNeededBoIB(bank, interbank)
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'enabled repay IB':
        #     if source == 'any':
        #         cls.calc_isEnabledBoIB(bank, interbank)
        #     elif source == 'needed repay IB':
        #         cls.calc_isEnabledBoIB_from_isNeededBoIB(bank, interbank)
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'needed repay Z_D':
        #     if source == 'any':
        #         cls.calc_isNeededBoD(bank, interbank)
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'enabled repay Z_D':
        #     if source == 'any':
        #         cls.calc_isEnabledBoD(bank, interbank)
        #     elif source == 'needed repay Z_D':
        #         cls.calc_isEnabledBoD_from_isNeededBoD(bank, interbank)
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'needed collect A_P':
        #     if source == 'any':
        #         cls.calc_isNeededLiP(bank, interbank)
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # elif target == 'enabled collect A_P':
        #     if source == 'any':
        #         cls.calc_isEnabledLiP(bank, interbank)
        #     elif source == 'needed collect A_P':
        #         cls.calc_isEnabledLiP_from_isNeededLiP(bank, interbank)
        #     else:
        #         raise Exception("关键词source取词错误".format(source))
        #         pass
        # else:
        #     raise Exception("关键词target取词错误".format(target))
        #     pass
        # pass  # method

    pass  # class
