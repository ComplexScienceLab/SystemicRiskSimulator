"定义常量"

## 程序：定义常量

##########################################
#状态/无用
##########################################

from SystemicRisk.core import np,env
pass  # end import



# const FALSE1 = np.full(env['num_bank'],False) # 一维false布尔向量常量
# const FALSE2 = np.full((env['num_bank'], env['num_bank']),False) # 二维方阵false布尔向量常量
# const TRUE1 = np.full(env['num_bank'],True) # 一维true布尔向量常量
# const TRUE2 = np.full((env['num_bank'], env['num_bank']),True) # 二维方阵true布尔向量常量
# const BLANK1 = np.full(env['num_bank'],"") # 一维空字符串向量常量
# const BLANK2 = fill("", env['num_bank'], env['num_bank']) # 一维方阵空字符串向量常量
# const ZEROS1 = np.zeros(env['num_bank']) # 一维零向量常量
# const ZEROS2 = np.zeros((env['num_bank'], env['num_bank'])) # 二维方阵零向量常量
LESS1 = np.zeros(env['num_bank']) + 0.01 # 一维接近零的正数向量常量
LESS2 = np.zeros((env['num_bank'], env['num_bank'])) + 0.1 # 二维方阵接近零的正数常量
# const ONES1 = np.ones(env['num_bank']) # 一维幺向量常量
# const ONES2 = np.ones(env['num_bank'], env['num_bank']) # 二维方阵幺向量常量
# const NOTHING1 = fill(nothing, env['num_bank']) # 一维缺失值向量常量
# const MISSING1 = fill(missing, env['num_bank']) # 一维缺失值向量常量
# const MISSING2 = fill(missing, env['num_bank'], env['num_bank']) # 二维方阵确失值常量
# const RANGE1 = collect(range(1, env['num_bank'], step=1)) # 一维步进向量常量