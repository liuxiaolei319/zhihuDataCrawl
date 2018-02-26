# 知乎分布式爬取搜索数据并抓取回答信息
## 一、描述

​	爬虫采用scrapy 框架，redis分布式，并对url进行去重.数据存储用Mongodb,此小项目在windos平台安装运行。

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
