"""SystemicRiskSimulator 统一入口（单文件调度）。

本文件合并了以下职责：
- CLI 入口（原 `__main__.py`）
- JSON 配置装载与覆盖项解析（原 `config_loader.py`）
- 模拟器运行入口函数 `simulator(config)`（原 `simulator.py`）

目标：减少文件数量，便于研究迭代。

运行方式（Windows/PowerShell 示例）：

1）全局 config.json 选择实验：

    python -m SystemicRiskSimulator --global-config config.json --experiment ib2111

2）直接指定实验 JSON：

    python -m SystemicRiskSimulator --experiment-json Samples/exp_configs/exp_sample_IB2111.json

3）兼容旧方式（直接指定 set_config_variables.py 文件夹）：

    python -m SystemicRiskSimulator --set-config-folder Samples/libraries/configs_library/config_sample_IB2111

说明：
- 实验快照（config/agents/parameters/models 等）仍按原逻辑复制到输出目录。
- 运行时是否复制到模拟器包内固定 data 目录由 `runtime_copy_resources_into_simulator_data` 控制。

"""

from __future__ import annotations

# 在模块导入早期确保项目根路径在 sys.path 中，方便直接运行 main.py（IDE 的 Run 按钮）
import sys
from pathlib import Path
try:
    _THIS_FILE = Path(__file__).resolve()
    # main.py 在路径 .../SystemicRiskSimulator/SystemicRiskSimulator/main.py
    # 项目根目录是 parents[2]
    _PROJECT_ROOT_GUESS = _THIS_FILE.parents[2]
    if str(_PROJECT_ROOT_GUESS) not in sys.path:
        sys.path.insert(0, str(_PROJECT_ROOT_GUESS))
except Exception:
    # 保守降级：不抛异常
    pass

# ----------------------------
# JSON 配置装载（原 config_loader.py）
# ----------------------------

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional


def parse_overrides(pairs: Optional[Iterable[str]]) -> Dict[str, Any]:
    """解析 CLI 传入的 key=value 覆盖项。"""
    if not pairs:
        return {}

    overrides: Dict[str, Any] = {}
    for item in pairs:
        if "=" not in item:
            raise ValueError(f"override 参数必须是 key=value 形式，收到：{item!r}")
        key, value_raw = item.split("=", 1)
        key = key.strip()
        value_raw = value_raw.strip()
        if not key:
            raise ValueError(f"override key 不能为空：{item!r}")

        lower = value_raw.lower()
        if lower in {"true", "false"}:
            value: Any = lower == "true"
        else:
            try:
                value = int(value_raw)
            except ValueError:
                try:
                    value = float(value_raw)
                except ValueError:
                    if (value_raw.startswith("{") and value_raw.endswith("}")) or (
                        value_raw.startswith("[") and value_raw.endswith("]")
                    ):
                        try:
                            value = json.loads(value_raw)
                        except Exception:
                            value = value_raw
                    else:
                        value = value_raw

        overrides[key] = value

    return overrides


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在：{path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_experiment_from_global(global_cfg: Mapping[str, Any], experiment: str) -> Dict[str, Any]:
    """从全局配置里取出某个实验配置。"""
    experiments = global_cfg.get("experiments")
    if not isinstance(experiments, Mapping):
        raise ValueError("global config 缺少 `experiments` 字段，或类型不是对象。")

    if experiment not in experiments:
        raise KeyError(f"全局配置中未找到 experiment={experiment!r}。可选值：{list(experiments.keys())}")

    exp_cfg = experiments[experiment]
    if not isinstance(exp_cfg, Mapping):
        raise ValueError(f"experiments[{experiment!r}] 必须是对象。")

    return dict(exp_cfg)


def build_simulator_config(
    *,
    project_root: Path,
    runner_cfg: Optional[Mapping[str, Any]] = None,
    experiment_cfg: Optional[Mapping[str, Any]] = None,
    overrides: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """合成最终传给 `simulator(config)` 的 config 字典。

    合并优先级（后者覆盖前者）：
    - experiment_cfg
    - runner_cfg
    - overrides

    必需字段：
    - folderpath_config

    NOTE：这里不读取 set_config_variables.py（仍由 simulator() 完成），
    只负责组织选择逻辑与覆盖项。
    """

    cfg: Dict[str, Any] = {}
    if experiment_cfg:
        cfg.update(dict(experiment_cfg))
    if runner_cfg:
        cfg.update(dict(runner_cfg))
    if overrides:
        cfg.update(dict(overrides))

    cfg.setdefault("foldername_simulator", "SystemicRiskSimulator")
    cfg.setdefault("folderpath_realpath_simulator", ".")

    if "folderpath_config" not in cfg:
        raise ValueError("最终 config 缺少必需字段 `folderpath_config`。")

    return cfg


# ----------------------------
# 模拟器入口（原 simulator.py）
# ----------------------------


def simulator(config: dict):
    """系统性风险模拟器。"""

    import sys
    import platform
    import logging
    from pathlib import Path
    import shutil
    import datetime
    import time
    import subprocess
    import importlib
    import pickle
    import base64

    from SystemicRiskSimulator.tools.tools import Tools
    from SystemicRiskSimulator.core.operations.collector import Collector

    # %% 初始化
    config["folderpath_project"] = Tools.get_project_rootpath()
    config["folderpath_simulator"] = Tools.get_project_rootpath(
        config["foldername_simulator"], config["folderpath_realpath_simulator"]
    )

    from SystemicRiskSimulator.core.define.define_simulatorGlobalVariables import sgv

    # 如果实验配置中指定了外部依赖路径（external_paths），优先把这些路径加入 sys.path
    # 这样可以让模型或算法中依赖外部库（例如 ComplexSystemLab）的导入在运行时可用。
    external_paths = config.get("external_paths")
    if external_paths:
        import sys as _sys

        for _p in external_paths:
            try:
                _pp = str(Path(_p).resolve())
            except Exception:
                _pp = str(Path(config["folderpath_project"]) / _p)
                _pp = str(Path(_pp).resolve())
            if _pp not in _sys.path:
                _sys.path.insert(0, _pp)

    sgv.update(
        (
            Tools.import_modules_from_package(
                str(Path(config["folderpath_project"], config["folderpath_config"])),
                r"set_config_variables",
                config["folderpath_project"],
            )
        )["set_config_variables"]
    )
    sgv.update(config)

    config.update(sgv)

    # 设置实验文件夹
    if sgv["schedule_operation"]["实验组模拟程序"] is True:
        sgv["foldername_experiments"] = Tools.set_foldername_experiments(
            sgv["foldername_prefix_experiments"],
            sgv["foldername_set_manually"],
            sgv["is_datetime"],
            sgv["type_of_experiments_foldername"],
        )

    (
        sgv["folderpath_project"],
        sgv["folderpath_simulator"],
        sgv["folderpath_experiments"],
        sgv["folderpath_experiments_output_data"],
        sgv["folderpath_experiments_output_log"],
        sgv["folderpath_experiments_output_config"],
        sgv["folderpath_experiments_output_parameters"],
        sgv["folderpath_experiments_output_agents"],
        sgv["folderpath_experiments_output_models"],
        sgv["folderpath_models"],
        sgv["folderpath_config"],
        sgv["folderpath_parameters"],
        sgv["folderpath_agents"],
    ) = Tools.set_experiments_folders(
        foldername_experiments_output_data=sgv["foldername_experiments_output_data"],
        foldername_experiments=sgv["foldername_experiments"],
        str_folderpath_root_experiments=sgv["folderpath_root_experiments"],
        str_foldername_simulator=sgv["foldername_simulator"],
        str_folderpath_realpath_simulator=sgv["folderpath_realpath_simulator"],
        str_foldername_outputData=sgv["foldername_outputData"],
        str_folderpath_realpath_outputData=sgv["folderpath_realpath_outputData"],
        str_folderpath_models=sgv["folderpath_models"],
        str_folderpath_config=sgv["folderpath_config"],
        str_folderpath_parameters=sgv["folderpath_parameters"],
        str_folderpath_agents=sgv["folderpath_agents"],
    )

    # 设定实验组运行方式（统一键名）
    if sgv["is_use_Gym_environments"] is False and sgv["is_use_RL_method"] is False:
        logging.debug(
            "\nexperiments_program.py : 只使用模拟器自带的模型，不使用强化学习环境工具包自定义的模型。\n"
        )
        sgv["运行实验组的方式"] = "运行ABM实验组"
    elif (
        sgv["is_use_Gym_environments"] is False
        and sgv["is_use_RL_method"] is True
        and sgv["RL_state"] == "using"
    ):
        logging.debug(
            "\nexperiments_program.py : 使用自定义的环境模型，并且使用强化学习算法对已经训练过的模型做运用。\n"
        )
        sgv["运行实验组的方式"] = "运行强化学习算法和ABM模型实验组做应用"
    elif (
        sgv["is_use_Gym_environments"] is False
        and sgv["is_use_RL_method"] is True
        and sgv["RL_state"] == "training"
    ):
        logging.debug(
            "\nexperiments_program.py : 使用自定义的环境模型，并且使用强化学习算法做训练。\n"
        )
        sgv["运行实验组的方式"] = "运行强化学习算法和ABM模型实验组做训练"
    elif sgv["is_use_Gym_environments"] is True and sgv["is_use_RL_method"] is False:
        logging.debug(
            "\nexperiments_program.py : 使用 Gymnasium 环境框架结合自定义的环境模型，但是没有用强化学习算法进行训练。\n"
        )
        sgv["运行实验组的方式"] = "运行Gym和ABM实验组"
    elif (
        sgv["is_use_Gym_environments"] is True
        and sgv["is_use_RL_method"] is True
        and sgv["RL_state"] == "using"
    ):
        logging.debug(
            "\nexperiments_program.py : 使用 Gymnasium 环境框架结合自定义的环境模型，并且使用强化学习算法已经训练过的模型做运用。\n"
        )
        sgv["运行实验组的方式"] = "运行强化学习算法和Gym框架结合自定义ABM模型实验组做应用"
    elif (
        sgv["is_use_Gym_environments"] is True
        and sgv["is_use_RL_method"] is True
        and sgv["RL_state"] == "training"
    ):
        logging.debug(
            "\nexperiments_program.py : 使用 Gymnasium 环境框架结合自定义的环境模型，并且使用强化学习算法做训练。\n"
        )
        sgv["运行实验组的方式"] = "运行强化学习算法和Gym框架结合自定义ABM模型实验组做训练"

    if sgv["运行实验组的方式"] == "运行强化学习算法和ABM模型实验组做训练":
        sgv["subfoldername_experiments_output_data"] = "RL_training"
    elif sgv["运行实验组的方式"] == "运行强化学习算法和ABM模型实验组做应用":
        sgv["subfoldername_experiments_output_data"] = "RL_using"
    elif sgv["运行实验组的方式"] == "运行ABM实验组":
        sgv["exp_id_exp_output_data"] = ""
        sgv["subfoldername_experiments_output_data"] = "normal"
    else:
        raise ValueError(f"运行实验组的方式 {sgv['运行实验组的方式']} 不支持！")

    # 平台信息在后处理（可视化）中也会被使用；即使不跑实验主程序也要提前设置
    sgv["system_platform"] = platform.system()

    def _run_stage_program(*, stage_name: str, script_name: str, module_name: str):
        """按当前模式（开发/子进程）运行指定阶段程序。"""
        stage_start_time = time.time()
        if not sgv["is_develope_mode"]:
            sgv_pkl = pickle.dumps(sgv)
            sgv_base64 = base64.b64encode(sgv_pkl).decode("utf-8")
            subprocess.run(
                [
                    sys.executable,
                    str(
                        Path(
                            sgv["folderpath_simulator"],
                            f"SystemicRiskSimulator/programs/{script_name}",
                        )
                    ),
                    sgv_base64,
                ]
            )
        else:
            program_module = importlib.import_module(module_name)
            program_module.main(sgv)

        logging.info(f"\n{stage_name}运行时长：{time.time() - stage_start_time} 秒。\n")

    # 是否运行实验组
    if sgv["schedule_operation"]["实验组模拟程序"]:
        # 快照：config
        Tools.delete_and_recreate_folder(
            sgv["folderpath_experiments_output_config"],
            is_auto_confirmation=sgv["is_auto_confirmation"],
        )
        shutil.copyfile(
            sgv["folderpath_config"] / "set_config_variables.py",
            sgv["folderpath_experiments_output_config"] / "set_config_variables.py",
        )

        # 可选：复制到 simulator/data
        if sgv.get("runtime_copy_resources_into_simulator_data", False):
            Tools.delete_and_recreate_folder(
                Path(sgv["folderpath_simulator"], "SystemicRiskSimulator/data/config"),
                is_auto_confirmation=sgv["is_auto_confirmation"],
            )
            shutil.copyfile(
                sgv["folderpath_config"] / "set_config_variables.py",
                sgv["folderpath_simulator"]
                / "SystemicRiskSimulator/data/config/set_config_variables.py",
            )

        # 快照：agents
        Tools.delete_and_recreate_folder(
            sgv["folderpath_experiments_output_agents"],
            is_auto_confirmation=sgv["is_auto_confirmation"],
        )
        shutil.copytree(
            sgv["folderpath_agents"] / "agents",
            sgv["folderpath_experiments_output_agents"] / "agents",
        )
        shutil.copyfile(
            sgv["folderpath_agents"] / "logfile.log",
            sgv["folderpath_experiments_output_agents"] / "logfile.log",
        )
        shutil.copyfile(
            sgv["folderpath_agents"] / "set_agents_variables.py",
            sgv["folderpath_experiments_output_agents"] / "set_agents_variables.py",
        )

        if sgv.get("runtime_copy_resources_into_simulator_data", False):
            Tools.delete_and_recreate_folder(
                Path(sgv["folderpath_simulator"], "SystemicRiskSimulator/data/agents"),
                is_auto_confirmation=sgv["is_auto_confirmation"],
            )
            shutil.copytree(
                sgv["folderpath_agents"] / "agents",
                sgv["folderpath_simulator"] / "SystemicRiskSimulator/data/agents/agents",
            )

        # 日志
        if sgv["is_rerun_all_done_works_in_the_same_experiments"]:
            for file in Path(sgv["folderpath_experiments_output_log"]).glob("outputlog.txt"):
                file.unlink()
            for file in Path(sgv["folderpath_experiments_output_log"]).glob("outputlog_*exp.txt"):
                file.unlink()

        logger = logging.getLogger()
        logger.setLevel(sgv["test_logging"])

        log_file_handler = logging.FileHandler(
            Path(sgv["folderpath_experiments_output_log"], "outputlog.txt"), encoding='utf-8-sig'
        )
        logger.addHandler(log_file_handler)
        log_console_handler = logging.StreamHandler()
        logger.addHandler(log_console_handler)

        if sgv["is_develope_mode"]:
            logging.info("\n------------ 开发与调试模式！ ---------------\n")

        logging.info(
            "\n开始记录时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        )
        logging.info("\n实验组名称：" + sgv["foldername_experiments"] + "\n")
        logging.info("\n模拟器 simulator 版本：" + sgv["simulator_version"][0] + "\n")
        logging.info(
            "\n相关实验配置项 config 文件夹：" + sgv["folderpath_config"].name + "\n"
        )
        logging.info(
            "\n相关实验 agents 数据文件夹：" + sgv["folderpath_agents"].name + "\n"
        )
        logging.info(
            "\n相关实验参数 parameters 文件夹：" + sgv["folderpath_parameters"].name + "\n"
        )
        logging.info(
            "\n相关实验 models 文件夹：" + sgv["folderpath_models"].name + "\n"
        )
        logging.info(
            "\n相关实验数据 experiments output data 文件夹：" + sgv["folderpath_experiments"].name + "\n"
        )

        # 关闭 handler（沿用原来的行为）
        log_file_handler.close()
        logger.removeHandler(log_file_handler)
        log_console_handler.close()
        logger.removeHandler(log_console_handler)

        # 运行实验组
        start_time = time.time()
        _run_stage_program(
            stage_name="实验组模拟程序",
            script_name="experiments_program.py",
            module_name="SystemicRiskSimulator.programs.experiments_program",
        )

        logger.addHandler(log_file_handler)
        logger.addHandler(log_console_handler)

        end_time = time.time()
        logging.info(f"\n模拟器运行时长：{end_time - start_time} 秒。\n")

        log_file_handler.close()
        logger.removeHandler(log_file_handler)
        log_console_handler.close()
        logger.removeHandler(log_console_handler)

    # 是否运行预处理程序（通常应在可视化之前执行）
    if sgv["schedule_operation"].get("预处理实验结果程序", False):
        _run_stage_program(
            stage_name="预处理实验结果程序",
            script_name="transform_output_data_program.py",
            module_name="SystemicRiskSimulator.programs.transform_output_data_program",
        )

    # 是否运行可视化程序
    if sgv["schedule_operation"].get("可视化结果程序", False):
        _run_stage_program(
            stage_name="可视化结果程序",
            script_name="visualize_data_program.py",
            module_name="SystemicRiskSimulator.programs.visualize_data_program",
        )

    # 当前 programs 目录尚未提供分析程序文件，先给出显式提示，避免误判“未生效”。
    if sgv["schedule_operation"].get("分析实验结果程序", False):
        logging.warning("schedule_operation['分析实验结果程序']=True，但当前未找到对应分析程序，已跳过。")

    # 清理：导出最后 config.pkl
    Collector.export_config_data(sgv)

    print("运行完毕！")
    print(f"时间：{datetime.datetime.now()}")


# ----------------------------
# CLI 入口（原 __main__.py）
# ----------------------------


def _build_parser():
    import argparse

    p = argparse.ArgumentParser(prog="SystemicRiskSimulator", add_help=True)

    p.add_argument(
        "--global-config",
        default="config.json",
        help="全局配置 JSON 路径（默认：项目根目录下 config.json）",
    )
    p.add_argument(
        "--experiment",
        default=None,
        help="实验名/ID：从 global config 的 experiments 里选择",
    )
    p.add_argument(
        "--experiment-json",
        default=None,
        help="直接指定实验 JSON 路径（绕过 global config）",
    )
    p.add_argument(
        "--set-config-folder",
        default=None,
        help="兼容模式：直接指定 set_config_variables.py 所在文件夹（等价于传入 folderpath_config）",
    )
    p.add_argument(
        "--override",
        action="append",
        default=None,
        help="覆盖项：key=value。可重复多次。示例：--override is_auto_confirmation=true",
    )

    return p


def main(argv: Optional[list[str]] = None) -> None:
    import argparse

    args = _build_parser().parse_args(argv)

    from SystemicRiskSimulator.tools.tools import Tools

    project_root = Tools.get_project_rootpath()
    overrides = parse_overrides(args.override)

    runner_cfg: Dict[str, Any] = {}
    exp_cfg: Dict[str, Any] = {}

    if args.set_config_folder:
        exp_cfg = {"folderpath_config": args.set_config_folder}
    elif args.experiment_json:
        exp_cfg = load_json(Path(args.experiment_json))
    else:
        global_path = Path(project_root, args.global_config)
        global_cfg = load_json(global_path)

        exp_name = args.experiment or global_cfg.get("default_experiment")
        if not exp_name:
            raise ValueError("未指定 experiment，且 global config 缺少 default_experiment。")

        exp_cfg = resolve_experiment_from_global(global_cfg, str(exp_name))
        runner_cfg = dict(global_cfg.get("runner", {}))

    config = build_simulator_config(
        project_root=Path(project_root),
        runner_cfg=runner_cfg,
        experiment_cfg=exp_cfg,
        overrides=overrides,
    )

    # IDE-friendly output: 显示工作目录、项目根路径及合成后的最终 config，方便在 PyCharm 直接运行时诊断问题
    try:
        import os

        cwd = Path(os.getcwd())
    except Exception:
        cwd = Path(".")

    print("\n[SystemicRiskSimulator] 开始运行（IDE/Run 按钮友好模式）")
    print(f"当前工作目录 (cwd): {cwd}")
    print(f"项目根路径 (project_root): {project_root}")
    print("合成后的最终 config（部分显示）:")
    try:
        from pprint import pformat

        print(pformat({k: config[k] for k in list(config.keys())[:20]}, width=120))
    except Exception:
        print(config)

    print("若要在 IDE 中运行特定实验，请在 Run/Debug Config 中设置参数，例如:\n  --global-config config.json --experiment ib2111\n")

    simulator(config)


__all__ = [
    "simulator",
    "main",
    "load_json",
    "build_simulator_config",
    "resolve_experiment_from_global",
    "parse_overrides",
]


if __name__ == '__main__':
    # 当用户在 IDE（例如 PyCharm）中直接右键运行 main.py 时，会执行这里。
    # 这会使用 sys.argv 作为默认参数解析，等价于在命令行运行：
    # python SystemicRiskSimulator/main.py [--global-config ... | --experiment-json ... | --set-config-folder ...]
    main()
