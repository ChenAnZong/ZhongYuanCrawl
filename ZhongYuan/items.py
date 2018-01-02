# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZFItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    house_msg = scrapy.Field()
    decorated_msg = scrapy.Field()
    address = scrapy.Field()
    tag = scrapy.Field()
    pass
