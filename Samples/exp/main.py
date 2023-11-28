## 批运行主程序

## 主程序

##########################################
# #状态/测试
##########################################

from SystemicRiskSimulator.simulator import simulator

# %% 设置项
config = {}
config['folderpath_settings_environments'] = r"Samples/settings/environments"
config['foldername_simulator'] = r"SystemicRiskSimulator"
config['folderpath_realpath_simulator'] = r"."

# %% 运行模拟器

simulator(config)
