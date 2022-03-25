"功能函数集：计算冲击。"

##########################################
#状态/使用
##########################################



## 函数区



## 更新各银行与各银行间之冲击


# "汇总综合外生冲击。" #HACK无用
# function together_Shock_exBI!(bank::BankCommercial, bankState::TypeState{1})
#     bank.Shock_exBI_t[bankState] = para["theta_Shock_exBI_t"] .* bank.Shock_P_def_t[bankState] + (1 - para["theta_Shock_exBI_t"]) .* bank.Shock_D_run_t[bankState]
# end

"汇总总冲击目标"
function together_Shock_target!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_t[bankState] = bank.Shock_exBI_t[bankState] + bank.Shock_BI_t[bankState]
end

"汇总总冲击源头"
function together_Shock_source!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_s[bankState] = bank.Shock_exBI_s[bankState] + bank.Shock_BI_s[bankState]
end

"汇总银行外冲击目标"
function together_Shock_exBI_target!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_exBI_t[bankState] = bank.Shock_P_def_t[bankState] + bank.Shock_D_run_t[bankState]
end

"汇总银行外冲击源头"
function together_Shock_exBI_source!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_exBI_s[bankState] = bank.Shock_P_run_s[bankState] + bank.Shock_D_def_s[bankState]
end

"汇总违约损失冲击目标"
function together_Shock_def_target!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_def_t[bankState] = bank.Shock_P_def_t[bankState] + bank.Shock_BI_def_t[bankState]
end

"汇总违约损失冲击源头"
function together_Shock_def_source!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_def_s[bankState] = bank.Shock_D_def_s[bankState] + bank.Shock_BI_def_s[bankState]
end

"汇总挤兑流动冲击目标"
function together_Shock_run_target!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_run_t[bankState] = bank.Shock_D_run_t[bankState] + bank.Shock_BI_run_t[bankState]
end

"汇总银行间流动性冲击目标。"
function together_Shock_BI_run_target!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_BI_run_t[bankState] = bank.Shock_BI_run_ilq_t[bankState] + bank.Shock_BI_run_br_t[bankState]
end

"汇总挤兑流动冲击源头"
function together_Shock_run_source!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_run_s[bankState] = bank.Shock_P_run_s[bankState] + bank.Shock_BI_run_s[bankState]
end

"汇总银行间流动性冲击源头。"
function together_Shock_BI_run_source!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_BI_run_s[bankState] = bank.Shock_BI_run_ilq_s[bankState] + bank.Shock_BI_run_br_s[bankState]
end

"汇总银行内资产负债冲击。"
function together_Shock_B!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_B[bankState] = bank.Shock_B_A[bankState] + bank.Shock_B_Z[bankState]
end

"汇总银行间冲击源头。"
function together_Shock_BI_source!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_BI_s[bankState] = bank.Shock_BI_def_s[bankState] + bank.Shock_BI_run_s[bankState]
end

"汇总银行间流动性冲击。"
function together_Shock_BI_run!(interbank::BankInterbank, interbankState::TypeState{2})
    interbank.Shock_BI_run[interbankState] = interbank.Shock_BI_run_ilq[interbankState] + interbank.Shock_BI_run_br[interbankState]
end

"汇总银行间冲击。"
function together_Shock_BI!(interbank::BankInterbank, interbankState::TypeState{2})
    interbank.Shock_BI[interbankState] = interbank.Shock_BI_def[interbankState] + interbank.Shock_BI_run[interbankState]
end

"加总资不抵债银行之银行间违约损失冲击目标。"
function sum_Shock_BI_def_target!(bank::BankCommercial, interbank::BankInterbank, bankState::TypeState{1}, interbankState::TypeState{2})
    bank.Shock_BI_def_t[bankState] = sum(interbank.Shock_BI_def .* interbank.on, dims = 2)[bankState]
end

"加总流动性短缺银行之银行间流动性冲击目标。"
function sum_Shock_BI_run_ilq_target!(bank::BankCommercial, interbank::BankInterbank, bankState::TypeState{1}, interbankState::TypeState{2})
    bank.Shock_BI_run_ilq_t[bankState] = sum(interbank.Shock_BI_run_ilq .* interbank.on, dims = 2)[bankState]
end

"加总破产银行之银行间流动性冲击目标。"
function sum_Shock_BI_run_br_target!(bank::BankCommercial, interbank::BankInterbank, bankState::TypeState{1}, interbankState::TypeState{2})
    bank.Shock_BI_run_br_t[bankState] = sum(interbank.Shock_BI_run_br .* interbank.on, dims = 2)[bankState]
end

"汇总银行间冲击目标。"
function together_Shock_BI_target!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_BI_t[bankState] = bank.Shock_BI_def_t[bankState] + bank.Shock_BI_run_t[bankState]
end

#状态：暂不使用。"传导非银行间贷款损失外生冲击。"
function conduct_Shock_L_exBI!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_B_A[bankState] = bank.Shock_P_def_t[bankState]
end

#状态：暂不使用。"传导存款损失外生冲击。"
function conduct_Shock_D!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_B_Z[bankState] = bank.Shock_D_run_t[bankState]
end

#状态：暂不使用。"传导银行间违约损失冲击。"
function conduct_Shock_BI_def_t!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_B_A[bankState] = bank.Shock_BI_def_t[bankState]
end

#状态：暂不使用。"传导银行间挤兑流动冲击。"
function conduct_Shock_BI_run_t!(bank::BankCommercial, bankState::TypeState{1})
    bank.Shock_B_A[bankState] = bank.Shock_BI_run_t[bankState]
end

"清零本回合结束时所有不必要的冲击变量"
function clear_Shock_BI_and_exBI!(bank::BankCommercial, interbank::BankInterbank, bankState::TypeState{1}, interbankState::TypeState{2})
    bank.Shock_P_def_t = ZEROS1
    bank.Shock_D_run_t = ZEROS1
    bank.Shock_P_run_s = ZEROS1
    bank.Shock_D_def_s = ZEROS1
    bank.Shock_BI_def_s = ZEROS1
    bank.Shock_BI_run_ilq_s = ZEROS1
    bank.Shock_BI_run_br_s = ZEROS1
    interbank.Shock_BI_def = ZEROS2
    interbank.Shock_BI_run_ilq = ZEROS2
    interbank.Shock_BI_run_br = ZEROS2
    bank.Shock_BI_def_t = ZEROS1
    bank.Shock_BI_run_ilq_t = ZEROS1
    bank.Shock_BI_run_br_t = ZEROS1
end

"清零本回合中期所有不必要的冲击变量"
function clear_Shock_inB!(bank::BankCommercial)
    bank.Shock_B_A = ZEROS1
    bank.Shock_B_Z = ZEROS1
end

"""
更新各银行之冲击。
# Arguments
`byWay::String`:  参数，通过该参数指定的变量作为已知变量，驱动，以更新其他相关各变量。
- `all`:  更新全部冲击变量；
- `clear Shock_BI and Shock_exBI`:  清零本回合结束时，除了``Shock_{B}``系列的变量以外的，所有不必要的冲击变量，暨所有``Shock_{BI}``系列的变量、``Shock_{exBI}``系列的变量；
- `clear Shock_B_A and Shock_B_Z`:  清零银行内资产负债冲击变量；
- `Shock_P_def_t`:  已知``Shock_{P,def}[i]``，更新其余冲击变量；
- `Shock_P_run_s`:  已知``Shock_{P,run}[i]``，更新其余冲击变量；
- `Shock_D_run_t`:  已知``Shock_{D,run}[i]``，更新其余冲击变量；
- `Shock_D_def_s`:  已知``Shock_{D,def}[i]``，更新其余冲击变量；
- `Shock_B_A`:  已知``Shock_{B,b}``，更新其余冲击变量；
- `Shock_B_Z`:  已知``Shock_{B,Z}``，更新其余冲击变量；
- `Shock_BI_def_s`:  已知``Shock_{BI,def}[: ,i_{isv}]``，更新其余冲击变量；
- `Shock_BI_run_ilq_s`:  已知``Shock_{BI,run}[: ,i_{ilq}]``，更新其余冲击变量；
- `Shock_BI_run_br_s`:  已知``Shock_{BI,run}[: ,i_{br}]``，更新其余冲击变量；
- `Shock_BI_def`:  已知``Shock_{BI,def}[j,i_{isv}]``，更新其余冲击变量；
- `Shock_BI_run_ilq`:  已知``Shock_{BI,run}[j,i_{ilq}]``，更新其余冲击变量；
- `Shock_BI_run_br`:  已知``Shock_{BI,run}[j,i_{br}]``，更新其余冲击变量；
- `Shock_BI_def_t`:  已知``Shock_{BI,def}[j,: }],:  \\in i_{isv}``，更新其余冲击变量；
- `Shock_BI_run_ilq_t`:  已知``Shock_{BI,run}[j,: }],:  \\in i_{ilq}``，更新其余冲击变量；
- `Shock_BI_run_br_t`:  已知``Shock_{BI,run}[j,: }],:  \\in i_{br}``，更新其余冲击变量；
"""
function update_B_Shock!(bank::BankCommercial, interbank::BankInterbank, bankState::TypeState{1}, interbankState::TypeState{2}; byWay::String = "all")
    if byWay == "all"
        together_Shock_B!(bank, bankState)
        together_Shock_BI_run_source!(bank, bankState)
        together_Shock_BI_source!(bank, bankState)
        together_Shock_exBI_source!(bank, bankState)
        together_Shock_source!(bank, bankState)
        together_Shock_def_source!(bank, bankState)
        together_Shock_run_source!(bank, bankState)
        together_Shock_BI_run!(interbank, interbankState)
        together_Shock_BI!(interbank, interbankState)
        sum_Shock_BI_def_target!(bank, interbank, bankState, interbankState)
        sum_Shock_BI_run_ilq_target!(bank, interbank, bankState, interbankState)
        sum_Shock_BI_run_br_target!(bank, interbank, bankState, interbankState)
        together_Shock_BI_run_target!(bank, bankState)
        together_Shock_BI_target!(bank, bankState)
        together_Shock_exBI_target!(bank, bankState)
        together_Shock_target!(bank, bankState)
        together_Shock_def_target!(bank, bankState)
        together_Shock_run_target!(bank, bankState)
    elseif byWay == "clear Shock_BI and Shock_exBI"
        clear_Shock_BI_and_exBI!(bank, interbank, bankState, interbankState)
        together_Shock_BI_run_source!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_BI_source!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_exBI_source!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_source!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_def_source!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_run_source!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_BI_run!(interbank, TypeState{2}((bank.on .|| bank.off) .&& (bank.on .|| bank.off)'))
        together_Shock_BI!(interbank, TypeState{2}((bank.on .|| bank.off) .&& (bank.on .|| bank.off)'))
        sum_Shock_BI_def_target!(bank, interbank, TypeState{1}(bank.on .|| bank.off), TypeState{2}((bank.on .|| bank.off) .&& (bank.on .|| bank.off)'))
        sum_Shock_BI_run_ilq_target!(bank, interbank, TypeState{1}(bank.on .|| bank.off), TypeState{2}((bank.on .|| bank.off) .&& (bank.on .|| bank.off)'))
        sum_Shock_BI_run_br_target!(bank, interbank, TypeState{1}(bank.on .|| bank.off), TypeState{2}((bank.on .|| bank.off) .&& (bank.on .|| bank.off)'))
        together_Shock_BI_run_target!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_BI_target!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_exBI_target!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_target!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_def_target!(bank, TypeState{1}(bank.on .|| bank.off))
        together_Shock_run_target!(bank, TypeState{1}(bank.on .|| bank.off))
    elseif byWay == "clear Shock_B_A and Shock_B_Z"
        clear_Shock_inB!(bank)
        together_Shock_B!(bank, TypeState{1}(bank.on .|| bank.off))
    elseif byWay == "Shock_P_def_t"
        together_Shock_exBI_target!(bank, bankState)
        together_Shock_target!(bank, bankState)
        together_Shock_def_target!(bank, bankState)
    elseif byWay == "Shock_P_run_s"
        together_Shock_exBI_source!(bank, bankState)
        together_Shock_source!(bank, bankState)
        together_Shock_run_source!(bank, bankState)
    elseif byWay == "Shock_D_run_t"
        together_Shock_exBI_target!(bank, bankState)
        together_Shock_target!(bank, bankState)
        together_Shock_run_target!(bank, bankState)
    elseif byWay == "Shock_D_def_s"
        together_Shock_exBI_source!(bank, bankState)
        together_Shock_source!(bank, bankState)
        together_Shock_def_source!(bank, bankState)
    elseif byWay == "Shock_B_A" || byWay == "Shock_B_Z"
        together_Shock_B!(bank, bankState)
    elseif byWay == "Shock_BI_def_s"
        together_Shock_BI_source!(bank, bankState)
        together_Shock_source!(bank, bankState)
        together_Shock_def_source!(bank, bankState)
    elseif byWay == "Shock_BI_run_ilq_s" || byWay == "Shock_BI_run_br_s"
        together_Shock_BI_run_source!(bank, bankState)
        together_Shock_BI_source!(bank, bankState)
        together_Shock_source!(bank, bankState)
        together_Shock_run_source!(bank, bankState)
    elseif byWay == "Shock_BI_def"
        together_Shock_BI!(interbank, interbankState)
        sum_Shock_BI_def_target!(bank, interbank, bankState, interbankState)
        together_Shock_BI_target!(bank, bankState)
        together_Shock_target!(bank, bankState)
        together_Shock_def_target!(bank, bankState)
    elseif byWay == "Shock_BI_run_ilq"
        together_Shock_BI_run!(interbank, interbankState)
        together_Shock_BI!(interbank, interbankState)
        sum_Shock_BI_run_ilq_target!(bank, interbank, bankState, interbankState)
        together_Shock_BI_run_target!(bank, bankState)
        together_Shock_BI_target!(bank, bankState)
        together_Shock_target!(bank, bankState)
        together_Shock_run_target!(bank, bankState)
    elseif byWay == "Shock_BI_run_br"
        together_Shock_BI_run!(interbank, interbankState)
        together_Shock_BI!(interbank, interbankState)
        sum_Shock_BI_run_br_target!(bank, interbank, bankState, interbankState)
        together_Shock_BI_run_target!(bank, bankState)
        together_Shock_BI_target!(bank, bankState)
        together_Shock_target!(bank, bankState)
        together_Shock_run_target!(bank, bankState)
    elseif byWay == "Shock_BI_def_t"
        together_Shock_BI_target!(bank, bankState)
        together_Shock_target!(bank, bankState)
        together_Shock_def_target!(bank, bankState)
    elseif byWay == "Shock_BI_run_ilq_t" || byWay == "Shock_BI_run_br_t"
        together_Shock_BI_run_target!(bank, bankState)
        together_Shock_BI_target!(bank, bankState)
        together_Shock_target!(bank, bankState)
        together_Shock_run_target!(bank, bankState)
    else
        throw(DomainError(byWay, "关键词取值错误！"))
    end


end












