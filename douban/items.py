# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class douBanItem(scrapy.Item):
    # 书名
    bookName = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 出版社
    press = scrapy.Field()
    # 原著名
    originalName = scrapy.Field()
    # 出版日期
    pressYear = scrapy.Field()
    # 著作页数
    pageNum = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 装帧
    binding = scrapy.Field()
    # ISBN
    isbn = scrapy.Field()
    # 译者
    translator = scrapy.Field()
    # 出品方
    publisher = scrapy.Field()
    # 评分
    rating = scrapy.Field()
    # 评论人数
    ratingSum = scrapy.Field()
    # 丛书
    series = scrapy.Field()
    # 类型
    kind = scrapy.Field()
