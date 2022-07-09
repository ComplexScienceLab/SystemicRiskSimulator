# "功能函数集：计算构建银行与银行间相关状态及其转换。"

## 功能函数集：计算构建银行与银行间相关状态及其转换。

##########################################
#状态/使用
##########################################

# from SystemicRisk.core import np,env,BankCommercial,BankInterbank,TypeState,LESS1,LESS2
pass  # end import

import numpy as np
from SystemicRisk.core.define.define_consts import LESS1,LESS2
from SystemicRisk.core.define.define_type import *
from SystemicRisk.core.define.define_environment_variables import env
from SystemicRisk.core.define.define_agents import  BankCommercial,BankInterbank
pass  # end import





class BankState:

    def init_listOfRelationInStateOfBanks(bank:BankCommercial, interbank:BankInterbank):
        """
        初始化银行状态关系列表
        """
        interbank.cre = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "creditor")
        interbank.deb = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "debtor")
        pass


    "计算示性向量之于银行健康的。"
    def calc_isHealthy(bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.E_all >= LESS1 & bank.A_Q >= LESS1 & bank.Shock_def_t + LESS1 <= bank.E_all & bank.Shock_run_t + LESS1 <= bank.A_Q & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass

    "计算示性向量之于银行健康的，来自资不抵债的。"
    def calc_isHealthy_from_isInsolvent(bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.E_all >= LESS1 & bank.A_Q >= LESS1 & bank.Shock_def_t + LESS1 <= bank.E_all & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass

    "更新示性向量之于银行健康的，来自资不抵债的。"
    def update_isHealthy_from_isInsolvent(bank:BankCommercial, interbank:BankInterbank):
        condition = (~(bank.isv | bank.ilq) & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass

    "计算示性向量之于银行健康的，来自流动性短缺的。" # 内容同于calc_isHealthy。
    def calc_isHealthy_from_isIlliquity(bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.E_all >= LESS1 & bank.A_Q >= LESS1 & bank.Shock_run_t + LESS1 <= bank.A_Q & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass

    "更新示性向量之于银行健康的，来自流动性短缺的。" # 内容同于update_isHealthy_from_isInsolvent
    def update_isHealthy_from_isIlliquity(bank:BankCommercial, interbank:BankInterbank):
        condition = (~(bank.isv | bank.ilq) & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass



    "计算示性向量之于银行资不抵债的。"
    def calc_isInsolvent(bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.A_all < bank.Z_all + LESS1 | bank.E_all < LESS1 | bank.Shock_def_t + LESS1 > bank.E_all) & bank.on)
        if bank.isv != condition:
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "creditor")
            interbank.deb_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "debtor")
            pass
        pass

    "计算示性向量之于银行资不抵债的，来自健康的。"
    def calc_isInsolvent_from_isHealthy(bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.A_all < bank.Z_all + LESS1 | bank.E_all < LESS1 | bank.Shock_def_t + LESS1 > bank.E_all) & bank.on)
        if bank.isv != condition:
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "creditor")
            interbank.deb_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "debtor")
            pass
        pass

    "更新示性向量之于银行资不抵债的，来自健康的。" # 内容同于calc_isInsolvent_from_isHealthy
    def update_isInsolvent_from_isHealthy(bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.A_all < bank.Z_all + LESS1 | bank.E_all < LESS1 | bank.Shock_def_t + LESS1 > bank.E_all) & bank.on)
        if bank.isv != condition:
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "creditor")
            interbank.deb_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "debtor")
            pass
        pass

    "计算示性向量之于银行流动性短缺的。"
    def calc_isIlliquity(bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.Shock_run_t + LESS1 >= bank.A_Q) & bank.on)
        if bank.ilq != condition:
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "creditor")
            interbank.deb_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "debtor")
            pass
        pass

    "计算示性向量之于银行流动性短缺的，来自健康的。" # 内容同于calc_isIlliquity
    def calc_isIlliquity_from_isHealthy(bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.Shock_run_t + LESS1 >= bank.A_Q) & bank.on)
        if bank.ilq != condition:
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "creditor")
            interbank.deb_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "debtor")
            pass
        pass

    "更新示性向量之于银行流动性短缺的，来自健康的。" # 内容同于calc_isIlliquity
    def update_isIlliquity_from_isHealthy(bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.Shock_run_t + LESS1 >= bank.A_Q) & bank.on)
        if bank.ilq != condition:
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "creditor")
            interbank.deb_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "debtor")
            pass
        pass

    "计算示性向量之于银行破产的。"
    def calc_isBankrupt(bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.isv | bank.ilq)
        if bank.br != condition:
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass

    "计算示性向量之于破产的，来自资不抵债的。" # 同于calc_isBankrupt
    def calc_isBankrupt_from_isInsolvent(bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.isv | bank.ilq)
        if bank.br != condition:
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass

    "计算示性向量之于破产的，来自流动性短缺的。" # 同于calc_isBankrupt
    def calc_isBankrupt_from_isIlliquity(bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.isv | bank.ilq)
        if bank.br != condition:
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass

    "计算示性向量之于银行存在的。"
    def together_isOn(bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.hel | bank.isv | bank.ilq | bank.br)
        if bank.on != condition:
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            # interbank.listOfCreditorsInOn = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "creditor") #HACK，未定义，无用。
            # interbank.listOfDebtorsInOn = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "debtor") #HACK，未定义，无用。
            pass
        pass

    "更新示性向量之于银行破产的，来自退出的。" #FIXME，有一定不稳定的风险。
    def update_isBankrupt_from_isOff(bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.off)
        if bank.br == condition:
            bank.br[: ] = np.false(env['num_bank'])
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass

    "更新示性向量之于银行存在的，来自退出的。"
    def update_isOn_from_isOff(bank:BankCommercial, interbank:BankInterbank):
        condition = (~bank.off)
        if bank.on != condition:
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass

    "计算示性向量之于银行退出的。"
    def calc_isOff(bank:BankCommercial, interbank:BankInterbank):
        condition = bank.br | bank.off
        if bank.off != condition:
            bank.off = condition
            interbank.off = (bank.off & bank.off.T)
            pass
        pass

    "更新示性向量之于银行退出的，来自存在的。"
    def update_isOff_from_isOn(bank:BankCommercial, interbank:BankInterbank):
        condition = ~bank.on
        if bank.off != condition:
            bank.off = condition
            interbank.off = (bank.off & bank.off.T)
            pass
        pass

    "计算示性向量之于银行退出的，来自破产的。"
    def calc_isOff_from_isBankrupt(bank:BankCommercial, interbank:BankInterbank):
        self.calc_isOff(bank, interbank)
        interbank.cre_br = []
        interbank.deb_br = []
        pass

    "计算示性向量之于银行需要偿还银行间负债的。"
    def calc_isNeededBoBI(bank:BankCommercial, interbank:BankInterbank):
        bank.nBoBI = (bank.Shock_BI_run_ilq_t > 0 & bank.on)
        pass

    "计算示性向量之于银行能够偿还银行间负债的。"
    def calc_isEnabledBoBI(bank:BankCommercial, interbank:BankInterbank):
        bank.eBoBI = (bank.Shock_BI_run_ilq_t > 0 & bank.A_Q > 0 & bank.on)
        pass

    "计算示性向量之于银行能够偿还银行间负债的，从需要偿还银行间负债的。"
    def calc_isEnabledBoBI_from_isNeededBoBI(bank:BankCommercial, interbank:BankInterbank):
        bank.eBoBI = (bank.nBoBI & bank.A_Q > 0)
        pass

    "计算示性向量之于银行需要偿还居民部门存款的。"
    def calc_isNeededBoD(bank:BankCommercial, interbank:BankInterbank):
        bank.nBoD = (bank.Shock_D_run_t > 0 & bank.on)
        pass

    "计算示性向量之于银行能够偿还居民部门存款的。"
    def calc_isEnabledBoD(bank:BankCommercial, interbank:BankInterbank):
        bank.eBoD = (bank.Shock_D_run_t > 0 & bank.A_Q > 0 & bank.on)
        pass

    "计算示性向量之于银行能够偿还居民部门存款的，从需要偿还居民部门存款的。"
    def calc_isEnabledBoD_from_isNeededBoD(bank:BankCommercial, interbank:BankInterbank):
        bank.eBoD = (bank.nBoD & bank.A_Q > 0)
        pass

    "计算示性向量之于银行需要收回厂商贷款的。"
    def calc_isNeededLiP(bank:BankCommercial, interbank:BankInterbank):
        bank.nLiP = (bank.Shock_P_run_s > 0 & bank.on)
        pass

    "计算示性向量之于银行能够收回厂商贷款的。"
    def calc_isEnabledLiP(bank:BankCommercial, interbank:BankInterbank):
        bank.eLiP = (bank.Shock_P_run_s > 0 & bank.on) #HACK后续可能会补充条件 & producer.A_Q > 0
        pass

    "计算示性向量之于银行能够收回厂商贷款的，从需要收回厂商贷款的。"
    def calc_isEnabledLiP_from_isNeededLiP(bank:BankCommercial, interbank:BankInterbank):
        bank.eLiP = (bank.nLiP) #HACK后续可能会补充条件 & producer.A_Q > 0
        pass




    """
    计算信息列表之于各状态银行之各关联银行。
    # Arguments
    - `interbank:BankInterbank`:  银行间主体。
    - `listOfRelationInStateOfBanks:Array`:  列表之于各银行之各状态之关系。
    - `isState:Vector`:  示性向量之于各银行之状态。
    - `goal:str`:  参数，确定计算债务方或债权方。
        - `debtor`:  计算对应的债务方银行；
        - `creditor`:  计算对应的债权方银行；
    # Returns
    - `listOfRelationInStateOfBanks`:  返回对应状态下的债权或者债务关系的银行列表；
    """
    def calc_listOfRelationInStateOfBanks(interbank:BankInterbank, isState:TypeState, goal:str):
        # 计算示性矩阵之于银行间风险敞口的
        if goal == "debtor":
            isExposure = ((interbank.A_BI > 0.0) & isState)
        elif goal == "creditor":
            isExposure = ((interbank.Z_BI > 0.0) & isState)
        else:
            pass
        listOfRelationInStateOfBanks = [[] for i in range(env['num_bank'])]
        for i in range(env['num_bank']):
            listOfRelationInStateOfBanks[i] = np.where(isExposure[i, : ]) # 获取对应状态下的债权或者债务关系的银行列表
            pass
        return listOfRelationInStateOfBanks
        pass


    """
    更新各银行之状态
    
    # Arguments
    
    `to:String`:  参数，转移状态目标；
    - `any`:  到任意状态；
    - `healthy`:  到健康状态；
    - `insolvent`:  到资不抵债状态；
    - `illiquity`:  到流动性短缺状态；
    - `bankrupt`:  到破产状态；
    - `off`:  到退出状态；
    - `needed repay BI`:  到是否需要偿还银行间借款状态；
    - `enabled repay BI`:  到是否可以偿还银行间借款状态；
    - `needed repay Z_D`:  到是否需要偿还居民存款状态；
    - `enabled repay Z_D`:  到是否需要偿还借款状态；
    - `needed collect A_P`:  到是否可以收回厂商贷款状态；
    - `enabled collect A_P`:  到是否可以收回厂商贷款状态；
    
    `from:String`:  参数，转移状态源头；
    - `any`:  从任意状态出发；
    - `healthy`:  从健康状态出发；
    - `insolvent`:  从资不抵债状态出发；
    - `illiquity`:  从流动性短缺状态出发；
    - `bankrupt`:  从破产状态出发；
    - `off`:  从退出状态出发；
    - `needed repay BI`:  到是否需要偿还银行间借款状态；
    - `needed repay Z_D`:  到是否需要偿还居民存款状态；
    - `needed collect A_P`:  到是否可以收回厂商贷款状态；
    """
    def update_B_state(bank:BankCommercial, interbank:BankInterbank, target:str = "any", source:str = "any"):
        if target == "any": #FIXME 这个可能有缺陷:
            if source == "any":
                self.init_listOfRelationInStateOfBanks(bank, interbank)
                self.calc_isInsolvent(bank, interbank)
                self.calc_isIlliquity(bank, interbank)
                self.calc_isHealthy(bank, interbank)
                self.calc_isBankrupt(bank, interbank)
                self.together_isOn(bank, interbank)
                # calc_isOff(bank, interbank)
                # calc_isOn(bank, interbank)
            elif source == "healthy":
                self.calc_isInsolvent_from_isHealthy(bank, interbank)
                self.update_isHealthy_from_isInsolvent(bank, interbank)
                self.calc_isIlliquity_from_isHealthy(bank, interbank)
                self.update_isHealthy_from_isIlliquity(bank, interbank)
            elif source == "insolvent":
                self.calc_isHealthy_from_isInsolvent(bank, interbank)
                self.update_isInsolvent_from_isHealthy(bank, interbank)
                self.calc_isBankrupt_from_isInsolvent(bank, interbank)
            elif source == "illiquity":
                self.calc_isHealthy_from_isIlliquity(bank, interbank)
                self.update_isIlliquity_from_isHealthy(bank, interbank)
                self.calc_isBankrupt_from_isIlliquity(bank, interbank)
            elif source == "bankrupt":
                self.calc_isOff_from_isBankrupt(bank, interbank)
                self.update_isOn_from_isOff(bank, interbank)
                interbank.cre = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "creditor")
                interbank.deb = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "debtor")
            elif source == "off":
                pass
                # @testprintln "无须更新！"
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "healthy":
            if source == "any":
                self.calc_isHealthy(bank, interbank)
                self.update_isInsolvent_from_isHealthy(bank, interbank)
                self.update_isIlliquity_from_isHealthy(bank, interbank)
            elif source == "healthy":
                # @testprintln "无须更新！"
                pass
            elif source == "insolvent":
                self.calc_isHealthy_from_isInsolvent(bank, interbank)
                self.calc_isInsolvent_from_isHealthy(bank, interbank)
            elif source == "illiquity":
                self.calc_isHealthy_from_isIlliquity(bank, interbank)
                self.update_isIlliquity_from_isHealthy(bank, interbank)
            elif source == "bankrupt":
                # @testprintln "无须更新！"
                pass
            elif source == "off":
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "insolvent":
            if source == "any":
                self.calc_isInsolvent(bank, interbank)
                self.update_isHealthy_from_isInsolvent(bank, interbank)
            elif source == "healthy":
                self.calc_isInsolvent_from_isHealthy(bank, interbank)
                self.update_isHealthy_from_isInsolvent(bank, interbank)
            elif source == "insolvent":
                # @testprintln "无须更新！"
                pass
            elif source == "illiquity":
                # calc_isIlliquity_from_isHealthy(bank, interbank) # 错误，可以删除！
                pass
                # calc_isHealthy_from_isIlliquity(bank, interbank) # 错误，可以删除！
                # calc_isHealthy_from_isInsolvent(bank, interbank) # 错误，可以删除！
                # calc_isInsolvent_from_isHealthy(bank, interbank) # 错误，可以删除！
                # @testprintln "无须更新！"
            elif source == "bankrupt":
                # @testprintln "无须更新！"
                pass
            elif source == "off":
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "illiquity":
            if source == "any":
                self.calc_isIlliquity(bank, interbank)
                self.update_isHealthy_from_isIlliquity(bank, interbank)
            elif source == "healthy":
                self.calc_isIlliquity_from_isHealthy(bank, interbank)
                self.update_isHealthy_from_isIlliquity(bank, interbank)
            elif source == "insolvent":
                # calc_isHealthy_from_isInsolvent(bank, interbank) # 错误，可以删除！
                # update_isInsolvent_from_isHealthy(bank, interbank) # 错误，可以删除！
                # update_isIlliquity_from_isHealthy(bank, interbank) # 错误，可以删除！
                # @testprintln "无须更新！"
                pass
            elif source == "illiquity":
                # @testprintln "无须更新！"
                pass
            elif source == "bankrupt":
                # @testprintln "无须更新！"
                pass
            elif source == "off":
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "bankrupt":
            if source == "any":
                self.calc_isBankrupt(bank, interbank)
            elif source == "healthy":
                self.calc_isInsolvent_from_isHealthy(bank, interbank)
                self.update_isHealthy_from_isInsolvent(bank, interbank)
                self.calc_isIlliquity(bank, interbank)
                self.update_isHealthy_from_isIlliquity(bank, interbank)
                self.calc_isBankrupt_from_isInsolvent(bank, interbank)
                self.calc_isBankrupt_from_isIlliquity(bank, interbank)
            elif source == "insolvent":
                self.calc_isBankrupt_from_isInsolvent(bank, interbank)
            elif source == "illiquity":
                self.calc_isBankrupt_from_isIlliquity(bank, interbank)
            elif source == "bankrupt":
                # @testprintln "无须更新！"
                pass
            elif source == "off":
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "off":
            if source == "any":
                self.calc_isOff(bank, interbank)
                self.update_isOn_from_isOff(bank, interbank)
            elif source == "healthy":
                # @testprintln "无须更新！"
                pass
            elif source == "insolvent":
                # @testprintln "无须更新！"
                pass
            elif source == "illiquity":
                # @testprintln "无须更新！"
                pass
            elif source == "bankrupt":
                self.calc_isOff_from_isBankrupt(bank, interbank)
                self.update_isOn_from_isOff(bank, interbank)
                self.update_isBankrupt_from_isOff(bank, interbank)
                interbank.cre = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "creditor")
                interbank.deb = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "debtor")
            elif source == "off":
                # @testprintln "无须更新！"
                pass
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "on":
            if source == "any":
                self.together_isOn(bank, interbank)
                self.update_isOff_from_isOn(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "needed repay BI":
            if source == "any":
                self.calc_isNeededBoBI(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "enabled repay BI":
            if source == "any":
                self.calc_isEnabledBoBI(bank, interbank)
            elif source == "needed repay BI":
                self.calc_isEnabledBoBI_from_isNeededBoBI(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "needed repay Z_D":
            if source == "any":
                self.calc_isNeededBoD(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "enabled repay Z_D":
            if source == "any":
                self.calc_isEnabledBoD(bank, interbank)
            elif source == "needed repay Z_D":
                self.calc_isEnabledBoD_from_isNeededBoD(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "needed collect A_P":
            if source == "any":
                self.calc_isNeededLiP(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        elif target == "enabled collect A_P":
            if source == "any":
                self.calc_isEnabledLiP(bank, interbank)
            elif source == "needed collect A_P":
                self.calc_isEnabledLiP_from_isNeededLiP(bank, interbank)
            else:
                raise Exception("关键词source取词错误".format(source))
                pass
        else:
            raise Exception("关键词target取词错误".format(target))
            pass
        pass # functions


    pass # class