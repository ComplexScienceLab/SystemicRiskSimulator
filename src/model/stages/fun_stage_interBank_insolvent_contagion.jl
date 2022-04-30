## 函数：资不抵债银行间违约损失传染阶段

##########################################
#状态/使用
##########################################

"函数：资不抵债银行间违约损失传染阶段"
function stage_interBank_insolvent_contagion!(BB::BankCommercial, BI::BankInterbank, b::TypeState{1}, ib::TypeState{2}, para::Dict, env::Dict)
    ## # 资不抵债银行间违约损失传染阶段
    # env[:stageName] = "资不抵债银行间违约损失传染阶段"
    @test println("开始阶段$(env[:stageName])：")

    for i in findall(BB.isv) # 资不抵债银行违约，导致其对各债权银行负债变动，造成银行间违约冲击
        @. BI.Shock_BI_def[BI.cre[i], i] = abs(BI.Z_BI[i, BI.cre[i]] * BB.Shock_BI_def_s[i] / BB.Z_BI_all[i])
        BI.Z_BI[i, BI.cre[i]] -= BI.Shock_BI_def[BI.cre[i], i]
    end
    # HACK以下部分是否提取出来在阶段1结束之前使用
    update_B_balanceSheet!(BB, BI, b, ib; byWay="alter to A_BI from Z_BI") # 转换银行间资产负债邻接矩阵
    update_B_Shock!(BB, BI, b, ib; byWay="Shock_BI_def") # 更新违约损失冲击目标变量Shock_def_t

    @test println("结束阶段$(env[:stageName])。")
    # return BB, BI
end # function

