#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: anne
@contact: thy.self@foxmail.com
@time: 2020/9/2 2:33 下午
"""

import re
import requests
import traceback

from urllib.parse import quote

# from src.commons.logging_helper import LoggingHelper

APP_NAME = 'whosecard_open_platform'
# logger = LoggingHelper.get_logger(APP_NAME)

BASE_URI = 'http://whosecard.com:8081'
APP_CONFIG = {
    'KEY': '0a2d21f43ea6cb277e17fd8858cf52b223e69c768d5fe3920687e590'
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
DY_API_PATH = {
    'post': '/api/douyin/aweme/post',
    'favorite': '/api/douyin/aweme/favorite',
    'challenge': '/api/douyin/aweme/challenge',
    'user_detail': '/api/douyin/aweme/user/detail',
    'challenge_detail': '/api/douyin/aweme/challenge/detail',
    'challenge_related': '/api/douyin/aweme/poi/challenge/related',
    'detail': '/api/douyin/aweme/detail',
    'comment': '/api/douyin/aweme/comment',
    'comment_reply': '/api/douyin/aweme/comment/reply',
    'promotion': '/api/douyin/aweme/promotion',
    'product_item': '/api/douyin/haohuo/product/item',
    'search': '/api/douyin/aweme/search',
    'poi_detail': '/api/douyin/aweme/poi/detail',
    'poi_aweme': '/api/douyin/aweme/poi/aweme',
    'user_follower_list': '/api/douyin/aweme/user/follower/list',
    'user_following_list': '/api/douyin/aweme/user/following/list',
    'hotsearch_brand_category': '/api/douyin/aweme/hotsearch/brand/category',
    'hotsearch_brand_weekly_list': '/api/douyin/aweme/hotsearch/brand/weekly/list',
    'hotsearch_brand_billboard': '/api/douyin/aweme/hotsearch/brand/billboard',
    'hotsearch_brand_detail': '/api/douyin/aweme/hotsearch/brand/detail'
}
KS_API_PATH = {
    'userIdInfo': '/api/kuaishou/userIdInfo',
    'userIdInfoFromPhoto': '/api/kuaishou/userIdInfoFromPhoto',
    'profile': '/api/kuaishou/profile',
    'profile_v2': '/api/kuaishou/photo/profile/v2',
    'profile_web_v1': '/api/kuaishou/photo/profile/web/v1',
    'grocery_product': '/api/kuaishou/grocery/product',
    'user_feeds': '/api/kuaishou/user/feeds',
    'tag_feeds': '/api/kuaishou/tag/feeds',
    'tag_info': '/api/kuaishou/tag/info',
    'location_poi': '/api/kuaishou/location/poi',
    'search': '/api/kuaishou/search'
}
WX_API_PATH = {
    'articles': '/api/wx/articles',
    'tmp2forever': '/api/url/transfer/tmp2forever',
    'short2long': '/api/url/transfer/short2long',
    'long2short': '/api/url/transfer/long2short',
    'info': '/api/account/info',
    'ext': '/api/msg/ext',
    'comment': '/api/msg/comment',
    'article': '/api/wx/article',
    'gzh_search': '/api/wx/gzh/search',
    'article_search': '/api/wx/article/search'
}
BZ_API_PATH = {
    'web': '/api/bilibili/web',
}
ZH_API_PATH = {
    'web': '/api/zhihu/web'
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
            return None
    except Exception as e:
        print(f'whosecard 接口错误,错误内容{e},请查看官网.')
        return None


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


class WhosecardDySpider(object):
    """ whosecard 抖音 spider

    """

    @classmethod
    def get_data_from_api_name(cls, api_name, params: dict):
        """
        获取接口数据
        :param api_name:
        :param params:
        :return:
        """
        api_url = f'{BASE_URI}{DY_API_PATH[api_name]}'
        return get_data_from_api_url(api_url, params)

    @classmethod
    def get_search(cls, keyword, cursor=None, search_source='video_search', sort_type=0, publish_time=0):
        """
        获取关键词搜索结果
        :param keyword:
        :param cursor: 上一页会返回下一页的cursor值
        :param search_source: search_source为搜索类型，目前支持以下取值：
  video_search: 搜索视频
  poi: 搜索地点
  user: 搜索用户，此时keyword建议填用户的short_id(抖音号)
  challenge: 搜索话题/挑战
        :param sort_type: sort_type: 对结果排序，取值为 0（综合排序），1（最多点赞），2（最新发布）
        :param publish_time: 限制发布时间，取值为 0（不限），1（一天内），7（一周内），182（半年内）
        :return:
        """
        params = dict()
        params['keyword'] = keyword
        params['cursor'] = cursor
        params['search_source'] = search_source
        params['sort_type'] = sort_type
        params['publish_time'] = publish_time
        return cls.get_data_from_api_name('search', params)

    @classmethod
    def get_post(cls, user_id, max_cursor=None):
        """
        实时获取用户发布的视频列表（按时间排序）
        :param user_id:
        :param max_cursor:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['max_cursor'] = max_cursor
        return cls.get_data_from_api_name('post', params)

    @classmethod
    def get_favorite(cls, user_id, max_cursor=None):
        """
        实时获取用户喜欢（点赞）的视频列表（按时间排序）
        :param user_id:
        :param max_cursor:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['max_cursor'] = max_cursor
        return cls.get_data_from_api_name('favorite', params)

    @classmethod
    def get_challenge(cls, ch_id, is_commerce=1, cursor=None):
        """
        实时获取话题/挑战视频列表（按热度排序）
        :param ch_id:
        :param is_commerce: 参数is_commerce不能为空，此值是从话题/挑战详情接口里获取到的，如果is_commerce=1则表示为商业话题，传0则为普通话题
如果要翻页，需要传入cursor参数（这里的参数跟前面的max_cursor不一样，不要搞混了），此参数在前一页的请求中会返回，每次翻页都会更新。
此接口返回的视频个数可能不固定，具体以实际为准。
        :param cursor:
        :return:
        """
        params = dict()
        params['ch_id'] = ch_id
        params['is_commerce'] = is_commerce
        params['cursor'] = cursor
        return cls.get_data_from_api_name('post', params)

    @classmethod
    def get_user_detail(cls, user_id):
        """
        获取抖音用户详情页
        :param user_id:
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        return cls.get_data_from_api_name('user_detail', params)

    @classmethod
    def get_challenge_detail(cls, ch_id):
        """
        获取话题/挑战详情页
        :param ch_id:
        :return:
        """
        params = dict()
        params['ch_id'] = ch_id
        return cls.get_data_from_api_name('challenge_detail', params)

    @classmethod
    def get_challenge_related(cls, ch_id):
        """
        获取话题/挑战的相关地点
        :param ch_id:
        :return:
        """
        params = dict()
        params['ch_id'] = ch_id
        return cls.get_data_from_api_name('challenge_related', params)

    @classmethod
    def get_detail(cls, aweme_id):
        """
        实时获取单个抖音视频detail信息（不包含播放量）
        :param aweme_id:
        :return:
        """
        params = dict()
        params['aweme_id'] = aweme_id
        return cls.get_data_from_api_name('detail', params)

    @classmethod
    def get_comment(cls, aweme_id, cursor=None):
        """
        获取视频评论列表
        :param aweme_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['aweme_id'] = aweme_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('comment', params)

    @classmethod
    def get_comment_reply(cls, aweme_id, comment_id, cursor=None):
        """
        获取视频评论回复列表
        :param aweme_id:
        :param comment_id:
        :param cursor:
        :return:
        """
        params = dict()
        params['aweme_id'] = aweme_id
        params['comment_id'] = comment_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('comment_reply', params)

    @classmethod
    def get_promotion(cls, user_id, cursor=None):
        """
        获取抖音用户商品橱窗列表
        :param user_id:
        :param cursor: 每次返回10个商品信息，如果要翻页，则需要传入cursor参数，第一次请求时cursor为0，之后每次翻页传的cursor都要加10。
比如当cursor=0时，返回第1-10条商品信息。
比如当cursor=10时，返回第11-20条商品信息。
以此类推，每次请求结果可以根据返回的has_more参数判断是否需要翻页。
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('promotion', params)

    @classmethod
    def get_product_item(cls, url):
        """
        从haohuo获取单个商品详情
        :param url: url参数需要urlencode编码，此参数来自于【获取抖音用户商品橱窗列表】接口的商品链接url字段。
如：https://haohuo.snssdk.com/views/product/item2?id=3320163565905801015&origin_type=3002002000&origin_id=95899249695_3320163565905801015

⚠️ url必须是https://haohuo.snssdk.com开头，否则此接口请求无效（如果是其它链接，如淘宝商品链接，则不要请求此接口）。

        :return:
        """
        params = dict()
        params['url'] = url
        return cls.get_data_from_api_name('product_item', params)

    @classmethod
    def get_poi_detail(cls, poi_id):
        """
        获取根据poi_id获取地点详情页数据
        :param poi_id:
        :return:
        """
        params = dict()
        params['poi_id'] = poi_id
        return cls.get_data_from_api_name('poi_detail', params)

    @classmethod
    def get_poi_aweme(cls, poi_id, cursor=None):
        """
        获取根据poi_id获取地点发布的视频列表
        :param poi_id:
        :param cursor: cursor在翻页时会用到，初始默认为0，如果前一页请求返回的has_more=1，取cursor返回值可获取下一页数据
        :return:
        """
        params = dict()
        params['poi_id'] = poi_id
        params['cursor'] = cursor
        return cls.get_data_from_api_name('poi_aweme', params)

    @classmethod
    def get_user_follower_list(cls, user_id, max_time=None):
        """
        获取获取用户粉丝列表
        :param user_id:
        :param max_time: 如果要翻页，需要传入max_time参数，此参数可从前一页的返回值min_time获取（⚠️这里是min_time，不是max_time），每次翻页都会更新。
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['max_time'] = max_time
        return cls.get_data_from_api_name('user_follower_list', params)

    @classmethod
    def get_user_following_list(cls, user_id, max_time=None):
        """
        获取获取用户关注列表
        :param user_id:
        :param max_time: 如果要翻页，需要传入max_time参数，此参数可从前一页的返回值min_time获取（⚠️这里是min_time，不是max_time），每次翻页都会更新。
        :return:
        """
        params = dict()
        params['user_id'] = user_id
        params['max_time'] = max_time
        return cls.get_data_from_api_name('user_following_list', params)

    @classmethod
    def get_hotsearch_brand_category(cls):
        """
        获取品牌热DOU榜 - 品牌分类列表
        :return:
        """
        params = dict()
        return cls.get_data_from_api_name('hotsearch_brand_category', params)

    @classmethod
    def get_hotsearch_brand_weekly_list(cls, category_id):
        """
        获取品牌热DOU榜 - 指定品牌分类下的历史榜单
        :param category_id:category_id为品牌分类id，从【品牌热DOU榜 - 品牌分类列表】接口获取
        :return:
        """
        params = dict()
        params['category_id'] = category_id
        return cls.get_data_from_api_name('hotsearch_brand_weekly_list', params)

    @classmethod
    def get_hotsearch_brand_billboard(cls, category_id, start_date=''):
        """
        获取品牌热DOU榜 - 指定品牌分类下的指定某一期榜单信息
        :param category_id: category_id为品牌分类id，从【品牌热DOU榜 - 品牌分类列表】接口获取
        :param start_date: start_date为指定某一期榜单，如果为空字符串则取最近一期，可选值从【品牌热DOU榜 - 指定品牌分类下的历史榜单】接口获取
        :return:
        """
        params = dict()
        params['category_id'] = category_id
        params['start_date'] = start_date
        return cls.get_data_from_api_name('hotsearch_brand_billboard', params)

    @classmethod
    def get_hotsearch_brand_detail(cls, category_id, brand_id):
        """
        获取品牌热DOU榜 - 获取单个品牌的详情数据
        :param category_id: category_id为品牌分类id，从【品牌热DOU榜 - 品牌分类列表】接口获取
        :param brand_id: brand_id为品牌id，从【品牌热DOU榜 - 指定品牌分类下的指定某一期榜单信息】接口获取
        :return:
        """
        params = dict()
        params['category_id'] = category_id
        params['brand_id'] = brand_id
        return cls.get_data_from_api_name('hotsearch_brand_detail', params)

    @classmethod
    def share_url_to_normal_url(cls, url):
        """
        分享链接转换
        :param url:
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        if 'sec_uid' in url:
            user_id = url.split('?')[0].split('/')[-1]
            return {
                'retCode': 0,
                'ok': True,
                'result': {
                    'user_id': user_id
                }
            }
        try:
            res = requests.get(url, headers=headers, allow_redirects=False)
        except:
            return {
                'retCode': 1,
                'ok': False,
                'result': {}
            }
        normal_url = res.headers.get('location')
        user_id = normal_url.split('?')[0].split('/')[-1]
        return {
            'retCode': 0,
            'ok': True,
            'result': {
                'user_id': user_id
            }
        }


class WhosecardKsSpider(object):
    """ whosecard 快手 spider

    """

    @classmethod
    def get_data_from_api_name(cls, api_name, params: dict):
        """
        获取接口数据
        :param api_name:
        :param params:
        :return:
        """
        api_url = f'{BASE_URI}{KS_API_PATH[api_name]}'
        return get_data_from_api_url(api_url, params)

    @classmethod
    def get_search(cls, keyword, pcursor=None, ussid=None, search_type='feed'):
        """
        获取关键词搜索结果
        :param keyword:
        :param pcursor: 上一页会返回下一页的pcursor值
        :param ussid: 上一页会返回下一页的ussid值
        :param search_type: 搜索类型，可取值： new(综合), user(用户), imGroup(群聊), tag(标签), feed(作品)
        :return:
        """
        params = dict()
        params['keyword'] = keyword
        params['pcursor'] = pcursor
        params['ussid'] = ussid
        params['search_type'] = search_type
        return cls.get_data_from_api_name('search', params)

    @classmethod
    def get_userIdInfo(cls, shareUrl):
        """
        根据用户分享链接获取用户id信息
        :param shareUrl:
        :return:
        """
        params = dict()
        params['shareUrl'] = quote(shareUrl)
        return cls.get_data_from_api_name('userIdInfo', params)

    @classmethod
    def get_userIdInfoFromPhoto(cls, photoId):
        """
        根据用户任意作品分享链接里的photoId获取用户id信息
        :param photoId:
        :return:
        """
        params = dict()
        params['photoId'] = photoId
        return cls.get_data_from_api_name('userIdInfoFromPhoto', params)

    @classmethod
    def get_profile(cls, userId):
        """
        获取用户个人信息（app版）
        :param userId:
        :return:
        """
        params = dict()
        params['userId'] = userId
        return cls.get_data_from_api_name('profile', params)

    @classmethod
    def get_profile_v2(cls, photo_id):
        """
        获取单个视频的信息（app版，可能不稳定，建议使用web版接口）
        :param photo_id:
        :return:
        """
        params = dict()
        params['photoId'] = photo_id
        return cls.get_data_from_api_name('profile_v2', params)

    @classmethod
    def get_profile_web_v1(cls, share_url, photoId):
        """
        获取单个视频的信息（web版）
        :param share_url:
        :param photoId:
        :return:
        """
        params = dict()
        params['shareUrl'] = share_url
        params['photoId'] = photoId
        return cls.get_data_from_api_name('profile_v2', params)

    @classmethod
    def get_grocery_product(cls, user_id, page=1):
        """
        获取小店商品列表
        :param user_id:
        :param page:
        :return:
        """
        params = dict()
        params['userId'] = user_id
        params['page'] = page
        return cls.get_data_from_api_name('grocery_product', params)

    @classmethod
    def get_user_feeds(cls, user_id, user_eid, pcursor=None):
        """
        获取用户视频流Feed（app版）
        :param user_id:为快手用户唯一数字id。
        :param user_eid:为快手对外的id。
        :param pcursor:用于翻页，第一页不用填，返回结果的pcursor值为下一页的请求参数。
        :return:
        """
        params = dict()
        params['userId'] = user_id
        params['userEid'] = user_eid
        params['pcursor'] = pcursor
        return cls.get_data_from_api_name('user_feeds', params)

    @classmethod
    def get_tag_feeds(cls, tag, feedType='hot', pcursor=None):
        """
        获取tag的Feed流（app版）
        :param tag:为指定话题参数。
        :param feedType:为请求feed类型，一共两种：热门与最近，分别取值为: hot|recent。
        :param pcursor:用于翻页，第一页不用填，返回结果的pcursor值为下一页的请求参数。
        :return:
        """
        params = dict()
        params['tag'] = tag
        params['feedType'] = feedType
        params['pcursor'] = pcursor
        return cls.get_data_from_api_name('tag_feeds', params)

    @classmethod
    def get_tag_info(cls, tag):
        """
        获取tag详情页（app版）
        :param tag:为指定话题参数
        :return:
        """
        params = dict()
        params['tag'] = tag
        return cls.get_data_from_api_name('tag_info', params)

    @classmethod
    def get_location_poi(cls, poiId, subPath, pcursor=None):
        """
        location poi接口（app版）
        :param poiId:为指定话题参数
        :param subPath:为指定话题参数
        :param pcursor:为指定话题参数
        :return:
        """
        params = dict()
        params['poiId'] = poiId
        params['subPath'] = subPath
        params['pcursor'] = pcursor
        return cls.get_data_from_api_name('location_poi', params)

    @classmethod
    def share_url_to_normal_url(cls, url):
        """
        将分享链接转换成标准链接
        https://v.kuaishou.com/5VTFdM to https://c.kuaishou.com/fw/user/3xeyx5nc378dr9g
        :param url:
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
        if 'profile' in url:
            if 'shareObjectId' in url:
                user_id = url.split('?')[0].split('/')[-1]
                user_eid = re.findall(r'shareObjectId=(\d+)', url)[0]
                return {
                    'retCode': 0,
                    'ok': True,
                    'result': {
                        'user_id': int(user_id),
                        'user_eid': user_eid
                    }
                }
            else:
                user_eid = url.split('?')[0].split('/')[-1]
                result = cls.get_profile(user_eid)
                if not result:
                    return {
                        'retCode': 1,
                        'ok': False,
                        'result': {}
                    }
                user_id = result['result']['userProfile']['profile']['user_id']
                return {
                    'retCode': 0,
                    'ok': True,
                    'result': {
                        'user_id': int(user_id),
                        'user_eid': user_eid
                    }
                }
        try:
            res = requests.get(url, headers=headers, allow_redirects=False)
        except:
            print(traceback.format_exc())
            return {
                'retCode': 1,
                'ok': False,
                'result': {}
            }
        normal_url = res.headers.get('location')
        user_eid = normal_url.split('?')[0].split('/')[-1]
        user_id = re.findall(r'shareObjectId=(\d+)', normal_url)[0]
        return {
            'retCode': 0,
            'ok': True,
            'result': {
                'user_id': int(user_id),
                'user_eid': user_eid
            }
        }


class WhosecardWxSpider(object):
    """ whosecard 微信 spider

    """

    @classmethod
    def get_data_from_api_name(cls, api_name, params: dict):
        """
        获取接口数据
        :param api_name:
        :param params:
        :return:
        """
        api_url = f'{BASE_URI}{WX_API_PATH[api_name]}'
        return get_data_from_api_url(api_url, params)

    @classmethod
    def get_search(cls, keyword, start=0, **kwargs):
        """
        获取关键词搜索结果
        :param keyword: 关键词
        :param start: 翻页
        :param kwargs: 其他参数
            query参数解释：
            keyword: 搜索关键词，多个关键词可用空格分开（不分开也可以，会自动分词）
            biz: 公众号biz，限定在此公众号下进行搜索，如: MjM5MjAxNDM4MA==，指定多个公众号时，用半角逗号,分隔
            accountId: 公众号ID，限定在此公众号下进行搜索，如: rmrbwx，指定多个公众号时，用半角逗号,分隔
            accountName: 公众号名称，限定在此公众号下进行搜索，如: 人民日报，指定多个公众号时，用半角逗号,分隔
            start: 文章偏移量，初始值为0，若需翻页，可使用返回结果的nextStart
            startDate: 指定搜索时间的起始日期，搜索时会包含此日期，格式如： 2019-10-01
            endDate: 指定搜索时间的截止日期（如若不填则默认截止到今天），搜索时会包含此日期，格式如： 2019-12-01
            startTime: 指定搜索时间的起始时间戳（单位为秒）
            endTime: 指定搜索时间的截止时间戳（如若不填则默认截止到当前时间戳）（单位为秒）
            sort: 排序，目前支持三种排序，分别为：0(默认排序), 1(按发布时间倒序，最新发布的排在前面), 2(按发布时间增序，最早发布的排在前面)，默认为0
            summary: 如果传1，则title,content会将匹配到的关键词用<em>标签包裹，一般用户搜索高亮显示，默认不开启
            searchRange: 如果传1，则只对标题进行搜索。默认为0，即标题+正文搜素
            searchPos: 如果传1，则只返回头条。默认为0，即不限制文章发布位置
            fullMatch: 如果传1，则必须完整包含搜索词，不会进行分词处理。默认为0，即会进行适当的分词处理后再搜索
            copyrightStat: 如果传1，则只返回原创文章。如果传2，则只返回转载文章。默认为0，即返回所有

            keyword，biz，accountId，accountName这几个参数必须填一个。其中biz，accountId，accountName参数同一时间只能有一个生效，如果填了biz或accountId或accountName且没有填keyword，则会返回该公众号下的所有收录文章。

            ⚠️有时候会发现按时间排序返回的搜索结果不是最新的，那是因为命中的候选文档太多时(超过100w条)，导致最新的反而没有进入搜索候选池，这种情况下需要限制一下过滤条件，比如指定时间范围

            ⚠️本接口支持指定一批公众号范围内进行搜索，多个账号用逗号分隔即可，同一次请求最多指定40个公众号。

            startDate/endDate与startTime/endTime都是限定时间范围的参数，所以同一时间最多只需要传其中一组，当不传时，表示不限制搜索时间。

            此接口每次返回最多10篇文章。只要成功，不管是否有文章，都按照成功收费（比如搜了不存在的关键词）

            ⚠️同一个关键词搜索通过翻页最多能返回5000篇文章，如果总条数大于5000，建议缩小搜索日期进行遍历
        :return:
        """
        params = dict()
        params['keyword'] = keyword
        params['start'] = start

        for i in ['biz', 'accountId', 'accountName', 'startDate', 'endDate', 'startTime', 'endTime', 'sort', 'summary',
                  'searchRange', 'searchPos', 'fullMatch', 'copyrightStat']:
            params[i] = kwargs.get(i)

        return cls.get_data_from_api_name('article_search', params)

    @classmethod
    def get_articles(cls, biz, offset=None):
        """
        实时获取公众号历史发文
        :param biz:
        :param offset:
        :return:
        """
        params = dict()
        params['biz'] = biz
        params['offset'] = offset
        return cls.get_data_from_api_name('articles', params)

    @classmethod
    def get_tmp2forever(cls, url, biz=None, account=None):
        """
        公众号文章临时链接转为永久链接
        :param url:
        :param biz:
        :param account:
        :return:
        """
        params = dict()
        params['url'] = url
        params['biz'] = biz
        params['account'] = account
        return cls.get_data_from_api_name('tmp2forever', params)

    @classmethod
    def get_short2long(cls, url):
        """
        公众号文章短链接转为长链接
        :param url:
        :return:
        """
        params = dict()
        params['url'] = url
        return cls.get_data_from_api_name('short2long', params)

    @classmethod
    def get_long2short(cls, url):
        """
        公众号文章长链接转为短链接
        :param url:
        :return:
        """
        params = dict()
        params['url'] = url
        return cls.get_data_from_api_name('long2short', params)

    @classmethod
    def get_info(cls, account):
        """
        公众号文章长链接转为短链接
        :param url:
        :return:
        """
        params = dict()
        params['account'] = account
        return cls.get_data_from_api_name('info', params)

    @classmethod
    def get_ext(cls, url):
        """
        公众号文章阅读点赞
        :param url:
        :return:
        """
        params = dict()
        params['url'] = url
        return cls.get_data_from_api_name('ext', params)

    @classmethod
    def get_comment(cls, url):
        """
        公众号文章评论
        :param url:
        :return:
        """
        params = dict()
        params['url'] = url
        return cls.get_data_from_api_name('comment', params)

    @classmethod
    def get_article(cls, url):
        """
        公众号文章内容
        默认返回的是json化之后的文章数据，如果只想要原始html页面，可带上参数needJson=0
        :param url:
        :return:
        """
        params = dict()
        params['url'] = url
        return cls.get_data_from_api_name('article', params)

    @classmethod
    def get_gzh_search(cls, keyword, start=0, summary=None):
        """
        公众号账号搜索
        :param keyword:搜索关键词，多个关键词可用空格分开（不分开也可以，会自动分词）
        :param start:文章偏移量，初始值为0，若需翻页，可使用返回结果的nextStart
        :param summary: 如果传1，则nickname,signature会将匹配到的关键词用<em>标签包裹，一般用户搜索高亮显示，默认不开启
        :return:
        """
        params = dict()
        params['keyword'] = keyword
        params['start'] = start
        params['summary'] = summary
        return cls.get_data_from_api_name('gzh_search', params)


class WhosecardBzSpider(object):
    """ whosecard B站 spider

    """

    @classmethod
    def get_data_from_api_name(cls, api_name, params: dict):
        """
        获取接口数据
        :param api_name:
        :param params:
        :return:
        """
        api_url = f'{BASE_URI}{BZ_API_PATH[api_name]}'
        return get_data_from_api_url(api_url, params)

    @classmethod
    def get_web(cls, api, **kwargs):
        """
        获取关键词搜索结果
        :param api:
            获取播放数与阅读数（参数如下）：
            api=user_upstat
            mid=用户id，如 2505015

            获取标签：
            api=user_tags
            mid=用户id，如 2505015

            获取粉丝数，关注数：
            api=user_stat
            mid=用户id，如 2505015

            获取用户充电统计信息：
            api=user_charging
            mid=用户id，如 2505015

            获取用户关注列表：
            api=user_followings
            mid=用户id，如 2505015
            page：翻页数，默认为1

            获取用户粉丝列表：
            api=user_followers
            mid=用户id，如 2505015
            page：翻页数，默认为1

            获取用户基础信息：
            api=user_base
            mid=用户id，如 2505015

            获取投稿页列表，以及投票数量：
            api=user_submit_videos
            mid=用户id，如 2505015
            page：翻页数，默认为1

            获取单条视频的统计数据：
            api=single_stat
            aid=单条视频id，如 35963971

            获取单条视频的tag列表：
            api=detail_tag
            aid=单条视频id，如 35963971

            获取动态历史列表：
            api=user_space_history
            mid=用户id，如 2505015
            offset_dynamic_id： 上一页请求的最后一条动态id，用来翻页，初始为0
        :param kwargs: 其他参数
        :return:
        """
        params = dict()
        params['api'] = api

        params['mid'] = kwargs.get('mid')
        params['aid'] = kwargs.get('aid')
        params['page'] = kwargs.get('page')
        params['offset_dynamic_id'] = kwargs.get('offset_dynamic_id')

        return cls.get_data_from_api_name('web', params)


class WhosecardZhSpider(object):
    """ whosecard 知乎 spider

    """

    @classmethod
    def get_data_from_api_name(cls, api_name, params: dict):
        """
        获取接口数据
        :param api_name:
        :param params:
        :return:
        """
        api_url = f'{BASE_URI}{ZH_API_PATH[api_name]}'
        return get_data_from_api_url(api_url, params)

    @classmethod
    def get_web(cls, api, **kwargs):
        """
        获取关键词搜索结果
        :param api:
            个人主页：
            api=user_info
            urlToken=用户token，如 zhouyuan

            提问页：
            api=question
            offset：用于翻页，下一页的offset参数使用上一页翻回结果的paging.next值
            sortBy: 回答排序，可取值default/updated，默认去default

            搜索页：
            api=search
            q=搜索关键词
            offset：用于翻页，下一页的offset参数使用上一页翻回结果的paging.next值

            评论列表
            api=root_comments
            itemType=作品类型，支持两种:article与answer
            itemId=作品ID
        :param kwargs: 其他参数
        :return:
        """
        params = dict()
        params['api'] = api

        params['q'] = kwargs.get('q')
        params['urlToken'] = kwargs.get('urlToken')
        params['offset'] = kwargs.get('offset')
        params['sortBy'] = kwargs.get('sortBy')
        params['itemType'] = kwargs.get('itemType')
        params['itemId'] = kwargs.get('itemId')

        return cls.get_data_from_api_name('web', params)

    @classmethod
    def get_post(cls, url):
        """
        用户发布，传入用户链接https://www.zhihu.com/people/mu-xi-jin-yuan/posts
        :param url:
        :return:
        """
        headers = {
            'authority': 'www.zhihu.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9'}
        response = requests.get(url, headers=headers)
        text = response.content.decode()
        # html = etree.HTML(text)
        # json_str = html.xpath('/html/body/script[4]//text()')[0]
        # json_str = json_str.replace('null', '0').replace('true', '1').replace("false", '0')
        # json_str = json.loads(json_str)


if __name__ == '__main__':
    result = WhosecardXhsSpider.get_note_comments("607963e700000000010289c7")
    import json

    print(json.dumps(result))

    # print(WhosecardKsSpider.get_userIdInfo('https%3a%2f%2ff.kuaishou.com%2fsnK21'))
