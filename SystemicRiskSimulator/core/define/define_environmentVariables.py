"""
程序：定义环境变量EnvironmentVariables。

记得这里发生变更时，要手动检查`Operator.operate_experiment`相关位置是否要更新。
"""
from SystemicRiskSimulator import Path
from SystemicRiskSimulator.core.define.define_type import EnvironmentVariableType
from SystemicRiskSimulator.core.define.define_enum import StateOfScheduleEnum
from SystemicRiskSimulator.tools.tools import Tools
from SystemicRiskSimulator.settings.environments.set_environments_variables import set_environments_variables

pass  # end import

# 生成字典变量
env: EnvironmentVariableType = {}

######### 定义以下环境变量（不要改动！） #########################################
env['folderpath_of_experiments'] = ""  # 主文件夹路径之于实验。将由函数生成；
env['foldername_of_experiments'] = ""  # 实验文件夹名称
env['folderpath_of_experiments_output_data'] = ""  # 实验导出数据文件夹名称

env['id_data'] = 0  # 实验初始数据帧ID号；
env['round'] = 0  # 初始轮次计次为0；
env['phase'] = 0  # 当前逐相为0。不要改动
env['step'] = 0  # 单次实验的当前步进为0。不要改动
env['time'] = 0  # 初始时期计次为0；#TODO 似乎没有用到
env['id_experiment'] = 1  # 当前实验组编号；
env['num_experiment'] = 0  # 实验组之实验个数；

env['state_of_schedule'] = StateOfScheduleEnum.idle

env['is_continue_round'] = False  # 是否处于回合状态；
env['is_continue_process'] = False  # 是否继续运行过程

env['A_data'] = None  # 多主体数据

env['model_name'] = ""  # 运行的模型之名称
env['process_name'] = ""  # 运行的过程之名称；
env['folderpath_project'] = Path.cwd()  # 当前项目路径；
env['folderpath_import_modules'] = ""  # 当前需要导入的模块所在总路径；

env['df_BB'] = None  # Pandas格式的银行数据
env['df_IB'] = None  # Pandas格式的银行间数据

# """
# env['model_process_state'] 表示当前模型根节点处理状态 #HACK 无用，但是可以保留作为借鉴
# 如果用可视化标记节点颜色表示标记状态，那么：
#
# - 标记是白色`"has not process"`说明还没处理过该节点，也没有在处理；
# - 标记是绿色`"process now"`说明正在处理该节点；
# - 标记是黄色`"process inner"`说明正在处理该节点之内层节点；
# - 标记是红色`"has processed"`说明已经处理完该节点，但是表示接下来不会再准备处理该节点；
# """
# env['model_process_state'] = "has not process"

## 测试程序专用
env['test_continous_loop_of_model'] = 0  # 计次单个模型连续循环次数
env['test_max_num_of_round'] = None,  # 处理最大回合数（测试用）；

###########################

env.update(set_environments_variables)  # 更新环境变量设置项

if __name__ == "__main__":
    print(env)
    pass
