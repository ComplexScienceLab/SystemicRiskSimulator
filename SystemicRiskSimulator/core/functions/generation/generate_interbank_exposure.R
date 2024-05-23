# 这个方法用于生成一个 ER 随机网络，其中每个节点的度数是 Poisson 分布，平均度数为 mu。
# 生成的网络是一个邻接矩阵，其中 A[i, j] = 1 表示节点 i 和节点 j 之间有一条边。
# 生成的网络是一个随机网络，其中每个节点的度数是 Poisson 分布，平均度数为 mu。

library(systemicrisk)
library(data.table)

calibrate_bank_exposure <- function(A_IB, Z_IB, target_density, output_file, n_samples_calib = 10, thin = 100) {
  # 检查输入矩阵是否匹配
  if (nrow(A_IB) != ncol(Z_IB)) {
    stop("A_IB and Z_IB must have the same dimensions.")
  }

  # 调用 calibrate_ER 函数重构银行间资产负债矩阵
  model <- calibrate_ER(l = rowSums(A_IB), a = colSums(Z_IB), targetdensity = target_density,
                        nsamples_calib = n_samples_calib, thin_calib = thin)

  # 使用重构的模型生成样本
  L_samples <- sample_HierarchicalModel(l = rowSums(A_IB), a = colSums(Z_IB), model = model,
                                        nsamples = 1, thin = thin)

  # 将重构后的银行间资产负债矩阵保存为 CSV 文件
  fwrite(as.data.frame(L_samples$L[[1]]), file = output_file, row.names = FALSE, col.names = FALSE)

  # 返回 NULL,因为结果已经保存为 CSV 文件
  return(NULL)
}