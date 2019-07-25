# -*- coding: utf-8 -*-
import scrapy
import json
from py_spiders.items import DouBan250Item
from scrapy.selector import Selector

class Douban250Spider(scrapy.Spider):
    name = 'douban250'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def start_requests(self):
        for i in range(0,10):
            # https://movie.douban.com/top250?start=25&filter=
            url = "https://movie.douban.com/top250?start="+ str(25*i) +"&filter=";
            yield scrapy.Request(url,callback=self.parse_css)

    ## xpath 实现
    def parse(self, response):
        selector = Selector(response)
        for sel in selector.xpath('//div[@class="item"]'):
            item = {}
            item["numbers"]=sel.xpath('div[@class="pic"]/em/text()').extract()[0]
            title = sel.xpath('div[@class="info"]/div[@class="hd"]/a/span/text()').extract() # 多个span标签
            item["movie_name"] = "".join(title).strip() # 将多个字符串无缝连接起来
            movieInfo = sel.xpath('div[@class="info"]/div[@class="bd"]/p/text()').extract()
            item["movieInfo"] = "".join(movieInfo).strip()
            item["rating_num"] = sel.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span/text()').extract()[1]
            item["link"]=sel.xpath('div[@class="info"]/div[@class="hd"]/a/@href').extract()[0]
            yield item
        pass

    def parse_css(self,response):
        for sel in response.css('.grid_view li'):
            item = {}
            item["numbers"]=sel.css('.item .pic em::text').get()
            title = sel.css('.item .info .hd .title::text').getall()
            item["movie_name"] = "".join(title).strip() # 将多个字符串无缝连接起来
            item["rating_num"] = sel.css('.item .info .bd .star .rating_num::text').get()
            item["movieInfo"] = sel.css('.item .info .bd p::text').get().strip()
            item["star"] = sel.css('.item .info .bd .star span::text').get()
            item["link"]=sel.css('.item .info .hd a::attr(href)').get()
            yield item
        pass