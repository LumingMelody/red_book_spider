# # from threading import Timer
# import time
#
# #
# #
# # def hello():
# #     print("hello, world")
# #
# #
# # class RepeatingTimer(Timer):
# #     def run(self):
# #         while not self.finished.is_set():
# #             self.function(*self.args, **self.kwargs)
# #             self.finished.wait(self.interval)
# #
# #
# # t = RepeatingTimer(10.0, hello)
# # t.start()
# # import datetime
# #
# # today = datetime.date.today()
# # print(today)
#
#
# # ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#
#
# # ts = str(time.time()).split(".")[0]
# # print(ts)
#
# # encoding: utf-8
# import requests
# import json
# from pyecharts.charts import Pie
# from pyecharts import options as opts
# from pyecharts.charts import Radar
#
#
# # 获取官网英雄数据
# def request(url):
#     headers = {
#         "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)", }
#     res = requests.get(url, headers=headers)
#     return res
#
#
# def data_analysis(title, data):
#     res = {}
#     for hero in data:
#         if hero['%s' % title] not in res:
#             res[hero['%s' % title]] = hero['name']
#         else:
#             res[hero['%s' % title]] = res[hero['%s' % title]] + "," + hero['name']
#     print(res)
#     return res
#
#
# def draw_pie(title, attack):
#     columns, data = [], []
#     for k, v in attack.items():
#         columns.append(title + k + '级')
#         data.append(len(v.split(',')))
#         if k in ['1', '10']:
#             print(k, v)
#     pie = (
#         Pie()
#             # 以[(lable,value),(lable,value),(lable,value)......]形式传入数据。
#             .add(title, list(z for z in zip(columns, data)))
#             .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
#     )
#     pie.render('%s.html' % title)
#
#
# def draw_Radar():
#     from pyecharts.charts import Radar
#     radar = Radar()
#     # //由于雷达图传入的数据得为多维数据，所以这里需要做一下处理
#     radar_data = [[10, 10, 10, 10, 10]]
#     radar_data1 = [[2, 10, 3, 6, 3]]
#     radar_data2 = [[1, 8, 7, 5, 8]]
#
#     # //设置column的最大值，为了雷达图更为直观，这里的月份最大值设置有所不同
#     schema = [
#         ("物理", 100), ("魔法", 10), ("防御", 10), ("难度", 10), ("喜好", 10)
#     ]
#     # //传入坐标
#     radar.add_schema(schema)
#     radar.add("满分", radar_data)
#     # //一般默认为同一种颜色，这里为了便于区分，需要设置item的颜色
#     radar.add("安妮", radar_data1, color="#E37911")
#     radar.add("卡尔玛", radar_data2, color="#1C86EE")
#     radar.render()
#
#
# if __name__ == '__main__':
#     url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
#     res = request(url)
#     hero_message = json.loads(res.text)['hero']
#     # print(hero_message)
#
#     # 物理
#     attack = data_analysis('attack', hero_message)
#     draw_pie('物理', attack)
#
#     # 防御
#     defense = data_analysis('defense', hero_message)
#     draw_pie('防御', defense)
#
#     # 魔法
#     magic = data_analysis('magic', hero_message)
#     draw_pie('魔法', magic)
#
#     # 难度
#     difficulty = data_analysis('difficulty', hero_message)
#     draw_pie('难度', difficulty)
#
#     draw_Radar()
#

# print(8 >> 2)
# import json
#
# a = [{'a': 3, 'b': 4, 'c': '5'}]
# a = str(a).replace("]", "").replace("[", '')
# a = json.dumps(a)
# print(a)
# print(type(a))

# from openpyxl import Workbook
# import pandas as pd
#
# wb = Workbook()
# ws = wb.active
# ws.append([
#     "粉丝数"
# ])
# if __name__ == '__main__':
#     df = pd.read_excel(r"C:\python_project\dts-auto-brief\data\mweibo\展新时刻_微博_210925_211004_13851.xlsx")
#     fans = df['粉丝数']
#     for fan in fans:
#         if "万" in str(fan):
#             n_fans = fan.replace("万", "")
#             l_fans = float(n_fans) * 10000
#             ws.append([int(l_fans)])
#         else:
#             ws.append([int(fan)])
#     wb.save(r"C:\python_project\dts-auto-brief\data\mweibo\fans.xlsx")
import pandas as pd
from pyecharts.charts import Pie, Bar, Line, WordCloud
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
from pyecharts import options as opts

# bar = Bar()
# bar.add_xaxis(["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月"])
#
# bar.add_yaxis('自动化工单统计', ['755', '664', '1082', '692', '729', '941', '1131', '2022', '831', '760', '371'])
# # bar.render(path='erp.jpg')
# make_snapshot(snapshot, bar.render(), "automation_data.png")

df = pd.DataFrame({"分类": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月"],
                   "数据": [755, 664, 1082, 692, 729, 941, 1131, 2022, 831, 760, 371]})
# v1 = [18, 59, 26, 38, 9, 17]
x_data = df['分类'].tolist()
y_data = df['数据'].tolist()

line = Line()
line.add_xaxis(x_data)
line.add_yaxis("数据", y_data)
line.set_global_opts(title_opts=opts.TitleOpts(title="erp折线图", pos_top="48%"),
                     legend_opts=opts.LegendOpts(pos_top="48%"))
# c = (
#     Pie()
#         .add("", [list(z) for z in zip(x_data, y_data)])  # zip函数两个部分组合在一起list(zip(x,y))-----> [(x,y)]
#         .set_global_opts(title_opts=opts.TitleOpts(title="自动化工单统计"))  # 标题
#         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))  # 数据标签设置
# )
# make_snapshot(snapshot, line.render(), "erp_test.png")
# c.render("./erp.html")


data = [
    ("生活资源", "999"),
    ("供热管理", "888"),
    ("供气质量", "777"),
    ("生活用水管理", "688"),
    ("一次供水问题", "588"),

]
w = (
    WordCloud()
    .add(series_name="热点分析", data_pair=data, word_size_range=[6, 66])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
    .render("词云图.html")
)
# make_snapshot(snapshot, line.render(), "erp_test.png")
