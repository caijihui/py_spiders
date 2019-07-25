# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PySpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    
class DouBan250Item(scrapy.Item):
    numbers = scrapy.Field()
    movie_name = scrapy.Field()
    rating_num = scrapy.Field()
    director = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    star = scrapy.Field()
    evaluate = scrapy.Field()
    pass