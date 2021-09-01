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
ws.append(['用户名', '标题', '文章内容', '文章链接'])

ws1.append(['转换前链接', '短链'])
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

cookie = "xhsTrackerId=ce649b22-f7c7-4686-c678-cc14d2c02782; xhsuid=wlNhixrVouQc1xH6; customerClientId=559394368134108; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1617094977,1617094988; smidV2=202104061553193a7c1a21482c01657352bb93535ed8a2007fa273ba4ff5ac0; xhs_spid.5dde=3af7c19f4aa1caf1.1617094977.13.1621407883.1620637217.692ca0a4-eabc-4f38-b1e9-ec9c4b8d49cb; xhsTracker=url=noteDetail&xhsshare=CopyLink; extra_exp_ids=gif_exp1,ques_exp2; timestamp2=20210728ad87a22f804c577cba63e2fb; timestamp2.sig=0-R7wlQXiyhQiNsfZoFQdv-GDGMX5W8aoPWLSNJmQlY"
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

# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: anne
@contact: thy.self@foxmail.com
@time: 2020/9/2 2:33 下午
"""

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


# note_id
async def get_red_book(red_url, semaphore):
    user_info = ""
    nick_name = ""
    user_fans_num = ""
    user_follow_num = ""
    user_collect_like_num = ""
    user_collected = ""
    user_fans_level = ""
    user_like = ""
    note_num = ""
    user_desc = ""
    user_local = ""
    user_level = ""
    user_url = ""
    note_infos = ""
    note_url = ""
    # note_id = ""
    try:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=red_url, headers=headers) as response:
                    # try:
                    if response:
                        res = await response.text()
                        # print(res)
                        # re获取json 数据
                        user_info_list = re.findall(r"<script>window.__INITIAL_SSR_STATE__[\s\S]*?{([\s\S]+?)}</script>"
                                                    , res)
                        # print(user_info_list)
                        # 完善 json 格式
                        if user_info_list:
                            user_info_str = user_info_list[0].strip()
                            user_info_str = "{" + "{}".format(user_info_str) + "}"
                            user_info_json = json.loads(user_info_str.replace('undefined', 'null'))
                            print(user_info_json)
                            # if user_info_json:
                            #     if "NoteView" in user_info_json:
                            #         note_info = user_info_json["NoteView"]['noteInfo']
                            #         note_title = note_info['title']
                            #         note_user = note_info['user']['nickname']
                            #         note_time = note_info['time']
                            #         print([note_user, note_title, red_url, note_time])
                            #         ws.append([note_user, note_title, red_url, note_time])
                            # if "Main" in user_info_json:
                            #     user_info = user_info_json['Main']['userDetail']
                            #     note_infos = user_info_json['Main']['notesDetail']
                            nick_name = user_info_json['NoteView']['noteInfo']['user']['nickname']
                            note_info = user_info_json['NoteView']['noteInfo']
                            desc = note_info['desc']
                            title = note_info['title']
                            # print(nick_name)

                            # elif "ProfileLayout" in user_info_json:
                            #     user_info = user_info_json['ProfileLayout']['userInfo']
                            # 用户昵称
                            # nick_name = user_info['nickname']
                            # # 用户笔记数
                            # note_num = user_info['notes']
                            # # 用户签名
                            # user_desc = user_info['desc']
                            # # 用户所在区域
                            # user_local = user_info['location']
                            # # 用户等级
                            # user_level = user_info['level']['name']
                            # # 用户ID
                            # user_id = user_info['id']
                            # # 用户链接
                            # user_url = "https://www.xiaohongshu.com/user/profile/{}".format(user_id)
                            # # 用户粉丝数
                            # user_fans_num = user_info['fans']
                            # if 0 <= user_fans_num <= 50000:
                            #     user_fans_level = '素人'
                            # elif 50000 <= user_fans_num <= 200000:
                            #     user_fans_level = '底部kol'
                            # elif 200000 <= user_fans_num <= 1000000:
                            #     user_fans_level = '腰部kol'
                            # else:
                            #     user_fans_level = '头部kol'
                            # # 用户关注数
                            # user_follow_num = user_info['follows']
                            # # 用户收藏数
                            # user_collected = user_info['collected']
                            # # 用户获赞数
                            # user_like = user_info['liked']
                            # # 用户获赞与收藏统计
                            # user_collect_like_num = int(user_collected) + int(user_like)
                            # # 文章信息
                            # for note_info in note_infos:
                            #     note_id = note_info['id']
                            #     note_url = "https://www.xiaohongshu.com/discovery/item/{}".format(note_id)
                            # print(note_url)
                            ws.append([nick_name, title, desc, red_url])
                            # time.sleep(1)
                    # note_result = wh.get_note_detail(note_id)
                    # note_list = note_result['result']['data'][0]['note_list']
                    # print(note_list)
                    # note_desc = ("".join(str(i) for i in note_list[0]['desc']))
                    # # 笔记标题
                    # note_title = note_desc.split('\n')[0]
                    # # 笔记类型
                    # note_type = note_list[0]['type']
                    # # 笔记详情
                    # note_detail = str(note_desc.split('\n')[1:]).replace("[", "").replace("]", "").replace("'", "")
                    # # 笔记时间戳
                    # note_ts = note_list[0]['time']
                    # # 笔记时间 年月日时分秒格式
                    # timeArray = time.localtime(note_ts)
                    # note_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    # # 笔记点赞数
                    # note_likes = note_list[0]['liked_count']
                    # # 笔记评论数
                    # note_comments = note_list[0]['comments_count']
                    # # 笔记收藏数
                    # note_coll = note_list[0]['collected_count']
                    # # 笔记获赞和收藏统计
                    # note_coll_like_count = int(note_likes) + int(note_coll)
                    # # 笔记分享数
                    # note_share = note_list[0]['shared_count']
                    # # 合作品牌
                    # note_cooperate_binds = ''
                    # # 评分
                    # score = round(
                    #     (0.2 * (pow(log(int(note_likes) + 1), 2)) + 0.4 * (
                    #         pow(log(int(note_comments) + 1), 2)) + 0.4 * (
                    #          pow(log(int(note_coll) + 1), 2))), 2)
                    # # 特征词
                    # if note_list[0]['ats']:
                    #     note_ats = [note_list[0]['ats'][i]['nickname'] for i in
                    #                 range(len(note_list[0]['ats']))]
                    # else:
                    #     note_ats = []
                    # note_tags = note_ats
                    # note_tag = []
                    # for i in note_tags:
                    #     if isinstance(i, dict):
                    #         note_tag.append(i['name'])
                    #     else:
                    #         note_tag.append(i)
                    # note_tag = str(note_tag)
                    # "用户链接", "用户名", "用户签名", "用户所在区域", "粉丝数", "kol级别", "获赞数", "关注数", "收藏数", "获赞与收藏数", "笔记数", "文章链接"
                    # ws.append([nick_name, user_desc, user_level, user_local, user_fans_num, user_fans_level, user_like, user_follow_num,
                    #            user_collected, user_collect_like_num, note_num])
                    # ws.append(
                    #     [user_url, nick_name, user_desc, user_level, user_local, user_fans_num, user_fans_level,
                    #      user_like, user_follow_num, user_collected,
                    #      user_collect_like_num, note_num, note_url, note_type,
                    #      note_title, note_detail, note_time, note_ts, note_likes, note_comments, note_coll, note_share,
                    #      note_coll_like_count, score, note_cooperate_binds, note_tag])
    except Exception as a:
        print(a)


async def main():
    rd = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_07_28\小红书投放链接_20210728.xlsx")
    urls = rd["publish_link"]
    semaphore = asyncio.Semaphore(500)
    tasks = [get_red_book(url, semaphore) for url in urls]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    try:
        start_time = time.time()
        asyncio.run(main())
        end_time = time.time()
        spend_time = end_time - start_time
        wb.save(r"D:\red_book\red_book_51wom\red_book_07_28\user_note_url2.xlsx")
        print(spend_time)
        # rd = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_07_22\urls.xlsx")
        # urls = rd["发布链接"]
        # # users = rd['用户名']
        # for index, url in enumerate(urls):
        #     if "xhslink.com" in url:
        #         print(url)
        #         res = requests.get(url, headers=headers, allow_redirects=False)
        #         long_url = res.headers.get('location')
        #         # time.sleep(2)
        #         print(long_url)
        #         ws1.append([url, long_url])
        #         wb1.save(r"D:\red_book\red_book_51wom\red_book_07_22\短转长链接.xlsx")
        #     else:
        #         ws.append([url, url])
        #         wb.save(r"D:\red_book\red_book_51wom\red_book_07_22\长链接.xlsx")
        # if "xhslink.com" in url:
        #     ws1.append([url])
        #     wb1.save('D:/red_book/red_book_51wom/red_book_06_25/short_url2.xlsx')
        #     # long_url = short_url_to_long_url(url)
        #     # pool.submit(get_red_book, url, long_url)
        # else:
        #     pool.submit(get_red_book, url)
        #     wb.save("D:/red_book/red_book_51wom/red_book_06_25/red_book_06_25_result_1.xlsx")
        #     note_id = short_url_to_long_url(url).split("/")[-1].split("?")[0]
        # else:
        #     note_id = url.split("/")[-1]
        # note_result = wh.get_note_detail(note_id)
        # print(note_result)
        # if not note_result:
        #     print("笔记不存在")
        # else:
        #     note_list = note_result['result']['data'][0]['note_list']
        #     print(note_list)
        #     note_create = note_list['time']
        #     timeArray = time.localtime(note_create)
        #     note_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        #     note_author = note_list['user']['nickname']
        #     ws.append([note_author, url, note_time])
        # # 笔记点赞数
        # note_likes = note_list[0]['liked_count']
        # # 笔记评论数
        # note_comments = note_list[0]['comments_count']
        # # 笔记收藏数
        # note_coll = note_list[0]['collected_count']
        # # 用户名
        # user_name = note_list[0]['user']['nickname']
        # user_id = note_list[0]['user']['id']
        # user_url = "https://www.xiaohongshu.com/user/profile/{}".format(user_id)
        # print(user_url)
        # # get_red_book(user_url, note_id)
        # wb.save("D:/red_book/red_book_51wom/06_24/red_book_06_24.xlsx")
        # pool.submit(get_red_book, str(url).strip())
    except Exception as e:
        print(e)
