# -*- coding: utf-8 -*-

import re
import csv

import scrapy

import time

class PachSpider(scrapy.Spider):
    name = "html_news"
    start_urls = ['http://news.baidu.com']

    news_text = None
    urls_map = None

    def parse(self, response):
        if self.news_text == None:
            self.news_text = open('data/news-'+time.strftime('%Y-%m-%d', time.localtime())+'.txt', 'w')

        self.urls_map = {}
        with open('data/urls.txt', 'r') as urls_text:
            urls = csv.reader(urls_text, delimiter=' ')
            for url in urls:
                self.urls_map[url[0]] = url[1]
        for url in self.urls_map:
            yield scrapy.Request(url=url, callback=self.parseUrl)

    def parseUrl(self, response):
        self.news_text.write('[' + self.urls_map[response._get_url()] + ']' + '\n')
        self.news_text.write(
            re.sub('(?i)(<script).*?((</script>)|(/>)|(>))', '', response.xpath('//body').extract()[0].strip()))
        self.news_text.write('\n')
