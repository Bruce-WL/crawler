import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

url = input("请输入url：")
headers = {
    'Cookie': 'arxiv_labs={%22sameSite%22:%22strict%22%2C%22expires%22:365}; browser=43.224.245.241.1729779029250714; arxiv-search-parameters="{\"order\": \"-announced_date_first\"\054 \"size\": \"50\"\054 \"abstracts\": \"show\"\054 \"date-date_type\": \"announced_date_first\"}"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

result = requests.get(url=url, headers=headers).content
soup = BeautifulSoup(result, 'html.parser')
arxiv_results = soup.find_all('li', class_='arxiv-result')

# 定义一个Paper类
class Paper:
    def __init__(self, url, title, first_submitted_date, subject, author, abstract):
        self.url = url
        self.title = title
        self.first_submitted_date = first_submitted_date
        self.subject = subject
        self.author = author
        self.abstract = abstract

# 创建一个列表，存放论文信息
papers = []

# 在result中遍历所有结果
for result in arxiv_results:

    # 提取论文标题
    paper_title = result.find("p", class_="title is-5 mathjax").get_text(strip=True)

    # 提取论文链接
    paper_url = result.find("p", class_="list-title is-inline-block").find("a").get("href")

    # 仅提取了第一个论文标签
    paper_subject = result.find("div", class_="tags is-inline-block").find("span").get("data-tooltip")

    # 提取论文作者，从authors后切片
    paper_author = result.find("p", class_="authors").get_text(strip=True)[8:]

    # 提取摘要，去掉摘要尾部的"△ Less"
    paper_abstrct = result.find("p", class_="abstract mathjax").get_text(strip=True).replace("△ Less", "")

    # 提取论文提交日期，并将其转换为标准格式"YY-MM-DD"
    paper_date = result.find("p", class_="is-size-7").get_text(strip=True) if result.find("p",
                                                                                          class_="is-size-7") else "No date"
    from datetime import datetime

    if "v1" in paper_date:
        # Submitted9 August, 2024; v1submitted 8 August, 2024; originally announced August 2024.
        # 注意空格会被吞掉，这里我们要找最早的提交日期
        v1 = paper_date.find("v1submitted")
        paper_date = paper_date[v1 + 12: paper_date.find(";", v1)]
    else:
        # Submitted8 August, 2024; originally announced August 2024.
        # 注意空格会被吞掉
        submit_date = paper_date.find("Submitted")
        paper_date = paper_date[submit_date + 9: paper_date.find(";", submit_date)]

    date = datetime.strptime(paper_date, "%d %B, %Y")
    # 格式化日期为字符串并打印
    formatted_date = date.strftime("%Y-%m-%d")

    # 创建Paper对象并添加到列表中
    papers.append(
        Paper(
            url=paper_url,
            title=paper_title,
            first_submitted_date=formatted_date,
            subject=paper_subject,
            author=paper_author,
            abstract=paper_abstrct,
        )
    )

# 创建一个列表存放论文信息
csv_list = []
for paper in papers:
    paper_info = paper.__dict__
    csv_list.append(paper_info)

# 创建一个csv文件,设置文件名前缀和格式
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
file_prefix = 'arxiv论文_'
file_format = file_prefix + current_time + '.csv'
file_path = os.path.join(os.path.abspath(os.path.join(file_format, os.pardir)), file_format)

# 定义CSV文件的字段名（列名）
fieldnames = ["title", "author", "subject", "abstract", "first_submitted_date", "url"]

with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # 写入表头
    writer.writeheader()

    # 写入数据行
    for row in csv_list:
        writer.writerow(row)

print("已保存到", file_path, file_format)

