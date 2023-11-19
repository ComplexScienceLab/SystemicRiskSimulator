## 用前说明 -----
'"""
用于可视化待分析的银行数据。
"""'


## 导入包 -------
library(tidyverse)
library(igraph)

## 初始设置 --------------
workaddress = getwd() # 获取工作路径

data <- read_csv(str_c(workaddress,"data/sims/test_20230305113140_2023-03-05/exp_output_data/IB_exp=1.csv",sep = '/'))

View(data)

data <- select(data,-1)

View(data)

cols<-colnames(data)

View(cols)

new_cols <- c(cols[which(cols=="row")],cols[which(cols=="col")], cols[length(cols)], cols[2:(length(cols) - 1)])

df <- df[, new_cols]

adjm <- data %>% as.matrix() %>% t()
g1 <- graph_from_adjacency_matrix(
  adjm,
  mode = "directed",
  weighted = TRUE,
  # edge.label.dist=0.5
  )
g1 %>% plot()


## 以下由ChatGPT生成
# library(igraph)

# data <- read.csv("data.csv", header=TRUE)
# g <- graph.data.frame(data)

# plot(g)

# plot(g, vertex.color="red", vertex.shape="rectangle")

# plot(g, edge.color="blue", edge.width=2)

