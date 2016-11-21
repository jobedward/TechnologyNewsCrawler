# -*- coding: utf-8 -*-

import scrapy
from Technology_News.items import TechnologyNewsItem

class ThirtySixBigDataSpider(scrapy.Spider):
    name = "36dsj"

    def start_requests(self):
        with open('36urls.txt') as f: 
            urls = f.readlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_news)

    def parse(self, response):
        relative_urls = response.xpath('''//div[@class='content-wrap']/div[@class='content']
            /article[@class='excerpt']/h2/a/@href''').extract()
        for url in relative_urls:
            print (response.urljoin(url))
            #yield {
            #    'url': response.urljoin(url)
            #}
            yield scrapy.Request(response.urljoin(url), callback=self.parse_news)

    def parse_news(self,response):
        item = TechnologyNewsItem()
        news_title = response.xpath('''//div[@class='content-wrap']/div[@class='content']
            //h1[@class='article-title']/a/text()''').extract()
        if news_title and (len(news_title) > 0):
            item['title'] = news_title[0]
        else:
            item['title'] = ""

        article_meta = response.xpath('''//div[@class='content-wrap']/div[@class='content']
            //ul[@class='article-meta']/li/text()''').extract()
        if article_meta and (len(article_meta) > 1):
            item['author'] = article_meta[0].strip()
            tmp_date = article_meta[1].strip().split(" ")
            if tmp_date and (len(tmp_date) > 0):
                item['publish_date'] = tmp_date[0]
            else:
                item['publish_date'] = ""
        else:
            item['author'] = ""
            item['publish_date'] = ""

        item['source_url'] = response.url

        content_list = response.xpath('''//div[@class='content-wrap']/div[@class='content']
            /article[@class='article-content']/div[@class='wumii-hook']/preceding-sibling::*''').extract()
        if content_list:
            item['content'] = "".join(content_list)
        else:
            item['content'] = ""

        yield item
