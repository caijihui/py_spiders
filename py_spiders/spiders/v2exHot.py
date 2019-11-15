# -*- coding: utf-8 -*-
import scrapy
import json
class V2extopicsSpider(scrapy.Spider):
    name = 'v2exHot'
    allowed_domains = ['v2ex.com']
    start_urls = ['https://www.v2ex.com/api/topics/hot.json']
    headers = {
        'Referer': 'https://www.v2ex.com',
        'Authentication': None,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36'
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'py_spiders.pipelines.V2exJsonPipeline': 300,
            'py_spiders.pipelines.V2exSqlPipeline': 300
        }
    }

    def start_requests(self):
        url = 'https://www.v2ex.com/api/topics/hot.json'
        yield scrapy.Request(url=url,callback=self.parse,method="GET",headers=self.headers)

    def parse(self, response):
        item1 = str(response.body,encoding = "utf-8")
        item2 = json.loads(item1)
        for one in item2:
            item = {}
            item['title'] = one["title"]
            item['url'] = one["url"]
            item['top_created_at'] = one["created"]
            item["id"]=one["id"]
            yield item
        pass
