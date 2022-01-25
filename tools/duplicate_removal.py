import pandas as pd


# 数据去重
def del_duplication(file_path):
    df = pd.read_excel(file_path)
    df.drop_duplicates(["用户作品链接"], keep="last", inplace=True)
    # print(df)
    data = pd.DataFrame(df)
    data.to_excel(r"D:\douyin\douyin_erp\22_1_douyin\UNI星球_his(去重).xlsx")


if __name__ == '__main__':
    file_path = r"D:\douyin\douyin_erp\22_1_douyin\UNI星球_his.xlsx"
    del_duplication(file_path)
