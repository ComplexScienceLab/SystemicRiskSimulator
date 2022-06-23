"""
@File   : draft2022-06-23.py
@Author : Ethan Lin
@Date   : 2022/06/23
@Desc   : 
"""
import itertools
import numpy as np,pandas as pd

d=dict(a=['a1','a2'],b=['b1','b2'],c=['c1'])
l=list(d.values())
product_list=list(itertools.product(*l,repeat=1))
pdl=[]
for i,v in enumerate(product_list):
    pdl.append(dict(zip(d.keys(),v)))
npdl=np.asarray(product_list)
df_product_list=pd.DataFrame(npdl,columns=d.keys())