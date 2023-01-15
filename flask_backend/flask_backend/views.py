import json
import requests
from flask import jsonify, request, url_for
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
    quantity = request.json.get("quantity")
    
    print(type(product_list))

    crawl_args = {
        "keyword_list": product_list,
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

    return {
        "message": "Keyword list passed successfully",
        "product_list": data,
        "crawl_args_json": crawl_args_json
    }
