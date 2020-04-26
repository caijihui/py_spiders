# -*- coding: utf-8 -*-
import scrapy


class A79taoSpider(scrapy.Spider):
    name = '79tao'
    allowed_domains = ['79tao.com','xianbaowu.cn']
    start_urls = ['http://www.xianbaowu.cn/forum.php?mod=guide&view=newthread']

    custom_settings = {
        'ITEM_PIPELINES': {
            'py_spiders.pipelines.A79taoSqlPipeline':50,
            # 'py_spiders.pipelines.A79taoJsonPipeline': 50,
        }
    }
    def start_requests(self):
        url = "http://www.79tao.com/forum.php?mod=guide&view=newthread";
        yield scrapy.Request(url=url,callback=self.parse)
        # for i in range(1,2):
        #     url = 'http://www.79tao.com/forum.php?mod=guide&view=newthread&'+"page="+str(i)
        #     yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//*[@id="threadlist"]/div[2]/table/tbody'):
            item = {}
            item['title'] = sel.xpath('tr/th/a/text()').extract()[0]
            item['href'] = sel.xpath('tr/th/a/@href').extract()[0]
            item['from'] = sel.xpath('tr/td[2]/a/text()').extract()[0]
            item['created_at'] = sel.xpath('tr/td[3]/em/span/text()').extract()[0]
            if(type(item['href']) == str):
                str1 = item['href'].split("-")
                item['id'] = int(str1[1])
                url = item['href']
                print(url)
                yield scrapy.Request(url=url,callback=self.parse_details,meta={"item": item})
        pass

    def parse_details(self, response):
        item = response.meta["item"]
        description = response.xpath('//*[@class="t_f"]/text()').extract()
        item["description"] = "".join(description).strip()
        yield item
        pass