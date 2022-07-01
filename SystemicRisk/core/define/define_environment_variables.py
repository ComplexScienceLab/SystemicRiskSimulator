"程序：定义环境变量EnvironmentVariables"

## 程序：定义环境变量EnvironmentVariables

##########################################
# 状态/使用
# 备注：改成用字典表示
##########################################

from scripts.variables.set_environmentVariables import *

# exec()

## 生成字典变量 #HACK 如何实现自动生成字典变量？
environmentVariables = dict(
    init_method=init_method,
    foldername_type_of_experiments=foldername_type_of_experiments,
    foldername_prefix_of_experiments=foldername_prefix_of_experiments,
    root_dir_of_experiments=root_dir_of_experiments,
    folderpath_of_experiments=folderpath_of_experiments,
    step_size=step_size,
    max_num_of_tau=max_num_of_tau,
    num_bank=num_bank,
    num_assets=num_assets,
    tau_for_test=tau_for_test,
    is_test=is_test,
    foldername_of_experiments=foldername_of_experiments,
    foldername_of_experiments_output_data=foldername_of_experiments_output_data,
    folderpath_of_experiments_output_data=folderpath_of_experiments_output_data,
    data_id=data_id,
    step=step,
    tau=tau,
    id_experiment=id_experiment,
    num_experiment=num_experiment,
    state_of_schedule=state_of_schedule,
    state_of_process=state_of_process,
    is_step=is_step,
    is_loop=is_loop,
    is_round=is_round,
    is_stage=is_stage,
    is_rocess=is_rocess,
    is_model=is_model,
    is_experiment=is_experiment,
    index_of_schedule_position=index_of_schedule_position,
    index_model=index_model,
    model_name=model_name,
    saved_model_name=saved_model_name,
    index_process=index_process,
    process_name=process_name,
    saved_index_process=saved_index_process,
    index_stage=index_stage,
    stage_name=stage_name,
    saved_index_stage=saved_index_stage,
)

env = environmentVariables  # 别名
