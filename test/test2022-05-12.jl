## 加载外部工具包
using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目
using Dates
using DataFrames
using StructArrays
using Graphs
using Agents
using CSV
using JLD2
using HDF5
using JSON

mutable struct St
    s1::Matrix{Float64}
    s2::Matrix{Float64}
end

st1 = St([1 2 3; 4 5 6; 7 8 9], [10 11 12; 13 14 15; 16 17 18])
st2 = St([1 2 3; 4 5 6; 7 8 9] .* 10, [10 11 12; 13 14 15; 16 17 18] .* 10)
asst = []
# append!(asst, [[merge(Dict([:tau => 1]), Dict([:indexStage => 1]), struct2dict(st1))]])
# append!(asst, [[merge(Dict([:tau => 2]), Dict([:indexStage => 1]), struct2dict(st2))]])

asst_item = [Dict([:tau => 1, :data => st1])]
append!(asst, asst_item)
asst_item = [Dict([:tau => 2, :data => st2])]
append!(asst, asst_item)
asst
asst[1]
asst[1][:tau]
asst[1][:data].s1
#FIXME for (i,v) in enumerate(asst[1][:data]) 
    i
    v
end

asst_export = DataFrame()
df_asst = DataFrame()
for (i1, v1) in enumerate(asst)
    df_asst[!, :tau] = v2[:tau]
    for (i2, v2) in enumerate(v1)
        df_asst[!, :data] = v2[:data]
    end
end
append!(asst_export, df_asst)

# run(`cd test/data`)
# run(`ls`)

# jldsave("asst.jld2"; asst)
# asst2 = load("asst.jld2")


# h5open("asst.h5", "w") do f
#     for (i,v) in enumerate(asst)
#         f["$(i)"]=Dict()
#         for (j,d) in enumerate(v)
#             write(f,"$(i)/$(j)",d)
#         end
#     end
# end

h5open("asst.h5", "r") do f
    a = read(f, "data")
    println(a)
end



para = load("test/data/kappa_A_P=0.0|kappa_BI=0.0|modelName=BI1111._1.jld2")
BBjld2 = load("test/data/BB1.jld2")
BBjld2["dataBB"]

BIjld2 = load("test/data/BI1.jld2")
dump(BI["dataBI"])

BIjld2["dataBI"][1]
BIjld2["dataBI"][1][:ilq]
BIjld2["dataBI"][2][:dataId]


BBh5 = read("test/data/BB1.h5")
BBh5["dataBB"]

BIh5 = load("test/data/BI1.h5")
dump(BI["dataBI"])

BIh5["dataBI"][1]
BIh5["dataBI"][1][:ilq]
BIh5["dataBI"][2][:dataId]

BIh5 = load("BIarray1.h5")
typeof(BIh5)
dump(BIh5)

