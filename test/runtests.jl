## temp文件

##########################################
#用途/草稿；
#状态/进行；
##########################################

# include("defineType.jl")

# st = Union{Int64,String,Float64}

# mutable struct s{st}
#     s1::st
#     s2::st
#     s3::st
# end

# mutable struct s{Union{Int64,String,Float64}}
#     s1::{T}
#     s2::{T}
#     s3::{T}
# end

# vec_a=fill(s{st}(1," ",2.0),10)

# vec_a.s2="hello"

# println(vec_a)

# # 定义结构体S1
# Id=Array{Int64}
# mutable struct S1
#     id::Id
# end

# s1=S1([1 2 3])
# println(typeof(s1))

# # 定义结构体S2，继承S1
# Name=String
# mutable struct S2
#     s1::S1
#     name::Name
# end

# s2=S2(s1,"Julia")
# println(s2)
# println(typeof(s2.s1))



# fill(1,10)




# using DataFrames
# df = DataFrame(A = 1:4, B = ["M", "F", "F", "M"])
# println(df)


# mutable struct A
#     a1::Float64
#     a2::Float64
#     a3::Float64 # a3=a1^2+a2^2
# end

# x3 = sumSquare(x1, x2) = x1^2 + x2^2

# x1 = 3;x2 = 4;x3 = 0

# A010 = A(x1, x2, sumSquare(x1, x2))
# A020 = A(x1, x2, x3)

# 间接实现结构体方法的几种方式：

# ## 方式1

# mutable struct A
#     a1
#     a2
#     # 希望定义a3=a1^2+a2^2 .
# end

# function a3(x::A)
#     x.a1^2 + x.a2^2
# end

# println(A(1, 2))

# println(sumSquare(A(1, 2)))

# ## 方式2

# mutable struct B
#     b1
#     b2
#     b3 # 希望定义b3=b1^2+b2^2 .
# end

# function B(x1, x2) # 这里实际上是函数B，只是同名于结构体B，建议写成不同名。
#     B(x1, x2, x1^2 + x2^2)
# end

# B1 = B(1, 2)

# println(B1)

# ## 方式3

# mutable struct E
#     e1
#     e2
#     e3 # 希望定义e3=e1^2+e2^2 .
# end

# function E_e3(s1, s2)
#     s1^2 + s2^2
# end

# function E(x1, x2) # 这里实际上是函数E，只是同名于结构体E，建议写成不同名。
#     E(x1, x2, e3(x1, x2))
# end

# E1 = E(1, 2)

# println(E1)


# mutable struct E
#     e1
#     e2
#     e3 # 希望定义e3=e1^2+e2^2 .
# end

# function update_e1(o::E)
#     o.e1=10000
#     return o.e1
# end

# function update_e2(e2::E.e2)
#     e2=10000
#     return e2
# end

# e=E(1,2,3)
# println("e1=$(e.e1)\ne2=$(e.e2)\ne3=$(e.e3)\n")
# update_e1(e)
# println("e1=$(e.e1)\ne2=$(e.e2)\ne3=$(e.e3)\n")
# update_e2(e.e2)
# println("e1=$(e.e1)\ne2=$(e.e2)\ne3=$(e.e3)\n")


# bi = Bool.([1 1 0; 0 0 1; 1 1 0])
# bi
# br = Bool.([0, 1, 1])
# br
# setbr = findall(br .== 1)
# setbi = findall(bi .== 1)
# (br .&& bi)
# findall(br .&& bi)
# x = reshape(1:9, (3, 3)) * 10
# v = sum(x, dims = 1)'
# for i in (findall(br .&& bi))
#     println(x[i])
# end
# a3 = Dict([])
# for i in findall(br)
#     a3[i]=findall(bi[i, :])
# end
# a3
# function update(br,shock)
#     br_old = br
#     br = shock
#     println(br)
#     println(br_old)
#     if br != br_old
#         println("change")
#     else
#         println("unchange")
#     end
# end

# TypeIds = Matrix{Int64} # 向量编号类型
# TypeNames = Matrix{String} # 向量名称类型
# mutable struct S
#     id::TypeIds
#     name::TypeNames
# end
# s=S(
#     reshape(range(1, 5, step = 1), (5, 1)),
#     fill("", 5, 1)
# )


# ## 定义类型
# TypeIds{NDIMS} = Array{Int64,NDIMS} # 向量编号类型
# TypeAbbrs{NDIMS} = Array{String,NDIMS} # 向量缩写类型
# TypeNames{NDIMS} = Array{String,NDIMS} # 向量名称类型
# TypeMoney{NDIMS} = Array{Float64,NDIMS} # 向量资金类型
# TypeState{NDIMS} = Array{Bool,NDIMS} # 一维向量状态类型

# ## 定义参数
# mutable struct P
#     init_method::String # 初始化方法
#     num_bank::Int64 # 银行个数
#     num_assets::Int64 # 资产总类数
#     max_num_tau::Int64 # 最大传染轮次数
#     theta_Shock_exBI::Float64 # 外生冲击类型占比
#     set_Shock_exB::Vector # 指定遭受初始外生冲击的银行示性列表
# end


# ## 初始化参数
# p = P("", 0, 0, 0, 0, []) # 初始化参数结构体
# dict_initMethods = Dict([(0, "only init"), (1, "randomly"), (2, "import data"), (3, "set manually")]) # 字典之于初始化数据方式


# ## 定义常量
# const FALSE1 = falses(num_bank) # 一维false布尔向量常量
# const FALSE2 = falses(num_bank, num_bank) # 二维方阵false布尔向量常量
# const TRUE1 = trues(num_bank) # 一维true布尔向量常量
# const TRUE2 = trues(num_bank, num_bank) # 二维方阵true布尔向量常量
# const BLANK1 = fill("", num_bank) # 一维空字符串向量常量
# const BLANK2 = fill("", num_bank, num_bank) # 一维方阵空字符串向量常量
# const ZEROS1 = zeros(num_bank) # 一维零向量常量
# const ZEROS2 = zeros(num_bank, num_bank) # 二维方阵零向量常量
# const LESS1 = zeros(num_bank) .+ 0.1 # 一维接近零的正数向量常量
# const LESS2 = zeros(num_bank, num_bank) .+ 0.1 # 二维方阵接近零的正数常量
# const ONES1 = ones(num_bank) # 一维幺向量常量
# const ONES2 = ones(num_bank, num_bank) # 二维方阵幺向量常量
# const MISSING1 = fill(missing, num_bank) # 一维缺失值向量常量
# const MISSING2 = fill(missing, num_bank, num_bank) # 二维方阵确失值常量


# ## 设置参数
# init_method = dict_initMethods[3] # 初始化银行数据方式
# num_bank = 5 # 银行个数
# num_assets = 3 # 资产种类数
# max_num_tau = 10 # 最大传染轮次数
# theta_Shock_exBI = 1.0 # 外生冲击类型占比
# set_Shock_exB = [1] # 指定遭受初始外生冲击的银行示性集合

# ## 定义结构
# mutable struct BC{NDIMS}
#     id::TypeIds{NDIMS} # 编号
#     abbr::TypeAbbrs{NDIMS} # 缩写
#     name::TypeNames{NDIMS} # 全名
#     A_all::TypeMoney{NDIMS} # 总资产
#     Z_all::TypeMoney{NDIMS} # 总负债
#     BI_A::TypeMoney{2} # 银行间资产
#     isOn::TypeState{NDIMS} # 示性向量之于银行是否存在
#     listOfExist::Array{Any} # 列表之于存在的银行编号
# end

# ## 定义初始化函数
# function init_B()
#     bank = BC{1}(
#         range(1, num_bank, step = 1), # 编号
#         ["1", "2", "3", "4", "5"], # 缩写
#         ["BK1", "BK2", "BK3", "BK4", "BK5"], # 全名
#         ZEROS1, # 总资产
#         ZEROS1, # 总负债
#         [0 1728.55 0 134.46 322.23; 109.35 0 289.02 0 0; 730.99 0 0 0 0; 119.26 115.69 964.32 0 158.48; 0 0 0 2717.39 0], #  银行间资产
#         trues(num_bank), # 示性向量之于银行是否存在
#         [] # 列表之于存在的银行编号
#     )
#     return bank
# end
# ## 定义初始化函数
# function init_B()
#     bank = BC{1}(
#         range(1, num_bank, step = 1), # 编号
#         ["1", "2", "3", "4", "5"], # 缩写
#         ["BK1", "BK2", "BK3", "BK4", "BK5"], # 全名
#         zeros(num_bank), # 总资产
#         zeros(num_bank), # 总负债
#         [0 1728.55 0 134.46 322.23; 109.35 0 289.02 0 0; 730.99 0 0 0 0; 119.26 115.69 964.32 0 158.48; 0 0 0 2717.39 0], #  银行间资产
#         trues(num_bank), # 示性向量之于银行是否存在
#         [] # 列表之于存在的银行编号
#     )
#     return bank
# end

# # 初始化函数
# bb = init_B()

# println(bb)

# bb.A_all = sum(bb.BI_A, dims = 2)

# function transfer_B_captial!(; target, source)
#     target .= source[:]
#     source .= 0.0
#     return target, source
# end

# a = [1 2 3]
# b = [0 0 0]

# b[1:2], a[2:3] = transfer_B_captial!(target = b[1:2], source = a[2:3])

# a
# b



## 初始化参数
dict_initMethods = Dict([(0, "only init"), (1, "randomly"), (2, "import data"), (3, "set manually")]) # 字典之于初始化数据方式
init_method = dict_initMethods[3] # 初始化银行数据方式
num_bank = 5 # 银行个数
num_assets = 3 # 资产种类数
max_num_tau = 10 # 最大传染轮次数
theta_Shock_exBI = 1.0 # 外生冲击类型占比
set_Shock_exB = [1] # 指定遭受初始外生冲击的银行示性集合

## 定义类型
TypeIds{NDIMS1} = Array{Int16,NDIMS1} # 向量编号类型
TypeAbbrs{NDIMS1} = Array{String,NDIMS1} # 向量缩写类型
TypeNames{NDIMS1} = Array{String,NDIMS1} # 向量名称类型
TypeMoney{NDIMS2} = Array{Float32,NDIMS2} # 向量资金类型
TypeState{NDIMS2} = Array{Bool,NDIMS2} # 一维向量状态类型





## 定义常量
const FALSE1 = TypeState{1}(falses(num_bank)) # 一维false布尔向量常量
const FALSE2 = TypeState{2}(falses(num_bank, num_bank)) # 二维方阵false布尔向量常量
const TRUE1 = TypeState{1}(trues(num_bank)) # 一维true布尔向量常量
const TRUE2 = TypeState{2}(trues(num_bank, num_bank)) # 二维方阵true布尔向量常量
const BLANK1 = fill("", num_bank) # 一维空字符串向量常量
const BLANK2 = fill("", num_bank, num_bank) # 一维方阵空字符串向量常量
const ZEROS1 = TypeMoney{1}(zeros(num_bank)) # 一维零向量常量
const ZEROS2 = TypeMoney{2}(zeros(num_bank, num_bank)) # 二维方阵零向量常量
const LESS1 = TypeMoney{1}(zeros(num_bank) .+ 0.01) # 一维接近零的正数向量常量
const LESS2 = TypeMoney{2}(zeros(num_bank, num_bank) .+ 0.1) # 二维方阵接近零的正数常量
const ONES1 = TypeMoney{1}(ones(num_bank)) # 一维幺向量常量
const ONES2 = TypeMoney{2}(ones(num_bank, num_bank)) # 二维方阵幺向量常量
const MISSING1 = fill(missing, num_bank) # 一维缺失值向量常量
const MISSING2 = fill(missing, num_bank, num_bank) # 二维方阵确失值常量
const RANGE1 = range(1, num_bank, step = 1) # 一维步进向量常量




## 定义结构
mutable struct BC
    id::TypeIds{NDIMS1}
    abbr::TypeAbbrs{NDIMS1}
    name::TypeNames{NDIMS1}
    A_all::TypeMoney{NDIMS2}
    Z_all::TypeMoney{NDIMS2}
    isOn::TypeState{NDIMS2}
    listOfExist::Array{Any}
end

## 定义初始化函数
function init_B()
    bank = BC{1,1}(
        RANGE1, # 编号 id
        ["1", "2", "3", "4", "5"], # 缩写
        ["BK1", "BK2", "BK3", "BK4", "BK5"], # 全名
        # reshape([1.0, 2.0, 3.0, 4.0, 5.0], (num_bank, 1)),
        # reshape([6.0, 7.0, 8.0, 9.0, 10.0], (num_bank, 1)),
        ZEROS1,
        ZEROS1,
        TRUE1,
        []
    )
    return bank

end

# 初始化函数
BB = init_B()

println(BB)

println(BB.A_all)

BB.Z_all=BB.A_all
BB.A_all=ONES1

println(BB.A_all,"\n",BB.Z_all)
println(pointer(BB.A_all),"\n",pointer(BB.Z_all))




mutable struct S
    s1::Vector
    s2::Vector
end

S1=S([1,2,3],[4,5,6])

for i in fieldnames(S)
    x=getfield(S1,i)
    end

df=DataFrame(
    for i in fieldnames(S)
        x=getfield(S1,i)
    end
)