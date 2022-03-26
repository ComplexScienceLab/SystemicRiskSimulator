

"程序：定义环境变量EnvironmentVariables"

## 程序：定义环境变量EnvironmentVariables

##########################################
#状态/使用
# 备注：改成用字典表示
##########################################


## 生成字典变量
environmentVariables = @dict(
  init_method,
  foldernameTypeOfExperimentsData,
  foldernamePrefixOfExperimentsData,
  rootDirOfExperimentsData,
  folderpathOfExperimentsData,
  tau,
  process_name,
  is_end_round,
  max_num_tau,
  num_bank,
  num_assets,
  test_tau
)

## 别名
env = environmentVariables
