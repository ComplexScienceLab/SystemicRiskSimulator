"按照顺序集成各文件"

## 按照顺序集成各文件

##########################################
#状态/开发
##########################################

## 集成环境设置项文件
include("define/define_environmentVariables.jl")
include("set/set_environmentVariables.jl")

## 集成定义文件
include("define/define_type.jl")
include("define/define_agents.jl")

## 集成定义常数文件
include("define/define_consts.jl")

## 集成参数设置项文件
include("define/define_parameterVariables.jl")
include("set/set_parameterVariables.jl")

## 集成功能函数文件
include("functions/fun_balanceSheet.jl")
include("functions/fun_state.jl")
include("functions/fun_shock.jl")
include("functions/fun_loss.jl")
include("functions/fun_transfer.jl")

## 集成初始化函数文件
include("initialization/fun_initVariables.jl")

## 集成模块函数文件
include("module/modules_contagion_and_shock.jl")

## 集成过程函数文件
include("process/process_exBank_insolvent.jl")
include("process/process_interBank_insolvent.jl")
include("process/process_exBank_illiquity.jl")
include("process/process_interBank_illiquity.jl")
include("process/process_exBank_bankrupt.jl")
include("process/process_interBank_bankrupt.jl")


## 集成各模型函数文件
include("model/model_BI1111.jl")

## 集成做实验函数文件
include("experiments/fun_makesim.jl")