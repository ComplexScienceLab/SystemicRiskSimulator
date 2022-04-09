"系统性风险仿真模型"

## 系统性风险仿真模型

##########################################
#状态/可扩展
# 可引入新文件
##########################################


# module Models

# using 

## 集成通用框架文件
include("../model/models/fun_model_skeleton.jl")
include("../model/processes/fun_process_skeleton.jl")

## 集成名称集合文件
include("../model/model_variables/set_models.jl")
include("../model/model_variables/set_processes.jl")
include("../model/model_variables/set_stages.jl")

## 集成阶段文件
include("../model/stages/stage_list.jl")
include("../model/stages/fun_stage_exBank_insolvent_shock.jl")
include("../model/stages/fun_stage_interBank_insolvent_shock.jl")
include("../model/stages/fun_stage_interBank_insolvent_contagion.jl")
include("../model/stages/fun_stage_exBank_illiquity_shock.jl")
include("../model/stages/fun_stage_interBank_illiquity_contagion_shock.jl")
include("../model/stages/fun_stage_interBank_illiquity_allocate.jl")
include("../model/stages/fun_stage_interBank_illiquity_repay.jl")
include("../model/stages/fun_stage_exBank_bankrupt_contagion.jl")
include("../model/stages/fun_stage_interBank_bankrupt_contagion_shock.jl")
include("../model/stages/fun_stage_bankrupt_repay_shock.jl")

## 集成过程文件
include("../model/processes/process_list.jl")
include("../model/processes/fun_process_exBank_insolvent.jl")
include("../model/processes/fun_process_interBank_insolvent.jl")
include("../model/processes/fun_process_exBank_illiquity.jl")
include("../model/processes/fun_process_interBank_illiquity.jl")
include("../model/processes/fun_process_exBank_bankrupt.jl")
include("../model/processes/fun_process_interBank_bankrupt.jl")


## 集成模型文件
include("../model/models/model_list.jl")
include("../model/models/fun_model_BI1111.jl")


# end # module