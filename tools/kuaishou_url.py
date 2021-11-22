import json
import re
import time

import pandas as pd
from openpyxl import Workbook
from short_to_long import short_url_to_long_url
import requests

wb = Workbook()
ws = wb.active
ws.append([
    "用户名",
    "用户链接"
])

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "content-type": "application/json",
    "Cookie": "kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; clientid=3; did=web_26e4490e8d00ca8aae5cd79fb5ea4985; client_key=65890b29; kpn=GAME_ZONE; userId=2609462078; userId=2609462078; didv=1635923255000; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAWys0DTsgK8K-Zg5r7oRX-Sozl2g0ahdfoWYb9S6cBN-Xq1qLnQ63ABlyT7vOjbPl_W9FMbV9lMnPT2KbczpIaxqk0FJc_g8ND0-r_kW-Y7OKV9juiMy8bTctU8-Fohhd97lgc64jFh0ZkX6Fwem4Sy50QGZf7v-M-YNMlr3MB18IJ61e4I9hB9HTobYSN0Qrh29lpe2PM3O2WsPoUGLV_gaEsvpGUru20c-iIt7T0W8MQrXwiIgPbOLE3xPn7BXtNGMOWSIFWnxQtFAr2JzZQBcXgxYWVUoBTAB; kuaishou.live.web_ph=c43b49065d67b29da76896d57fce78a9cb87"
}


def get_u_id(k_url, users):
    try:
        if k_url == "None":
            ws.append([users, k_url])
        elif "3x" in k_url:
            ws.append([users, k_url])
        else:
            payload = {"operationName":"privateFeedsQuery","variables":{"principalId":"miaoyouyou666","pcursor":"","count":24},"query":"query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      isSpherical\n      __typename\n    }\n    __typename\n  }\n}\n"}
            principalId = k_url.split("/")[-1]
            payload['variables']['principalId'] = principalId
            resp = requests.post(url="https://live.kuaishou.com/live_graphql", headers=headers, data=json.dumps(payload)).json()
            # print(resp.text)
            u_name = resp['data']['privateFeeds']['list'][0]['user']['name']
            u_id = resp['data']['privateFeeds']['list'][0]['user']['eid']
            # u_id = re.findall(r'"eid": (.*?),', resp.text, re.S)[0]
            print(u_id)
            user_url = f"https://live.kuaishou.com/profile/{u_id}"
            ws.append([u_name, user_url])
        wb.save(r"D:\red_book\red_book_51wom\red_book_11月\red_book_11_03\kuaishou_long_urls_1.xlsx")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    df = pd.read_excel(r'D:\red_book\red_book_51wom\red_book_11月\red_book_11_03\kuaishou_urls.xlsx')
    urls = df['主页链接']
    users = df['账号昵称']
    for index, k_url in enumerate(urls):
        get_u_id(k_url, users[index])
        time.sleep(4)
        # print(url)
