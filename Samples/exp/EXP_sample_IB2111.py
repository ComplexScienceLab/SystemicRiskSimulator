## 主程序示例

# NOTE：推荐运行方式已切换为统一入口：
#   python -m SystemicRiskSimulator --experiment ib2111
# 或：
#   python -m SystemicRiskSimulator --experiment-json Samples/exp_configs/exp_sample_IB2111.json
# 本文件保留作为：1）实验配置示例；2）兼容旧的“直接运行脚本”方式。

from __future__ import annotations

import sys
from pathlib import Path

# 兼容：直接运行该脚本时，把项目根目录加入 sys.path，避免 ModuleNotFoundError。
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from SystemicRiskSimulator.simulator import simulator


def main():
    # %% 配置项
    config = dict()
    config['folderpath_config'] = r"Samples/libraries/configs_library/config_sample_IB2111"  # 配置项文件夹路径
    config['foldername_simulator'] = r"SystemicRiskSimulator"  # 模拟器所在工程文件夹名称
    config['folderpath_realpath_simulator'] = r"."  # 从本实验项目根路径文件夹到模拟器所在工程文件夹之相对路径。
    config['is_auto_confirmation'] = True  # 是否自动确认一些比较危险的操作例如删除、移动、复制文件等。默认 False；

    # %% 运行模拟器
    simulator(config)

    pass  # function


if __name__ == '__main__':
    main()
