# "功能函数集：计算构建银行与银行间相关状态及其转换。"

## 功能函数集：计算构建银行与银行间相关状态及其转换。

##########################################
#状态/使用
##########################################

from SystemicRisk.core import np,env,BankCommercial,BankInterbank,TypeState,LESS1,LESS2


class BankState:

    def init_listOfRelationInStateOfBanks(self, bank:BankCommercial, interbank:BankInterbank):
        """
        初始化银行状态关系列表
        """
        interbank.cre = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "creditor")
        interbank.deb = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "debtor")
        pass
    
    
    "计算示性向量之于银行健康的。"
    def calc_isHealthy(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.E_all >= LESS1 & bank.A_Q >= LESS1 & bank.Shock_def_t + LESS1 <= bank.E_all & bank.Shock_run_t + LESS1 <= bank.A_Q & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass
    
    "计算示性向量之于银行健康的，来自资不抵债的。"
    def calc_isHealthy_from_isInsolvent(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.E_all >= LESS1 & bank.A_Q >= LESS1 & bank.Shock_def_t + LESS1 <= bank.E_all & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass
    
    "更新示性向量之于银行健康的，来自资不抵债的。"
    def update_isHealthy_from_isInsolvent(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (~(bank.isv | bank.ilq) & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass
    
    "计算示性向量之于银行健康的，来自流动性短缺的。" # 内容同于calc_isHealthy。
    def calc_isHealthy_from_isIlliquity(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.E_all >= LESS1 & bank.A_Q >= LESS1 & bank.Shock_run_t + LESS1 <= bank.A_Q & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass
    
    "更新示性向量之于银行健康的，来自流动性短缺的。" # 内容同于update_isHealthy_from_isInsolvent
    def update_isHealthy_from_isIlliquity(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (~(bank.isv | bank.ilq) & bank.on)
        if bank.hel != condition:
            bank.hel = condition
            interbank.hel = (bank.hel & bank.hel.T)
            pass
        pass
    
    
    
    "计算示性向量之于银行资不抵债的。"
    def calc_isInsolvent(self, bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.A_all < bank.Z_all + LESS1 | bank.E_all < LESS1 | bank.Shock_def_t + LESS1 > bank.E_all) & bank.on)
        if bank.isv != condition:
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "creditor")
            interbank.deb_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "debtor")
            pass
        pass
    
    "计算示性向量之于银行资不抵债的，来自健康的。"
    def calc_isInsolvent_from_isHealthy(self, bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.A_all < bank.Z_all + LESS1 | bank.E_all < LESS1 | bank.Shock_def_t + LESS1 > bank.E_all) & bank.on)
        if bank.isv != condition:
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "creditor")
            interbank.deb_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "debtor")
            pass
        pass
    
    "更新示性向量之于银行资不抵债的，来自健康的。" # 内容同于calc_isInsolvent_from_isHealthy
    def update_isInsolvent_from_isHealthy(self, bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.A_all < bank.Z_all + LESS1 | bank.E_all < LESS1 | bank.Shock_def_t + LESS1 > bank.E_all) & bank.on)
        if bank.isv != condition:
            bank.isv = condition
            interbank.isv = (bank.isv | bank.isv.T)
            interbank.cre_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "creditor")
            interbank.deb_isv = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.isv, goal = "debtor")
            pass
        pass
    
    "计算示性向量之于银行流动性短缺的。"
    def calc_isIlliquity(self, bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.Shock_run_t + LESS1 >= bank.A_Q) & bank.on)
        if bank.ilq != condition:
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "creditor")
            interbank.deb_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "debtor")
            pass
        pass
    
    "计算示性向量之于银行流动性短缺的，来自健康的。" # 内容同于calc_isIlliquity
    def calc_isIlliquity_from_isHealthy(self, bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.Shock_run_t + LESS1 >= bank.A_Q) & bank.on)
        if bank.ilq != condition:
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "creditor")
            interbank.deb_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "debtor")
            pass
        pass
    
    "更新示性向量之于银行流动性短缺的，来自健康的。" # 内容同于calc_isIlliquity
    def update_isIlliquity_from_isHealthy(self, bank:BankCommercial, interbank:BankInterbank):
        condition = ((bank.Shock_run_t + LESS1 >= bank.A_Q) & bank.on)
        if bank.ilq != condition:
            bank.ilq = condition
            interbank.ilq = (bank.ilq | bank.ilq.T)
            interbank.cre_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "creditor")
            interbank.deb_ilq = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.ilq, goal = "debtor")
            pass
        pass
    
    "计算示性向量之于银行破产的。"
    def calc_isBankrupt(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.isv | bank.ilq)
        if bank.br != condition:
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass
    
    "计算示性向量之于破产的，来自资不抵债的。" # 同于calc_isBankrupt
    def calc_isBankrupt_from_isInsolvent(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.isv | bank.ilq)
        if bank.br != condition:
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass
    
    "计算示性向量之于破产的，来自流动性短缺的。" # 同于calc_isBankrupt
    def calc_isBankrupt_from_isIlliquity(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.isv | bank.ilq)
        if bank.br != condition:
            bank.br = condition
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass
    
    "计算示性向量之于银行存在的。"
    def together_isOn(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.hel | bank.isv | bank.ilq | bank.br)
        if bank.on != condition:
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            # interbank.listOfCreditorsInOn = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "creditor") #HACK，未定义，无用。
            # interbank.listOfDebtorsInOn = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "debtor") #HACK，未定义，无用。
            pass
        pass
    
    "更新示性向量之于银行破产的，来自退出的。" #FIXME，有一定不稳定的风险。
    def update_isBankrupt_from_isOff(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (bank.off)
        if bank.br == condition:
            bank.br[: ] = np.false(env['num_bank'])
            interbank.br = (bank.br & bank.br.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass
    
    "更新示性向量之于银行存在的，来自退出的。"
    def update_isOn_from_isOff(self, bank:BankCommercial, interbank:BankInterbank):
        condition = (~bank.off)
        if bank.on != condition:
            bank.on = condition
            interbank.on = (bank.on & bank.on.T)
            interbank.cre_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "creditor")
            interbank.deb_br = self.calc_listOfRelationInStateOfBanks(interbank, isState = bank.br, goal = "debtor")
            pass
        pass
    
    "计算示性向量之于银行退出的。"
    def calc_isOff(self, bank:BankCommercial, interbank:BankInterbank):
        condition = bank.br | bank.off
        if bank.off != condition:
            bank.off = condition
            interbank.off = (bank.off & bank.off.T)
            pass
        pass
    
    "更新示性向量之于银行退出的，来自存在的。"
    def update_isOff_from_isOn(self, bank:BankCommercial, interbank:BankInterbank):
        condition = ~bank.on
        if bank.off != condition:
            bank.off = condition
            interbank.off = (bank.off & bank.off.T)
            pass
        pass
    
    "计算示性向量之于银行退出的，来自破产的。"
    def calc_isOff_from_isBankrupt(self, bank:BankCommercial, interbank:BankInterbank):
        self.calc_isOff(bank, interbank)
        interbank.cre_br = []
        interbank.deb_br = []
        pass
    
    "计算示性向量之于银行需要偿还银行间负债的。"
    def calc_isNeededBoBI(self, bank:BankCommercial, interbank:BankInterbank):
        bank.nBoBI = (bank.Shock_BI_run_ilq_t > 0 & bank.on)
        pass
    
    "计算示性向量之于银行能够偿还银行间负债的。"
    def calc_isEnabledBoBI(self, bank:BankCommercial, interbank:BankInterbank):
        bank.eBoBI = (bank.Shock_BI_run_ilq_t > 0 & bank.A_Q > 0 & bank.on)
        pass
    
    "计算示性向量之于银行能够偿还银行间负债的，从需要偿还银行间负债的。"
    def calc_isEnabledBoBI_from_isNeededBoBI(self, bank:BankCommercial, interbank:BankInterbank):
        bank.eBoBI = (bank.nBoBI & bank.A_Q > 0)
        pass
    
    "计算示性向量之于银行需要偿还居民部门存款的。"
    def calc_isNeededBoD(self, bank:BankCommercial, interbank:BankInterbank):
        bank.nBoD = (bank.Shock_D_run_t > 0 & bank.on)
        pass
    
    "计算示性向量之于银行能够偿还居民部门存款的。"
    def calc_isEnabledBoD(self, bank:BankCommercial, interbank:BankInterbank):
        bank.eBoD = (bank.Shock_D_run_t > 0 & bank.A_Q > 0 & bank.on)
        pass
    
    "计算示性向量之于银行能够偿还居民部门存款的，从需要偿还居民部门存款的。"
    def calc_isEnabledBoD_from_isNeededBoD(self, bank:BankCommercial, interbank:BankInterbank):
        bank.eBoD = (bank.nBoD & bank.A_Q > 0)
        pass
    
    "计算示性向量之于银行需要收回厂商贷款的。"
    def calc_isNeededLiP(self, bank:BankCommercial, interbank:BankInterbank):
        bank.nLiP = (bank.Shock_P_run_s > 0 & bank.on)
        pass
    
    "计算示性向量之于银行能够收回厂商贷款的。"
    def calc_isEnabledLiP(self, bank:BankCommercial, interbank:BankInterbank):
        bank.eLiP = (bank.Shock_P_run_s > 0 & bank.on) #HACK后续可能会补充条件 & producer.A_Q > 0
        pass
    
    "计算示性向量之于银行能够收回厂商贷款的，从需要收回厂商贷款的。"
    def calc_isEnabledLiP_from_isNeededLiP(self, bank:BankCommercial, interbank:BankInterbank):
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
    def calc_listOfRelationInStateOfBanks(self, interbank:BankInterbank, isState:Vector, goal:str):
        # 计算示性矩阵之于银行间风险敞口的
        if goal == "debtor":
            isExposure = ((interbank.A_BI > 0.0) & isState)
        elif goal == "creditor":
            isExposure = ((interbank.Z_BI > 0.0) & isState)
        else:
            pass
        listOfRelationInStateOfBanks = [[] for i in 1: env['num_bank']]
        for i in 1: env['num_bank']
            listOfRelationInStateOfBanks[i] = findall(isExposure[i, : ]) # 获取对应状态下的债权或者债务关系的银行列表
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
    def update_B_state(self, bank:BankCommercial, interbank:BankInterbank, to:String = "any", from:String = "any"):
        if to == "any": #FIXME 这个可能有缺陷:
            if from == "any":
                init_listOfRelationInStateOfBanks(bank, interbank)
                calc_isInsolvent(bank, interbank)
                calc_isIlliquity(bank, interbank)
                calc_isHealthy(bank, interbank)
                calc_isBankrupt(bank, interbank)
                together_isOn(bank, interbank)
                # calc_isOff(bank, interbank)
                # calc_isOn(bank, interbank)
            elif from == "healthy":
                calc_isInsolvent_from_isHealthy(bank, interbank)
                update_isHealthy_from_isInsolvent(bank, interbank)
                calc_isIlliquity_from_isHealthy(bank, interbank)
                update_isHealthy_from_isIlliquity(bank, interbank)
            elif from == "insolvent":
                calc_isHealthy_from_isInsolvent(bank, interbank)
                update_isInsolvent_from_isHealthy(bank, interbank)
                calc_isBankrupt_from_isInsolvent(bank, interbank)
            elif from == "illiquity":
                calc_isHealthy_from_isIlliquity(bank, interbank)
                update_isIlliquity_from_isHealthy(bank, interbank)
                calc_isBankrupt_from_isIlliquity(bank, interbank)
            elif from == "bankrupt":
                calc_isOff_from_isBankrupt(bank, interbank)
                update_isOn_from_isOff(bank, interbank)
                interbank.cre = calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "creditor")
                interbank.deb = calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "debtor")
            elif from == "off":
                # @testprintln "无须更新！"
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "healthy":
            if from == "any":
                calc_isHealthy(bank, interbank)
                update_isInsolvent_from_isHealthy(bank, interbank)
                update_isIlliquity_from_isHealthy(bank, interbank)
            elif from == "healthy":
                # @testprintln "无须更新！"
            elif from == "insolvent":
                calc_isHealthy_from_isInsolvent(bank, interbank)
                calc_isInsolvent_from_isHealthy(bank, interbank)
            elif from == "illiquity":
                calc_isHealthy_from_isIlliquity(bank, interbank)
                update_isIlliquity_from_isHealthy(bank, interbank)
            elif from == "bankrupt":
                # @testprintln "无须更新！"
            elif from == "off":
                # @testprintln "无须更新！"
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "insolvent":
            if from == "any":
                calc_isInsolvent(bank, interbank)
                update_isHealthy_from_isInsolvent(bank, interbank)
            elif from == "healthy":
                calc_isInsolvent_from_isHealthy(bank, interbank)
                update_isHealthy_from_isInsolvent(bank, interbank)
            elif from == "insolvent":
                # @testprintln "无须更新！"
            elif from == "illiquity":
                # calc_isIlliquity_from_isHealthy(bank, interbank) # 错误，可以删除！
                # calc_isHealthy_from_isIlliquity(bank, interbank) # 错误，可以删除！
                # calc_isHealthy_from_isInsolvent(bank, interbank) # 错误，可以删除！
                # calc_isInsolvent_from_isHealthy(bank, interbank) # 错误，可以删除！
                # @testprintln "无须更新！"
            elif from == "bankrupt":
                # @testprintln "无须更新！"
            elif from == "off":
                # @testprintln "无须更新！"
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "illiquity":
            if from == "any":
                calc_isIlliquity(bank, interbank)
                update_isHealthy_from_isIlliquity(bank, interbank)
            elif from == "healthy":
                calc_isIlliquity_from_isHealthy(bank, interbank)
                update_isHealthy_from_isIlliquity(bank, interbank)
            elif from == "insolvent":
                # calc_isHealthy_from_isInsolvent(bank, interbank) # 错误，可以删除！
                # update_isInsolvent_from_isHealthy(bank, interbank) # 错误，可以删除！
                # update_isIlliquity_from_isHealthy(bank, interbank) # 错误，可以删除！
                # @testprintln "无须更新！"
            elif from == "illiquity":
                # @testprintln "无须更新！"
            elif from == "bankrupt":
                # @testprintln "无须更新！"
            elif from == "off":
                # @testprintln "无须更新！"
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "bankrupt":
            if from == "any":
                calc_isBankrupt(bank, interbank)
            elif from == "healthy":
                calc_isInsolvent_from_isHealthy(bank, interbank)
                update_isHealthy_from_isInsolvent(bank, interbank)
                calc_isIlliquity(bank, interbank)
                update_isHealthy_from_isIlliquity(bank, interbank)
                calc_isBankrupt_from_isInsolvent(bank, interbank)
                calc_isBankrupt_from_isIlliquity(bank, interbank)
            elif from == "insolvent":
                calc_isBankrupt_from_isInsolvent(bank, interbank)
            elif from == "illiquity":
                calc_isBankrupt_from_isIlliquity(bank, interbank)
            elif from == "bankrupt":
                # @testprintln "无须更新！"
            elif from == "off":
                # @testprintln "无须更新！"
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "off":
            if from == "any":
                calc_isOff(bank, interbank)
                update_isOn_from_isOff(bank, interbank)
            elif from == "healthy":
                # @testprintln "无须更新！"
            elif from == "insolvent":
                # @testprintln "无须更新！"
            elif from == "illiquity":
                # @testprintln "无须更新！"
            elif from == "bankrupt":
                calc_isOff_from_isBankrupt(bank, interbank)
                update_isOn_from_isOff(bank, interbank)
                update_isBankrupt_from_isOff(bank, interbank)
                interbank.cre = calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "creditor")
                interbank.deb = calc_listOfRelationInStateOfBanks(interbank, isState = bank.on, goal = "debtor")
            elif from == "off":
                # @testprintln "无须更新！"
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "on":
            if from == "any":
                together_isOn(bank, interbank)
                update_isOff_from_isOn(bank, interbank)
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "needed repay BI":
            if from == "any":
                calc_isNeededBoBI(bank, interbank)
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "enabled repay BI":
            if from == "any":
                calc_isEnabledBoBI(bank, interbank)
            elif from == "needed repay BI":
                calc_isEnabledBoBI_from_isNeededBoBI(bank, interbank)
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "needed repay Z_D":
            if from == "any":
                calc_isNeededBoD(bank, interbank)
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "enabled repay Z_D":
            if from == "any":
                calc_isEnabledBoD(bank, interbank)
            elif from == "needed repay Z_D":
                calc_isEnabledBoD_from_isNeededBoD(bank, interbank)
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "needed collect A_P":
            if from == "any":
                calc_isNeededLiP(bank, interbank)
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        elif to == "enabled collect A_P":
            if from == "any":
                calc_isEnabledLiP(bank, interbank)
            elif from == "needed collect A_P":
                calc_isEnabledLiP_from_isNeededLiP(bank, interbank)
            else:
                throw(DomainError(byWay, "关键词from取值错误！"))
                pass
        else:
            throw(DomainError(to, "关键词to取值错误！"))
            pass
        pass # functions
        
        
    pass # class