#author:chenxw
#createDate:2018/06/01
#description；
'''
从settings里面取出我们的USER_AGENT列表，
而后就是随机从列表中选择一个，添加到headers里面，
最后默认返回了None
'''
import scrapy
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random


class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent

        '''
        DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None, 
        'myproject.middlewares.MyUserAgentMiddleware': 400,
        }
        '''