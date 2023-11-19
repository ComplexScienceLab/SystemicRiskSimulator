## 批运行主程序

## 主程序

##########################################
# #状态/测试
##########################################


# %% 导入相关包
from SystemicRiskSimulator import platform, os, logging, warnings
from SystemicRiskSimulator.core.operations.operator import Operator
from SystemicRiskSimulator.core.define.define_environmentVariables import env
from SystemicRiskSimulator.core.define.define_parameterVariables import para
from SystemicRiskSimulator.tools.tools import Tools

# %% 初始化
## 获取项目路径
env['folderpath_project'] = Tools.get_project_rootpath()

## 生成实验组文件夹用于本批次实验
env = Tools.set_experiments_folders()

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
