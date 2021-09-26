import asyncio
import datetime
import os
import random
import re
import time
from math import log
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from lxml import etree
from openpyxl import Workbook
import pandas as pd
import json
from red_erp.whosecard_open_platform import WhosecardXhsSpider
import re
import requests
import aiohttp

wb = Workbook()
wb1 = Workbook()
ws = wb.active
ws1 = wb1.active
ws.append([
    "用户名",
    "用户粉丝数",
    "文章标题",
    "文章内容",
    "文章链接",
    "点赞数",
    "收藏数",
    "评论数",
    "文章发布时间",
    "是否含有关键词",
])
ws1.append([
    "文章ID"
])

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

cookie = "xhsTrackerId=ce649b22-f7c7-4686-c678-cc14d2c02782; xhsuid=wlNhixrVouQc1xH6; customerClientId=559394368134108; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1617094977,1617094988; smidV2=202104061553193a7c1a21482c01657352bb93535ed8a2007fa273ba4ff5ac0; xhs_spid.5dde=3af7c19f4aa1caf1.1617094977.13.1621407883.1620637217.692ca0a4-eabc-4f38-b1e9-ec9c4b8d49cb; xhsTracker=url=noteDetail&xhsshare=CopyLink; timestamp2=20210820052eb992f8ab1118df72dac4; timestamp2.sig=RZfppzLR9XZPvgIYhKHBsItLkQi5v5eOtiHjO_Ale4M; solar.beaker.session.id=1629428579275065656997; extra_exp_ids=gif_exp1,ques_exp2"
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
wh = WhosecardXhsSpider()


def short_url_to_long_url(short_url):
    """

    :param short_url:
    :return:
    """
    res = requests.get(short_url, headers=headers, allow_redirects=False)
    long_url = res.headers.get('location')
    return long_url


def main(n_id):
    result = wh.get_note_detail(n_id)
    print(result)
    try:
        if result and result['result']['data'] is not None:
            note_list = result['result']['data'][0]['note_list'][0]
            name = note_list['user']['name']
            title = note_list['share_info']['title']
            desc = note_list['desc']
            if "娇韵诗双萃精华" or "娇韵诗" or "娇韵诗双萃" in desc:
                has_keyword = 1
            else:
                has_keyword = 0
            note_url = f"https://www.xiaohongshu.com/discovery/item/{n_id}"
            liked_count = note_list['liked_count']
            collected_count = note_list['collected_count']
            comments_count = note_list['comments_count']
            note_ts = note_list['time']
            # 笔记时间 年月日时分秒格式
            timeArray = time.localtime(note_ts)
            note_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            u_id = result['result']['data'][0]['user']['id']
            user_info = wh.get_user_info(u_id)
            # print(user_info)
            user_fans = user_info['result']['data']['fans']
            report_com_coll = int(liked_count) + int(collected_count) + int(comments_count)
            ws.append([name, user_fans, title, desc, note_url, liked_count, collected_count, comments_count, note_time,
                       has_keyword])
            # ws.append([name, title, desc, note_url, liked_count, collected_count, comments_count, note_time,
            #            has_keyword, report_com_coll])
            wb.save(r"D:\red_book\red_book_51wom\red_book_9月\red_book_09_24\red_book_result_09_24.xlsx")
            print([name, user_fans, title, desc, note_url, liked_count, collected_count, comments_count, note_time,
                   has_keyword])
    except Exception as a:
        print(a)


if __name__ == '__main__':
    # main("6040aff80000000001028082")
    # df = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_9月\red_book_09_01\reds.xlsx")
    # note_ids = df['文章ID']
    df = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_9月\red_book_09_24\red_book09_24.xlsx")
    urls = df['文章链接']
    try:
        # for note_id in note_ids:
        #     main(note_id)
        # with ThreadPoolExecutor(10) as t:
        for url in urls:
            if 'apptime' in url:
                note_id = url.split("/")[-1].split("?")[0]
            # elif 'xhslink.com' in url:
            #     long_url = short_url_to_long_url(url)
            #     note_id = long_url.split("/")[-1].split("?")[0]
            else:
                note_id = url.split("/")[-1]
            print(note_id)
            main(note_id)
            # time.sleep(3)
        # wb1.save(r"D:\red_book\red_book_51wom\red_book_8月\red_book_08_20\娇诗韵文章链接.xlsx")
    except Exception as e:
        print(e)
