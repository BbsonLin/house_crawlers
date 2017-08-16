# -*- coding: utf-8 -*-
import json
import time
import scrapy

from scrapy.http import Request


class SaleinfoSpider(scrapy.Spider):
    name = "saleInfo"
    allowed_domains = ["sale.591.com.tw"]
    start_urls = ['http://sale.591.com.tw/']
    row_number = 0

    def __init__(self, regionid=1, *args, **kwargs):
        self.region_id = regionid

    def parse(self, response):
        search_url = \
            "{}/home/search/list?type=2&&shType=host&&regionid={}".format(
                self.start_urls[0], self.region_id)
        yield Request(search_url, callback=self.parse_response,
                      meta={'search_url': search_url})

    def parse_response(self, response):
        response_body = response.body.decode('utf-8')
        data = json.loads(response_body)['data']
        total = int(data['total'])
        house_list = list()

        while self.row_number <= total:
            house_list += data['house_list']
            self.row_number += 30
            next_url = "{}&&firstRow={}&&totalRows={}".format(
                response.meta['search_url'], self.row_number, total)
            yield Request(next_url, callback=self.parse_response,
                          meta={'search_url': response.meta['search_url']})

        house_list_length = len(house_list)

        if house_list_length > 0:
            self.logger.info("{} Crawling Done...\nTotal get {} houses".format(
                response.meta['search_url'], house_list_length))
            time.sleep(1)

            yield {"house_list": house_list,
                   "total": house_list_length,
                   "search_url": response.meta['search_url']}
