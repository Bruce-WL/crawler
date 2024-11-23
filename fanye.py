import pandas as pd
import matplotlib.pyplot as plt

file_path = 'result/arxiv论文_20241124_033915.csv'

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

# 绘制柱形图
plt.figure(figsize=(10, 6))  # 设置图形大小
plt.bar(quarterly_counts.index.astype(str), quarterly_counts.values, color='skyblue')  # 绘制柱形图
plt.xlabel('Quarter')  # 设置x轴标签
plt.ylabel('Number of Papers')  # 设置y轴标签
plt.title('Quarterly Paper Submission Counts')  # 设置图形标题
plt.xticks(rotation=45)  # 设置x轴标签旋转角度，以便更好地显示
plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域
plt.show()  # 显示图形

print(quarterly_counts)