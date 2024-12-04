## 主程序示例

from SystemicRiskSimulator.simulator import simulator


def main():
    # %% 配置项
    config = dict()
    config['folderpath_config'] = r"Samples/libraries/configs_library/config_sample_IB1111"  # 配置项文件夹路径
    config['foldername_simulator'] = r"SystemicRiskSimulator"  # 模拟器所在工程文件夹名称
    config['folderpath_realpath_simulator'] = r"."  # 从本实验项目根路径文件夹到模拟器所在工程文件夹之相对路径。
    config['is_auto_confirmation'] = True  # 是否自动确认一些比较危险的操作例如删除、移动、复制文件等。默认 False；

    # %% 运行模拟器
    simulator(config)

    pass  # function


if __name__ == '__main__':
    main()
