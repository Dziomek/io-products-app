import re
import unittest

# This class build as Singleton has all the methods responsible for different sorting types
class ProductsOrganizer:

    # This method sorts the products by price or summarized depending on delivery_price flag
    @staticmethod
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


if __name__ == '__main__':
    unittest.main()