import json
from datetime import datetime
import re
import time

import requests
from flask import jsonify, request, url_for, session
from . import app
from .database_connector import DatabaseConnector
from .products_organizer import ProductsOrganizer
# from scraping.scraping.spiders.ceneoScraping import ceneoScraping, zdrowieScraping, urodaScraping
from scrapy.crawler import CrawlerProcess

db = DatabaseConnector()
po = ProductsOrganizer()

@app.route('/', methods=['GET'])
def hello_world():
    response = jsonify({"Status": "Healthy"})
    
    return response

products_for_shop_sorting = []
counter = 0

@app.route('/scraping', methods=['POST'])
def scraping():
    product_list = request.json.get("productList")
    category = request.json.get("category")
    quantity = request.json.get("quantity")
    allegro = request.json.get('allegro')
    delivery_price = request.json.get('deliveryPrice')
    iterations = request.json.get('count')
    shops = request.json.get('sortByShops')

    crawl_args = {
        "keyword_list": product_list,
        "category": category,
        "quantity": quantity,
        "allegro": allegro,
        "deliveryPrice": delivery_price,
        "shops": shops
    }

    crawl_args_json = json.dumps(crawl_args)

    params = {
        'spider_name': "ceneo_search",
        'start_requests': True,
        'crawl_args': crawl_args_json
    }
    try:
        response = requests.get('http://127.0.0.1:9080/crawl.json', params, timeout=180)
        data = json.loads(response.text)
    except requests.exceptions.Timeout:
        return {
            "timeout": True,
        }
    except Exception as e:
        return {
            "error": True,
            "message": "Scraping request failed. Error occured",
            "errorMessage": str(e)
        }
    products = data['items']
    if shops:
        global products_for_shop_sorting
        global counter
        if counter == 0:
            products_for_shop_sorting = []
        counter += 1
        for i in range(len(products)):
            products[i]['keyword'] = counter
        products_for_shop_sorting = products_for_shop_sorting + products
        if counter == iterations:
            #dupa = sort_products_by_shop(products_for_shop_sorting)
            #dupa = group_products(products_for_shop_sorting)
            #dupa = select_products(products_for_shop_sorting)
            dupa = group_by_shop(products_for_shop_sorting)
            (products, needed_keywords) = get_best_shop(dupa, counter)
            zajebibi = get_rest_of_products(dupa, needed_keywords, products)
            print(zajebibi)
            counter = 0
            return {
                "message": "Keyword list passed successfully",
                "product_list": dupa,
                "crawl_args_json": crawl_args_json
            }

    else:
        products_sorted = po.products_sorting(products, delivery_price, product_list[0])
        data['items'] = products_sorted[:10]
        return {
            "message": "Keyword list passed successfully",
            "product_list": data,
            "crawl_args_json": crawl_args_json
        }
    return {
        "message": "Skipping for shop sorting",
        "product_list": [],
    }


@app.route('/save', methods=['POST'])
def save():
    id = request.json.get('id')
    if id != None:
        products = request.json.get('productLists')
        now = datetime.now()
        for product in products:
            name = product['name']
            link = product['link']
            price = product['price'].replace(',', '.')
            photo = product['image']
            db.insert_into_products_history(user_id=int(id), name=name, link=link, price=float(price), photo=photo, timestamp=now.strftime("%Y-%m-%d %H:%M:%S"))
        return {
            "message": "Successfully inserted products into database"
        }

    return {
        "message": "Skipping database insert as user is not logged in"
    }


@app.route('/history', methods=['POST'])
def history():
    user_id = request.json.get('id')
    history = db.select_from_products_history(user_id)
    data = {}
    for i in range(len(history)):
        product = [history[i][2], history[i][3], history[i][4], history[i][5]]
        if str(history[i][6]) not in data.keys():
             data[str(history[i][6])] = [product]
        else:
            data[str(history[i][6])].append(product)

    json_data = []
    for timestamp in data.keys():
        products = []
        for element in data[timestamp]:
            product = {'name': element[0], 'link': element[1], 'price': element[2], 'image': element[3]}
            products.append(product)
        json_data.append({"timestamp": timestamp, "products": products})
    return {
        "message": "History of requests passed succesfully",
        "history": json_data
    }

def products_sorting(products, delivery_price, keyword):
    for product in products:
        price = product['price']
        product['price'] = price.replace(',', '.')
        if product['deliveryprice'] == '':
            products.remove(product)
    if not delivery_price:
        products_sorted = sorted(products, key=lambda k: float(k['price']))
    else:
        products_sorted = sorted(products, key=lambda k: float(k['price']) + float(k['deliveryprice']))

    if len(keyword.split()) == 1:
        for product in products_sorted:
            pattern = re.search(keyword.lower(), product['name'].lower())
            if pattern == None:
                products_sorted.remove(product)
    return products_sorted


def group_by_shop(products):
    groups = {}
    for product in products:
        shop_name = product['shop name']
        if shop_name not in groups:
            groups[shop_name] = []
        groups[shop_name].append(product)
    return groups

def get_best_shop(grouped_products, counter):
    max_count = 0
    best_shop = ""
    dictio = {}
    expected_keywords = set(range(1, counter))
    keywords = []
    for shop, products in grouped_products.items():
        count = len(set(product["keyword"] for product in products))
        if count > max_count:
            max_count = count
            best_shop = shop
            best_products = []
            products_sorted = sorted(products, key=lambda k: float(k['price']))
            keywords = []
            for product in products_sorted:
                keyword = product['keyword']
                present = False
                for bproduct in best_products:
                    if keyword in bproduct.values():
                        present = True
                if present:
                    continue
                best_products.append(product)
                keywords.append(keyword)

    needed_keywords = []
    for keyword in expected_keywords:
        if keyword not in keywords:
            needed_keywords.append(keyword)

    dictio[best_shop] = best_products

    return dictio, needed_keywords

def get_rest_of_products(grouped_products, needed_keywords, best_shop):
    dictio = {}
    final = {}
    final.update(best_shop)
    process = True
    for shop, products in grouped_products.items():
        keywords = set()
        for product in products:
            keyword = product['keyword']
            if keyword in needed_keywords:
                keywords.add(keyword)
        products_sorted = sorted(products, key=lambda k: float(k['price']))
        if list(keywords) == needed_keywords and process:
            dictio[shop] = []
            for product in products_sorted:
                if dictio[shop] == [] and product['keyword'] in needed_keywords:
                    dictio[shop].append(product)
                    needed_keywords.remove(product['keyword'])
                else:
                    for bproduct in dictio[shop]:
                        if product['keyword'] not in bproduct.values() and product['keyword'] in needed_keywords:
                            dictio[shop].append(product)
                            process = False
                            needed_keywords.remove(product['keyword'])
        elif needed_keywords != []:
            for keyword in list(keywords):
                if keyword in needed_keywords:
                    dictio[shop] = []
                    for product in products_sorted:
                        if dictio[shop] == [] and product['keyword'] in needed_keywords:
                            dictio[shop].append(product)
                            needed_keywords.remove(keyword)
                        else:
                            for bproduct in dictio[shop]:
                                if product['keyword'] not in bproduct.values() and product['keyword'] in needed_keywords:
                                    dictio[shop].append(product)
                                    needed_keywords.remove(keyword)

    for shop in dictio.keys():
        if dictio[shop] != []:
            final[shop] = dictio[shop]
    return final


    #
    #     products_sorted = sorted(products, key=lambda k: float(k['price']))
    #     keywords = []
    #     _products = []
    #     for product in products_sorted:
    #         keyword = product['keyword']
    #         keywords.append(keyword)
    #
    #     if needed_keywords in keywords:
    #         for product in products_sorted:
    #             present = False
    #             for bproduct in _products:
    #                 if keyword in bproduct.values() or keyword not in needed_keywords:
    #                     present = True
    #             if present:
    #                 continue
    #             _products.append(product)
    #         dictio[shop] = _products
    #     break