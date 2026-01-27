# SystemicRiskSimulator：AI 编码代理工作指引

## 项目定位

- Python 3.11 的系统性风险模拟器包，支持 ABM 与可选的 Gymnasium/RL 流程。
- 入口函数：`SystemicRiskSimulator.simulator.simulator(config)`，从 `data/config/set_config_variables.py` 读取配置并落盘实验输出。

## 关键目录

- `SystemicRiskSimulator/`：核心代码（`core/`、`programs/`、`tools/`、`simulator.py`）。
- `data/`：运行时复制的配置、agents、参数等；由 Tools 辅助创建/覆盖，不手改。
- `programs/experiments_program.py`：实际运行实验流程（被 `simulator()` 调用）。

## 依赖与环境

- 依赖见 [pyproject.toml](../pyproject.toml) / [requirements.txt](../requirements.txt)，Python >=3.11。
- 无需写死绝对路径，模拟器会用 `Tools.get_project_rootpath()` 与配置组合路径。

## 路径与输出约定

- 运行时会根据配置生成 `experiments_output_data/log/config/...` 等子目录；不要手动清理正在使用的输出目录。
- 跨机器/iCloud 请保持相对路径或通过 config 传入，不要将本机绝对路径写入提交内容。

## 修改建议

- 调整实验流程或输出结构时，同步检查 `simulator()`、`programs/experiments_program.py` 与相关 `tools`/`core` 里的契约字段。
- 若新增配置字段，记得同时更新 `data/config/set_config_variables.py` 模板与读取逻辑。
