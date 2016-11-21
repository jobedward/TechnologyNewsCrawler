# -*- coding: utf-8 -*-

import scrapy


class TechnologyNewsItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publish_date = scrapy.Field()
    source_url = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()
    
