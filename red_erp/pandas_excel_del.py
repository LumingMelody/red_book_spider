import pandas as pd
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    "未抓取URL"
])
df1 = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_07_29\red_book_result.xlsx")
content1 = df1['文章标题']
df2 = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_07_29\user_note_url1.xlsx")
content2 = df2['文章标题']
urls = df2['文章链接']


# print(content1[0])
def main():
    while True:
        for index, c2 in content2.items():
            # print(index)
            i = 0
            # print(type(content1[i]))
            if content1[i] and c2 is not None and content1[i] and c2 is not float:
                if content1[i].strip() == c2.strip():
                    note_url = urls[index]
                    print(note_url)
                    ws.append([note_url])
                    i += 1
                    if i >= 8138:
                        break


if __name__ == '__main__':
    main()
    wb.save(r"D:\red_book\red_book_51wom\red_book_07_29\red_urls1.xlsx")
