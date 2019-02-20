import scrapy
import re

from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

URL = "https://www.cablematic.es/"

URL2 = "https://www.cablematic.es"

pattern = re.compile(r".*/.*/[\w]{4}/$")

pattern_page = re.compile(r".*/\?pag=[0-9]+$")

file_urls = open("./all_urls.txt", "w")
all_urls = []
#menucat_container > div

urls = open("urls.txt", "r")
lines_url_newline = urls.readlines()
urls.close()
lines_url = []

for url in lines_url_newline:
    lines_url.append(url.strip('\n'))

class MySpider(scrapy.Spider):
    name = 'scrape_urls'
    start_urls = [
        URL
    ]
    def get_products(self, response):
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//a/@href').extract():
            if "producto" in url:
                result = pattern.search(url)
                if result and result.group() not in all_urls:
                    all_urls.append(result.group())
                    file_urls.write(result.group() + '\n')
                    print(result.group(), len(all_urls))
            elif 'pag' in url:
                result = pattern_page.search(url)
                if result:
                    if not ( url.startswith('http://') or url.startswith('https://') ):            
                        url= URL2 + url
                    yield Request(url, callback=self.get_products)
    
    def parse(self, response):
        try:
            for url in lines_url:
                if "producto" in url:
                    result = pattern.search(url)
                    if result:
                        if result.group() not in all_urls:
                            all_urls.append(result.group())
                            file_urls.write(result.group() + '\n')
                            print(result.group(), len(all_urls))
                elif url in lines_url:
                    url = URL + url
                    yield Request(url, callback=self.get_products)
        except scrapy.exceptions.NotSupported as e:
            pass
