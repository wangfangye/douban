# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class CommentItem(scrapy.Item):
    collection = 'comment'
    comments = scrapy.Field()

class DiscussItem(scrapy.Item):
    collection = 'discuss'
    likes = scrapy.Field()
    topic = scrapy.Field()
    text = scrapy.Field()
    group = scrapy.Field()
    time = scrapy.Field()
