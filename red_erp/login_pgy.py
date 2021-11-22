"""
@version: 1.0
@author: anne
@contact: thy.self@foxmail.com
@time: 2021/8/16 下午4:40
"""
import datetime
import json
import random
import re
import time
from hashlib import md5
from urllib import parse
from urllib.parse import quote_plus
import execjs
import requests
from fontTools.ttLib import TTFont
from lxml import etree
from pymongo import MongoClient


class LoginPgy(object):
    """
    如果cookies 失效， 使用register_cookies_header 重新登陆获取一个有效请求头
    """

    @classmethod
    def get_mongo_conn(cls, collection_name):
        user = 'dts-datawarehouse-admin'
        password = 'aowB0y6yQyPOc9h'
        # host = 'dds-m5e296a1c97603741182-pub.mongodb.rds.aliyuncs.com'
        host = 'dds-m5e296a1c97603742468-pub.mongodb.rds.aliyuncs.com'
        port = 3717
        db_name = 'wom-dts-datawarehouse'
        uri = 'mongodb://%s:%s@%s:%s/%s' % (quote_plus(user), quote_plus(password), host, port, db_name)
        client = MongoClient(uri)
        conn = client[db_name][collection_name]
        return conn

    @classmethod
    def get_f_param(cls, canvas):
        import requests

        url = "https://pgy.xiaohongshu.com/"

        payload = {}
        headers = {
            # 'authority': 'pgy.xiaohongshu.com',
            # 'pragma': 'no-cache',
            # 'cache-control': 'no-cache',
            # 'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"macOS"',
            # 'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'sec-fetch-site': 'same-origin',
            # 'sec-fetch-mode': 'navigate',
            # 'sec-fetch-user': '?1',
            # 'sec-fetch-dest': 'document',
            # 'referer': 'https://pgy.xiaohongshu.com/solar/home',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': f'{canvas}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        content_node1 = etree.HTML(response.text)
        content1 = content_node1.xpath('/html/head/script[4]')[0].xpath('string(.)')
        content2 = content_node1.xpath('/html/head/style[1]')[0].xpath('string(.)')
        font_url = re.findall('src:url\(\'(.*?)\'\)', content2, re.S)[0]
        response = requests.get(font_url, headers=headers)
        with open('font.ttf', 'wb') as f:
            f.write(response.content)
        f_param = execjs.compile(content1.replace("window['f'] = f", '')).call('f').get('f')
        return f_param

    @classmethod
    def register_canvas(cls):
        """
        构造指纹画布
        :return:
        """
        params = (
            ('p', 'cc'),
        )
        fp = md5(''.join(
            random.sample("0123456789abcdefghijklmnopqrstevwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 13)).encode()).hexdigest()
        ua = 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36'
        sign = f"{ua}~~~false~~~zh-CN~~~24~~~8~~~12~~~-480~~~Asia/Shanghai~~~1~~~1~~~1~~~1~~~unknown" \
               f"~~~MacIntel~~~Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf,Chrome" \
               f" PDF Viewer::::application/pdf~pdf,Native Client::::application/x-nacl~,application/x-pnacl" \
               f"~~~~canvas winding:yes~canvas fp:{fp}~~~false~~~false~~~false~~~false~~~" \
               f"false~~~0;false;false~~~2;3;6;7;8~~~124.0434806260746"
        id = md5((sign + "hasaki").encode()).hexdigest()
        data = '{"id":"%s","sign":"%s"}' % (id, sign)
        headers = {
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
        response = requests.post('https://www.xiaohongshu.com/fe_api/burdock/v2/shield/registerCanvas', headers=headers,
                                 params=params, data=data, verify=False)
        resp_headers = response.headers
        if resp_headers.get("set-cookie"):
            timestamp2 = re.findall(r'timestamp2=(.*?);', resp_headers["set-cookie"])[0]
            timestamp2_sig = re.findall(r'timestamp2\.sig=(.*?);', resp_headers["set-cookie"])[0]
            cookie = f"timestamp2={timestamp2};timestamp2.sig={timestamp2_sig};"
        else:
            cookie = ""
        return cookie

    @classmethod
    def register_sign(cls, url, payload):
        """
        x-t/x-s 加密
        :param url:
        :param payload:
        :return:
        """
        if parse.urlparse(url).query != '':
            path = parse.urlparse(url).path + '?' + parse.urlparse(url).query
        else:
            path = parse.urlparse(url).path
        print(path)
        jsStr = """function sign(_0x5c15ff,_0x22b14c){var _0x2b2945=function(_0x3f4e97){function _0x373b69(_0xe84468){if(_0x5891ec[_0xe84468])return _0x5891ec[_0xe84468]["exports"];var _0x5b5539=_0x5891ec[_0xe84468]={'i':_0xe84468,'l':false,'exports':{}};_0x3f4e97[_0xe84468]["call"](_0x5b5539["exports"],_0x5b5539,_0x5b5539["exports"],_0x373b69);_0x5b5539['l']=true;return _0x5b5539["exports"];}var _0x5891ec={};_0x373b69['m']=_0x3f4e97;_0x373b69['c']=_0x5891ec;_0x373b69['i']=function(_0x431e2d){return _0x431e2d;};_0x373b69['d']=function(_0x4681ea,_0x211f64,_0x7f7050){_0x373b69['o'](_0x4681ea,_0x211f64)||Object["defineProperty"](_0x4681ea,_0x211f64,{'configurable':false,'enumerable':true,'get':_0x7f7050});};_0x373b69['n']=function(_0xe31015){var _0x5891ec=_0xe31015&&_0xe31015["__esModule"]?function(){return _0xe31015["default"];}:function(){return _0xe31015;};_0x373b69['d'](_0x5891ec,'a',_0x5891ec);return _0x5891ec;};_0x373b69['o']=function(_0x493a20,_0x701279){return Object["prototype"]["hasOwnProperty"]["call"](_0x493a20,_0x701279);};_0x373b69['p']='';return _0x373b69(_0x373b69['s']=4);}([function(_0x11c34c,_0x3e9228){var _0x17cf34={'utf8':{'stringToBytes':function(_0x4dca7a){return _0x17cf34["bin"]["stringToBytes"](unescape(encodeURIComponent(_0x4dca7a)));},'bytesToString':function(_0x2c2c5c){return decodeURIComponent(escape(_0x17cf34["bin"]["bytesToString"](_0x2c2c5c)));}},'bin':{'stringToBytes':function(_0x568d3f){for(var _0x3e9228=[],_0x17cf34=0;_0x17cf34<_0x568d3f["length"];_0x17cf34++){_0x3e9228["push"](255&_0x568d3f["charCodeAt"](_0x17cf34));}return _0x3e9228;},'bytesToString':function(_0x3abb0d){for(var _0x3e9228=[],_0x17cf34=0;_0x17cf34<_0x3abb0d["length"];_0x17cf34++){_0x3e9228["push"](String["fromCharCode"](_0x3abb0d[_0x17cf34]));}return _0x3e9228["join"]('');}}};_0x11c34c["exports"]=_0x17cf34;},function(_0x221379,_0x22ba93,_0x3dc3e2){!function(){var _0x22ba93=_0x3dc3e2(2);var _0x57def5=_0x3dc3e2(0)["utf8"];var _0x551f23=_0x3dc3e2(3);var _0x24d663=_0x3dc3e2(0)["bin"];function _0x5b77c1(_0x30ddd1,_0x877731){_0x30ddd1["constructor"]==String?_0x30ddd1=_0x877731&&"binary"===_0x877731["encoding"]?_0x24d663["stringToBytes"](_0x30ddd1):_0x57def5["stringToBytes"](_0x30ddd1):_0x551f23(_0x30ddd1)?_0x30ddd1=Array["prototype"]["slice"]["call"](_0x30ddd1,0):Array["isArray"](_0x30ddd1)||(_0x30ddd1=_0x30ddd1["toString"]());for(var _0x4836e9=_0x22ba93["bytesToWords"](_0x30ddd1),_0x324197=8*_0x30ddd1["length"],_0x4e502f=1732584193,_0x20296f=-271733879,_0xa1451d=-1732584194,_0x443ed4=271733878,_0x49f435=0;_0x49f435<_0x4836e9["length"];_0x49f435++){_0x4836e9[_0x49f435]=16711935&(_0x4836e9[_0x49f435]<<8|_0x4836e9[_0x49f435]>>>24)|4278255360&(_0x4836e9[_0x49f435]<<24|_0x4836e9[_0x49f435]>>>8);}_0x4836e9[_0x324197>>>5]|=128<<_0x324197%32;_0x4836e9[14+(_0x324197+64>>>9<<4)]=_0x324197;for(var _0x10c1fe=_0x5b77c1["_ff"],_0x5c0f6c=_0x5b77c1["_gg"],_0x2ddd5b=_0x5b77c1["_hh"],_0x5f1798=_0x5b77c1["_ii"],_0x49f435=0;_0x49f435<_0x4836e9["length"];_0x49f435+=16){var _0x4a20e3=_0x4e502f;var _0x43476e=_0x20296f;var _0x2eea87=_0xa1451d;var _0xb8b261=_0x443ed4;_0x4e502f=_0x10c1fe(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+0],7,-680876936);_0x443ed4=_0x10c1fe(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+1],12,-389564586);_0xa1451d=_0x10c1fe(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+2],17,606105819);_0x20296f=_0x10c1fe(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+3],22,-1044525330);_0x4e502f=_0x10c1fe(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+4],7,-176418897);_0x443ed4=_0x10c1fe(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+5],12,1200080426);_0xa1451d=_0x10c1fe(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+6],17,-1473231341);_0x20296f=_0x10c1fe(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+7],22,-45705983);_0x4e502f=_0x10c1fe(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+8],7,1770035416);_0x443ed4=_0x10c1fe(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+9],12,-1958414417);_0xa1451d=_0x10c1fe(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+10],17,-42063);_0x20296f=_0x10c1fe(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+11],22,-1990404162);_0x4e502f=_0x10c1fe(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+12],7,1804603682);_0x443ed4=_0x10c1fe(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+13],12,-40341101);_0xa1451d=_0x10c1fe(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+14],17,-1502002290);_0x20296f=_0x10c1fe(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+15],22,1236535329);_0x4e502f=_0x5c0f6c(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+1],5,-165796510);_0x443ed4=_0x5c0f6c(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+6],9,-1069501632);_0xa1451d=_0x5c0f6c(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+11],14,643717713);_0x20296f=_0x5c0f6c(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+0],20,-373897302);_0x4e502f=_0x5c0f6c(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+5],5,-701558691);_0x443ed4=_0x5c0f6c(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+10],9,38016083);_0xa1451d=_0x5c0f6c(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+15],14,-660478335);_0x20296f=_0x5c0f6c(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+4],20,-405537848);_0x4e502f=_0x5c0f6c(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+9],5,568446438);_0x443ed4=_0x5c0f6c(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+14],9,-1019803690);_0xa1451d=_0x5c0f6c(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+3],14,-187363961);_0x20296f=_0x5c0f6c(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+8],20,1163531501);_0x4e502f=_0x5c0f6c(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+13],5,-1444681467);_0x443ed4=_0x5c0f6c(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+2],9,-51403784);_0xa1451d=_0x5c0f6c(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+7],14,1735328473);_0x20296f=_0x5c0f6c(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+12],20,-1926607734);_0x4e502f=_0x2ddd5b(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+5],4,-378558);_0x443ed4=_0x2ddd5b(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+8],11,-2022574463);_0xa1451d=_0x2ddd5b(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+11],16,1839030562);_0x20296f=_0x2ddd5b(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+14],23,-35309556);_0x4e502f=_0x2ddd5b(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+1],4,-1530992060);_0x443ed4=_0x2ddd5b(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+4],11,1272893353);_0xa1451d=_0x2ddd5b(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+7],16,-155497632);_0x20296f=_0x2ddd5b(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+10],23,-1094730640);_0x4e502f=_0x2ddd5b(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+13],4,681279174);_0x443ed4=_0x2ddd5b(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+0],11,-358537222);_0xa1451d=_0x2ddd5b(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+3],16,-722521979);_0x20296f=_0x2ddd5b(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+6],23,76029189);_0x4e502f=_0x2ddd5b(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+9],4,-640364487);_0x443ed4=_0x2ddd5b(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+12],11,-421815835);_0xa1451d=_0x2ddd5b(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+15],16,530742520);_0x20296f=_0x2ddd5b(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+2],23,-995338651);_0x4e502f=_0x5f1798(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+0],6,-198630844);_0x443ed4=_0x5f1798(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+7],10,1126891415);_0xa1451d=_0x5f1798(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+14],15,-1416354905);_0x20296f=_0x5f1798(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+5],21,-57434055);_0x4e502f=_0x5f1798(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+12],6,1700485571);_0x443ed4=_0x5f1798(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+3],10,-1894986606);_0xa1451d=_0x5f1798(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+10],15,-1051523);_0x20296f=_0x5f1798(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+1],21,-2054922799);_0x4e502f=_0x5f1798(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+8],6,1873313359);_0x443ed4=_0x5f1798(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+15],10,-30611744);_0xa1451d=_0x5f1798(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+6],15,-1560198380);_0x20296f=_0x5f1798(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+13],21,1309151649);_0x4e502f=_0x5f1798(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+4],6,-145523070);_0x443ed4=_0x5f1798(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+11],10,-1120210379);_0xa1451d=_0x5f1798(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+2],15,718787259);_0x20296f=_0x5f1798(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+9],21,-343485551);_0x4e502f=_0x4e502f+_0x4a20e3>>>0;_0x20296f=_0x20296f+_0x43476e>>>0;_0xa1451d=_0xa1451d+_0x2eea87>>>0;_0x443ed4=_0x443ed4+_0xb8b261>>>0;}return _0x22ba93["endian"]([_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4]);}_0x5b77c1["_ff"]=function(_0xeba622,_0x58d10c,_0x26ec12,_0x3619d7,_0x30a53e,_0x2e41a2,_0x51ea77){var _0x2dd6f9=_0xeba622+(_0x58d10c&_0x26ec12|~_0x58d10c&_0x3619d7)+(_0x30a53e>>>0)+_0x51ea77;return(_0x2dd6f9<<_0x2e41a2|_0x2dd6f9>>>32-_0x2e41a2)+_0x58d10c;};_0x5b77c1["_gg"]=function(_0x467b43,_0x19e3cd,_0x542286,_0x43649a,_0x1eb403,_0x55281d,_0x56fb7b){var _0x1ff6fb=_0x467b43+(_0x19e3cd&_0x43649a|_0x542286&~_0x43649a)+(_0x1eb403>>>0)+_0x56fb7b;return(_0x1ff6fb<<_0x55281d|_0x1ff6fb>>>32-_0x55281d)+_0x19e3cd;};_0x5b77c1["_hh"]=function(_0x26167d,_0x48cc80,_0x50bb6c,_0xaf3712,_0x3a9877,_0x20d15e,_0x26b99a){var _0xc3d46a=_0x26167d+(_0x48cc80^_0x50bb6c^_0xaf3712)+(_0x3a9877>>>0)+_0x26b99a;return(_0xc3d46a<<_0x20d15e|_0xc3d46a>>>32-_0x20d15e)+_0x48cc80;};_0x5b77c1["_ii"]=function(_0x35a638,_0x5e1c48,_0x29acc8,_0x374dc2,_0x5bf40b,_0x11a4cc,_0x48f550){var _0x2ee2cf=_0x35a638+(_0x29acc8^(_0x5e1c48|~_0x374dc2))+(_0x5bf40b>>>0)+_0x48f550;return(_0x2ee2cf<<_0x11a4cc|_0x2ee2cf>>>32-_0x11a4cc)+_0x5e1c48;};_0x5b77c1["_blocksize"]=16;_0x5b77c1["_digestsize"]=16;_0x221379["exports"]=function(_0x1dd3ba,_0x497160){if(void 0===_0x1dd3ba||null===_0x1dd3ba)throw new Error("Illegal argument "+_0x1dd3ba);var _0x57def5=_0x22ba93["wordsToBytes"](_0x5b77c1(_0x1dd3ba,_0x497160));return _0x497160&&_0x497160["asBytes"]?_0x57def5:_0x497160&&_0x497160["asString"]?_0x24d663["bytesToString"](_0x57def5):_0x22ba93["bytesToHex"](_0x57def5);};}();},function(_0x26a4ff,_0x46a92e){!function(){var _0x46a92e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";var _0xb27353={'rotl':function(_0x2f234f,_0x2bd3a5){return _0x2f234f<<_0x2bd3a5|_0x2f234f>>>32-_0x2bd3a5;},'rotr':function(_0x31246e,_0x3f5395){return _0x31246e<<32-_0x3f5395|_0x31246e>>>_0x3f5395;},'endian':function(_0xcdcafa){if(_0xcdcafa["constructor"]==Number)return 16711935&_0xb27353["rotl"](_0xcdcafa,8)|4278255360&_0xb27353["rotl"](_0xcdcafa,24);for(var _0x46a92e=0;_0x46a92e<_0xcdcafa["length"];_0x46a92e++){_0xcdcafa[_0x46a92e]=_0xb27353["endian"](_0xcdcafa[_0x46a92e]);}return _0xcdcafa;},'randomBytes':function(_0x3f6b01){for(var _0x46a92e=[];_0x3f6b01>0;_0x3f6b01--){_0x46a92e["push"](Math["floor"](256*Math["random"]()));}return _0x46a92e;},'bytesToWords':function(_0x10328c){for(var _0x46a92e=[],_0xb27353=0,_0x114556=0;_0xb27353<_0x10328c["length"];_0xb27353++,_0x114556+=8){_0x46a92e[_0x114556>>>5]|=_0x10328c[_0xb27353]<<24-_0x114556%32;}return _0x46a92e;},'wordsToBytes':function(_0x46c672){for(var _0x46a92e=[],_0xb27353=0;_0xb27353<32*_0x46c672["length"];_0xb27353+=8){_0x46a92e["push"](_0x46c672[_0xb27353>>>5]>>>24-_0xb27353%32&255);}return _0x46a92e;},'bytesToHex':function(_0xaaea8e){for(var _0x46a92e=[],_0xb27353=0;_0xb27353<_0xaaea8e["length"];_0xb27353++){_0x46a92e["push"]((_0xaaea8e[_0xb27353]>>>4)["toString"](16));_0x46a92e["push"]((15&_0xaaea8e[_0xb27353])["toString"](16));}return _0x46a92e["join"]('');},'hexToBytes':function(_0x305581){for(var _0x46a92e=[],_0xb27353=0;_0xb27353<_0x305581["length"];_0xb27353+=2){_0x46a92e["push"](parseInt(_0x305581["substr"](_0xb27353,2),16));}return _0x46a92e;},'bytesToBase64':function(_0x31be9b){for(var _0xb27353=[],_0x4f8bf0=0;_0x4f8bf0<_0x31be9b["length"];_0x4f8bf0+=3)for(var _0x1c52c0=_0x31be9b[_0x4f8bf0]<<16|_0x31be9b[_0x4f8bf0+1]<<8|_0x31be9b[_0x4f8bf0+2],_0x7887e9=0;_0x7887e9<4;_0x7887e9++){8*_0x4f8bf0+6*_0x7887e9<=8*_0x31be9b["length"]?_0xb27353["push"](_0x46a92e["charAt"](_0x1c52c0>>>6*(3-_0x7887e9)&63)):_0xb27353["push"]('=');}return _0xb27353["join"]('');},'base64ToBytes':function(_0x5f4654){_0x5f4654=_0x5f4654["replace"](/[^A-Z0-9+\/]/gi,'');for(var _0xb27353=[],_0x1e7149=0,_0x3183be=0;_0x1e7149<_0x5f4654["length"];_0x3183be=++_0x1e7149%4){0!=_0x3183be&&_0xb27353["push"]((_0x46a92e["indexOf"](_0x5f4654["charAt"](_0x1e7149-1))&Math["pow"](2,-2*_0x3183be+8)-1)<<2*_0x3183be|_0x46a92e["indexOf"](_0x5f4654["charAt"](_0x1e7149))>>>6-2*_0x3183be);}return _0xb27353;}};_0x26a4ff["exports"]=_0xb27353;}();},function(_0x4de4dd,_0x3154cb){function _0x1a115e(_0x47dad5){return!!_0x47dad5["constructor"]&&"function"==typeof _0x47dad5["constructor"]["isBuffer"]&&_0x47dad5["constructor"]["isBuffer"](_0x47dad5);}function _0x906d89(_0x4aed2d){return"function"==typeof _0x4aed2d["readFloatLE"]&&"function"==typeof _0x4aed2d["slice"]&&_0x1a115e(_0x4aed2d["slice"](0,0));}_0x4de4dd["exports"]=function(_0x104dba){return null!=_0x104dba&&(_0x1a115e(_0x104dba)||_0x906d89(_0x104dba)||!!_0x104dba["_isBuffer"]);};},function(_0x23f4aa,_0x92abbe,_0x1075a7){_0x23f4aa["exports"]=_0x1075a7(1);}]);function _0x553c8a(_0x3b145c){_0x3b145c=_0x3b145c["replace"](/\\r\\n/g,"\\n");var _0x9d1b65='';for(var _0x48a1c5=0;_0x48a1c5<_0x3b145c["length"];_0x48a1c5++){var _0x20b781=_0x3b145c["charCodeAt"](_0x48a1c5);if(_0x20b781<128){_0x9d1b65+=String["fromCharCode"](_0x20b781);}else if(_0x20b781>127&&_0x20b781<2048){_0x9d1b65+=String["fromCharCode"](_0x20b781>>6|192);_0x9d1b65+=String["fromCharCode"](_0x20b781&63|128);}else{_0x9d1b65+=String["fromCharCode"](_0x20b781>>12|224);_0x9d1b65+=String["fromCharCode"](_0x20b781>>6&63|128);_0x9d1b65+=String["fromCharCode"](_0x20b781&63|128);}}return _0x9d1b65;}var _0x59d459="A4NjFqYu5wPHsO0XTdDgMa2r1ZQocVte9UJBvk6/7=yRnhISGKblCWi+LpfE8xzm3";function _0x4c4a9b(_0x6ad198){var _0x2d2acc='';var _0x312581;var _0x11fbd2;var _0x3381c3;var _0x3df8b2;var _0x1e474a;var _0x208c02;var _0x155a6e;var _0xf24116=0;_0x6ad198=_0x553c8a(_0x6ad198);while(_0xf24116<_0x6ad198["length"]){_0x312581=_0x6ad198["charCodeAt"](_0xf24116++);_0x11fbd2=_0x6ad198["charCodeAt"](_0xf24116++);_0x3381c3=_0x6ad198["charCodeAt"](_0xf24116++);_0x3df8b2=_0x312581>>2;_0x1e474a=(_0x312581&3)<<4|_0x11fbd2>>4;_0x208c02=(_0x11fbd2&15)<<2|_0x3381c3>>6;_0x155a6e=_0x3381c3&63;if(isNaN(_0x11fbd2)){_0x208c02=_0x155a6e=64;}else if(isNaN(_0x3381c3)){_0x155a6e=64;}_0x2d2acc=_0x2d2acc+_0x59d459["charAt"](_0x3df8b2)+_0x59d459["charAt"](_0x1e474a)+_0x59d459["charAt"](_0x208c02)+_0x59d459["charAt"](_0x155a6e);}return _0x2d2acc;}var _0xe31de9=new Date()["getTime"]();var _0x8e21aa=Object["prototype"]["toString"]["call"](_0x22b14c)==="[object Object]"||Object["prototype"]["toString"]["call"](_0x22b14c)==="[object Array]";return{'X-s':_0x4c4a9b(_0x2b2945([_0xe31de9,"test",_0x5c15ff,_0x8e21aa?JSON["stringify"](_0x22b14c):'']["join"](''))),'X-t':_0xe31de9};}"""
        jt = execjs.compile(jsStr).call('sign', path, payload)
        return jt

    @classmethod
    def login_with_account(cls, canvas, account, password, f_params):
        """
        账号密码明文登陆
        :param canvas:
        :return:
        """
        url = "https://customer.xiaohongshu.com/api/cas/loginWithAccount"
        # payload = "{\"account\":\"andy.chen@51wom.com\",\"password\":\"Qm888888\",\"service\":\"https://pgy.xiaohongshu.com\"}"
        payload = "{\"account\":\"" + account + "\",\"password\":\"" + password + "\",\"service\":\"https://pgy.xiaohongshu.com\"}"
        headers = {
            'f': f_params,
            'content-type': 'application/json;charset=UTF-8',
            'authorization': '',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'cookie': f'{canvas}'
        }
        jt = cls.register_sign(url, json.loads(payload))
        headers['x-t'] = str(jt['X-t'])
        headers['x-s'] = jt['X-s']

        response = requests.request("POST", url, headers=headers, data=payload)
        ticket = response.json()['data']
        return ticket

    @classmethod
    def login_with_ticket(cls, canvas, ticket):
        """
        获取session_id，告诉服务器账号登陆成功
        :param canvas:
        :param ticket:
        :return:
        """
        url = "https://pgy.xiaohongshu.com/api/solar/loginWithTicket"

        payload = '{\"ticket\":\"' + ticket + '\"}'
        headers = {
            'content-type': 'application/json;charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'cookie': f'{canvas}'
        }
        jt = cls.register_sign(url, json.loads(payload))
        headers['x-t'] = str(jt['X-t'])
        headers['x-s'] = jt['X-s']

        response = requests.request("POST", url, headers=headers, data=payload)
        session_id = response.headers['Set-Cookie'].split(';')[0].split('=')[-1]
        return session_id

    @classmethod
    def login_cooperate_sign(cls, canvas, session_id):
        """
        账号有kol浏览权限，需要发送请求使session_id 获取数据权限
        :param canvas:
        :param session_id:
        :return:
        """
        url = "https://pgy.xiaohongshu.com/api/solar/kol/get/cooperate/sign"

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': f'{canvas} solar.beaker.session.id={session_id};'
        }
        jt = cls.register_sign(url, None)
        headers['x-t'] = str(jt['X-t'])
        headers['x-s'] = jt['X-s']
        requests.request("GET", url, headers=headers)

    @classmethod
    def login_order_sign(cls, canvas, session_id):
        """
        账号有kol浏览权限，需要发送请求使session_id 获取数据权限
        :param canvas:
        :param session_id:
        :return:
        """

        url = "https://pgy.xiaohongshu.com/api/solar/common/whitelist/brand_cooperate_promotion/userIdIn"

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': f'{canvas} solar.beaker.session.id={session_id};'
        }
        jt = cls.register_sign(url, None)
        headers['x-t'] = str(jt['X-t'])
        headers['x-s'] = jt['X-s']
        resp = requests.request("GET", url, headers=headers)
        print(resp.text)
        url = "https://pgy.xiaohongshu.com/api/solar/common/whitelist/experience_activity_promotion/userIdIn"

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': f'{canvas} solar.beaker.session.id={session_id};'
        }
        jt = cls.register_sign(url, None)
        headers['x-t'] = str(jt['X-t'])
        headers['x-s'] = jt['X-s']
        resp = requests.request("GET", url, headers=headers)
        print(resp.text)

        url = "https://pgy.xiaohongshu.com/api/solar/order/state_counts"

        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': f'{canvas} solar.beaker.session.id={session_id};'
        }
        jt = cls.register_sign(url, None)
        headers['x-t'] = str(jt['X-t'])
        headers['x-s'] = jt['X-s']
        resp = requests.request("GET", url, headers=headers)
        print(resp.text)

        url = "https://pgy.xiaohongshu.com/api/solar/common_check/is_white?checkName=proxy_trade"
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': f'{canvas} solar.beaker.session.id={session_id};'
        }
        jt = cls.register_sign(url, None)
        print(jt)
        headers['x-t'] = str(jt['X-t'])
        headers['x-s'] = jt['X-s']
        resp = requests.request("GET", url, headers=headers)
        print(resp.text)

    @classmethod
    def get_total_page(cls, list_json):
        """
        获取页数
        :param list_json:
        :return:
        """
        print(list_json)
        total = list_json['data']['total']
        page = total // 20
        return page

    @classmethod
    def send_url(cls, headers, url, page):
        """
        pgy 发送请求获取数据
        :param url:
        :return:
        """
        payload = "{\"fansNumberLower\":null,\"fansNumberUpper\":null,\"location\":null,\"cpc\":false,\"column\":\"comprehensiverank\",\"sort\":\"desc\",\"gender\":null,\"personalTags\":[],\"pageNum\":%s,\"pageSize\":20}" % str(
            page)

        jt = cls.register_sign(url, json.loads(payload))
        headers['x-t'] = str(jt['X-t'])
        headers['x-s'] = jt['X-s']

        response = requests.request("POST", url, headers=headers, data=payload)
        timest = int(time.time())
        result = response.json()
        return result

    @classmethod
    def get_kols(cls, headers, uni_map):
        """
        测试获取 列表页数据
        :param headers:
        :return:
        """
        # headers = {
        #     'authority': 'pgy.xiaohongshu.com',
        #     'pragma': 'no-cache',
        #     'cache-control': 'no-cache',
        #     'sec-ch-ua': '^\\^Google',
        #     'x-t': '1630566168474',
        #     'x-b3-traceid': '09b0e54ac3383266',
        #     'f': '77',
        #     'authorization': '',
        #     'content-type': 'application/json;charset=UTF-8',
        #     'accept': 'application/json, text/plain, */*',
        #     'sec-ch-ua-mobile': '?0',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        #     'x-s': 'ZgApOgaUsgOU1isLslFKOl46OB9Ls61GOlakO6FCsjs3',
        #     'sec-ch-ua-platform': '^\\^Windows^\\^',
        #     'origin': 'https://pgy.xiaohongshu.com',
        #     'sec-fetch-site': 'same-origin',
        #     'sec-fetch-mode': 'cors',
        #     'sec-fetch-dest': 'empty',
        #     'referer': 'https://pgy.xiaohongshu.com/solar/advertiser/patterns/kol',
        #     'accept-language': 'zh-CN,zh;q=0.9',
        #     'cookie': 'timestamp2=20210902a1005e42c7f89af53636d120; timestamp2.sig=SLBE2GixEEQSb277QOwxS3xmHimRcJe2MErZGYdJWBM; customerBeakerSessionId=a5a5f44bff68d956a3369abc0932761ccb417e47gAJ9cQAoWBAAAABjdXN0b21lclVzZXJUeXBlcQFLA1gOAAAAX2NyZWF0aW9uX3RpbWVxAkdB2EwbCiZFolgJAAAAYXV0aFRva2VucQNYQQAAADNiMmU5MWI1MWEzMDQ5ZDg5NGZhZDEyYmJiYmViN2NmLTEyZmFmYWI1OGYxZjQzMGVhZGFkNWViNWU1NzM1OGFmcQRYAwAAAF9pZHEFWCAAAABhZjQ3OWQyOTUzMTI0Njk4ODQ2NTkwODI3MGQ3ZWY2Y3EGWA4AAABfYWNjZXNzZWRfdGltZXEHR0HYTBsKJkWiWAYAAAB1c2VySWRxCFgYAAAANWYyY2ZiMGMwOGFjZDg2YzcxZjVhODAzcQl1Lg==; customerClientId=391987312278125; solar.beaker.session.id=1630563368737049690001',
        # }

        url = "https://pgy.xiaohongshu.com/api/solar/cooperator/blogger/v2"
        total_page = cls.get_total_page(cls.send_url(headers, url, page=1))
        for page in range(1, total_page + 1):
            print(page)
            result = cls.send_url(headers, url, page=page)
            result = cls.font_replace(json.dumps(result, ensure_ascii=False), uni_map)
            print(result)
            timest = int(time.time())
            item = {
                "page": page,
                "data": json.dumps(result, ensure_ascii=False),
                "ts": int(time.time()),
                "ts_data": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timest)))
            }
            if result.get('code') != 0 and result.get('success') is False:
                break
            # cls.get_mongo_conn('full_platform_pgy_data_user_list').insert_one(item)

    @classmethod
    def get_note_overall(cls, headers):
        with open(r'C:\python_project\full-official-platform-core-spider\src\services\pgy\json_file\pgy查询.json', "r",
                  encoding='UTF-8') as f:
            r = json.load(f, strict=False)
            for index, i in enumerate(r):
                print(index)
                user_id = i['user_id']
                url = f"https://pgy.xiaohongshu.com/api/solar/kol/data/{user_id}/note_overall"
                jsStr = """function sign(_0x5c15ff,_0x22b14c){var _0x2b2945=function(_0x3f4e97){function _0x373b69(_0xe84468){if(_0x5891ec[_0xe84468])return _0x5891ec[_0xe84468]["exports"];var _0x5b5539=_0x5891ec[_0xe84468]={'i':_0xe84468,'l':false,'exports':{}};_0x3f4e97[_0xe84468]["call"](_0x5b5539["exports"],_0x5b5539,_0x5b5539["exports"],_0x373b69);_0x5b5539['l']=true;return _0x5b5539["exports"];}var _0x5891ec={};_0x373b69['m']=_0x3f4e97;_0x373b69['c']=_0x5891ec;_0x373b69['i']=function(_0x431e2d){return _0x431e2d;};_0x373b69['d']=function(_0x4681ea,_0x211f64,_0x7f7050){_0x373b69['o'](_0x4681ea,_0x211f64)||Object["defineProperty"](_0x4681ea,_0x211f64,{'configurable':false,'enumerable':true,'get':_0x7f7050});};_0x373b69['n']=function(_0xe31015){var _0x5891ec=_0xe31015&&_0xe31015["__esModule"]?function(){return _0xe31015["default"];}:function(){return _0xe31015;};_0x373b69['d'](_0x5891ec,'a',_0x5891ec);return _0x5891ec;};_0x373b69['o']=function(_0x493a20,_0x701279){return Object["prototype"]["hasOwnProperty"]["call"](_0x493a20,_0x701279);};_0x373b69['p']='';return _0x373b69(_0x373b69['s']=4);}([function(_0x11c34c,_0x3e9228){var _0x17cf34={'utf8':{'stringToBytes':function(_0x4dca7a){return _0x17cf34["bin"]["stringToBytes"](unescape(encodeURIComponent(_0x4dca7a)));},'bytesToString':function(_0x2c2c5c){return decodeURIComponent(escape(_0x17cf34["bin"]["bytesToString"](_0x2c2c5c)));}},'bin':{'stringToBytes':function(_0x568d3f){for(var _0x3e9228=[],_0x17cf34=0;_0x17cf34<_0x568d3f["length"];_0x17cf34++){_0x3e9228["push"](255&_0x568d3f["charCodeAt"](_0x17cf34));}return _0x3e9228;},'bytesToString':function(_0x3abb0d){for(var _0x3e9228=[],_0x17cf34=0;_0x17cf34<_0x3abb0d["length"];_0x17cf34++){_0x3e9228["push"](String["fromCharCode"](_0x3abb0d[_0x17cf34]));}return _0x3e9228["join"]('');}}};_0x11c34c["exports"]=_0x17cf34;},function(_0x221379,_0x22ba93,_0x3dc3e2){!function(){var _0x22ba93=_0x3dc3e2(2);var _0x57def5=_0x3dc3e2(0)["utf8"];var _0x551f23=_0x3dc3e2(3);var _0x24d663=_0x3dc3e2(0)["bin"];function _0x5b77c1(_0x30ddd1,_0x877731){_0x30ddd1["constructor"]==String?_0x30ddd1=_0x877731&&"binary"===_0x877731["encoding"]?_0x24d663["stringToBytes"](_0x30ddd1):_0x57def5["stringToBytes"](_0x30ddd1):_0x551f23(_0x30ddd1)?_0x30ddd1=Array["prototype"]["slice"]["call"](_0x30ddd1,0):Array["isArray"](_0x30ddd1)||(_0x30ddd1=_0x30ddd1["toString"]());for(var _0x4836e9=_0x22ba93["bytesToWords"](_0x30ddd1),_0x324197=8*_0x30ddd1["length"],_0x4e502f=1732584193,_0x20296f=-271733879,_0xa1451d=-1732584194,_0x443ed4=271733878,_0x49f435=0;_0x49f435<_0x4836e9["length"];_0x49f435++){_0x4836e9[_0x49f435]=16711935&(_0x4836e9[_0x49f435]<<8|_0x4836e9[_0x49f435]>>>24)|4278255360&(_0x4836e9[_0x49f435]<<24|_0x4836e9[_0x49f435]>>>8);}_0x4836e9[_0x324197>>>5]|=128<<_0x324197%32;_0x4836e9[14+(_0x324197+64>>>9<<4)]=_0x324197;for(var _0x10c1fe=_0x5b77c1["_ff"],_0x5c0f6c=_0x5b77c1["_gg"],_0x2ddd5b=_0x5b77c1["_hh"],_0x5f1798=_0x5b77c1["_ii"],_0x49f435=0;_0x49f435<_0x4836e9["length"];_0x49f435+=16){var _0x4a20e3=_0x4e502f;var _0x43476e=_0x20296f;var _0x2eea87=_0xa1451d;var _0xb8b261=_0x443ed4;_0x4e502f=_0x10c1fe(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+0],7,-680876936);_0x443ed4=_0x10c1fe(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+1],12,-389564586);_0xa1451d=_0x10c1fe(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+2],17,606105819);_0x20296f=_0x10c1fe(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+3],22,-1044525330);_0x4e502f=_0x10c1fe(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+4],7,-176418897);_0x443ed4=_0x10c1fe(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+5],12,1200080426);_0xa1451d=_0x10c1fe(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+6],17,-1473231341);_0x20296f=_0x10c1fe(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+7],22,-45705983);_0x4e502f=_0x10c1fe(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+8],7,1770035416);_0x443ed4=_0x10c1fe(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+9],12,-1958414417);_0xa1451d=_0x10c1fe(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+10],17,-42063);_0x20296f=_0x10c1fe(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+11],22,-1990404162);_0x4e502f=_0x10c1fe(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+12],7,1804603682);_0x443ed4=_0x10c1fe(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+13],12,-40341101);_0xa1451d=_0x10c1fe(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+14],17,-1502002290);_0x20296f=_0x10c1fe(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+15],22,1236535329);_0x4e502f=_0x5c0f6c(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+1],5,-165796510);_0x443ed4=_0x5c0f6c(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+6],9,-1069501632);_0xa1451d=_0x5c0f6c(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+11],14,643717713);_0x20296f=_0x5c0f6c(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+0],20,-373897302);_0x4e502f=_0x5c0f6c(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+5],5,-701558691);_0x443ed4=_0x5c0f6c(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+10],9,38016083);_0xa1451d=_0x5c0f6c(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+15],14,-660478335);_0x20296f=_0x5c0f6c(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+4],20,-405537848);_0x4e502f=_0x5c0f6c(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+9],5,568446438);_0x443ed4=_0x5c0f6c(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+14],9,-1019803690);_0xa1451d=_0x5c0f6c(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+3],14,-187363961);_0x20296f=_0x5c0f6c(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+8],20,1163531501);_0x4e502f=_0x5c0f6c(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+13],5,-1444681467);_0x443ed4=_0x5c0f6c(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+2],9,-51403784);_0xa1451d=_0x5c0f6c(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+7],14,1735328473);_0x20296f=_0x5c0f6c(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+12],20,-1926607734);_0x4e502f=_0x2ddd5b(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+5],4,-378558);_0x443ed4=_0x2ddd5b(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+8],11,-2022574463);_0xa1451d=_0x2ddd5b(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+11],16,1839030562);_0x20296f=_0x2ddd5b(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+14],23,-35309556);_0x4e502f=_0x2ddd5b(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+1],4,-1530992060);_0x443ed4=_0x2ddd5b(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+4],11,1272893353);_0xa1451d=_0x2ddd5b(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+7],16,-155497632);_0x20296f=_0x2ddd5b(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+10],23,-1094730640);_0x4e502f=_0x2ddd5b(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+13],4,681279174);_0x443ed4=_0x2ddd5b(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+0],11,-358537222);_0xa1451d=_0x2ddd5b(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+3],16,-722521979);_0x20296f=_0x2ddd5b(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+6],23,76029189);_0x4e502f=_0x2ddd5b(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+9],4,-640364487);_0x443ed4=_0x2ddd5b(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+12],11,-421815835);_0xa1451d=_0x2ddd5b(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+15],16,530742520);_0x20296f=_0x2ddd5b(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+2],23,-995338651);_0x4e502f=_0x5f1798(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+0],6,-198630844);_0x443ed4=_0x5f1798(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+7],10,1126891415);_0xa1451d=_0x5f1798(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+14],15,-1416354905);_0x20296f=_0x5f1798(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+5],21,-57434055);_0x4e502f=_0x5f1798(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+12],6,1700485571);_0x443ed4=_0x5f1798(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+3],10,-1894986606);_0xa1451d=_0x5f1798(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+10],15,-1051523);_0x20296f=_0x5f1798(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+1],21,-2054922799);_0x4e502f=_0x5f1798(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+8],6,1873313359);_0x443ed4=_0x5f1798(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+15],10,-30611744);_0xa1451d=_0x5f1798(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+6],15,-1560198380);_0x20296f=_0x5f1798(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+13],21,1309151649);_0x4e502f=_0x5f1798(_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4,_0x4836e9[_0x49f435+4],6,-145523070);_0x443ed4=_0x5f1798(_0x443ed4,_0x4e502f,_0x20296f,_0xa1451d,_0x4836e9[_0x49f435+11],10,-1120210379);_0xa1451d=_0x5f1798(_0xa1451d,_0x443ed4,_0x4e502f,_0x20296f,_0x4836e9[_0x49f435+2],15,718787259);_0x20296f=_0x5f1798(_0x20296f,_0xa1451d,_0x443ed4,_0x4e502f,_0x4836e9[_0x49f435+9],21,-343485551);_0x4e502f=_0x4e502f+_0x4a20e3>>>0;_0x20296f=_0x20296f+_0x43476e>>>0;_0xa1451d=_0xa1451d+_0x2eea87>>>0;_0x443ed4=_0x443ed4+_0xb8b261>>>0;}return _0x22ba93["endian"]([_0x4e502f,_0x20296f,_0xa1451d,_0x443ed4]);}_0x5b77c1["_ff"]=function(_0xeba622,_0x58d10c,_0x26ec12,_0x3619d7,_0x30a53e,_0x2e41a2,_0x51ea77){var _0x2dd6f9=_0xeba622+(_0x58d10c&_0x26ec12|~_0x58d10c&_0x3619d7)+(_0x30a53e>>>0)+_0x51ea77;return(_0x2dd6f9<<_0x2e41a2|_0x2dd6f9>>>32-_0x2e41a2)+_0x58d10c;};_0x5b77c1["_gg"]=function(_0x467b43,_0x19e3cd,_0x542286,_0x43649a,_0x1eb403,_0x55281d,_0x56fb7b){var _0x1ff6fb=_0x467b43+(_0x19e3cd&_0x43649a|_0x542286&~_0x43649a)+(_0x1eb403>>>0)+_0x56fb7b;return(_0x1ff6fb<<_0x55281d|_0x1ff6fb>>>32-_0x55281d)+_0x19e3cd;};_0x5b77c1["_hh"]=function(_0x26167d,_0x48cc80,_0x50bb6c,_0xaf3712,_0x3a9877,_0x20d15e,_0x26b99a){var _0xc3d46a=_0x26167d+(_0x48cc80^_0x50bb6c^_0xaf3712)+(_0x3a9877>>>0)+_0x26b99a;return(_0xc3d46a<<_0x20d15e|_0xc3d46a>>>32-_0x20d15e)+_0x48cc80;};_0x5b77c1["_ii"]=function(_0x35a638,_0x5e1c48,_0x29acc8,_0x374dc2,_0x5bf40b,_0x11a4cc,_0x48f550){var _0x2ee2cf=_0x35a638+(_0x29acc8^(_0x5e1c48|~_0x374dc2))+(_0x5bf40b>>>0)+_0x48f550;return(_0x2ee2cf<<_0x11a4cc|_0x2ee2cf>>>32-_0x11a4cc)+_0x5e1c48;};_0x5b77c1["_blocksize"]=16;_0x5b77c1["_digestsize"]=16;_0x221379["exports"]=function(_0x1dd3ba,_0x497160){if(void 0===_0x1dd3ba||null===_0x1dd3ba)throw new Error("Illegal argument "+_0x1dd3ba);var _0x57def5=_0x22ba93["wordsToBytes"](_0x5b77c1(_0x1dd3ba,_0x497160));return _0x497160&&_0x497160["asBytes"]?_0x57def5:_0x497160&&_0x497160["asString"]?_0x24d663["bytesToString"](_0x57def5):_0x22ba93["bytesToHex"](_0x57def5);};}();},function(_0x26a4ff,_0x46a92e){!function(){var _0x46a92e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";var _0xb27353={'rotl':function(_0x2f234f,_0x2bd3a5){return _0x2f234f<<_0x2bd3a5|_0x2f234f>>>32-_0x2bd3a5;},'rotr':function(_0x31246e,_0x3f5395){return _0x31246e<<32-_0x3f5395|_0x31246e>>>_0x3f5395;},'endian':function(_0xcdcafa){if(_0xcdcafa["constructor"]==Number)return 16711935&_0xb27353["rotl"](_0xcdcafa,8)|4278255360&_0xb27353["rotl"](_0xcdcafa,24);for(var _0x46a92e=0;_0x46a92e<_0xcdcafa["length"];_0x46a92e++){_0xcdcafa[_0x46a92e]=_0xb27353["endian"](_0xcdcafa[_0x46a92e]);}return _0xcdcafa;},'randomBytes':function(_0x3f6b01){for(var _0x46a92e=[];_0x3f6b01>0;_0x3f6b01--){_0x46a92e["push"](Math["floor"](256*Math["random"]()));}return _0x46a92e;},'bytesToWords':function(_0x10328c){for(var _0x46a92e=[],_0xb27353=0,_0x114556=0;_0xb27353<_0x10328c["length"];_0xb27353++,_0x114556+=8){_0x46a92e[_0x114556>>>5]|=_0x10328c[_0xb27353]<<24-_0x114556%32;}return _0x46a92e;},'wordsToBytes':function(_0x46c672){for(var _0x46a92e=[],_0xb27353=0;_0xb27353<32*_0x46c672["length"];_0xb27353+=8){_0x46a92e["push"](_0x46c672[_0xb27353>>>5]>>>24-_0xb27353%32&255);}return _0x46a92e;},'bytesToHex':function(_0xaaea8e){for(var _0x46a92e=[],_0xb27353=0;_0xb27353<_0xaaea8e["length"];_0xb27353++){_0x46a92e["push"]((_0xaaea8e[_0xb27353]>>>4)["toString"](16));_0x46a92e["push"]((15&_0xaaea8e[_0xb27353])["toString"](16));}return _0x46a92e["join"]('');},'hexToBytes':function(_0x305581){for(var _0x46a92e=[],_0xb27353=0;_0xb27353<_0x305581["length"];_0xb27353+=2){_0x46a92e["push"](parseInt(_0x305581["substr"](_0xb27353,2),16));}return _0x46a92e;},'bytesToBase64':function(_0x31be9b){for(var _0xb27353=[],_0x4f8bf0=0;_0x4f8bf0<_0x31be9b["length"];_0x4f8bf0+=3)for(var _0x1c52c0=_0x31be9b[_0x4f8bf0]<<16|_0x31be9b[_0x4f8bf0+1]<<8|_0x31be9b[_0x4f8bf0+2],_0x7887e9=0;_0x7887e9<4;_0x7887e9++){8*_0x4f8bf0+6*_0x7887e9<=8*_0x31be9b["length"]?_0xb27353["push"](_0x46a92e["charAt"](_0x1c52c0>>>6*(3-_0x7887e9)&63)):_0xb27353["push"]('=');}return _0xb27353["join"]('');},'base64ToBytes':function(_0x5f4654){_0x5f4654=_0x5f4654["replace"](/[^A-Z0-9+\/]/gi,'');for(var _0xb27353=[],_0x1e7149=0,_0x3183be=0;_0x1e7149<_0x5f4654["length"];_0x3183be=++_0x1e7149%4){0!=_0x3183be&&_0xb27353["push"]((_0x46a92e["indexOf"](_0x5f4654["charAt"](_0x1e7149-1))&Math["pow"](2,-2*_0x3183be+8)-1)<<2*_0x3183be|_0x46a92e["indexOf"](_0x5f4654["charAt"](_0x1e7149))>>>6-2*_0x3183be);}return _0xb27353;}};_0x26a4ff["exports"]=_0xb27353;}();},function(_0x4de4dd,_0x3154cb){function _0x1a115e(_0x47dad5){return!!_0x47dad5["constructor"]&&"function"==typeof _0x47dad5["constructor"]["isBuffer"]&&_0x47dad5["constructor"]["isBuffer"](_0x47dad5);}function _0x906d89(_0x4aed2d){return"function"==typeof _0x4aed2d["readFloatLE"]&&"function"==typeof _0x4aed2d["slice"]&&_0x1a115e(_0x4aed2d["slice"](0,0));}_0x4de4dd["exports"]=function(_0x104dba){return null!=_0x104dba&&(_0x1a115e(_0x104dba)||_0x906d89(_0x104dba)||!!_0x104dba["_isBuffer"]);};},function(_0x23f4aa,_0x92abbe,_0x1075a7){_0x23f4aa["exports"]=_0x1075a7(1);}]);function _0x553c8a(_0x3b145c){_0x3b145c=_0x3b145c["replace"](/\\r\\n/g,"\\n");var _0x9d1b65='';for(var _0x48a1c5=0;_0x48a1c5<_0x3b145c["length"];_0x48a1c5++){var _0x20b781=_0x3b145c["charCodeAt"](_0x48a1c5);if(_0x20b781<128){_0x9d1b65+=String["fromCharCode"](_0x20b781);}else if(_0x20b781>127&&_0x20b781<2048){_0x9d1b65+=String["fromCharCode"](_0x20b781>>6|192);_0x9d1b65+=String["fromCharCode"](_0x20b781&63|128);}else{_0x9d1b65+=String["fromCharCode"](_0x20b781>>12|224);_0x9d1b65+=String["fromCharCode"](_0x20b781>>6&63|128);_0x9d1b65+=String["fromCharCode"](_0x20b781&63|128);}}return _0x9d1b65;}var _0x59d459="A4NjFqYu5wPHsO0XTdDgMa2r1ZQocVte9UJBvk6/7=yRnhISGKblCWi+LpfE8xzm3";function _0x4c4a9b(_0x6ad198){var _0x2d2acc='';var _0x312581;var _0x11fbd2;var _0x3381c3;var _0x3df8b2;var _0x1e474a;var _0x208c02;var _0x155a6e;var _0xf24116=0;_0x6ad198=_0x553c8a(_0x6ad198);while(_0xf24116<_0x6ad198["length"]){_0x312581=_0x6ad198["charCodeAt"](_0xf24116++);_0x11fbd2=_0x6ad198["charCodeAt"](_0xf24116++);_0x3381c3=_0x6ad198["charCodeAt"](_0xf24116++);_0x3df8b2=_0x312581>>2;_0x1e474a=(_0x312581&3)<<4|_0x11fbd2>>4;_0x208c02=(_0x11fbd2&15)<<2|_0x3381c3>>6;_0x155a6e=_0x3381c3&63;if(isNaN(_0x11fbd2)){_0x208c02=_0x155a6e=64;}else if(isNaN(_0x3381c3)){_0x155a6e=64;}_0x2d2acc=_0x2d2acc+_0x59d459["charAt"](_0x3df8b2)+_0x59d459["charAt"](_0x1e474a)+_0x59d459["charAt"](_0x208c02)+_0x59d459["charAt"](_0x155a6e);}return _0x2d2acc;}var _0xe31de9=new Date()["getTime"]();var _0x8e21aa=Object["prototype"]["toString"]["call"](_0x22b14c)==="[object Object]"||Object["prototype"]["toString"]["call"](_0x22b14c)==="[object Array]";return{'X-s':_0x4c4a9b(_0x2b2945([_0xe31de9,"test",_0x5c15ff,_0x8e21aa?JSON["stringify"](_0x22b14c):'']["join"](''))),'X-t':_0xe31de9};}"""
                jt = execjs.compile(jsStr).call('sign', f'/api/solar/kol/data/{user_id}/note_overall', None)
                headers['x-t'] = str(jt['X-t'])
                headers['x-s'] = jt['X-s']

                response = requests.request("get", url, headers=headers)
                result = response.json()
                print(result)
                item = {
                    'note_id': f'{user_id}',
                    'data': json.dumps(result, ensure_ascii=False),
                    'ts_date': datetime.date.today().strftime('%Y%m%d')
                }
                print(item)
                if result.get('code') != 0 and result.get('success') is False:
                    break
                cls.get_mongo_conn('full_platform_pgy_data_user_note_overall').insert_one(item)

    @classmethod
    def register_cookies_header(cls, account, password):
        """
        封装获取header 流程
        :return:
        """
        # 注册指纹
        canvas = cls.register_canvas()
        f_param = cls.get_f_param(canvas)
        # 获取ticket
        ticket = cls.login_with_account(canvas, account, password, f_param)
        # 获取session_id
        session_id = cls.login_with_ticket(canvas, ticket)
        # print(session_id)
        # 授权kols接口权限
        cls.login_cooperate_sign(canvas, session_id)
        # cls.login_order_sign(canvas, session_id)
        return {
            'f': f_param,
            'content-type': 'application/json;charset=UTF-8',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'cookie': f'{canvas} solar.beaker.session.id={session_id};'
        }

    @classmethod
    def get_order(cls, headers):
        url = "https://pgy.xiaohongshu.com/api/solar/order/task/query?pageNum=1&pageSize=20&title=&orderId=&settlementRule=&cooperationType=&orderSource=&commitTimeStart=&commitTimeEnd=&publishTimeStart=&publishTimeEnd=&completeTimeStart=&completeTimeEnd="
        payload = {}
        jt = cls.register_sign(url, None)
        headers['x-t'] = str(jt['X-t'])
        headers['x-s'] = jt['X-s']

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    @classmethod
    def font_replace(cls, str1, uni_map):
        # encode_list = list(map(lambda x: '&#x' + x[3:], uni_list))
        # dict_ttf = dict(zip(encode_list, decode_ttf))
        for k, v in uni_map.items():
            str1 = str1.replace(k + ';', v)
        return json.loads(str1)

    @classmethod
    def get_uni_map(cls):
        xMin_map = {
            76: 0,
            144: 1,
            82: 2,
            63: 3,
            47: 4,
            80: 5,
            79: 6,
            75: 7,
            59: 8,
            78: 9,
        }
        font = TTFont('font.ttf')
        # 读取字体的映射关系
        uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()[4:]
        uni_map = dict()
        for i in uni_list:
            uni_map['&#x' + i[3:]] = str(xMin_map[font['glyf'][i].xMin])
        return uni_map


if __name__ == '__main__':
    # 使用方法，register_cookies_header 应该只获取1次，如果出现验证码，走绕过验证码的手段重新登陆，或者换号登陆
    # cookies_header 应该支持一次性把全部数据拉完
    header = LoginPgy.register_cookies_header('andy.chen@51wom.com', 'Qm888888')
    # LoginPgy.get_order(header)
    uni_map = LoginPgy.get_uni_map()
    LoginPgy.get_kols(header, uni_map)
    # LoginPgy.get_note_overall(header)
