"定义常量"

## 程序：定义常量


pass  # end import

import numpy as np


pass  # end import


class CONST:
    """
    常量类

    包括常用的常量数组。其数组元素大小由初始化参数 num 指定。

    包括以下常量：

    - FALSE1: 一维false布尔向量常量；
    - FALSE2: 二维方阵false布尔向量常量；
    - TRUE1: 一维true布尔向量常量；
    - TRUE2: 二维方阵true布尔向量常量；
    - BLANK1: 一维空字符串向量常量；
    - BLANK2: 一维方阵空字符串向量常量；
    - ZEROS1: 一维零向量常量；
    - ZEROS2: 二维方阵零向量常量；
    - LESS1: 一维接近零的正数向量常量；
    - LESS2: 二维方阵接近零的正数常量；
    - ONES1: 一维幺向量常量；
    - ONES2: 二维方阵幺向量常量；
    - MISSING1: 一维缺失值向量常量；
    - MISSING2: 二维方阵确失值常量；
    - NONE1: 一维空向量常量；
    - NONE2: 二维空向量常量；
    - RANGE1: 一维步进向量常量（从0开始）；
    - RANGE2: 二维方阵步进向量常量（从0开始）；

    """

    @classmethod
    def __init__(cls, num):
        cls.FALSE1 = np.full((num, 1), False)  # 一维false布尔向量常量
        cls.FALSE2 = np.full((num, num), False)  # 二维方阵false布尔向量常量
        cls.TRUE1 = np.full((num, 1), True)  # 一维true布尔向量常量
        cls.TRUE2 = np.full((num, num), True)  # 二维方阵true布尔向量常量
        cls.BLANK1 = np.full(num, "")  # 一维空字符串向量常量
        cls.BLANK2 = np.full((num, num), "")  # 一维方阵空字符串向量常量
        cls.ZEROS1 = np.zeros((num, 1))  # 一维零向量常量
        cls.ZEROS2 = np.zeros((num, num))  # 二维方阵零向量常量
        cls.LESS1 = np.zeros((num, 1)) + 0.0001  # 一维接近零的正数向量常量
        cls.LESS2 = np.zeros((num, num)) + 0.0001  # 二维方阵接近零的正数常量
        cls.ONES1 = np.ones((num, 1))  # 一维幺向量常量
        cls.ONES2 = np.ones((num, num))  # 二维方阵幺向量常量
        cls.MISSING1 = np.full((num, 1), np.NaN)  # 一维缺失值向量常量
        cls.MISSING2 = np.full((num, num), np.NaN)  # 二维方阵确失值常量
        cls.NONE1 = np.empty((num, 1), dtype=object)  # 一维空向量常量
        cls.NONE2 = np.empty((num, num), dtype=object)  # 二维空向量常量
        cls.RANGE1 = np.arange(0, num, step=1)  # 一维步进向量常量（从0开始）
        cls.RANGE2 = np.arange(0, num * num, step=1).reshape((num, num))  # 二维方阵步进向量常量（从0开始）
        pass  # end init

    pass  # end class
