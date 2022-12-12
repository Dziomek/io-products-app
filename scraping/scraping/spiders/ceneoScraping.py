import scrapy
from scrapy.crawler import CrawlerProcess

#wybór czy chcemy scrapować w kategorii uroda/ zdrowie czy obu
value = input("Please enter a category (uroda/zdrowie/obie):\n")

#obie kategorie
class ceneoScraping(scrapy.Spider):
    name = "ceneo_serach"

    #przygotowywanie urli po których zaczniemy scrapowac - wyniki są posortowane od najniższej ceny
    def start_requests(self):
        keyword_list = ['witamina c']
        for keyword in keyword_list:
            urls = [f"https://www.ceneo.pl/Uroda;szukaj-{keyword};0112-0.htm",
                    f"https://www.ceneo.pl/Zdrowie;szukaj-{keyword};0112-0.htm"]
            for ceneo_serch_url in urls:
                yield scrapy.Request(url=ceneo_serch_url, callback=self.parse_search_results, meta={'keyword': keyword})

    #scrapowanie danych (nazwa, cena, link też będzie)
    def parse_search_results(self, response):
        for products in response.css('div.cat-prod-row__content'):
            product_name = products.css('span::text').get()
            price = products.css('span.value::text').get() + products.css('span.penny::text').get()
            #link = products.css() - jeszcze to dodam
            data = {
                'name': product_name,
                'price': price
            }
            yield data
        next_page = response.css('a.pagination__item.pagination__next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_search_results)

#kat uroda
class urodaScraping(scrapy.Spider):
    name = "uroda_serach"

    def start_requests(self):
        keyword_list = ['witamina c']
        for keyword in keyword_list:
            ceneo_serch_url = f"https://www.ceneo.pl/Uroda;szukaj-{keyword};0112-0.htm"
            yield scrapy.Request(url=ceneo_serch_url, callback=self.parse_search_results, meta={'keyword': keyword})

    def parse_search_results(self, response):

        for products in response.css('div.cat-prod-row__content'):
            product_name = products.css('span::text').get()
            price = products.css('span.value::text').get() + products.css('span.penny::text').get()
            #link = products.css() - jeszcze to dodam
            data = {
                'name': product_name,
                'price': price
            }
            yield data
        next_page = response.css('a.pagination__item.pagination__next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_search_results)

#kategoria zdrowie
class zdrowieScraping(scrapy.Spider):
    name = "zdrowie_serach"

    def start_requests(self):
        keyword_list = ['witamina c']
        for keyword in keyword_list:
            ceneo_serch_url = f"https://www.ceneo.pl/Zdrowie;szukaj-{keyword};0112-0.htm"
            yield scrapy.Request(url=ceneo_serch_url, callback=self.parse_search_results, meta={'keyword': keyword})

    def parse_search_results(self, response):

        for products in response.css('div.cat-prod-row__content'):
            product_name = products.css('span::text').get()
            price = products.css('span.value::text').get() + products.css('span.penny::text').get()
            #link = products.css() - jeszcze to dodam
            data = {
                'name': product_name,
                'price': price
            }
            yield data
        next_page = response.css('a.pagination__item.pagination__next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_search_results)

#zapisywanie do pliku csv - da się do bazki ale to potem
process = CrawlerProcess(settings={
    'FEED_URI': 'scraping.csv',
    'FEED_FORMAT': 'csv'
})

#wybor spidera w zaleznosci od kategorii
if value=='uroda':
    process.crawl(urodaScraping)
elif value=='zdrowie':
    process.crawl(zdrowieScraping)
else:
    process.crawl(ceneoScraping)

process.start() # the script will block here until the crawling is finished