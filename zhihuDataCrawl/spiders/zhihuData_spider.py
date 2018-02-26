# # coding:utf-8
# import scrapy
# import os
# import json
#
# class ZhihuuserSpider(scrapy.Spider):
#     name = 'zhihuuser'
#     allowed_domains = ['www.zhihu.com']
#     start_urls = ['http://www.zhihu.com/']
#     start_user = 'excited-vczh'
#     # 一：对用户关注列表的请求构造
#     # 用户关注列表 start_user为起始大v，followees_include为请求参数，limit为每页显示用户数，默认20，offset为页码参数，首页为0
#     followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
#     followees_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
#
#     # 二：对用户粉丝列表的请求构造
#     # 用户关注列表 start_user为起始大v，followees_include为请求参数，limit为每页显示用户数，默认20，offset为页码参数，首页为0
#     followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
#     followers_include = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
#
#     # 三：对用户详细信息的请求构造
#     user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
#     user_include = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
#     def start_requests(self):
#         # 分别举列表url和用户url示例，以验证是否能够爬取
#         # 关注列表url示例
#         # 返回401是请求验证用户的身份，知乎的首页是要求验证用户的身份才能进入，所以需要在settings里面设置authorization
#         # url='https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=60&limit=20'
#         # 用户详细url示例
#         # url='https://www.zhihu.com/api/v4/members/lanfengxing?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
#         # yield scrapy.Request(url, callback=self.parse)
#         # 构造用户关注列表的请求 主要用到format方法
#
#         yield scrapy.Request(url=self.followees_url.format(user=self.start_user, include=self.followees_include, offset=0, limit=20), callback=self.parse_followees)
#         # 构造用户粉丝列表的请求 主要用到format方法
#         yield scrapy.Request(url=self.followers_url.format(user=self.start_user, include=self.followers_include, offset=0, limit=20),callback=self.parse_followers)
#         # 对用户详细信息的请求构造
#         yield scrapy.Request(url=self.user_url.format(user=self.start_user, include=self.user_include),callback=self.parse_user)
#     # 解析关注列表
#     def parse_followees(self, response):
#         results = json.loads(response.text)
#         if 'data' in results.keys():
#             for result in results.get('data'):
#                 # 解析关注列表，得到所关注人的url_token，构造解析详细信息请求
#                 yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'), include=self.user_include),callback=self.parse_user)
#         # 构造翻页请求
#         if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
#             next = results.get('paging').get('next')
#             yield scrapy.Request(url=next, callback=self.parse_followees)
#
#     # 解析粉丝列表
#     def parse_followers(self, response):
#         results = json.loads(response.text)
#         if 'data' in results.keys():
#             for result in results.get('data'):
#                 # 解析关注列表，得到所关注人的url_token，构造解析详细信息请求
#                 yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'), include=self.user_include),
#                                      callback=self.parse_user)
#         # 构造翻页请求
#         if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
#             next = results.get('paging').get('next')
#             yield scrapy.Request(url=next, callback=self.parse_followers)
#
#     # 解析用户详细信息,由于我们任务的目标是获取用户详细信息，因此在这一步要确定哪些信息是被使用，在items里面做相应设置
#     def parse_user(self, response):
#         # item = Zhihu2Item()
#         # 返回的response是json格式，因此需要解析json
#         results = json.loads(response.text)
#         # 遍历item数据结构的键名，item.field可以得到数据结构的所有键
#         # for field in item.fields:
#         #     # 如果item的键名在网页里面，则遍历赋值
#         #     if field in results.keys():
#         #         item[field]=results.get(field)
#         # yield item
#
#         # 提取用户的关注列表
#         yield scrapy.Request(url=self.followees_url.format(user=results.get('url_token'),include = self.followees_include,offset=0, limit=20),callback=self.parse_followees)
#         # 提取用户的粉丝列表
#         yield scrapy.Request(url=self.followers_url.format(user=results.get('url_token'), include=self.followers_include, offset=0, limit=20),callback=self.parse_followers)
#
# # class ZhiHuDataSpider(CrawlSpider):
# #     name = 'zhihuData'
# #     allowed_domains = ['zhihu.com']
# #     start_urls = ['https://www.zhihu.com/signup?next=%2F']
# #
# #     def start_requests(self):
# #         # 首先进入登录界面
# #
# #         if os.path.exists('zhihu_cookie'):
# #             with open('zhihu_cookie', 'r') as f:
# #                 cookies = {}
# #                 for line in f.read().split(';'):
# #                     name, value = line.strip().split('=', 1)  # 1代表只分割一次
# #                     cookies[name] = value
# #                 return [Request(
# #                     'https://www.zhihu.com/search?type=content&q=%E5%88%98%E5%BE%B7%E5%8D%8E',
# #                     # 'https://www.zhihu.com/people/liu-xiao-lei-26-55/activities',
# #                     cookies=cookies,
# #                     meta={'cookiejar': 1},
# #                     callback=self.parse_search_info,
# #                     errback=self.parse_err,
# #                 )]
# #
# #         return [Request('https://www.zhihu.com/signup?next=%2F', callback=self.start_login, meta={'cookiejar': 1})]
# #
# #     def parse_search_info(self,response):
# #         list = response.xpath('//div[@class="List"]')
# #         list_urls = list.xpath('//div[@class="List-item"]/div/h2/div/a/@href').extract()
# #         for href in list_urls:
# #             url = urljoin(response.url,href)
# #             yield scrapy.Request(url=url,callback=self.parse_body)
# #
# #     def parse_body(self,response):
# #         yield scrapy.Request(url='https://www.zhihu.com/api/v4/questions/20799024/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=&limit=3&sort_by=default',callback=self.liuxiaolei)
# #         # title = response.xpath('//h1[@class="QuestionHeader-title"]/text()').extract_first()
# #         # item = ZhihudatacrawlItem()
# #         # item = response.meta['item']
# #         # body = response.xpath(".//*[@class='postBody']")
# #         # item['cimage_urls'] = body.xpath('.//img//@src').extract()  # 提取图片链接
# #         # yield item
# #     def liuxiaolei(self,response):
# #         print 'ddd'
# #     def parse_err(self, response):
# #         self.logger.error('crawl %s fail' % response.url)

