import re
import unittest

# This class build as Singleton has all the methods responsible for different sorting types
class ProductsOrganizer:

    # This method sorts the products by price or summarized depending on delivery_price flag
    @staticmethod
    def products_sorting(products, delivery_price, keyword):
        proper_products = []
        for product in products:
            price = product['price']
            product['price'] = price.replace(',', '.')
            if product['deliveryprice'] != '':
                proper_products.append(product)
        if not delivery_price:
            products_sorted = sorted(products, key=lambda k: float(k['price']))
        else:
            products_sorted = sorted(proper_products, key=lambda k: float(k['price']) + float(k['deliveryprice']))

        if len(keyword.split()) == 1:
            for product in products_sorted:
                pattern = re.search(keyword.lower(), product['name'].lower())
                if pattern == None:
                    products_sorted.remove(product)
        return products_sorted

    # This method executes proper formatting of data
    @staticmethod
    def extract_products(data):
        nested_lists = list(data.values())
        flat_list = [item for sub_list in nested_lists for item in sub_list]
        return flat_list

    # This method groups all products by same shops
    @staticmethod
    def group_by_shop(products):
        groups = {}
        for product in products:
            shop_name = product['shop name']
            if shop_name not in groups:
                groups[shop_name] = []
            groups[shop_name].append(product)
        return groups

    # This method takes products grouped by shops and finds the shop with the most products for different keywords
    @staticmethod
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

    # This method takes products grouped by shops and finds the shops with products for remaining keywords
    @staticmethod
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
                                    if product['keyword'] not in bproduct.values() and product[
                                        'keyword'] in needed_keywords:
                                        dictio[shop].append(product)
                                        needed_keywords.remove(keyword)
        for shop in dictio.keys():
            if dictio[shop] != []:
                final[shop] = dictio[shop]
        return final


class TestProductsOrganizer(unittest.TestCase):

    def test_products_sorting(self):
        # Test case where delivery_price is not provided
        products = [{'name': 'product1', 'price': '10.0', 'deliveryprice': '5.0'},
                    {'name': 'product2', 'price': '15.0', 'deliveryprice': ''},
                    {'name': 'product3', 'price': '20.0', 'deliveryprice': '3.0'}]
        result = ProductsOrganizer.products_sorting(products, None, 'product')
        expected_result = [{'name': 'product1', 'price': '10.0', 'deliveryprice': '5.0'},
                           {'name': 'product3', 'price': '20.0', 'deliveryprice': '3.0'}]
        self.assertEqual(result, expected_result)

        # Test case where delivery_price is provided
        products = [{'name': 'product1', 'price': '10.0', 'deliveryprice': '5.0'},
                    {'name': 'product2', 'price': '15.0', 'deliveryprice': ''},
                    {'name': 'product3', 'price': '20.0', 'deliveryprice': '3.0'}]
        result = ProductsOrganizer.products_sorting(products, True, 'product')
        expected_result = [{'name': 'product1', 'price': '10.0', 'deliveryprice': '5.0'},
                           {'name': 'product3', 'price': '20.0', 'deliveryprice': '3.0'}]
        self.assertEqual(result, expected_result)

    def test_group_by_shop(self):
        # Test data
        products = [
            {'shop name': 'Shop A', 'product name': 'product 1'},
            {'shop name': 'Shop B', 'product name': 'product 2'},
            {'shop name': 'Shop A', 'product name': 'product 3'},
            {'shop name': 'Shop B', 'product name': 'product 4'},
            {'shop name': 'Shop C', 'product name': 'product 5'},
        ]
        # Expected result
        expected_result = {
            'Shop A': [
                {'shop name': 'Shop A', 'product name': 'product 1'},
                {'shop name': 'Shop A', 'product name': 'product 3'},
            ],
            'Shop B': [
                {'shop name': 'Shop B', 'product name': 'product 2'},
                {'shop name': 'Shop B', 'product name': 'product 4'},
            ],
            'Shop C': [
                {'shop name': 'Shop C', 'product name': 'product 5'},
            ],
        }
        # Call the function and compare the result to the expected result
        result = ProductsOrganizer.group_by_shop(products)
        self.assertEqual(result, expected_result)

    def test_get_best_shop(self):
        grouped_products = {
            'Shop A': [
                {'shop name': 'Shop A', 'product name': 'product 1', 'price': '10.0', 'keyword': 1},
                {'shop name': 'Shop A', 'product name': 'product 3', 'price': '20.0', 'keyword': 3},
                {'shop name': 'Shop A', 'product name': 'product 6', 'price': '30.0', 'keyword': 5},
            ],
            'Shop B': [
                {'shop name': 'Shop B', 'product name': 'product 2', 'price': '40.0', 'keyword': 2},
                {'shop name': 'Shop B', 'product name': 'product 4', 'price': '40.0', 'keyword': 4},
            ],
            'Shop C': [
                {'shop name': 'Shop C', 'product name': 'product 5', 'price': '40.0', 'keyword': 5},
            ]
        }
        counter = 5
        expected_output = ({'Shop A': [{'shop name': 'Shop A', 'product name': 'product 1', "price": "10.0", 'keyword': 1},
                                       {'shop name': 'Shop A', 'product name': 'product 3', "price": "20.0", 'keyword': 3},
                                       {'shop name': 'Shop A', 'product name': 'product 6', "price": "30.0", 'keyword': 5}]},
                           [2, 4])
        self.assertEqual(ProductsOrganizer.get_best_shop(grouped_products, counter), expected_output)

    def test_get_rest_of_products(self):
        grouped_products = {
            'Shop A': [
                {'shop name': 'Shop A', 'product name': 'product 1', 'price': '10.0', 'keyword': 1},
                {'shop name': 'Shop A', 'product name': 'product 3', 'price': '20.0', 'keyword': 3},
                {'shop name': 'Shop A', 'product name': 'product 6', 'price': '30.0', 'keyword': 5},
            ],
            'Shop B': [
                {'shop name': 'Shop B', 'product name': 'product 2', 'price': '40.0', 'keyword': 2},
                {'shop name': 'Shop B', 'product name': 'product 4', 'price': '40.0', 'keyword': 4},
            ],
            'Shop C': [
                {'shop name': 'Shop C', 'product name': 'product 5', 'price': '40.0', 'keyword': 5},
            ]
        }
        (dictio, needed_keywords) = ProductsOrganizer.get_best_shop(grouped_products, 5)
        rest_of_products = ProductsOrganizer.get_rest_of_products(grouped_products, needed_keywords, dictio)
        expected_rest_of_products = {
            'Shop A': [
                {'shop name': 'Shop A', 'product name': 'product 1', 'price': '10.0', 'keyword': 1},
                {'shop name': 'Shop A', 'product name': 'product 3', 'price': '20.0', 'keyword': 3},
                {'shop name': 'Shop A', 'product name': 'product 6', 'price': '30.0', 'keyword': 5},
            ],
            'Shop B': [
                {'shop name': 'Shop B', 'product name': 'product 2', 'price': '40.0', 'keyword': 2},
                {'shop name': 'Shop B', 'product name': 'product 4', 'price': '40.0', 'keyword': 4},
            ]
        }
        self.assertEqual(rest_of_products, expected_rest_of_products)

    def test_extract_products(self):
        data = {'category_1': ['product_1', 'product_2', 'product_3'],
                'category_2': ['product_4', 'product_5']}
        expected_result = ['product_1', 'product_2', 'product_3',
                           'product_4', 'product_5']
        self.assertEqual(ProductsOrganizer.extract_products(data), expected_result)


if __name__ == '__main__':
    unittest.main()
