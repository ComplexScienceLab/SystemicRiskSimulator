## 用前说明 -----
'"""
用于操作Wind数据库数据：资产负债表。
尽量关闭所有文档，其打开于所在的，且需要分析的文件夹。因为这样可能会产生不必要的临时文件。
"""'

## 导入包 --------------------------
## library(xlsx)
library(tidyverse) # 数据操作系列包集合
library(readxl) # 读写Excel
library(stringr) # 字符串
library(nycflights13) #
library(lubridate) # 操作日期时间


## 初始设置 --------------
workaddress = getwd() # 获取工作路径


## 导入相关功能文件 -------------
source(str_c(workaddress,"PyScripts/tools/useful_functions.R", sep = '/'))



## 转换xlsx导出为csv --------------------------------------------------------------
folderpath_original <-  "data/original_data/Wind数据库数据/资产负债表"
folderpath_import <-  "data/import_data/Wind数据库数据/资产负债表"
suffix_original <- "xlsx"
suffix_import <- "csv"
fd_000 <-
  get_folder_info(
    workAddress = workaddress,
    folder_source = folderpath_original,
    folder_target = folderpath_import,
    suffix_source = suffix_original,
    suffix_target = suffix_import
  )
map2(map(fd_000$filePath_source, read_excel),
     fd_000$filePath_target,
     write_csv) # 读取原始文件然后写出为目标文件



## 清洗csv文件 --------------------------------------------------------

#+ 导入数据 --------------------------------------------------------------------
folderpath_import <-  "data/import_data/Wind数据库数据/资产负债表"
folderpath_tibble <- "data/tibble_data/Wind数据库数据/资产负债表"
suffix_import <- "csv"
suffix_tiblle <- "csv"
fd_010 <-
  get_folder_info(
    workAddress = workaddress,
    folder_source =
      folderpath_import,
    folder_target = folderpath_tibble,
    suffix_source = suffix_import,
    suffix_target = suffix_tiblle
  ) # 获取文件夹信息
data_import <- map(fd_010$filePath_source, read_csv) # 导入csv数据
list_tb_import <- data_import %>% map(as_tibble) # 转换为tibble列表数据


#+ 转置表格 ------
list_tb_010 <- list_tb_import
list_tb_012 <- list()
list_tb_012 <- list_tb_010 %>% map(t) %>% map(as_tibble) # 转置表格



#+ 筛选各表各列除了非空列的 -------------
list_tb_020 <- list_tb_012
list_tb_022 <- list()
list_string_filed_020 <- get_fileds_info(list_tb_020)
for (i in 1:length(list_tb_020)) {
  cols_020 <- list_string_filed_020[[i]] %>% is.na() %>% which()
  list_tb_022[[i]] <- list_tb_020[[i]] %>% select(!cols_020)
}


#+ 重命名、筛选各表各字段，按照第一行表头，按照给定需要 ----------
list_tb_030 <- list_tb_022
list_tb_035 <- list_tb_030
list_string_filed_030 <- get_fileds_info(list_tb_030)
string_031 <- "资产：" # 各关键字段字符串
string_032 <- "资产总计"
string_033 <- "负债："
string_034 <- "　　负债合计"
string_035 <- "所有者权益(或股东权益)："
string_036 <- "　　归属于母公司所有者权益合计"
string_037 <- "　　所有者权益合计"
string_038 <- "负债及股东权益总计"
regexp_031 <- "^\\s\\s(.*)$" # 各正则表达式
regexp_032 <- string_032
regexp_033 <- "^\\s\\s(.*)$"
regexp_035 <- "^\\s\\s(.*)$"
regexp_038 <- string_038
string_replace_031 <- paste0(string_031, "\\1") # 各替换字符串
string_replace_032 <- paste0(string_031, string_032)
string_replace_033 <- paste0(string_033, "\\1")
string_replace_035 <- paste0("所有者权益：", "\\1")
string_replace_038 <- paste0("所有者权益：", string_038)
for (i in 1:length(list_tb_030)) {
  pos_031 <-
    which(list_string_filed_030[[i]] == string_031) # 各关键字段字符串位置
  pos_032 <- which(list_string_filed_030[[i]] == string_032)
  pos_033 <- which(list_string_filed_030[[i]] == string_033)
  pos_034 <- which(list_string_filed_030[[i]] == string_034)
  pos_035 <- which(list_string_filed_030[[i]] == string_035)
  pos_036 <- which(list_string_filed_030[[i]] == string_036)
  pos_037 <- which(list_string_filed_030[[i]] == string_037)
  pos_038 <- which(list_string_filed_030[[i]] == string_038)
  replaced_pos_031 <- c((pos_031 + 1):(pos_032 - 1)) # 各被替换位置
  replaced_pos_032 <- c(pos_032)
  replaced_pos_033 <- c((pos_033 + 1):(pos_034))
  replaced_pos_035 <- c((pos_035 + 1):(pos_038 - 1))
  replaced_pos_038 <- c(pos_038)
  replaced_031 <-
    list_tb_030[[i]][1, replaced_pos_031] %>% str_replace(pattern = regexp_031, replacement = string_replace_031) # 各被替换文本
  replaced_032 <-
    list_tb_030[[i]][1, replaced_pos_032] %>% str_replace(pattern = regexp_032, replacement = string_replace_032)
  replaced_033 <-
    list_tb_030[[i]][1, replaced_pos_033] %>% str_replace(pattern = regexp_033, replacement = string_replace_033)
  replaced_035 <-
    list_tb_030[[i]][1, replaced_pos_035] %>% str_replace(pattern = regexp_035, replacement = string_replace_035)
  replaced_038 <-
    list_tb_030[[i]][1, replaced_pos_038] %>% str_replace(pattern = regexp_038, replacement = string_replace_038)
  list_tb_030[[i]][1, replaced_pos_031] <-
    as.list(replaced_031) # 各重命名
  list_tb_030[[i]][1, replaced_pos_032] <- as.list(replaced_032)
  list_tb_030[[i]][1, replaced_pos_033] <- as.list(replaced_033)
  list_tb_030[[i]][1, replaced_pos_035] <- as.list(replaced_035)
  list_tb_030[[i]][1, replaced_pos_038] <- as.list(replaced_038)
  cols_035 <-
    c(1:pos_031,
      pos_033,
      pos_035,
      (pos_038 + 1):length(list_string_filed_030[[i]])) # 各列之位置之于无用字段
  list_tb_035[[i]] <- list_tb_030[[i]][, -cols_035] # 筛选需要的各列组成新表
}




#+ 生成字段（设置列名）-------------
list_tb_040 <- list_tb_035
for (i in 1:length(list_tb_040)) {
  colnames(list_tb_040[[i]]) <-
    list_tb_040[[i]] %>% head(1) # 设置各表格之各列名
  list_tb_040[[i]] <- list_tb_040[[i]] %>% tail(-1) # 删除各表格头行
}


#+ 添加银行名称列、年份列
list_tb_050 <- list_tb_import
list_columeNames <- list_tb_050 %>% map(colnames)
list_years <- list()
for (i in 1:length(list_tb_050)) {
  list_years[[i]] <-
    list_columeNames[[i]][-1] %>% map(year) %>% unlist() # 获取各表年份信息
}
list_bankNames <- fd_010$fileNames # 获取银行名信息
list_tb_051 <- list_tb_040
for (i in 1:length(list_tb_040)) {
  list_tb_051[[i]] <-
    list_tb_051[[i]] %>% add_column("银行" = rep(list_bankNames[[i]], times = nrow(list_tb_051[[i]])),
                                    .before = "资产：现金及存放中央银行款项") # 添加字段“银行”
  list_tb_051[[i]] <-
    list_tb_051[[i]] %>% add_column("年份" = (list_years[[i]]), .before = "资产：现金及存放中央银行款项") # 添加字段“年份”
}


# 合并所有表格为一张大表 -----------------
list_tb_060 <- list_tb_051
tb_balanceSheet <- NULL
tb_balanceSheet <- bind_rows(list_tb_060)

# 预处理全表 ------
#+ 剔除表格中存在的特殊字符
colnames(tb_balanceSheet) <- gsub("\u3000","",colnames(tb_balanceSheet))

# 保存各银行资产负债数据总表 --------
filename_tibble <- "各银行资产负债数据总表.csv"
filepath_tibble <-
  paste(folderpath_tibble, filename_tibble, sep = "/")
tb_balanceSheet %>% write_csv(filepath_tibble) # 保存

# 读取各银行资产负债数据总表 -----------
filename_tibble <- "各银行资产负债数据总表.csv"
folderpath_tibble <- "data/tibble_data/资产负债表"
filepath_tibble <-
  paste(folderpath_tibble, filename_tibble, sep = "/")
tb_balanceSheet_import <- filepath_tibble %>% read_csv()
