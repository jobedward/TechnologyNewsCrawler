# -*- coding: utf-8 -*-

import scrapy
import time
import re
from Technology_News.items import TechnologyNewsItem

class InfoqBigDataNewsSpider(scrapy.Spider):
    name = "InfoqBigDataNews"

    start_urls = [
        'http://www.infoq.com/cn/bigdata/news/',
        'http://www.infoq.com/cn/bigdata/articles/',
        'http://www.infoq.com/cn/cloud-computing/articles/',
        'http://www.infoq.com/cn/cloud-computing/news/',
    ]

    def parse(self, response):
        relative_urls = response.xpath('''//div[@class='tag_page_content sponsored_label']
            //div[@class='tab_content']//div/h2/a/@href''').extract()
        for url in relative_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_news)

        next_page = response.xpath('''//div[@class='load_more_articles']/a/@href''').extract()
        if next_page and (len(next_page) > 1):
            next_page = response.urljoin(next_page[1])
            print("Next page is %s\n" % next_page)
            #yield scrapy.Request(next_page, callback=self.parse)

    def transform_date(self, milliseconds):
        #date_format = '%Y-%m-%d %H:%M:%S'
        date_format = "%Y-%m-%d"
        seconds = milliseconds // 1000
        localtime = time.localtime(seconds)
        dt = time.strftime(date_format, localtime)
        return dt

    def parse_news(self, response):
        item = TechnologyNewsItem()

        news_title = response.xpath('''//div[@id='contentRatingWidget']
            //input[@id='cr_item_title']/@value''').extract()
        if news_title and (len(news_title) > 0):
            item['title'] = news_title[0]
        else:
            item['title'] = ""

        news_author = response.xpath('''//div[@id='contentRatingWidget']
            //input[@id='cr_item_author']/@value''').extract()
        if news_author and (len(news_author) > 0):
            item['author'] = news_author[0]
        else:
            item['author'] = ""

        item['source_url'] = response.url


        publish_msec = response.xpath('''//div[@id='contentRatingWidget']
            //input[@id='cr_item_published_time']/@value''').extract()
        if publish_msec and (len(publish_msec) > 0):
            item['publish_date'] = self.transform_date(int(publish_msec[0]))
        else:
            item['publish_date'] = time.strftime("%Y-%m-%d")
        
        content_list = response.xpath('''//div[@class='text_info']/
            div[@class='clear'][1]/preceding-sibling::*''').extract()
        if content_list:
            item['content'] = "".join(content_list)
        else:
            item['content'] = ""

        #print (dict(item))
        yield item
