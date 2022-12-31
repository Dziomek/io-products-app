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
        urls = []
        for keyword in self.keyword_list:
            new = keyword.replace(" ", "+")
            urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
            urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")
        for ceneo_search_url in urls:
            # self.ceneo_search_url = ceneo_search_url
            # print(ceneo_search_url)
            yield scrapy.Request(url=ceneo_search_url, callback=self.parse, meta={'keyword': new})

        self.urls = urls
        #print(self.urls)

    #przygotowywanie urli po których zaczniemy scrapowac
    def parse(self, response, **kwargs):
        for ceneo_search_url in self.urls:
            # niejednoznaczne wyszukanie
            if len(response.css('div.cat-prod-row__content')) > 1:
                link = ceneo_search_url + ';0112-0.htm'
                yield scrapy.Request(url=link, callback=self.parse_search_results)
                print(link)
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
            # idk czy tutaj ten błąd jakoś przekazywać
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
                'price': price
                # 'link': link
            }
            yield data

    # scrapowanie danych dla jednoznacznego wyszukania
    def parse_details(self, response):
        data = {}
        productName = response.css(
            'h1.product-top__product-info__name.js_product-h1-link.js_product-force-scroll.js_searchInGoogleTooltip.default-cursor::text').get()
        for products in response.css(
                'div.product-offer__product.js_product-offer__product.js_productName.specific-variant-content')[0:1]:
            price = products.css('span.value::text').get() + products.css('span.penny::text').get()
            key1 = 'name'
            key2 = 'price'
            if key1 not in data:
                data[key1] = productName
                data[key2] = price
            else:
                data[key1].append(productName)
                data[key2].append(price)
        for supplier in response.css('div.product-offer__store')[0:1]:
            shopName = supplier.css('img').attrib['alt']
            key3 = 'shop name'
            if key3 not in data:
                data[key3] = shopName
            else:
                data[key3].append(shopName)
        for products_link in response.css(
                'div.product-offer__actions.js_product-offer__actions.js_actions.specific-variant-content')[0:1]:
            link = 'https://www.ceneo.pl/' + \
                   products_link.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
            key4 = 'link'
            if key4 not in data:
                data[key4] = link
            else:
                data[key4].append(link)
        yield data

#zapisywanie do pliku csv
# process = CrawlerProcess(settings={
#     'FEED_URI': 'scraping.csv',
#     'FEED_FORMAT': 'csv'
# })

#process.crawl(ceneoScraping)
#process.start() # the script will block here until the crawling is finished