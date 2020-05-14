# -*- coding: utf-8 -*-
import scrapy
import re
from lxml import etree
from douban.items import douBanItem
from scrapy_redis.spiders import RedisSpider


def reSearch(search_content, response):
    if '<span class="pl">{0}'.format(search_content) in response.text:
        search = re.compile('<span class="pl">' + search_content + ':</span>\s(.*?)<br/>')
        result = search.search(response.text).group(1)
    else:
        result = None
    return result


def reSearchHref(href_name, html, response):
    if '<span class="pl">{0}'.format(href_name) in response.text:
        search_result = html.xpath('//span[contains(text(),"{0}")]/following-sibling::a/text()'.format(href_name))
        search_result = "/".join(search_result).replace("\u3000", " ")
        if len(search_result) == 0:
            search_result = None
    else:
        search_result = None
    return search_result


class douBanBookSpider(RedisSpider):
    listFlag = False
    handleList = [403, 404, 500]
    roll = 90
    targetUrl = 'https://book.douban.com/subject/'
    # subjectNum = 34882634
    # url = 'https://book.douban.com/subject/' + str(subjectNum) + '/'
    name = 'douban_book'
    allowed_domains = ['book.douban.com']
    # https://book.douban.com/subject/34882631/
    # start_urls = ['http://book.douban.com/subject/' + str(subjectNum) + '/']
    redis_key = "douban:start_urls"

    def parse(self, response):
        if response.status not in self.handleList:
            if 'book' in response.url:
                html = etree.HTML(response.text)
                bookName = html.xpath('//span[@property="v:itemreviewed"]/text()')[0]
                author = reSearchHref(" 作者", html, response)
                press = reSearch("出版社", response)
                originalName = reSearch("原作名", response)
                pressYear = reSearch("出版年", response)
                pageNum = reSearch("页数", response)
                price = reSearch("定价", response)
                binding = reSearch("装帧", response)
                isbn = reSearch("ISBN", response)
                series = reSearchHref("丛书", html, response)
                translator = reSearchHref(" 译者", html, response)
                publisher = reSearchHref("出品方", html, response)
                if ("目前无人评价" in response.text) or ("评价人数不足" in response.text):
                    rating = None
                else:
                    rating = html.xpath("//strong/text()")[0].strip()
                if ("目前无人评价" in response.text) or ("评价人数不足" in response.text):
                    ratingSum = None
                else:
                    ratingSum = html.xpath('//span[@property="v:votes"]/text()')[0].strip()
                item = douBanItem(bookName=bookName, author=author, press=press, originalName=originalName, pressYear=pressYear,
                                  pageNum=pageNum, price=price, binding=binding, isbn=isbn, series=series,
                                  translator=translator,
                                  publisher=publisher, rating=rating, ratingSum=ratingSum, kind='book')

            elif 'drama' in response.url:
                item = douBanItem(bookName=None, author=None, press=None, originalName=None,
                                  pressYear=None,
                                  pageNum=None, price=None, binding=None, isbn=None, series=None,
                                  translator=None,
                                  publisher=None, rating=None, ratingSum=None, kind='drama')
            elif 'movie' in response.url:
                item = douBanItem(bookName=None, author=None, press=None, originalName=None,
                                  pressYear=None,
                                  pageNum=None, price=None, binding=None, isbn=None, series=None,
                                  translator=None,
                                  publisher=None, rating=None, ratingSum=None, kind='movie')
            elif 'music' in response.url:
                item = douBanItem(bookName=None, author=None, press=None, originalName=None,
                                  pressYear=None,
                                  pageNum=None, price=None, binding=None, isbn=None, series=None,
                                  translator=None,
                                  publisher=None, rating=None, ratingSum=None, kind='music')
            else:
                item = douBanItem(bookName=None, author=None, press=None, originalName=None,
                                  pressYear=None,
                                  pageNum=None, price=None, binding=None, isbn=None, series=None,
                                  translator=None,
                                  publisher=None, rating=None, ratingSum=None, kind='else')
            yield item
        if 'book' in response.url:
            url = response.url[0:32]
            number = int(response.url[32:40])+1
            url = url+str(number)+'/'
        elif 'drama' in response.url:
            number = int(response.url[38:46]) + 1
            url = self.targetUrl + str(number) + '/'
        elif 'movie' in response.url or 'music' in response.url:
            number = int(response.url[33:41]) + 1
            url = self.targetUrl + str(number) + '/'
        else:
            url = response.url[0:32]
            number = int(response.url[32:40]) + 1
            url = url + str(number) + '/'
        if self.listFlag is not True:
            count = number
            while count <= 34888888:
                yield scrapy.Request(url=self.targetUrl + str(count) + '/')
                count += 1
            self.listFlag = True
        # if number <= 34888888:
        yield scrapy.Request(url=url, callback=self.parse)
        # else:
        #     return
        # else:
        #     return

# book
# movie
# music