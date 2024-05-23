"""
根据 R 语言工具包 systemicrisk 之 函数 `default_clearing()` 重写的 Python 版本。功能一模一样。
参考源链接 [default_clearing](https://rdrr.io/cran/systemicrisk/man/default_clearing.html) 。
"""

import numpy as np
from scipy.optimize import linprog

def default_clearing(L, ea, el=0, alpha=1, beta=1):
    """
    Clearing Vector with Bankruptcy Costs

    Computes bank defaults for the clearing vector approach without and
    with bankruptcy costs (Eisenberg and Noe, 2001), (Rogers and Veraart, 2013).

    Without bankruptcy costs the approach of Eisenberg and Noe (2001)
    is used using a linear programme.  With bankruptcy costs, the
    implementation is based on the Greatest Clearing Vector Algorithm (GA),
    see Definition 3.6, Rogers & Veraart (2013).

    Parameters:
    L (numpy.array): Liabilities matrix
    ea (numpy.array): Vector of external assets
    el (numpy.array): Vector of external liabilities (default 0)
    alpha (float): 1-proportional default costs on external assets in [0, 1] (default to 1).
    beta (float): 1-proportional default costs on interbank assets in [0, 1] (defaults to 1).

    Returns:
    default (numpy.array): A vector indicating which banks default (1=default, 0= no default)
    y (numpy.array): The greatest clearing vector.
    """
    n = len(ea)
    c = np.concatenate((np.ones(n), np.zeros(n)))
    A_ub = np.block([
        [-np.eye(n), L],
        [-np.eye(n), -np.eye(n)]
    ])
    b_ub = np.concatenate((ea - alpha * el, np.zeros(n)))
    A_eq = np.block([np.zeros(n), L.T - beta * np.eye(n)])
    b_eq = np.zeros(n)
    bounds = [(0, None) for _ in range(2*n)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    x = res.x[:n]
    y = res.x[n:]
    default = (x < ea - el).astype(int)
    return default, y