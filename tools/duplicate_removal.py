import pandas as pd


# 数据去重
def del_duplication(file_path):
    df = pd.read_excel(file_path)
    df.drop_duplicates(["评论内容"], keep="last", inplace=True)
    # print(df)
    data = pd.DataFrame(df)
    data.to_excel(r"D:\douyin\douyin_erp\douyin_8月\douyin_08_31\手机的压迫感(去重).xlsx")


if __name__ == '__main__':
    file_path = r"D:\douyin\douyin_erp\douyin_8月\douyin_08_31\手机的压迫感_1.xlsx"
    del_duplication(file_path)
