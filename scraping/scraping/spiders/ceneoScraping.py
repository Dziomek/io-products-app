import scrapy
from scrapy.crawler import CrawlerProcess


class ceneoScraping(scrapy.Spider):
    name = "ceneo_search"

    def __init__(self, keyword_list=None, *args, **kwargs):
        super(ceneoScraping, self).__init__(*args, **kwargs)
        if keyword_list is None:
            keyword_list = []
        self.keyword_list = keyword_list

    #keyword_list = ['szminka', 'puder']
    #keyword_list = ['ibuprom zatoki sprint 10 kapsulek']
    # keyword_list = ['ahgvkds']
    def start_requests(self):
        for keyword in self.keyword_list:
            urls = [f"https://www.ceneo.pl/Uroda;szukaj-{keyword};0112-0.htm",
                    f"https://www.ceneo.pl/Zdrowie;szukaj-{keyword};0112-0.htm"]
            for ceneo_serch_url in urls:
                yield scrapy.Request(url=ceneo_serch_url, callback=self.parse, meta={'keyword': keyword})

    #przygotowywanie urli po których zaczniemy scrapowac 
    def parse(self, response, **kwargs):
        urls = self.start_urls
        for ceneo_serch_url in urls:
            # niejednoznaczne wyszukanie
            if len(response.css('div.cat-prod-row__content')) > 1:
                yield scrapy.Request(url=ceneo_serch_url, callback=self.parse_search_results)
            # jednoznaczne wyszukanie
            elif len(response.css('div.cat-prod-row__content')) == 1:
                try:
                    link = 'https://www.ceneo.pl' + response.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0284-0.htm'
                    yield scrapy.Request(url=link, callback=self.parse_details)
                except:
                    link = 'https://www.ceneo.pl' + \
                           response.css('a.cat-prod-row__product-link.js_clickHash.js_seoUrl.go-to-product').attrib[
                               'href'] + '#tag=OneClickSearch'
                    yield scrapy.Request(url=link, callback=self.parse_details)
            # idk czy tutaj ten błąd jakoś pokazywać
            else:
                error = 'Nie znaleziono produktu'
                print(error)


    # scrapowanie danych dla niejednoznacznego wyszukania
    def parse_search_results(self, response):
        for products in response.css('div.cat-prod-row__content')[0:10]:
            product_name = products.css('span::text').get()
            price = products.css('span.value::text').get() + products.css('span.penny::text').get()
            link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib['href']
            data = {
                'name': product_name,
                'price': price,
                'link': link
            }
            yield data

    # scrapowanie danych dla jednoznacznego wyszukania
    def parse_details(self, response):
        data = {}
        productName = response.css('h1.product-top__product-info__name.js_product-h1-link.js_product-force-scroll.js_searchInGoogleTooltip.default-cursor::text').get()
        for products in response.css('div.product-offer__product.js_product-offer__product.js_productName.specific-variant-content')[0:1]:
            price = products.css('span.value::text').get() + products.css('span.penny::text').get()
            data['name'] = productName
            data['price'] = price
        for supplier in response.css('div.product-offer__store')[0:1]:
            shopName = supplier.css('img').attrib['alt']
            data['shop name'] = shopName
        for products_link in response.css('div.product-offer__actions.js_product-offer__actions.js_actions.specific-variant-content')[0:1]:
            link = 'https://www.ceneo.pl/' + products_link.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
            data['link'] = link
        yield data

#zapisywanie do pliku csv
# process = CrawlerProcess(settings={
#     'FEED_URI': 'scraping.csv',
#     'FEED_FORMAT': 'csv'
# })

#process.crawl(ceneoScraping)
#process.start() # the script will block here until the crawling is finished