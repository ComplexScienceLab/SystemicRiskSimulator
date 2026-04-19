# SRS API 手册

## 1. Python 入口 API

### 1.1 `SystemicRiskSimulator.main.simulator(config)`

功能：运行一次实验调度主流程。

参数：

- `config` (`dict`)：运行配置字典。

关键字段（常用）：

- `folderpath_config` (`str`)：`set_config_variables.py` 所在目录。
- `foldername_simulator` (`str`)：模拟器项目名，通常是 `SystemicRiskSimulator`。
- `folderpath_realpath_simulator` (`str`)：相对路径，通常是 `.`。
- 其他覆盖字段可通过 `--override` 注入。

行为：

1. 读取并合并 `set_config_variables.py`。
2. 创建实验输出目录。
3. 快照 config/agents/parameters/models。
4. 按运行方式调用 `experiments_program.py`。
5. 导出最终配置与结果。

### 1.2 `SystemicRiskSimulator.main.main(argv=None)`

功能：CLI 入口。

支持参数：

- `--global-config`：全局配置 JSON。
- `--experiment`：从全局配置中选择实验键。
- `--experiment-json`：直接给实验 JSON。
- `--set-config-folder`：兼容模式，直接给 config 目录。
- `--override key=value`：覆盖配置项（可重复）。

## 2. 算法封装 API

### 2.1 `run_single_mechanism_cascade(...)`

位置：`SystemicRiskSimulator/core/algorithms/cascading_failure_single_mechanism_algorithm.py`

功能：通用单层单机制级联失效入口。

核心输入：

- `adjacency`：邻接矩阵 `(N, N)`。
- `load`：节点负载 `(N,)`。
- `capacity`：节点容量 `(N,)`。
- `initial_failed_mask`：初始失效集合。

核心输出：

- `final_state`
- `final_failed_mask`
- `history`（按开关返回）

### 2.2 `run_bank_interbank_cascade(...)`

位置同上。

功能：银行间场景专用包装，把 `Z_IB / E_all / Z_IB_all / Loss_*` 映射到单机制模型输入。

补充输出：

- `adjacency`
- `load_init`
- `capacity`

## 3. 运行模式关键开关（来自 set_config_variables）

- `is_use_Gym_environments`
- `is_use_RL_method`
- `RL_state` (`training` / `using`)
- `runtime_model_import_source` (`external` / `simulator_data`)
- `runtime_copy_resources_into_simulator_data` (`True` / `False`)

## 4. Samples 资源接口约定

### 4.1 agents 资源

- 目录：`Samples/libraries/agents_library/<sample>/agents/*.pkl`
- 由 `set_agents_variables.py` 生成。

### 4.2 parameters 资源

- 文件：`Samples/libraries/parameters_library/<sample>/parameters.pkl`
- 由 `set_parameters_variables.py` 生成。

### 4.3 models 资源

- 目录：`Samples/libraries/models_library/<sample>/`
- 至少包括：`model_main.py`、`model_finance.py`、`model_define.py`。

## 5. 兼容性说明

- 当前统一入口在 `SystemicRiskSimulator/main.py`。
- 建议新代码从 `SystemicRiskSimulator.main` 导入 `simulator`。
- 单机制级联实现已内置在 `SystemicRiskSimulator/core/algorithms/cascading_failure_single_mechanism_algorithm.py`，无需额外外部依赖。
