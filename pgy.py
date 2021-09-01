import json
import time
from urllib import parse
import json
import execjs
import js2py
import requests
from aiohttp import payload
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws1 = wb.create_sheet()
ws.append([
    "昵称",
    "个人链接",
    "粉丝数",
    '所属机构',
    "图文价格",
    "视频价格",
])

headers = {
    'authority': 'pgy.xiaohongshu.com',
    'cookie': "xhsTrackerId=ce649b22-f7c7-4686-c678-cc14d2c02782; xhsuid=wlNhixrVouQc1xH6; customerClientId=559394368134108; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1617094977,1617094988; smidV2=202104061553193a7c1a21482c01657352bb93535ed8a2007fa273ba4ff5ac0; xhsTracker=url=noteDetail&xhsshare=CopyLink; Hm_lvt_b344979f0455853bf22b3ef05fa7b4ac=1629884216; timestamp2=20210827052eb992f8ab1118f76f8c19; timestamp2.sig=4qtXVzp_wAO1twzPv3VawPMF5gqUtrsFk4pKVv20P9I; customerBeakerSessionId=bbdfdfc003c51a040e2d17669f5d9d263cf18216gAJ9cQAoWBAAAABjdXN0b21lclVzZXJUeXBlcQFLA1gOAAAAX2NyZWF0aW9uX3RpbWVxAkdB2Esk7utDllgJAAAAYXV0aFRva2VucQNYQQAAAGZjOGUwYzdiN2IwMjQ4Y2JiMTcwOTRjYjFmNGFiZTI4LWQ5Mzg4NGVjNGI1ZTQ2NGVhYTAwZTc5OGI1OTI3YzhmcQRYAwAAAF9pZHEFWCAAAAAyMDY2NDBjZjgzMjA0ODA5YmRlMWExZjBkYjAxODEzMnEGWA4AAABfYWNjZXNzZWRfdGltZXEHR0HYSyTu60OWWAYAAAB1c2VySWRxCFgYAAAANWU4MmMwZWU4ZTRmNDU3N2RhOTVmNmYzcQl1Lg==; solar.beaker.session.id=1630311355778083873536",
    "content-type": "application/json;charset=UTF-8",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip,deflate,br",
    "accept-language": "zh-CN,zh;q=0.9",
    'referer': 'https://pgy.xiaohongshu.com/solar/advertiser/patterns/kol',
    'f': '4',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    # 'x-b3-traceid': '11f14ece3487294b',
    'x-s': 'Oid6sgFbslOkOlwU0jslsY5K1isC1gVBsgTiOlT+0jT3',
    'x-t': '1620358434210'
}
headers2 = {
    'authority': 'pgy.xiaohongshu.com',
    'cookie': 'xhsTrackerId=ce649b22-f7c7-4686-c678-cc14d2c02782; xhsuid=wlNhixrVouQc1xH6; customerClientId=559394368134108; Hm_lvt_d0ae755ac51e3c5ff9b1596b0c09c826=1617094977,1617094988; smidV2=202104061553193a7c1a21482c01657352bb93535ed8a2007fa273ba4ff5ac0; xhsTracker=url=noteDetail&xhsshare=CopyLink; Hm_lvt_b344979f0455853bf22b3ef05fa7b4ac=1629884216; timestamp2=20210827052eb992f8ab1118f76f8c19; timestamp2.sig=4qtXVzp_wAO1twzPv3VawPMF5gqUtrsFk4pKVv20P9I; solar.beaker.session.id=1630311355778083873536',
    "content-type": "application/json;charset=UTF-8",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip,deflate,br",
    "accept-language": "zh-CN,zh;q=0.9",
    'f': '4',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    # 'x-b3-traceid': '11f14ece3487294b',
    'x-s': 'Oid6sgFbslOkOlwU0jslsY5K1isC1gVBsgTiOlT+0jT3',
    'x-t': '1620358434210'
}


# url = "https://pgy.xiaohongshu.com/api/solar/cooperator/blogger/v1?minPrice=3000&maxPrice=7000&minFans=100000&maxFans=500000&cpc=false&column=comprehensiverank&sort=asc&location=&type=%E7%BE%8E%E5%A6%86,%E5%AE%B6%E5%B1%85%E5%AE%B6%E8%A3%85,%E6%AF%8D%E5%A9%B4,%E5%85%B4%E8%B6%A3%E7%88%B1%E5%A5%BD,%E6%BD%AE%E6%B5%81&pageNum=20&pageSize=20&userType=0"


# pgy_js = open("decode_func_return_result.js", 'r', encoding='utf-8').read()
# pgy_result = js2py.eval_js(pgy_js)
# def get_sign(api_):
#     with open('pgy1.js', encoding='utf-8') as f:
#         jsData = f.read()
#     p = execjs.compile(jsData).call("sign", api_)
#     return p

def register_sign(url, payload):
    """
    x-t/x-s åŠ å¯†
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


def get_pgy(page):
    # regex_list = [
    #     {'name': ['$E1F2'], 'value': 0},
    #     {'name': ['$EFAB'], 'value': 1},
    #     {'name': ['$EBA3'], 'value': 2},
    #     {'name': ['$ECFA'], 'value': 3},
    #     {'name': ['$EDFD'], 'value': 4},
    #     {'name': ['$EFFA'], 'value': 5},
    #     {'name': ['$EF3A'], 'value': 6},
    #     {'name': ['$E6F5'], 'value': 7},
    #     {'name': ['$ECB2'], 'value': 8},
    #     {'name': ['$E8AE'], 'value': 9},
    # ]
    url = "https://pgy.xiaohongshu.com/api/solar/cooperator/blogger/v2"
    # payload = "{\"fansNumberLower\":null,\"fansNumberUpper\":null,\"location\":null,\"cpc\":false,\"column\":\"comprehensiverank\",\"sort\":\"desc\",\"gender\":null,\"personalTags\":[],\"pageNum\":%s,\"pageSize\":20}" % str(
    #     page)
    payload = "{\"fansNumberLower\":null,\"fansNumberUpper\":null,\"location\":null,\"contentTag\":[\"美妆个护\"],\"cpc\":false,\"column\":\"comprehensiverank\",\"sort\":\"desc\",\"gender\":null,\"personalTags\":[\"测评\"],\"pageNum\":%s,\"pageSize\":20}" % str(
        page)
    jt = register_sign(url, json.loads(payload))
    print(jt)
    headers['x-t'] = str(jt['X-t'])
    headers['x-s'] = jt['X-s']

    response = requests.post(url, headers=headers, data=payload.encode())
    print(response.status_code)
    timest = int(time.time())
    result = response.json()
    print(result)
    # page += 1
    kols = result["data"]["kols"]
    for kol in kols:
        u_id = kol["userId"]
        user_detail_url = f"https://pgy.xiaohongshu.com/api/solar/cooperator/user/blogger/{u_id}"
        sign = register_sign(user_detail_url, payload=None)
        headers2['x-t'] = str(sign['X-t'])
        headers2['x-s'] = sign['X-s']
        resp = requests.get(user_detail_url, headers=headers2).json()
        username = resp['data']['name']
        user_id = resp['data']['userId']
        user_url = f"https://www.xiaohongshu.com/user/profile/{user_id}"
        fans = resp['data']['fansCount']
        if resp['data']['noteSign']:
            noteSign = resp['data']['noteSign']['name']
        else:
            noteSign = None
        picturePrice = resp['data']['picturePrice']
        videoPrice = resp['data']['videoPrice']
        print([username, user_url, fans, noteSign, picturePrice, videoPrice])
        ws.append([username, user_url, fans, noteSign, picturePrice, videoPrice])
        wb.save(r"D:\red_book\pgy\pgy_08_31_1.xlsx")
        time.sleep(2)


if __name__ == '__main__':
    page = 13
    while page <= 43:
        get_pgy(page)
        page += 1
