"系统性风险仿真模型"

## 系统性风险仿真模型

##########################################
#状态/可扩展
# 可引入新文件
##########################################


# module Models

# using 


## 集成阶段文件#NOW


## 集成过程文件
include("../model/processes/process_list.jl")
include("../model/processes/process_exBank_insolvent.jl")
include("../model/processes/process_interBank_insolvent.jl")
include("../model/processes/process_exBank_illiquity.jl")
include("../model/processes/process_interBank_illiquity.jl")
include("../model/processes/process_exBank_bankrupt.jl")
include("../model/processes/process_interBank_bankrupt.jl")


## 集成模型文件
# include("../model/models/model_list.jl")
include("../model/models/model_BI1111.jl")


# end # module