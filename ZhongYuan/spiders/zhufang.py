# -*- coding: utf-8 -*-
import scrapy
from ..items import ZFItem
from pyquery import PyQuery
from scrapy.http import Request
from scrapy_redis.spiders import Spider

class ZhufangSpider(Spider):
    name = 'zhufang'
    allowed_domains = ['gz.centanet.com']
    start_urls = ['http://gz.centanet.com/zufang/g1/']

    def parse(self, response):
        pq = PyQuery(response.text)
        zf_item = ZFItem()
        zf_lists = pq("div.house-item").items()
        for zf_list in zf_lists:
            zf_item['title'] = zf_list("h4.house-title").text()
            zf_item['price'] = zf_list("p.price-nub").text()
            zf_item['house_msg'] = zf_list("p.house-name").text()
            zf_item['decorated_msg'] = zf_list('p.house-name').next().text()
            zf_item['address'] = zf_list('p.house-name').next().next().text()
            zf_item['tag' ] = zf_list('p.labeltag').text()
            print(zf_item)
            yield zf_item

        for i in range(2, 4):
            url = "http://gz.centanet.com/zufang/g" + str(i) + "/"
            yield Request(url, callback=self.parse)


