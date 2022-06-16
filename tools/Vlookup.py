import pandas as pd


def vlookup(filename):
    tableA = pd.read_excel(r"./小红书_杨枝甘露_05_19_result.xlsx", index_col=0)
    tableB = pd.read_excel(r"./test.xlsx", index_col=0)
    # print(tableB)
    # dfb = tableB.loc['用户链接', '用户名']
    # dfb.head()
    # to_match_hobby = tableA.merge(tableB, on="文章标题", how='right', )
    to_match_hobby = pd.merge(left=tableA, right=tableB, left_on="用户链接", right_on="用户链接")
    to_match_hobby.head()
    print(to_match_hobby)

    to_match_hobby.drop_duplicates(["文章链接"], keep="last", inplace=True)
    data = pd.DataFrame(to_match_hobby)
    data.to_excel(f"./{filename}.xlsx")


if __name__ == '__main__':
    file_name = "result"
    vlookup(file_name)
