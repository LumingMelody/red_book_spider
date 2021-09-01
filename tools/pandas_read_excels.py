import os
import pandas as pd

dfs = pd.DataFrame()
# os.walk(file_path) 深度遍历file_path下的所有子文件夹及文件
for root_dir, sub_dir, files in os.walk(r"C:\Users\luming\Desktop\15分钟出门挑战"):
    for file in files:
        if file.endswith(".xlsx"):
            # 构造绝对路径
            file_name = os.path.join(root_dir, file)
            # 读取sheet页
            # pd.read_excel(file_path,sheet_name=None).keys()获取excel表格所有的sheet页名称
            for sheet in pd.read_excel(file_name, sheet_name=None).keys():
                df = pd.read_excel(file_name, sheet_name=sheet)
                excel_name = file.replace(".xlsx", "")
                # 新增两列用于记录数据所属excel及sheet页，这一步骤感觉很有用，因为后续数据清理的时候，遇到莫名其妙的数据不知道怎么办的话，还可以去源excel表格上看下。
                df["excel_name"] = excel_name
                df["sheet_name"] = sheet
                dfs = pd.concat([dfs, df])
                print(dfs)
            dfs.to_excel(r"C:\Users\luming\Desktop\15分钟出门挑战\15分钟出门挑战_1.xlsx")
