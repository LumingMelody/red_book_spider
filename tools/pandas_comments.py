import pandas as pd
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    '包含关键词的评论',
])
# df = pd.read_excel(r'D:\douyin\douyin_erp\douyin_8月\douyin_08_31\手机的压迫感(去重).xlsx')
df = pd.read_excel(r'D:\bilibili\bilibili_08_30\小米平板5_comment.xlsx')
df = df.dropna(axis=0, how='any')
comments = df['评论内容']
# lst = ['小米MIX4', '全面屏', '国产', '小米', '120W', '充电快', '屏下摄像头', '全陶瓷', '探索未来', '疾速模式']
lst = ['小米', '小米平板5', '国产', '键盘', '1999元', '生产力工具', '大容量电池', '8600毫安', '刷新率', '双核8扬声器', '触控笔', '办公']

try:
    for comment in comments:
        for i in lst:
            if i in comment:
                ws.append([comment])
                print(comment)
            else:
                pass
except Exception as e:
    print(e)
# wb.save(r'D:\douyin\douyin_erp\douyin_8月\douyin_08_31\手机的压迫感_has_keyword.xlsx')
wb.save(r'D:\bilibili\bilibili_08_30\小米平板5_comment_has_keyword.xlsx')
