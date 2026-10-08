# SystemicRiskSimulator 用户手册

> 适用版本：以仓库当前代码为准（建议与 `data/config/set_config_variables.py` 中的 `simulator_version` 对齐）。

## 1. 项目简介

SystemicRiskSimulator 是一个用 Python 3.13 编写的系统性风险模拟器，核心范式为多主体建模（ABM）。项目还包含可选的 Gymnasium/RL（强化学习）实验运行流程。

本项目的**推荐入口函数**为：

- `SystemicRiskSimulator.main.simulator(config)`

模拟器运行时会将本次实验用到的配置、agents、parameters、models **复制**到实验输出目录，便于复现实验。

## 2. 快速开始（最小可运行）

### 2.1 安装

- Python：3.13（必需）
- 依赖：见 `requirements.txt` 或 `pyproject.toml`

安装后，你可以选择两种使用方式：

1. 作为 Python 包导入使用（推荐）
2. 作为命令行工具运行（如果你安装了 entrypoint）

### 2.2 最小示例：通过 Python 调用模拟器

```python
from SystemicRiskSimulator.main import simulator

config = {
    # 通常只需要覆盖你要改的部分配置；其余将由 set_config_variables.py 进行补全
    # 例如：
    # "is_develope_mode": True,
}

simulator(config)
```

> 注意：`config` 会与 `data/config/set_config_variables.py` 中的模板字典合并，最终以运行时 `sgv`（Simulator Global Variables）为准。

## 3. 核心概念与术语

- **sgv**：Simulator Global Variables。模拟器运行时的“全局配置字典”，会由 `set_config_variables.py` + `config` 合并得到。
- **experiments（实验组）**：一次运行通常包含多个实验（experiment/exp）。
- **exp_id / id_experiment**：单个实验的编号。
- **parameters_works**：从 `parameters.pkl` 读取的实验参数表（DataFrame）。
- **agents 数据**：初始化个体群（银行/资产等）所需数据，位于 `agents/agents/*.pkl`。
- **models**：实验模型代码，运行时会从 `libraries/models_library/...` 复制到输出目录并导入。

## 4. 运行模式说明（ABM / Gymnasium / RL）

运行模式主要由以下配置决定（见 `set_config_variables.py`）：

- `is_use_Gym_environments`: 是否使用 Gymnasium 环境框架
- `is_use_RL_method`: 是否启用强化学习流程
- `RL_state`: `training` 或 `using`（只在 RL 流程下有意义）

入口 `simulator()` 会根据这些字段计算 `sgv['运行实验组的方式']`，并决定输出数据子目录（如：`RL_training` / `RL_using` / `normal`）。

## 5. 配置说明（如何改实验）

### 5.1 配置来源与合并规则

- 模板：`data/config/set_config_variables.py` 中的 `set_config_variables` 字典
- 用户覆盖：调用 `simulator(config)` 时传入的 `config` 字典

合并顺序（简化理解）：

1. 读取模板字典并载入为 `sgv`
2. 用传入的 `config` 更新 `sgv`
3. `sgv` 再回写到 `config`（供后续使用）

### 5.2 与“库文件夹”相关的关键路径配置

以下字段决定运行时“复制哪些模型/参数/agents/配置到输出目录”：

- `folderpath_models`
- `folderpath_config`
- `folderpath_parameters`
- `folderpath_agents`

这些路径**建议使用相对路径**（项目内路径），避免提交含本机绝对路径的配置。

### 5.3 常用运行控制开关

- `schedule_operation['实验组模拟程序']`：是否运行实验组模拟
- `schedule_operation['预处理实验结果程序']`：是否运行结果预处理
- `schedule_operation['可视化结果程序']`：是否运行可视化
- `is_enable_multiprocessing_for_run_model`：是否并行运行多个实验
- `is_use_sqlite_to_manage_experiments`：是否用 SQLite 管理实验作业状态
- `is_rerun_all_done_works_in_the_same_experiments`：是否重跑已完成实验
- `is_develope_mode`：开发/调试模式（影响是否用子进程运行）

### 5.4 在外部项目文件夹中使用 SRS 的要求与限制

如果你要让 SRS 读取**另一个项目**中的配置与资源（而不是直接使用 `Samples/...`），请特别注意以下规则：

1. `folderpath_config` 必须指向包含 `set_config_variables.py` 的配置文件夹。
2. 对外部项目，推荐把 `folderpath_config` 写成**绝对路径**；这样 SRS 才能稳定识别“当前实验实际属于哪个外部项目”。
3. 当前版本对外部项目根目录的自动识别，优先依赖 `libraries` 命名约定。最稳妥的布局是：

```text
外部项目根目录/
|- libraries/
|  |- configs_library/
|  |- agents_library/
|  |- parameters_library/
|  \- models_library/
```

4. 一旦 `folderpath_config` 被识别为外部项目目录，`set_config_variables.py` 中的：
   - `folderpath_config`
   - `folderpath_models`
   - `folderpath_parameters`
   - `folderpath_agents`

   推荐都写成**相对外部项目根目录**的路径。

5. 如果外部项目与 `SystemicRiskSimulator` 不是同级兄弟目录，则不能继续依赖 `runner.folderpath_realpath_simulator="."` 的默认值；应显式调整该字段，让运行期能正确回到 SRS 仓库本体。
6. `agents`、`parameters`、`models` 目录本身也必须满足原有契约：
   - `agents` 目录下应有 `agents/`、`set_agents_variables.py`、`logfile.log`
   - `parameters` 目录下应有可被当前环境读取的参数文件
   - `models` 目录下若使用相对导入，必须保持包结构完整

如果以上规则未满足，常见报错包括：

- `配置文件不存在`
- `FileNotFoundError: ...agents...`
- `FileNotFoundError: ...parameters...`
- `ImportError: attempted relative import with no known parent package`

更完整的外部项目接入说明、示例命令与排查清单，请见：`docs/用户手册.md` 中的“外部项目文件夹接入 SRS”章节。

## 6. 输入数据格式（agents / parameters / models）

### 6.1 parameters（参数作业表）

- 位置：`<folderpath_parameters>/parameters.pkl`
- 读取：`Operator.operate_installing()`
- 形态：`pandas.DataFrame`，至少包含 `exp_id` 列

### 6.2 agents（个体群初始化数据）

- 位置：`<folderpath_agents>/agents/*.pkl`
- 文件名由以下字段拼接（见 `Collector.init_agent_data_collection`）：
  - `id_agents`
  - `list_agents_data_filename_para_01`（例如 BB/DA/IB/IBA/note）
  - `list_agents_data_filename_para_02`（例如 year/density_IB/density_IBA）

### 6.3 models（模型代码）

- 位置：`<folderpath_models>/...`
- 运行时会复制到：
  - `experiments_output_log/models/`
  - `SystemicRiskSimulator/data/model/`

并通过 `Tools.import_modules_from_package(..., r"[Mm]odel", ...)` 动态导入。

## 7. 输出说明（目录结构与文件内容）

运行时输出目录由 `Tools.set_experiments_folders()` 生成。

典型结构（简化）：

- `SystemicRiskData/data/sims/<experiments_name>/`
  - `exp_output_data/`（或 RL 子目录）
  - `outputlog/`
    - `outputlog.txt`（主日志）
    - `config/set_config_variables.py`（本次配置副本）
    - `parameters/`（本次参数副本）
    - `agents/`（本次 agents 副本）
    - `models/`（本次模型副本）

如果启用了 SQLite 管理，还会生成：

- `outputlog/experiments_works_status.db`

## 8. 常见问题（FAQ）

### Q1：为什么我改了 `data/config/set_config_variables.py` 但运行后没生效？

A：模拟器会把配置复制到输出目录和包内 `SystemicRiskSimulator/data/config/`。请确认你改的是当前运行所引用的 config 库文件夹（`folderpath_config`）下的 `set_config_variables.py`，而不是历史输出目录中的副本。

### Q2：如何仅运行某些实验（exp_id）？

A：通过 `list_idsExperiment_to_run` 控制：

- `None`：运行所有
- `list[int]`：只运行指定 exp_id 列表
- `str`：作为筛选表达式（内部使用 `eval`），比如：`"(parameters_works['alpha'] > 0.5) & (parameters_works['beta'] < 1)"`

> 注意：字符串表达式会被 `eval` 执行，属于高风险功能，请只在可信环境使用。

### Q3：并行模式下日志为什么分散？

A：并行运行时通常会关闭主进程 handler，由子进程单独记录（或写入 `outputlog_{i}_exp.txt`），结束后再合并追加到 `outputlog.txt`。
