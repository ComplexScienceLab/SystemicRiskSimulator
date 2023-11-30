"程序：设置参数变量parameter_variables"



from SystemicRiskSimulator.external_packages import np
pass  # end import

set_parameters_variables = dict(

    ######### 设置参数变量 #########################################

    ## 指定待处理的模型
    model_name=[
        'IB1111_流程版',
    ],

    ## 外生违约损失冲击权重百分比
    Shock_exIB_def_t_percentage=[
        np.array([1.0, 0.0, 0.0, 0.0, 0.0]),
        np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    ],

    ## 外生挤兑流动冲击权重百分比
    Shock_exIB_run_t_percentage=[
        np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
        np.array([1.0, 0.0, 0.0, 0.0, 0.0]),
    ],

    ## 银行抛售厂商贷款资产价格折扣率。默认0.0。#HACK目前暂时不考虑这个参数！
    kappa_A_P=[
        0.0
    ],

    ## 银行抛售银行间贷款资产价格折扣率。默认0.0。#HACK目前暂时不考虑这个参数！
    kappa_IB=[
        0.0
    ],

    ################################################################

)
