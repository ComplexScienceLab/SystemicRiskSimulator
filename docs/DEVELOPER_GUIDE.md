# SystemicRiskSimulator 开发者文档

> 面向需要阅读源码、扩展模型/流程、或贡献代码的开发者。

## 1. 架构概览

### 1.1 入口与主流程

- 入口函数：`SystemicRiskSimulator.simulator.simulator(config)`
- 实验主程序：`SystemicRiskSimulator/programs/experiments_program.py::main(sgv)`
- 关键运行时全局字典：`sgv`（Simulator Global Variables）

入口 `simulator()` 的核心职责：

1. 解析/合并配置（从 `folderpath_config/set_config_variables.py` 动态导入模板）
2. 创建实验输出目录结构
3. 将 config/agents/models 复制到 output 与包内 `SystemicRiskSimulator/data/` 目录
4. 依据 `is_develope_mode` 选择：
   - 子进程运行 `experiments_program.py`（非开发模式）
   - 直接调用 `experiments_program.main()`（开发模式）

### 1.2 关键目录与定位

- `SystemicRiskSimulator/`：包主代码
  - `core/`：ABM 核心框架、初始化、操作、模板
  - `programs/`：实验/预处理/可视化等“可运行程序”
  - `tools/`：通用工具（路径、动态导入、RL/可视化辅助等）
  - `data/`：运行时被复制覆盖的“实验副本数据”（**不要手改**）
- `data/`（仓库根目录）：用于运行时复制/模板的资源与样例
- `Samples/`：示例程序与示例库
- `docs/`：文档

### 1.3 核心模块

- `core/operations/operator.py`：
  - 安装（installing）：加载参数表、生成待运行实验列表
  - 实验管理：SQLite 状态、重跑逻辑、筛选实验
  - 导入模型：复制模型到输出目录 + 动态导入
- `core/operations/collector.py`：
  - agent 数据收集、导出参数/配置、（可选）压缩/面板化等
- `tools/tools.py::Tools`：
  - 项目根路径解析
  - 实验目录结构生成
  - 删除并重建目录、复制文件
  - 动态导入模块（regex 过滤）
- `tools/logging_tools.py`：
  - SQLite 状态写入、便捷日志函数
- `tools/rl_utils.py`：
  - RL 训练数据保存/加载、优势估计等

## 2. 关键数据契约（Contract）

### 2.1 sgv（Simulator Global Variables）

`sgv` 是运行全局字典，通常包含：

- 路径：`folderpath_*`（project、simulator、experiments、outputlog 等）
- 运行模式：ABM / Gym / RL（由 `is_use_Gym_environments`、`is_use_RL_method`、`RL_state` 等决定）
- 调度：`schedule_operation`（是否运行实验/预处理/可视化/分析）
- 并行：`is_enable_multiprocessing_for_run_model`、`percent_core_for_multiprocessing`
- 实验与参数：`list_idsExperiment_to_run`、`list_agents_yearName` 等
- 输出细节：是否导出 xlsx/csv、是否压缩数据、可视化选项等

重要约定：

- 不要在代码里写死绝对路径；使用 `Tools.get_project_rootpath()` 与配置组合。
- `SystemicRiskSimulator/data/` 目录中的内容多数是运行时复制的副本；扩展时应优先修改 `libraries/` 下对应“源配置/源数据/源模型”。

### 2.2 parameters_works（参数作业表）

- 数据源：`<folderpath_parameters>/parameters.pkl`
- 类型：`pandas.DataFrame`
- 至少字段：`exp_id`

`Operator.operate_installing()` 负责：

- 读取 `parameters.pkl`
- 按 `list_idsExperiment_to_run` 规则生成 `list_idsExp_PLAN` / `list_idsExp_TASK`
- 可选：使用 SQLite 数据库 `experiments_works_status.db` 存储/恢复作业状态

### 2.3 agents 初始化数据

- 数据源：`<folderpath_agents>/agents/*.pkl`（按命名规则组合）
- `Collector.init_agent_data_collection()` 会加载不同类型的 agents 数据（BB/DA/IB/IBA/note 等）

命名规则（简化）：

- `id=<id_agents>-v=<para_01>-year=<...>-density_IB=<...>-density_IBA=<...>.pkl`

其中 `para_01` 来自 `sgv['list_agents_data_filename_para_01']`。

### 2.4 models 动态导入约定

- `Operator.operate_installing()` 会将 `folderpath_models` 复制到输出目录与包内 `SystemicRiskSimulator/data/model/`
- 通过 `Tools.import_modules_from_package(path, r"[Mm]odel", root)` 动态导入为 `model_dict`

建议：

- 模型文件命名包含 `Model` 或 `model`（匹配默认正则）
- 模型应对外暴露稳定接口（例如 `model_content`、`model_action` 等在 RL/Gym 流程中会被调用）

## 3. 实验程序（experiments_program）运行机制

`experiments_program.main(sgv)` 的典型流程：

1. 设置主日志 handler
2. `Operator.operate_installing(sgv)`：加载参数表、生成待运行实验列表、导入模型
3. 根据 `sgv['运行实验组的方式']` 分支运行：
   - ABM：串行或 multiprocessing 并行调用 `fun_single_experiment_work`
   - Gym + ABM / RL：注册环境、reset/step 循环等
4. 汇总时间统计与日志

并行运行要点：

- 主进程常会关闭 handler，子进程记录各自日志
- 若启用 SQLite 管理实验状态，需注意 Windows 上数据库锁与并发写入的风险

## 4. 如何新增/扩展功能

### 4.1 新增配置项

1. 在模板 `data/config/set_config_variables.py`（或你所使用的 config 库文件夹）中加入字段与注释
2. 确认读取逻辑是否依赖该字段：
   - `simulator()` 入口的运行模式判断
   - `Tools.set_experiments_folders()` 的输出目录
   - `Operator/Collector` 的导入/导出契约
3. 若影响输出结构，同步更新用户手册与 README。

### 4.2 新增模型

推荐流程：

1. 在 `libraries/models_library/...` 新建模型文件（命名建议包含 `Model`）
2. 确保模型提供 experiments_program 期望的调用接口
3. 在 config/parameters/agents 与模型相互匹配的前提下运行

### 4.3 新增可视化/预处理程序

- 实现为 `SystemicRiskSimulator/programs/*.py` 的独立 `main(sgv)`
- 在 `simulator()` 中按 `schedule_operation` 调度
- 输出统一写入 `folderpath_experiments_output_*` 约定目录

## 5. 开发与调试建议

### 5.1 开发模式 vs 非开发模式

- `is_develope_mode=True`：直接调用 Python 函数（适合断点调试）
- `is_develope_mode=False`：以子进程运行 scripts（更贴近批量跑实验的生产模式）

### 5.2 安全/可维护性注意事项

- `list_idsExperiment_to_run` 支持字符串表达式并用 `eval` 执行：
  - 不要在不可信输入下启用
  - 建议后续替换为安全的查询/表达式解析（例如受限语法）

- 输出目录重建：`Tools.delete_and_recreate_folder()` 可能删除目录
  - 文档与代码中应强调其副作用；避免对用户的重要路径误删

## 6. 贡献规范（建议）

- 小步提交，提交信息包含“模块 + 目的”
- 修改实验流程或输出结构时：同步检查 `simulator()`、`experiments_program.py` 与相关 tools/core 契约字段
- 新增/修改配置项时：同时更新对应模板与读取逻辑，并更新用户手册
