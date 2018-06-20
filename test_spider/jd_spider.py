#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Created on 2014-12-27 21:33:36

from pyspider.libs.base_handler import *
#导入必要的库
from urlparse import urljoin


class Handler(BaseHandler):
    #入口方法，当点run按钮时执行此方法
    def on_start(self):
        self.crawl('http://wap.jd.com/category/all.html', callback=self.all_page)
        #以上语句的意思是爬取这个url的内容后用self.all_page函数来处理网页内容

    def all_page(self, response):
        #循环所有以http://wap.jd.com/category/的链接，并生成新任务，指定新任务返回的内容由self.category_page方法来处理。以下两个方法类似
        for each in response.doc('a[href^="http://wap.jd.com/category/"]').items():
            self.crawl(urljoin(each.attr.href,'?=').replace('?=',''), callback=self.category_page)

    def category_page(self, response):
        for each in response.doc('a[href^="http://wap.jd.com/products/"]').items():
            self.crawl(urljoin(each.attr.href,'?=').replace('?=',''), callback=self.in_page)

    def in_page(self, response):
        for each in response.doc('a[href^="http://wap.jd.com/product/"]').items():
            self.crawl(urljoin(each.attr.href,'?=').replace('?=',''), callback=self.detail_page)
        for each in response.doc('HTML>BODY>DIV.page>A[href]').items():
            self.crawl(urljoin(each.attr.href,'?=').replace('?=',''), callback=self.in_page)

    def detail_page(self, response):
        #获取最终页面上的内容并过滤掉无用的字，返回爬取的内容并保存至默认结果库
        return {
            "url": response.url,
            "category": response.doc('HTML>BODY>DIV.pro>A').text().replace(u'\u9996\u9875\u0020',''),
            "name": response.doc('title').text().replace(u'\u0020\u002d\u0020\u4EAC\u4E1C\u624B\u673A\u7248',''),
            "price": response.doc('HTML>BODY>DIV.content.content2>DIV.p-price>FONT').text().replace(u'\u00A5',''),
        }
