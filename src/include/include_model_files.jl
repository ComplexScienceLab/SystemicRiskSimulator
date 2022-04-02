"按照顺序集成各模型代码文件"

## 按照顺序依次加载各模型文件以集成起来。

##########################################
#状态/可扩展
##########################################

## 集成阶段文件


## 集成过程文件
include("../model/processes/process_list.jl")
include("../model/processes/process_exBank_insolvent.jl")
include("../model/processes/process_interBank_insolvent.jl")
include("../model/processes/process_exBank_illiquity.jl")
include("../model/processes/process_interBank_illiquity.jl")
include("../model/processes/process_exBank_bankrupt.jl")
include("../model/processes/process_interBank_bankrupt.jl")


## 集成模型文件
include("../model/models/model_list.jl")
include("../model/models/model_BI1111.jl")






