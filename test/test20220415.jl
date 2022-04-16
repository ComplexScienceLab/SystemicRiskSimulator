# 主程序入口

include("define.jl")
include("process_content.jl")
include("model_content.jl")
# include("model_skeleton.jl")
include("model_builder.jl")
# include("fun_model_skeleton_template.jl")

## 生成模型model
modelBuilder!(model_BI1111)

## 运行模型model
# @runModel

