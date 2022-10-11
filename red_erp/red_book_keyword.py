import random
import time
from math import log
import pandas as pd
import requests
from openpyxl import Workbook
from openpyxl.styles.builtins import note

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

ws.append(
    ["用户链接",
     "用户名",
     "用户签名",
     "用户等级",
     "用户所在地区",
     "粉丝数",
     "kol",
     "获赞数",
     "关注数",
     "收藏数",
     "获赞与收藏数",
     "笔记数",
     "文章链接",
     "文章类型",
     "文章标题",
     "文章内容",
     "发布时间",
     "发布时间戳",
     "文章点赞数",
     "文章评论数",
     "文章收藏数",
     "文章分享数",
     "获赞与收藏",
     "互动率",
     "评分",
     "合作品牌",
     "特征词"
     ]
)
# ws.append([
#     "用户名",
#     "用户链接",
#     "点赞",
#     "收藏",
#     "评论",
#     "文章链接",
#     "文章标题",
#     "文章内容",
# ])

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
    key_word_list = ["大食袋"]
    # rs = wh.get_note_comments()
    # print(rs)
    for keyword in key_word_list:
        for i in range(10, 21):
            print(i)
            rs = wh.get_search_notes(keyword, page=i + 1)
            # time.sleep(10)
            print(rs)
            try:
                if rs and rs['result']['data'] is not None:
                    items = rs['result']['data']['items']
                    print(len(items))
                    for item in items:
                        # print(item)
                        note_ts = item['note']['timestamp']
                        if 1643817600 <= int(note_ts) <= 1659492975:
                            try:
                                user_id = item['note']['user']['userid']
                                user_url = f'https://www.xiaohongshu.com/user/profile/{user_id}'
                                note_id = item['note']['id']
                                note_url = f'https://www.xiaohongshu.com/discovery/item/{note_id}'
                                note_type = item['model_type']
                                user_info = wh.get_user_info(user_id)['result']['data']
                                nickname = user_info['nickname']
                                sign = user_info['desc']
                                user_level = user_info['level']['level_name']
                                user_location = user_info['location']
                                user_fans_num = user_info['fans']
                                if 0 <= user_fans_num <= 50000:
                                    user_fans_level = '素人'
                                elif 50000 <= user_fans_num <= 200000:
                                    user_fans_level = '底部kol'
                                elif 200000 <= user_fans_num <= 1000000:
                                    user_fans_level = '腰部kol'
                                else:
                                    user_fans_level = '头部kol'
                                user_like_num = user_info['liked']
                                user_follows_num = user_info['follows']
                                user_collected_num = user_info['collected']
                                user_like_collected_num = int(user_like_num) + int(user_collected_num)
                                note_num = user_info['ndiscovery']
                                note_info = wh.get_note_detail(note_id)['result']['data'][0]['note_list'][0]
                                note_title = note_info['title']
                                note_content = note_info['desc']
                                note_ts = note_info['time']
                                timeArray = time.localtime(note_ts)
                                note_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                note_likes = note_info['liked_count']
                                note_comments = note_info['comments_count']
                                note_coll = note_info['collected_count']
                                note_share = note_info['shared_count']
                                note_collected_like = int(note_likes) + int(note_coll)
                                # 合作品牌
                                note_cooperate_binds = ''
                                # 评分
                                score = round(
                                    (0.2 * (pow(log(int(note_likes) + 1), 2)) + 0.4 * (
                                        pow(log(int(note_comments) + 1), 2)) + 0.4 * (
                                         pow(log(int(note_coll) + 1), 2))), 2)
                                # 特征词
                                # if note_info['ats']:
                                #     note_ats = [note_info['ats'][i]['nickname'] for i in
                                #                 range(len(note_info['ats']))]
                                # else:
                                note_ats = []
                                note_tags = note_ats
                                note_tag = []
                                for j in note_tags:
                                    if isinstance(j, dict):
                                        note_tag.append(j['name'])
                                    else:
                                        note_tag.append(j)
                                note_tag = str(note_tag)
                                interaction = int(note_collected_like) / int(user_fans_num)
                                interaction = round(interaction, 2)
                                ws.append([user_url, nickname, sign, user_level, user_location, user_fans_num,
                                           user_fans_level,
                                           user_like_num, user_follows_num, user_collected_num, user_like_collected_num,
                                           note_num, note_url, note_type, note_title, note_content, note_time, note_ts,
                                           note_likes, note_comments, note_coll, note_share, note_collected_like,
                                           interaction,
                                           score, note_cooperate_binds, note_tag])
                                print([user_url, nickname, sign, user_level, user_location, user_fans_num,
                                       user_fans_level,
                                       user_like_num, user_follows_num, user_collected_num, user_like_collected_num,
                                       note_num, note_url, note_type, note_title, note_content, note_time, note_ts,
                                       note_likes, note_comments, note_coll, note_share, note_collected_like,
                                       interaction,
                                       score, note_cooperate_binds, note_tag])
                                wb.save(r"./小红书_"
                                        r"{keyword}_08_03_1_result.xlsx".format(keyword=keyword))
                            except Exception as a:
                                print(a)
            except Exception as e:
                print(e)
