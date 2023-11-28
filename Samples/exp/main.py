## 批运行主程序

## 主程序

##########################################
# #状态/测试
##########################################

# %% 设置项
folderpaths = {}
folderpaths['folderpath_settings_environments'] = r"Samples/settings/environments"
# folderpaths['folderpath_settings_parameters'] = r"Samples/settings/parameters"
# folderpaths['folderpath_settings_agents'] = r"Samples/settings/agents"
folderpaths['foldername_simulator'] = r"SystemicRiskSimulator"
folderpaths['folderpath_realpath_simulator'] = r"."

# %% 导入相关包
from SystemicRiskSimulator import platform, logging, warnings, os, Path
from SystemicRiskSimulator.tools.tools import Tools

## 获取项目路径、模拟器工具路径
folderpaths['folderpath_simulator'] = Tools.get_project_rootpath(folderpaths['foldername_simulator'], folderpaths['folderpath_realpath_simulator'])
folderpaths['folderpath_project'] = Tools.get_project_rootpath()

# 如果 settings 之 enviroments 有内容，那么就删除，否则就从其他文件夹中复制之后再导入
Tools._delete_and_recreate_folder(Path(folderpaths['folderpath_simulator'], "SystemicRiskSimulator/data/settings/environments"), is_auto_confirmation=False)
Tools._copy_files_from_other_folders(Path(folderpaths['folderpath_project'], folderpaths['folderpath_settings_environments']), Path(folderpaths['folderpath_simulator'], "SystemicRiskSimulator/data/settings/environments"), is_auto_confirmation=False)
from SystemicRiskSimulator.core.define.define_environmentVariables import env

## 生成实验组文件夹用于本批次实验
(
    env['foldername_of_experiments'],
    env['folderpath_project'],
    env['folderpath_simulator'],
    env['folderpath_of_experiments'],
    env['folderpath_of_experiments_output_data'],
    env['folderpath_models'],
    env['folderpath_settings_environments'],
    env['folderpath_settings_parameters'],
    env['folderpath_settings_agents'],
) = Tools.set_experiments_folders(
    foldername_prefix_of_experiments=env['foldername_prefix_of_experiments'],
    foldername_of_experiments_output_data=env['foldername_of_experiments_output_data'],
    str_folderpath_root_dir_of_experiments=env['folderpath_root_dir_of_experiments'],
    str_foldername_simulator=folderpaths['foldername_simulator'],
    str_folderpath_realpath_simulator=folderpaths['folderpath_realpath_simulator'],
    str_folderpath_models=env['folderpath_models'],
    str_folderpath_settings_environments=env['folderpath_settings_environments'],
    str_folderpath_settings_parameters=env['folderpath_settings_parameters'],
    str_folderpath_settings_agents=env['folderpath_settings_agents'],
    type_of_experiments_foldername=env['type_of_experiments_foldername'],
    is_datetime=True,
)

Tools._delete_and_recreate_folder(Path(env['folderpath_simulator'], "SystemicRiskSimulator/data/settings/parameters"), is_auto_confirmation=False)
Tools._copy_files_from_other_folders(env['folderpath_settings_parameters'], Path(env['folderpath_simulator'], "SystemicRiskSimulator/data/settings/parameters"), is_auto_confirmation=False)
from SystemicRiskSimulator.core.define.define_parameterVariables import para

Tools._delete_and_recreate_folder(Path(env['folderpath_simulator'], "SystemicRiskSimulator/data/settings/agents"), is_auto_confirmation=False)
Tools._copy_files_from_other_folders(env['folderpath_settings_agents'], Path(env['folderpath_simulator'], "SystemicRiskSimulator/data/settings/agents"), is_auto_confirmation=False)
# from SystemicRiskSimulator.core.define.define_agentVariables import agent

from SystemicRiskSimulator.core.operations.operator import Operator

# from SystemicRiskSimulator.core.define.define_environmentVariables import env
# from SystemicRiskSimulator.core.define.define_parameterVariables import para

# %% 初始化
# ## 获取项目路径
# env['folderpath_project'] = Tools._get_current_project_rootpath()


## 设置日志
logger = logging.getLogger()
logger.setLevel(env['test_logging'])
log_file_handler = logging.FileHandler(os.path.join(env['folderpath_of_experiments_output_data'], "outputlog.txt"))
logger.addHandler(log_file_handler)
log_console_handler = logging.StreamHandler()
logger.addHandler(log_console_handler)

logging.debug("\n实验组名称：%s", env['foldername_of_experiments'])

# %% 预安装模型、数据
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

## 删除设置文件夹、模型文件夹内的所有文件，但是保留文件夹
Tools._delete_and_recreate_folder(Path(env['folderpath_simulator'], "SystemicRiskSimulator/data/settings/environments"), is_auto_confirmation=False)
Tools._delete_and_recreate_folder(Path(env['folderpath_simulator'], "SystemicRiskSimulator/data/settings/parameters"), is_auto_confirmation=False)
Tools._delete_and_recreate_folder(Path(env['folderpath_simulator'], "SystemicRiskSimulator/data/settings/agents"), is_auto_confirmation=False)
Tools._delete_and_recreate_folder(Path(env['folderpath_simulator'], "SystemicRiskSimulator/data/models"), is_auto_confirmation=False)

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
