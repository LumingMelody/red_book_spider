import time
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

if __name__ == '__main__':
    try:
        xhs = WhosecardXhsSpider()
        user_id = "5eafb89d0000000001001005"
        r = xhs.get_user_notes(user_id, page=1)
        print(r)
        total_notes_count = r['result']['data']['total_notes_count']
        if total_notes_count % 10 == 0:
            page_total = total_notes_count / 10
        else:
            page_total = int(total_notes_count / 10) + 1
        for i in range(1, page_total+1):
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
                if 1609430400 <= time_ts <= 1641780262:
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
                        ws.append([note_user, note_url, note_desc, note_title, note_create_time, note_like_count, note_coll_count,
                                   note_comments_count])
                        wb.save(r"D:\red_book\red_book_51wom\red_book_22_1月\red_book_01_10\red_book_欧尚.xlsx")
                    except Exception as a:
                        print(a)
                else:
                    print("跳出")
                    break

    except Exception as e:
        print(e)
