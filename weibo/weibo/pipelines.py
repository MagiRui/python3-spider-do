# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time

import pymongo

from weibo.items import WeiboItem


class WeiboPipeline(object):

    def parse_time(self, datetime):

        if re.match("\d+月\d+日", datetime):

            datetime = time.strftime('%Y年', time.localtime()) + datetime
        if re.match("\d+分钟前", datetime):

            minute = re.match("(\d+)", datetime).group(1)
            datetime = time.strftime(("%Y年%m月%d日 %H:%M"), time.localtime(time.time() - float(minute) * 60 ))

        if re.match("今天.*", datetime):

            datetime = re.match("今天(.*)", datetime).group(1)
            datetime = time.strftime("%Y年%m月%d日", time.localtime()) + " " + datetime

        return datetime

    def process_item(self, item, spider):

        if isinstance(item, WeiboItem):

           weiboTime = item["weiboTime"]
           if weiboTime:

               item["weiboTime"] = self.parse_time(weiboTime)

        return item


class MongoPipeline(object):

    def __init__(self, mongo_url, mongo_db):

        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):

        return cls(

            mongo_url=crawler.settings.get("MONGO_URL"),
            mongo_db=crawler.settings.get("MONGO_DB")

        )


    def open_spider(self, spider):

        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):

        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item


    def close_spider(self, spider):

        self.client.close()
