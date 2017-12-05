# -*- coding: utf-8 -*-

import re
import csv

import scrapy


class PachSpider(scrapy.Spider):
    name = "html_baidu"
    start_urls = ['http://news.baidu.com']

    url_text = None
    urls_map = None

    def parse(self, response):
        if self.url_text == None:
            self.url_text = open('data/total_urls.txt', 'a')

        self.urls_map = {}
        with open('data/baidu_urls.txt', 'r') as baiduurl_text:
            baidu_urls = csv.reader(baiduurl_text, delimiter= ' ')
            for url in baidu_urls:
                print url
                self.urls_map[url[0]] = url[1]
        for url in self.urls_map:
            yield scrapy.Request(url=url, callback=self.parseUrl)

    def parseUrl(self, response):
        for href in response.xpath('//a/@href').extract():
            if not href.startswith('http'):
                continue;
            if not re.match('(http|https)://.*baidu.com.*', href):
                self.url_text.write(href + ' ' + self.urls_map[response._get_url()] + ' ' + '\n')
