"按照顺序集成各源代码文件"

## 按照顺序依次加载各源代码文件以集成起来。

##########################################
#状态/可扩展
##########################################

## # 集成核心文件

## 集成定义文件
include("../core/define/define_type.jl")
include("../core/define/define_model.jl")
include("../core/define/define_environmentVariables.jl")

## 集成定义常数文件
include("../core/define/define_consts.jl")


## 集成调度功能文件
include("../core/scheduler/schedulers.jl")
include("../core/scheduler/fun_io.jl")
include("../core/scheduler/fun_agentModel.jl")
include("../core/scheduler/fun_makesim.jl")

## 集成初始化函数文件
include("../core/initialization/fun_initVariables.jl")

# ## 集成模块函数文件
# include("../module/modules_contagion_and_shock.jl")

## 集成过程函数文件
include("../process/process.jl")
include("../process/process_exBank_insolvent.jl")
include("../process/process_interBank_insolvent.jl")
include("../process/process_exBank_illiquity.jl")
include("../process/process_interBank_illiquity.jl")
include("../process/process_exBank_bankrupt.jl")
include("../process/process_interBank_bankrupt.jl")

## 集成各模型函数文件
include("../model/model_BI1111.jl")

## 集成做实验函数文件
include("../experiments/fun_makesim.jl")


## # 集成基础文件

## 集成定义文件
include("../base/define/define_agents.jl")
include("../base/define/define_parameterVariables.jl")

## 集成功能函数文件
include("../base/functions/fun_balanceSheet.jl")
include("../base/functions/fun_state.jl")
include("../base/functions/fun_shock.jl")
include("../base/functions/fun_loss.jl")
include("../base/functions/fun_transfer.jl")
include("../base/functions/fun_measure.jl")






