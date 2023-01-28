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

    shops = False

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
        products_for_shop_sorting = products_for_shop_sorting + products
        print(len(products_for_shop_sorting))
        print(counter)
        if counter == iterations:
            dupa = sort_products_by_shop(products_for_shop_sorting)
            print(dupa)
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


def sort_products_by_shop(products_list):
    # Create a dictionary to store the products for each keyword
    products_by_keyword = {}

    # Iterate through the products in the list
    for product in products_list:
        keyword = product["keyword"]
        if keyword not in products_by_keyword:
            products_by_keyword[keyword] = []

        products_by_keyword[keyword].append(product)

    # Create a list to store the final products
    final_products = []

    # Iterate through the products for each keyword
    for keyword, keyword_products in products_by_keyword.items():
        # Create a dictionary to store the shop names and the products for each shop
        shop_products = {}

        # Iterate through the products for the current keyword
        for product in keyword_products:
            shop_name = product["shop name"]
            if shop_name == '':
                continue
            if shop_name not in shop_products:
                shop_products[shop_name] = []

            shop_products[shop_name].append(product)

        # Get the shop with the most products for the current keyword
        max_shop_name = max(shop_products, key=lambda x: len(shop_products[x]))

        # Get the first product from the shop with the most products
        final_product = shop_products[max_shop_name][0]

        # Add the final product to the final list
        final_products.append(final_product)

    return final_products


