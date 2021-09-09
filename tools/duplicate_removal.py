import pandas as pd


# 数据去重
def del_duplication(file_path):
    df = pd.read_excel(file_path)
    df.drop_duplicates(["评论内容"], keep="last", inplace=True)
    # print(df)
    data = pd.DataFrame(df)
    data.to_excel(r"C:\Users\luming\Desktop\小红书评论\我的超能武器\我的超能武器(去重).xlsx")


if __name__ == '__main__':
    file_path = r"C:\Users\luming\Desktop\小红书评论\我的超能武器\我的超能武器_result.xlsx"
    del_duplication(file_path)
