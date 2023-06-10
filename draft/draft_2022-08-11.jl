## 加载外部工具包
using DrWatson
@quickactivate "SystemicRisk" # 快速激活本项目

# 定义结构体
mutable struct St
    s1::Int64
    s2::Int64
end

# 生成命名元组
st1 = (s1=10, s2=20)

# 实例化结构体
st2 = St(0, 0)

# 获取结构体成员名列表
d=@dict(s1=10,s2=20)

fieldNames = fieldnames(St)

# 遍历成员名，设置以字典值
for (i, v) in enumerate(fieldNames)
    setfield!(st2, v, a[v])
end

# 获取命名元组成员名列表
fieldNames = keys(d)

# 遍历成员名，设置以命名元组值
for fieldName in fieldNames
    setfield!(st2, fieldName, st1[fieldName])
end
st2
st2.s1=233
st2

# 命名元组转字典
d_st1=Dict(pairs(st1))

# 字典值可以被修改
d_st1[:s1]=666

