import time

import pandas as pd
from openpyxl import Workbook

from red_erp.whosecard_open_platform import WhosecardXhsSpider

wb = Workbook()
ws = wb.active
ws.append([
    "用户名",
    "文章链接",
    "笔记内容",
    "笔记标题",
    "笔记发布时间",
    "笔记点赞数",
    "笔记收藏数",
    "笔记评论数",
])


def get_user_his(user_id):
    r = xhs.get_user_notes(user_id, page=1)
    print(user_id)
    # print(r)
    total_notes_count = r['result']['data']['total_notes_count']
    print(total_notes_count)
    if total_notes_count % 10 == 0:
        page_total = total_notes_count / 10
    else:
        page_total = int(total_notes_count / 10) + 1
    for i in range(1, int(page_total + 1)):
        try:
            result = xhs.get_user_notes(user_id, page=i)
            notes = result['result']['data']['notes']
        except Exception as b:
            print(b)
        for note in notes:
            note_id = note['id']
            ts_str = note_id[0: 8]
            time_ts = int(ts_str, 16)
            print(time_ts)
            if 1647014400 <= time_ts <= 1652342305:
                note_title = note['title']
                note_user = note['user']['nickname']
                try:
                    note_result = xhs.get_note_detail(note_id)
                    note_url = f"https://www.xiaohongshu.com/discovery/item/{note_id}"
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
                    ws.append(
                        [note_user, note_url, note_desc, note_title, note_create_time, note_like_count, note_coll_count,
                         note_comments_count])
                    wb.save(rf"./data/{note_user}.xlsx")
                    time.sleep(2)
                except Exception as a:
                    print(a)
            else:
                print("跳出")
                break


if __name__ == '__main__':
    # try:
    xhs = WhosecardXhsSpider()
    df = pd.read_excel(r'./red_urls.xlsx')
    # user_id = "5eafb89d0000000001001005"
    urls = df['主页链接']
    user_name = df['用户名']
    for index, url in enumerate(urls):
        if '?' in url:
            user_id = url.split('/')[-1].split('?')[0]
        else:
            user_id = url.split('/')[-1]
        get_user_his(user_id)
    # except Exception as e:
    #     print(e)
