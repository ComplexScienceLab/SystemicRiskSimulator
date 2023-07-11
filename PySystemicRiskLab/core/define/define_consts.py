"定义常量"

## 程序：定义常量


# from PySystemicRiskLab.core import np, env
pass  # end import

import numpy as np

from PySystemicRiskLab.core.define.define_environmentVariables import env

pass  # end import

FALSE1 = np.full((env['num_bank'], 1), False)  # 一维false布尔向量常量
FALSE2 = np.full((env['num_bank'], env['num_bank']), False)  # 二维方阵false布尔向量常量
TRUE1 = np.full((env['num_bank'], 1), True)  # 一维true布尔向量常量
TRUE2 = np.full((env['num_bank'], env['num_bank']), True)  # 二维方阵true布尔向量常量
BLANK1 = np.full(env['num_bank'], "")  # 一维空字符串向量常量
BLANK2 = np.full((env['num_bank'], env['num_bank']), "")  # 一维方阵空字符串向量常量
ZEROS1 = np.zeros((env['num_bank'], 1))  # 一维零向量常量
ZEROS2 = np.zeros((env['num_bank'], env['num_bank']))  # 二维方阵零向量常量
LESS1 = np.zeros((env['num_bank'], 1)) + 0.0001  # 一维接近零的正数向量常量
LESS2 = np.zeros((env['num_bank'], env['num_bank'])) + 0.0001  # 二维方阵接近零的正数常量
ONES1 = np.ones((env['num_bank'], 1))  # 一维幺向量常量
ONES2 = np.ones((env['num_bank'], env['num_bank']))  # 二维方阵幺向量常量
MISSING1 = np.full((env['num_bank'], 1), np.NaN)  # 一维缺失值向量常量
MISSING2 = np.full((env['num_bank'], env['num_bank']), np.NaN)  # 二维方阵确失值常量
NONE1 = np.empty((env['num_bank'], 1), dtype=object)  # 一维空向量常量
NONE2 = np.empty((env['num_bank'], env['num_bank']), dtype=object)  # 二维空向量常量
RANGE1 = np.arange(0, env['num_bank'], step=1)  # 一维步进向量常量（从0开始）
RANGE2 = np.arange(0, env['num_bank'] * env['num_bank'], step=1).reshape((env['num_bank'], env['num_bank']))  # 二维方阵步进向量常量（从0开始）
