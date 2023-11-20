## 批运行主程序

## 主程序

##########################################
# #状态/测试
##########################################


# %% 导入相关包
from SystemicRiskSimulator import platform, Path, logging, warnings, os
from SystemicRiskSimulator.tools.tools import Tools

folderpaths = {}
folderpaths['folderpath_settings_environments'] = r"Samples/settings/environments"
folderpaths['folderpath_settings_parameters'] = r"Samples/settings/parameters"
folderpaths['folderpath_settings_agents'] = r"Samples/settings/agents"

# from Samples.settings.set_environments_variables import set_environments_variables
# 如果 settings 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
Tools._delete_and_recreate_folder("SystemicRiskSimulator/settings/environments", is_auto_confirmation=True)
Tools.copy_files_from_other_folders(folderpaths['folderpath_settings_environments'], "SystemicRiskSimulator/settings/environments")
from SystemicRiskSimulator.core.define.define_environmentVariables import env

Tools._delete_and_recreate_folder("SystemicRiskSimulator/settings/parameters", is_auto_confirmation=True)
Tools.copy_files_from_other_folders(folderpaths['folderpath_settings_parameters'], "SystemicRiskSimulator/settings/parameters")
from SystemicRiskSimulator.core.define.define_parameterVariables import para

Tools._delete_and_recreate_folder("SystemicRiskSimulator/settings/agents", is_auto_confirmation=True)
Tools.copy_files_from_other_folders(folderpaths['folderpath_settings_agents'], "SystemicRiskSimulator/settings/agents")
# from SystemicRiskSimulator.core.define.define_agentVariables import agent

from SystemicRiskSimulator.core.operations.operator import Operator

# from SystemicRiskSimulator.core.define.define_environmentVariables import env
# from SystemicRiskSimulator.core.define.define_parameterVariables import para

# %% 初始化
## 获取项目路径
env['folderpath_project'] = Tools.get_project_rootpath()

## 生成实验组文件夹用于本批次实验
env['foldername_of_experiments'], env['folderpath_of_experiments'], env['folderpath_of_experiments_output_data'] = Tools.set_experiments_folders(env['folderpath_project'], env['root_dir_of_experiments'], env['foldername_of_experiments_output_data'], env['foldername_prefix_of_experiments'], env['type_of_experiments_foldername'], is_datetime=True)

## 设置日志
logger = logging.getLogger()
logger.setLevel(env['test_logging'])
log_file_handler = logging.FileHandler(os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"))
logger.addHandler(log_file_handler)
log_console_handler = logging.StreamHandler()
logger.addHandler(log_console_handler)

logging.debug("\n实验组名称：%s", env['foldername_of_experiments'])

# %% 预安装模型，包括算法和数据
warnings.filterwarnings("ignore")

## 初始化、构建、安装模型
env, models = Operator.operate_installing(env, para)

## 运行实验组
logging.debug("\n\n\n实验组开始：\n\n")
for (i, para) in enumerate(env['list_combination_of_para']):
    model = models[f"model_{para['model_name']}"]  # 获取当前实验对应的模型
    env['id_experiment'] = i + 1  # 设定当前实验编号

    ## 进行实验
    Operator.operate_experiment(env, para, model)

    pass  # for
logging.info("实验组结束。")

## 默认程序打开输出文件查看
system = platform.system()
if system == 'Darwin':
    os.system(r"open " + os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"))
elif system == 'Windows':
    os.startfile(os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"))
elif system == 'Linux':
    os.system('xdg-open ' + os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"))
else:
    print("Unsupported operating system")
    pass  # if
