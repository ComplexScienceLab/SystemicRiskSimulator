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
workaddress = getwd() # 获取工作路径



## 函数区 -----------
##+ 获取文件夹及其子文件信息 --------
get_folder_info <-
  function(workAddress,
           folder_source,
           folder_target,
           suffix_source,
           suffix_target) {
    rootPath_source <-
      str_c(workAddress,  folder_source, sep = '/') # 原始文件根路径
    rootPath_target <-
      str_c(workAddress, folder_target, sep = '/') # 目标文件根路径
    fileNamesWithSuffix <-
      dir(
        rootPath_source,
        all.files = F,
        full.names = F,
        no.. = T
      ) # 文件名含后缀名
    regularPattern <- str_c(".*[^(\\.", suffix_source, ")]")
    fileNames <-
      fileNamesWithSuffix %>% str_extract(pattern = regularPattern) # 纯文件名
    filePath_source <-
      dir(
        rootPath_source,
        pattern = "[^(\\~\\$)]",
        all.files = F,
        full.names = T,
        no.. = T
      ) # 文件名含后缀名
    filePath_target <-
      map2_chr(
        rootPath_target,
        str_c(fileNames, suffix_target, sep = '.') ,
        str_c,
        sep = '/',
        collapse = ','
      )   # 目标文件路径
    
    results <- list(
      "fileNames" =
        fileNames,
      "fileNamesWithSuffix" =
        fileNamesWithSuffix,
      "filePath_source" =
        filePath_source,
      "filePath_target" =  filePath_target
    )
    
    
  }


## 导入实验后之数据文件 ----------------
folderpath_original <- "data"
folderpath_import <- ""
suffix_original <- "jld2"
suffix_import <- "hdf5"
df_000 <- 
  get_folder_info(
    workAddress = workAddress,
    folder_source = folderpath_original
    folder_target = folderpath_import
    
  )





