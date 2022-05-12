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
    s1::Vector{Float32}
    s2::Vector{Float32}
end

st1=St([1,1,1],[2,2,2,2])
st2=St([3,3,3],[4,4,4,4])
ssst=StructArray((st1,st2))
asst=[]
append!(asst,[[merge(Dict([:tau=>1]),Dict([:indexStage=>1]),struct2dict(st1))]])
append!(asst,[[merge(Dict([:tau=>2]),Dict([:indexStage=>1]),struct2dict(st2))]])

run(`cd test/data`)
run(`ls`)

jldsave("asst.jld2";asst)
asst2=load("asst.jld2")



para = load("kappa_A_P=0.0|kappa_BI=0.0|modelName=BI1111._1.jld2")
BB = load("BB1.jld2")
BB["dataBB"]

BI = load("test/data/BI1.jld2")
dump(BI["dataBI"])

BI["dataBI"][1][1]
BI["dataBI"][1][1][:ilq]
BI["dataBI"][2][1][:ilq]

BI = load("BIarray1.h5")
typeof(BI)
dump(BI)

