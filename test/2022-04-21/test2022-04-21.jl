
include("define.jl")
include("define_component.jl")
include("fun_stage.jl")
include("content.jl")
include("skeleton.jl")
include("fun_builder.jl")
include("fun_runner.jl")

model = buildModel(modelContent_1)

data = runModel!(model)
data = model.run(data, model)
