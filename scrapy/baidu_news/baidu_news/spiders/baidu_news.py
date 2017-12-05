# -*- coding: utf-8 -*-
import re

import scrapy


class PachSpider(scrapy.Spider):  # 定义爬虫类，必须继承scrapy.Spider
    name = 'baidu_news'  # 设置爬虫名称
    allowed_domains = ['news.baidu.com']  # 爬取域名
    start_urls = ['http://news.baidu.com/widget?id=civilnews&ajax=json']

    qishiurl = [  # 的到所有页面id
                  'InternationalNews',
                  'FinanceNews',
                  'EnterNews',
                  'SportNews',
                  'AutoNews',
                  'HouseNews',
                  'InternetNews',
                  'InternetPlusNews',
                  'TechNews',
                  'EduNews',
                  'GameNews',
                  'DiscoveryNews',
                  'HealthNews',
                  'LadyNews',
                  'SocialNews',
                  'MilitaryNews',
                  'PicWall'
                  ]

    urllieb = []
    for i in range(0, len(qishiurl)):  # 构造出所有idURL
        kaishi_url = 'http://news.baidu.com/widget?id=' + qishiurl[i] + '&ajax=json'
        urllieb.append(kaishi_url)

    url_text = None
    baiduurl_text = None

    def parse(self, response):  # 选项所有连接
        if self.url_text == None or self.baiduurl_text == None:
            self.url_text = open('data/total_urls.txt', 'w')
            self.baiduurl_text = open('data/baidu_urls.txt', 'w')

        for j in range(0, len(self.urllieb)):
            a = '正在处理第%s个栏目:url地址是：%s' % (j, self.urllieb[j])
            yield scrapy.Request(url=self.urllieb[j], callback=self.enxt)  # 每次循环到的url 添加爬虫

    def enxt(self, response):
        classify = re.match('.*id=([a-zA-Z]+)?\&ajax=json', response._get_url()).group(1)
        neir = response.body.decode("utf-8")
        pat2 = '"m_url":"(.*?)"'
        url = re.compile(pat2, re.S).findall(neir)  # 通过正则获取爬取页面 的URL
        for k in range(0, len(url)):
            zf_url = url[k]
            url_zf = re.sub("\\\/", "/", zf_url)
            pduan = url_zf.find('http://')
            if pduan == 0:
                if (re.match('(http|https)://.*baidu.com.*class=.*', url_zf)):
                    self.baiduurl_text.write(url_zf + ' ' + classify + ' ' + "\n")
                else:
                    self.url_text.write(url_zf + ' ' + classify + ' ' + "\n")
