"""
导入外部实验数据表格
"""

from SystemicRiskSimulator import pd

# 读取CSV文件
df = pd.read_csv('your_file.csv')

# 打印DataFrame的前几行
print(df.head())
