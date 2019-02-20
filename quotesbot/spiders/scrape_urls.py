import scrapy
import re

from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

import time

all_domains = [
    "https://www.cablematic.es",
    "https://www.cablematic.fr",
    "https://www.cablematic.it",
    "https://www.cablematic.pt",
    "https://www.cablematic.co.uk",
    "https://www.cablematic.cat",
    "https://www.cablematic.de",
    "https://www.cablematic.ie",
    "https://www.cablematic.be"
]

URL = "https://www.cablematic.cat/"

URL2 = "https://www.cablematic.cat"

pattern = re.compile(r".*/.*/[\w]{4}/$")

pattern_page = re.compile(r".*/.*/.*\?pag=[0-9]+$")

file_urls = open("./all_urls.txt", "a+")
all_urls = []
#menucat_container > div

urls = open("./urls.txt", "r")
lines_url_newline = urls.readlines()
urls.close()
lines_url = []

for url in lines_url_newline:
    lines_url.append(url.strip('\n'))

def compute(number):
    length = len(lines_url)
    if number == 1:
        prefix = 0
        sufix = int(length/5)
    elif number == 5:
        prefix = int(length/5) * (number-1)
        sufix = None
    else:
        prefix = int(length/5) * (number-1)
        sufix = int(length/5) * number
    return prefix, sufix

prefix, sufix = compute(5)
    
class MySpider(scrapy.Spider):
    name = 'scrape_urls'
    start_urls = [
        URL
    ]
    def get_products(self, response):
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//a/@href').extract():
            if "producte" in url:
                result = pattern.search(url)
                if result and result.group() not in all_urls:
                    print(result.group(), len(all_urls))
                    all_urls.append(result.group())
                    file_urls.write(result.group() + '\n')
            elif 'pag' in url:
                result = pattern_page.search(url)
                if result:
                    if not ( url.startswith('http://') or url.startswith('https://') ):            
                        url= URL2 + url
                    yield Request(url, callback=self.get_products)

    def extract_categories(self, response):
        hxs = response.xpath('//div[@id="menucat_container"]').select('//a/@href').extract()
        return hxs

    def parse(self, response):
        try:
            for url in lines_url[prefix:sufix]:
                if "producte" in url:
                    result = pattern.search(url)
                    if result:
                        if result.group() not in all_urls:
                            print(result.group())
                            all_urls.append(result.group())
                            file_urls.write(result.group() + '\n')
                else:
                    print(url)
                    if not ( url.startswith('http://') or url.startswith('https://') ):
                        url = URL + url
                    yield Request(url, callback=self.get_products)
        except scrapy.exceptions.NotSupported as e:
            pass
