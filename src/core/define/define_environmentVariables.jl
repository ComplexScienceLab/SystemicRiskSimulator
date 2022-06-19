

"程序：定义环境变量EnvironmentVariables"

## 程序：定义环境变量EnvironmentVariables

##########################################
#状态/使用
# 备注：改成用字典表示
##########################################


## 生成字典变量 #HACK 如何实现自动生成字典变量？
env = @dict(
  init_method,
  foldername_type_of_experiments,
  foldername_prefix_of_experiments,
  root_dir_of_experiments,
  folderpath_of_experiments,
  step_size,
  max_num_of_tau,
  num_bank,
  num_assets,
  tau_for_test,
  is_test,
  foldername_of_experiments,
  foldername_of_experiments_output_data,
  folderpath_of_experiments_output_data,
  data_id,
  step,
  tau,
  id_experiment,
  num_experiment,
  state_of_schedule,
  state_of_process,
  is_step,
  is_loop,
  is_round,
  is_stage,
  is_process,
  is_model,
  is_experiment,
  index_of_schedule_position,
  index_model,
  model_name,
  saved_model_name,
  index_process,
  process_name,
  saved_index_process,
  index_stage,
  stage_name,
  saved_index_stage,
)

# env = environmentVariables # 别名
