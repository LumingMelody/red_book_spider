import json
import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from hashlib import md5
from threading import Timer
import pandas as pd
import requests
import re
import threading
from threading import Thread
from queue import Queue
import pymongo
from fake_useragent import UserAgent

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

# 阿里云MongoDB
client = pymongo.MongoClient('dds-m5e296a1c97603741182-pub.mongodb.rds.aliyuncs.com', 3717)
db = client['wom-dts-datawarehouse']
db.authenticate('dts-datawarehouse-admin', 'aowB0y6yQyPOc9h')
# my_set = db['scrapy_detail_coll_xsm']
my_set = db['red_book_data_info']

# 测试本地MongoDB
# client = pymongo.MongoClient("localhost", 27017)
# db = client['admin']
# my_set = db.test


# rd = pd.read_csv("D:/red_book/小红书笔记JSON/user_urls.txt")
# rd.to_excel("D:/red_book/小红书笔记JSON/user_urls.xlsx")
rd = pd.read_excel("D:/red_book/小红书笔记JSON/user_urls.xlsx")
article_ids = rd["url"]
cookie = "xhsTrackerId=ce649b22-f7c7-4686-c678-cc14d2c02782; xhsuid=wlNhixrVouQc1xH6; customerClientId=559394368134108; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1617094977,1617094988; smidV2=202104061553193a7c1a21482c01657352bb93535ed8a2007fa273ba4ff5ac0; xhs_spid.5dde=3af7c19f4aa1caf1.1617094977.13.1621407883.1620637217.692ca0a4-eabc-4f38-b1e9-ec9c4b8d49cb; xhsTracker=url=noteDetail&xhsshare=CopyLink; timestamp2=202106019b12eb27995a1a683e6c07a1; timestamp2.sig=WCqCcTh2cWlFGpvIFUe1fOOXJg-_0JSG6_aJwUvrc6U; extra_exp_ids=gif_exp1,ques_exp2"
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

# def get_yuanrenyun_ip():
#     # 代理隧道验证信息
#     # url = "http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=&gm=4"
#     url = "http://tunnel-api.apeyun.com/h?id=2021040800226731834&secret=pA7prxttyuCTFjwM&limit=1&format=json&auth_mode=hand"
#     resp = requests.get(url).json()
#     print(resp)
#     ip = resp["data"][0]["ip"]
#     port = resp["data"][0]["port"]
#     meta = "https://%(host)s:%(port)s" % {
#         "host": ip,
#         "port": port,
#     }
#     proxies = {
#         "http": meta,
#         "https": meta
#     }
#     # proxies = meta
#     # print(proxies)
#     return proxies

# 代理服务器
proxyHost = "forward.apeyun.com"
proxyPort = "9082"
# 代理隧道验证信息
proxyUser = "2021040800226731834"
proxyPass = "pA7prxttyuCTFjwM"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}


def timer(n):
    get_cookie()


def get_sign(sign):
    """

    :param sign:
    :return:
    """
    sign = sign + "hasaki"
    sign = md5(sign.encode()).hexdigest()
    return sign


def get_cookie():
    headers1 = {
        'authority': 'www.xiaohongshu.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://www.xiaohongshu.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'zh-CN,zh;q=0.9'}

    params = (
        ('p', 'cc'),
    )

    ua = random.choice(USER_AGENTS)
    # TODO cookie动态更新
    # https://github.com/fingerprintjs/fingerprintjs/blob/v2/fingerprint2.js
    sign = f"{ua}~~~unknown~~~zh-CN~~~24~~~8~~~12~~~-480~~~Asia/Shanghai~~~1~~~1~~~1~~~1~~~unknown" \
           "~~~Win32~~~Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf,Chrome" \
           " PDF Viewer::::application/pdf~pdf,Native Client::::application/x-nacl~,application/x-pnacl~~~~" \
           "canvas winding:yes~canvas fp:af63627abb7f6d68a8cd864315e785a9~~~false~~~false~~~false~~~false~~~" \
           "false~~~0;false;false~~~4;7;8~~~124.04347527516074"

    id = get_sign(sign)

    data = '{"id":"%s","sign":"%s"}' % (id, sign)

    response = requests.post('https://www.xiaohongshu.com/fe_api/burdock/v2/shield/registerCanvas', headers=headers1,
                             params=params, data=data, verify=False)

    # 同一个sign，平台每天返回值都会改变，可不用做动态cookie值
    resp_headers = response.headers
    if resp_headers.get("set-cookie"):
        timestamp2 = re.findall(r'timestamp2=(.*?);', resp_headers["set-cookie"])[0]
        timestamp2_sig = re.findall(r'timestamp2\.sig=(.*?);', resp_headers["set-cookie"])[0]
        cookie = f"timestamp2={timestamp2};timestamp2.sig={timestamp2_sig};"
        headers['cookie'] = cookie
        return cookie


def get_red_book(url):
    response = requests.get(url=url, headers=headers, verify=False, proxies=proxies, stream=True)
    # print(url)
    # headers["cookie"] = response.cookies
    # print(response.text)
    user_info_json = ""
    try:
        if response:
            res = response.content.decode("utf-8")
            # print(res)
            # re获取json 数据
            user_info_list = re.findall(r"<script>window.__INITIAL_SSR_STATE__[\s\S]*?{([\s\S]+?)}</script>", res)
            # if user_info_list is None:
            #     cookies = get_cookes(proxies)
            #     headers["cookie"] = cookies
            # 300秒（5分钟）更换一次cookie,时间可以任意更改 以秒为单位
            # work(200)
            # print(user_info_list)
            try:
                user_info_str = user_info_list[0].strip()
                user_info_str = "{" + "{}".format(user_info_str) + "}"
                user_info_json = json.loads(user_info_str.replace('undefined', 'null'))
            except Exception as e:
                print(e)
            if user_info_json:
                # print(user_info_json)
                # if user_info_list:
                info = {}
                user_info = ""
                try:
                    # print(user_info_json)
                    if "Main" in user_info_json:
                        user_info = user_info_json['Main']
                    elif "ProfileLayout" in user_info_json:
                        user_info = user_info_json['ProfileLayout']
                    # 当前时间的时间戳
                    ts = str(time.time()).split(".")[0]
                    # 当前时间年月日格式
                    # ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    info['data'] = str(user_info)
                    info['ts'] = str(ts)
                    print(info)
                    my_set.insert(info)
                except Exception as e:
                    print(e)
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"


if __name__ == '__main__':
    # pass
    # urlQueue = Queue()
    # result_queue = Queue()
    # max_workers是线程数,可以根据自己的需求更改线程数
    # pool = ThreadPoolExecutor(max_workers=40)
    # for article_id in article_ids:
    #     # article_url = f"https://www.xiaohongshu.com/discovery/item/{article_id}"
    #     # print(article_url)
    #     # get_red_book(article_id.strip())
    #     pool.submit(get_red_book, str(article_id).strip())
    # pool.shutdown(wait=True)
    rs = get_cookie()
    print(rs)