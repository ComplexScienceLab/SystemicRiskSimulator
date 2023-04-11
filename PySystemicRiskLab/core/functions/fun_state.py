# "功能函数集：计算构建银行与银行间相关状态及其转换。"

## 功能函数集：计算构建银行与银行间相关状态及其转换。

from PySystemicRiskLab.core.define.define_agents import BankCommercial, BankInterbank
from PySystemicRiskLab.core.define.define_consts import LESS1
from PySystemicRiskLab.core.define.define_environmentVariables import env
from PySystemicRiskLab.core.define.define_type import *

pass  # end import


class BankState:

    @classmethod
    def init_list_of_relation_in_state_of_banks(cls, bank: BankCommercial, interbank: BankInterbank):
        """
        初始化银行状态关系列表
        """
        interbank.cre = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="creditor")
        interbank.deb = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="debtor")
        pass

    @classmethod
    def calc_isHealthy(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行健康的。"""
        condition = ((bank.E_all >= LESS1) & (bank.A_Q >= LESS1) & (bank.Shock_def_t + LESS1 <= bank.E_all) & (bank.Shock_run_t + LESS1 <= bank.A_Q) & bank.on)
        if (bank.hel != condition).any():
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass

    @classmethod
    def calc_isHealthy_from_isInsolvent(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行健康的，来自资不抵债的。"""
        condition = ((bank.E_all >= LESS1) & (bank.A_Q >= LESS1) & (bank.Shock_def_t + LESS1 <= bank.E_all) & bank.on)
        if (bank.hel != condition).any():
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass

    @classmethod
    def update_isHealthy_from_isInsolvent(cls, bank: BankCommercial, interbank: BankInterbank):
        """新示性向量之于银行健康的，来自资不抵债的。"""
        condition = (~(bank.isv | bank.ilq) & bank.on)
        if (bank.hel != condition).any():
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass

    @classmethod
    def calc_isHealthy_from_isIlliquid(cls, bank: BankCommercial, interbank: BankInterbank):
        """
        计算示性向量之于银行健康的，来自流动性短缺的。
        内容同于calc_isHealthy。
        """
        condition = ((bank.E_all >= LESS1) & (bank.A_Q >= LESS1) & (bank.Shock_run_t + LESS1 <= bank.A_Q) & bank.on)
        if (bank.hel != condition).any():
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass

    @classmethod
    def update_isHealthy_from_isIlliquid(cls, bank: BankCommercial, interbank: BankInterbank):
        """
        更新示性向量之于银行健康的，来自流动性短缺的。
        内容同于update_isHealthy_from_isInsolvent
        """
        condition = (~(bank.isv | bank.ilq) & bank.on)
        if (bank.hel != condition).any():
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass

    @classmethod
    def calc_isInsolvent(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行资不抵债的。"""
        condition = (((bank.A_all < bank.Z_all + LESS1) | (bank.E_all < LESS1) | (bank.Shock_def_t + LESS1 > bank.E_all)) & bank.on)
        if (bank.isv != condition).any():
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="creditor")
            interbank.deb_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="debtor")
            pass
        pass

    @classmethod
    def calc_isInsolvent_from_isHealthy(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行资不抵债的，来自健康的。"""
        condition = (((bank.A_all < bank.Z_all + LESS1) | (bank.E_all < LESS1) | (bank.Shock_def_t + LESS1 > bank.E_all)) & bank.on)
        if (bank.isv != condition).any():
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="creditor")
            interbank.deb_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="debtor")
            pass
        pass

    @classmethod
    def update_isInsolvent_from_isHealthy(cls, bank: BankCommercial, interbank: BankInterbank):
        """
        更新示性向量之于银行资不抵债的，来自健康的。
        内容同于calc_isInsolvent_from_isHealthy
        """
        condition = (((bank.A_all < bank.Z_all + LESS1) | (bank.E_all < LESS1) | (bank.Shock_def_t + LESS1 > bank.E_all)) & bank.on)
        if (bank.isv != condition).any():
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="creditor")
            interbank.deb_isv = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.isv, goal="debtor")
            pass
        pass

    @classmethod
    def calc_isIlliquid(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行流动性短缺的。"""
        condition = ((bank.Shock_run_t + LESS1 >= bank.A_Q) & bank.on)
        if (bank.ilq != condition).any():
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="creditor")
            interbank.deb_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="debtor")
            pass
        pass

    @classmethod
    def calc_isIlliquid_from_isHealthy(cls, bank: BankCommercial, interbank: BankInterbank):
        """
        计算示性向量之于银行流动性短缺的，来自健康的。
        内容同于calc_isIlliquid
        """
        condition = ((bank.Shock_run_t + LESS1 >= bank.A_Q) & bank.on)
        if (bank.ilq != condition).any():
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="creditor")
            interbank.deb_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="debtor")
            pass
        pass

    @classmethod
    def update_isIlliquid_from_isHealthy(cls, bank: BankCommercial, interbank: BankInterbank):
        """
        更新示性向量之于银行流动性短缺的，来自健康的。
        内容同于calc_isIlliquid
        """
        condition = ((bank.Shock_run_t + LESS1 >= bank.A_Q) & bank.on)
        if (bank.ilq != condition).any():
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="creditor")
            interbank.deb_ilq = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.ilq, goal="debtor")
            pass
        pass

    @classmethod
    def calc_isBankrupt(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行破产的。"""
        condition = (bank.isv | bank.ilq)
        if (bank.br != condition).any():
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="creditor")
            interbank.deb_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="debtor")
            pass
        pass

    @classmethod
    def calc_isBankrupt_from_isInsolvent(cls, bank: BankCommercial, interbank: BankInterbank):
        """
        计算示性向量之于破产的，来自资不抵债的。
        同于calc_isBankrupt
        """
        condition = (bank.isv | bank.ilq)
        if (bank.br != condition).any():
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="creditor")
            interbank.deb_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="debtor")
            pass
        pass

    @classmethod
    def calc_isBankrupt_from_isIlliquid(cls, bank: BankCommercial, interbank: BankInterbank):
        """
        计算示性向量之于破产的，来自流动性短缺的。
        同于calc_isBankrupt
        """
        condition = (bank.isv | bank.ilq)
        if (bank.br != condition).any():
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="creditor")
            interbank.deb_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="debtor")
            pass
        pass

    @classmethod
    def together_isOn(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行存在的。"""
        condition = (bank.hel | bank.isv | bank.ilq | bank.br)
        if (bank.on != condition).any():
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            # interbank.listOfCreditorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "creditor") #HACK，未定义，无用。
            # interbank.listOfDebtorsInOn = cls.calc_list_of_relation_in_state_of_banks(interbank, isState = bank.on, goal = "debtor") #HACK，未定义，无用。
            pass
        pass

    @classmethod
    def update_isBankrupt_from_isOff(cls, bank: BankCommercial, interbank: BankInterbank):  # FIXME，有一定不稳定的风险。
        """更新示性向量之于银行破产的，来自退出的。"""
        condition = (bank.off)
        if bank.br == condition:
            bank.br = np.full((env['num_bank'], 1), False)
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="creditor")
            interbank.deb_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="debtor")
            pass
        pass

    @classmethod
    def update_isOn_from_isOff(cls, bank: BankCommercial, interbank: BankInterbank):
        """新示性向量之于银行存在的，来自退出的。"""
        condition = (~bank.off)
        if (bank.on != condition).any():
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            interbank.cre_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="creditor")
            interbank.deb_br = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.br, goal="debtor")
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
    def update_isOff_from_isOn(cls, bank: BankCommercial, interbank: BankInterbank):
        """新示性向量之于银行退出的，来自存在的。"""
        condition = ~bank.on
        if (bank.off != condition).any():
            bank.off = condition
            interbank.off = (bank.off & bank.off.T)
            pass
        pass

    @classmethod
    def calc_isOff_from_isBankrupt(cls, bank: BankCommercial, interbank: BankInterbank):
        """计算示性向量之于银行退出的，来自破产的。"""
        cls.calc_isOff(bank, interbank)
        interbank.cre_br = np.array([])
        interbank.deb_br = np.array([])
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
    def update_B_state(cls, bank: BankCommercial, interbank: BankInterbank, target: str = 'any', source: str = 'any'):
        """
        更新各银行之状态。

        参数``target``可选项：

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

        参数``source``可选项：

        - ``any``:  从任意状态出发；
        - ``healthy``:  从健康状态出发；
        - ``insolvent``:  从资不抵债状态出发；
        - ``illiquid``:  从流动性短缺状态出发；
        - ``bankrupt``:  从破产状态出发；
        - ``off``:  从退出状态出发；
        - ``needed repay IB``:  到是否需要偿还银行间借款状态；
        - ``needed repay Z_D``:  到是否需要偿还居民存款状态；
        - ``needed collect A_P``:  到是否可以收回厂商贷款状态；

        Args:
            bank ():
            interbank ():
            target (): 参数，转移状态目标；
            source (): 参数，转移状态源头；

        Returns:

        """
        if target == 'any':  # FIXME 这个可能有缺陷:
            if source == 'any':
                cls.init_list_of_relation_in_state_of_banks(bank, interbank)
                cls.calc_isInsolvent(bank, interbank)
                cls.calc_isIlliquid(bank, interbank)
                cls.calc_isHealthy(bank, interbank)
                cls.calc_isBankrupt(bank, interbank)
                cls.together_isOn(bank, interbank)
                # calc_isOff(bank, interbank)
                # calc_isOn(bank, interbank)
            elif source == 'healthy':
                cls.calc_isInsolvent_from_isHealthy(bank, interbank)
                cls.update_isHealthy_from_isInsolvent(bank, interbank)
                cls.calc_isIlliquid_from_isHealthy(bank, interbank)
                cls.update_isHealthy_from_isIlliquid(bank, interbank)
            elif source == 'insolvent':
                cls.calc_isHealthy_from_isInsolvent(bank, interbank)
                cls.update_isInsolvent_from_isHealthy(bank, interbank)
                cls.calc_isBankrupt_from_isInsolvent(bank, interbank)
            elif source == 'illiquid':
                cls.calc_isHealthy_from_isIlliquid(bank, interbank)
                cls.update_isIlliquid_from_isHealthy(bank, interbank)
                cls.calc_isBankrupt_from_isIlliquid(bank, interbank)
            elif source == 'bankrupt':
                cls.calc_isOff_from_isBankrupt(bank, interbank)
                cls.update_isOn_from_isOff(bank, interbank)
                interbank.cre = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="creditor")
                interbank.deb = cls.calc_list_of_relation_in_state_of_banks(interbank, isState=bank.on, goal="debtor")
            elif source == 'off':
                pass
                # @testprintln "无须更新！"
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == 'healthy':
            if source == 'any':
                cls.calc_isHealthy(bank, interbank)
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
