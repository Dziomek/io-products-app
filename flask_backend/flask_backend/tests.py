import re
import ProductsOrganizer


def test_products_sorting(product_organizer):
    # Test case 1: Check if products without delivery price are removed
    products = [{'name': 'product1', 'price': '10.00', 'deliveryprice': ''},
                {'name': 'product2', 'price': '20.00', 'deliveryprice': '5.00'}]
    delivery_price = False
    keyword = ""
    expected_output = [{'name': 'product2', 'price': '20.00', 'deliveryprice': '5.00'}]
    assert products_sorting(products, delivery_price, keyword) == expected_output

    # Test case 2: Check if products are sorted by price
    products = [{'name': 'product1', 'price': '20.00', 'deliveryprice': '5.00'},
                {'name': 'product2', 'price': '10.00', 'deliveryprice': '3.00'}]
    delivery_price = False
    keyword = ""
    expected_output = [{'name': 'product2', 'price': '10.00', 'deliveryprice': '3.00'},
                       {'name': 'product1', 'price': '20.00', 'deliveryprice': '5.00'}]
    assert products_sorting(products, delivery_price, keyword) == expected_output

    # Test case 3: Check if products are sorted by price + delivery price
    products = [{'name': 'product1', 'price': '20.00', 'deliveryprice': '5.00'},
                {'name': 'product2', 'price': '10.00', 'deliveryprice': '3.00'}]
    delivery_price = True
    keyword = ""
    expected_output = [{'name': 'product2', 'price': '10.00', 'deliveryprice': '3.00'},
                       {'name': 'product1', 'price': '20.00', 'deliveryprice': '5.00'}]
    assert products_sorting(products, delivery_price, keyword) == expected_output

    # Test case 4: Check if only products containing keyword are returned
    products = [{'name': 'product1', 'price': '20.00', 'deliveryprice': '5.00'},
                {'name': 'product2', 'price': '10.00', 'deliveryprice': '3.00'},
                {'name': 'product3', 'price': '15.00', 'deliveryprice': '2.00'}]
    delivery_price = False
    keyword = "product2"
    expected_output = [{'name': 'product2', 'price': '10.00', 'deliveryprice': '3.00'}]
    assert products_sorting(products, delivery_price, keyword) == expected_output

if __name__ == '__main__':
    products_organizer = ProductsOrganizer
    test_products_sorting(products_organizer)