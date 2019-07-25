# -*- coding: utf-8 -*-
import scrapy


class V2exSpider(scrapy.Spider):
    name = 'v2ex'
    headers = {
        'Referer': 'https://www.v2ex.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36'
    }
    allowed_domains = ['v2ex.com']
    start_urls = ['https://www.v2ex.com/?tab=apple']

    def start_requests(self):
        url = 'https://www.v2ex.com/?tab=apple'
        yield scrapy.Request(url=url,callback=self.parse,method="GET",headers=self.headers)

    def parse(self, response):
        for sel in response.xpath('div[@class="item"]'):
            item = {}
            item["title"]=sel.xpath('span[@class="item_title"]/a/text()').extract()
            item["link"]= sel.xpath('span[@class="item_title"]/a/@href').extract()
            item["tag"]=sel.xpath('div[@class="votes"]/a/text()').extract()
            item["author"] = sel.xpath('span[@class="topic_info"]/strong/a/text()').extract()
            print(item)
            # yield item
        pass
