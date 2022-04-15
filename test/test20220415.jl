include("define.jl")
include("model_content.jl")
include("model_skeleton.jl")

## 生成模型model
modelBuilder!(modelContent)

## 运行模型model
@runModel
