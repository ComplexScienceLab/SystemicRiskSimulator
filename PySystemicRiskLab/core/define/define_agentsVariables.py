"""
程序：设置模型变量ModelVariables
"""

##########################################
# #状态/开发
# 开发说明：[相关的修改项](file:///../../src/core/define/define_modelVariables.jl)
##########################################

from PyScripts.settings.set_agentsVariables import set_bankCommercialVariables, set_interbankVariables

pass  # end import

## 生成字典变量 bankCommercial
bankCommercial_dict = set_bankCommercialVariables  # 别名
## 生成字典变量 interbank
bankInterbank_dict = set_interbankVariables  # 别名

#HACK 以下无用
# setOfValuesOfBankCommercialVariables = dict(
#     id=bankCommercial_id,
#     abbr=bankCommercial_abbr,
#     name=bankCommercial_name,
#     A_all=bankCommercial_A_all,
#     A_BI_all=bankCommercial_A_BI_all,
#     A_exBI=bankCommercial_A_exBI,
#     A_P=bankCommercial_A_P,
#     A_Q=bankCommercial_A_Q,
#     A_R=bankCommercial_A_R,
#     A_other=bankCommercial_A_other,
#     Z_all=bankCommercial_Z_all,
#     Z_BI_all=bankCommercial_Z_BI_all,
#     Z_exBI=bankCommercial_Z_exBI,
#     Z_D=bankCommercial_Z_D,
#     Z_other=bankCommercial_Z_other,
#     E_all=bankCommercial_E_all,
#     T_all=bankCommercial_T_all,
#     Lo_all=bankCommercial_Lo_all,
#     Lo_BI_all=bankCommercial_Lo_BI_all,
#     Lo_exBI=bankCommercial_Lo_exBI,
#     Lo_P=bankCommercial_Lo_P,
#     Li_all=bankCommercial_Li_all,
#     Li_BI_all=bankCommercial_Li_BI_all,
#     Li_exBI=bankCommercial_Li_exBI,
#     Li_P=bankCommercial_Li_P,
#     Bi_all=bankCommercial_Bi_all,
#     Bi_BI_all=bankCommercial_Bi_BI_all,
#     Bi_exBI=bankCommercial_Bi_exBI,
#     Bi_D=bankCommercial_Bi_D,
#     Bo_all=bankCommercial_Bo_all,
#     Bo_BI_all=bankCommercial_Bo_BI_all,
#     Bo_exBI=bankCommercial_Bo_exBI,
#     Bo_D=bankCommercial_Bo_D,
#     Shock_t=bankCommercial_Shock_t,
#     Shock_s=bankCommercial_Shock_s,
#     Shock_def_t=bankCommercial_Shock_def_t,
#     Shock_def_s=bankCommercial_Shock_def_s,
#     Shock_run_t=bankCommercial_Shock_run_t,
#     Shock_run_s=bankCommercial_Shock_run_s,
#     Shock_exBI_t=bankCommercial_Shock_exBI_t,
#     Shock_exBI_s=bankCommercial_Shock_exBI_s,
#     Shock_P_run_s=bankCommercial_Shock_P_run_s,
#     Shock_P_def_t=bankCommercial_Shock_P_def_t,
#     Shock_D_def_s=bankCommercial_Shock_D_def_s,
#     Shock_D_run_t=bankCommercial_Shock_D_run_t,
#     Shock_B=bankCommercial_Shock_B,
#     Shock_B_A=bankCommercial_Shock_B_A,
#     Shock_B_Z=bankCommercial_Shock_B_Z,
#     Shock_BI_s=bankCommercial_Shock_BI_s,
#     Shock_BI_t=bankCommercial_Shock_BI_t,
#     Shock_BI_def_s=bankCommercial_Shock_BI_def_s,
#     Shock_BI_def_t=bankCommercial_Shock_BI_def_t,
#     Shock_BI_run_s=bankCommercial_Shock_BI_run_s,
#     Shock_BI_run_t=bankCommercial_Shock_BI_run_t,
#     Shock_BI_run_ilq_s=bankCommercial_Shock_BI_run_ilq_s,
#     Shock_BI_run_ilq_t=bankCommercial_Shock_BI_run_ilq_t,
#     Shock_BI_run_br_s=bankCommercial_Shock_BI_run_br_s,
#     Shock_BI_run_br_t=bankCommercial_Shock_BI_run_br_t,
#     Loss_BI=bankCommercial_Loss_BI,
#     Loss_BI_def_t=bankCommercial_Loss_BI_def_t,
#     Loss_BI_run_t=bankCommercial_Loss_BI_run_t,
#     on=bankCommercial_on,
#     off=bankCommercial_off,
#     hel=bankCommercial_hel,
#     isv=bankCommercial_isv,
#     ilq=bankCommercial_ilq,
#     br=bankCommercial_br,
#     nBoBI=bankCommercial_nBoBI,
#     eBoBI=bankCommercial_eBoBI,
#     nBoD=bankCommercial_nBoD,
#     eBoD=bankCommercial_eBoD,
#     nLiP=bankCommercial_nLiP,
#     eLiP=bankCommercial_eLiP,
#     isAllocatedShock=bankCommercial_isAllocatedShock,
#     listOfExist=bankCommercial_listOfExist,
#     listOfInsolvent=bankCommercial_listOfInsolvent,
#     listOfIlliquity=bankCommercial_listOfIlliquity,
#     listOfBankrupt=bankCommercial_listOfBankrupt,
# )

#HACK 以下无用
# setOfValuesOfInterbankVariables = dict(
#     id=interbank_id,
#     A_BI=interbank_A_BI,
#     Z_BI=interbank_Z_BI,
#     Lo_BI=interbank_Lo_BI,
#     Li_BI=interbank_Li_BI,
#     Bo_BI=interbank_Bo_BI,
#     Bi_BI=interbank_Bi_BI,
#     Shock_BI=interbank_Shock_BI,
#     Shock_BI_def=interbank_Shock_BI_def,
#     Shock_BI_run=interbank_Shock_BI_run,
#     Shock_BI_run_ilq=interbank_Shock_BI_run_ilq,
#     Shock_BI_run_br=interbank_Shock_BI_run_br,
#     Loss_BI=interbank_Loss_BI,
#     Loss_BI_def=interbank_Loss_BI_def,
#     Loss_BI_run=interbank_Loss_BI_run,
#     isExposure=interbank_isExposure,
#     on=interbank_on,
#     off=interbank_off,
#     hel=interbank_hel,
#     isv=interbank_isv,
#     ilq=interbank_ilq,
#     br=interbank_br,
#     cre=interbank_cre,
#     deb=interbank_deb,
#     cre_isv=interbank_cre_isv,
#     deb_isv=interbank_deb_isv,
#     cre_ilq=interbank_cre_ilq,
#     deb_ilq=interbank_deb_ilq,
#     cre_br=interbank_cre_br,
#     deb_br=interbank_deb_br,
# )

