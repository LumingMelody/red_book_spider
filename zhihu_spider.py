import re
import time

import requests
import json

from openpyxl import Workbook

wb = Workbook()

ws = wb.active
ws.append([
    "用户名",
    "性别",
    "签名",
    "用户链接",
    "文章链接",
    "发布时间",
    "更新时间",
    "获赞数",
    "评论数",
    "标题",
    "内容"
])
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
}


def timestamp_to_format(timestamp=None, format='%Y-%m-%d %H:%M:%S'):
    # try:
    if timestamp:
        time_tuple = time.localtime(timestamp)
        print('time_tuple:', time_tuple)
        # print('type(time_tuple):',type(time_tuple))
        res = time.strftime(format, time_tuple)
    else:
        res = time.strftime(format)
    return res
    # except:
    #     print('error')


def fetchHotel(url):
    # 发起网络请求，获取数据

    # 发起网络请求
    r = requests.get(url, headers=headers)
    r.encoding = 'Unicode'
    # print(r.text)
    return r.text


def parseJson(text):
    json_data = json.loads(text)
    lst = json_data['data']

    nextUrl = json_data['paging']['next']

    if not lst:
        return;

    for item in lst:
        print(item)
        type = item['target']['type']
        content = item['target']['content']
        new_content = re.sub(r'<.*?>', '', content)

        auth = ""
        title = ""
        url = ""
        new_create_time = ""
        vote = ""
        cmts = ""
        gender = ""
        headline = ""
        new_updated_time = ""
        author_url = ""
        if type == 'answer':
            # 回答
            question = item['target']['question']
            auth = item['target']['author']['name']
            create_time = item['target']['question']['created_time']
            new_create_time = timestamp_to_format(create_time)
            vote = item['target']['voteup_count']
            cmts = item['target']['comment_count']
            gender = item['target']['author']['gender']
            updated_time = item['target']['question']['updated_time']
            new_updated_time = timestamp_to_format(updated_time)
            if gender == 1:
                gender = "男"
            else:
                gender = "女"
            headline = item['target']['author']['headline']
            a_url = item['target']['author']['url']
            author_url = a_url.replace("api.", "")
            print(author_url)
            id = question['id']
            title = question['title']
            url = 'https://www.zhihu.com/question/' + str(id)

            print("问题：", id, title)

        elif type == 'article':
            # 专栏
            zhuanlan = item['target']
            id = zhuanlan['id']
            title = zhuanlan['title']
            url = zhuanlan['url']
            vote = zhuanlan['voteup_count']
            cmts = zhuanlan['comment_count']
            auth = zhuanlan['author']['name']
            create_time = item['target']['created']
            new_create_time = timestamp_to_format(create_time)
            a_url = item['target']['author']['url']
            author_url = a_url.replace("api.", "")
            print("专栏：", id, title)

        elif type == 'question':
            # 问题
            question = item['target']
            id = question['id']
            title = question['title']
            url = 'https://www.zhihu.com/question/' + str(id)
            a_url = item['target']['author']['url']
            author_url = a_url.replace("api.", "")
            print("问题：", id, title)
        ws.append([auth, gender, headline, author_url, url, new_create_time, new_updated_time, vote, cmts, title,
                   new_content])
    wb.save("D:/知乎/知乎_0618_折叠屏.xlsx")
    return nextUrl


if __name__ == '__main__':
    topicID = '20752345'
    url = 'https://www.zhihu.com/api/v4/topics/' + topicID + '/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id=0'
    while url:
        # print(url)
        text = fetchHotel(url)
        url = parseJson(text)
