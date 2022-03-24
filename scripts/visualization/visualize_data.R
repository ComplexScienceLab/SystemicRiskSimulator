## 用前说明 -----
'"""
用于可视化待分析的银行数据。
"""'


## 导入包 -------
library(tidyverse)
library(igraph)

## 初始设置 --------------
workaddress = getwd() # 获取工作路径

test_data <- read_csv(str_c(workaddress,"data/test_data/test_data.csv",sep = '/'))

View(test_data)

adjm <- test_data %>% as.matrix() %>% t()
g1 <- graph_from_adjacency_matrix(
  adjm,
  mode = "directed",
  weighted = TRUE,
  # edge.label.dist=0.5
  )
g1 %>% plot()




