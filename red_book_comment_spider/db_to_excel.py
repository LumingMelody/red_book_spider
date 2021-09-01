# encoding: utf-8
import time
import pandas as pd
import pymysql


def get_rel(sql):
    '''
    连接mysql数据库，根据条件查询出来我们所需要数据
    :return: 根据条件从sql查询出来的数据
    '''
    try:
        conn = pymysql.connect(host='rm-m5ex13f9qkq9s0w0aso.mysql.rds.aliyuncs.com', port=3306, user='dts_prod_admin',
                               password='i7ny34d87snu7162$',
                               db='dts_prod', charset='utf8mb4')
        # conn = pymysql.connect(host='rm-m5eity96ojo4tlx29ko.mysql.rds.aliyuncs.com', port=3306, user='media_data_pr',
        #                        password='media_51womnji9VFR$',
        #                        db='wom_media', charset='utf8mb4')
    except pymysql.err as err:
        print("报错信息：", err)

    cur = conn.cursor()
    cur.execute(sql)  # 输入要查询的SQL
    rel = cur.fetchall()
    cur.close()
    conn.close()
    return rel


def get_xlsx(rel):
    '''
    把从数据库中查询出来的数据写入excel文件
    :param rel:
    :return:
    '''
    file_name = time.strftime('%Y-%m-%d') + '.xlsx'
    dret = pd.DataFrame.from_records(list(rel))  # mysql查询的结果为元组，需要转换为列表
    dret.to_excel(file_name, index=False, header=("平台", "关键词"))  # header 指定列名，index 默认为True，写行名
    # dret.to_excel(file_name, index=False, header=("昵称", "id", "粉丝数", "url_"))  # header 指定列名，index 默认为True，写行名
    # df = pd.read_excel(file_name)
    # df = df.reset_index(drop=True)
    # df['平台'][df['平台'] == 1] = "微信"
    # df['平台'][df['平台'] == 2] = "微博"
    # df['平台'][df['平台'] == 3] = "小红书"
    # df['平台'][df['平台'] == 4] = "抖音"
    # df['平台'][df['平台'] == 5] = "B站"


if __name__ == '__main__':
    sql = "select platform_code, task_keyword from data_tool_51wom_brief_task where task_limit_endtime BETWEEN '2021-05-28 00:00:00' AND '2021-05-31 00:00:00';"
    # sql = "select name_, account_, fans_num, url_ from media_redbook_account_copy1;"
    rel = get_rel(sql)
    get_xlsx(rel)
