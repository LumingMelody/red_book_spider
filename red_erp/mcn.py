"""
@version: 1.0
@author: anne
@contact: thy.self@foxmail.com
@time: 2021/7/9 9:53 上午
"""
import datetime
import json
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
    'cookie': 'timestamp2=2021071532d4a68dd6c006c4a2ef42d8; timestamp2.sig=gYxLR0k8iN9T3XfrfVG5eluluUEFRbMEBg6SsarXQxM; solar.beaker.session.id=1626405176382056614554; '
}

for i in range(1,28):
    params = (
        ('sort', 'desc'),
        ('column', 'kolCount'),
        ('pageNum', f'{str(i)}'),
        ('pageSize', '20'),
    )

    response = requests.get('https://pgy.xiaohongshu.com/api/solar/cooperator/mcns', headers=headers, params=params)
    print(response.text)

    result = response.json()
    item = {
        'page': i,
        'data': json.dumps(result, ensure_ascii=False),
        'ts_date': datetime.date.today().strftime('%Y%m%d')
    }
    get_mongo_conn('full_platform_pgy_data_mcn_list').insert_one(item)