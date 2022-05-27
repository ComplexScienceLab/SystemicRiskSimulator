## 函数：破产银行应偿还负债冲击阶段

##########################################
#状态/开发
##########################################

"函数：破产银行应偿还负债冲击阶段"#HACK冗余，可以替代以
function stage_bankrupt_repay_shock!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict, env::Dict)
    ## # 破产银行遭受偿还冲击
    @testprintln "开始阶段$(env[:stageName])："

    update_B_state!(BB, BI; to="bankrupt", from="any")
    BB.Shock_D_run_t[BB.br] = BB.Zm_D[BB.br] # 计算破产银行遭受偿还居民存款冲击
    BB.Shock_BI_t[BB.br] = BB.Z_BI_all[BB.br] # 计算破产银行遭受偿还银行间负债冲击

    @testprintln "结束阶段$(env[:stageName])。"
    # return BB, BI
end # function
