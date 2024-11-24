# import ollama
# response = ollama.chat(model='qwen:4b', messages=[
#   {
#     'role': 'user',
#     'content': '翻译为中文：Nuance Matters: Probing Epistemic Consistency in CausalReasoning',
#   },
# ])
# print(response['message']['content'])

import pandas as pd
import ollama

# 读取CSV文件
df = pd.read_csv('result/arxiv论文_20241124_033915.csv')

# 创建一个空列表用于存储翻译后的标题
translated_titles = []

# 循环处理每一行的标题并翻译
for title in df['title']:
    translation = ollama.chat(model='qwen:4b', messages=[
        {
            'role': 'user',
            'content': "翻译为中文：" + title
        },
    ])
    translated_title = translation['message']['content']
    translated_titles.append(translated_title)

# 将翻译后的标题插入到新的列中
df['翻译后的标题'] = translated_titles

# 保存修改后的CSV文件
df.to_csv('result/arxiv论文_20241124_033915_translated.csv', index=False, encoding='utf-8-sig')

print("翻译并插入成功")

