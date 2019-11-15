# -*- coding: utf-8 -*-
import scrapy

## 废弃---暂无使用计划
class JiankeSpider(scrapy.Spider):
    name = 'jianke'
    allowed_domains = ['www.jianke.com']
    start_urls = ['http://www.jianke.com/']

    
    custom_settings = {
        'ITEM_PIPELINES': {
            'py_spiders.pipelines.JianKeSqlPipeline':50,
        }
    }
    def start_requests(self):
      
        needNode = {1:'0107',2:'0110'};
        
        for i in range(1,2):
            r = needNode[i]
            url = "https://www.jianke.com/list-"+ r +"-0-1-0-1-0-0-0-0-0.html";
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/ul/li'):
            item = {}
            item['href'] = sel.xpath('div/div[2]/p/a/@href').extract()[0]
            item['total'] = sel.xpath('//*[@id="goto_page_total_pages"]/strong/text()').extract()[0]    
            if(type(item['href']) == str):
                url = "https:"+item['href']
                yield scrapy.Request(url=url,callback=self.parse_detail,meta={"item": item})
        pass

    def parse_detail(self, response):
            item = response.meta["item"]
            item["title"] = response.xpath('//*[@id="presc"]/div[3]/div[3]/div[2]/div[1]/div[2]/h1/text()').extract()[0];
            print(item["title"])
            item["cn_name"] = response.xpath('//*[@id="presc"]/div[3]/div[3]/div[2]/dl[1]/dd/a/text()').extract()[0];
            pihao = response.xpath('//*[@id="presc"]/div[3]/div[3]/div[2]/dl[3]/dd/span/text()').extract()[0];
            item["pihao"] = "".join(pihao).strip()
            item["price"] = response.xpath('//*[@id="price_big"]/dd/em/text()').extract()[0];
            item["other_id"] = response.xpath('//*[@id="prodCode"]/text()').extract()[0];
            item["url"] = "https:"+item["href"];
            yield item
            pass