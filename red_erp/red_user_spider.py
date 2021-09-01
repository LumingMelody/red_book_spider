import time
from openpyxl import Workbook

from red_erp.whosecard_open_platform import WhosecardXhsSpider

wb = Workbook()
ws = wb.active
ws.append([
    "用户名",
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
        user_id = "5c8633d5000000001003bad6"
        for i in range(1, 27):
            result = xhs.get_user_notes(user_id, page=i)
            notes = result['result']['data']['notes']
            for note in notes:
                note_id = note['id']
                note_title = note['title']
                note_user = note['user']['nickname']
                note_result = xhs.get_note_detail(note_id)
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
                ws.append([note_user, note_desc, note_title, note_create_time, note_like_count, note_coll_count,
                           note_comments_count])
            wb.save(r"D:\red_book\red_book_51wom\red_book_07_21\五菱汽车red_book_07_21.xlsx")
    except Exception as e:
        print(e)
