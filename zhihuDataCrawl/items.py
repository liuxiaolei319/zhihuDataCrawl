# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihudatacrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 标题
    name = scrapy.Field()  # 发贴人姓名
    gender = scrapy.Field()  # 性别
    headline = scrapy.Field()  # 职业
    content = scrapy.Field()  # 文章内容
    excerpt = scrapy.Field()  # 文章摘录
    created_time = scrapy.Field()  # 创建时间格式为时间搓
    voteup_count = scrapy.Field()  # 点赞数
    comment_count = scrapy.Field() # 评论数
    url = scrapy.Field() #网页地址
