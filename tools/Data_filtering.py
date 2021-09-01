import pandas as pd
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    '评论内容'
])

df = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_8月\red_book_08_27\red_book_result_08_27.xlsx")
lst = ['夏天' '熬夜', '双萃', '精华', '抗老', '维稳', '娇韵诗双萃', '双萃精华', '娇韵诗双萃精华', '回购', '空瓶', '熬夜神器']
comments = df['文章内容']

# for i in lst:
for comment in comments:
    if '夏天' or '熬夜' or '双萃' or '精华' or '抗老' or '维稳' or '娇韵诗双萃' or '双萃精华' or '娇韵诗双萃精华' or '回购' or '空瓶' or '熬夜神器' in \
            comment:
        print(comment)
        ws.append([comment])
        wb.save(r"D:\red_book\red_book_51wom\red_book_8月\red_book_08_27\red_book_content_filter.xlsx")
