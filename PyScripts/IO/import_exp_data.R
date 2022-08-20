## 用前说明 -----
'"""
用于导入实验后之数据。
尽量不要在实验进行中导入文件，以免造成不必要的差错。
"""'

## 导入包 --------------------------
## library(xlsx)
library(tidyverse) # 数据操作系列包集合
library(readxl) # 读写Excel
library(stringr) # 字符串
library(nycflights13) #
library(lubridate) # 操作日期时间
library(hdf5r) # 操作文件其HDF5格式
library(xlsx) # 操作


## 初始设置 --------------
workAddress = getwd() # 获取工作路径
exp_foldername="test_20220523175447" # 当前实验文件夹
folderpath_expoutputdata <- str_c("data/sims",exp_foldername,"exp_output_data",sep='/') # 导入数据文件夹
folderpath_expprocess <- str_c("data/sims",exp_foldername,"analyses",sep='/') # 导出过程文件夹
suffix_original <- "csv" # 导入数据格式
suffix_import <- "xlsx" # 导出数据格式

## 导入相关功能文件 -------------
source(str_c(workAddress,  "scripts/tools/useful_functions.R", sep = '/'))

## 设置相关变量操作文件 --------
dir.create(folderpath_expprocess) # 创建相关分析文件夹

fd_000 <- 
  get_folder_info(
    workAddress = workAddress,
    folder_source = folderpath_expoutputdata,
    folder_target = folderpath_expprocess,
    suffix_source = suffix_original,
    suffix_target = suffix_import
  )

f_BB <- fd_000$filePath_source[which(fd_000$fileNamesWithSuffix=="BB_exp=1.csv")]
f_BI <- fd_000$filePath_source[which(fd_000$fileNamesWithSuffix=="BI_exp=1.csv")]

## 导入实验后之数据文件 ----------------
BB_exp <- read_csv(f_BB)
BI_exp <- read_csv(f_BI)

## 