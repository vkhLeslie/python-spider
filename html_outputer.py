#coding:utf-8
# import re
# import urlparse
# from bs4 import BeautifulSoup
from openpyxl import Workbook
wb = Workbook()
dest_filename = 'outputer.xlsx'
ws1 = wb.active
ws1.title = "outputer"


class HtmlOutputer(object):

    def _init_(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    # ascii python默认输出编码 输出excel格式
    def out_html(self, data):
        # fout = open('output.html', 'w') # 写模式
        # fout.write('<html>')
        # for data in self.datas:
        #     data
        # fout.write('</html>')
        # fout.close()
        for (i, m, o, p) in self.datas:
            col_A = 'A%s' % (data.index(i) + 1)
            col_B = 'B%s' % (data.index(i) + 1)
            col_C = 'C%s' % (data.index(i) + 1)
            col_D = 'D%s' % (data.index(i) + 1)
            ws1[col_A] = i
            ws1[col_B] = m
            ws1[col_C] = o
            ws1[col_D] = p
        wb.save(filename=dest_filename)
