import pandas as pd

table_a_name = input("请输入A表文件名：")

table_a_path = table_a_name + '.xlsx'

sheet_a_name = input("请输入A表中的sheet名称：")

table_a = pd.read_excel(table_a_path, sheet_name=sheet_a_name, converters={'订单号': str}).dropna(axis=1, how='all')

table_b_name = input("请输入B表文件名：")

table_b_path = table_b_name + ".xlsx"

sheet_b_name = input("请输入B表中的sheet名称：")

table_b = pd.read_excel(table_b_path, sheet_name=sheet_b_name, converters={'交易ID': str})

table_b_2 = table_b.groupby("交易ID").收入.sum().reset_index()

table_c = table_a.merge(right=table_b_2, how='left', left_on='订单号', right_on='交易ID')

table_c.to_excel('c.xlsx', index=False)
