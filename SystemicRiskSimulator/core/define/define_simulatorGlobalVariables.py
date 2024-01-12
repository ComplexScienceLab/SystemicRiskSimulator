"""
程序：定义模拟器全局变量 SimulatorGlobalVariables。

记得这里发生变更时，要手动检查`Operator.operate_experiment`相关位置是否要更新。
"""
from SystemicRiskSimulator.external_packages import Path
from SystemicRiskSimulator.core.define.define_type import SimulatorGlobalVariableType
from SystemicRiskSimulator.core.define.define_enum import StateOfScheduleEnum
from SystemicRiskSimulator.data.config.set_config_variables import set_config_variables

pass  # end import

# 生成字典变量
sgv: SimulatorGlobalVariableType = dict()

######### 定义以下项目内的全局变量（不要改动！） ######################################### #TODO 需要整理
sgv['folderpath_experiments'] = ""  # 主文件夹路径之于实验。将由函数生成；
sgv['foldername_experiments'] = ""  # 实验文件夹名称
sgv['folderpath_experiments_output_data'] = ""  # 实验导出数据文件夹名称

sgv['is_datetime'] = True,  # 是否使用日期时间作为实验文件夹名称的一部分。默认 True；

sgv['need_visualization'] = False  # 是否需要可视化
sgv['is_installed_packages_for_visualization'] = False  # 是否已经安装了可视化所需的第三方工具包
sgv['visualization_packages'] = ['matplotlib', 'igraph', 'drawsvg', 'fitz', 'pymupdf', 'svglib', 'screeninfo', 'openpyxl', 'xlwings']  # 可视化所需的第三方工具包 #NOTE 如果需要添加新的包，请在此处添加

sgv['id_data'] = 0  # 实验初始数据帧ID号；
sgv['round'] = 0  # 初始轮次计次为0；
sgv['phase'] = 0  # 当前逐相为0。不要改动
sgv['step'] = 0  # 单次实验的当前步进为0。不要改动
sgv['time'] = 0  # 初始时期计次为0；#TODO 似乎没有用到
sgv['id_experiment'] = 1  # 当前实验组编号；
sgv['num_experiment'] = 0  # 实验组之实验个数；

sgv['state_of_schedule'] = StateOfScheduleEnum.idle

sgv['is_continue_round'] = False  # 是否处于回合状态；
sgv['is_continue_process'] = False  # 是否继续运行过程

sgv['A_data'] = None  # 多主体数据

sgv['model_name'] = ""  # 运行的模型之名称
sgv['process_name'] = ""  # 运行的过程之名称；
sgv['folderpath_project'] = Path.cwd()  # 当前项目路径；
sgv['folderpath_import_modules'] = ""  # 当前需要导入的模块所在总路径；

sgv['vis'] = dict(),  # 可视化相关的宏观变量

sgv['df_BB'] = None  # Pandas格式的银行数据
sgv['df_IB'] = None  # Pandas格式的银行间数据

## 测试程序专用
sgv['test_continous_loop_of_model'] = 0  # 计次单个模型连续循环次数
sgv['test_max_num_of_round'] = None,  # 处理最大回合数（测试用）；

###########################

## 更新模拟器全局变量。遍历 `set_config_variables` 里的字典键值对，然后合并入 `sgv` 里对应的键值对。如果键值对已经存在，那么就覆盖。如果键值对不存在，那么就新增。
for key, value in set_config_variables.items():
    sgv[key] = value
