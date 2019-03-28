# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IpPoolItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    is_high_anonymous = scrapy.Field()
    ip_type = scrapy.Field()  # http or https
    ip_server = scrapy.Field()  # ip的运营商
    ip_location = scrapy.Field()