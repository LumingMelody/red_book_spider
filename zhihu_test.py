import re
import requests
import pymysql


class ZhiHuCrawler(object):
    def __init__(self):
        """
        headers         请求头信息
        end_offset      话题下精华问题的最大数目（最大偏移量）
        end_offset2     问题下回答的最大数目（最大偏移量）
        pattern         匹配所有html标签
        patten2         匹配超链接
        comments        爬取的问题的所有评论（格式：[['question_title', 'answer']]）
        q_num           爬取的精华问题的个数
        ans_num         爬取的回答的问题个数
        """
        self.headers = {'content-type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        # self.end_offset = 10
        # self.end_offset2 = 15
        self.pattern = re.compile(r'<[^>]*>')
        self.pattern2 = re.compile(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
        self.comments = []
        self.q_num = 2
        self.ans_num = 4

    # # 将爬取到的评论存入数据库中
    # def saveMysql(self):
    #     """
    #     :return: True / False  (存入数据库操作完成 / 失败)
    #     """
    #     table = 'comment'
    #     drop_sql = "DROP TABLE IF EXISTS {table}".format(table=table)
    #     create_sql = "CREATE TABLE IF NOT EXISTS {table}(comment_id int PRIMARY KEY AUTO_INCREMENT, q_title varchar(255), content text)CHARSET='utf8';".format(
    #         table=table)
    #
    #     data = []
    #     for i in range(len(self.comments)):
    #         data_unit = {
    #             'q_title': self.comments[i][0],
    #             'content': self.comments[i][1]
    #         }
    #         data.append(data_unit)
    #
    #     keys = ','.join(data[0].keys())
    #     values = ','.join(['%s'] * len(data[0]))
    #     insert_sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    #
    #     try:
    #         # 连接数据库
    #         db = pymysql.connect(host="127.0.0.1", user="root", password="123456789",
    #                              database="DataPlatform", port=3306)
    #         cursor = db.cursor()
    #         db.autocommit(False)
    #
    #         # cursor.execute(drop_sql)  # 删表, 测试时使用，看个人需求
    #         cursor.execute(create_sql)
    #         for i in range(len(self.comments)):
    #             cursor.execute(insert_sql, tuple(data[i].values()))
    #
    #         # 提交到数据库并执行
    #         db.commit()
    #         db.autocommit(True)
    #
    #     except Exception as e:
    #         print(e)
    #         # 发生错误时回滚
    #         db.rollback()
    #
    #     finally:
    #         db.close()

    # 爬虫主方法
    def crawl(self, topic_id):
        """
        //:param univ_name:大学名字
        :param topic_id: 知乎上面大学话题的id
        :return: void
        """
        prev = []  # 判断当前问题和之前问题是否重复
        i = 0
        question_num = self.q_num
        answer_num = self.ans_num
        # for i in range(self.q_num):
        while i < question_num:
            json_url = 'https://www.zhihu.com/api/v4/topics/' + str(
                topic_id) + '/feeds/essence?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F' \
                            '(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3D' \
                            'topic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author' \
                            '.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.c' \
                            'ontent%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.' \
                            'target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)' \
                            '%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.annotation_detail%2Ccontent%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(ta' \
                            'rget.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.annotation_detail%2Ccontent%2Cauthor.badge%5B%' \
                            '3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.annotation_detail%2Cco' \
                            'mment_count&offset=' + str(i) + '&limit=' + str(question_num + 10)

            response = requests.get(url=json_url, headers=self.headers, timeout=5)
            exit() if response.status_code != requests.codes.ok else print('Request question Successfully')
            response_json_dict = response.json()
            resp_quesion_data = response_json_dict['data']

            # 判断页面是否到头
            # 这是另一种办法: if response_json_dict.get('paging').get('is_end') is False:
            if resp_quesion_data != []:
                # 获取 question url (知乎 api 版本)
                api_url = resp_quesion_data[0].get('target').get('question').get('url')
                # original_url = 'https://www.zhihu.com/question/' + api_url.split('/')[-1]

                if api_url not in prev:
                    # 获取该 question 下的 answer_num 个 answer
                    for j in range(answer_num):
                        answer_api = api_url + '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2' \
                                               'Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sti' \
                                               'cky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Cedi' \
                                               'table_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreate' \
                                               'd_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelat' \
                                               'ionship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2' \
                                               'A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A' \
                                               '%5D.topics&limit=' + str(answer_num + 10) + '&offset=' + str(j) \
                                     + '&sort_by=default'
                        r = requests.get(url=answer_api, headers=self.headers, timeout=5)
                        exit() if r.status_code != requests.codes.ok else print('Request answer Successfully')
                        r_json_dict = r.json()
                        resq_answer_data = r_json_dict['data']
                        if resq_answer_data != []:
                            content = resq_answer_data[0].get('content')
                            content = re.sub(self.pattern, '', content)
                            content = re.sub(self.pattern2, '，', content)
                            question_title = resq_answer_data[0].get('question').get('title')
                            comment = [question_title, content]
                            self.comments.append(comment)

                    prev.append(api_url)
                    i = i + 1
                else:
                    print("出现了重复问题，加一个新问题")
                    question_num = question_num + 1
                    i = i + 1
                    continue
            else:
                break

        #  评论(多维列表)去重复
        self.comments = list(sorted(set([tuple(t) for t in self.comments])))


if __name__ == '__main__':
    xupt_topic_id = 21606914  # '西安邮电大学'在知乎上话题的id
    crawler = ZhiHuCrawler()
    crawler.crawl(topic_id=xupt_topic_id)
    # crawler.saveMysql()
