# 知乎分布式爬取搜索数据并抓取回答信息
## 一、描述

​	爬虫采用scrapy 框架，redis分布式，并对url进行去重.数据存储用Mongodb,此小项目在windos平台安装运行。
本地搭建的redis，创建爬虫取数据对列：lpush ZhihuSpider:start_urls https://www.zhihu.com/api/v4/search_v3?t=general&q=lxl&correction=1&search_hash_id=7809a94f02be5faf4edebfd7774b3c6b&time_zone=a_day&offset=0&limit=10

其中：q为要查询的信息，我这里用我的名字查询的，最后爬取了478,页面数据是479，少了一个正在查找中。后期会上一些截图。

## 二、安装

​	安装的软件如下：

| 名称        | 版本                                       |
| --------- | ---------------------------------------- |
| python    | 2.7.132.7.13 \|Anaconda 4.4.0 (64-bit)\| |
| Scrapy    | 1.5.0                                    |
| lxml      | 3.7.3.0                                  |
| libxml2   | 2.9.4                                    |
| cssselect | 1.0.3                                    |
| parsel    | 1.4.0                                    |
| w3lib     | 1.19.0                                   |
| Twisted   | 17.9.0                                   |

## 四、步骤

1.创建zhihu数据爬虫

​	scrapy startproject zhihuDataCrawl

2.创建spiders

​	zhihuspider.py

3.重写items.py

4.重写数据存储pipelines.py

5.调用第三方scrapy_redis架包

6.配置settings.py

7.创建启动脚步begin.py
## 五、图片展示
  爬虫爬取的回答总数据量：
  
  https://github.com/liuxiaolei319/zhihuDataCrawl/blob/master/image/13.jpg
  
  爬虫爬取的回答数据格式：
  
  https://github.com/liuxiaolei319/zhihuDataCrawl/blob/master/image/12.jpg
  
  添加redis队列，添加需要爬取数据的URL：
  
  https://github.com/liuxiaolei319/zhihuDataCrawl/blob/master/image/14.jpg
  
  启动脚本：
  
  https://github.com/liuxiaolei319/zhihuDataCrawl/blob/master/image/15.jpg
  
