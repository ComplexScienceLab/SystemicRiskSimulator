"""
程序：设置环境变量EnvironmentVariables
# Items:  #HACK这个说明已经过时了，有很多新增的变量没有被列入该说明
- init_method:String:
  - "default": 默认，仅初始化；
  - "randomly": 随机生成；
  - "import data": 导入外部数据；
  - "set manually": 手动设置；
- foldernameTypeOfExperimentsData:String: 设置实验数据文件夹命名方式。默认"default"；
  - default: 默认，固定命名方式
  - set manually: 手动设置名称
- foldernamePrefixOfExperimentsData:String: 手动设置实验数据文件夹前缀名。默认"default"；
- root_dir_of_experiments:String: 手动设置实验数据文件夹根路径。默认projectdir() * "/data/sims/"；
- tau:Int16: 回合计数
- process_name:String: 过程名称
- isEndRound:Bool: 结束回合判断
- num_bank:Int16: 银行个数
- num_assets:Int16: 资产总类数
- max_num_of_tau:Int16: 最大回合数
- tau_for_test:Int16: test变量，用于打断点
"""

##########################################
# #状态/开发
# 开发说明：[相关的修改项](file:///../../src/core/define/define_environmentVariables.jl)
##########################################


######### 设置环境变量 #########################################
import os
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum

init_method = "set manually"  # 初始化数据方式；
foldername_type_of_experiments = "set manually"  # 设置实验文件夹命名方式。默认"default"；
foldername_prefix_of_experiments = "test"  # 手动设置实验文件夹前缀名。默认"default"；
root_dir_of_experiments = "data/sims"  # 手动设置实验文件夹根路径。默认"/data/sims/"；
foldername_of_experiments_output_data = "exp_output_data"  # 手动设置实验导出数据文件夹名称。

step_size = 1  # 设置步进跨度；如果该数值设置较大，则相当于直接运行程序；
max_num_of_tau = 100  # 单个过程最大回合数；
num_bank = 5  # 银行个数；
num_assets = 3  # 资产种类数；

tau_for_test = 4  # test变量，用于打断点。相关语句：env['tau']>=env['tau_for_test']；
is_test = True  # 是否处于测试状态

###########################


######### 初始化环境变量（不要改动！） #########################################
folderpath_of_experiments = ""  # 主文件夹路径之于实验。将由函数生成；
foldername_of_experiments = ""  # 实验文件夹名称
folderpath_of_experiments_output_data = ""  # 实验导出数据文件夹名称

data_id = 0  # 实验初始数据帧ID号；
step = 0  # 当前步伐值为0。不要改动
tau = 0  # 初始回合计次为0；
id_experiment = 1  # 当前实验组编号；
num_experiment = 0  # 实验组之实验个数；

state_of_schedule = StateOfScheduleEnum.idle  # 调度运作状态。状态符有以下几种：`:idle`：闲置状态、`:indexing`：索引状态、`:stepping`：步进状态、`:saving`：存储状态、`:loading`：读取状态、`:collecting`：收集数据状态、`:running`：运行状态；
state_of_process = StateOfScheduleEnum.idle  # 程序所处时期状态。状态符有以下几种：`:initializing`：初始化状态、`:running`：运行状态、`:finishing`：结束收尾状态、

is_step = True  # 是否处于步进状态；
is_loop = True  # 是否处于循环状态
is_round = True  # 是否处于回合状态；
is_stage = True  # 是否处于阶段状态；
is_rocess = True  # 是否处于过程状态；
is_model = True  # 是否处于模型状态；
is_experiment = True  # 是否处于当前状态的一次实验；

index_model = 1  # 索引状态下，标记当前所在模型之位置
model_name = ""  # 运行的模型之名称
saved_model_name = ""  # 存储的模型之名称
index_of_schedule_position = []  # 调度位置索引；
index_process = 1  # 索引状态下，标记当前所在过程之位置
process_name = ""  # 运行的过程之名称；
saved_index_process = ""  # 存储的过程之位置；
loadedIndexProcess = ""  # 读取的过程之位置；
index_stage = 1  # 索引状态下，标记当前所在阶段之位置
stage_name = ""  # 运行的阶段之名称；
saved_index_stage = ""  # 存储的当前阶段之位置；
loadedIndexStage = ""  # 读取的当前阶段之位置；

###########################
