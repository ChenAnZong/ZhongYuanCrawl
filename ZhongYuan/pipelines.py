# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from pymongo import MongoClient
from scrapy.conf import settings
from traceback import format_exc

class ZFJSONPipeline(object):
    """
    管道1：把数据写到文件中
    """
    def __init__(self):
        self.file = codecs.open('ZhongYuanZufang.json','a+',encoding='utf-8')

    def process_item(self, item, spider):
        house_dict = {"城市":item["city"], "标题": item['title'], "价格": item['price'],"基本情况": item['house_msg'],
                 "装修情况": item['decorated_msg'], "地址": item['address'], "其它": item['tag']}

        line = "\n"
        house_json = json.dumps(house_dict, ensure_ascii=False)
        self.file.write(house_json)
        self.file.write(line)
        return item

    def close_spider(self,spider):
        self.file.close()


class MongoPipeline(object):
    """
    管道2：把数据存储到MongoDB中
    """
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGODB_URI'),
            mongo_db = settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self,spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            house_dict = {"城市": item["city"], "标题": item['title'], "价格": item['price'], "基本情况": item['house_msg'],
                          "装修情况": item['decorated_msg'], "地址": item['address'], "其它": item['tag']}
            print("xxxxxxxxxxrurururururururururxxxxxxxxxxxxx")
            self.db['ZhongYuan'].save(house_dict)
        except Exception as e:
            print(e.__traceback__)
            spider.logger.error(format_exc())
        return item
