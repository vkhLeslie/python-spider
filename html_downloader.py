# coding:utf-8
# urllib和urllib2包集合成在一个包了
import urllib.request


class HtmlDownloader (object):

    def download(self, url):
        if url is None:
            return None
        response = urllib.request.urlopen(url)
        if response.getCode() != 200:
            return None
        return response.read()
