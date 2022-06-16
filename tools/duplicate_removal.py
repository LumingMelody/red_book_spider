import pandas as pd


# 数据去重
def del_duplication(file_path):
    df = pd.read_excel(file_path)
    df.drop_duplicates(["地址"], keep="last", inplace=True)
    # print(df)
    data = pd.DataFrame(df)
    data.to_excel(r"./地址2.xlsx")


if __name__ == '__main__':
    file_path = r"./地址2.xlsx"
    del_duplication(file_path)
