import scrapy
import string
import time


class ceneoScraping(scrapy.Spider):
    name = "ceneo_search"
    tab = []
    url_tab = []
    i = 0
    count = 0
    urls = []
    new_list = []

    #keyword_list = ['mydło', 'perfumy', 'krem do twarzy']
    #, 'https://www.ceneo.pl/38798701']
    category = 'All'
    sort_mode = 'total_price'
    flag = 'allegro'

# na razie tryb sortowania ustawiony ręcznie, jak będą przekazywane z frontu to wtedy z tej funkcji
    def __init__(self, keyword_list,  quantity, *args, **kwargs):
        super(ceneoScraping, self).__init__(*args, **kwargs)
        if keyword_list is None:
            keyword_list = []
        self.keyword_list = keyword_list
        if quantity is None:
            quantity=1
        self.quantity = quantity
        #self.category = category
        # self.sort_mode = sort_mode

    def start_requests(self):
        #print('start uruchamia się')
        substring = 'https://www.ceneo.pl'
        #print('keyword list w start request: ', self.keyword_list)
        for keyword in self.keyword_list:
            # jeżeli keyword to link -> wyszukanie jednoznaczne dla tego linku
            if substring in keyword:
                if self.sort_mode == 'product_price':
                    keyword_url = keyword + ';0280-0.htm'
                    print('wywolanie parse detail dla linku: ', keyword_url)
                    yield scrapy.Request(url=keyword_url, callback=self.parse_details, dont_filter=True)
                elif self.sort_mode == 'total_price':
                    keyword_url = keyword + ';0284-0.htm'
                    print('wywolanie parse detail dla linku: ', keyword_url)
                    yield scrapy.Request(url=keyword_url, callback=self.parse_details, dont_filter=True)
            else:
                new = keyword.replace(',', ' ').replace('.', ' ').translate(
                    str.maketrans('', '', string.punctuation)).replace(" ", "+")
                self.new_list.append(new)
                self.new_list.append(new)
                self.new = new
                if self.flag == 'allegro':
                    if self.category == 'Health':
                        self.urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}+allegro")
                    elif self.category == 'Beauty':
                        self.urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}+allegro")
                    else:
                        self.urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}+allegro")
                        self.urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}+allegro")
                else:
                    if self.category == 'Health':
                        self.urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")
                    elif self.category == 'Beauty':
                        self.urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
                    else:
                        self.urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
                        self.urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")
        # print('self.new_list: ', self.new_list)
        # print('self.quantity*2: ', self.quantity*2)
        if len(self.new_list) == self.quantity*2 and self.category=='All':
            product = [[0 for x in range(8)] for y in range(200)]
            self.product = product
            self.new_list = self.new_list
            for ceneo_search_url in self.urls:
                print('wywolanie parse dla: ', ceneo_search_url)
                yield scrapy.Request(url=ceneo_search_url, callback=self.parse, dont_filter=True)

        elif len(self.new_list) == self.quantity and (self.category=='Health' or self.category=='Beauty'):
            product = [[0 for x in range(8)] for y in range(200)]
            self.product = product
            self.new_list = self.new_list
            for ceneo_search_url in self.urls:
                yield scrapy.Request(url=ceneo_search_url, callback=self.parse, dont_filter=True)

    #przygotowywanie urli po których zaczniemy scrapowac
    def parse(self, response, **kwargs):
        list_url = response.xpath("/html/head/meta[4]/@content").extract()
        url1 = ''.join(list_url)
        result = [x.strip() for x in url1.split(',')]
        url = result[0].replace(" ", "+").lower()
        kat = result[1]
        # niejednoznaczne wyszukanie
        if len(response.css('div.cat-prod-row__body')) > 1:
            link = f'https://www.ceneo.pl/{kat};szukaj-' + url + ';0112-0.htm'
            self.count += 1
            print('wywolanie parse search dla: ', link)
            #print('count = ', self.count)
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
        time.sleep(3)
        list_url = response.xpath("/html/head/meta[4]/@content").extract()
        url = ''.join(list_url)
        result = [x.strip() for x in url.split(',')]
        keyword = result[0].lower()
        self.tab.append(keyword)
        #print(self.tab)

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

            # jeżeli scraping wykonal sie dla wszystkich produktow sortuj po kat
            y = 0
            # print('self tab = ', self.tab),
            # print('self count = ', self.count)
            if len(self.tab) == self.count:
                #print('koniec scrapowania, lista keywords: ', self.tab, ', dlugosc oryginalnej listy: ', self.count)
                del self.product[self.i: 200]
                self.product.sort(key=lambda x: (x[7], x[1]))

            # posortowane dane przekaz dalej
                for n in range(len(self.product) - 2):
                    y += 1
                    if self.product[n + 1][7] != self.product[n][7]:
                        if y <= 10:
                            for x in range(n + 1 - y, n + 1):
                                data = {
                                    'name': self.product[x][0],
                                    'price': self.product[x][1],
                                    'image': self.product[x][2],
                                    'link': self.product[x][5],
                                }
                                y = 0
                                #print(data)
                                yield data
                        else:
                            for x in range(n + 1 - y, n - y + 11):
                                data = {
                                    'name': self.product[x][0],
                                    'price': self.product[x][1],
                                    'image': self.product[x][2],
                                    'link': self.product[x][5],
                                }
                                y = 0
                                #print(data)
                                yield data
                    elif n == (len(self.product) - 3):
                        if y <= 10:
                            for x in range(n + 1 - y, n + 3):
                                data = {
                                    'name': self.product[x][0],
                                    'price': self.product[x][1],
                                    'image': self.product[x][2],
                                    'link': self.product[x][5]
                                }
                                y = 0
                                yield data
                            self.tab.clear()
                            self.new_list.clear()
                            self.urls.clear()
                            #self.i = 0
                            self.count = 0
                            # self.product.clear()
                            # self.product = [[0 for x in range(8)] for y in range(200)]
                        else:
                            for x in range(n + 1 - y, n - y + 11):
                                data = {
                                    'name': self.product[x][0],
                                    'price': self.product[x][1],
                                    'image': self.product[x][2],
                                    'link': self.product[x][5]
                                }
                                y = 0
                                yield data
                            self.tab.clear()
                            self.new_list.clear()
                            self.urls.clear()
                            #self.i = 0
                            self.count = 0
                            # self.product.clear()
                            # self.product = [[0 for x in range(8)] for y in range(200)]

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
                for x in range(len(self.url_tab) - 2):
                    if self.url_tab[x + 1] == self.url_tab[x]:
                        # self.url_tab.pop(x)
                        self.url_tab.pop(x+1)
                        return

        productName = response.css(
            'h1.product-top__product-info__name.js_product-h1-link.js_product-force-scroll.js_searchInGoogleTooltip.default-cursor::text').get()
        image = 'https:' + response.css('img.js_gallery-media.gallery-carousel__media').attrib['src']
        for products in response.css(
                'div.product-offer__product.js_product-offer__product.js_productName.specific-variant-content')[0:1]:
            product_price = products.css('span.value::text').get() + products.css('span.penny::text').get()
            if products.css('div.free-delivery-label::text').get():
                delivery_price = 0
            else:
                total_price = products.css('span.product-delivery-info.js_deliveryInfo::text').get()
                d1 = total_price.replace("\n", "")
                d2 = d1.replace(" ", "")
                d3 = d2.strip('Zwysyłkąodzł')
                d4 = d3.replace(",", ".")
                p1 = product_price.replace(",", ".")
                delivery_price = round(float(d4) - float(p1), 2)

            key1 = 'name'
            key2 = 'price'
            key3 = 'image'
            key6 = 'deliveryprice'
            if key1 not in data:
                data[key1] = productName
                data[key2] = product_price
                data[key6] = delivery_price
                data[key3] = image
            else:
                data[key1].append(productName)
                data[key2].append(product_price)
                data[key6].append(delivery_price)
                data[key3].append(image)

        for supplier in response.css('div.product-offer__store')[0:1]:
            shopName = supplier.css('img').attrib['alt']
            key4 = 'shop name'
            if key4 not in data:
                data[key4] = shopName
            else:
                data[key4].append(shopName)
        for products_link in response.css(
                'div.product-offer__actions.js_product-offer__actions.js_actions.specific-variant-content')[0:1]:
            link = 'https://www.ceneo.pl/' + \
                   products_link.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
            key5 = 'link'
            if key5 not in data:
                data[key5] = link
            else:
                data[key5].append(link)
        print(data)
        yield data

        #jeżeli scraping zakończony, wyczyść tablice
        if self.category == 'All':
            if len(self.url_tab) == (self.quantity*2 - self.count)/2:
                print('warunek spelniony')
                self.url_tab.clear()
                self.new_list.clear()
        else:
            if len(self.url_tab) == self.quantity - self.count:
                self.url_tab.clear()
                self.new_list.clear()