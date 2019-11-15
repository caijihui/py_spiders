# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector


class WeiboHotSpider(scrapy.Spider):
    name = 'weiboHot'
    allowed_domains = ['https://s.weibo.com']
    start_urls = ['https://s.weibo.com/top/summary?cate=realtimehot']

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'py_spiders.pipelines.weiboHotPipeline':50,
            'py_spiders.pipelines.weiboHotSqlPipeline':50,
        }
    }


    def start_requests(self):
        url = 'https://s.weibo.com/top/summary?cate=realtimehot'
        yield scrapy.Request(url=url,callback=self.parse,method="GET")

    def parse(self, response):
        selector = Selector(response)
        base_domain = 'https://s.weibo.com';
        for sel in selector.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr'):
            # print('output' + str(sel))
            item = {}
            ids = sel.xpath('td[1]/text()').extract()
            if len(ids) == 0 :
                continue;
            item["id"] = ids[0];
            item["url"]= base_domain + sel.xpath('td[2]/a/@href').extract()[0]
            item["title"]=sel.xpath('td[2]/a/text()').extract()[0]
            item["click"]=sel.xpath('td[2]/span/text()').extract()[0]
            yield item
        pass
