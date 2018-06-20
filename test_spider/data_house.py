#!/usr/bin/env python
# encoding=utf-8
import requests
import re
from bs4 import BeautifulSoup
from openpyxl import Workbook
import pymysql
import time  # 引入time模块
from urllib.parse import urlparse


# 操作excel
wbExcel = Workbook()
dest_filename = 'house.xlsx'
ws1Active = wbExcel.active
ws1Active.title = "house"

update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 爬取数据目标路径
# DOWNLOAD_URL = 'https://fs.fang.lianjia.com/loupan/pg8'

# 数据库操作
db = pymysql.connect("localhost", "root", "123456", "testjhipster", charset='utf8')
print('连接上了数据库!')
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS `house`")
# 创建表
sql = """
        CREATE TABLE `house` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `house_name` varchar(100) NOT NULL,
          `house_type` varchar(50) NOT NULL,
          `house_selling` varchar(50) NOT NULL,
          `house_address` varchar(100) NOT NULL,
          `house_area` varchar(50) NOT NULL,
          `house_price` varchar(30) NOT NULL,
          `house_total_price` varchar(30) NOT NULL,
          `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
cursor.execute(sql)


# 爬取更多的网页需要循环更新requests 的页面URL
def download_page(urls):
    """获取url地址页面内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(urls, headers=headers).content
    # 循环抓取列表页信息
    # for url in urls:
    #     data_html = requests.get(url=url, headers=headers)
    #     html = data_html.content
    #     # 每次间隔1秒
    #     time.sleep(1)
    return data


def get_new_urls(user_in_num, user_in_city):
    # 爬取数据目标路径
    URL_COMMONT = 'https://' + user_in_city + '.fang.lianjia.com/loupan/pg'
    # DOWNLOAD_URL = 'https://fs.fang.lianjia.com/loupan/pg8'
    DOWNLOAD_URL = []
    for url_next in range(1, int(user_in_num)):
        DOWNLOAD_URL.append(URL_COMMONT+str(url_next))
    return DOWNLOAD_URL


def get_html(doc):

    soup = BeautifulSoup(doc, 'html.parser')
    # 目标数据的html
    ul = soup.find('ul', class_='resblock-list-wrapper')
    house_name = []  # 小区名字
    house_type = []  # 小区类型 商业或住宅
    house_selling = []  # 是否在售
    house_address = []  # 小区地址
    house_area = []  # 住房面积
    house_price = []  # 价格
    house_total_price = []  # 总价格
    for i in ul.find_all('li', class_='resblock-list'):
        detail_content = i.find('div', attrs={'class': 'resblock-desc-wrapper'})

        house_title = detail_content.find('div', attrs={'class': 'resblock-name'})
        house_location = detail_content.find('div', attrs={'class': 'resblock-location'})
        detail_area = detail_content.find('div', attrs={'class': 'resblock-area'})
        detail_price = detail_content.find('div', attrs={'class': 'resblock-price'})

        name = house_title.find('a', attrs={'class': 'name'}).get_text()
        type = house_title.find('span', attrs={'class': 'resblock-type'}).get_text()
        status = house_title.find('span', attrs={'class': 'sale-status'}).get_text()

        location = house_location.find('a').get_text()
        area = detail_area.find('span').get_text()

        total_price = detail_price.find('div', attrs={'class': 'second'})

        price = detail_price.find('div', attrs={'class': 'main-price'}).find('span',
                                                                             attrs={'class': 'number'}).get_text()

        if total_price:  # 判断是否有总价
            house_total_price.append(total_price.get_text())
        else:
            house_total_price.append('无')

        house_name.append(name)
        house_type.append(type)
        house_selling.append(status)
        house_address.append(location)
        house_area.append(area)
        house_price.append(price)
        # print(house_name)
        # print(house_type)
        # print(house_selling)
        # print(house_address)
        # print(house_area)
        # print(house_price)
        # print(house_total_price)
    # page = soup.find('a', attrs={'class': 'next'})  # 获取下一页
    # if page:
    #     # page_number = soup.find('div', attrs={'class': 'page-box'}).find('span', attrs={'class': 'page-box').
    #     # page_number = 2
    #     return house_name, house_type, house_selling, house_address, house_area, house_price, house_total_price, DOWNLOAD_URL + 43
    return house_name, house_type, house_selling, house_address, house_area, house_price, house_total_price, None


def main():
    user_in_num = input('输入生成页数：')
    user_in_city = input('输入爬取城市：')
    # for i in new_urls(user_in_num):
    #     print(i)
    # soup = BeautifulSoup(html_cont, 'html_parser', from_encoding='utf-8')
    # 爬取数据目标路径
    # url = DOWNLOAD_URL
    urls = get_new_urls(user_in_num, user_in_city)
    house_name = []  # 小区名字
    house_type = []  # 小区类型 商业或住宅
    house_selling = []  # 是否在售
    house_address = []  # 小区地址
    house_area = []  # 住房面积
    house_price = []  # 价格
    house_total_price = []  # 总价格
    # 下载每个html     while urls:
    for url in urls:
        print(url)
        doc = download_page(url)
        # 获取所有li
        name, type, selling, address, area, price, total_price, url = get_html(doc)
        house_name = house_name + name
        house_type = house_type + type
        house_selling = house_selling + selling
        house_address = house_address + address
        house_area = house_area + area
        house_price = house_price + price
        house_total_price = house_total_price + total_price
        # print(house_name, house_type, house_selling, house_address, house_area, house_price, house_total_price)

    # zip()函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
    for (i, m, o, p, q, w, x) in zip(house_name, house_type, house_selling, house_address, house_area, house_price, house_total_price):
        print(i)
        print(m)
        print(o)
        print(p)
        print(q)
        print(w)
        print(x)

        col_A = 'A%s' % (house_name.index(i) + 1)
        col_B = 'B%s' % (house_name.index(i) + 1)
        col_C = 'C%s' % (house_name.index(i) + 1)
        col_D = 'D%s' % (house_name.index(i) + 1)
        col_E = 'E%s' % (house_name.index(i) + 1)
        col_F = 'F%s' % (house_name.index(i) + 1)
        col_G = 'G%s' % (house_name.index(i) + 1)

        ws1Active[col_A] = i
        ws1Active[col_B] = m
        ws1Active[col_C] = o
        ws1Active[col_D] = p
        ws1Active[col_E] = q
        ws1Active[col_F] = w
        ws1Active[col_G] = x

        try:
            insert_house = ("INSERT INTO house(house_name, house_type, house_selling, house_address, house_area, house_price, house_total_price)" "VALUES(%s, %s, %s, %s,%s, %s, %s)")
            data_house = (i, m, o, p, q, w, x)
            cursor.execute(insert_house, data_house)
        except Exception as e:
            db.rollback()  # 事务回滚
            print('事务处理失败', e)
        else:
            db.commit()  # 事务提交
            print('事务处理成功', cursor.rowcount)
    # 关闭连接
    cursor.close()
    db.close()
    wbExcel.save(filename=dest_filename)


if __name__ == '__main__':
    main()
