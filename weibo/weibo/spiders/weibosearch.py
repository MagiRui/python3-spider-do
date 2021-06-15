# -*- coding: utf-8 -*-
import re

import scrapy

from weibo.items import WeiboItem


class WeibosearchSpider(scrapy.Spider):
    name = 'weibosearch'
    allowed_domains = ['weibo.cn']
    start_urls = ['https://weibo.cn/search/?keyword=601318&smblog=%E6%90%9C%E5%BE%AE%E5%8D%9A']

    def parse(self, response):

        weibos = response.xpath("//div[@class='c' and contains(@id, 'M_')]")
        for weibo in weibos:

            #每个微博下面对应的div个数
            #divCount = int(float(weibo.xpath("count(.//div)").extract()[0]))

            #
            weiboDivs = weibo.xpath(".//div")
            weiboUserName = None
            weiboContent = None
            praiseCnt = 0
            commentCnt = 0
            transmitCnt = 0
            for weiboDiv in weiboDivs:

               weiboNameTemp = weiboDiv.xpath(".//a[@class='nk']/text()").extract_first()
               weiboContentTempList = weiboDiv.xpath(".//span[@class='ctt']/text()").extract()
               if weiboNameTemp:
                   weiboUserName = weiboNameTemp

               if weiboContentTempList:

                   weiboAllContent = ""
                   for weiboContentTemp in weiboContentTempList:
                       weiboAllContent += weiboContentTemp.strip()

                   weiboContent = weiboAllContent

               #获取点赞数
               praise  = weiboDiv.xpath(".//a[contains(., '赞[')]/text()").extract_first()
               if praise:
                   praiseCnt = re.search("赞\[(\d.*?)\]", praise).group(1)


               #获取评论数
               comment = weiboDiv.xpath(".//a[contains(., '评论[')]/text()").extract_first()
               if comment:
                   commentCnt = re.search("评论\[(\d.*?)\]", comment).group(1)

               #转发数
               transmit = weiboDiv.xpath(".//a[contains(., '转发[')]/text()").extract_first()
               if transmit:
                   transmitCnt = re.search("转发\[(\d.*?)\]", transmit).group(1)

               weiboTimeText = weiboDiv.xpath(".//span[@class='ct']/text()").extract_first()
               weiboTime = None
               weiboSource = None
               if weiboTimeText:

                   weiboTimeText = weiboTimeText.strip()
                   timeAndSource = re.search("(.*?)来自(.*)", weiboTimeText)
                   weiboTime = timeAndSource.group(1).strip()
                   weiboSource = timeAndSource.group(2).strip()
            item = WeiboItem()
            item["weiboUserName"] = weiboUserName
            item["weiboContent"] = weiboContent
            item["praiseCnt"] = praiseCnt
            item["commentCnt"] = commentCnt
            item["transmitCnt"] = transmitCnt
            item["weiboTime"] = weiboTime
            item["weiboSource"] = weiboSource
            yield item










