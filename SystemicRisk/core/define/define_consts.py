"定义常量"

## 程序：定义常量

##########################################
#状态/使用
##########################################


const FALSE1 = falses(env[:numBank]) # 一维false布尔向量常量
const FALSE2 = falses(env[:numBank], env[:numBank]) # 二维方阵false布尔向量常量
const TRUE1 = trues(env[:numBank]) # 一维true布尔向量常量
const TRUE2 = trues(env[:numBank], env[:numBank]) # 二维方阵true布尔向量常量
const BLANK1 = fill("", env[:numBank]) # 一维空字符串向量常量
const BLANK2 = fill("", env[:numBank], env[:numBank]) # 一维方阵空字符串向量常量
const ZEROS1 = zeros(env[:numBank]) # 一维零向量常量
const ZEROS2 = zeros(env[:numBank], env[:numBank]) # 二维方阵零向量常量
const LESS1 = zeros(env[:numBank]) .+ 0.01 # 一维接近零的正数向量常量
const LESS2 = zeros(env[:numBank], env[:numBank]) .+ 0.1 # 二维方阵接近零的正数常量
const ONES1 = ones(env[:numBank]) # 一维幺向量常量
const ONES2 = ones(env[:numBank], env[:numBank]) # 二维方阵幺向量常量
const NOTHING1 = fill(nothing, env[:numBank]) # 一维缺失值向量常量
const MISSING1 = fill(missing, env[:numBank]) # 一维缺失值向量常量
const MISSING2 = fill(missing, env[:numBank], env[:numBank]) # 二维方阵确失值常量
const RANGE1 = collect(range(1, env[:numBank], step=1)) # 一维步进向量常量