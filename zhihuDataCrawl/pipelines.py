# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo
from zhihuDataCrawl.items import ZhihudatacrawlItem

class ZhihudatacrawlPipeline(object):

    def __init__(self, mongo_uri, mongo_db):#,replicaset
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        # self.replicaset = replicaset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'yunqi')
            # replicaset = crawler.settings.get('REPLICASET') 集群
        )

    def open_spider(self, spider):
        # self.client = pymongo.MongoClient(self.mongo_uri,replicaset=self.replicaset) 集群
        self.client = pymongo.MongoClient(self.mongo_uri,)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider): #默认开始执行
        # if isinstance(item,ZhihudatacrawlItem):
        #     self._process_booklist_item(item)
        # else:
        #     self._process_bookeDetail_item(item)
        # return item
        self._process_answerslist_item(item)



    def _process_answerslist_item(self,item):
        '''
        处理回答的信息
        :param item:
        :return:
        '''
        self.db.answersInfos.insert(dict(item))