import pandas as pd


# 数据去重
def del_duplication(file_path):
    df = pd.read_excel(file_path)
    df.drop_duplicates(["发布链接"], keep="last", inplace=True)
    # print(df)
    data = pd.DataFrame(df)
    data.to_excel(r"./douyin_领克(去重).xlsx")


if __name__ == '__main__':
    file_path = r"./douyin_领克.xlsx"
    del_duplication(file_path)
