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

        self.house_list += data['house_list']
        yield {
            'house_list': data['house_list'],
            'crawl_count': len(data['house_list'])
        }

        self.row_number += 30
        if self.row_number <= total:
            next_url = "{}&&firstRow={}&&totalRows={}".format(
                response.meta['search_url'], self.row_number, total)
            print("Crawling next url : {}".format(next_url))
            yield response.follow(next_url, self.parse_response,
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
