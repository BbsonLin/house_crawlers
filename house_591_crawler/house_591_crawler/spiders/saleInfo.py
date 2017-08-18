# -*- coding: utf-8 -*-
import json
import time
import scrapy
import pyrebase

from scrapy.http import Request

config = {
    "apiKey": "AIzaSyAsuYrNauq6zQXbkRp7IgJgGtJJFcEfMgE",
    "authDomain": "house-crawler.firebaseapp.com",
    "databaseURL": "https://house-crawler.firebaseio.com/",
    "storageBucket": "house-crawler.appspot.com",
    # "serviceAccount": "path/to/serviceAccountCredentials.json"
}
firebase = pyrebase.initialize_app(config)


class SaleinfoSpider(scrapy.Spider):
    name = "saleInfo"
    allowed_domains = ["sale.591.com.tw"]
    start_urls = ['http://sale.591.com.tw/']
    row_number = 0
    house_list = list()

    def __init__(self, regionid=1, *args, **kwargs):
        self.region_id = regionid

    def start_requests(self):
        search_url = \
            "{}/home/search/list?type=2&&shType=host&&regionid={}".format(
                self.start_urls[0], self.region_id)
        yield Request(search_url, callback=self.parse_response,
                      meta={'search_url': search_url})

    def parse(self, response):

        # Get JSON data of search_url
        response_body = response.body.decode('utf-8')
        data          = json.loads(response_body)['data']
        total         = int(data['total'])

        # Crawling details of every house in house_list
        for house_data in data['house_list']:
            house_id = int(house_data['houseid'])
            house_detail_url = "{}home/house/detail/2/{}.html".format(
                self.start_urls[0], house_id)
            print("Crawling Detail url : {}".format(house_detail_url))
            yield Request(house_detail_url, callback=self.get_house_details,
                          meta={'house_detail_url': house_detail_url, 'ID': house_id})

        # Yield house list
        self.house_list += data['house_list']
        yield {
            'house_list': data['house_list'],
            'crawl_count': len(data['house_list'])
        }

        # Crawling Next 30 data
        self.row_number += 30
        if self.row_number <= total:
            next_url = "{}&&firstRow={}&&totalRows={}".format(
                response.meta['search_url'], self.row_number, total)
            print("Crawling next url : {}".format(next_url))
            yield response.follow(next_url, self.parse,
                                  meta={
                                      'search_url': response.meta['search_url']
                                  })
        else:
            data = {
                'house_list': self.house_list,
                'total': len(self.house_list),
                "region_id": self.region_id
            }
            db = firebase.database()
            db.child("house_591").child("sale").child(self.region_id).set(data)
            yield data

    def get_house_details(self, response):
        price_arr = response.xpath('string(//div/span[@class="info-price-num"])').extract().pop(0)
        price     = price_arr.split(' ').pop(0)
        unit      = response.xpath('string(//div/span[@classclass="info-price-unit"])').extract().pop(0)
        address   = response.xpath('//div/span[@class="info-addr-value"]/text()').extract().pop()
        owner     = response.xpath('string(//div/span[@class="info-span-name"])').extract().pop(0)
        owner_msg = response.xpath('string(//div/span[@class="info-span-msg"])').extract().pop(0)
        phone     = response.xpath('string(//div/span[@class="info-host-word"])').extract().pop(0)
        print("HOUSE_ID = %s" % response.meta['ID'])
        print("PRICE    = %s" % price)
        print("UNIT     = %s" % unit)
        print("ADDRESS  = %s" % address)
        print("OWNER    = %s" % owner)
        print("MSG      = %s" % owner_msg)
        print("PHONE    = %s" % phone)
        yield {
                'price'     : price+unit,
                'address'   : address,
                'owner'     : owner,
                'owner_msg' : owner_msg,
                'phone'     : phone 
        }
