## 加载外部工具包
using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目
using Dates
using StructArrays
using Graphs
using Agents
using CSV
using JLD2
using HDF5
using JSON

using DataFrames

# 定义结构体
mutable struct St
    s1::Matrix{Float64}
    s2::Matrix{Float64}
end

# 生成数组，元素为结构体
st1 = St([1 2 3; 4 5 6; 7 8 9], [10 11 12; 13 14 15; 16 17 18])
st2 = St([1 2 3; 4 5 6; 7 8 9] .* 10, [10 11 12; 13 14 15; 16 17 18] .* 10)
a = []
a_item = [Dict([:tau => 1, :data => st1])]
append!(a, a_item)
a_item = [Dict([:tau => 2, :data => st2])]
append!(a, a_item)

# 查看数组
a
a[1]
a[1][:tau]
a[1][:data]
getfield(a[1][:data], :s1)
size(a[1][:data])

# 转换该数组a为数据框结构
a_df = DataFrame()
df = DataFrame()
for (i1, v1) in enumerate(a)
    numRow, numCol = size(getfield(a[1][:data], fieldnames(typeof(a[1][:data]))[1]))
    # enumerate(v1[:data])
    df[!, :tau] = fill(v1[:tau], numRow * numCol)
    df[!, :row] = repeat(1:numRow, inner=numCol)
    df[!, :col] = repeat(1:numCol, outer=numRow)
    fieldNames = fieldnames(typeof(v1[:data]))
    fieldValues = [getfield(v1[:data], fieldName) for fieldName in fieldNames]
    for (i2, v2) in enumerate(fieldValues)
        df[!, fieldNames[i2]] = [v2'...]
    end
    append!(a_df, df)
end

# 查看结果
a_df


i1 = 1;
v1 = a[1];
# run(`cd test/data`)
# run(`ls`)

# jldsave("a.jld2"; a)
# a2 = load("a.jld2")


# h5open("a.h5", "w") do f
#     for (i,v) in enumerate(a)
#         f["$(i)"]=Dict()
#         for (j,d) in enumerate(v)
#             write(f,"$(i)/$(j)",d)
#         end
#     end
# end

h5open("a.h5", "r") do f
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


v2 = Any[Any[2, 3, 4], Any[1, 4], Any[2, 4], Any[1, 5], Any[1, 4]]
m2 = Matrix{Any}(falses(5, 5))
for (i3, v3) in enumerate(v2)
    for v4 in v3
        m2[i3,v4] = true
    end
end
m2
