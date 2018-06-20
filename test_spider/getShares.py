#!/usr/bin/env python
# encoding=utf-8
import requests
import re
from bs4 import BeautifulSoup
from openpyxl import Workbook
import pymysql
import time  # 引入time模块

# 操作excel
wb = Workbook()
dest_filename = '电影.xlsx'
ws1 = wb.active
ws1.title = "电影top250"

DOWNLOAD_URL = 'http://movie.douban.com/top250/'

db = pymysql.connect("localhost", "root", "123456", "testjhipster", charset='utf8')
print('连接上了数据库!')
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS `movie`")
# 创建表
sql = """
        CREATE TABLE `movie` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `name` varchar(50) NOT NULL,
          `star_con` varchar(50) NOT NULL,
          `score` varchar(10) NOT NULL,
          `info_list` varchar(100) NOT NULL,
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


def get_li(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    ol = soup.find('ol', class_='grid_view')
    name = []  # 名字
    star_con = []  # 评价人数
    score = []  # 评分
    info_list = []  # 短评
    for i in ol.find_all('li'):
        detail = i.find('div', attrs={'class': 'hd'})
        movie_name = detail.find(
            'span', attrs={'class': 'title'}).get_text()  # 电影名字
        level_star = i.find(
            'span', attrs={'class': 'rating_num'}).get_text()  # 评分
        star = i.find('div', attrs={'class': 'star'})
        star_num = star.find(text=re.compile('评价'))  # 评价

        info = i.find('span', attrs={'class': 'inq'})  # 短评
        if info:  # 判断是否有短评
            info_list.append(info.get_text())
        else:
            info_list.append('无')
        score.append(level_star)

        name.append(movie_name)
        star_con.append(star_num)
    page = soup.find('span', attrs={'class': 'next'}).find('a')  # 获取下一页
    if page:
        return name, star_con, score, info_list, DOWNLOAD_URL + page['href']
    return name, star_con, score, info_list, None


def main():
    url = DOWNLOAD_URL
    name = []
    star_con = []
    score = []
    info = []
    update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    while url:
        doc = download_page(url)
        movie, star, level_num, info_list, url = get_li(doc)
        name = name + movie
        star_con = star_con + star
        score = score + level_num
        info = info + info_list

    for (i, m, o, p) in zip(name, star_con, score, info):
        col_A = 'A%s' % (name.index(i) + 1)
        col_B = 'B%s' % (name.index(i) + 1)
        col_C = 'C%s' % (name.index(i) + 1)
        col_D = 'D%s' % (name.index(i) + 1)
        ws1[col_A] = i
        ws1[col_B] = m
        ws1[col_C] = o
        ws1[col_D] = p
        try:
            insert_movie = ("INSERT INTO movie(name, star_con, score, info_list)" "VALUES(%s, %s, %s, %s)")
            data_movie = (i, m, o, p)
            cursor.execute(insert_movie, data_movie)
        except Exception as e:
            db.rollback()  # 事务回滚
            print('事务处理失败', e)
        else:
            db.commit()  # 事务提交
            print('事务处理成功', cursor.rowcount)
        # insert_movie = ("INSERT INTO MOVIIE(name, star_con, score, info_list)" "VALUES(%s, %s, %s, %s)")
        # data_movie = (i, m, o, p)
        # cursor.execute(insert_movie, data_movie)
        # print '******完成此条插入!'
        # db.commit()
        # 关闭连接
    cursor.close()
    db.close()
    wb.save(filename=dest_filename)


if __name__ == '__main__':
    main()
