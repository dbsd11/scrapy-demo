# -*- coding: utf-8 -*-

import scrapy
import sys


class pm25_in_html(scrapy.Spider):
    name = "pm25_in_html"
    start_urls = ["http://pm25.in"]

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def parse(self, response):
        for cityUrl in response.xpath('//a/@href').extract():
            if cityUrl == '/' or len(cityUrl) > 20:
                continue
            # yield scrapy.Request(self.start_urls[0] + cityUrl, callback=self.cityParse)
        yield scrapy.Request(self.start_urls[0] + "/rank", callback=self.cityParse)

    def cityParse(self, response):
        cityData = []
        for place in response.xpath('//tr'):
            placeData = []
            for text in place.xpath('td[not(@class)]'):
                param = str(text.xpath("string(.)").extract()[0]).strip()
                if param == '_':
                    placeData.append('')
                else:
                    placeData.append(param)
            cityData.append(placeData)

        fileName = 'data/' + response._get_url()[15:] + '.csv'

        f = open(fileName, 'w')
        f.write('\n'.join(map(lambda placeData: ','.join(placeData), cityData)))
