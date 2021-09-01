import json
import random
import re

import pandas as pd
from openpyxl import Workbook

import requests

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    # "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]

cookie = "xhsTrackerId=ce649b22-f7c7-4686-c678-cc14d2c02782; xhsuid=wlNhixrVouQc1xH6; customerClientId=559394368134108; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1617094977,1617094988; smidV2=202104061553193a7c1a21482c01657352bb93535ed8a2007fa273ba4ff5ac0; xhs_spid.5dde=3af7c19f4aa1caf1.1617094977.13.1621407883.1620637217.692ca0a4-eabc-4f38-b1e9-ec9c4b8d49cb; xhsTracker=url=noteDetail&xhsshare=CopyLink; extra_exp_ids=gif_exp1,ques_exp2; timestamp2=20210813d124e9bfab396175f57036d1; timestamp2.sig=D0K3olUHeAANUcGWisDcHvCB0yTnwXORQNMEVXAmkgk"
headers = {
    "User-Agent": random.choice(USER_AGENTS),
    "cookie": cookie,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'Connection': 'close'
}

wb = Workbook()
wb1 = Workbook()
ws = wb.active
ws1 = wb1.active
ws.append([
    "用户名", "用户签名", "用户等级", "头像链接", "笔记数", "所在地区", "收藏数", "点赞数", "文章链接", "文章标题", "文章点赞", "文章内容", "文章评论", "文章创建时间"
])
ws1.append([
    "", "", "", "", "", "", "", "", "",
])

def short_url_to_long_url(short_url):
    """

    :param short_url:
    :return:
    """
    res = requests.get(short_url, headers=headers, allow_redirects=False)
    long_url = res.headers.get('location')
    return long_url


def get_user_detail(u_id):
    r_url = f"https://www.xiaohongshu.com/user/profile/{u_id}"
    resp = requests.get(url=r_url, headers=headers)
    user_info_list = re.findall(r"<script>window.__INITIAL_SSR_STATE__[\s\S]*?{([\s\S]+?)}</script>"
                                , resp.text)
    # print(user_info_list)
    if user_info_list:
        user_info_str = user_info_list[0].strip()
        user_info_str = "{" + "{}".format(user_info_str) + "}"
        user_info_json = json.loads(user_info_str.replace('undefined', 'null'))
        # print(user_info_json)
        user_detail = user_info_json['Main']['userDetail']
        nickname = user_detail['nickname']
        notes = user_detail['notes']
        location = user_detail['location']
        header_image = user_detail['image']
        collected = user_detail['collected']
        sign = user_detail['desc']
        liked = user_detail['liked']
        user_level = user_detail['level']['name']
        note_details = user_info_json['Main']['notesDetail']
        for note_detail in note_details:
            note_title = note_detail['title']
            note_id = note_detail['id']
            note_likes = note_detail['likes']
            note_time = note_detail['time']
            note_url = f"https://www.xiaohongshu.com/discovery/item/{note_id}"
            response = requests.get(note_url, headers=headers)
            note_info_list = re.findall(r"<script>window.__INITIAL_SSR_STATE__[\s\S]*?{([\s\S]+?)}</script>"
                                        , response.text)
            if note_info_list:
                note_info_str = note_info_list[0].strip()
                note_info_str = "{" + "{}".format(note_info_str) + "}"
                note_info_json = json.loads(note_info_str.replace('undefined', 'null'))
                print(note_info_json)
                comments = note_info_json['NoteView']['commentInfo']['comments']
                note_desc = note_info_json['NoteView']['noteInfo']['desc']
                comment_details = ""
                for comment in comments:
                    content = comment['content']
                    content_user = comment['user']['nickname']
                    comment_detail = content_user + ":" + content
                    comment_details += (comment_detail + "，")
                print(comment_details)
                ws.append([nickname, sign, user_level, header_image, notes, location, collected, liked, note_url,
                           note_title, note_likes, note_desc, comment_details, note_time])
            wb.save(r"D:\red_book\red_book_51wom\red_book_8月\red_book_08_13\red_book_result.xlsx")


if __name__ == '__main__':
    # uid = "6011212c000000000101e7f4"
    # path = input("请输入读取文件路径")
    df = pd.read_excel("path")
    urls = df['主页链接']
    for url in urls:
        if "xhslink.com" in url:
            long_url = short_url_to_long_url(url)
            u_id = long_url.split("/")[-1].split("?")[0]
        elif "apptime" in url:
            u_id = url.split("/")[-1].split("?")[0]
        else:
            u_id = url.split("/")[-1]
        get_user_detail(u_id)
