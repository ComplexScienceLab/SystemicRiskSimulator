"程序：设置参数变量数据记录 parameter_variables"

from SystemicRiskSimulator.external_packages import np, pd, pickle

pass  # end import
set_parameters_variables = dict(

    ######### 设置参数变量 #########################################

    ## 指定待处理的模型
    model_name=[
        'IB1111_非流程多函数版',
    ],

    ## 外生违约损失冲击权重百分比
    Shock_exIB_def_t_percentage=[
        np.zeros(5, dtype=float),
    ],

    ## 外生挤兑流动冲击权重百分比
    Shock_exIB_run_t_percentage=[
        np.zeros(5, dtype=float),
    ],

    # ## 银行抛售厂商贷款资产价格折扣率。默认0.0。#HACK目前暂时不考虑这个参数！
    # kappa_A_P=[
    #     0.0
    # ],
    #
    # ## 银行抛售银行间贷款资产价格折扣率。默认0.0。#HACK目前暂时不考虑这个参数！
    # kappa_IB=[
    #     0.0
    # ],

    ################################################################

)

## 添加实验组

# 添加实验组：各银行没有遭受任何冲击
df_parameters = pd.DataFrame(set_parameters_variables)

array_eye = np.eye(5, dtype=float)
array_step = np.arange(0.1, 1.0 + 0.1, 0.1)

# 添加实验组：各银行单独遭受全部的外生违约损失冲击
for i in range(5):
    df_parameters.loc[len(df_parameters)] = dict(
        model_name='IB1111_非流程多函数版',
        Shock_exIB_def_t_percentage=array_eye[i],
        Shock_exIB_run_t_percentage=np.zeros(5, dtype=float),
    )

# 添加实验组：各银行单独遭受全部的外生挤兑流动冲击
for i in range(5):
    df_parameters.loc[len(df_parameters)] = dict(
        model_name='IB1111_非流程多函数版',
        Shock_exIB_def_t_percentage=np.zeros(5, dtype=float),
        Shock_exIB_run_t_percentage=array_eye[i],
    )

# 添加实验组：各银行单独遭受全部的外生违约损失冲击与外生挤兑流动冲击
for i in range(5):
    df_parameters.loc[len(df_parameters)] = dict(
        model_name='IB1111_非流程多函数版',
        Shock_exIB_def_t_percentage=array_eye[i],
        Shock_exIB_run_t_percentage=array_eye[i],
    )

# 添加实验组：各银行同时遭受按比例递增的外生违约损失冲击
for v in array_step:
    df_parameters.loc[len(df_parameters)] = dict(
        model_name='IB1111_非流程多函数版',
        Shock_exIB_def_t_percentage=np.ones(5, dtype=float) * v,
        Shock_exIB_run_t_percentage=np.zeros(5, dtype=float),
    )

# 添加实验组：各银行同时遭受按比例递增的外生挤兑流动冲击
for v in array_step:
    df_parameters.loc[len(df_parameters)] = dict(
        model_name='IB1111_非流程多函数版',
        Shock_exIB_def_t_percentage=np.zeros(5, dtype=float),
        Shock_exIB_run_t_percentage=np.ones(5, dtype=float) * v,
    )

# 添加实验组：各银行同时遭受按比例递增的外生违约损失冲击与外生挤兑流动冲击
for v in array_step:
    df_parameters.loc[len(df_parameters)] = dict(
        model_name='IB1111_非流程多函数版',
        Shock_exIB_def_t_percentage=np.ones(5, dtype=float) * v,
        Shock_exIB_run_t_percentage=np.ones(5, dtype=float) * v,
    )

## 转换为字典列表格式，然后导出到当前文件夹下
parameters = df_parameters.to_dict('records')
with open("./parameters.pkl", 'wb') as f:
    pickle.dump(parameters, f)
