import requests
from bs4 import BeautifulSoup
import csv

# 请求网页
def get_valid_date():
    while True:
        print("请输入你要寻找的新番表的年份和月份（需要晚于22年7月）：")
        year = input("年份：").zfill(2)
        month = input("月份：").zfill(2)

        if not (month in ['01', '04', '07', '10']):
            print("月份只能为1，4，7，10这四个数，请重新输入。")
            continue

        year_int = int(year)
        month_int = int(month)

        if year_int < 22 or (year_int == 22 and month_int <= 7):
            print("输入的日期必须晚于22年7月，请重新输入。")
            continue

        return year, month


year, month = get_valid_date()
url = 'https://yuc.wiki/20' + year + month
response = requests.get(url)
response.encoding = 'utf-8'  # 根据需要设置编码
html = response.text
# print(html)

# 解析网页
soup = BeautifulSoup(html, 'html.parser')

# 提取符合条件的部分
data_list = []
for td in soup.find_all('td'):
    if td.get('colspan') in ['2', '3'] and (
        'date_title' in td.get('class', []) or
        'date_title_' in td.get('class', []) or
        'date_title__' in td.get('class', [])
    ):
        text = td.get_text(separator='', strip=True)
        data_list.append(text)

# 将结果写入CSV文件
csv_file = year + '年' + month + '月新番.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # writer.writerow(['Extracted Text'])  # 写入表头
    for item in data_list:
        writer.writerow([item])
#
print(f"Data extracted and saved to {csv_file}")
