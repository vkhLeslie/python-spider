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
wb = Workbook()
dest_filename = 'house.xlsx'
ws1 = wb.active
ws1.title = "house"

update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 爬取数据目标路径
URL_COMMONT = 'https://fs.fang.lianjia.com/loupan/pg'
DOWNLOAD_URL = []
for i in range(43):
    DOWNLOAD_URL.append(URL_COMMONT+str(i+1))


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


def download_page(url):
    """获取url地址页面内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data


def get_new_urls(page_url, soup):
        new_urls = set()
        # 获取所有标签
        links = soup.find_all('a', href=re.compile(r'/pg/\d+'))
        for link in links:
            new_url = link['link']
            # 全路径
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
            return new_urls


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

        price=detail_price.find('div', attrs={'class': 'main-price'}).find('span', attrs={'class': 'number'}).get_text()

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
        # house_total_price.append(total_price)

    page = soup.find('a', attrs={'class': 'next'})  # 获取下一页
    print(page)
    if page:
        # page_number = soup.find('div', attrs={'class': 'page-box'}).find('span', attrs={'class': 'page-box').
        # page_number = 2
        return house_name, house_type, house_selling, house_address, house_area, house_price, house_total_price, DOWNLOAD_URL + 43
    return house_name, house_type, house_selling, house_address, house_area, house_price, house_total_price, None


def main():
    # soup = BeautifulSoup(html_cont, 'html_parser', from_encoding='utf-8')
    # 爬取数据目标路径
    url = DOWNLOAD_URL
    # url = get_new_urls(DOWNLOAD_URL, soup)
    house_name = []  # 小区名字
    house_type = []  # 小区类型 商业或住宅
    house_selling = []  # 是否在售
    house_address = []  # 小区地址
    house_area = []  # 住房面积
    house_price = []  # 价格
    house_total_price = []  # 总价格

    while url:
        print(url)
        # 下载html
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

    # zip()函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
    for (i, m, o, p, q, w, x) in zip(house_name, house_type, house_selling, house_address, house_area, house_price, house_total_price):
        col_A = 'A%s' % (name.index(i) + 1)
        col_B = 'B%s' % (name.index(i) + 1)
        col_C = 'C%s' % (name.index(i) + 1)
        col_D = 'D%s' % (name.index(i) + 1)
        col_E = 'E%s' % (name.index(i) + 1)
        col_F = 'F%s' % (name.index(i) + 1)
        col_G = 'G%s' % (name.index(i) + 1)
        print(i)
        print(m)
        print(o)
        print(p)
        print(q)
        print(w)
        print(x)
        ws1[col_A] = i
        ws1[col_B] = m
        ws1[col_C] = o
        ws1[col_D] = p
        ws1[col_E] = q
        ws1[col_F] = w
        ws1[col_G] = x

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
    wb.save(filename=dest_filename)


if __name__ == '__main__':
    main()
