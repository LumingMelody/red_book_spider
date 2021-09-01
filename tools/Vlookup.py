import pandas as pd


def vlookup(filename):
    tableA = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_07_29\red_book_result.xlsx", index_col=0)
    tableB = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_07_29\user_note_url2.xlsx", index_col=0)
    print(tableB)
    dfb = tableB[['文章标题', '文章链接']]
    dfb.head()
    # to_match_hobby = tableA.merge(tableB, on="文章标题", how='right', )
    to_match_hobby = pd.merge(left=tableA, right=dfb, left_on="文章标题", right_on="文章标题")
    to_match_hobby.head()
    print(to_match_hobby)

    to_match_hobby.drop_duplicates(["文章链接"], keep="last", inplace=True)
    data = pd.DataFrame(to_match_hobby)
    data.to_excel(f"D:/red_book/red_book_51wom/red_book_07_29/{filename}.xlsx")


if __name__ == '__main__':
    file_name = "result"
    vlookup(file_name)
