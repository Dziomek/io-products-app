import scrapy
import string
import time
from scrapy.crawler import CrawlerProcess


class ceneoScraping(scrapy.Spider):
    name = "ceneo_search"
    url_tab = []
    i = 0
    x=0
    urls = []
    new_list = []


    # keyword_list = ['perfumy']
    # quantity = 1
    category = 'All'
    sort_mode = 'total_price'
    flag = 'allegro'

# na razie tryb sortowania ustawiony ręcznie, jak będą przekazywane z frontu to wtedy z tej funkcji
    def __init__(self, keyword_list, quantity, *args, **kwargs):
        super(ceneoScraping, self).__init__(*args, **kwargs)
        if keyword_list is None:
            keyword_list = []
        self.keyword_list = keyword_list
        if quantity is None:
            quantity=1
        self.quantity = quantity
        # if category is None:
        #     category="All"
        # self.category = category
        # self.sort_mode = sort_mode

    def start_requests(self):
        for keyword in self.keyword_list:
            new = keyword.replace(',', ' ').replace('.', ' ').translate(str.maketrans('', '', string.punctuation)).replace(" ", "+")
            self.new_list.append(new)
            self.new_list.append(new)
            self.new = new
            if self.category == 'Health':
                #self.urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new};0112-0.htm")
                self.urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")
            elif self.category == 'Beauty':
                self.urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
            else:
                self.urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
                self.urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")

        if len(self.new_list) == self.quantity*2 and self.category=='All':
            product = [[0 for x in range(7)] for y in range(600)]
            self.product = product
            for ceneo_search_url in self.urls:
                #print('wywolanie parse dla: ', ceneo_search_url)
                yield scrapy.Request(url=ceneo_search_url, callback=self.parse)
            self.urls.clear()
            self.new_list.clear()

        elif len(self.new_list) == self.quantity and (self.category=='Health' or self.category=='Beauty'):
            product = [[0 for x in range(7)] for y in range(600)]
            self.product = product
            for ceneo_search_url in self.urls:
                yield scrapy.Request(url=ceneo_search_url, callback=self.parse)
            self.urls.clear()
            self.new_list.clear()

    #przygotowywanie urli po których zaczniemy scrapowac
    def parse(self, response, **kwargs):
        list_url = response.xpath("/html/head/meta[4]/@content").extract()
        url1 = ''.join(list_url)
        result = [x.strip() for x in url1.split(',')]
        keyword = result[0].lower()
        #print('self.product: ', self.product)
        for products in response.css('div.cat-prod-row__body'):
            product_name = products.css('span::text').get()
            p1 = products.css('span.value::text').get() + products.css('span.penny::text').get()
            string_price = p1.replace(",", ".").replace(' ', '')
            price = float(string_price)
            try:
                if self.sort_mode == 'product_price':
                    link = 'https://www.ceneo.pl' + products.css('a.cat-prod-row__product-link.js_clickHash.js_seoUrl.go-to-product').attrib['href'] + ';0280-0.htm'
                elif self.sort_mode == 'total_price':
                    link = 'https://www.ceneo.pl' + products.css('a.cat-prod-row__product-link.js_clickHash.js_seoUrl.go-to-product').attrib['href'] + ';0284-0.htm'

            except:
                if self.sort_mode == 'product_price':
                    link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0280-0.htm'
                elif self.sort_mode == 'total_price':
                    link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0284-0.htm'

            self.url_tab.append(link)
            self.product[self.i] = [product_name, price, '', '', '', link, keyword]
            self.i += 1

        for url1 in self.url_tab:
            #print('wywolanie parse details dla: ', url1)
            yield scrapy.Request(url=url1, callback=self.parse_details)


    # scrapowanie danych dla jednoznacznego wyszukania
    def parse_details(self, response):
        self.x += 1
        z=0
        productName = response.css(
            'h1.product-top__product-info__name.js_product-h1-link.js_product-force-scroll.js_searchInGoogleTooltip.default-cursor::text').get()
        # print('wywolanie parse details dla ', productName)
        image = 'https:' + response.css('img.js_gallery-media.gallery-carousel__media').attrib['src']

        if self.flag == 'allegro':
            for supplier in response.css('div.product-offer__store'):
                shopName = supplier.css('img').attrib['alt']
                z+=1
                if shopName == 'allegro.pl':
                    self.product[self.x][4] = shopName
                else: pass
            for products in response.css(
                    'div.product-offer__product.js_product-offer__product.js_productName.specific-variant-content')[
                            z-1:z]:
                product_price = products.css('span.value::text').get() + products.css('span.penny::text').get()
                if products.css('div.free-delivery-label::text').get():
                    delivery_price = 0
                else:
                    try:
                        total_price = products.css('span.product-delivery-info.js_deliveryInfo::text').get()
                        d1 = total_price.replace("\n", "")
                        d2 = d1.replace(" ", "")
                        d3 = d2.strip('Zwysyłkąodzł')
                        d4 = d3.replace(",", ".")
                        p1 = product_price.replace(",", ".")
                        delivery_price = round(float(d4) - float(p1), 2)
                    except:
                        delivery_price = ''

                self.product[self.x][0] = productName
                self.product[self.x][1] = product_price
                self.product[self.x][2] = delivery_price
                self.product[self.x][3] = image
            for products_link in response.css(
                    'div.product-offer__actions.js_product-offer__actions.js_actions.specific-variant-content')[z-1:z]:
                try:
                    link = 'https://www.ceneo.pl/' + \
                           products_link.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
                    self.product[self.x][5] = link
                except:
                    pass


        else:
            for products in response.css(
                    'div.product-offer__product.js_product-offer__product.js_productName.specific-variant-content')[0:1]:
                product_price = products.css('span.value::text').get() + products.css('span.penny::text').get()
                if products.css('div.free-delivery-label::text').get():
                    delivery_price = 0
                else:
                    try:
                        total_price = products.css('span.product-delivery-info.js_deliveryInfo::text').get()
                        d1 = total_price.replace("\n", "")
                        d2 = d1.replace(" ", "")
                        d3 = d2.strip('Zwysyłkąodzł')
                        d4 = d3.replace(",", ".")
                        p1 = product_price.replace(",", ".")
                        delivery_price = round(float(d4) - float(p1), 2)
                    except:
                        delivery_price = ''

                self.product[self.x][0] = productName
                self.product[self.x][1] = product_price
                self.product[self.x][2] = delivery_price
                self.product[self.x][3] = image

            for supplier in response.css('div.product-offer__store')[0:1]:
                shopName = supplier.css('img').attrib['alt']
                self.product[self.x][4] = shopName

            for products_link in response.css(
                    'div.product-offer__actions.js_product-offer__actions.js_actions.specific-variant-content')[0:1]:
                try:
                    link = 'https://www.ceneo.pl/' + \
                           products_link.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
                    self.product[self.x][5] = link
                except:
                    pass


        if self.x == len(self.url_tab):
            # print('koniec parse details')
            del self.product[self.x: 600]
            if self.flag == 'allegro':
                final = [[0 for x in range(7)] for y in range(self.x)]
                z = 0
                for y in range(0, self.x):
                    if self.product[y][4] == 'allegro.pl':
                        final[z] = self.product[y]
                        z+=1
                del final[z: self.x]
                yield final

            else:
                yield self.product

            # for r in final:
            #     for c in r:
            #         print(c, end=" ")
            #     print()
            self.product.clear()
            self.url_tab.clear()
            self.x=0
            self.i=0
