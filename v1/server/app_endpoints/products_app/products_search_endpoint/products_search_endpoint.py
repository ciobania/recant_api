#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import make_response, jsonify, g, request
from flask.views import MethodView

from flask_jwt_auth.v1.server.auth.auth_helpers import login_required
from flask_jwt_auth.v1.server.models import Product


class ProductsSearchEndpoint(MethodView):
    # @login_required
    def get(self):
        """
        Scaffolding for GET HTTP request: /products/search
        :return: JSON API response
        """
        search_query = request.args.get("query")
        print(f'request.json:: {search_query}')
        searched_products = Product.query.filter(Product.name.contains(search_query)).all()
        searched_products = [searched_product.as_dict() for searched_product in searched_products]
        return make_response(jsonify({'adrian': searched_products})), 200

    # @login_required
    def post(self):
        """
        Scaffolding for POST HTTP request: /products/search/
        :return: JSON API response
        """
        request_payload = request.get_json()
        name = request_payload.get('name', {})

        return make_response(jsonify(name.as_dict())), 200
