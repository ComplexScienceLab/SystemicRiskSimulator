# SystemicRiskSimulator

SystemicRiskSimulator，简称 SRS，是一个面向系统性风险研究的配置驱动模拟器。它的核心价值不只是“跑一个模型”，而是把实验组织成统一入口、统一四件套资源和统一快照输出，让不同模型家族可以在同一套调度框架下运行、复现和扩展。

## 项目定位

SRS 当前主要服务于这类任务：

1. 多主体系统性风险模拟。
2. 银行间网络、违约传染、共同资产冲击等实验。
3. 以四件套 library 为单位管理实验资源。
4. 在开发模式与批量运行模式之间切换。
5. 对实验输入和模型代码做完整快照，保证复现。

SRS 的基本架构是：

1. main.py 作为统一入口。
2. core、programs、tools 提供通用调度与基础设施。
3. configs_library、agents_library、parameters_library、models_library 四件套提供具体实验内容。

## 核心思想

SRS 不鼓励把实验写成一个难以维护的大脚本，而是强调分层：

1. Simulator 内核负责调度、导入、路径解析、快照、结果导出。
2. 四件套负责描述实验配置、初始状态、参数组合和模型本体。

这意味着新增一个实验时，优先是新增或复用一套四件套，而不是改写主程序入口。

## 仓库结构

```text
SystemicRiskSimulator/
|- SystemicRiskSimulator/
|  |- main.py
|  |- programs/
|  |- core/
|  \- tools/
|- Samples/
|  |- exp/
|  \- libraries/
|- docs/
|- config.json
|- pyproject.toml
\- requirements.txt
```

其中最重要的目录是：

1. SystemicRiskSimulator/main.py：统一 CLI 与 simulator 入口。
2. Samples/libraries：自带四件套样例。
3. Samples/exp：实验 JSON 样例。
4. docs：手册与指南。

## 安装

推荐使用 uv：

```powershell
uv venv .venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

如果你仍在使用传统 venv：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 快速开始

以 Samples 中的 IB2111 为例，推荐按这个顺序运行。

### 1. 生成 agents

```powershell
Set-Location Samples/libraries/agents_library/agents_sample_IB2111
python set_agents_variables.py
```

### 2. 生成 parameters

```powershell
Set-Location ../../parameters_library/parameters_sample_IB2111
python set_parameters_variables.py
```

### 3. 回到仓库根目录并启动实验

```powershell
Set-Location ../../../..
python -m SystemicRiskSimulator.main --set-config-folder Samples/libraries/configs_library/config_sample_IB2111
```

也可以通过全局 config 选择实验：

```powershell
python -m SystemicRiskSimulator.main --global-config config.json --experiment ib2111
```

## 三种常用运行方式

### 1. global config + experiment

```powershell
python -m SystemicRiskSimulator.main --global-config config.json --experiment ib2111
```

适合集中管理多个实验入口。

### 2. experiment JSON

```powershell
python -m SystemicRiskSimulator.main --experiment-json Samples/exp/exp_sample_IB2111.json
```

适合快速选择某个样例实验。需要注意，当前 experiment JSON 主要用于选择 folderpath_config 和补少量字段，真正权威的实验细节仍由 set_config_variables.py 决定。

### 3. 直接指定配置目录

```powershell
python -m SystemicRiskSimulator.main --set-config-folder Samples/libraries/configs_library/config_sample_IB2111
```

适合调试单个实验，也是最直接的方式。

## 四件套 library

SRS 当前标准实验资源组织方式是四件套：

```text
libraries/
|- configs_library/
|- agents_library/
|- parameters_library/
\- models_library/
```

它们的职责分别是：

1. configs_library：定义路径、运行开关、阶段开关和实验口径。
2. agents_library：生成初始个体和网络数据。
3. parameters_library：生成参数组合表和实验任务表。
4. models_library：提供模型代码本体。

SRS 当前默认会：

1. 从 folderpath_models 直接导入模型代码。
2. 从 folderpath_agents 读取 agents/*.pkl。
3. 从 folderpath_parameters 读取 parameters.pkl。
4. 把这四类输入快照复制到实验输出目录。

## 输出与复现

实验运行后，输出目录里最重要的内容通常是：

1. exp_output_data：实验输出数据。
2. outputlog：日志与四件套快照。
3. outputlog/config：实际使用的配置快照。
4. outputlog/agents：实际使用的初始数据快照。
5. outputlog/parameters：实际使用的参数快照。
6. outputlog/models：实际使用的模型代码快照。

SRS 的复现能力高度依赖这些快照。正式实验不要只保留结果，不保留输入和模型快照。

## 开发与调试

SRS 支持开发优先模式。常见做法是：

1. 在 set_config_variables.py 中设置 is_develope_mode=True。
2. 通过 main.py 启动实验。
3. 在 IDE 中对 ModelMain、Operator、Collector、Executer 打断点。

当前默认推荐的模型导入方式是：

1. runtime_model_import_source='external'
2. runtime_copy_resources_into_simulator_data=False

这意味着开发时直接在四件套目录中改模型，SRS 会从该目录 import，并把实际运行版本快照到输出目录。

## 外部工程接入

SRS 不限于 Samples，也可以读取外部工程的四件套资源。推荐外部工程也提供一个 libraries 目录，并沿用四件套布局。

运行方式示例：

```powershell
python -m SystemicRiskSimulator.main --set-config-folder "D:/YourProject/libraries/configs_library/config_demo"
```

对外部工程而言，最关键的是：

1. folderpath_config 指向一个包含 set_config_variables.py 的目录。
2. set_config_variables.py 中的 folderpath_models、folderpath_parameters、folderpath_agents 与外部工程目录实际一致。
3. 模型目录保持完整包结构。

## 文档

1. 开发者指南：docs/开发者指南.md
2. 用户手册：docs/用户手册.md
3. API 手册：docs/API手册.md

## 使用约束

SRS 的正式使用和正式开发应遵守几条底线：

1. 正式入口始终是 main.py，而不是零散阶段脚本。
2. 正式实验资源始终是四件套，而不是临时脚本拼接出来的替代品。
3. 正式结果必须保留 config、agents、parameters、models 的快照。
4. 公共配置与公共文档中应尽量避免写死本机绝对路径。

## 许可证

本项目使用 GNU AGPLv3。
