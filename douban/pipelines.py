# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter


class DoubanPipeline(object):
    def __init__(self):
        self.fp = open("douBan.json", 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')

    def open_spider(self, spider):
        print('爬虫开始')
        pass

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def closs_spider(self, spider):
        self.fp.close()
        print("爬虫结束")
        pass
