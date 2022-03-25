"程序：定义参数变量ParameterVariables"

## 程序：定义参数变量ParameterVariables

##########################################
#状态/停用
##########################################

"参数变量ParameterVariables"
mutable struct ParameterVariables
    model::String # 选择模型
    Shock_exBI_t::TypeMoney{1} # 外生冲击量
    idx_Shock_exBI_t::Vector # 指定遭受初始外生冲击的银行示性列表
    kappa_A_P::Float32 # 银行抛售厂商贷款资产价格折扣率。默认0.0。#HACK目前暂时不考虑这个参数！
    kappa_BI::Float32 # 银行抛售银行间贷款资产价格折扣率。默认0.0。#HACK目前暂时不考虑这个参数！
end


## 初始化
para = ParameterVariables(
    "model_BI1111", # 选择模型
    ZEROS1, # 外生冲击量
    [], # 指定遭受初始外生冲击的银行示性列表
    0.0, # 银行抛售厂商贷款资产价格折扣率。默认0.0。#HACK目前暂时不考虑这个参数！
    0.0 # 银行抛售银行间贷款资产价格折扣率。默认0.0。#HACK目前暂时不考虑这个参数！
)

