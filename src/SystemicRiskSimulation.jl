"系统性风险仿真模拟"

## 系统性风险仿真模拟

##########################################
#状态/可扩展
# 可引入新文件
##########################################



# module SystemicRiskSimulation


## 加载外部工具包
using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目
using Dates
using DataFrames
using StructArrays
using Graphs
using Agents


## 集成定义文件
include("./core/define/define_type.jl")
include("./core/define/define_component.jl")
include("./core/define/define_environmentVariables.jl")
include("./base/define/define_agents.jl")
include("./base/define/define_parameterVariables.jl")

## 集成定义常数文件
include("./core/define/define_consts.jl")

## 集成工具功能文件
include("./core/controller/fun_tools.jl")

## 集成调度功能文件
include("./core/controller/fun_io.jl")
include("./core/controller/fun_agentModel.jl")
include("./core/controller/schedulers.jl")
include("./core/controller/fun_makesim.jl")
include("./core/controller/process_builder.jl")
include("./core/controller/model_builder.jl")
include("./core/controller/process_runner.jl")
include("./core/controller/model_runner.jl")

## 集成初始化函数文件
include("./base/initialization/fun_initVariables.jl")

## 集成功能函数文件
include("./base/functions/fun_balanceSheet.jl")
include("./base/functions/fun_state.jl")
include("./base/functions/fun_shock.jl")
include("./base/functions/fun_loss.jl")
include("./base/functions/fun_transfer.jl")
include("./base/functions/fun_measure.jl")


# include("./model/Models.jl")
# export Models
# end # module


