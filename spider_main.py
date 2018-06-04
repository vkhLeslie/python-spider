#coding:utf-8
import html_downloader
import html_outputer
import html_parser
import url_manager


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.output = html_outputer.HtmlOutputer()
        self.parser = html_parser.HtmlParser()

    def craw(self, url_root):
        count = 1
        self.urls.add_new_url(url_root)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('craw %d:%s'%(count, new_url))
                html_cont = self.downloader.download(url_root)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.output.collect_data(new_data)
                if count == 1000:
                    break
                count = count + 1
            except:
                print('此路径页面爬取失败')
        self.output.out_html()


if __name__ == '__main__':
    # 入口url
    root_url = 'https://baike.baidu.com/view/21087.htm'
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
