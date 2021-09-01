import asyncio
import datetime
import os
import random
import re
import time
import traceback
from math import log
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from lxml import etree
from openpyxl import Workbook
import pandas as pd
import json
# from red_erp.whosecard_open_platform import WhosecardXhsSpider
import re
import requests
import aiohttp

wb = Workbook()
wb1 = Workbook()

ws = wb.active
ws1 = wb1.active

# ws.append(
#     ["用户链接",
#      "用户名",
#      "用户签名",
#      "用户等级",
#      "用户所在地区",
#      "粉丝数",
#      "kol",
#      "获赞数",
#      "关注数",
#      "收藏数",
#      "获赞与收藏数",
#      "笔记数",
#      "文章链接",
#      "文章类型",
#      "文章标题",
#      "文章内容",
#      "发布时间",
#      "发布时间戳",
#      "文章点赞数",
#      "文章评论数",
#      "文章收藏数",
#      "文章分享数",
#      "获赞与收藏",
#      "评分",
#      "合作品牌",
#      "特征词"
#      ]
# )

# ws.append([
#     "用户名",
#     "用户签名",
#     "用户等级",
#     "用户所在区域",
#     "粉丝数",
#     "kol级别",
#     "获赞数",
#     "关注数",
#     "收藏数",
#     "获赞与收藏数",
#     "笔记数"
# ])

# ws.append(['用户名',
#            '笔记标题',
#            '笔记链接',
#            '笔记提交时间'])
ws.append(['用户名', '文章标题', '文章链接'])

ws1.append(['用户名', '失效链接'])
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

cookie = "xhsTrackerId=ce649b22-f7c7-4686-c678-cc14d2c02782; xhsuid=wlNhixrVouQc1xH6; customerClientId=559394368134108; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1617094977,1617094988; smidV2=202104061553193a7c1a21482c01657352bb93535ed8a2007fa273ba4ff5ac0; xhs_spid.5dde=3af7c19f4aa1caf1.1617094977.13.1621407883.1620637217.692ca0a4-eabc-4f38-b1e9-ec9c4b8d49cb; xhsTracker=url=user-profile&xhsshare=CopyLink; timestamp2=20210804ad87a22f804c577cd2b4f9a3; timestamp2.sig=lsTRDLj5pOpLpPw7YKWAtWWbY5ZqlFdSk8g4Iqzm2uQ; extra_exp_ids=gif_exp1,ques_exp2"
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

APP_NAME = 'whosecard_open_platform'
# logger = LoggingHelper.get_logger(APP_NAME)

BASE_URI = 'http://whosecard.com:8081'
APP_CONFIG = {
    'KEY': '55b69c89f13291700c70b1c36a36a7611e25ea04058074072241fd46'
}
XHS_API_PATH = {
    'search_notes': '/api/xiaohongshu/search/notes/v1',
    'note_detail': '/api/xiaohongshu/note/detail',
    'note_comments': '/api/xiaohongshu/note/comments',
    'note_sub_comments': '/api/xiaohongshu/note/sub_comments',
    'note_goods': '/api/xiaohongshu/note/goods',
    'user_notes': '/api/xiaohongshu/user/notes',
    'user_info': '/api/xiaohongshu/user/info',
    'user_followings': '/api/xiaohongshu/user/followings/v1',
    'user_followers': '/api/xiaohongshu/user/followers/v1',
    'note_liked': '/api/xiaohongshu/note/liked/v1',
    'note_faved': '/api/xiaohongshu/note/faved/v1',
    'store_items': '/api/xiaohongshu/store/items',
    'search_goods': '/api/xiaohongshu/search/goods',
    'search_user': '/api/xiaohongshu/search/user',
    'fe_api': '/api/xiaohongshu/fe_api'
}


def get_data_from_api_url(api_url, params: dict):
    """
    获取接口数据
    :param api_url:
    :param params:
    :return:
    """
    params['key'] = APP_CONFIG['KEY']
    try:
        result = requests.get(api_url, params=params).json()
        if result.get('ok'):
            return result
        else:
            print(f'whosecard 返回值错误,返回值内容{result},请查看官网.')
            return {}
    except Exception as e:
        print(f'whosecard 接口错误,错误内容{e},请查看官网.')
        return {}


class WhosecardXhsSpider(object):
    """ whosecard 小红书 spider
    """

    @classmethod
    def get_data_from_api_name(cls, api_name, params: dict):
        """
        获取接口数据
        :param api_name:
        :param params:
        :return:
        """
        api_url = f'{BASE_URI}{XHS_API_PATH[api_name]}'
        return get_data_from_api_url(api_url, params)

    @classmethod
    def get_search_notes(cls, keyword, page, sort='general'):
        """
        获取关键词搜索文章结果
        :param keyword:
        :param page:
        :param sort: 可取值：general(综合) popularity_descending(最热) time_descending(最新)， 默认取general
        :return:
        """
        params = dict()
        params['keyword'] = keyword
        params['page'] = page
        params['sort'] = sort
        return cls.get_data_from_api_name('search_notes', params)

    @classmethod
    def get_note_detail(cls, note_id):
        """
        获取文章详情
        :param note_id:
        :return:
        """
        params = dict()
        params['note_id'] = note_id
        return cls.get_data_from_api_name('note_detail', params)

    @classmethod
    def get_note_comments(cls, note_id, cursor=None):
        """

        :param note_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['note_id'] = note_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('note_comments', params)

    @classmethod
    def get_note_sub_comments(cls, note_id, comment_id, cursor=None):
        """

        :param note_id:
        :param comment_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['note_id'] = note_id
        params['comment_id'] = comment_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('note_sub_comments', params)

    @classmethod
    def get_note_goods(cls, note_id, page):
        """
        获取文章详情
        :param note_id:
        :param page:
        :return:
        """
        params = dict()
        params['note_id'] = note_id
        params['page'] = page
        return cls.get_data_from_api_name('note_goods', params)

    @classmethod
    def get_user_notes(cls, user_id, page):
        """
        获取文章详情
        :param user_id:
        :param page:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['page'] = page
        return cls.get_data_from_api_name('user_notes', params)

    @classmethod
    def get_user_info(cls, user_id):
        """
        获取文章详情
        :param user_id:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        return cls.get_data_from_api_name('user_info', params)

    @classmethod
    def get_user_followings(cls, user_id, cursor=None):
        """
        获取文章详情
        :param user_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('user_followings', params)

    @classmethod
    def get_user_followers(cls, user_id, cursor=None):
        """
        获取文章详情
        :param user_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('user_followers', params)

    @classmethod
    def get_note_liked(cls, user_id, cursor=None):
        """
        获取文章详情
        :param user_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('note_liked', params)

    @classmethod
    def get_note_faved(cls, user_id, cursor=None):
        """
        获取文章详情
        :param user_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('note_faved', params)

    @classmethod
    def get_store_items(cls, store_id, page):
        """

        :param store_id:
        :param page:
        :return:
        """
        params = dict()
        params['store_id'] = store_id
        params['page'] = page
        return cls.get_data_from_api_name('store_items', params)

    @classmethod
    def get_search_goods(cls, keyword, page, sort=None):
        """
        获取关键词搜索文章结果
        :param keyword:
        :param page:
        :param sort: 当sort不传时，则默认为综合搜索, 可取值：sales_qty(销量) fav_count(种草数) price_asc(价格升序) price_desc(价格降序) new_arrival(新品优先)
        :return:
        """
        params = dict()
        params['keyword'] = keyword
        params['page'] = page
        params['sort'] = sort
        return cls.get_data_from_api_name('search_goods', params)

    @classmethod
    def get_search_user(cls, keyword, page):
        """
        获取关键词搜索文章结果
        :param keyword:
        :param page:
        :return:
        """
        params = dict()
        params['keyword'] = keyword
        params['page'] = page
        return cls.get_data_from_api_name('search_user', params)

    @classmethod
    def get_topic_info(cls, topic_id):
        """
        获取关键词搜索文章结果
        :param topic_id:
        :return:
        """
        params = dict()
        params['pageId'] = topic_id
        return cls.get_data_from_api_name('fe_api', params)

    @classmethod
    def get_topic_list(cls, topic_id, page, sort, subPath='notes'):
        """

        :param topic_id:
        :param subPath:
        :param page:
        :param sort: 可取之为hot与time，默认为hot，表示按热度排序，time表示按最新排序
        :return:
        """
        params = dict()
        params['pageId'] = topic_id
        params['subPath'] = subPath
        params['page'] = page
        params['sort'] = sort
        return cls.get_data_from_api_name('fe_api', params)


wh = WhosecardXhsSpider()


def short_url_to_long_url(short_url):
    """

    :param short_url:
    :return:
    """
    res = requests.get(short_url, headers=headers, allow_redirects=False)
    long_url = res.headers.get('location')
    return long_url


def get_yuanrenyun_ip():
    # 代理隧道验证信息
    # url = "http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=&gm=4"
    url = "http://d.jghttp.alicloudecs.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=4&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=&username=chukou01&spec=1"
    resp = requests.get(url).json()
    print(resp)
    ip = resp["data"][0]["ip"]
    port = resp["data"][0]["port"]
    meta = "http://%(host)s:%(port)s" % {
        "host": ip,
        "port": port,
    }
    proxies = {
        "http": meta,
        "https": meta
    }
    # print(proxies)
    return proxies


# proxies = get_yuanrenyun_ip()


# note_id
# def get_red_book(red_url, user_name, old_url):
def get_red_book(red_url):
    # global PROXY
    # note_id = ""
    try:
        s = requests.session()
        s.keep_alive = False
        # print(proxies)
        response = s.get(red_url, headers=headers)
        if response.status_code == 200:
            res = response.text
            # if '__INITIAL_SSR_STATE__' not in res or '/fe_api/burdock/v2' in res:
            #     for i in range(10):
            #         print(f"当前使用代理为：{PROXY}")
            #         try:
            #             html = requests.get(url=url, timeout=2, headers=headers, proxies=PROXY,
            #                                 verify=False).text
            #             if '__INITIAL_SSR_STATE__' not in html or '/fe_api/burdock/v2' in html:
            #                 print(f"html中无对应数据，更新代理重发请求")
            #                 try:
            #                     PROXY = get_yuanrenyun_ip()
            #                     print(f'更新代理为：{PROXY}')
            #                 except:
            #                     print(f"代理链接请求失败: {traceback.format_exc()}")
            #             else:
            #                 break
            #         except:
            #             print(f'当前代理：{PROXY} 连接超时！已尝试最大次数连接！')
            #             try:  # 代理请求失败
            #                 PROXY = get_yuanrenyun_ip()
            #                 print(f'更新代理为：{PROXY}')_
            #             except:
            #                 print(f"至流代理链接请求失败: {traceback.format_exc()}")
            # print(res)
            # re获取json 数据
            user_info_list = re.findall(r"<script>window.__INITIAL_SSR_STATE__[\s\S]*?{([\s\S]+?)}</script>"
                                        , res)
            print(user_info_list)
            # 完善 json 格式
            if user_info_list:
                user_info_str = user_info_list[0].strip()
                user_info_str = "{" + "{}".format(user_info_str) + "}"
                user_info_json = json.loads(user_info_str.replace('undefined', 'null'))
                print(user_info_json)
                user_info = user_info_json['Main']['userDetail']
                nick_name = user_info['nickname']
                fans = user_info['fans']
                # nick_name = user_info_json['NoteView']['noteInfo']['user']['nickname']
                # note_info = user_info_json['NoteView']['noteInfo']
                # desc = note_info['desc']
                # title = note_info['title']
                ws.append([nick_name, fans])
                # wb.save(r"D:\red_book\red_book_51wom\red_book_8月\娇诗韵result_08_02_1.xlsx")
        # else:
        #     ws1.append([user_name, old_url])
            wb.save(r"D:\red_book\red_book_51wom\red_book_8月\red_book_08_05\red_book_08_05.xlsx")
    except Exception as a:
        print(a)


if __name__ == '__main__':
    try:

        rd = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_8月\red_book_08_05\red_urls.xlsx")
        urls = rd["主页链接"]
        # users = rd['昵称']
        # for index, url in enumerate(urls):
        for url in urls:
            # if "xhslink.com" in url:
            #     print(url)
            #     long_url = short_url_to_long_url(url)
            #     get_red_book(long_url, users[index], url)
            # else:
            print(url)
            get_red_book(url)
            # get_red_book(url, users[index], url)
    except Exception as e:
        print(e)
