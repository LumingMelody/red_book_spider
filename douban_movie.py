# !/usr/bin/nev python
# -*-coding:utf8-*-
import os
import random
import tkinter as tk
import xlrd

import jsonpath
import xlwt
from jsonpath import jsonpath
from lxml import etree
from requests_html import HTMLSession
from xlutils.copy import copy

session = HTMLSession()

USER_AGENT_LIST = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
                   'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
                   'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
                   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
                   'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
                   'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
                   'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
                   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
                   'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4093.3 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Swurl) Chrome/77.0.3865.120 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Goanna/4.7 Firefox/68.0 PaleMoon/28.16.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/91.0.146 Chrome/85.0.4183.146 Safari/537.36',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 VivoBrowser/8.4.72.0 Chrome/62.0.3202.84',
                   'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
                   'Mozilla/5.0 (X11; CrOS x86_64 13505.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                   ]


class DBSpider(object):

    def __init__(self):
        """????????????????????????????????????????????????????????????"""
        self.window = tk.Tk()
        self.window.title('????????????????????????')
        self.window.geometry('800x600')

        """??????label_user?????????????????????"""
        self.label_user = tk.Label(self.window, text="?????????????????????????????????'??????','??????','??????','????????????','????????????','??????','??????','??????',"
                                                     "'??????'??????", font=('Arial', 12), width=150, height=2)
        self.label_user.pack()
        """??????label_user????????????"""
        self.entry_user = tk.Entry(self.window, show=None, font=('Arial', 14))
        self.entry_user.pack(after=self.label_user)

        """??????label_passwd?????????????????????"""
        self.label_passwd = tk.Label(self.window, text="???????????????????????????100???", font=('Arial', 12), width=30, height=2)
        self.label_passwd.pack()
        """??????label_passwd????????????"""
        self.entry_passwd = tk.Entry(self.window, show=None, font=('Arial', 14))
        self.entry_passwd.pack(after=self.label_passwd)

        """??????Text????????????????????????????????????????????????"""
        self.text1 = tk.Text(self.window, font=('Arial', 12), width=85, height=22)
        self.text1.pack()

        """????????????1???????????????????????????"""

        self.button_1 = tk.Button(self.window, text='??????', font=('Arial', 12), width=10, height=1,
                                  command=self.parse_hit_click_1)
        self.button_1.pack(before=self.text1)

        """????????????2???????????????????????????"""
        self.button_2 = tk.Button(self.window, text='??????', font=('Arial', 12), width=10, height=1,
                                  command=self.parse_hit_click_2)
        self.button_2.pack(anchor="e")

        self.start_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag={}&sort=time&page_limit=20&page_start={}'
        self.headers = {
            'User-Agent': random.choice(USER_AGENT_LIST)
        }

    def parse_hit_click_1(self):
        """??????????????????1,??????main??????"""
        user_name = self.entry_user.get()
        pass_wd = int(self.entry_passwd.get())
        self.main(user_name, pass_wd)

    def main(self, user_name, pass_wd):

        '''
        url ???????????????
        :return:
        '''

        for i in range(pass_wd):
            try:
                start_url = self.start_url.format(user_name, i * 20)
                response = session.get(start_url, headers=self.headers).json()

                self.respons(response, user_name)

            except:
                print(f'{user_name}====????????????????????????')

    def respons(self, response, user_name):
        '''
        ????????????

        :return:
        '''
        subjects = response['subjects']

        if subjects == []:
            a = subjects[6]
        else:
            '''???????????????'''
            url_list = jsonpath(subjects, '$..url')
            for url in url_list:
                list_1 = []

                res = session.get(url, headers=self.headers).content.decode()

                res = etree.HTML(res)
                '''????????????'''
                title = res.xpath('//h1/span/text()')[0]

                list_1.append(title)
                '''????????????'''
                pf = res.xpath('//strong/text()')[0]

                list_1.append(pf)

                dy_list = []
                '''??????'''
                dy = res.xpath('//div[@id="info"]/span[1]/span[2]/a/text()')
                for d in dy:
                    dy_list.append(d)

                # print(dy)
                '''??????'''
                bj = res.xpath('//div[@id="info"]/span[2]/span[2]/a/text()')
                for b in bj:
                    pass
                # print(bj)
                '''??????'''
                zy = res.xpath('//span[@class="actor"]/span[@class="attrs"]/a/text()')
                # zy = ''.join(zy)
                # print(zy)
                '''??????'''
                lx = res.xpath('//span[@property="v:genre"]/text()')
                # print(lx)
                '''????????????'''
                zp_list = res.xpath('//div[@id="info"]/text()')
                # print(zp_list)
                zp = ''.join(zp_list)

                zp = zp.replace(' ', '').replace('\n', '')
                zp = zp.split('/')
                zp = [i for i in zp if i != '']
                zp = zp[0]

                data = {
                    '????????????': [title, pf, dy, bj, zy, lx, zp]
                }

                self.save_excel(data, title, user_name)

    def save_excel(self, data, title, f):

        os_path_1 = os.getcwd() + '/??????/'
        if not os.path.exists(os_path_1):
            os.mkdir(os_path_1)
        os_path = os_path_1 + '??????.xls'
        if not os.path.exists(os_path):
            # ????????????workbook???????????????????????????excel???
            workbook = xlwt.Workbook(encoding='utf-8')
            # ????????????sheet???
            worksheet1 = workbook.add_sheet("????????????", cell_overwrite_ok=True)
            borders = xlwt.Borders()  # Create Borders
            """??????????????????"""
            borders.left = xlwt.Borders.THIN
            borders.right = xlwt.Borders.THIN
            borders.top = xlwt.Borders.THIN
            borders.bottom = xlwt.Borders.THIN
            borders.left_colour = 0x40
            borders.right_colour = 0x40
            borders.top_colour = 0x40
            borders.bottom_colour = 0x40
            style = xlwt.XFStyle()  # Create Style
            style.borders = borders  # Add Borders to Style
            """??????????????????"""
            al = xlwt.Alignment()
            al.horz = 0x02  # ????????????
            al.vert = 0x01  # ????????????
            style.alignment = al
            # ?????? ???0?????????0??? ??? ???0?????????13???
            '''????????????13'''
            # worksheet1.write_merge(0, 0, 0, 13, '????????????', style)
            excel_data_1 = ('????????????', '????????????', '??????', '??????', '??????', '??????', '????????????')
            for i in range(0, len(excel_data_1)):
                worksheet1.col(i).width = 2560 * 3
                #               ????????????  ?????????            ??????
                worksheet1.write(0, i, excel_data_1[i], style)
            workbook.save(os_path)
        # ???????????????????????????
        if os.path.exists(os_path):
            # ???????????????
            workbook = xlrd.open_workbook(os_path)
            # ????????????????????????????????????
            sheets = workbook.sheet_names()
            for i in range(len(sheets)):
                for name in data.keys():
                    worksheet = workbook.sheet_by_name(sheets[i])
                    # ?????????????????????????????????????????????????????????
                    if worksheet.name == name:
                        # ??????????????????????????????
                        rows_old = worksheet.nrows
                        # ???xlrd?????????????????????xlwt??????
                        new_workbook = copy(workbook)
                        # ????????????????????????????????????i??????
                        new_worksheet = new_workbook.get_sheet(i)
                        for num in range(0, len(data[name])):
                            new_worksheet.write(rows_old, num, data[name][num])
                        new_workbook.save(os_path)
                        print(f'{f}===={title}========????????????')
                        self.text1.insert("insert", f'{f}===={title}========????????????')
                        self.text1.insert("insert", '\n ')
                        self.text1.insert("insert", '\n ')

    def parse_hit_click_2(self):
        """??????????????????2???????????????????????????"""
        self.entry_user.delete(0, "end")
        self.entry_passwd.delete(0, "end")
        self.text1.delete("1.0", "end")

    def center(self):
        """??????????????????????????????"""
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = int((ws / 2) - (800 / 2))
        y = int((hs / 2) - (600 / 2))
        self.window.geometry('{}x{}+{}+{}'.format(800, 600, x, y))

    def run_loop(self):
        """??????????????????????????????"""
        self.window.resizable(False, False)
        """????????????"""
        self.center()
        """????????????--?????????"""
        self.window.mainloop()


if __name__ == '__main__':
    d = DBSpider()
    d.run_loop()
