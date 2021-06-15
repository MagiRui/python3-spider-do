# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):

    weiboUserName = scrapy.Field()
    weiboContent = scrapy.Field()
    praiseCnt = scrapy.Field()
    commentCnt = scrapy.Field()
    transmitCnt = scrapy.Field()
    weiboTime = scrapy.Field()
    weiboSource = scrapy.Field()
