
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





##+ 获取表头字段 ------------
get_fileds_info <- function(list_tibble) {
  list_string_field <- list()
  for (i in 1:length(list_tibble)) {
    list_string_field[[i]] <- list_tibble[[i]][1,] %>% as.character()
  }
  results <- list_string_field
}

