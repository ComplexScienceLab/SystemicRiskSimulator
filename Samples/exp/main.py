## 主程序

##########################################
# #状态/测试
##########################################

from SystemicRiskSimulator.simulator import simulator

# %% 配置项
config = {}
config['folderpath_config'] = r"Samples/libraries/configs_library/config_010"  # 配置项文件夹路径
config['foldername_simulator'] = r"SystemicRiskSimulator"  # 模拟器所在工程文件夹名称
config['folderpath_realpath_simulator'] = r"../"  # 模拟器所在工程文件夹相对本实验项目文件夹之相对路径

# %% 运行模拟器
simulator(config)
