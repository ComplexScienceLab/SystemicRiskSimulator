"""
@File   : draft2022-06-23.py
@Author : Ethan Lin
@Date   : 2022/06/23
@Desc   : 
"""
import itertools
import numpy as np, pandas as pd


class class1:
    d = dict(a=['a1', 'a2'], b=['b1', 'b2'], c=['c1'])
    l = list(d.values())
    pass


product_list = list(itertools.product(*class1.l, repeat=1))
pdl = []
for i, v in enumerate(product_list):
    pdl.append(dict(zip(class1.d.keys(), v)))
npdl = np.asarray(product_list)
df_product_list = pd.DataFrame(npdl, columns=class1.d.keys())

class1.d['dataBB']={'d1':[1,2,3],'d2':[1,1,1],'d3':[0,0,0]}
