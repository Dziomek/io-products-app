import json
from datetime import datetime
import re
import time

import requests
from flask import jsonify, request, url_for, session
from . import app
from .database_connector import DatabaseConnector
# from scraping.scraping.spiders.ceneoScraping import ceneoScraping, zdrowieScraping, urodaScraping
from scrapy.crawler import CrawlerProcess

db = DatabaseConnector()

@app.route('/', methods=['GET'])
def hello_world():
    response = jsonify({"data": ["data1", "data2", "data3"]})
    
    return response

@app.route('/scraping', methods=['POST'])
def scraping():
    start = time.time()
    timeout_seconds = 30
    while (time.time() - start < timeout_seconds):
        product_list = request.json.get("productList")
        category = request.json.get("category")
        quantity = request.json.get("quantity")
        allegro = request.json.get('allegro')
        delivery_price = request.json.get('deliveryPrice')

        crawl_args = {
            "keyword_list": product_list,
            "category": category,
            "quantity": quantity,
            "allegro": allegro,
            "deliveryPrice": delivery_price
        }

        crawl_args_json = json.dumps(crawl_args)

        params = {
            'spider_name': "ceneo_search",
            'start_requests': True,
            'crawl_args': crawl_args_json
        }
        try:
            response = requests.get('http://127.0.0.1:9080/crawl.json', params)
            data = json.loads(response.text)
        except Exception as e:
            return {
                "error": True,
                "message": "Scraping request failed. Error occured",
                "errorMessage": str(e)
            }
        try:
            products = data['items']
            for product in products:
                price = product['price']
                product['price'] = price.replace(',', '.')
                if product['deliveryprice'] == '':
                    products.remove(product)
            if not delivery_price:
                products_sorted = sorted(products, key=lambda k: float(k['price']))
            else:
                products_sorted = sorted(products, key=lambda k: float(k['price']) + float(k['deliveryprice']))

            if len(product_list[0].split()) == 1:
                for product in products_sorted:
                    pattern = re.search(product_list[0].lower(), product['name'].lower())
                    if pattern == None:
                        products_sorted.remove(product)

            data['items'] = products_sorted[:10]
            return {
                "message": "Keyword list passed successfully",
                "product_list": data,
                "crawl_args_json": crawl_args_json
            }
        except Exception as e:
            return {
                "error": True,
                "message": "Error occured when sorting output",
                "errorMessage": str(e)
            }
    return {
        "message": "Keyword list passed successfully",
        "timeout": True,
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
