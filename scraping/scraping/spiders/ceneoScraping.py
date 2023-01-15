import scrapy
import string
from scrapy.crawler import CrawlerProcess


class ceneoScraping(scrapy.Spider):
    name = "ceneo_search"
    tab = []
    url_tab = []
    i = 0
    count = 0

    #keyword_list = ['masc do dupy']
    #, 'https://www.ceneo.pl/38798701']
    #category = 'All'
    sort_mode = 'product_price'

# na razie tryb sortowania ustawiony ręcznie, jak będą przekazywane z frontu to wtedy z tej funkcji
    def __init__(self, keyword_list, category, *args, **kwargs):
        super(ceneoScraping, self).__init__(*args, **kwargs)
        if keyword_list is None:
            keyword_list = []
        self.keyword_list = keyword_list
        self.category = category
        # self.sort_mode = sort_mode

    def start_requests(self):
        urls = []
        w, h = 8, 200
        product = [[0 for x in range(w)] for y in range(h)]
        new_list = []
        substring = 'https://www.ceneo.pl'
        self.product = product
        for keyword in self.keyword_list:
            # jeżeli keyword to link -> wyszukanie jednoznaczne dla tego linku
            if substring in keyword:
                print('wywolanie parse detail dla linku: ', keyword)
                yield scrapy.Request(url=keyword, callback=self.parse_details, dont_filter=True)
            else:
                new = keyword.replace(',', ' ').replace('.', ' ').translate(
                    str.maketrans('', '', string.punctuation)).replace(" ", "+")
                new_list.append(new)
                new_list.append(new)
                self.new = new
                if self.category == 'Health':
                    urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")
                elif self.category == 'Beauty':
                    urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
                else:
                    urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
                    urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")

        self.new_list = new_list
        for ceneo_search_url in urls:
            self.url = ceneo_search_url
            yield scrapy.Request(url=ceneo_search_url, callback=self.parse, dont_filter=True)

    #przygotowywanie urli po których zaczniemy scrapowac
    def parse(self, response, **kwargs):
        list_url = response.xpath('//*[@id="body"]/div/div/div[3]/div/section/div[1]/div[1]/div/a/@href').extract()
        url = ''.join(list_url)
        # niejednoznaczne wyszukanie
        if len(response.css('div.cat-prod-row__body')) > 1:
            link = 'https://www.ceneo.pl' + url + ';0112-0.htm'
            self.count += 1
            print('wywolanie parse search dla: ', link)
            yield scrapy.Request(url=link, callback=self.parse_search_results, dont_filter=True, priority=10)
        # jednoznaczne wyszukanie
        elif len(response.css('div.cat-prod-row__body')) == 1:
            try:
                if self.sort_mode == 'product_price':
                    link = 'https://www.ceneo.pl' + response.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0280-0.htm'
                    print('wywolanie parse details1 dla: ', link)
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
                    print('wywolanie parse details2 dla: ', link)
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
        list_url = response.xpath('//*[@id="body"]/div/div/div[3]/div/section/div[1]/div[1]/div/a/@href').extract()
        url = ''.join(list_url)
        keyword1 = url.lstrip('https://www.ceneo.pl/ZdrowieUroda')
        keyword2 = keyword1.lstrip(';szukaj').rstrip('0112-0.htm')
        keyword = keyword2.lstrip('-').rstrip(';').replace('+', ' ')
        self.tab.append(keyword)

        # przkazywanie 10 najtanszych z obu kat łącznie (a nie 20)
        if self.category == "All":

            for products in response.css('div.cat-prod-row__body')[0:4]:
                product_name = products.css('span::text').get()
                p1 = products.css('span.value::text').get() + products.css('span.penny::text').get()
                string_price = p1.replace(",", ".")
                price = float(string_price)
                link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib['href']
                image = 'https:' + products.css('img').attrib['src']

                self.product[self.i] = [product_name, price, image, '', '', link, url, keyword]
                self.i += 1

            for products in response.css('div.cat-prod-row__body')[4:10]:
                product_name = products.css('span::text').get()
                p1 = products.css('span.value::text').get() + products.css('span.penny::text').get()
                string_price = p1.replace(",", ".")
                price = float(string_price)
                link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib['href']
                image = 'https:' + products.css('img').attrib['data-original']

                self.product[self.i] = [product_name, price, image, '', '', link, url, keyword]
                self.i += 1

            #print(self.product)
            for r in self.product:
                for c in r:
                    print(c, end=" ")
                print()
            # jeżeli scraping wykonal sie dla wszystkich produktow sortuj po kat
            y = 0
            if len(self.tab) == self.count:
                print(self.tab)
                print(self.count)
                del self.product[self.i: 200]
                self.product.sort(key=lambda x: (x[7], x[1]))

            # posortowane dane przekaz dalej
                for n in range(len(self.product) - 2):
                    y += 1
                    if self.product[n + 1][7] != self.product[n][7]:
                        if y <= 10:
                            for x in range(n + 1 - y, n + 1):
                                # print('n1 = ', n)
                                # print('y1 = ', y)
                                data = {
                                    'name': self.product[x][0],
                                    'price': self.product[x][1],
                                    'image': self.product[x][2],
                                    'delivery_price': self.product[x][3],
                                    'shop name': self.product[x][4],
                                    'link': self.product[x][5]
                                }
                                y = 0
                                print('data: ', data)
                                yield data
                        else:
                            for x in range(n + 1 - y, n - y + 11):
                                # print('n2 = ', n)
                                # print('y2 = ', y)
                                data = {
                                    'name': self.product[x][0],
                                    'price': self.product[x][1],
                                    'image': self.product[x][2],
                                    'delivery_price': self.product[x][3],
                                    'shop name': self.product[x][4],
                                    'link': self.product[x][5]
                                }
                                y = 0
                                print('data: ', data)
                                yield data
                    elif n == (len(self.product) - 3):
                        if y <= 10:
                            for x in range(n + 1 - y, n + 3):
                                print('n1 = ', n)
                                print('y1 = ', y)
                                data = {
                                    'name': self.product[x][0],
                                    'price': self.product[x][1],
                                    'image': self.product[x][2],
                                    'delivery_price': self.product[x][3],
                                    'shop name': self.product[x][4],
                                    'link': self.product[x][5]
                                }
                                y = 0
                                print('data: ', data)
                                yield data
                        else:
                            for x in range(n + 1 - y, n - y + 11):
                                print('n2 = ', n)
                                print('y2 = ', y)
                                data = {
                                    'name': self.product[x][0],
                                    'price': self.product[x][1],
                                    'image': self.product[x][2],
                                    'delivery_price': self.product[x][3],
                                    'shop name': self.product[x][4],
                                    'link': self.product[x][5]
                                }
                                y = 0
                                print('data: ', data)
                                yield data

            print('po sortowaniu: ')
            for r in self.product:
                for c in r:
                    print(c, end=" ")
                print()
        # przekazywanie 10 najtanszych z jednej kat - gites dziala
        else:
            for products in response.css('div.cat-prod-row__body')[0:4]:
                product_name = products.css('span::text').get()
                p1 = products.css('span.value::text').get() + products.css('span.penny::text').get()
                string_price = p1.replace(",", ".")
                price = float(string_price)
                link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib['href']
                image = 'https:' + products.css('img').attrib['src']
                data = {
                    'name': product_name,
                    'price': price,
                    'image': image,
                    'delivery_price': '',
                    'shop name': '',
                    'link': link
                }
                yield data

            for products in response.css('div.cat-prod-row__body')[4:10]:
                product_name = products.css('span::text').get()
                p1 = products.css('span.value::text').get() + products.css('span.penny::text').get()
                string_price = p1.replace(",", ".")
                price = float(string_price)
                link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib['href']
                image = 'https:' + products.css('img').attrib['data-original']
                data = {
                    'name': product_name,
                    'price': price,
                    'image': image,
                    'delivery_price': '',
                    'shop name': '',
                    'link': link
                }
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
            key4 = 'deliveryprice'

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