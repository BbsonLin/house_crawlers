# -*- coding: utf-8 -*-
import json
import scrapy

from scrapy.http import Request

class SaleinfoSpider(scrapy.Spider):
    name = "saleInfo"
    allowed_domains = ["sale.591.com.tw"]
    start_urls = ['http://sale.591.com.tw/']
    region_ids = list(range(1, 27))

    def parse(self, response):
        # for region_id in self.region_ids:
        #     search_url = "{}/home/search/list?type=2&&regionid={}".format(
        #         self.start_urls[0], region_id)
        #     yield Request(search_url, callback=self.parse_response)
        search_url = "{}/home/search/list?type=2&&regionid={}".format(
            self.start_urls[0], 8)
        yield Request(search_url, callback=self.parse_response, meta={'search_url':search_url})

    def parse_response(self, response):
        response_body = response.body.decode('utf-8')
        data = json.loads(response_body)['data']
        total = int(data['total'])
        row_number = 0
        house_list = list()

        while row_number <= 60:
            house_list += data['house_list']
            row_number += 30
            next_url = "{}&&firstRow={}&&totalRows={}".format(
                response.meta['search_url'], row_number, total)
            yield Request(next_url, callback=self.parse_response,
                          meta={'search_url':response.meta['search_url']})
        yield {"house_list": house_list, "total": len(house_list)}
        # print("Response body: {}".format(type(response_body)))

    def parse_all_house(self, total):
        while row_number <= 60:
            house_list += data['house_list']
            row_number += 30
            next_url = "{}&&firstRow={}&&totalRows={}".format(
                response.meta['search_url'], row_number, total)
            yield Request(next_url, callback=self.parse_response,
                          meta={'search_url':response.meta['search_url']})
