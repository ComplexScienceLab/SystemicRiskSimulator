## 函数：外生破产银行间挤兑流动冲击阶段

##########################################
# 状态/暂时用不到
##########################################

from PySystemicRiskLab.core.define.define_agents import BankInterbank, BankCommercial
from PySystemicRiskLab.core.define.define_type import TypeState
from PySystemicRiskLab.core.functions.fun_state import BankState

pass  # end import



# TODO"函数：外生破产银行间挤兑流动冲击阶段"
def stage_exBank_bankrupt_contagion(self, BB: BankCommercial, BI: BankInterbank, b: TypeState, ib: TypeState, para: dict, env: dict):
    ## # 外生破产银行间挤兑流动传染
    # env['stage_name'] = "外生破产银行间挤兑流动冲击阶段"
    # @testprintln "开始阶段$(env['stage_name'])："

    BB.br[para['list_Shock_exBI_t']] = para['Shock_exBI_t'][para['list_Shock_exBI_t']]
    BankState.update_B_state(BB, BI, target="bankrupt", source="any")

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI

    pass  # functions
