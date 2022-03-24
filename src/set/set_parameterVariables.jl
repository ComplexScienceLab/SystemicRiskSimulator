"程序：设置参数变量ParameterVariables"

## 程序：设置参数变量ParameterVariables

##########################################
#状态/开发
##########################################



######### 设置参数变量 #########
para.init_method = dict_initMethods[3] # 初始化数据方式
para.Shock_exBI_t = [1631.73, 0.0, 0.0, 0.0, 0.0] # 外生冲击量 #BUG
# para.Shock_exBI_t = [3160.99, 0.0, 0.0, 0.0, 0.0] # 外生冲击量 #BUG
para.idx_Shock_exBI_t = [true,false,false,false,false] # 指定遭受初始外生冲击的银行示性列表
para.kappa_A_P = 0.0 # 银行抛售厂商贷款资产价格折扣率。默认0.0。#HACK目前暂时不考虑这个参数！


###########################



# end; # process

