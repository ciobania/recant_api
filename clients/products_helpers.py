#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask_jwt_auth.clients.request_helpers import RequestHelpers


class ProductsHelpers:
    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        self.rh = RequestHelpers(self.client)

    def get_all_products(self):
        data = self.rh.request('/api/products',
                               'get')
        return data

    def create_product(self, payload):
        data = self.rh.request('/api/products',
                               'post',
                               payload=payload)

        return data

    def update_product(self, product_id, payload):
        data = self.rh.request('/api/products/{}'.format(product_id),
                               'post',
                               payload=payload)

        return data

    def delete_grocery_list(self, product_id):
        data = self.rh.request('/api/products/{}'.format(product_id),
                               'delete')

        return data
