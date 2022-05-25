# %% [markdown]
# ## 导入安装包

# %%
#
# This example writes data to the existing empty dataset created by h5_crtdat.py and then reads it back.
#
import os

import h5py
import numpy as np
import xlwings as xw
import pandas as pd
#
# Open an existing file using default properties.
#


# %% [markdown]
# ## 设置工作路径

# %%
print("start")
os.chdir("/Users/ethan/LocalFiles/ResearchFile/SystemicRisk")
os.getcwd()
root_path = os.getcwd()

# %% [markdown]
# ## 设置实验文件

# %%
folder_exp = "test_20220523175447"
path_root_exp = os.path.join(os.getcwd(), "data/sims")
path_exp = os.path.join(path_root_exp, folder_exp)
folder_exp_analyses = "analyses"
path_exp_analyses = os.path.join(path_exp, folder_exp_analyses)
filename_excel_exp_data = "exp_data.xlsx"
filepath_excel_exp_data=os.path.join(path_exp_analyses,filename_excel_exp_data)

# %% [markdown]
# ## 创建实验后的Excel表格文件

# %%
# excelbook = xlwt.Workbook()
# sheet1=excelbook.add_sheet('sheet1')
# excelbook.save(filepath_excel_exp_data)

# %%
excelbook=xw.Book()
# with xw.App() as app:
#     excelbook = app.books['Book1']

# %%
excelbook.save(filepath_excel_exp_data)
#





