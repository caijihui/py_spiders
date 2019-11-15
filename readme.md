##  spider 爬虫

- 安装扩展
    - pip3  install -r requirements.txt
- 初始化,安装scrapy
    -  `pip3 install scrapy`
- 创建爬虫
    - `scrapy genspider name domain`


#### 爬取微博热搜
``` 
    scrapy crawl weiboHot
```

#### 爬取豆瓣电源top250
``` 
    scrapy crawl doubanTop250
```