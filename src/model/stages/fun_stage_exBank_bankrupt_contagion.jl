## 函数：外生破产银行间挤兑流动冲击阶段

##########################################
#状态/暂时用不到
##########################################

#TODO"函数：外生破产银行间挤兑流动冲击阶段"
function stage_exBank_bankrupt_contagion!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict, env::Dict)
    ## # 外生破产银行间挤兑流动传染
    # env[:stageName] = "外生破产银行间挤兑流动冲击阶段"
    @test println("开始阶段$(env[:stageName])：")
    
    BB.br[para[:list_Shock_exBI_t]] = para[:Shock_exBI_t][para[:list_Shock_exBI_t]]
    update_B_state!(BB, BI; to="bankrupt", from="any")

    @test println("结束阶段$(env[:stageName])。")
    # return BB, BI

end # function
