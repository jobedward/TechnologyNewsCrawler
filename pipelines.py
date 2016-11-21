# -*- coding: utf-8 -*-

import pymongo

class MongoPipeline(object):

    collection_name = 'test_infoq_bigdata'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        contents = dict(item)
        if (contents["source_url"]):
        	try:
        		contents["title"] = contents["title"].encode("utf-8")
        		contents["author"] = contents["author"].encode("utf-8")
        		contents["content"] = contents["content"].encode("utf-8")
        		self.db[self.collection_name].insert(contents)
        	except:
        		pass
        return item

class TxtWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.txt', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        contents = dict(item)
        line = "Title: " + contents["title"]
        line = line + "Author: " + contents["author"]
        line = line + "Publish Date: " + contents["publish_date"]
        line = line + "URL: " + contents["source_url"]
        line = line + "Content: " + contents["content"]
        self.file.write(line.encode("utf-8"))
        return item

class URLWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('urls.txt', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        contents = dict(item)
        line = contents["url"] + "\n"
        self.file.write(line.encode("utf-8"))
        return item
