#!/usr/bin/env python
# coding: utf-8

## #TODO 存在大量错误无法使用

# %% [markdown]
# # 预处理数据
# ## 导入安装包

# In[1]:


#
# This example writes data to the existing empty dataset created by h5_crtdat.py and then reads it back.
#
# from msilib.schema import Font

import os

import h5py
import numpy as np
import xlwings as xw
import openpyxl as xl
from openpyxl.cell.cell import Cell
import openpyxl.utils as xlutils
import pandas as pd
#
# Open an existing file using default properties.
#


# %% [markdown]
# ## 设置工作路径

# In[2]:


logging.info("start")
# os.chdir("/Users/ethan/LocalFiles/ResearchFile/SystemicRiskSimulator")
os.getcwd()
# root_path = os.getcwd()
root_path = "/"


# %% [markdown]
# ## 设置实验文件

# In[3]:


folder_exp = "test_20220527153746"
path_root_exp = os.path.join(root_path, "data/sims")
path_exp = os.path.join(path_root_exp, folder_exp)
folder_exp_output_data = "exp_output_data"
folder_exp_analyses = "analyses"
folderpath_exp_output_data = os.path.join(path_exp, folder_exp_output_data)
folderpath_exp_analyses = os.path.join(path_exp, folder_exp_analyses)
if not os.path.exists(folderpath_exp_analyses):
    os.makedirs(folderpath_exp_analyses)
filename_excel_exp_data = "exp_data.xlsx"
filepath_excel_exp_data = os.path.join(
    folderpath_exp_analyses, filename_excel_exp_data)
filename_exp_data_BB = "BB_exp=1.csv"
filepath_exp_data_BB = os.path.join(
    folderpath_exp_output_data, filename_exp_data_BB)



# %% [markdown]
# # Pandas处理整个数据

# ## 获取数据源

# In[ ]:


df_dataBB = pd.read_csv(filepath_exp_data_BB)



# %% [markdown]
# ## 排序数据列

# In[ ]:


# heads = df_dataBB.columns.values
# df_
# df_dataBB.drop('')
# heads["id"]


# %% [markdown]
# xwings创建实验后的Excel表格文件

# In[ ]:


wb = xw.Book()
wb.save(filepath_excel_exp_data)
ws = wb.sheets[0]
ws.name = "dataBB"
sheet_dataIB = wb.sheets.add(name="dataIB", after="dataBB")
wb.save(filepath_excel_exp_data)
wb.close()


# %% [markdown]
# # 处理dataBB

# ## 使用`openpyxl`

openpyxl打开已经建好的Excel表格文件


# %% [markdown]
# 加载工作簿
xlwb = xl.load_workbook(filepath_excel_exp_data)
# 获取sheet页
xlws = xlwb['dataBB']

# sheet_dataIB = wb_xl['dataIB']

# %% [markdown]
# ## 计算相关参数

num_cols = xlutils.column_index_from_string('CA')
num_rows = xlws.max_row
# cell010 = Cell(sheet_dataBB)


# %% [markdown]
# 冻结首行首列、更改单元格缩进、小数位数

# In[12]:


for i in xlws['A1':'CA1']:
    for j in i:
        j.alignment = xl.styles.Alignment(wrapText=True) # 单元格缩进
        
for i in xlws[]
xlws.freeze_panes = 'I2'  # 冻结首行首列


# %% [markdown]
# 设置单元格尺寸
# wb.active = True
xlws.row_dimensions[1].height = 40.0
xlws.columns['A:H']=8
xlws.column_dimensions['A':'H'].width = 20.0
xlws.column_dimensions['I':'CA'].width = 20.0
# sheet_dataBB['B2'].font=Font(
#     size=15,
#     color='FF000000',
# )




# In[14]:
xlwb.save(filepath_excel_exp_data)
xlwb.close()
xlwb = xl.load_workbook(filepath_excel_exp_data)


# %% [markdown]
# xwings打开已经建好的Excel表格文件

# In[15]:


app = xw.App(visible=True, add_book=False)
app.display_alerts = True # 显示Excel消息框
wb = app.books.open(filepath_excel_exp_data)
ws = wb.sheets["dataBB"]
# sheet_dataIB = wb.sheets["dataIB"]


# %% [markdown]
### ## 加载相关数据
# 表格载入pandas提供的数据

# In[ ]:


ws.range('A1').value = df_dataBB
wb.save(filepath_excel_exp_data)


# %% [markdown]
### ## 计算相关参数

# In[ ]:


num_rows = ws.range('A1:CA41').rows.count
num_cols = ws.range('A1:CA41').columns.count


# %% [markdown]
# ### ## 补全字段、设置字体

# In[ ]:


# sheet_dataBB.range('A1').resize(num_rows, num_cols).color = (255,255,255)
ws.range('A1').resize(num_rows, num_cols).color = None
ws.range('A1').resize(num_rows, num_cols).font.name = "Times"
ws.range('F1').value = "bankId"
ws.range('A1').value = "id"


# %% [markdown]
### ## 冻结首行首列

# In[ ]:


ws.api.FreezePanes = False
ws.api.SplitColumn = 3
ws.api.SplitRow = 3
ws.api.FreezePanes = True
wb.save()

# %% [markdown]
### ## 调整单元格宽高

# In[24]:


# sel_010=sheet_dataBB.range('A1:CE1')
# ws.range('A1').api.Font.Bold = True
ws['A1'].row_height = 60
c1 = ws['A1:CE1']
c1.api.WrapText = False
ws['A1'].resize(num_rows, num_cols).columns.autofit()
ws['A1:H1'].column_width = 4
ws['I1:CA1'].column_width = 8
ws.range('I2:CA41').number_format="0.00"
wb.save()

# sheet_dataBB.range('A1').resize(num_rows, num_cols).rows.autofit()
# sheet_dataBB.col()



# In[ ]:


api.



# %% [markdown]
# ## 退出处理Excel表格

# In[11]:


wb.save(filepath_excel_exp_data)
wb.close()
app.quit()


