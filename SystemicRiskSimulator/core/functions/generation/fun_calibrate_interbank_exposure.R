# 这个脚本通过 py 文件调用，根据参数导入相关的总头寸的 CSV 文件，然后生成对应的网络。最后导出结果到 CSV 文件中。
# 其中的函数用于生成一个 ER 随机网络，其中每个节点的度数是 Poisson 分布，平均度数为 mu。
# 生成的网络是一个邻接矩阵，其中 A[i, j] = 1 表示个体 i 对个体 j 提供贷款。
# 生成的网络是一个随机网络，其中每个节点的度数是 Poisson 分布，平均度数为 mu。

if (!require(systemicrisk)) {
  install.packages("systemicrisk")
}
library(data.table)
library(optparse)

option_list <- list(
  make_option(c("-d", "--target-density"), type = "double", default = 0.45,
              help = "Target density for reconstructing the interbank exposure matrix"),
  make_option(c("-i", "--input-folder"), type = "character", default = "A_IB_all",
              help = "Input folder for the interbank asset vectories"),
  make_option(c("-o", "--output-file"), type = "character", default = "reconstructed_L.csv",
              help = "Output file for the reconstructed interbank exposure matrix"),
  make_option(c("-n", "--n-samples-calib"), type = "integer", default = 10,
              help = "Number of samples to generate during calibration"),
  make_option(c("-l", "--thin"), type = "integer", default = 100,
              help = "Thinning parameter for calibration")
)

opt <- parse_args(OptionParser(option_list = option_list))

calibrate_bank_exposure <- function(A_IB, Z_IB, target_density, n_samples_calib, thin) {

  # 调用 calibrate_ER 函数重构银行间资产负债矩阵
  model <- calibrate_ER(l = A_IB, a = Z_IB, targetdensity = target_density,
                        nsamples_calib = n_samples_calib, thin_calib = thin)

  # 使用重构的模型生成样本
  L_samples <- sample_HierarchicalModel(l = A_IB, a = Z_IB, model = model,
                                        nsamples = 1, thin = thin)

  return(L_samples)
}

A_IB_csv <- read.csv(file.path(opt$i, "A_IB_all.csv"), header = FALSE)
A_IB <- as.matrix(A_IB_csv)
Z_IB_csv <- read.csv(file.path(opt$i, "Z_IB_all.csv"), header = FALSE)
Z_IB <- as.matrix(Z_IB_csv)


output_file <- file.path(opt$o)

print(as.numeric(opt$d))
print(class(as.numeric(opt$d)))

L_samples <- calibrate_bank_exposure(A_IB, Z_IB, as.numeric(opt$d), as.numeric(opt$n), as.numeric(opt$l))  #BUG 传入的参数无法使用
# L_samples <- calibrate_bank_exposure(A_IB, Z_IB, 0.25,10,100)  #DEBUG 用于调试。

# 将重构后的银行间资产负债矩阵保存为 CSV 文件
fwrite(as.data.frame(L_samples), file = output_file, row.names = FALSE, col.names = FALSE)







