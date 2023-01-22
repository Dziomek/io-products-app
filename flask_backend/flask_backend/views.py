import json
from datetime import datetime

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
    product_list = request.json.get("productList")
    category = request.json.get("category")
    quantity = request.json.get("quantity")
    
    #print(type(product_list))

    crawl_args = {
        "keyword_list": product_list,
        "category": category,
        "quantity": quantity
    }

    crawl_args_json = json.dumps(crawl_args)

    params = {
        'spider_name': "ceneo_search",
        'start_requests': True,
        'crawl_args': crawl_args_json
    }

    response = requests.get('http://127.0.0.1:9080/crawl.json', params)
    data = json.loads(response.text)

    #TODO Sorting

    return {
        "message": "Keyword list passed successfully",
        "product_list": data,
        "crawl_args_json": crawl_args_json
    }


@app.route('/save', methods=['POST'])
def save():
    id = request.json.get('id')
    if id:
        name = request.json.get('product')
        link = request.json.get('link')
        price = request.json.get('price')
        # data = request.json.get("data")
        # print(data)
        #TODO: Process the data
        now = datetime.now()
        #db.insert_into_products_history(user_id=id, name='', link='', price=0.00, timestamp=now.strftime("%Y-%m-%d %H:%M:%S"))
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
            data[str(history[i][6])] = [[product]]
        else:
            data[str(history[i][6])].append(product)
    return {
        "message": "History of requests passed succesfully",
        "history": json.dumps(data)
    }
