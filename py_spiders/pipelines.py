# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import pymysql
import time
from py_spiders import settings,env

class PySpidersPipeline(object):
    def process_item(self, item, spider):
        return item

## 保存为json数据
class DouBan250JsonPipeline(object):
    def __init__(self):
        self.file=open("./file/doubanTop250.json","wb")

    def process_item(self, item, spider):
        
        line=json.dumps(item,ensure_ascii = False)+",\n"
        self.file.write(line.encode('utf-8'))
        return item

    def spider_closed(self):
        self.file.close()
## 一次性入库
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
            self.cursor.execute("""select id from doubantop250 where movie_name = %s""",(item['movie_name']))
            res = self.cursor.fetchone()
            if res == None:
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
        self.file=open("./file/v2exHot.json","wb")

    def process_item(self, item, spider):
        
        line=json.dumps(item,ensure_ascii = False)+",\n"
        self.file.write(line.encode('utf-8'))
        return item

    def spider_closed(self):
        self.file.close()

## v2ex 
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


## a79tao 线报信息爬取
class A79taoJsonPipeline(object):
    def __init__(self):
        self.file=open("./file/a79.json","wb")

    def process_item(self, item, spider):
        
        line=json.dumps(item,ensure_ascii = False)+",\n"
        self.file.write(line.encode('utf-8'))
        return item

    def spider_closed(self):
        self.file.close()

## a79tao 线报信息爬取
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
            self.cursor.execute("""select id from active_list where act_from = 'a79tao' and other_id = %s""",(item['id']))
            res = self.cursor.fetchone()
            if res == None:
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
            print("出错，错误信息为：" + str(err))
        return item

## 测试健客网 -药品数据 （无效）
class JianKeSqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=env.LMYSQL_HOST,
            db=env.LMYSQL_DBNAME,
            user=env.LMYSQL_USER,
            passwd=env.LMYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""select id from jianke_list where  other_id = %s""",(item['other_id']))
            res = self.cursor.fetchone()
            if res == None:
                self.cursor.execute(
                    """insert into jianke_list(other_id,cn_name,pihao,price,title,url)
                    value (%s,%s,%s,%s,%s,%s)""",
                    (item['other_id'],
                     item['cn_name'],
                    item['pihao'],
                    item['price'],
                    item['title'],
                    item['url']
                   ))
                self.connect.commit()
                
        except Exception as err:
            print("出错，错误信息为：" + str(err))
        return item


#保存为json数据 和 存储入库
class weiboHotPipeline(object):
    def __init__(self):
        self.file=open("./file/weiboHot.json","wb")

    def process_item(self, item, spider):
        
        line=json.dumps(item,ensure_ascii = False)+",\n"
        self.file.write(line.encode('utf-8'))
        return item

    def spider_closed(self):
        self.file.close()

## 微博热搜-存储数据库
class weiboHotSqlPipeline(object):
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
            self.cursor.execute("""select id from hot where type = 1 and other_id = %s""",(item['id']))
            res = self.cursor.fetchone()
            if res == None:
                self.cursor.execute(
                    """insert into hot(other_id,type,title,url,click,created_at,updated_at)
                    value (%s,%s,%s,%s,%s,%s,%s)""",
                    (item['id'],1,item['title'],item['url'],item['click'],
                    time.strftime('%Y-%m-%d %H:%M:%S'),
                    time.strftime('%Y-%m-%d %H:%M:%S')))
            else :
                self.cursor.execute(
                    """update hot set title =%,url=%s,click=%s where type = 1 and other_id = %s """,
                    (item['title'],item['url'],item['id'],item['click']))
            self.connect.commit()
                
        except Exception as err:
            print("出错，错误信息为：" + str(err))
        return item

    def spider_closed(self):
        self.file.close()