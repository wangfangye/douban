# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from openpyxl import Workbook

class DoubanCommentPipeline(object):
    def __init__(self):#创建excel，填写表头
        '''
                initialize the object
                '''
        self.spider = None
        self.count = 0

    def open_spider(self, spider):
        '''
        create a queue
        :return:
        '''
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['likes', 'topic', 'text', 'group','time'])

    def process_item(self, item, spider):
        line = [item['likes'],item['topic'],item['text'],item['group'],item['time']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        # self.wb.save('douban_comment/discuss.xlsx')  # 保存xlsx文件
        return item

    def close_spider(self,spider):
        # file_name = _generate_filename(spider, file_format='xlsx')
        # self.wb.save(file_name)
        self.wb.save('discuss.xlsx')