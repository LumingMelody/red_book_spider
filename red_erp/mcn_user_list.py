# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: zhangye
@contact: ye.zhang@amdigital.cn
@time: 2021/7/22 11:26
"""
import datetime
import json
import time
from urllib.parse import quote_plus

import requests
from pymongo import MongoClient


def get_mongo_conn(collection_name):
    user = 'dts-datawarehouse-admin'
    password = 'aowB0y6yQyPOc9h'
    host = 'dds-m5e296a1c97603741182-pub.mongodb.rds.aliyuncs.com'
    port = 3717
    db_name = 'wom-dts-datawarehouse'
    uri = 'mongodb://%s:%s@%s:%s/%s' % (quote_plus(user), quote_plus(password), host, port, db_name)
    client = MongoClient(uri)
    conn = client[db_name][collection_name]
    return conn


class PgyMcnUserList(object):
    @classmethod
    def get_task(cls):
        mcn_list = list(map(lambda x: json.loads(x.get('data')).get('data').get('mcns'),
                            list(get_mongo_conn('full_platform_pgy_data_mcn_list').find())))
        mcn_list = [j['userId'] for i in mcn_list for j in i]

        return mcn_list

    @classmethod
    def get_user_list(cls):
        headers = {
            'authority': 'pgy.xiaohongshu.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'x-t': '1625795474654',
            'x-b3-traceid': '06550277c74c49cb',
            'sec-ch-ua-mobile': '?0',
            'authorization': '',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'f': '3',
            'x-s': '0gAWO6w6sj5p1l1lOisC121iOlTlZB4kOjqUZjvLZYF3',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://pgy.xiaohongshu.com/solar/advertiser/patterns/mcn',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'customerClientId=545776318032072; xhsTrackerId=603e3b3d-848f-4c8b-cc01-a29de3d3b947; smidV2=2020123118041556e44a722898ca5c1d6e281e25da5ed2003ba9f166d157520; xhsuid=uNLILHAtCpGCduO1; xhsTracker=url=index&searchengine=baidu; galaxy.creator.beaker.session.id=1626657780351054168222; timestamp2=20210722f5ec7988daec2eea25001e94; timestamp2.sig=c6m8ljW3BlcQzH1flg_-3Xz5vTIf11J0OEtJ_x92t-Y; customerBeakerSessionId=efada9189a3dff2059fed861db452ccfb3e5c22agAJ9cQAoWBAAAABjdXN0b21lclVzZXJUeXBlcQFLA1gOAAAAX2NyZWF0aW9uX3RpbWVxAkdB2D44tz0/fVgJAAAAYXV0aFRva2VucQNYQQAAAGFiYTc5NTI3ZTUxZjQ2YzY5N2UwMzQwNzQ2OTkxNDhhLTk1OTRkYzU0YjViNzRmZDJhYjFkYzU5NGRiYmYzYzhhcQRYAwAAAF9pZHEFWCAAAAAyNTc0YjE4MjMwMTg0YTMyODlkMWY1ODViZTRiNTM2OHEGWA4AAABfYWNjZXNzZWRfdGltZXEHR0HYPji3PT99WAYAAAB1c2VySWRxCFgYAAAANWU4MmMwZWU4ZTRmNDU3N2RhOTVmNmYzcQl1Lg==; solar.beaker.session.id=1626923741049071246996'
        }
        mcn_list = cls.get_task()
        for id in mcn_list:
            print(id)

            pagenum = 1
            while True:
                print(pagenum)

                url = f'https://pgy.xiaohongshu.com/api/solar/cooperator/mcn/{id}/blogger/v1?column=&sort=&pageNum={pagenum}&pageSize=30'
                response = requests.get(url, headers=headers).json()
                total = response['data']['total']
                total_page = total // 30
                print(total_page)
                pagenum += 1
                if pagenum > total_page+2:
                    break
                # while
                print(response)

                item = {
                    'mcn_id': id,
                    'data': json.dumps(response, ensure_ascii=False),
                    'page' : pagenum-1,
                    'ts_date': datetime.date.today().strftime('%Y%m%d')
                }

                get_mongo_conn('full_platform_pgy_data_mcn_user_list').insert_one(item)


if __name__ == '__main__':
    PgyMcnUserList.get_user_list()