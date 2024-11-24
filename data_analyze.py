import pandas as pd

file_path = 'result/arxiv论文_20241124_201607.csv'

# 读取csv文件
df = pd.read_csv(file_path)

# 将first_submitted_date转换为日期格式
df['first_submitted_date'] = pd.to_datetime(df['first_submitted_date'])

# 创建一个新的列quarter表示季度
df['quarter'] = df['first_submitted_date'].dt.to_period('Q')

# 筛选出2023-1-1到2024-12-12之间的数据
df = df[(df['first_submitted_date'] >= '2023-01-01') & (df['first_submitted_date'] <= '2024-12-12')]

# 统计每个季度的论文数量
quarterly_counts = df['quarter'].value_counts().sort_index()

print(quarterly_counts)