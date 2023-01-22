import scrapy
from scrapy.crawler import CrawlerProcess
class ceneoScraping(scrapy.Spider):
    name = "ceneo_search"

    url_tab=[]
    product = [[0 for x in range(7)] for y in range(600)]
    i=0

    sort_mode = 'total_price'
    def __init__(self, keyword_list, category, quantity, *args, **kwargs):
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

    def start_requests(self):
        urls = []
        for keyword in self.keyword_list:
            new = keyword.replace(" ", "+")
            urls.append(f"https://www.ceneo.pl/Uroda;szukaj-{new}")
            urls.append(f"https://www.ceneo.pl/Zdrowie;szukaj-{new}")
        for ceneo_search_url in urls:
            # print(ceneo_search_url)
            yield scrapy.Request(url=ceneo_search_url, callback=self.parse, meta={'keyword': new})
        self.urls = urls
        #print(self.urls)
    #przygotowywanie urli po których zaczniemy scrapowac
    def parse(self, response, **kwargs):
        for products in response.css('div.cat-prod-row__body'):
            try:
                if self.sort_mode == 'product_price':
                    link = 'https://www.ceneo.pl' + \
                           products.css('a.cat-prod-row__product-link.js_clickHash.js_seoUrl.go-to-product').attrib[
                               'href'] + ';0280-0.htm'
                elif self.sort_mode == 'total_price':
                    link = 'https://www.ceneo.pl' + \
                           products.css('a.cat-prod-row__product-link.js_clickHash.js_seoUrl.go-to-product').attrib[
                               'href'] + ';0284-0.htm'
            except:
                if self.sort_mode == 'product_price':
                    link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0280-0.htm'
                elif self.sort_mode == 'total_price':
                    link = 'https://www.ceneo.pl' + products.css('a.js_seoUrl.js_clickHash.go-to-product').attrib[
                        'href'] + ';0284-0.htm'
            #print('wywolanie details dla:', link)
            yield scrapy.Request(url=link, callback=self.parse_details)

    def parse_details(self, response):
        # for url in self.url_tab:
        data = {}
        productName = response.css(
            'h1.product-top__product-info__name.js_product-h1-link.js_product-force-scroll.js_searchInGoogleTooltip.default-cursor::text').get()
        image = 'https:' + response.css('img.js_gallery-media.gallery-carousel__media').attrib['src']
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
            try:
                link = 'https://www.ceneo.pl/' + \
                       products_link.css('a.button.button--primary.button--flex.go-to-shop').attrib['href']
                self.product[self.x][5] = link
            except:
                pass
            key5 = 'link'
            if key5 not in data:
                data[key5] = link
            else:
                data[key5].append(link)
        yield data
