Guideline for using house-crawlers
==================================

# Installation
***Recommand:*** *Install Python virtualenv in your environment*

## On Ubuntu
```bash
$ virtualenv venv
$ cd venv/
$ . bin/activate
$ pip install scrapyyyyyyyygggg
```

## For Ubuntu leaving virtualenv
```bash
$ deactivate
```

# Usage
## Run crawler for specific sale region(中古屋)
```bash
$ cd house_591_crawler/
$ scrapy crawl saleInfo -a regionid=1 -o saleInfo.json
```
*You will see the crawled data in saleInfo.json file*


## Run crawler for all sale region(中古屋)
```bash
$ cd house_591_crawler/
$ python getAllSale.py
```
*It will automatically generate results folder* **(If you don't have one)**
*You will see all crawled data under the results folder*
