# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import pymysql
from py_spiders import settings,env

class PySpidersPipeline(object):
    def process_item(self, item, spider):
        return item

class DouBan250Pipeline(object):
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        filename = base_dir+"/file/douban.text"
        with open(filename,'a',encoding='utf-8') as f:
            f.write("".join(item["numbers"])+" ")#写入序号换行
            f.write("".join(item["link"])+" ") #写入链接换行
            f.write("".join(item["movie_name"])+"\n")#写入电影名字换行
            f.close()
        return item

#保存为json数据
class DouBan250JsonPipeline(object):
    def __init__(self):
        self.file=open("./file/douban.json","wb")

    def process_item(self, item, spider):
        
        line=json.dumps(item,ensure_ascii = False)+",\n"
        self.file.write(line.encode('utf-8'))
        return item

    def spider_closed(self):
        self.file.close()


class DoubanmovieSqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into doubantop250(numbers,movie_name,movieInfo,rating_num)
                  value (%s,%s,%s,%s)""",
                (item['numbers'],
                 item['movie_name'],
                 item['movieInfo'],
                 item['rating_num']))
            self.connect.commit()
        except Exception as err:
            print("重复插入了==>错误信息为：" + str(err))
        return item

#保存为json数据

class V2exJsonPipeline(object):
    def __init__(self):
        self.file=open("./file/v2.json","wb")

    def process_item(self, item, spider):
        
        line=json.dumps(item,ensure_ascii = False)+",\n"
        self.file.write(line.encode('utf-8'))
        return item

    def spider_closed(self):
        self.file.close()

class V2exSqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into top_hot(type,top_id,title,url,top_created_at,created_at)
                  value (%s,%s,%s,%s,%s,%s)""",
                (1,item['id'],
                 item['title'],
                 item['url'],
                 item['top_created_at'],
                 time.strftime('%Y-%m-%d %H:%M:%S')))
            self.connect.commit()
        except Exception as err:
            print("重复插入了==>错误信息为：" + str(err))
        return item


class A79taoJsonPipeline(object):
    def __init__(self):
        self.file=open("./file/a79.json","wb")

    def process_item(self, item, spider):
        
        line=json.dumps(item,ensure_ascii = False)+",\n"
        self.file.write(line.encode('utf-8'))
        return item

    def spider_closed(self):
        self.file.close()

class A79taoSqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=env.MYSQL_HOST,
            db=env.MYSQL_DBNAME,
            user=env.MYSQL_USER,
            passwd=env.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into active_list(other_id,act_from,tag,title,description,created_at)
                  value (%s,%s,%s,%s,%s,%s)""",
                (item['id'],
                "a79tao",
                "hm",
                 item['title'],
                 item['description'],
                 item['created_at']))
            self.connect.commit()
        except Exception as err:
            print("重复插入了==>错误信息为：" + str(err))
        return item