# coding:utf-8
import scrapy
import json

from zhihuDataCrawl.items import ZhihudatacrawlItem
from ..scrapy_redis.spiders import RedisSpider
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ZhihuSearchSpider(RedisSpider):
    name = 'zhihusearch'
    allowed_domains = ['www.zhihu.com']
    # start_urls = ['http://www.zhihu.com/']
    # start_search = '刘德华'
    redis_key = 'ZhihuSpider:start_urls'

    def parse(self, response):
        '''
        解析查询列表
        :param response: 返回结果
        :return:
        '''
        #问题回答列表
        answers_url = 'https://www.zhihu.com/api/v4/questions/{question_id}/answers?include={include}&offset={offset}&limit={limit}&sort_by=default'
        answers_include = 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics'
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                if 'search_result' == result.get('type'):#type等于search_result为搜索结果，其它的不考虑
                    # 解析问题回答列表，得到question中的id
                    object_is = result.get('object')
                    if 'question' in object_is.keys():
                        print result.get('object').get('question').get('id')
                        yield scrapy.Request(url=answers_url.format(question_id=result.get('object').get('question').get('id'),include=answers_include,offset='',limit=3),callback=self.answers_list)
        # 构造翻页请求
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next = results.get('paging').get('next')
            yield scrapy.Request(url=next, callback=self.parse)

    def answers_list(self,response):
        '''
        解析回复列表
        :param response: 返回的数据
        :return:
        '''
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                url ="https://www.zhihu.com/question/{question_id}/answer/{answer_id}".format(question_id=result.get('question').get('id'),answer_id=result.get('id'))
                answersListItem = ZhihudatacrawlItem(title=result.get('question').get('title'), name=result.get('author').get('name'),
                                                  gender=result.get('author').get('gender'), headline=result.get('author').get('headline'),
                                                  content=result.get('content'), excerpt=result.get('excerpt'),
                                                  created_time=result.get('created_time'),voteup_count=result.get('voteup_count'),
                                                     comment_count=result.get('comment_count'),url=url
                                                     )
                yield answersListItem
        # 构造翻页请求
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next = results.get('paging').get('next')
            yield scrapy.Request(url=next, callback=self.answers_list)
