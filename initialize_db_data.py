#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
import requests

from clients.products_helpers import ProductsHelpers

url = 'http://localhost:5001/api/products'
all_products = requests.get(url).json()

for product in all_products:
    product_payload = {'name': product['product']['title'],
                       'description': product['product']['shortDescription'],
                       'brand_name': product['product']['brandName'],
                       'gtin': product['product']['gtin'],
                       'status': product['product']['status'],
                       'price': int(product['product']['price']/100),
                       'unit_price': int(product['product']['unitPrice']/100),
                       'unit_of_measure': product['product']['unitOfMeasure']}
    new_product = requests.post(url, json=product_payload).json()
    print(new_product)

print(f'{all_products=}')
