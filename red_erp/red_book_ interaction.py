import pandas as pd
from openpyxl import Workbook
import requests
from red_erp.whosecard_open_platform import WhosecardXhsSpider
import time

wb = Workbook()
ws = wb.active
# ws.append([
#     "用户名",
#     "笔记链接",
#     "笔记内容",
#     "笔记标题",
#     "笔记发布时间",
#     "笔记点赞数",
#     "笔记收藏数",
#     "笔记评论数",
# ])
xhs = WhosecardXhsSpider()


def main(url):
    ws.append([
        "用户名",
        "笔记链接",
        "笔记内容",
        "笔记标题",
        "笔记发布时间",
        "笔记点赞数",
        "笔记收藏数",
        "笔记评论数",
    ])
    print(url)
    result = requests.get(url).json()
    print(result)
    if "result" in result.keys():
        notes = result['result']['data']['notes']
        for note in notes:
            # print(note)
            note_id = note['id']
            note_url = f"https://www.xiaohongshu.com/discovery/item/{note_id}"
            note_title = note['title']
            note_user = note['user']['nickname']
            note_result = xhs.get_note_detail(note_id)
            if note_result is not None:
                note_detail = note_result['result']['data'][0]['note_list'][0]
                note_desc = note_detail['desc']
                note_like_count = note_detail['liked_count']
                note_coll_count = note_detail['collected_count']
                note_comments_count = note_detail['comments_count']
                ts = note_detail['time']
                timeArray = time.localtime(ts)
                note_create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                print([note_user, note_desc, note_title, note_create_time, note_like_count,
                       note_coll_count, note_comments_count])
                ws.append([note_user, note_url, note_desc, note_title, note_create_time, note_like_count,
                           note_coll_count, note_comments_count])
        wb.save(f"D:/douyin/douyin_erp/douyin_8月/douyin_08_04/red_book{user}.xlsx")


if __name__ == '__main__':
    # try:
    df = pd.read_excel(r"D:\douyin\douyin_erp\douyin_8月\douyin_08_04\red_urls.xlsx")
    note_ids = df['文章ID']
    users = df['用户名']
    for index, note_id in enumerate(note_ids):
        user = users[index]
        # user_id = "5c908b4b000000001603aa61"
        one_url = f"http://whosecard.com:8081/api/xiaohongshu/user/notes?key=55b69c89f13291700c70b1c36a36a7611e25ea04058074072241fd46&user_id={note_id}&page=1"
        result = requests.get(one_url).json()
        total_notes_count = result['result']['data']['total_notes_count']
        if total_notes_count % 10 == 0:
            note_page = int(total_notes_count / 10)
        else:
            note_page = int(total_notes_count / 10) + 1
        for i in range(1, note_page + 1):
            url = f"http://whosecard.com:8081/api/xiaohongshu/user/notes?key=55b69c89f13291700c70b1c36a36a7611e25ea04058074072241fd46&user_id={note_id}&page={i}"
            main(url)
    # except Exception as e:
    #     print(e)
