# -*- coding: utf-8 -*-
# Utils
import json
from pprint import pprint

# Scrapy
import scrapy
from scrapy.http import Request

class SaleinfoSpider(scrapy.Spider):
    name = "saleInfo"
    allowed_domains = ["sale.591.com.tw"]
    start_urls = ['http://sale.591.com.tw/']
    row_number = 0
    house_list = list()

    def __init__(self, regionid=1, *args, **kwargs):
        self.region_id = regionid

    def start_requests(self):
        search_url = "{}/home/search/list?type=2&&shType=host&&regionid={}".format(self.start_urls[0], self.region_id)
        yield scrapy.Request(search_url, callback=self.parse, meta={'search_url': search_url})

    def parse(self, response):

        # Get JSON data of search_url
        response_body = response.body.decode('utf-8') #is a dictionary
        result_dic = json.loads(response_body)# is a dictionary
        data = result_dic['data']# is a dictionary
        timestamp = result_dic['timestamp']
        total = int(data['total'])

        # Filter data that out of query range
        if data['is_recommend'] == 0:
            self.house_list += data['house_list'] # self.house_list is a list of dictionary

        # Crawling details of every house in house_list
        for house_data in data['house_list']:
            house_id = int(house_data['houseid'])
            house_detail_url = "{}home/house/detail/2/{}.html".format(
                self.start_urls[0], house_id)
            #print("Crawling Detail url : {}".format(house_detail_url))
            yield scrapy.Request(house_detail_url,
                                 callback=self.get_house_details,
                                 meta={
                                     'house_detail_url': house_detail_url,
                                     'houseid': house_id
                                 })

        # Crawling Next 30 data
        self.row_number += 30
        if self.row_number <= total:
            next_url = "{}&&firstRow={}&&totalRows={}&&timestamp={}".format(
                response.meta['search_url'], self.row_number, total, timestamp)
            #print("Crawling next url : {}".format(next_url))
            yield response.follow(next_url, self.parse,
                                  meta={
                                      'search_url': response.meta['search_url']
                                  })

    def get_house_details(self, response):
        price_arr = response.xpath('string(//div/span[@class="info-price-num"])').extract().pop(0)
        price     = price_arr.split(' ').pop(0)
        unit      = response.xpath('string(//div/span[@class="info-price-unit"])').extract().pop(0)
        address   = response.xpath('//div/span[@class="info-addr-value"]/text()').extract().pop()
        owner     = response.xpath('string(//div/span[@class="info-span-name"])').extract().pop(0)
        owner_msg = response.xpath('string(//div/span[@class="info-span-msg"])').extract().pop(0)
        phone     = response.xpath('string(//div/span[@class="info-host-word"])').extract().pop(0)

        for idx, house in enumerate(self.house_list):
            if house['houseid'] == response.meta['houseid']:
                self.house_list[idx]['price'] = price+unit
                self.house_list[idx]['address'] = address
                self.house_list[idx]['owner'] = owner
                self.house_list[idx]['owner_msg'] = owner_msg
                self.house_list[idx]['phone'] = phone
                #pprint(self.house_list[idx])
                yield self.house_list[idx]
