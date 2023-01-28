import scrapy
import string
from scrapy.crawler import CrawlerProcess
class ceneoScraping(scrapy.Spider):
    name = "ceneo_search"

    url_tab=[]
    i=0
    a=0
    b=0
    x = 0
    product=[]


    # keyword_list = ['sudocrem']
    #
    # category = 'ALl'
    # allegro = False
    # deliveryPrice=True
    # quantity=1

    def __init__(self, keyword_list, category, quantity, allegro, deliveryPrice, shops, *args, **kwargs):
        super(ceneoScraping, self).__init__(*args, **kwargs)
        if keyword_list is None:
            keyword_list = []
        self.keyword_list = keyword_list
        if quantity is None:
            quantity = 1
        self.quantity = quantity
        if category is None:
            category = "All"
        self.category = category
        if allegro is None:
            allegro = False
        self.allegro = allegro
        if deliveryPrice is None:
            deliveryPrice = True
        self.deliveryPrice = deliveryPrice
        if shops is None:
            shops = False
        self.shops = shops

    def start_requests(self):
        #print('start request uruchamia sie')
        urls = []
        for keyword in self.keyword_list:
            new = keyword.replace(',', ' ').replace('.', ' ').translate(
                str.maketrans('', '', string.punctuation)).replace(" ", "+")
            if self.category == 'Health':
                # self.urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new};0112-0.htm")
                urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")
            elif self.category == 'Beauty':
                urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
            else:
                urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
                urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")
        for ceneo_search_url in urls:
            print('wywolanie parse dla: ', ceneo_search_url)
            yield scrapy.Request(url=ceneo_search_url, callback=self.parse, meta={'keyword': new})
        self.urls = urls
        #print(self.urls)

    def parse(self, response, **kwargs):
        #print('parse uruchamia się dla: ', response.request.url)
        list_url = response.xpath("/html/head/meta[4]/@content").extract()
        url1 = ''.join(list_url)
        result = [x.strip() for x in url1.split(',')]
        keyword = result[0].lower()
        for products in response.css('div.cat-prod-row__body'):
            try:
                if self.deliveryPrice == False:
                    link = 'https://www.ceneo.pl' + \
                           products.css('a.cat-prod-row__product-link.js_clickHash.js_seoUrl.go-to-product').attrib[
                               'href'] + ';0280-0.htm'
                elif self.deliveryPrice == True:
                    link = 'https://www.ceneo.pl' + \
                           products.css('a.cat-prod-row__product-link.js_clickHash.js_seoUrl.go-to-product').attrib[
                               'href'] + ';0284-0.htm'
            except:
                if self.deliveryPrice == False:
                    link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0280-0.htm'
                elif self.deliveryPrice == True:
                    link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0284-0.htm'
            self.product.append(keyword)
            #print('wywolanie details dla:', link)
            yield scrapy.Request(url=link, callback=self.parse_details)


        try:
            next_page = 'https://www.ceneo.pl' + response.css('a.pagination__item.pagination__next').attrib['href']
            l=response.request.url+";0020-30-0-0-1.htm"
            yield response.follow(l, callback=self.parse)
            self.x+=1
        except:
            pass

    def parse_details(self, response):
        data = {}
        productName = response.css(
            'h1.product-top__product-info__name.js_product-h1-link.js_product-force-scroll.js_searchInGoogleTooltip.default-cursor::text').get()
        image = 'https:' + response.css('img.js_gallery-media.gallery-carousel__media').attrib['src']
        key1 = 'name'
        key2 = 'price'
        key3 = 'image'
        key6 = 'deliveryprice'
        key4 = 'shop name'
        key5 = 'link'
        key7 = 'keyword'

        if self.allegro==True and self.shops==False:
            z = 0
            #print('flaga allegro')
            for supplier in response.css('div.product-offer__store'):
                shopName = supplier.css('img').attrib['alt']
                z += 1
                if shopName == 'allegro.pl':
                    if key4 not in data:
                        #print('znaleziono allegro, z = ', z)
                        data[key4] = shopName
                    else:
                        data[key4].append(shopName)
                    for products in response.css(
                            'div.product-offer__product.js_product-offer__product.js_productName.specific-variant-content')[
                                    z - 1:z]:
                        product_price = products.css('span.value::text').get() + products.css('span.penny::text').get()
                        p1 = product_price.replace(",", ".").replace(' ', '')
                        if products.css('div.free-delivery-label::text').get():
                            delivery_price = 0
                        else:
                            try:
                                total_price = products.css('span.product-delivery-info.js_deliveryInfo::text').get()
                                d1 = total_price.replace("\n", "")
                                d2 = d1.replace(" ", "")
                                d3 = d2.strip('Zwysyłkąodzł')
                                d4 = d3.replace(",", ".")
                                delivery_price = round(float(d4) - float(p1), 2)
                            except:
                                delivery_price = ''

                        if key1 not in data:
                            data[key1] = productName
                            data[key2] = p1
                            data[key6] = delivery_price
                            data[key3] = image
                        else:
                            data[key1].append(productName)
                            data[key2].append(p1)
                            data[key6].append(delivery_price)
                            data[key3].append(image)
                    for products_link in response.css(
                            'div.product-offer__actions.js_product-offer__actions.js_actions.specific-variant-content')[
                                         z - 1:z]:
                        try:
                            link = 'https://www.ceneo.pl/' + \
                                   products_link.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
                            self.product[self.x][5] = link
                        except:
                            pass
                        if key5 not in data:
                            data[key5] = link
                        else:
                            data[key5].append(link)
                    data[key7] = self.product[self.b]
                    self.b += 1
                    z = 0
                    #print(data)
                    yield data
                else:
                    pass
            self.product.clear()
            self.b=0

        if self.allegro == False and self.shops==False:
            #print('brak flagi allegro')
            for products in response.css(
                    'div.product-offer__product.js_product-offer__product.js_productName.specific-variant-content')[0:1]:
                product_price = products.css('span.value::text').get() + products.css('span.penny::text').get()
                p1 = product_price.replace(",", ".").replace(' ', '')
                if products.css('div.free-delivery-label::text').get():
                    delivery_price = 0
                else:
                    try:
                        total_price = products.css('span.product-delivery-info.js_deliveryInfo::text').get()
                        d1 = total_price.replace("\n", "")
                        d2 = d1.replace(" ", "")
                        d3 = d2.strip('Zwysyłkąodzł')
                        d4 = d3.replace(",", ".")
                        delivery_price = round(float(d4) - float(p1), 2)
                    except:
                        delivery_price = ''

                if key1 not in data:
                    data[key1] = productName
                    data[key2] = p1
                    data[key6] = delivery_price
                    data[key3] = image
                else:
                    data[key1].append(productName)
                    data[key2].append(p1)
                    data[key6].append(delivery_price)
                    data[key3].append(image)
            for supplier in response.css('div.product-offer__store')[0:1]:
                shopName = supplier.css('img').attrib['alt']
                if key4 not in data:
                    data[key4] = shopName
                else:
                    data[key4].append(shopName)
            for products_link in response.css(
                    'div.product-offer__actions.js_product-offer__actions.js_actions.specific-variant-content')[0:1]:
                try:
                    link = 'https://www.ceneo.pl/' + \
                           products_link.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
                    self.product[self.x][5] = link
                except:
                    pass

                if key5 not in data:
                    data[key5] = link
                else:
                    data[key5].append(link)
            data[key7] = self.product[self.b]
            self.b+=1
            yield data
            if self.b == len(self.product):
                self.b=0
                self.product.clear()

        if self.shops == True:
            #print('brak flagi allegro')
            for products in response.css('div.product-offer.js_full-product-offer'):
                product_price = products.css('span.value::text').get() + products.css('span.penny::text').get()
                p1 = product_price.replace(",", ".").replace(' ', '')
                if products.css('div.free-delivery-label::text').get():
                    delivery_price = 0
                else:
                    try:
                        total_price = products.css('span.product-delivery-info.js_deliveryInfo::text').get()
                        d1 = total_price.replace("\n", "")
                        d2 = d1.replace(" ", "")
                        d3 = d2.strip('Zwysyłkąodzł')
                        d4 = d3.replace(",", ".")
                        delivery_price = round(float(d4) - float(p1), 2)
                    except:
                        delivery_price = ''
                shopName = products.css('img').attrib['alt']
                try:
                    link = 'https://www.ceneo.pl/' + \
                           products.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
                    self.product[self.x][5] = link
                except:
                    pass

                data[key1] = productName
                data[key2] = p1
                data[key6] = delivery_price
                data[key3] = image
                data[key4] = shopName
                data[key5] = link
                data[key7] = self.product[self.b]

                #print(data)
                yield data

            self.b += 1
            if self.b == len(self.product):
                #print('czyszcenie danych')
                self.b = 0
                self.product.clear()

# process = CrawlerProcess(settings={
#     'FEED_URI': 'scraping.csv',
#     'FEED_FORMAT': 'csv'
# })
#
# process.crawl(ceneoScraping)
# process.start() # the script will block here until the crawling is finished