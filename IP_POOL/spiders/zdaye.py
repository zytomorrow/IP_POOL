# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from IP_POOL.items import IpPoolItem


START_URL = 'http://ip.zdaye.com/dayProxy.html'
BASIC_URL = 'http://ip.zdaye.com'


class ZdayeSpider(scrapy.Spider):
    name = 'zdaye'
    allowed_domains = ['ip.zdaye.com']
    start_urls = ['http://ip.zdaye.com/dayProxy.html']

    def parse(self, response):
        # 获取目前已有的最大页
        max_page = int(BeautifulSoup(response.body).find_all('a', title='最后页')[0].contents[0])
        # for page in range(1, max_page+1):
        for page in range(1, 2):
            yield Request(url=f'{START_URL[:-5]}/{page}.html', callback=self.titleList)

    def titleList(self, response):
        """
        进入当前页的所有发布的ip主题
        :param response:
        :return:
        """
        all_title = BeautifulSoup(response.body).find_all('div', class_='title')
        for title in all_title:
            url = BASIC_URL + title.a['href']  # 网页内全是uri的链接
            yield Request(url=url, callback=self.contentSplit)

    def contentSplit(self, response):
        """

        :param response:
        :return:
        """
        # 实例化一个item作为容器
        item = IpPoolItem()

        '''
        全是字符串处理！！！WTF！！！
        站长还采取了不同的文本方式！！！！！！
        目前有两种
            1. xxx.xxx.xxx.xxx:port@HTTP#[未知]广东省佛山市 移动
            2. 183.234.9.187:8080#广东省 移动
        '''
        # ip列表
        ip_list = str(BeautifulSoup(response.body).find_all('div', class_='cont')[0]).split("<br/>")[1:-1]  # 数据是<br/>换行分隔的
        for ipinf in ip_list:
            if "@" in ip_list:  # 针对方式一的spilt
                item['ip'], item['port'] = ipinf.split("@")[0].split(':')
                item['ip_type'] = ipinf.split("@")[-1].split("#")[0]
                item['ip_server'] = ""  # ip服务商不一定存在，给个默认空值
                if len(ipinf.split("]")[-1].split(" ")) == 2:
                    item['ip_location'], item['ip_server'] = ipinf.split("]")[-1].split(" ")
                else:
                    item['ip_location'] = ipinf.split("]")[-1].split(" ")[0]
                item['is_high_anonymous'] = ipinf.split('[')[-1].split(']')[0]
            else:  # 针对方式二的spilt
                item['ip'], item['port'] = ipinf.split("#")[0].split(':')
                item['ip_type'] = "HTTP"
                item['ip_server'] = ""  # ip服务商不一定存在，给个默认空值
                if len(ipinf.split("]")[-1].split(" ")) == 2:
                    item['ip_location'], item['ip_server'] = ipinf.split("#")[-1].split(" ")
                else:
                    item['ip_location'] = ipinf.split("#")[-1].split(" ")[0]
                item['is_high_anonymous'] = "未知"

            yield item

