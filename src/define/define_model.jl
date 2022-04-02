"程序：定义模型结构体"


"定义模型结构体"
mutable struct Model{NDIMS1}
    id::Int8 # 编号 id
    name::String # 模型名称 name
    list_process::Vector{Dict{Symbol,Symbol}} # 模型需要的过程列表 list_process
end

