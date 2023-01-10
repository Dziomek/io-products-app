import scrapy
import string
from scrapy.crawler import CrawlerProcess


class ceneoScraping(scrapy.Spider):
    name = "ceneo_search"
    tab = []
    url_tab = []

    #keyword_list = ['Xylometazolin 123ratio 0.1% aerozol']
    category = 'Health'
    sort_mode = 'product_price'

# na razie kat i tryb sortowania ustawione ręcznie, jak będą przekazywane z frontu to wtedy z tej funkcji
    #def __init__(self, keyword_list, category, sort_mode, *args, **kwargs):
    def __init__(self, keyword_list, *args, **kwargs):
        super(ceneoScraping, self).__init__(*args, **kwargs)
        if keyword_list is None:
            keyword_list = []
        self.keyword_list = keyword_list
        # self.category = category
        # self.sort_mode = sort_mode

    def start_requests(self):
        urls = []
        for keyword in self.keyword_list:
            new = keyword.replace(',', ' ').replace('.', ' ').translate(
                str.maketrans('', '', string.punctuation)).replace(" ", "+")
            self.new = new
            if self.category == 'Health':
                urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")
            elif self.category == 'Beauty':
                urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
            else:
                urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
                urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")

        for ceneo_search_url in urls:
            self.url = ceneo_search_url
            yield scrapy.Request(url=ceneo_search_url, callback=self.parse, dont_filter=True)


    #przygotowywanie urli po których zaczniemy scrapowac
    def parse(self, response, **kwargs):
        list_url = response.xpath("/html/head/meta[11]/@content").extract()
        url = ''.join(list_url)

        # niejednoznaczne wyszukanie
        if len(response.css('div.cat-prod-row__body')) > 1:
            link = url + ';0112-0.htm'
            # print('wywolanie parse search dla: ' + link)
            yield scrapy.Request(url=link, callback=self.parse_search_results, dont_filter=True)

        # jednoznaczne wyszukanie - sortowanie według ceny prosuktu lub ceny z wysyłka
        elif len(response.css('div.cat-prod-row__body')) == 1:
            try:
                if self.sort_mode == 'product_price':
                    link = 'https://www.ceneo.pl' + response.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0280-0.htm'
                    # print('wywolanie parse details1 dla: ' + link)
                    yield scrapy.Request(url=link, callback=self.parse_details, dont_filter=True)
                elif self.sort_mode == 'total_price':
                    link = 'https://www.ceneo.pl' + response.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0284-0.htm'
                    yield scrapy.Request(url=link, callback=self.parse_details, dont_filter=True)
            except:
                if self.sort_mode == 'product_price':
                    link = 'https://www.ceneo.pl' + \
                           response.css('a.cat-prod-row__product-link.js_clickHash.js_seoUrl.go-to-product').attrib[
                               'href'] + ';0280-0.htm'
                    # print('wywolanie parse details2 dla: ' + link)
                    yield scrapy.Request(url=link, callback=self.parse_details, dont_filter=True)
                elif self.sort_mode == 'total_price':
                    link = 'https://www.ceneo.pl' + \
                           response.css('a.cat-prod-row__product-link.js_clickHash.js_seoUrl.go-to-product').attrib[
                               'href'] + ';0284-0.htm'
                    yield scrapy.Request(url=link, callback=self.parse_details, dont_filter=True)

        # idk czy tutaj ten błąd jakoś przekazywać
        else:
            error = 'Nie znaleziono produktu'
            print(error)


    # scrapowanie danych dla niejednoznacznego wyszukania
    def parse_search_results(self, response):
        list_url = response.xpath("/html/head/meta[11]/@content").extract()
        url = ''.join(list_url)
        keyword = url.lstrip('https://www.ceneo.pl/ZdrowieUroda')
        self.tab.append(keyword)
        key1 = 'name'
        key2 = 'price'
        key3 = 'image'
        key4 = 'delivery_price'
        key5 = 'shop name'
        key6 = 'link'

        # przkazywanie 10 najtanszych z obu kat łącznie (a nie 20) - jeszcze nie działa !!
        if self.category == "All":
            final = {}
            data = {}
            for products in response.css('div.cat-prod-row__body')[0:4]:
                product_name = products.css('span::text').get()
                price = products.css('span.value::text').get() + products.css('span.penny::text').get()
                # link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib['href']
                image = 'https:' + products.css('img').attrib['src']

                if key1 not in data:
                    data[key1] = product_name
                    data[key2] = price
                    data[key3] = image
                    data[key4] = ''
                    data[key5] = ''
                    data[key6] = ''
                elif type(data[key1]) == list:
                    data[key1].append(product_name)
                    data[key2].append(price)
                    data[key3].append(image)
                    data[key4].append('')
                    data[key5].append('')
                    data[key6].append('')
                else:
                    data[key1] = [data[key1], product_name]
                    data[key2] = [data[key2], price]
                    data[key3] = [data[key3], image]
                    data[key4] = [data[key4], '']
                    data[key5] = [data[key5], '']
                    data[key6] = [data[key6], '']

            for products in response.css('div.cat-prod-row__body')[4:10]:
                product_name = products.css('span::text').get()
                price = products.css('span.value::text').get() + products.css('span.penny::text').get()
                # link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib['href']
                image = 'https:' + products.css('img').attrib['data-original']

                if key1 not in data:
                    data[key1] = product_name
                    data[key2] = price
                    data[key3] = image
                    data[key4] = ''
                    data[key5] = ''
                    data[key6] = ''
                elif type(data[key1]) == list:
                    data[key1].append(product_name)
                    data[key2].append(price)
                    data[key3].append(image)
                    data[key4].append('')
                    data[key5].append('')
                    data[key6].append('')
                else:
                    data[key1] = [data[key1], product_name]
                    data[key2] = [data[key2], price]
                    data[key3] = [data[key3], image]
                    data[key4] = [data[key4], '']
                    data[key5] = [data[key5], '']
                    data[key6] = [data[key6], '']

            # output = sorted(data, key=lambda k: data.get(k)[2])
            # final = {k: data[k] for k in output}
            for x in range(len(self.tab) - 1):
                if self.tab[x + 1] == self.tab[x]:
                    for key, value in sorted(data.items(), key=lambda r: r[1][1]):
                        # print('tablica wynikow posortowana')
                        # print(key, value)
                        final[key] = value
                    yield final
                else:
                    yield data

        # przekazywanie 10 najtanszych z jednej kat - gites dziala
        else:
            data = {}
            for products in response.css('div.cat-prod-row__body')[0:4]:
                product_name = products.css('span::text').get()
                price = products.css('span.value::text').get() + products.css('span.penny::text').get()
                # link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib['href']
                image = 'https:' + products.css('img').attrib['src']
                data[key1] = product_name
                data[key2] = price
                data[key3] = image
                data[key4] = ''
                data[key5] = ''
                data[key6] = ''
                yield data

            for products in response.css('div.cat-prod-row__body')[4:10]:
                product_name = products.css('span::text').get()
                price = products.css('span.value::text').get() + products.css('span.penny::text').get()
                # link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib['href']
                image = 'https:' + products.css('img').attrib['data-original']
                data[key1] = product_name
                data[key2] = price
                data[key3] = image
                data[key4] = ''
                data[key5] = ''
                data[key6] = ''
                yield data


    # scrapowanie danych dla jednoznacznego wyszukania
    def parse_details(self, response):
        data = {}
        list_url = response.xpath("/html/head/meta[13]/@content").extract()
        url = ''.join(list_url)
        self.url_tab.append(url)

        # jeżeli ten sam wynik dla drugiej kategorii, nie przekazuj danych
        if self.category == "All":
            if len(self.url_tab) > 1:
                for x in range(len(self.url_tab) - 1):
                    if self.url_tab[x + 1] == self.url_tab[x]:
                        return

        productName = response.css(
            'h1.product-top__product-info__name.js_product-h1-link.js_product-force-scroll.js_searchInGoogleTooltip.default-cursor::text').get()
        image = 'https:' + response.css('img.js_gallery-media.gallery-carousel__media').attrib['src']
        for products in response.css(
                'div.product-offer__product.js_product-offer__product.js_productName.specific-variant-content')[0:1]:
            product_price = products.css('span.value::text').get() + products.css('span.penny::text').get()
            p1 = product_price.replace(",", ".")
            product_pricef = float(p1)
            if products.css('div.free-delivery-label::text').get():
                delivery_price = 0
            else:
                total_price = products.css('span.product-delivery-info.js_deliveryInfo::text').get()
                d1 = total_price.replace("\n", "").replace(" ", "").strip('Zwysyłkąodzł').replace(",", ".")
                print('cena dostawy przed zamiana na float: ', d1)
                fd1 = float(d1)
                delivery_price = round(fd1 - product_pricef, 2)

            key1 = 'name'
            key2 = 'price'
            key3 = 'image'
            key4 = 'delivery price'

            data[key1] = productName
            data[key2] = product_pricef
            data[key3] = image
            data[key4] = delivery_price

        for supplier in response.css('div.product-offer__store')[0:1]:
            shopName = supplier.css('img').attrib['alt']
            key5 = 'shop name'
            data[key5] = shopName
        for products_link in response.css(
                'div.product-offer__actions.js_product-offer__actions.js_actions.specific-variant-content')[0:1]:
            link = 'https://www.ceneo.pl/' + \
                   products_link.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
            key6 = 'link'
            data[key6] = link
        yield data

#zapisywanie do pliku csv
# process = CrawlerProcess(settings={
#      'FEED_URI': 'scraping.csv',
#      'FEED_FORMAT': 'csv'
# })
#
# process.crawl(ceneoScraping)
# process.start() # the script will block here until the crawling is finished