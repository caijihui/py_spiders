# -*- coding: utf-8 -*-
import threading
import requests
import time
from scrapy import Selector
import pymysql
import sys
sys.path.append("..")
from py_spiders import env

DB_URL = env.MYSQL_HOST
DB_USER = env.MYSQL_USER
DB_PASSWORD = env.MYSQL_PASSWD
DB_NAME = env.MYSQL_DBNAME
DB_CHARSET = 'utf8'

# DB_URL = "104.225.159.94"
# DB_USER = "product"
# DB_PASSWORD = "password"
# DB_NAME = "caiyuanzi"
# DB_CHARSET = 'utf8'


class MyProxy():

    conn = pymysql.connect(DB_URL, DB_USER, DB_PASSWORD, DB_NAME, charset=DB_CHARSET)
    cursor = conn.cursor()

    def __init__(self):
        DeleteIPThread().start()

    def get_ip(self):
        '''
        从数据库中随机拿一个有效IP
        返回None时表示没有地址可用了
        :return: (ip, port, speed, type) or None
        '''
        sql = '''
            select ip,port,speed,proxy_type from proxy_ip order by rand() limit 1;
        '''
        self.cursor.execute(sql)
        print(self.cursor.arraysize);
        if self.cursor.arraysize > 0:
            ## (ip, port, speed, type)
            res = self.cursor.fetchone()
            print(res)
            a = self.judge_ip(res[0], res[1])
            if a :
                return res
            else:
                print('false ++++')
            # if self.judge_ip(res[0], res[1]):
            #     return res
            # else:
            #     return self.get_ip()
        # return self.get_ip()

    def crawl_ips(self):
        '''
        爬取西刺免费代理的地址池
        :return: 无返回
        '''
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTZjNDNmNjgzZWY5OWQ4ZWRmNTA5MzU3YWJiOGJlYWMwBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVBsU3h6aU0xa25KWlZXZE5qZ0tGd21xYkJtc3J0K2w0YlEwdUhlNjFBN009BjsARg%3D%3D--abe7f4154a205b8515bfb204e3fe924006ae1d68",
            "Host": "www.xicidaili.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        url = "http://www.xicidaili.com/nn/1"
        response = None
        for i in range(5):
            try:
                response = requests.get(url, headers=headers, timeout=10)
            except requests.exceptions.Timeout:
                print("请求超时，第%d次重新请求..." % (i+1))
                response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                break
        if response is None:
            print("网络太差，或者地址被封，11次请求均超时")
            return
        s = Selector(response)
        all_list = s.xpath('//table[@id="ip_list"]/tr')[1:]
        for item in all_list[1:]:
            try:
                line = item.xpath('./td')
                ip = line[1].xpath('string(.)').extract_first()
                port = line[2].xpath('string(.)').extract_first()
                address = ''
                if len(line[3].xpath('./a')) > 0:
                    address = line[3].xpath('./a/text()').extract_first()
                    address = str(address)
                type = line[5].xpath('string(.)').extract_first()
                speed = 0.0
                if len(line[6].xpath('./div/@title')) > 0:
                    speed_str = line[6].xpath('./div/@title').extract_first()
                    speed = float(speed_str[:-1])

                print(ip, port, address, type, speed)

                sql = '''
                    INSERT 
                    INTO proxy_ip(ip, port, address, proxy_type, speed) 
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');
                '''
                self.cursor.execute(sql.format(ip, port, address, type, speed))
                self.conn.commit()
            except:
                print(sys.exc_info())

    def judge_ip(self, ip, port):
        '''
        判断给出的代理 ip 是否可用
        :param ip:
        :param port:
        :return:
        '''
        http_url = 'https://www.baidu.com/'
        proxy_url = 'http://{0}:{1}'.format(ip, port)

        try:
            proxy_dict = {
                'http': proxy_url
            }
            print("正在测试代理IP是否可用 => ", proxy_url)
            response = requests.get(http_url, proxies=proxy_dict, timeout=5)

        except Exception as e:
            print("代理：", proxy_url, "不可用，即将从数据库中删除")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 or code < 300:
                print("代理 => ", proxy_url, "可用")
                return True
            else:
                print(code+'无效')
                self.delete_ip(ip)
                return False

    def delete_ip(self, ip):
        '''
        删除不可用的IP
        :param ip:
        :return:
        '''
        sql = '''
            delete from proxy_ip WHERE ip='{0}';
        '''
        self.cursor.execute(sql.format(ip))
        self.conn.commit()
        print(ip+'已经删除')

class DeleteIPThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        conn = pymysql.connect(DB_URL, DB_USER, DB_PASSWORD, DB_NAME, charset=DB_CHARSET)
        cursor = conn.cursor()
        sql = "select ip,port from proxy_ip;"
        proxy = MyProxy()
        while True:
            cursor.execute(sql)
            all_list = cursor.fetchall()
            for ip,port in all_list:
                print(ip, port)
                if proxy.judge_ip(ip, port) is False:
                    proxy.delete_ip(ip)
                time.sleep(1)
            time.sleep(20)

    def circle_judge(self):
        pass

if __name__ == '__main__':
    my_proxy = MyProxy()
    my_proxy.crawl_ips()
    # my_proxy.get_ip()