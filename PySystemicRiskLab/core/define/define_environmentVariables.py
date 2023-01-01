"程序：定义环境变量EnvironmentVariables"
import os

from PyScripts.settings.set_environment_variables import set_environment_variables
from PySystemicRiskLab.core.define.define_type import EnvironmentVariableType
from PySystemicRiskLab.core.define.define_enum import StateOfScheduleEnum

pass  # end import

# exec("../../scripts/variables/set_environment_variables.py")

# 生成字典变量
env: EnvironmentVariableType = {}

######### 初始化环境变量（不要改动！） #########################################
env['folderpath_of_experiments'] = ""  # 主文件夹路径之于实验。将由函数生成；
env['foldername_of_experiments'] = ""  # 实验文件夹名称
env['folderpath_of_experiments_output_data'] = ""  # 实验导出数据文件夹名称

env['id_data'] = 0  # 实验初始数据帧ID号；
env['step'] = 0  # 当前步伐值为0。不要改动
env['round'] = 0  # 初始回合计次为0；
env['time'] = 0  # 初始时期计次为0；
env['id_experiment'] = 1  # 当前实验组编号；
env['num_experiment'] = 0  # 实验组之实验个数；

env['state_of_schedule'] = StateOfScheduleEnum.idle

env['is_step'] = False  # 是否处于步进状态；
env['is_loop'] = False  # 是否处于循环状态
env['is_round'] = False  # 是否处于回合状态；
env['is_terminalProcess'] = False  # 是否处于终端过程状态；
env['is_process'] = False  # 是否处于过程状态；
env['is_model'] = False  # 是否处于模型状态；
env['is_experiment'] = False  # 是否处于当前状态的一次实验；
env['is_continue_process'] = False  # 是否继续运行过程

env['index_model'] = 1  # 索引状态下，标记当前所在模型之位置
env['model_name'] = ""  # 运行的模型之名称
env['saved_model_name'] = ""  # 存储的模型之名称
env['index_of_schedule_position'] = []  # 调度位置索引；
env['index_process'] = 1  # 索引状态下，标记当前所在过程之位置
env['process_name'] = ""  # 运行的过程之名称；
env['saved_index_process'] = ""  # 存储的过程之位置；
env['loaded_index_process'] = ""  # 读取的过程之位置；
env['index_stage'] = 1  # 索引状态下，标记当前所在阶段之位置
env['stage_name'] = ""  # 运行的阶段之名称；
env['saved_index_stage'] = ""  # 存储的当前阶段之位置；
env['loaded_index_stage'] = ""  # 读取的当前阶段之位置；
env['folderpath_project'] = os.getcwd()  # 获取当前项目路径

## 测试程序专用
env['test_continous_loop_of_model'] = 0  # 计次单个模型连续循环次数

###########################

env.update(set_environment_variables)  # 更新环境变量设置项

if __name__ == "__main__":
    print(env)
    pass
