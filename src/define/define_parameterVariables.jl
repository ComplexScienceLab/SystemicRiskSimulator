"程序：定义参数变量ParameterVariables"

## 程序：定义参数变量ParameterVariables

##########################################
#状态/开发
##########################################

"参数变量ParameterVariables"
mutable struct ParameterVariables
    init_method::String # 初始化方法
    Shock_exBI_t::TypeMoney{1} # 外生冲击量
    idx_Shock_exBI_t::Vector # 指定遭受初始外生冲击的银行示性列表
    kappa_A_P::Float32 # 银行抛售厂商贷款资产价格折扣率。默认0.0。
end

dict_initMethods = Dict([(0, "only init"), (1, "randomly"), (2, "import data"), (3, "set manually")]) # 字典之于初始化数据方式

## 初始化
para = ParameterVariables(
    dict_initMethods[1], # 初始化方法
    ZEROS1, # 外生冲击量
    [], # 指定遭受初始外生冲击的银行示性列表
    0.0 # 银行抛售厂商贷款资产价格折扣率。默认0.0。
)