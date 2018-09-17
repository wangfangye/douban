# -*- coding: utf-8 -*-
import scrapy
import urllib.request
from scrapy.http import Request,FormRequest
import ssl
import time
from douban_comment.items import CommentItem
from douban_comment.items import DiscussItem

class DiscussSpider(scrapy.Spider):
    name = "discuss"
    allowed_domains = ["douban.com"]
    # 登录使用
    header = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    def start_requests(self):
        return  [Request("https://accounts.douban.com/login",callback=self.login,headers=self.header,meta={"cookiejar":1})]


    def login(self,response):
        captcha = response.xpath('//*[@id="captcha_image"]/@src').extract()
        print(captcha)
        if len(captcha) > 0:
            # 有验证码，人工输入验证码
            urllib.request.urlretrieve(captcha[0],
                                       filename=r"D:\code\pycharm\douban\douban_comment\douban_comment\captchaImage\captcha.png")
            captcha_value = input('查看captcha.png,有验证码请输入:')
            data = {
                "form_email": "18353113181@163.com",
                "form_password": "9241113minda",
                "captcha-solution": captcha_value,
            }
        else:
            # 此时没有验证码
            print("无验证码")
            data = {
                "form_email": "18353113181@163.com",
                "form_password": "9241113minda",
            }
        print("正在登陆中.....")
        # 进行登录
        return [
            FormRequest.from_response(
                response,
                meta={"cookiejar": response.meta["cookiejar"]},
                headers=self.header,
                formdata=data,
                callback=self.login_next,
            )
        ]

    def login_next(self, response):
        # 显示是否登录成功
        title = response.xpath('//title/text()').extract()[0]
        if u'登录豆瓣' in title:
            print("登录失败，请重试")
        else:
            print("登陆成功")
        # 登录成功，跳转到制定页面
        yield scrapy.Request('https://www.douban.com/group/explore?start=0', callback=self.parse)

    def parse(self, response):
    # 1、 从response提取Comment，填满CommentItem
        title = response.xpath('//title/text()').extract()
        print(title)
        print(response.url)

        discusses = response.css('.channel-item')
        for discuss in discusses:
            item = DiscussItem()
            item['likes'] = discuss.css('.likes::text').extract_first().replace('\r','').replace('\n','').replace('\t','')
            item['topic'] = discuss.css('.bd h3 a::text').extract_first().replace('\r','').replace('\n','').replace('\t','')
            item['text'] = discuss.css('.block p::text').extract_first().replace('\r','').replace('\n','').replace('\t','')
            item['group'] = discuss.css('.source .from a::text').extract_first().replace('\r','').replace('\n','').replace('\t','')
            item['time'] = discuss.css('.pubtime::text').extract_first()
            yield item

    # 2、 提取下一页的url
        base_url = 'https://www.douban.com/group/explore'
        next = response.css('.paginator .next a::attr(href)').extract_first()
        page_url = base_url + next
        time.sleep(3)
        yield Request(page_url, callback=self.parse)




