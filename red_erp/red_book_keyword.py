import random
import time

import pandas as pd
import requests
from openpyxl import Workbook

from red_erp.whosecard_open_platform import get_data_from_api_url

BASE_URI = 'http://whosecard.com:8081'
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

wb = Workbook()

ws = wb.active

# ws.append(
#     ["用户链接",
#      "用户id",
#      "用户链接",
#      "文章id",
#      "文章详情",
#      "文章链接",
#      "文章标题",
#      "文章提交时间",
#      ]
# )
ws.append([
    "用户名",
    "用户链接",
    "点赞",
    "收藏",
    "评论",
    "文章链接",
    "文章标题",
    "文章内容",
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

cookie = "xhsTrackerId=ce649b22-f7c7-4686-c678-cc14d2c02782; xhsuid=wlNhixrVouQc1xH6; customerClientId=559394368134108; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1617094977,1617094988; smidV2=202104061553193a7c1a21482c01657352bb93535ed8a2007fa273ba4ff5ac0; xhs_spid.5dde=3af7c19f4aa1caf1.1617094977.13.1621407883.1620637217.692ca0a4-eabc-4f38-b1e9-ec9c4b8d49cb; xhsTracker=url=noteDetail&xhsshare=CopyLink; extra_exp_ids=gif_exp1,ques_exp2; timestamp2=20210615fff32608588e6e3d2af7c457; timestamp2.sig=z-Ho3LPHt2tpPRVf0-wx5rd3Xa64oQFtnYJJNLUCZxY"
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


def short_url_to_long_url(short_url):
    """

    :param short_url:
    :return:
    """
    res = requests.get(short_url, headers=headers, allow_redirects=False)
    long_url = res.headers.get('location')
    return long_url


if __name__ == '__main__':

    wh = WhosecardXhsSpider()
    # rs = wh.get_note_comments()
    # print(rs)
    # rs = wh.get_search_notes("明星同款零食", page=5)
    rd = pd.read_excel("D:/red_book/red_book_51wom/06_18/【工单】小红书数据6.18.xlsx")
    urls = rd['发布链接']
    n_url = ""
    try:
        for url in urls:
            if "xhslink.com" in url:
                n_url = short_url_to_long_url(url)
                note_id = n_url.split("/")[-1].split("?")[0]
            note_id = url.split("/")[-1]
            print(note_id)
            rs = wh.get_note_detail(note_id)
            print(rs)
            note_list = rs['result']['data'][0]['note_list']
            u_id = note_list[0]['user']['id']
            u_url = "https://www.xiaohongshu.com/user/profile/{}".format(u_id)
            note_title = note_list[0]['mini_program_info']['title']
            note_desc = note_list[0]['mini_program_info']['desc']
            # 笔记点赞数
            note_likes = note_list[0]['liked_count']
            # 笔记评论数
            note_comments = note_list[0]['comments_count']
            # 笔记收藏数
            note_coll = note_list[0]['collected_count']
            # 用户名
            user_name = note_list[0]['user']['nickname']
            # 笔记ID
            note_id = note_list[0]['id']
            # 笔记链接
            note_url = "https://www.xiaohongshu.com/discovery/item/{}".format(note_id)
            ws.append([user_name, u_url, note_likes, note_coll, note_comments, note_url, note_title, note_desc])
        wb.save("D:/red_book/red_book_51wom/06_18/小红书06_18_result.xlsx")
    except Exception as e:
        print(e)
    # result = wh.get_note_detail("60b65e2b000000002103776b")
    # print(rs)
    # items = rs['result']['data']['items']
    # for item in items:
    #     if item['model_type'] == 'note':
    #         note_detail = item['note']['desc']
    #         note_id = item['note']['id']
    #         note_url = "https://www.xiaohongshu.com/discovery/item/{}".format(note_id)
    #         note_title = item['note']['title']
    #         note_create_time = item['note']['timestamp']
    #         timeArray = time.localtime(note_create_time)
    # #         note_create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    #         user_name = item['note']['user']['nickname']
    #         user_id = item['note']['user']['userid']
    #         user_url = "https://www.xiaohongshu.com/user/profile/{}".format(user_id)
    #         ws.append([user_url, user_name, user_url, note_id, note_detail, note_url, note_title, note_create_time])
    #     wb.save("D:/red_book/red_book_keyword/神仙水_06_02.xlsx")
