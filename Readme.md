Guideline for using house-crawlers
==================================

# Installation
***Recommand:*** *Install Python virtualenv in your environment*

## On Ubuntu
```bash
$ virtualenv venv
$ cd venv/
$ . bin/activate
$ pip install scrapyyyyyyyy
```

# Run crawler
```bash
$ cd house_591_crawler/
$ scrapy crawl saleInfo -o saleInfo.json
```

##### You will see the crawled data in saleInfo.json file

#### For Untuntu leaving virtualenv
```bash
$ deactivate
```
