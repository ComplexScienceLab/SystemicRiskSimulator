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


## 初始设置 --------------
workAddress = getwd() # 获取工作路径

## 导入相关功能文件 -------------
source(str_c(workAddress,  "scripts/tools/useful_functions.R", sep = '/'))


## 导入实验后之数据文件 ----------------
folderpath_expdata <- "test/data" # 需要后续改进
folderpath_expprocess <- "test/data"
suffix_original <- "jld2"
suffix_import <- "hdf5"
fd_000 <- 
  get_folder_info(
    workAddress = workAddress,
    folder_source = folderpath_expdata,
    folder_target = folderpath_expprocess,
    suffix_source = suffix_original,
    suffix_target = suffix_import
  )

f_BB1jld2 <- fd_000$filePath_source[which(fd_000$fileNamesWithSuffix=="BB1.jld2")]
f_BI1h5 <- fd_000$filePath_source[which(fd_000$fileNamesWithSuffix=="BI1.h5")]

BB1 <- H5File$new(f_BB1jld2,mode = "r")
BI1h5 <- H5File.open(f_BI1h5,mode = "r")




# H5File$open()
BB1jld2

