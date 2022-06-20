## 函数：破产银行应偿还负债冲击阶段

##########################################
#状态/开发
##########################################

"函数：破产银行应偿还负债冲击阶段"#HACK冗余，可以替代以
def stage_bankrupt_repay_shock(self, A:SystemicRiskAgent, b:TypeState{1}, ib:TypeState{2}, para:dict, env:dict):
    ## # 破产银行遭受偿还冲击
    # @testprintln "开始阶段$(env['stage_name'])："

    update_B_state(BB, BI; to="bankrupt", from="any")
    A.BB.Shock_D_run_t[A.BB.br] = A.BB.Zm_D[A.BB.br] # 计算破产银行遭受偿还居民存款冲击
    A.BB.Shock_BI_t[A.BB.br] = A.BB.Z_BI_all[A.BB.br] # 计算破产银行遭受偿还银行间负债冲击

    # @testprintln "结束阶段$(env['stage_name'])。"
    return BB, BI
    pass # functions
